# 🐛 Bug Diagnosis: Sequence Mismatch Issue

## Problem Description

When opening the visualizer from the GUI, the initial and final sequences shown in the HTML don't match what was displayed in the GUI.

## Root Cause

The issue is in the training loop. Here's what happens:

### Current Flow (BROKEN)

```
1. GUI creates environment
   → env.sequence = "ACGTACGT..." (random)
   
2. GUI stores initial sequence
   → self.initial_sequence = "ACGTACGT..."
   → GUI displays: "Initial seq: ACGTACGT..."
   
3. Training starts with env.reset() INSIDE the loop
   → Episode 0: env.reset() → NEW sequence "TGCATGCA..."
   → Episode 1: env.reset() → NEW sequence "GGGGCCCC..."
   → Episode 2: env.reset() → NEW sequence "ATATAGGG..."
   → ... (200 episodes, each with different sequence)
   → Episode 199: env.reset() → NEW sequence "CCCCAAAA..."
   
4. Training ends
   → env.sequence = "CCCCAAAA..." (from LAST episode)
   → GUI displays: "Final seq: CCCCAAAA..."
   
5. User clicks "Open Visualizer"
   → initial = "ACGTACGT..." (stored from step 2)
   → target = "CCCCAAAA..." (current env.sequence from step 4)
   → These are UNRELATED sequences!
```

### The Bug

The `train()` function calls `env.reset()` at the start of EACH episode, generating a new random sequence. This means:

- The initial sequence the GUI shows is from episode 0 (before training)
- The final sequence the GUI shows is from episode 199 (last episode)
- **These two sequences are completely unrelated!**

### Code Location

**File**: `rl_model/train.py`
```python
def train(episodes=200, seq_len=20, max_edits=10, env=None):
    env = env or SequenceEnv(seq_len=seq_len, max_edits=max_edits)
    agent = ReinforceAgent(seq_len=seq_len)

    for ep in range(episodes):
        obs = env.reset()  # ← BUG: Generates new sequence each time!
        # ... training logic ...
```

## Solutions

### Option 1: Single Episode Mode (Simplest)

Make the visualizer show a SINGLE transformation episode instead of multiple training episodes.

**Pros:**
- Simplest fix
- Shows actual transformation of one sequence
- Makes sense for visualization

**Cons:**
- Doesn't show the trained agent's performance
- Only one episode

**Implementation:**
```python
# After training, run ONE more episode to demonstrate
def demonstrate(agent, env, initial_sequence):
    """Run one episode to show transformation of a specific sequence."""
    # Set the sequence manually
    env.sequence = initial_sequence
    env.steps = 0
    env.history = []
    
    # Run the trained agent
    obs = env.sequence
    done = False
    while not done:
        action, _ = agent.select_action(obs)
        env_action = agent.action_to_env(action)
        obs, _, done, info = env.step(env_action)
    
    return env.sequence  # This is the final transformed sequence
```

### Option 2: Track First and Last Episode (Current Debug Approach)

Store the initial sequence from the first episode and use it as the "initial" sequence.

**Pros:**
- Shows the training process
- Easy to implement

**Cons:**
- "Initial" and "final" are from different episodes
- Doesn't show a true transformation

**Implementation:**
```python
def train(episodes=200, seq_len=20, max_edits=10, env=None):
    env = env or SequenceEnv(seq_len=seq_len, max_edits=max_edits)
    agent = ReinforceAgent(seq_len=seq_len)
    
    # Store first episode's initial sequence
    first_sequence = env.sequence
    
    for ep in range(episodes):
        obs = env.reset()
        # ... training ...
    
    # Return both sequences
    return agent, env, first_sequence, env.sequence
```

### Option 3: Fixed Target Mode (Best for RL)

Instead of random sequences, train towards a FIXED target sequence.

**Pros:**
- Shows true transformation: initial → target
- Makes sense for RL (learn to reach a goal)
- Visualizer shows the actual learning goal

**Cons:**
- Requires changing the reward model
- More complex implementation

**Implementation:**
```python
class SequenceEnv:
    def __init__(self, seq_len=20, max_edits=10, fixed_initial=None, fixed_target=None):
        self.seq_len = seq_len
        self.max_edits = max_edits
        self.fixed_initial = fixed_initial
        self.fixed_target = fixed_target
        self.reset()
    
    def reset(self):
        if self.fixed_initial:
            self.sequence = self.fixed_initial
        else:
            self.sequence = "".join(random.choices(self.BASES, k=self.seq_len))
        self.steps = 0
        self.history = []
        return self._get_obs()
```

## Recommended Solution

**Use Option 1: Single Episode Demonstration Mode**

This is the best fit for your visualizer because:
1. It shows a clear transformation: A → B
2. It demonstrates what the trained agent can do
3. It's simple to implement and understand
4. It matches user expectations (see one sequence transform into another)

### Implementation Plan

1. After training completes, run ONE demonstration episode
2. Use the stored initial sequence
3. Let the trained agent transform it
4. Pass both to the visualizer

## Testing the Current State

Run the GUI and check the terminal output. You should see:

```
[DEBUG] Training starting with initial sequence: ACGTACGT...
Episode   0: final_seq=TGCATGCA... reward=...
Episode  10: final_seq=GGGGCCCC... reward=...
...
[DEBUG] Training finished:
  Initial sequence was: ACGTACGT...
  Final sequence is:    CCCCAAAA...
  Sequences match: False

[DEBUG] Opening visualizer:
  Initial (stored): ACGTACGT...
  Final (current):  CCCCAAAA...
  Match: False
```

This confirms the sequences are unrelated.

## Next Steps

1. ✅ Added debug logging to confirm the issue
2. ⬜ Decide which solution to implement
3. ⬜ Implement the chosen solution
4. ⬜ Test the visualizer shows correct transformation
5. ⬜ Remove debug logging (or keep for troubleshooting)

Would you like me to implement Option 1 (demonstration mode)?

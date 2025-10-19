import random
import numpy as np

class SequenceEnv:
    """A minimal sequence-editing environment.

    Observation: current sequence as a string.
    Action: (pos, base) where base in {A,C,G,T} and pos is index.
    Episode ends after max_edits steps or when the agent emits a noop.
    """

    BASES = ["A", "C", "G", "T"]

    def __init__(self, target_ft="AAAAA", target_tfl1="TTTTT", seq_len=20, max_edits=10):
        self.seq_len = seq_len
        self.max_edits = max_edits
        self.target_ft = target_ft
        self.target_tfl1 = target_tfl1
        self.reset()

    def reset(self):
        # start with a random sequence
        self.sequence = "".join(random.choices(self.BASES, k=self.seq_len))
        self.steps = 0
        self.history = []
        return self._get_obs()

    def _get_obs(self):
        return self.sequence

    def step(self, action):
        """Apply action and return obs, reward, done, info.

        action: tuple (pos, base) or None for noop
        """
        if action is None:
            done = True
            reward = 0.0
            info = {"reason": "noop"}
            return self._get_obs(), reward, done, info

        pos, base = action
        pos = int(pos)
        base = str(base)
        old = self.sequence
        if pos < 0 or pos >= self.seq_len or base not in self.BASES:
            raise ValueError("Invalid action")

        if old[pos] != base:
            seq_list = list(old)
            seq_list[pos] = base
            self.sequence = "".join(seq_list)
            self.history.append((pos, base))

        self.steps += 1
        done = self.steps >= self.max_edits
        reward = 0.0  # reward is computed externally by a reward model
        info = {}
        return self._get_obs(), reward, done, info

    def render(self):
        print(f"seq={self.sequence} steps={self.steps}")

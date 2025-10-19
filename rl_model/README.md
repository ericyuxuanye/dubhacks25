# rl_model (BloomSync AI toy)

This folder contains a small, safe, abstract reinforcement learning toy that
demonstrates sequence-editing with a simple reward model. It's intended for
educational/demo purposes and does not provide any wet-lab actionable advice.

Files:
- `env.py`: Sequence editing environment.
- `reward_model.py`: Simulated reward function (k-mer and motif based).
- `agent.py`: Small PyTorch REINFORCE agent.
- `train.py`: Training loop.
- `run_demo.py`: Short demo runner.
- `tests/test_env.py`: Basic smoke tests.

Architecture (mapping to PlantUML):

The project architecture follows the BloomSync AI RL sketch. Below is a
concise mapping of PlantUML components to the package modules:

- RL Agent:
	- Encoder: `encoder.SimpleEncoder` (toy embedding)
	- Policy Head: `agent.PolicyNet` + softmax
	- Value Head: `value.ValueHead` (optional)

- Environment (`env.SequenceEnv`): sequence simulator (apply edit/stop)

- Scorers (`scorers.py`): ft_similarity, tfl1_similarity, motif_validator

- Constraint Engine (`constraints.py`): enforce_budget, allowed_positions_mask

- Reward Model (`reward_model.py`): compute_reward combining scorers and constraints

PlantUML source (for reference):

```
@startuml
skinparam componentStyle rectangle
skinparam shadowing false
skinparam wrapWidth 200
title BloomSync AI – RL Architecture (Flowering Edit Design)

node "RL Agent" as AG {
	component "Encoder\n(CNN/BiLSTM or Transformer)" as ENC
	component "Policy Head\nπ(a|s)" as POL
	component "Value Head\nV(s)" as VAL
}

node "Environment" as ENV {
	component "Sequence Simulator\n(apply edit → seq')" as SIM
	component "Scorers" as SCO {
		[FT/TFL1 Similarity\n(aligner or embedder)]
		[Motif Validator\n(PEBP loop, no STOP)]
		[gRNA Feasibility\n(PAM, GC, length)]
	}
	component "Constraint Engine\n(length, budget, masks)" as CONS
	component "Reward Model\n(learned DNN)" as REW
}

cloud "Reference Bank" as REF {
	[AtFT, AtTFL1]
	[SFT/SP, FvFT1/FvTFL1] 
}

database "Data Sources" as DS {
	[NCBI]
	[UniProt]
	[GDR]
}

AG -down-> ENV : action a_t
ENV -down-> SIM : apply edit/stop
SIM -right-> SCO : seq'
SCO -right-> CONS : flags/masks
SCO -down-> REW : features
CONS -down-> REW : constraints
REW -left-> AG : reward r_t
ENV -left-> AG : state s_{t+1}
REF -[dotted]-> SCO
DS -[dotted]-> ENV : annotations/GO
@enduml
```

Note: the codebase provides high-level, non-actionable placeholders for the
components in this diagram. If you want, I can progressively replace the
placeholders with richer, testable implementations (encoder variations,
learned reward network, or Gym API compatibility).

Run a short demo:

```fish
python -m rl_model.run_demo
```

Graphical demo (Tkinter)

```fish
python -m rl_model.gui
```

This will open a small window with a "Start Training" button and a simulated
progress bar. The underlying toy training still runs in the background.

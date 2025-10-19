# BloomSync AI — dubhacks25

This repository contains a small, self-contained reinforcement learning (RL)
toy and a simple GUI demo. It's intended for educational and demo purposes
only — it does not provide wet-lab instructions or actionable biological
protocols.

Contents
- `rl_model/`: RL toy implementation (environment, agent, reward model,
  training loop, and a Tkinter GUI demo).
- data files used for demos: `flowering_genes.csv`, `flowering_genes_with_fasta.csv`.

Highlights
- A minimal sequence-editing environment (`SequenceEnv`) that accepts edits
  and ends episodes after a budgeted number of edits.
- A small REINFORCE agent implemented in `rl_model/agent.py` and training loop
  in `rl_model/train.py`.
- A Tkinter GUI demo (`rl_model/gui.py`) that runs training in a background
  thread and shows a simulated progress bar. The GUI now includes an
  Objectives panel (checkboxes + presets) so users can select optimization
  goals for demonstration.

Quickstart

1. Create a Python environment (recommended: conda or venv) with Python 3.10+.

2. Install dependencies listed in `rl_model/requirements.txt`:

```fish
conda activate <env>
pip install -r rl_model/requirements.txt
```

3. Run the short demo (console):

```fish
python -m rl_model.run_demo
```

4. Run the GUI demo:

```fish
python -m rl_model.gui
```

Using the GUI Objectives
- The GUI provides checkboxes for these objectives (any combination allowed):
  - Cause flowers / fruit on new wood
  - Change wood strength for single-wire training
  - Change height to facilitate picking
  - Concentrate fruit zone for efficient picking
- A preset combobox lets you quickly pick common combinations (All, None,
  or single-objective presets). Selections are attached to the environment as
  `env.objectives` for demonstration; the training loop behavior is unchanged
  unless you choose to wire the objectives into the reward model.

Development notes
- Tests: `rl_model/tests/test_env.py` includes smoke tests for `SequenceEnv`.
- To add objective-aware training, update `rl_model/reward_model.py` to
  consider `env.objectives` when computing rewards.

License & safety
- This is a demo project. The code is explicitly non-actionable with
  respect to biological protocols. Treat it as a pedagogical example only.

If you want a tailored README section (e.g., for a talk or hackathon
poster), tell me which audience and I'll generate a short version.

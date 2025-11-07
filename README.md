# BloomSync AI

BloomSync AI is a compact reinforcement-learning toy built for demos: a
REINFORCE agent edits a short MdTFL1a fragment toward an MdFT1-like target,
then pipes the result into a WebGL visualizer so you can narrate the “before →
after” story without touching real lab workflows.

## Safety & intent
- Ships only synthetic, length-matched fragments and motif scores.
- No code describes or executes wet-lab procedures.
- Purpose: UI/UX storytelling, hackathon pitches, and pedagogy.

## Setup
1. Install Python 3.10+ and create a virtual environment.
2. `pip install -r rl_model/requirements.txt`

## Run the demos
- RL console trace: `python3 -m rl_model.run_demo`
- GUI + objectives + visualizer launcher: `python3 -m rl_model.gui`
- Menu with shortcuts/tests: `python3 demo.py`
- Standalone visualizer sanity check: `python3 test_visualizer_params.py`
- Smoke tests: `python3 -m pytest rl_model/tests/test_env.py`

## Visualizer flow (GUI button)
```
SequenceEnv reset (curated MdTFL1→MdFT1 case)
        ↓
Background REINFORCE training with shaped reward
        ↓
GUI enables “🧬 Open Visualizer” and starts a tiny HTTP server
        ↓
Browser opens http://localhost:PORT/sequence_transformation_viz.html
        ↓
JavaScript reads ?initial=...&target=... and animates the edits
```

## Repo highlights
- `rl_model/sample_sequences.py` – curated demo case + motifs.
- `rl_model/env.py` – deterministic environment with noisy resets + edit log.
- `rl_model/reward_model.py` – FT vs TFL1 k-mer overlap, motif boosts, edit cost.
- `rl_model/train.py` – REINFORCE loop returning a reward trace for the UI.
- `rl_model/gui.py` – Tkinter front-end, objectives panel, browser launcher.
- `sequence_transformation_viz.html` – WebGL helix with play/step/reset controls.
- `demo.py` & `test_*.py` – CLI helpers for demos and integration smoke tests.

## Extending the toy
- Add new curated fragments in `sample_sequences.py` and pass `case_id=` to the
  env or GUI.
- Wire GUI objective selections into `reward_model.compute_reward` for custom
  scoring.
- Swap the heuristic reward with a learned scorer while keeping the same demo UX.

---

Treat BloomSync AI as narrative scaffolding—safe to show, fun to tweak, and
decoupled from real experimentation. Have fun telling the story! 🎬🧬

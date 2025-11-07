"""Run a short training/demo and generate a 3D visualization of input and
output sequences using rl_model.visualize.

This script is intended for local debugging and demo generation.
"""

from rl_model import train
from rl_model.sample_sequences import get_case
from rl_model.visualize import animate_edit_history


def run_and_visualize(out_html="visual_demo.html", episodes=30, max_edits=8):
    # create env and run the short training to get an agent and env
    case = get_case()
    agent, env, _ = train.train(episodes=episodes, max_edits=max_edits, case_id=case.case_id)

    # We will produce a visualization from env.history if present
    # SequenceEnv records edits into env.history during demo runs.
    initial = env.history[0][2] if False else None

    # More reliably: reset a new env, capture initial seq, run the trained agent
    from rl_model.env import SequenceEnv
    e = SequenceEnv(max_edits=max_edits, case_id=case.case_id)
    init_seq = e.sequence
    edits = []
    done = False
    steps = 0
    # run the agent until done
    while not done and steps < max_edits:
        action, _ = agent.select_action(e.sequence)
        env_action = agent.action_to_env(action)
        obs, _, done, info = e.step(env_action)
        if env_action is not None:
            edits.append(env_action)
        steps += 1

    # edits is a list of (pos, base) tuples; animate
    animate_edit_history(init_seq, edits, out_html=out_html)


if __name__ == "__main__":
    run_and_visualize()

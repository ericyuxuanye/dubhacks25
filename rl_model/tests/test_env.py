import pytest

from rl_model.env import SequenceEnv
from rl_model.reward_model import compute_reward


def test_env_step_and_reward():
    env = SequenceEnv(seq_len=10, max_edits=5)
    seq = env.reset()
    assert len(seq) == 10
    obs, _, done, _ = env.step((0, "A"))
    assert len(obs) == 10
    # compute reward doesn't crash
    r = compute_reward(env.sequence, env.target_ft, env.target_tfl1, n_edits=1)
    assert isinstance(r, float)


def test_env_defaults_to_demo_case():
    env = SequenceEnv(max_edits=4)
    seq = env.reset()
    assert env.case is not None
    assert len(seq) == len(env.target_ft) == len(env.target_tfl1)

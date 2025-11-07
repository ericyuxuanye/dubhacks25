from .env import SequenceEnv
from .agent import ReinforceAgent
from .reward_model import compute_reward
import time
from typing import List, Optional, Tuple


def train(
    episodes: int = 200,
    seq_len: Optional[int] = None,
    max_edits: int = 10,
    env: Optional[SequenceEnv] = None,
    case_id: Optional[str] = None,
) -> Tuple[ReinforceAgent, SequenceEnv, List[float]]:
    """Run training and return the agent, final env, and reward trace."""
    env = env or SequenceEnv(seq_len=seq_len, max_edits=max_edits, case_id=case_id)
    agent = ReinforceAgent(seq_len=env.seq_len)
    episode_scores: List[float] = []
    motifs = env.case.motifs if env.case else None

    for ep in range(episodes):
        obs = env.reset()
        log_probs = []
        rewards = []
        n_edits = 0
        done = False
        prev_score = compute_reward(
            env.sequence, env.target_ft, env.target_tfl1, n_edits, motifs=motifs
        )

        while not done:
            action, lp = agent.select_action(obs)
            env_action = agent.action_to_env(action)
            obs, _, done, _ = env.step(env_action)
            if env_action is not None:
                n_edits += 1
            current_score = compute_reward(
                env.sequence, env.target_ft, env.target_tfl1, n_edits, motifs=motifs
            )
            shaped_reward = current_score - prev_score
            prev_score = current_score
            log_probs.append(lp)
            rewards.append(shaped_reward)

        # small push to ensure we keep learning even if only noop happened
        if not rewards:
            rewards = [prev_score]

        agent.update(log_probs, rewards)
        episode_scores.append(prev_score)
        if ep % 20 == 0:
            print(
                f"Episode {ep:3d}: reward={prev_score:+.4f} edits={n_edits} seq={env.sequence}"
            )
        time.sleep(0.01)

    return agent, env, episode_scores


if __name__ == "__main__":
    train(episodes=30)

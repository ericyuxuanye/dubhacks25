import random
from .env import SequenceEnv
from .agent import ReinforceAgent
from .reward_model import compute_reward

def train(episodes=50, seq_len=20, max_edits=10):
    env = SequenceEnv(seq_len=seq_len, max_edits=max_edits)
    agent = ReinforceAgent(seq_len=seq_len)

    for ep in range(episodes):
        obs = env.reset()
        log_probs = []
        rewards = []
        n_edits = 0
        done = False
        while not done:
            action, lp = agent.select_action(obs)
            env_action = agent.action_to_env(action)
            obs, _, done, info = env.step(env_action)
            if env_action is not None:
                n_edits += 1
            # compute immediate reward with current seq
            r = compute_reward(env.sequence, env.target_ft, env.target_tfl1, n_edits)
            log_probs.append(lp)
            rewards.append(r)

        agent.update(log_probs, rewards)
        if ep % 10 == 0:
            print(f"Episode {ep:3d}: final_seq={env.sequence} reward={rewards[-1]:.4f}")

    return agent, env


if __name__ == "__main__":
    train(episodes=30)

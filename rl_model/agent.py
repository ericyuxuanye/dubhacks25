import torch
import torch.nn as nn
import torch.optim as optim
import random

from .env import SequenceEnv


class PolicyNet(nn.Module):
    def __init__(self, seq_len, n_actions):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(seq_len * 4, 128),
            nn.ReLU(),
            nn.Linear(128, n_actions),
        )

    def forward(self, x):
        return self.fc(x)


class ReinforceAgent:
    """Very small REINFORCE agent.

    Actions are flattened: pos * 4 + base_idx, plus one noop action at the end.
    """

    def __init__(self, seq_len, lr=1e-3):
        self.seq_len = seq_len
        self.n_bases = 4
        self.n_actions = seq_len * self.n_bases + 1
        self.policy = PolicyNet(seq_len, self.n_actions)
        self.optimizer = optim.Adam(self.policy.parameters(), lr=lr)

    def encode_seq(self, seq):
        # one-hot encoding
        mapping = {"A":0, "C":1, "G":2, "T":3}
        arr = torch.zeros(self.seq_len, 4)
        for i, ch in enumerate(seq):
            arr[i, mapping.get(ch,0)] = 1.0
        return arr.view(-1)

    def select_action(self, seq):
        x = self.encode_seq(seq).unsqueeze(0)
        logits = self.policy(x)
        probs = torch.softmax(logits, dim=-1)
        m = torch.distributions.Categorical(probs)
        a = m.sample()
        return int(a.item()), m.log_prob(a)

    def action_to_env(self, action):
        if action == self.n_actions - 1:
            return None
        pos = action // self.n_bases
        base_idx = action % self.n_bases
        base = ["A","C","G","T"][base_idx]
        return (pos, base)

    def update(self, log_probs, rewards, gamma=0.99):
        # compute discounted returns
        R = 0
        returns = []
        for r in reversed(rewards):
            R = r + gamma * R
            returns.insert(0, R)
        returns = torch.tensor(returns)

        returns = (returns - returns.mean()) / (returns.std() + 1e-8)
        
        loss = 0
        for lp, R in zip(log_probs, returns):
            loss = loss - lp * R

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

"""Encoder module (safe placeholder).

Provides a small embedding encoder interface used by the RL agent. This is a
toy implementation (one-hot + linear) for experiments and demos only.
"""

import torch
import torch.nn as nn


class SimpleEncoder(nn.Module):
    def __init__(self, seq_len, emb_dim=32):
        super().__init__()
        self.seq_len = seq_len
        self.emb_dim = emb_dim
        self.fc = nn.Sequential(
            nn.Linear(seq_len * 4, emb_dim),
            nn.ReLU(),
        )

    def forward(self, x):
        return self.fc(x)

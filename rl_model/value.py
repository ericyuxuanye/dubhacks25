"""Value head placeholder.

Provides a minimal value network to estimate V(s) from encoder features.
"""

import torch
import torch.nn as nn


class ValueHead(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
        )

    def forward(self, x):
        return self.net(x).squeeze(-1)

import random
from typing import List, Optional

from .sample_sequences import DemoCase, get_case


class SequenceEnv:
    """A minimal sequence-editing environment backed by curated demo data.

    Observation: current sequence as a string.
    Action: (pos, base) where base is part of the alphabet (default DNA).
    Episode ends after max_edits steps or when the agent emits a noop.
    """

    BASES = ["A", "C", "G", "T"]

    def __init__(
        self,
        target_ft: Optional[str] = None,
        target_tfl1: Optional[str] = None,
        seq_len: Optional[int] = None,
        max_edits: int = 10,
        start_sequence: Optional[str] = None,
        noise_prob: float = 0.1,
        case_id: Optional[str] = None,
        alphabet: Optional[List[str]] = None,
    ):
        self.max_edits = max_edits
        self.noise_prob = noise_prob
        self.alphabet = alphabet or self.BASES
        self.case: Optional[DemoCase] = None

        if seq_len is None and (target_ft is None or target_tfl1 is None or start_sequence is None):
            self.case = get_case(case_id or "mdtfl1_to_mdft1")
            target_ft = self.case.target_sequence
            target_tfl1 = self.case.avoid_sequence
            start_sequence = self.case.initial_sequence
            seq_len = len(start_sequence)
        else:
            seq_len = seq_len or (len(start_sequence) if start_sequence else None)
            if seq_len is None:
                raise ValueError("seq_len or start_sequence must be provided for ad-hoc envs")
            target_ft = target_ft or self._random_sequence(seq_len)
            target_tfl1 = target_tfl1 or self._random_sequence(seq_len)
            start_sequence = start_sequence or self._random_sequence(seq_len)

        if len(start_sequence) != seq_len:
            raise ValueError("start_sequence length must match seq_len")
        if len(target_ft) != seq_len or len(target_tfl1) != seq_len:
            raise ValueError("target sequences must match seq_len")

        self.seq_len = seq_len
        self.target_ft = target_ft
        self.target_tfl1 = target_tfl1
        self.start_sequence = start_sequence
        self.sequence = start_sequence
        self.initial_sequence = start_sequence
        self.history = []
        self.steps = 0

        self.reset()

    def _random_sequence(self, length: int) -> str:
        return "".join(random.choices(self.alphabet, k=length))

    def _mutate_sequence(self, sequence: str, prob: float) -> str:
        seq_list = list(sequence)
        for idx, base in enumerate(seq_list):
            if random.random() < prob:
                choices = [b for b in self.alphabet if b != base]
                seq_list[idx] = random.choice(choices)
        return "".join(seq_list)

    def reset(self):
        # start near the curated sequence with a bit of noise for variability
        self.sequence = self._mutate_sequence(self.start_sequence, self.noise_prob)
        self.initial_sequence = self.sequence
        self.steps = 0
        self.history = []
        return self._get_obs()

    def _get_obs(self):
        return self.sequence

    def step(self, action):
        """Apply action and return obs, reward, done, info."""
        if action is None:
            done = True
            reward = 0.0
            info = {"reason": "noop"}
            return self._get_obs(), reward, done, info

        pos, base = action
        pos = int(pos)
        base = str(base)
        old = self.sequence
        if pos < 0 or pos >= self.seq_len or base not in self.alphabet:
            raise ValueError("Invalid action")

        if old[pos] != base:
            seq_list = list(old)
            prev_base = seq_list[pos]
            seq_list[pos] = base
            self.sequence = "".join(seq_list)
            self.history.append({"step": self.steps, "pos": pos, "from": prev_base, "to": base})

        self.steps += 1
        done = self.steps >= self.max_edits
        reward = 0.0  # reward is computed externally by a reward model
        info = {}
        return self._get_obs(), reward, done, info

    def render(self):
        print(f"seq={self.sequence} steps={self.steps}")

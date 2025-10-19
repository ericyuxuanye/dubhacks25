"""Constraint engine (toy): budgets, masks, and simple checks.

This module provides safe helper functions for enforcing simple constraints
like max edits, allowed positions, and masks. It does not expose any protocol
for lab work.
"""


def enforce_budget(n_edits, max_edits):
    return n_edits <= max_edits


def allowed_positions_mask(seq_len, forbidden=None):
    mask = [True] * seq_len
    if forbidden:
        for p in forbidden:
            if 0 <= p < seq_len:
                mask[p] = False
    return mask

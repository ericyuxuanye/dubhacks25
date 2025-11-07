"""Curated demo sequences used by the BloomSync RL toy environment.

The repo ships with short, GC-balanced fragments that mimic an edit where an
MdTFL1-like repressor segment is steered toward an MdFT1 flowering locus.
They are synthetic, non-actionable snippets that provide stable data for demos.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class DemoCase:
    case_id: str
    title: str
    description: str
    initial_name: str
    initial_sequence: str
    target_name: str
    target_sequence: str
    avoid_name: str
    avoid_sequence: str
    objectives: List[str]
    motifs: List[str]


# These fragments were constructed to resemble short promoter windows while
# remaining safe-to-share synthetic data for offline demos.
_MDFT1_SEGMENT = "AAGCCCAATAAACCACTCTGACTGGCCGAATAGGGATATAGGCAACGACATGTGCGGCGA"
_MDTFL1_SEGMENT = "AAGGCCAATAGACCTATATGCCTGCCCGATTAGGCGTAAACGCGGCAACATGTGCAGTTA"


DEMO_CASES: Dict[str, DemoCase] = {
    "mdtfl1_to_mdft1": DemoCase(
        case_id="mdtfl1_to_mdft1",
        title="MdTFL1a → MdFT1 flowering boost",
        description=(
            "Start from a MdTFL1-like repressor fragment and edit toward the "
            "flowering MdFT1 motif cluster. Rewarding FT-like k-mers while "
            "penalizing TFL1 motifs produces a meaningful training signal."
        ),
        initial_name="MdTFL1a fragment",
        initial_sequence=_MDTFL1_SEGMENT,
        target_name="MdFT1 promoter fragment",
        target_sequence=_MDFT1_SEGMENT,
        avoid_name="MdTFL1a reference",
        avoid_sequence=_MDTFL1_SEGMENT,
        objectives=[
            "flowers",
            "height",
        ],
        motifs=[
            "AAGCCCA",
            "GACTGG",
            "GGATAT",
        ],
    ),
}


def get_case(case_id: str = "mdtfl1_to_mdft1") -> DemoCase:
    """Return the requested demo case (defaults to the MdTFL1→MdFT1 edit)."""
    try:
        return DEMO_CASES[case_id]
    except KeyError as exc:
        available = ", ".join(sorted(DEMO_CASES))
        raise ValueError(
            f"Unknown demo case '{case_id}'. Available cases: {available}"
        ) from exc


def list_cases() -> List[str]:
    """Return the available case identifiers."""
    return sorted(DEMO_CASES.keys())


__all__ = ["DemoCase", "get_case", "list_cases", "DEMO_CASES"]

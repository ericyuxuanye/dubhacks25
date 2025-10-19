"""Scorers for similarity and motif validation (safe, simulated).

Contains non-actionable placeholder scorers used to compute features for the
reward model. Implementations use simple sequence heuristics (k-mer overlap,
motif presence) and do NOT provide lab guidance.
"""

from .reward_model import kmer_score, motif_value


def ft_similarity(seq, reference, k=3):
    return kmer_score(seq, reference, k=k)


def tfl1_similarity(seq, reference, k=3):
    return kmer_score(seq, reference, k=k)


def motif_validator(seq, motifs=None):
    return motif_value(seq, motifs=motifs)

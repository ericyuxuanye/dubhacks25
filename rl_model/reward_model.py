from collections import Counter
from typing import Iterable, Optional

def kmer_score(seq, target, k=3):
    """Simple k-mer overlap score between seq and target (normalized).

    Returns a score in [0,1].
    """
    if len(seq) < k or len(target) < k:
        return 0.0
    def kmers(s):
        return [s[i:i+k] for i in range(len(s)-k+1)]

    a = Counter(kmers(seq))
    b = Counter(kmers(target))
    inter = sum(min(a[k], b[k]) for k in a.keys() & b.keys())
    denom = max(1, sum(b.values()))
    return inter / denom


def motif_value(seq, motifs=None):
    """Counts presence of known motifs. Returns normalized score."""
    if motifs is None:
        motifs = ["ATG", "TATA", "GATA"]
    count = 0
    for m in motifs:
        if m in seq:
            count += 1
    return count / len(motifs)


def compute_reward(
    seq: str,
    target_ft: str,
    target_tfl1: str,
    n_edits: int,
    *,
    motifs: Optional[Iterable[str]] = None,
    w1: float = 1.0,
    w2: float = 0.9,
    w3: float = 0.4,
    w4: float = 0.6,
) -> float:
    """Compute R = w1*S_FT - w2*S_TFL1 - w3*edit_penalty + w4*V_motifs."""
    s_ft = kmer_score(seq, target_ft, k=4)
    s_tfl1 = kmer_score(seq, target_tfl1, k=4)
    v_m = motif_value(seq, motifs=motifs)
    edit_penalty = n_edits / max(1, len(seq))
    R = w1 * s_ft - w2 * s_tfl1 - w3 * edit_penalty + w4 * v_m
    return float(R)

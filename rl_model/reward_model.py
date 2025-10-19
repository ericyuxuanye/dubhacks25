import math
from collections import Counter

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


def compute_reward(seq, target_ft, target_tfl1, n_edits,
                   w1=1.0, w2=0.8, w3=0.1, w4=0.5):
    """Compute R = w1*S_FT - w2*S_TFL1 - w3*N_edits + w4*V_motifs"""
    s_ft = kmer_score(seq, target_ft)
    s_tfl1 = kmer_score(seq, target_tfl1)
    v_m = motif_value(seq)
    R = w1 * s_ft - w2 * s_tfl1 - w3 * (n_edits) + w4 * v_m
    return float(R)

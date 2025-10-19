def seq_diff(a, b):
    """Return number of differing positions between two sequences of equal length."""
    assert len(a) == len(b)
    return sum(1 for x, y in zip(a, b) if x != y)

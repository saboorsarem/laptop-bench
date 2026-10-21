def chunk(seq, n):
    if n <= 0:
        raise ValueError("n must be positive")
    return [list(seq[i:i + n]) for i in range(0, len(seq), n)]

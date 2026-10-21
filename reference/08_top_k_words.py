import re
from collections import Counter


def top_k_words(text, k):
    counts = Counter(re.findall(r"[a-z0-9]+", text.lower()))
    return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))[:max(k, 0)]

Write `solution.py` containing one function:

```python
def top_k_words(text, k):
    ...
```

Split `text` into words on every character that is not an ASCII letter or digit, lowercase everything, and return the `k` most frequent words as a list of `(word, count)` tuples. Sort by count descending, then by word ascending. `k <= 0` returns `[]`, and `k` larger than the number of distinct words returns all of them.

`top_k_words("the cat, the dog. The end!", 2)` returns `[("the", 3), ("cat", 1)]`.

Answer with the complete file in a single ```python code block and nothing else.

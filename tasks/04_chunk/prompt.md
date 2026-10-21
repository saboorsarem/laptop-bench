Write `solution.py` containing one function:

```python
def chunk(seq, n):
    ...
```

Return `seq` split into a list of lists of at most `n` items, keeping the order. The last group may be shorter. `seq` can be any sequence.

Rules:
- `chunk([1, 2, 3, 4, 5], 2)` returns `[[1, 2], [3, 4], [5]]`.
- `chunk("abcde", 2)` returns `[["a", "b"], ["c", "d"], ["e"]]`, always lists, never strings.
- `chunk([], 3)` returns `[]`.
- `n <= 0` raises `ValueError`.
- The input sequence must not be modified.

Answer with the complete file in a single ```python code block and nothing else.

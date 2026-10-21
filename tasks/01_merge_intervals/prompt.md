Write `solution.py` containing one function:

```python
def merge_intervals(intervals):
    ...
```

`intervals` is a list of `[start, end]` integer pairs, not necessarily sorted. Return a new list of pairs where every overlapping or touching interval is merged, sorted by start.

Rules:
- `[]` returns `[]`.
- Intervals that only touch are merged: `[[1, 2], [2, 3]]` returns `[[1, 3]]`.
- Zero-length intervals are valid integers, e.g. `[[5, 5]]` returns `[[5, 5]]`.
- The input list must not be modified.

Answer with the complete file in a single ```python code block and nothing else.

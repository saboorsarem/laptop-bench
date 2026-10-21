This file contains a bug.

```python
def binary_search(arr, target):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid
        else:
            hi = mid
    return -1
```

For some inputs it loops forever, for others it returns a wrong index. `arr` is a list of integers sorted ascending and may contain duplicates.

Fix the bug and return the complete corrected `solution.py`, keeping the function signature. Any index holding `target` is accepted, `-1` when it is absent. Answer with the complete file in a single ```python code block and nothing else.

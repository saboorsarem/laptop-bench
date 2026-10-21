Write `solution.py` containing one function:

```python
def version_compare(a, b):
    ...
```

Both arguments are dotted numeric string versions such as `"1.2.3"`. Return `-1` if `a` is older, `0` if they are equal, `1` if `a` is newer. Compare component by component numerically, not as strings, and treat missing components as zero, so `"1.2"` equals `"1.2.0"`. Components are non-negative integers.

Examples:
- `version_compare("1.2", "1.10")` returns `-1`
- `version_compare("1.2.0", "1.2")` returns `0`
- `version_compare("2", "1.9.9")` returns `1`

Answer with the complete file in a single ```python code block and nothing else.

Write `solution.py` containing one function:

```python
def csv_to_json(text):
    ...
```

`text` is CSV with a header row and comma separators, possibly quoted fields, possibly a trailing newline. Return a list of dicts, one per data row, keyed by the header names.

Convert each field like this:
- `""` (empty) becomes `None`
- a value matching an optional minus and digits becomes `int`
- a value matching an optional minus, digits, a dot and digits becomes `float`
- anything else stays a `str`, and quotes around it must be removed

`csv_to_json("a,b\n1,2.5\n")` returns `[{"a": 1, "b": 2.5}]`.

Answer with the complete file in a single ```python code block and nothing else.

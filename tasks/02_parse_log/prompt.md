Write `solution.py` containing one function:

```python
def parse_log(line):
    ...
```

`line` is one access-log line in this exact shape:

```
203.0.113.5 - - [12/Mar/2026:10:11:12 +0000] "GET /api/v1/items?id=3 HTTP/1.1" 200 512
```

Return a dict with these keys:
- `ip`: string, `"203.0.113.5"`
- `method`: string, `"GET"`
- `path`: string, the request target with the query string, `"/api/v1/items?id=3"`
- `status`: int, `200`
- `bytes`: int, `512`

A `-` in the size field means 0. Raise `ValueError` on a line that does not match the shape. A trailing newline must be accepted.

Answer with the complete file in a single ```python code block and nothing else.

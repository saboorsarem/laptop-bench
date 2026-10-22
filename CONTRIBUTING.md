# Contributing

Two useful contributions: numbers from your machine, and tasks that expose real
failure modes.

## Report your machine

1. Run the suite against a model you actually use:

   ```bash
   python bench.py --base-url http://127.0.0.1:8080/v1 --model "<model id>"
   ```

2. Add the JSON file from `results/` and one row to the table in `results/README.md`.
3. Include the machine line: CPU or Apple chip, GPU and VRAM, RAM. Results without
   hardware are not merged.
4. One model per pull request. Mention the runtime and its version in the description.

Do not edit an existing result file, and do not rerun other people's setups to
"correct" them. Two rows for the same model on different machines is the point.

## Add a task

Create three files:

```
tasks/09_short_name/prompt.md     # the request, signature and edge cases
tasks/09_short_name/check.py      # asserts; runs next to the model's solution.py
reference/09_short_name.py        # a correct solution
```

Rules for `check.py`:

- exit 0 on success, raise or exit non-zero on failure, print nothing on success;
- fail on a plausible naive implementation, not only on empty input;
- no network, no sleeps, no randomness, no reliance on the clock;
- under one second of runtime.

Rules for `prompt.md`:

- state the exact function and signature, and every edge case the check tests;
- request the answer as a single ```` ```python ```` block;
- avoid ambiguity about types. Say "always lists, never strings" rather than
  "any sequence" if the check distinguishes them.

Then validate:

```bash
python selftest.py
```

CI runs the same command, so a red check means the pull request cannot be merged.

## Code changes

`bench.py` stays dependency-free, Python 3.9+, one file. Keep the task format stable:
result files from old versions must remain readable.

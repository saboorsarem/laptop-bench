# Methodology

The goal is a number a person can trust in five minutes, not a definitive ranking.
Every choice below trades coverage for reproducibility on consumer hardware.

## Protocol

1. Each task is a single request to `POST {base_url}/chat/completions`.
2. The prompt is `tasks/<id>/prompt.md`, verbatim. For tasks with `starter.py`, the
   file contents are appended as the current version of `solution.py`.
3. `temperature: 0`, `max_tokens: 2048`, streaming enabled. Nothing else is set; the
   server applies its own defaults for the rest.
4. One sample per task. No retries, no self-consistency, no tool use.
5. The answer is parsed by taking the **last** ```` ```python ```` block. If there is
   no fenced block, the whole message is treated as code. Nothing is repaired.
6. The extracted text is written as `solution.py` in a fresh temp directory together
   with the task's `check.py`, then `python check.py` runs with a 20-second timeout.
   Exit code 0 means pass.
7. Timing: time to first token is measured to the first non-empty `delta.content` or
   `delta.reasoning_content`. Tokens per second is `completion_tokens /
   (total_seconds - ttft)`, averaged over tasks that reported usage.

## Scoring

`pass@1` is passes divided by tasks. All tasks have equal weight. A failing task is a
failure for any reason: wrong output, exception in the check, timeout, or an endpoint
error.

## Known biases

- **Small suite.** Eight tasks: one failure moves the score by 12.5 points. Treat
  differences under 25 points as noise.
- **Single sample.** At temperature 0 most servers are close to deterministic but not
  exactly; llama.cpp produced different results on one task across two runs of the same
  model.
- **Python, short, English.** No multi-file edits, no tool calls, no long context. A
  model that shines at agentic coding can score poorly here and vice versa.
- **Prompt phrasing.** Every prompt states the function signature and edge cases
  explicitly, so the test measures implementation, not inference of intent. Tasks that
  turned out ambiguous were rewritten and rerun, not silently re-scored.
- **Speed is decode speed.** On CPU, and on GPUs that offload only part of the model,
  prompt processing dominates real-world latency. `ttft` is the column to read for
  that.
- **Hardware noise.** Background load matters: a parallel download changed one CPU
  result from 6.7 to 4.7 tok/s on the same machine. Close other work before reporting.

## Adding tasks

A task is accepted when:

- the same prompt would make a competent engineer write essentially the same code;
- `check.py` fails on a plausible wrong implementation, not only on empty input;
- `reference/<id>.py` passes `check.py`, and `python selftest.py` is green;
- it runs in under a second on a laptop and needs no network, randomness or clock.

Prefer a bug fix or a spec with a real edge case over a puzzle. Coverage targets:
parsing, string handling, data transformation, error semantics, small algorithms.

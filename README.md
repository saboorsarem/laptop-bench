# laptop-bench

[![selftest](https://github.com/saboorsarem/laptop-bench/actions/workflows/selftest.yml/badge.svg)](https://github.com/saboorsarem/laptop-bench/actions/workflows/selftest.yml)
[![license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](bench.py)

Coding models are ranked on H100 clusters and then used on laptops. This project
closes that gap with a short, verified task set and one number that matters:
**can this model solve your work on your machine, and how long does it take.**

```
pass@1: 6/8 (75%)   6.7 tok/s   ttft 1.01s   252s total   i5-12450H, 16 GB RAM, no GPU
```

No dependencies, one file, any OpenAI-compatible server: llama.cpp, LM Studio, Ollama,
vLLM, SGLang, `rec`.

## Results

Measured on the machine in the machine column, one sample per task, temperature 0.

| model | quant | machine | pass@1 | tok/s | ttft | total |
| --- | --- | --- | --- | --- | --- | --- |
| qwen3-4b-instruct-2507 | Q4_K_M | i5-12450H, 16 GB, no GPU | 6/8 (75%) | 6.7 | 1.01 s | 252 s |

Full records, including per-task output and the exact command, are in
[`results/`](results/). To add your machine, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Quickstart

Serve a model with [llama.cpp](https://github.com/ggml-org/llama.cpp):

```bash
winget install llama.cpp          # Windows
brew install llama.cpp            # macOS
llama-server -hf unsloth/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M -c 8192 --port 8080
```

Run the benchmark in another terminal:

```bash
python bench.py --base-url http://127.0.0.1:8080/v1 \
  --model "unsloth/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M"
```

Output ends with the summary line and a JSON file in `results/`. Any OpenAI-compatible
server works; only the base URL and model id change:

| runtime | base URL | notes |
| --- | --- | --- |
| llama.cpp | `http://127.0.0.1:8080/v1` | `llama-server -hf <repo>:<quant>` |
| LM Studio | `http://127.0.0.1:1234/v1` | `lms server start` |
| Ollama | `http://127.0.0.1:11434/v1` | `ollama serve` |
| vLLM / SGLang | `http://127.0.0.1:8000/v1`, `:30000/v1` | |
| rec (Recursive) | `http://127.0.0.1:11500/v1` | key from `rec auth token` |

## What is measured

- **pass@1** — tasks solved on the first attempt, out of 8.
- **tok/s** — generated tokens divided by generation time (total minus time to first
  token), averaged over tasks. Prompt processing is excluded.
- **ttft** — median time to first token, prompt processing included.
- **total** — wall clock for the whole run, including local test execution.

Every result file also records CPU, GPU, RAM, OS, Python and the command that produced
it. Protocol details, scoring rules and known biases are in
[docs/METHODOLOGY.md](docs/METHODOLOGY.md).

## Scope

This is a smoke test, not a leaderboard of intelligence. Eight small Python tasks,
one sample each. It answers whether a model is usable on a given box and roughly how
fast, in about five minutes. It does not measure long-horizon agentic work, other
languages, or prompt sensitivity.

## Add a task

```
tasks/09_my_task/prompt.md   # what to ask, and the exact function signature
tasks/09_my_task/check.py    # asserts, run in the same directory as the answer
reference/09_my_task.py      # a correct solution, proves the task is solvable
```

The model's answer is saved as `solution.py` in a temp directory, next to `check.py`.
Optional `starter.py` in the task folder is shown to the model as its current file,
which is how the bug-fix task works.

Validate the whole suite after adding anything:

```bash
python selftest.py
```

## Safety

The model's code is executed locally by `check.py`. Tasks are reviewed but this is not
a sandbox: use a container or a throwaway VM for untrusted models, tasks or endpoints.

## License

MIT.

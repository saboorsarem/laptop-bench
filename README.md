# laptop-bench

Benchmark coding models on the machine you actually own.

Most model launches quote numbers from an H100. This runs a small, verified task set
against any OpenAI-compatible endpoint and reports what a laptop really gets:
pass@1, time to first token, tokens per second, total seconds and RAM.

```
pass@1: 6/8 (75%)   6.7 tok/s   ttft 1.01s   252s total   16 GB RAM
```

## What it is not

Not SWE-bench, not a leaderboard of intelligence. Eight small tasks, one sample each,
temperature 0. It answers one question honestly: *is this model usable on this box,
and how painful is it?* Add tasks. Publish your numbers.

## Run it

Download a model and serve it with [llama.cpp](https://github.com/ggml-org/llama.cpp):

```bash
winget install llama.cpp          # Windows
brew install llama.cpp            # macOS
llama-server -hf unsloth/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M -c 8192 --port 8080
```

Then, in another terminal:

```bash
python bench.py --base-url http://127.0.0.1:8080/v1 \
  --model "unsloth/Qwen3-4B-Instruct-2507-GGUF:Q4_K_M"
```

Any OpenAI-compatible server works. Only the base URL, model id and optional key change:

| runtime | base URL | notes |
| --- | --- | --- |
| llama.cpp | `http://127.0.0.1:8080/v1` | `llama-server -hf <repo>:<quant>` |
| LM Studio | `http://127.0.0.1:1234/v1` | `lms server start` |
| Ollama | `http://127.0.0.1:11434/v1` | `ollama serve` |
| rec (Recursive) | `http://127.0.0.1:11500/v1` | key from `rec auth token` |

No dependencies. Python 3.9+.

## Submit your machine

```bash
python bench.py --base-url ... --model <id>
```

writes `results/<date>-<model>.json`. Open a PR with that file plus one line in
`results/README.md`. Include the CPU/GPU line — results without hardware are noise.

## Add a task

```
tasks/09_my_task/prompt.md   # what to ask, and the exact function signature
tasks/09_my_task/check.py    # asserts, run in the same directory as the answer
reference/09_my_task.py      # a correct solution, proves the task is solvable
```

`check.py` runs in a temp directory with the model's file saved as `solution.py`.
It must print nothing and exit 0 on success. Optional `starter.py` in the task folder
is shown to the model as the current file, for bug-fix tasks.

Validate everything you add:

```bash
python selftest.py
```

## Safety

The model's code is executed locally by `check.py`. Tasks are small and reviewed, but
this is not a sandbox: run it in a container or a throwaway VM if you feed it untrusted
models or tasks.

## License

MIT.

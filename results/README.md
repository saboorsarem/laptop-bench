# Results

One row per machine. Numbers are meaningless without the hardware line, so always
include it.

| date | model | quant | machine | pass@1 | tok/s | ttft | total | file |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-10-22 | qwen3-4b-instruct-2507 | Q4_K_M | i5-12450H, 16 GB RAM, no GPU | 6/8 (75%) | 6.7 | 1.01 s | 252 s | [json](2026-10-22-unsloth-qwen3-4b-instruct-2507-gguf-q4-k-m.json) |

How to read the columns:

- **pass@1** — tasks solved first try, out of 8.
- **tok/s** — generated tokens divided by generation time (total minus time to first token), averaged over tasks. Prompt processing is excluded, so this is decode speed.
- **ttft** — median time to first token, includes prompt processing.
- **total** — wall clock for the whole run.

Notes on this run: llama.cpp on CPU only, `-c 8192`, one sample per task at
temperature 0. Failed `02_parse_log` (regex too strict) and `06_csv_to_json`
(hand-rolled parser broke on the trailing newline, `IndexError`). Task set is small,
so one failure moves the score by 12.5 points — treat this as a smoke test, not a
ranking.

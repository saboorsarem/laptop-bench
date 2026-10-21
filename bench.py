#!/usr/bin/env python3
"""laptop-bench: run a small coding task set against any OpenAI-compatible endpoint.

Reports pass rate, time to first token, tokens/sec and machine RAM, so two models
can be compared on the hardware a person actually owns.

    python bench.py --base-url http://127.0.0.1:8080/v1 --model flint
"""
import argparse
import json
import os
import platform
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
TASKS_DIR = os.path.join(ROOT, "tasks")
RESULTS_DIR = os.path.join(ROOT, "results")
CODE_BLOCK = re.compile(r"```(?:python|py)?\s*\n(.*?)```", re.S)


def total_ram_gb():
    try:
        if sys.platform == "win32":
            import ctypes

            class Status(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]

            status = Status()
            status.dwLength = ctypes.sizeof(Status)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status))
            return round(status.ullTotalPhys / 2**30)
        with open("/proc/meminfo") as handle:
            for line in handle:
                if line.startswith("MemTotal:"):
                    return round(int(line.split()[1]) * 1024 / 2**30)
    except Exception:
        pass
    return None


def machine():
    return {
        "cpu": os.environ.get("PROCESSOR_IDENTIFIER") or platform.processor() or platform.machine(),
        "os": f"{platform.system()} {platform.release()}",
        "ram_gb": total_ram_gb(),
        "python": platform.python_version(),
    }


def stream_chat(base_url, api_key, model, prompt, max_tokens, timeout):
    """Returns (text, reasoning, ttft_s, seconds, usage|None)."""
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": max_tokens,
        "stream": True,
        "stream_options": {"include_usage": True},
    }
    payload = json.dumps(body).encode()
    url = base_url.rstrip("/") + "/chat/completions"

    def post(data):
        request = urllib.request.Request(
            url, data=data, headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
        )
        return urllib.request.urlopen(request, timeout=timeout)

    started = time.time()
    try:
        response = post(payload)
    except urllib.error.HTTPError as error:
        if error.code != 400:
            raise
        body.pop("stream_options")
        response = post(json.dumps(body).encode())

    first = None
    answer, reasoning, usage = [], [], None
    with response:
        for raw in response:
            line = raw.decode("utf-8", "replace").strip()
            if not line.startswith("data:"):
                continue
            data = line[5:].strip()
            if data == "[DONE]":
                break
            try:
                chunk = json.loads(data)
            except json.JSONDecodeError:
                continue
            usage = chunk.get("usage") or usage
            for choice in chunk.get("choices", []):
                delta = choice.get("delta") or {}
                thought, content = delta.get("reasoning_content"), delta.get("content")
                if (thought or content) and first is None:
                    first = time.time() - started
                if thought:
                    reasoning.append(thought)
                if content:
                    answer.append(content)
    seconds = time.time() - started
    return "".join(answer), "".join(reasoning), first or seconds, seconds, usage


def extract_code(text):
    blocks = CODE_BLOCK.findall(text)
    return (blocks[-1] if blocks else text).strip() + "\n"


def run_check(workdir, code, timeout):
    with open(os.path.join(workdir, "solution.py"), "w", encoding="utf-8") as handle:
        handle.write(code)
    try:
        done = subprocess.run(
            [sys.executable, "check.py"],
            cwd=workdir,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return False, "check timed out"
    if done.returncode == 0:
        return True, ""
    return False, (done.stderr or done.stdout).strip()[-300:]


def load_task(name):
    path = os.path.join(TASKS_DIR, name)
    prompt = open(os.path.join(path, "prompt.md"), encoding="utf-8").read().strip()
    starter = os.path.join(path, "starter.py")
    if os.path.exists(starter):
        prompt += "\n\nCurrent file `solution.py`:\n\n```python\n" + open(starter, encoding="utf-8").read().strip() + "\n```"
    return prompt, os.path.join(path, "check.py")


def main():
    parser = argparse.ArgumentParser(description="Benchmark a local coding model.")
    parser.add_argument("--base-url", default="http://127.0.0.1:8080/v1")
    parser.add_argument("--api-key", default=os.environ.get("BENCH_API_KEY", "none"))
    parser.add_argument("--model", required=True)
    parser.add_argument("--max-tokens", type=int, default=2048)
    parser.add_argument("--timeout", type=float, default=600, help="per-request timeout, seconds")
    parser.add_argument("--check-timeout", type=float, default=20, help="per-task test timeout, seconds")
    parser.add_argument("--only", nargs="*", help="run only these task ids")
    parser.add_argument("--out", help="write JSON here")
    args = parser.parse_args()

    names = sorted(os.listdir(TASKS_DIR))
    names = [n for n in names if os.path.isdir(os.path.join(TASKS_DIR, n))]
    if args.only:
        names = [n for n in names if any(o in n for o in args.only)]
    if not names:
        sys.exit("no tasks matched")

    print(f"model:  {args.model}")
    print(f"url:    {args.base_url}")
    print(f"tasks:  {len(names)}")
    print()

    records = []
    for index, name in enumerate(names, 1):
        prompt, check_path = load_task(name)
        try:
            answer, reasoning, ttft, seconds, usage = stream_chat(
                args.base_url, args.api_key, args.model, prompt, args.max_tokens, args.timeout
            )
        except Exception as error:
            print(f"[{index}/{len(names)}] {name}: endpoint error: {error}")
            records.append({"id": name, "passed": False, "error": f"endpoint: {error}", "seconds": None, "tokens": None})
            continue
        with tempfile.TemporaryDirectory() as workdir:
            with open(os.path.join(workdir, "check.py"), "w", encoding="utf-8") as handle:
                handle.write(open(check_path, encoding="utf-8").read())
            passed, detail = run_check(workdir, extract_code(answer), args.check_timeout)
        completion = (usage or {}).get("completion_tokens")
        record = {
            "id": name,
            "passed": passed,
            "seconds": round(seconds, 1),
            "ttft_s": round(ttft, 2),
            "tokens": completion,
            "reasoning_chars": len(reasoning),
            "detail": detail,
        }
        records.append(record)
        print(f"[{index}/{len(names)}] {name}: {'pass' if passed else 'FAIL'} ({seconds:.1f}s, ttft {ttft:.2f}s)" + (f" - {detail}" if detail else ""))

    passed = sum(1 for r in records if r["passed"])
    timed = [r for r in records if r["seconds"]]
    token_counts = [r["tokens"] for r in records if r["tokens"]]
    speeds = [
        r["tokens"] / max(r["seconds"] - r["ttft_s"], 1e-6)
        for r in records
        if r["tokens"] and r["seconds"]
    ]
    summary = {
        "passed": passed,
        "total": len(records),
        "pass_rate": round(passed / len(records), 3),
        "tok_per_s": round(sum(speeds) / len(speeds), 1) if speeds else None,
        "ttft_s": round(sorted(r["ttft_s"] for r in timed)[len(timed) // 2], 2) if timed else None,
        "total_seconds": round(sum(r["seconds"] or 0 for r in records), 1),
        "total_tokens": sum(token_counts) if token_counts else None,
    }

    result = {
        "tool": "laptop-bench",
        "version": "0.1",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "model": args.model,
        "base_url": args.base_url,
        "machine": machine(),
        "settings": {"max_tokens": args.max_tokens, "temperature": 0},
        "summary": summary,
        "tasks": records,
    }

    print()
    print(f"pass@1: {passed}/{len(records)} ({summary['pass_rate'] * 100:.0f}%)   "
          f"{summary['tok_per_s']} tok/s   ttft {summary['ttft_s']}s   "
          f"{summary['total_seconds']}s total   {machine()['ram_gb']} GB RAM")

    out = args.out
    if not out:
        slug = re.sub(r"[^a-z0-9]+", "-", args.model.lower()).strip("-")
        out = os.path.join(RESULTS_DIR, f"{time.strftime('%Y-%m-%d')}-{slug}.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
    print(f"saved:  {out}")


if __name__ == "__main__":
    main()

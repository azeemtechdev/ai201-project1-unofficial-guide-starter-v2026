"""
Capstone trials: your five criteria, run 3 times each, cache OFF.

    python run_capstone.py --label before
    python run_capstone.py --label after        (after your improvement)

Writes results/capstone_<label>_<time>.md with the table and the real output
for each criterion. Every request also goes into logs/runs.jsonl.
"""
import argparse
import os
import time
from datetime import datetime

os.environ["AI201_CACHE"] = "0"   # before config is imported
os.environ["AI201_FAULT"] = ""

import app
import config
import generate
import logger
from questions import answered

COVERED = "how many gb ram should my laptop be for cs course?"
INVALID = ["", "   ", "x" * 501, "y" * 800, "z" * 2000]
# criterion 3 wants 2 whitespace-only + 3 over-500-char inputs
INVALID = ["   ", "\n \t ", "x" * 501, "y" * 800, "z" * 2000]


def log_lines() -> int:
    if not config.LOG_PATH.exists():
        return 0
    return len([l for l in config.LOG_PATH.read_text(encoding="utf-8").splitlines() if l.strip()])


def norm(s: str) -> str:
    return "".join(s.lower().split())


def set_timeout(seconds):
    config.REQUEST_TIMEOUT_S = seconds
    generate._client = None          # client bakes the timeout in when created


def c1():
    """Real client timeout, 5 times."""
    notes, ok = [], 0
    set_timeout(0.001)
    try:
        for _ in range(5):
            o = app.ask_pipeline(COVERED)
            row = logger.read_log(1)[0]
            good = (
                o["status"] == "error"
                and o["error_type"] == "timeout"
                and "too long" in o["answer"].lower()
                and row["status"] == "error"
                and row["error_type"] == "timeout"
            )
            ok += good
            notes.append(f"{'PASS' if good else 'FAIL'} status={row['status']} "
                         f"error_type={row['error_type']} msg={o['answer']!r}")
    finally:
        set_timeout(20.0)
    return ok, 5, notes


def c2():
    """10 questions, one forced timeout: exactly 10 new log lines."""
    qs = [q["question"] for q in answered()] * 2
    before = log_lines()
    statuses = []
    for i, q in enumerate(qs):
        config.FAULT = "timeout" if i == 4 else ""
        statuses.append(app.ask_pipeline(q)["status"])
    config.FAULT = ""
    added = log_lines() - before
    return added, 10, [f"new log lines: {added} (expected 10)", f"statuses: {statuses}"]


def c3():
    """5 invalid inputs rejected, logged as rejected with 0 tokens."""
    ok, notes = 0, []
    for text in INVALID:
        o = app.ask_pipeline(text)
        row = logger.read_log(1)[0]
        good = (o["status"] == "rejected" and row["status"] == "rejected"
                and row["tokens"] == 0 and bool(o["answer"]))
        ok += good
        notes.append(f"{'PASS' if good else 'FAIL'} len={len(text)} status={row['status']} "
                     f"tokens={row['tokens']} msg={o['answer']!r}")
    return ok, 5, notes


def c4():
    """11 requests in one session; first is cold, 10 warm; count under 1900 ms."""
    qs = [q["question"] for q in answered()]
    seq = (qs * 3)[:11]
    times, notes = [], []
    for i, q in enumerate(seq):
        o = app.ask_pipeline(q)
        row = logger.read_log(1)[0]
        tag = "cold (not counted)" if i == 0 else "warm"
        notes.append(f"{tag:<18} {row['status']:<9} {row['duration_ms']:>6} ms")
        if i > 0:
            times.append((row["status"] == "answered", row["duration_ms"]))
    fast = sum(1 for ok, ms in times if ok and ms < 1900)
    return fast, 10, notes


def c5():
    """Original test questions still contain their expected phrase."""
    ok, notes = 0, []
    for q in answered():
        o = app.ask_pipeline(q["question"])
        good = o["status"] == "answered" and norm(q["expects"]) in norm(o["answer"])
        ok += good
        notes.append(f"{'PASS' if good else 'FAIL'} expects={q['expects']!r}\n"
                     f"      Q: {q['question']}\n      A: {o['answer']}")
    return ok, 5, notes


CRITERIA = [
    ("1. Real timeout gives clear message + error/timeout log row", "5 of 5", c1, lambda s, t: s >= 5),
    ("2. Every request logged (10 new lines, 1 forced failure)", "10 of 10", c2, lambda s, t: s == 10),
    ("3. Invalid input rejected, 0 tokens, logged", "5 of 5", c3, lambda s, t: s >= 5),
    ("4. Warm requests under 1.9s", "9 of 10", c4, lambda s, t: s >= 9),
    ("5. Original questions still contain expected phrase", "5 of 5", c5, lambda s, t: s >= 5),
]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--label", default="before")
    args = p.parse_args()

    scores = {c[0]: [] for c in CRITERIA}
    details = {c[0]: [] for c in CRITERIA}
    for trial in (1, 2, 3):
        print(f"=== trial {trial} of 3 ===", flush=True)
        for name, target, fn, passes in CRITERIA:
            s, total, notes = fn()
            scores[name].append((s, total))
            details[name].append((trial, notes))
            print(f"  {name[:48]:<48} {s}/{total}", flush=True)

    lines = [f"# Capstone run: {args.label}  ({datetime.now():%Y-%m-%d %H:%M})\n",
             "| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |",
             "|---|---|---|---|---|---|"]
    for name, target, fn, passes in CRITERIA:
        runs = scores[name]
        verdict = "MET" if all(passes(s, t) for s, t in runs) else "MISSED"
        cells = " | ".join(f"{s}/{t}" for s, t in runs)
        lines.append(f"| {name} | {target} | {cells} | {verdict} |")
    lines.append("")
    for name, *_ in CRITERIA:
        lines.append(f"## {name}\n")
        for trial, notes in details[name]:
            lines.append(f"**Trial {trial}**\n```")
            lines.extend(notes)
            lines.append("```\n")

    config.RESULTS_DIR.mkdir(exist_ok=True)
    out = config.RESULTS_DIR / f"capstone_{args.label}_{datetime.now():%Y-%m-%d_%H%M}.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print("\n" + "\n".join(lines[:9]))
    print(f"\nFull output saved to {out}")


if __name__ == "__main__":
    main()
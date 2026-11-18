"""
Capstone cost measurement: 10 real runs, cache OFF, averaged.

    python measure_cost.py

Cost here = tokens used and seconds per run, read back from the service and
the clock (not from a pricing page). Every run is also written to
logs/runs.jsonl by ask_pipeline, so these are your first log entries.
"""
import os

os.environ["AI201_CACHE"] = "0"   # must be set before config is imported
os.environ["AI201_FAULT"] = ""

import statistics
import app
import config
import generate
from questions import answered

questions = [q["question"] for q in answered()]
runs = (questions * 2)[:10]          # 5 questions, twice each = 10 runs

rows = []
for i, q in enumerate(runs, 1):
    before = generate.token_counts()
    outcome = app.ask_pipeline(q)
    after = generate.token_counts()
    from logger import read_log
    last = read_log(1)[0]
    rows.append(
        {
            "status": outcome["status"],
            "ms": last["duration_ms"],
            "tokens": after["total"] - before["total"],
        }
    )
    print(f"{i:>2}. {outcome['status']:<9} {last['duration_ms']:>6} ms  "
          f"{rows[-1]['tokens']:>5} tokens  {q[:55]!r}")

model_runs = [r for r in rows if r["status"] == "answered"]
print("\n--- measured cost per run ---")
print(f"runs: {len(rows)}  (answered by the model: {len(model_runs)})")
if model_runs:
    print(f"avg tokens per answered run: {statistics.mean(r['tokens'] for r in model_runs):.0f}")
    print(f"avg seconds per answered run: {statistics.mean(r['ms'] for r in model_runs)/1000:.2f}")
    print(f"slowest: {max(r['ms'] for r in model_runs)/1000:.2f}s")
print(generate.usage())
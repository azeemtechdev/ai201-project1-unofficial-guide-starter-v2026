"""
Structured run log.

Every question that goes through `app.py::ask_pipeline` leaves one JSON line in
logs/runs.jsonl -- answered, refused, rejected or failed. A run that errored
leaves a record too, because a failure that shows up only as an absence is one
you will never find.

Read it back with:  python logger.py        (last 10 entries, one per line)
"""

import json
import sys
from datetime import datetime, timezone

import config


def log_run(**fields) -> dict:
    """Append one record. Never raises: logging must not break a run."""
    record = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    record.update(fields)
    try:
        config.LOG_PATH.parent.mkdir(exist_ok=True)
        with open(config.LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception as exc:  # noqa: BLE001
        print(f"  [log] could not write log: {exc}", file=sys.stderr)
    return record


def read_log(n: int | None = None) -> list[dict]:
    if not config.LOG_PATH.exists():
        return []
    lines = config.LOG_PATH.read_text(encoding="utf-8").splitlines()
    records = [json.loads(line) for line in lines if line.strip()]
    return records[-n:] if n else records


if __name__ == "__main__":
    for r in read_log(10):
        print(
            f"{r['ts']}  {r['status']:<9} {r['duration_ms']:>6}ms  "
            f"{r.get('error_type') or '-':<18} {r['question'][:50]!r}"
        )
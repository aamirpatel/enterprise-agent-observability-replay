import csv
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
for name in ["historical_sessions.jsonl", "trace_events.jsonl"]:
    rows = [json.loads(x) for x in (root / "sample_data" / name).read_text().splitlines() if x]
    assert rows, f"No rows in {name}"
with (root / "sample_data" / "failure_scenarios.csv").open(newline="") as handle:
    assert len(list(csv.DictReader(handle))) >= 5
print("Starter assets validated successfully")

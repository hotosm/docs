"""Run eval questions against a running API: uv run python evals/run.py [api_url]"""

import json
import sys
import time
from pathlib import Path

import httpx
import yaml

API = next((a for a in sys.argv[1:] if not a.startswith("-")), None) or "http://localhost:8000"
REFUSAL_MARKERS = ["couldn't find", "could not find", "not in the doc", "don't have", "do not have"]


def ask(question: str) -> dict:
    out = {"answer": "", "sources": [], "ttft": None, "grounded": None}
    start = time.monotonic()
    with httpx.stream(
        "POST", f"{API}/api/chat", json={"messages": [{"role": "user", "content": question}]}, timeout=600
    ) as r:
        r.raise_for_status()
        event = None
        for line in r.iter_lines():
            if line.startswith("event: "):
                event = line[7:]
            elif line.startswith("data: "):
                data = json.loads(line[6:])
                if event == "token":
                    out["ttft"] = out["ttft"] or time.monotonic() - start
                    out["answer"] += data["t"]
                elif event == "sources":
                    out["sources"] = [s["url"] for s in data]
                elif event == "done":
                    out["grounded"] = data["grounded"]
                elif event == "error":
                    out["answer"] += f"[ERROR {data['message']}]"
    out["total"] = time.monotonic() - start
    return out


def main() -> None:
    cases = yaml.safe_load((Path(__file__).parent / "questions.yaml").read_text())
    passed = 0
    for case in cases:
        res = ask(case["q"])
        text = res["answer"].lower()
        problems = []
        if case.get("refuse"):
            if res["grounded"] and not any(m in text for m in REFUSAL_MARKERS):
                problems.append("answered instead of refusing")
        else:
            problems += [f"missing '{k}'" for k in case.get("expect", []) if k.lower() not in text]
            if case.get("source") and not any(case["source"] in u.lower() for u in res["sources"]):
                problems.append(f"no source matching '{case['source']}'")
            if res["grounded"] and "[" not in res["answer"]:
                problems.append("no citations")
        ok = not problems
        passed += ok
        ttft = f"{res['ttft']:.1f}s" if res["ttft"] else "-"
        print(f"{'PASS' if ok else 'FAIL'}  ttft={ttft:>6} total={res['total']:.1f}s  {case['q']}")
        if problems:
            print("      ", "; ".join(problems))
        if "-v" in sys.argv:
            print("      ", res["answer"].replace("\n", "\n       "), "\n")
    print(f"\n{passed}/{len(cases)} passed")


if __name__ == "__main__":
    main()

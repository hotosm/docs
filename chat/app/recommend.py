"""Deterministic project planner driven by rules.yaml."""

from pathlib import Path

import yaml


def _matches(cond: dict | None, answers: dict) -> bool:
    if not cond:
        return True
    return all(answers.get(k) in [str(v) for v in allowed] for k, allowed in cond.items())


class Planner:
    def __init__(self, rules_file: Path):
        cfg = yaml.safe_load(rules_file.read_text())
        self.questions: list[dict] = cfg["questions"]
        self.stages: list[dict] = cfg["stages"]
        self.tools: dict[str, dict] = cfg["tools"]
        self.rules: list[dict] = cfg["rules"]
        for q in self.questions:
            for opt in q.get("options", []):
                opt["value"] = str(opt["value"])

    def public_config(self) -> dict:
        return {"questions": self.questions, "stages": self.stages}

    def visible_questions(self, answers: dict) -> list[dict]:
        return [q for q in self.questions if _matches(q.get("ask_if"), answers)]

    def validate(self, answers: dict) -> dict:
        clean = {}
        for q in self.visible_questions(answers):
            v = answers.get(q["id"])
            if v is None:
                continue
            if q.get("type") == "text":
                clean[q["id"]] = str(v)[:300]
            elif str(v) in {o["value"] for o in q["options"]}:
                clean[q["id"]] = str(v)
        return clean

    def recommend(self, answers: dict) -> dict:
        answers = self.validate(answers)
        chosen: dict[str, list[str]] = {}
        notes: list[str] = []
        for rule in self.rules:
            if not _matches(rule.get("when"), answers):
                continue
            if rule.get("unless") and _matches(rule["unless"], answers):
                continue
            for tid in rule.get("remove", []):
                chosen.pop(tid, None)
            for tid in rule.get("add", []):
                chosen.setdefault(tid, [])
                if rule.get("reason") and rule["reason"] not in chosen[tid]:
                    chosen[tid].append(rule["reason"])
            if rule.get("note") and rule["note"] not in notes:
                notes.append(rule["note"])

        stages = []
        for stage in self.stages:
            tools = [
                {"id": tid, **self.tools[tid], "reasons": reasons}
                for tid, reasons in chosen.items()
                if self.tools[tid]["stage"] == stage["id"]
            ]
            if tools:
                stages.append({**stage, "tools": tools})

        return {
            "answers": answers,
            "scope": self._scope({s["id"] for s in stages}),
            "stages": stages,
            "notes": notes,
        }

    @staticmethod
    def _scope(present: set[str]) -> str:
        core = present & {"imagery", "digitise", "field"}
        if core == {"imagery", "digitise", "field"}:
            return "Full end-to-end workflow"
        if core == {"field"}:
            return "Field collection only"
        if core <= {"imagery", "digitise"} and "digitise" in core:
            return "Remote mapping only"
        if not core:
            return "Use existing data"
        labels = {"imagery": "imagery", "digitise": "remote mapping", "field": "field collection"}
        return "Partial workflow: " + " + ".join(labels[s] for s in ("imagery", "digitise", "field") if s in core)

    def describe(self, plan: dict) -> str:
        """Plain-text summary given to the LLM."""
        labels = {q["id"]: q for q in self.questions}
        lines = ["User's situation:"]
        for k, v in plan["answers"].items():
            q = labels[k]
            ans = v if q.get("type") == "text" else next(
                o["label"] for o in q["options"] if o["value"] == v
            )
            lines.append(f"- {q['text']} {ans}")
        lines.append(f"\nRecommended scope: {plan['scope']}")
        for s in plan["stages"]:
            lines.append(f"\n{s['label']}:")
            for t in s["tools"]:
                lines.append(f"- {t['name']}: {' '.join(t['reasons'])}")
        if plan["notes"]:
            lines.append("\nNotes:")
            lines.extend(f"- {n}" for n in plan["notes"])
        return "\n".join(lines)

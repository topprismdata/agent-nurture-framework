#!/usr/bin/env python3
"""capability_review — qualitative reflection notes. Emits NO scores.

Replaces the former `capability_assessment.py` (ADR-001 § Migration).

Why no numbers: the old tool averaged Dreyfus-style ordinal ratings across six
dimensions into a single score. Averaged ordinals are statistically weak, and a
self-assessed number was being consumed as capability *evidence*. Per
docs/progress-measurement.md, capability claims come only from behavioral
metrics recorded as EvidenceRecords.

This tool structures human reflection: free-text notes per dimension plus
optional links to EvidenceRecords. Output is a review note — useful for teams,
never promotable as measurement.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

DIMENSIONS = [
    ("Domain knowledge", "Where did domain understanding help? Where was it missing?"),
    ("Task execution", "Which tasks completed smoothly? Which needed rework?"),
    ("Error recovery", "How were failures diagnosed? Recurring failure patterns?"),
    ("Reasoning quality", "Judged from decisions/outcomes: where were choices well-grounded?"),
    ("Autonomy", "Where did the agent need supervision it should not have?"),
    ("Adaptability", "What changed in environment/tooling and how was it absorbed?"),
]


def collect_interactive() -> dict[str, dict[str, str]]:
    print("Qualitative capability review — free-text notes only (no scoring).\n"
          "Link EvidenceRecord ids wherever possible.\n")
    out: dict[str, dict[str, str]] = {}
    for dim in DIMENSIONS:
        print(f"## {dim[0]}\n  {dim[1]}")
        note = input("notes> ").strip()
        refs = input("evidence ids (comma-separated, optional)> ").strip()
        out[dim[0]] = {"note": note, "evidence_refs": [r.strip() for r in refs.split(",") if r.strip()]}
        print()
    return out


def collect_from_file(path: Path) -> dict[str, dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    out: dict[str, dict[str, str]] = {}
    for dim, _ in DIMENSIONS:
        v = data.get(dim, {})
        out[dim] = {"note": str(v.get("note", "")).strip(),
                    "evidence_refs": [str(r) for r in v.get("evidence_refs", [])]}
    return out


def render(answers: dict[str, dict[str, str]]) -> str:
    lines = [
        "# Qualitative Capability Review",
        "",
        f"_Generated {datetime.now(timezone.utc).isoformat(timespec='seconds')}_",
        "",
        "> Reflection notes only. NOT capability evidence — behavioral metrics",
        "> (task success, repeated mistakes, negative transfer) carry evidentiary",
        "> weight per docs/progress-measurement.md.",
        "",
    ]
    for dim, entry in answers.items():
        lines.append(f"## {dim}")
        lines.append(entry["note"] or "_(no notes this period)_")
        if entry["evidence_refs"]:
            lines.append("")
            lines.append("Evidence: " + ", ".join(f"`{r}`" for r in entry["evidence_refs"]))
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--from-json", type=Path, default=None,
                    help="read notes from JSON instead of interactive prompts")
    ap.add_argument("--output-dir", type=Path, default=Path("./reviews"))
    args = ap.parse_args()

    answers = collect_from_file(args.from_json) if args.from_json else collect_interactive()
    md = render(answers)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    md_path = args.output_dir / f"capability-review-{stamp}.md"
    json_path = args.output_dir / f"capability-review-{stamp}.json"
    md_path.write_text(md, encoding="utf-8")
    json_path.write_text(json.dumps({"generated_at": stamp, "answers": answers}, indent=2),
                         encoding="utf-8")
    print(md)
    print(f"\nSaved: {md_path} and {json_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

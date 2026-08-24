#!/usr/bin/env python3
"""evidence_freshness_check — evidence-based freshness triage for capabilities.

Replaces the former `crystallization_scheduler.py` (ADR-001 § Migration).

Core change: staleness is judged from CapabilityRecord freshness metadata
(schemas/capability-record.schema.json), NEVER from file mtime. Day-age
thresholds are deliberately absent; see docs/crystallization-cycle.md §2.

Classifications emitted:
  unknown-freshness        no topprism.freshness metadata (needs onboarding)
  never-verified           last_verified is null
  contradicted-unresolved  last_contradicted set (freezes promotions per docs)
  dependency-drift-suspect current_version differs from version_at_verification
  source-drift-suspect     source_version differs since last verification
  ok-as-of <date>          nothing suspect; freshness anchored to last_verified

Exit codes: 0 clean/informational; 1 if any contradicted-unresolved found
(promotion freeze is a hard signal); with --strict, any non-ok classification
also exits 1.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from anf_frontmatter import discover_skills, parse_frontmatter  # noqa: E402


def classify(meta: dict[str, Any]) -> list[str]:
    tp = meta.get("metadata", {})
    if not isinstance(tp, dict):
        return ["unknown-freshness"]
    tp = tp.get("topprism", {})
    if not isinstance(tp, dict):
        return ["unknown-freshness"]

    fr = tp.get("freshness")
    if not isinstance(fr, dict) or not fr:
        return ["unknown-freshness"]

    out: list[str] = []
    if fr.get("last_contradicted"):
        if tp.get("lifecycle_status") != "disputed":
            out.append("contradicted-unresolved")

    lv = fr.get("last_verified")
    if not lv:
        out.append("never-verified")

    for dep in fr.get("dependencies", []) or []:
        if isinstance(dep, dict) and dep.get("current_version") and \
           dep.get("version_at_verification") and \
           dep["current_version"] != dep["version_at_verification"]:
            out.append(f"dependency-drift-suspect:{dep.get('name','?')}")

    sv = fr.get("source_version")
    if isinstance(sv, dict) and sv.get("verified") and sv.get("current") \
            and sv["verified"] != sv["current"]:
        out.append("source-drift-suspect")

    if not out and lv:
        out.append(f"ok-as-of {lv}")
    elif lv and all(o.startswith(("dependency-", "source-")) for o in out):
        out.append(f"(anchored last_verified {lv})")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default="./skills")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 on ANY non-ok classification (default: only on contradicted-unresolved)")
    args = ap.parse_args()

    files = discover_skills(Path(args.dir))
    if not files:
        print(f"No SKILL.md files found under {args.dir}")
        return 0

    counts: dict[str, int] = {}
    frozen = False
    for f in files:
        meta, _ = parse_frontmatter(f.read_text(encoding="utf-8", errors="replace"))
        cls = classify(meta)
        name = str((meta or {}).get("name") or f.parent.name)
        print(f"{name}\n  {'; '.join(cls)}")
        for c in cls:
            key = c.split(":")[0]
            counts[key] = counts.get(key, 0) + 1
            if key == "contradicted-unresolved":
                frozen = True

    print("\nSummary:", ", ".join(f"{k}={v}" for k, v in sorted(counts.items())) or "nothing classified")
    print("Freshness is evidence-based; mtime is never consulted. "
          "Suspect ≠ stale — resolve via re-verify / re-scope / deprecate.")

    if frozen:
        print("Promotion freeze: contradicted-unresolved present.", file=sys.stderr)
        return 1
    if args.strict and any(k != "ok-as-of" for k in counts):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

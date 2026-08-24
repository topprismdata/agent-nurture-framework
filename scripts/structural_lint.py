#!/usr/bin/env python3
"""structural_lint — validate skill docs against Agent Skills + ANF metadata.

Replaces the former `skill_audit.py` (ADR-001 § Migration).

What this tool checks (structure only, NO quality scores):
  - YAML frontmatter present and parseable
  - Agent Skills required fields: name, description
  - ANF topprism namespace (when present): capability_id / lifecycle_status /
    risk_level / scope / provenance_chain_id formats and enums
  - Body non-empty with a Markdown heading
  - Relative links resolve to existing files

Exit code: 0 if all PASS, 1 if any FAIL. `--strict` also fails on WARN.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from anf_frontmatter import discover_skills, parse_frontmatter  # noqa: E402

LIFECYCLE = {"draft", "active", "refining", "stable", "disputed", "deprecated"}
RISK = {"low", "medium", "high"}
SCOPE = {"personal", "project", "team", "organization"}

CAP_ID = re.compile(r"^cap-[A-Za-z0-9._-]+$")
PROV_ID = re.compile(r"^prov-[A-Za-z0-9._-]+$")

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def lint(path: Path) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []

    def add(level: str, msg: str) -> None:
        issues.append({"level": level, "msg": msg})

    text = path.read_text(encoding="utf-8", errors="replace")
    meta, body = parse_frontmatter(text)

    if not meta:
        add("FAIL", "missing or unparseable YAML frontmatter")
        return issues

    for field in ("name", "description"):
        v = meta.get(field)
        if not isinstance(v, str) or not v.strip():
            add("FAIL", f"Agent Skills field missing/empty: {field}")

    tp_raw = meta.get("metadata")
    tp = tp_raw.get("topprism") if isinstance(tp_raw, dict) else None
    if isinstance(tp, dict) and tp:
        cap = tp.get("capability_id")
        if isinstance(cap, str) and not CAP_ID.match(cap):
            add("FAIL", f"capability_id format invalid: {cap!r} (expected cap-...)")
        ls = tp.get("lifecycle_status")
        if ls is not None and ls not in LIFECYCLE:
            add("FAIL", f"lifecycle_status invalid: {ls!r}")
        rl = tp.get("risk_level")
        if rl is not None and rl not in RISK:
            add("FAIL", f"risk_level invalid: {rl!r}")
        sc = tp.get("scope")
        if sc is not None and sc not in SCOPE:
            add("FAIL", f"scope invalid: {sc!r}")
        prov = tp.get("provenance_chain_id")
        if isinstance(prov, str) and prov and not PROV_ID.match(prov):
            add("FAIL", f"provenance_chain_id format invalid: {prov!r}")
        status = ls if isinstance(ls, str) else "draft"
        if status == "active" and not prov:
            add("WARN", "active capability should reference provenance_chain_id "
                        "(knowledge-architecture §4.1)")
    elif meta.get("topprism"):
        add("WARN", "topprism block found at top level; expected metadata.topprism")

    if not body.strip():
        add("FAIL", "empty body")
    elif not re.search(r"^#{1,6}\s+\S", body, re.MULTILINE):
        add("FAIL", "no Markdown heading in body")

    for m in LINK_RE.finditer(body):
        target = m.group(1)
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        t = target.split("#", 1)[0].strip()
        if t and not (path.parent / t).exists():
            add("FAIL", f"broken relative link: {target}")

    return issues


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default="./skills")
    ap.add_argument("--strict", action="store_true", help="treat WARN as failure")
    args = ap.parse_args()

    files = discover_skills(Path(args.dir))
    if not files:
        print(f"No SKILL.md files found under {args.dir}")
        return 0

    failed = warned = 0
    for f in files:
        issues = lint(f)
        lvl_fail = [i for i in issues if i["level"] == "FAIL"]
        lvl_warn = [i for i in issues if i["level"] == "WARN"]
        failed += len(lvl_fail)
        warned += len(lvl_warn)
        print(f"{'PASS' if not lvl_fail else 'FAIL'}  {f}")
        for i in issues:
            print(f"   {i['level']}: {i['msg']}")

    print(f"\n{len(files)} file(s): {failed} error(s), {warned} warning(s). "
          f"(Structural lint only — behavioral evaluation belongs to skill-tester.)")
    return 1 if failed or (args.strict and warned) else 0


if __name__ == "__main__":
    sys.exit(main())

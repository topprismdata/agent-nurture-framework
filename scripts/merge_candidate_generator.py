#!/usr/bin/env python3
"""merge_candidate_generator — lexical prefilter for consolidation review.

Replaces the former `skill_consolidation_checker.py` (ADR-001 § Migration).

Contract (docs/fragmentation-management.md):
  - Output is a CANDIDATE list. Every record carries requires_human_review=true.
  - This tool NEVER merges anything and never recommends merging on similarity
    alone; semantic overlap, evidence overlap, and contradiction checks plus a
    human decision are required downstream.

Method: stopword-tokenized Jaccard over description and body tokens,
combined 0.4/0.6, plus union-find clustering at the cluster threshold.
Thresholds are triage knobs, NOT decisions.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from anf_frontmatter import discover_skills, parse_frontmatter  # noqa: E402

_STOPWORDS = frozenset("""
a an the and or but if then else of for to in on with without by from as at is
are was were be been being do does did this that these those it its their your
our when while how what which who whom why not no yes can could should would
will shall may might must use used using make made new set get put run into
over under more less most least very much many any all each every both few
""".split())

DESC_WEIGHT = 0.4
BODY_WEIGHT = 0.6
PAIR_THRESHOLD = 0.5   # triage: report pairs above this
CLUSTER_THRESHOLD = 0.3  # triage: union-find clusters above this


def tokenize(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]{2,}", text.lower()) if w not in _STOPWORDS}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def load(path: Path) -> dict[str, Any]:
    meta, body = parse_frontmatter(path.read_text(encoding="utf-8", errors="replace"))
    sid = str(meta.get("name") or path.parent.name)
    return {
        "id": sid,
        "path": str(path),
        "desc_tokens": tokenize(str(meta.get("description", ""))),
        "body_tokens": tokenize(body),
    }


def combined(sim_desc: float, sim_body: float) -> float:
    return round(DESC_WEIGHT * sim_desc + BODY_WEIGHT * sim_body, 4)


class UF:
    def __init__(self, ids: list[str]) -> None:
        self.p = {i: i for i in ids}

    def find(self, x: str) -> str:
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a: str, b: str) -> None:
        self.p[self.find(a)] = self.find(b)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default="./skills")
    ap.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = ap.parse_args()

    root = Path(args.dir)
    skills = [load(p) for p in discover_skills(root)]
    if len(skills) < 2:
        print("fewer than two skills found; nothing to compare")
        return 0

    pairs: list[dict[str, Any]] = []
    for i in range(len(skills)):
        for j in range(i + 1, len(skills)):
            a, b = skills[i], skills[j]
            sd = jaccard(a["desc_tokens"], b["desc_tokens"])
            sb = jaccard(a["body_tokens"], b["body_tokens"])
            c = combined(sd, sb)
            if c >= CLUSTER_THRESHOLD:
                pairs.append({
                    "a": a["id"], "b": b["id"],
                    "similarity": {"description": round(sd, 4), "body": round(sb, 4), "combined": c},
                    "requires_human_review": True,
                })
    pairs.sort(key=lambda p: p["similarity"]["combined"], reverse=True)

    uf = UF([s["id"] for s in skills])
    strong_pairs = [p for p in pairs if p["similarity"]["combined"] >= PAIR_THRESHOLD]
    for p in strong_pairs:
        uf.union(p["a"], p["b"])
    clusters: dict[str, list[str]] = {}
    for s in skills:
        clusters.setdefault(uf.find(s["id"]), []).append(s["id"])
    multi = sorted(sorted(v) for v in clusters.values() if len(v) > 1)

    result = {
        "_notice": "Candidates ONLY. Lexical overlap never merges skills. "
                   "Requires semantic/evidence/contradiction checks + human decision.",
        "requires_human_review": True,
        "pair_threshold_triage": PAIR_THRESHOLD,
        "cluster_threshold_triage": CLUSTER_THRESHOLD,
        "candidates": [p for p in pairs if p["similarity"]["combined"] >= CLUSTER_THRESHOLD],
        "triage_clusters_strong": multi,
    }

    if args.format == "json":
        print(json.dumps(result, indent=2))
        return 0

    print("# Merge candidates (human review required)\n")
    print("> Lexical prefilter output. Do NOT merge on this alone — see "
          "docs/fragmentation-management.md for the full gate sequence.\n")
    if not result["candidates"]:
        print("No candidate pairs above triage threshold.")
    for p in result["candidates"]:
        mark = "strong" if p["similarity"]["combined"] >= PAIR_THRESHOLD else "weak"
        print(f"- [{mark}] {p['a']}  <->  {p['b']}  combined={p['similarity']['combined']} "
              f"(desc={p['similarity']['description']}, body={p['similarity']['body']})")
    if multi:
        print("\nTriage clusters:")
        for c in multi:
            print(f"  - {', '.join(c)}")
    print("\nNext steps per cluster: semantic overlap → evidence overlap → "
          "contradiction check → human-approved diff → post-merge validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

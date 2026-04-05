#!/usr/bin/env python3
"""
Skill Consolidation Checker for the Agent Nurture Framework.

Analyzes skill files for overlapping content using Jaccard similarity on
tokenised descriptions and body text. Identifies clusters of related skills,
flags pairs with >50 % overlap, and outputs merge recommendations.
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Extract YAML-like frontmatter and body."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", text, re.DOTALL)
    if not match:
        return {}, text
    meta: dict[str, Any] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta, match.group(2)


def discover_skills(skill_dir: Path) -> list[Path]:
    """Find all markdown skill files under *skill_dir*."""
    skills: list[Path] = []
    if not skill_dir.exists():
        return skills
    for root, _dirs, files in os.walk(skill_dir):
        for fname in files:
            if fname.lower().endswith(".md") and fname.lower() != "readme.md":
                skills.append(Path(root) / fname)
    return sorted(set(skills))


# ---------------------------------------------------------------------------
# Tokenisation & similarity
# ---------------------------------------------------------------------------

_STOPWORDS = frozenset(
    "a an the and or but in on at to for of with by from is are was were be been "
    "being have has had do does did will would could should may might shall can "
    "it its this that these those i we you they he she me us him her them my our "
    "your their his its".split()
)


def tokenize(text: str) -> set[str]:
    """Lowercase, split on non-alpha, remove stopwords, return a set."""
    words = re.findall(r"[a-z0-9]{2,}", text.lower())
    return {w for w in words if w not in _STOPWORDS}


def jaccard(set_a: set[str], set_b: set[str]) -> float:
    """Compute Jaccard similarity between two sets."""
    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


# ---------------------------------------------------------------------------
# Core analysis
# ---------------------------------------------------------------------------

def load_skill_tokens(filepath: Path) -> dict[str, Any]:
    """Load a skill file and return token sets for description and body."""
    raw = filepath.read_text(encoding="utf-8", errors="replace")
    meta, body = parse_frontmatter(raw)
    desc = meta.get("description", "")
    return {
        "path": str(filepath),
        "name": meta.get("name", filepath.stem),
        "category": filepath.parent.name,
        "desc_tokens": tokenize(desc),
        "body_tokens": tokenize(body),
    }


def compute_similarity_matrix(
    skills: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Compute pairwise similarity and return sorted list of pairs."""
    pairs: list[dict[str, Any]] = []
    n = len(skills)
    for i in range(n):
        for j in range(i + 1, n):
            a, b = skills[i], skills[j]
            desc_sim = jaccard(a["desc_tokens"], b["desc_tokens"])
            body_sim = jaccard(a["body_tokens"], b["body_tokens"])
            combined = round(0.4 * desc_sim + 0.6 * body_sim, 4)
            if combined > 0.05:  # filter out trivial similarity
                pairs.append(
                    {
                        "skill_a": a["name"],
                        "skill_b": b["name"],
                        "desc_similarity": round(desc_sim, 4),
                        "body_similarity": round(body_sim, 4),
                        "combined_similarity": combined,
                    }
                )
    return sorted(pairs, key=lambda p: p["combined_similarity"], reverse=True)


def find_clusters(
    skills: list[dict[str, Any]], pairs: list[dict[str, Any]], threshold: float = 0.3
) -> list[list[str]]:
    """Group skills into clusters using union-find over similar pairs."""
    parent: dict[str, str] = {s["name"]: s["name"] for s in skills}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x: str, y: str) -> None:
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    for p in pairs:
        if p["combined_similarity"] >= threshold:
            union(p["skill_a"], p["skill_b"])

    clusters: dict[str, list[str]] = defaultdict(list)
    for s in skills:
        clusters[find(s["name"])].append(s["name"])
    return [sorted(members) for members in clusters.values() if len(members) > 1]


def generate_merge_recommendations(
    pairs: list[dict[str, Any]], threshold: float = 0.5
) -> list[dict[str, Any]]:
    """Flag pairs whose overlap exceeds *threshold*."""
    return [
        {
            "skill_a": p["skill_a"],
            "skill_b": p["skill_b"],
            "similarity": p["combined_similarity"],
            "recommendation": "merge"
            if p["combined_similarity"] >= 0.7
            else "review for overlap",
        }
        for p in pairs
        if p["combined_similarity"] >= threshold
    ]


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def format_markdown(
    pairs: list[dict[str, Any]],
    clusters: list[list[str]],
    merges: list[dict[str, Any]],
    total_skills: int,
) -> str:
    lines: list[str] = []
    lines.append("# Skill Consolidation Report\n")
    lines.append(f"- **Total skills analysed:** {total_skills}")
    lines.append(f"- **Similarity pairs found:** {len(pairs)}")
    lines.append(f"- **Clusters detected:** {len(clusters)}")
    lines.append(f"- **Merge recommendations:** {len(merges)}")

    if merges:
        lines.append("\n## Merge / Review Recommendations\n")
        lines.append("| Skill A | Skill B | Similarity | Action |")
        lines.append("|---------|---------|------------|--------|")
        for m in merges:
            lines.append(
                f"| {m['skill_a']} | {m['skill_b']} "
                f"| {m['similarity']:.2f} | {m['recommendation']} |"
            )

    if clusters:
        lines.append("\n## Skill Clusters (similarity >= 0.30)\n")
        for idx, cluster in enumerate(clusters, 1):
            lines.append(f"### Cluster {idx}")
            for name in cluster:
                lines.append(f"- {name}")
            lines.append("")

    if pairs:
        lines.append("\n## Top Similar Pairs\n")
        lines.append("| Skill A | Skill B | Desc Sim | Body Sim | Combined |")
        lines.append("|---------|---------|----------|----------|----------|")
        for p in pairs[:20]:
            lines.append(
                f"| {p['skill_a']} | {p['skill_b']} "
                f"| {p['desc_similarity']:.2f} | {p['body_similarity']:.2f} "
                f"| {p['combined_similarity']:.2f} |"
            )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check skill files for overlap and produce consolidation recommendations."
    )
    parser.add_argument(
        "--dir",
        type=str,
        default=None,
        help="Path to skill directory (default: ./skills or ~/.claude/skills)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="Similarity threshold for flagging overlap (default: 0.5)",
    )
    parser.add_argument(
        "--cluster-threshold",
        type=float,
        default=0.3,
        help="Similarity threshold for clustering (default: 0.3)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output base path (default: ./consolidation-report). "
        "Appends .json and .md automatically.",
    )
    args = parser.parse_args()

    # Resolve skill directory
    if args.dir:
        skill_dir = Path(args.dir).resolve()
    else:
        skill_dir = Path("./skills").resolve()
        if not skill_dir.exists():
            skill_dir = Path.home() / ".claude" / "skills"

    if not skill_dir.exists():
        print(f"Error: Skill directory not found: {skill_dir}", file=sys.stderr)
        sys.exit(1)

    skill_files = discover_skills(skill_dir)
    if len(skill_files) < 2:
        print("Need at least 2 skill files to check consolidation.", file=sys.stderr)
        sys.exit(0)

    print(f"Analysing {len(skill_files)} skill(s) in {skill_dir} ...")

    skills = [load_skill_tokens(fp) for fp in skill_files]
    pairs = compute_similarity_matrix(skills)
    clusters = find_clusters(skills, pairs, threshold=args.cluster_threshold)
    merges = generate_merge_recommendations(pairs, threshold=args.threshold)

    report: dict[str, Any] = {
        "total_skills": len(skills),
        "similarity_threshold": args.threshold,
        "cluster_threshold": args.cluster_threshold,
        "pairs": pairs,
        "clusters": clusters,
        "merge_recommendations": merges,
    }

    base = args.output or "./consolidation-report"
    json_path = Path(f"{base}.json")
    md_path = Path(f"{base}.md")

    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"JSON report written to {json_path}")

    md_content = format_markdown(pairs, clusters, merges, len(skills))
    md_path.write_text(md_content, encoding="utf-8")
    print(f"Markdown report written to {md_path}")

    print(
        f"\nSummary: {len(merges)} merge recommendation(s), "
        f"{len(clusters)} cluster(s) detected."
    )


if __name__ == "__main__":
    main()

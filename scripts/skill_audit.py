#!/usr/bin/env python3
"""
Skill Audit Tool for the Agent Nurture Framework.

Assesses the quality of SKILL.md files in a skill library, scoring each on
five dimensions: description quality, structure, examples, metadata, and
content quality. Produces JSON and Markdown reports.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Extract YAML-like frontmatter (between --- delimiters) and body."""
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
    """Find all SKILL.md files under *skill_dir*, including nested dirs."""
    skills: list[Path] = []
    if not skill_dir.exists():
        return skills
    for root, _dirs, files in os.walk(skill_dir):
        for fname in files:
            if fname.lower() == "skill.md":
                skills.append(Path(root) / fname)
            elif fname.lower().endswith(".md") and fname.lower() != "readme.md":
                # Also accept individual markdown skill files
                skills.append(Path(root) / fname)
    return sorted(set(skills))


# ---------------------------------------------------------------------------
# Scoring helpers (each returns 0-10)
# ---------------------------------------------------------------------------

def score_description(content: str, meta: dict[str, Any]) -> float:
    """Description quality: presence and detail of a description."""
    desc = meta.get("description", "")
    if not desc:
        # Try to find a description heading in the body
        m = re.search(r"(?:^|\n)#+\s*Description\s*\n+(.*?)(?=\n#|\Z)", content, re.DOTALL)
        if m:
            desc = m.group(1).strip()
    words = len(desc.split())
    if words == 0:
        return 0.0
    if words < 10:
        return 3.0
    if words < 30:
        return 6.0
    if words < 60:
        return 8.0
    return 10.0


def score_structure(content: str) -> float:
    """Structure: number and depth of markdown headings."""
    headings = re.findall(r"^(#{1,4})\s+(.+)$", content, re.MULTILINE)
    if not headings:
        return 0.0
    level_counts: dict[int, int] = {}
    for hashes, _title in headings:
        level_counts[len(hashes)] = level_counts.get(len(hashes), 0) + 1
    # Expect at least h2 sections and some h3 detail
    score = min(len(headings) / 6, 1.0) * 7  # up to 7 pts for heading count
    if 2 in level_counts and 3 in level_counts:
        score += 3.0
    elif 2 in level_counts:
        score += 1.5
    return min(score, 10.0)


def score_examples(content: str) -> float:
    """Examples: presence of code blocks or example sections."""
    code_blocks = re.findall(r"```[\s\S]*?```", content)
    example_sections = len(re.findall(r"(?i)#.*example", content))
    score = 0.0
    score += min(len(code_blocks) * 2.5, 6.0)
    score += min(example_sections * 2.0, 4.0)
    return min(score, 10.0)


def score_metadata(meta: dict[str, Any]) -> float:
    """Metadata: richness of YAML frontmatter fields."""
    expected = {"name", "description", "version", "author", "category", "tags", "created", "updated"}
    present = sum(1 for k in expected if k in meta and meta[k])
    return round(min(present / len(expected) * 10, 10.0), 1)


def score_content_quality(content: str) -> float:
    """Content quality: word count, list usage, internal links."""
    words = len(content.split())
    lists = len(re.findall(r"^\s*[-*]\s+", content, re.MULTILINE))
    links = len(re.findall(r"\[.*?\]\(.*?\)", content))
    score = 0.0
    if words > 100:
        score += 3.0
    elif words > 50:
        score += 1.5
    score += min(lists / 5, 1.0) * 3.5
    score += min(links / 3, 1.0) * 3.5
    return min(score, 10.0)


# ---------------------------------------------------------------------------
# Main audit logic
# ---------------------------------------------------------------------------

def audit_skill(filepath: Path) -> dict[str, Any]:
    """Score a single skill file and return a result dict."""
    raw = filepath.read_text(encoding="utf-8", errors="replace")
    meta, body = parse_frontmatter(raw)

    dims = {
        "description": score_description(body, meta),
        "structure": score_structure(body),
        "examples": score_examples(body),
        "metadata": score_metadata(meta),
        "content_quality": score_content_quality(body),
    }
    overall = round(sum(dims.values()) / len(dims), 2)

    # Determine relative path category prefix
    rel = str(filepath)
    category = filepath.parent.name

    # File modification time
    mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
    age_days = (datetime.now() - mtime).days

    return {
        "path": str(filepath),
        "name": meta.get("name", filepath.stem),
        "category": category,
        "dimensions": dims,
        "overall_score": overall,
        "last_modified": mtime.isoformat(),
        "age_days": age_days,
        "word_count": len(body.split()),
    }


def generate_report(results: list[dict[str, Any]]) -> dict[str, Any]:
    """Produce a summary report from individual skill audits."""
    if not results:
        return {"total_skills": 0, "summary": "No skills found."}

    by_category: dict[str, list[dict[str, Any]]] = {}
    for r in results:
        by_category.setdefault(r["category"], []).append(r)

    scores = [r["overall_score"] for r in results]
    avg_score = round(sum(scores) / len(scores), 2)
    sorted_by_score = sorted(results, key=lambda r: r["overall_score"], reverse=True)

    stale_threshold = 30
    stale_skills = [r for r in results if r["age_days"] > stale_threshold]

    return {
        "generated_at": datetime.now().isoformat(),
        "total_skills": len(results),
        "average_score": avg_score,
        "categories": {cat: len(skills) for cat, skills in by_category.items()},
        "top_skills": [
            {"name": s["name"], "score": s["overall_score"]}
            for s in sorted_by_score[:5]
        ],
        "bottom_skills": [
            {"name": s["name"], "score": s["overall_score"]}
            for s in sorted_by_score[-5:]
        ],
        "stale_skills": [
            {"name": s["name"], "age_days": s["age_days"]}
            for s in stale_skills
        ],
        "skills": results,
    }


def format_markdown(report: dict[str, Any]) -> str:
    """Render the report as a human-readable Markdown string."""
    lines: list[str] = []
    lines.append("# Skill Audit Report")
    lines.append(f"\nGenerated: {report['generated_at']}")
    lines.append(f"\n## Summary")
    lines.append(f"- **Total skills:** {report['total_skills']}")
    lines.append(f"- **Average quality score:** {report['average_score']}/10")
    lines.append(f"- **Categories:** {len(report['categories'])}")

    if report["categories"]:
        lines.append("\n### Skills by Category")
        lines.append("")
        lines.append("| Category | Count |")
        lines.append("|----------|-------|")
        for cat, count in sorted(report["categories"].items()):
            lines.append(f"| {cat} | {count} |")

    if report["top_skills"]:
        lines.append("\n### Top Skills")
        lines.append("")
        lines.append("| Name | Score |")
        lines.append("|------|-------|")
        for s in report["top_skills"]:
            lines.append(f"| {s['name']} | {s['score']} |")

    if report["bottom_skills"]:
        lines.append("\n### Bottom Skills")
        lines.append("")
        lines.append("| Name | Score |")
        lines.append("|------|-------|")
        for s in report["bottom_skills"]:
            lines.append(f"| {s['name']} | {s['score']} |")

    if report["stale_skills"]:
        lines.append("\n### Stale Skills (>30 days since last update)")
        lines.append("")
        for s in report["stale_skills"]:
            lines.append(f"- **{s['name']}** — {s['age_days']} days old")

    if report["skills"]:
        lines.append("\n### All Skills Detail")
        lines.append("")
        lines.append("| Name | Category | Score | Age (days) | Words |")
        lines.append("|------|----------|-------|------------|-------|")
        for s in sorted(report["skills"], key=lambda x: x["overall_score"], reverse=True):
            lines.append(
                f"| {s['name']} | {s['category']} | {s['overall_score']} | {s['age_days']} | {s['word_count']} |"
            )

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit skill files and produce quality reports."
    )
    parser.add_argument(
        "--dir",
        type=str,
        default=None,
        help="Path to skill directory (default: ./skills or ~/.claude/skills)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output base path (default: ./skill-audit-report). "
        "Appends .json and .md automatically.",
    )
    parser.add_argument(
        "--json-only",
        action="store_true",
        help="Only output JSON report.",
    )
    parser.add_argument(
        "--markdown-only",
        action="store_true",
        help="Only output Markdown report.",
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

    # Discover and audit
    skill_files = discover_skills(skill_dir)
    if not skill_files:
        print(f"No skill files found in {skill_dir}", file=sys.stderr)
        sys.exit(0)

    print(f"Auditing {len(skill_files)} skill(s) in {skill_dir} ...")

    results = [audit_skill(fp) for fp in skill_files]
    report = generate_report(results)

    # Determine output paths
    base = args.output or "./skill-audit-report"
    json_path = Path(f"{base}.json")
    md_path = Path(f"{base}.md")

    if not args.markdown_only:
        json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"JSON report written to {json_path}")

    if not args.json_only:
        md_content = format_markdown(report)
        md_path.write_text(md_content, encoding="utf-8")
        print(f"Markdown report written to {md_path}")

    print(f"\nSummary: {report['total_skills']} skills, average score {report['average_score']}/10")


if __name__ == "__main__":
    main()

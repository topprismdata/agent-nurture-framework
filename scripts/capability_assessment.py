from __future__ import annotations

#!/usr/bin/env python3
"""
Capability Assessment Tool for the Agent Nurture Framework.

Interactive tool that loads a capability matrix template, prompts the user for
ratings on each dimension, calculates an overall score, and generates an
assessment report. Supports custom dimensions via a JSON file.

Uses a 1-5 Dreyfus scale:
  1 = Novice, 2 = Advanced Beginner, 3 = Competent, 4 = Proficient, 5 = Expert
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


# Dreyfus level labels for the 1-5 scale
DREYFUS_LABELS: dict[int, str] = {
    1: "Novice",
    2: "Advanced Beginner",
    3: "Competent",
    4: "Proficient",
    5: "Expert",
}

# Default capability dimensions with descriptions
DEFAULT_DIMENSIONS: list[dict[str, str]] = [
    {"name": "Domain Knowledge", "description": "Depth and breadth of domain-specific knowledge"},
    {"name": "Task Execution", "description": "Ability to complete assigned tasks accurately"},
    {"name": "Error Recovery", "description": "Handling of edge cases, errors, and unexpected inputs"},
    {"name": "Knowledge Recall", "description": "Retrieval and application of previously learned skills"},
    {"name": "Reasoning Depth", "description": "Quality of analytical and logical reasoning"},
    {"name": "Communication Clarity", "description": "Clarity and usefulness of responses and explanations"},
    {"name": "Autonomy", "description": "Ability to work independently without constant guidance"},
    {"name": "Adaptability", "description": "Flexibility when facing new or changed requirements"},
    {"name": "Consistency", "description": "Reliability of output quality across sessions"},
    {"name": "Learning Velocity", "description": "Rate of improvement over time with accumulated experience"},
]


def load_dimensions(template_path: str | None) -> list[dict[str, str]]:
    """Load dimensions from a JSON file, or return defaults."""
    if template_path is None:
        return DEFAULT_DIMENSIONS

    path = Path(template_path)
    if not path.exists():
        print(f"Warning: Template file not found at {path}, using defaults.", file=sys.stderr)
        return DEFAULT_DIMENSIONS

    raw = path.read_text(encoding="utf-8")

    # Try JSON first
    try:
        data = json.loads(raw)
        if isinstance(data, list) and all("name" in d for d in data):
            return data
    except json.JSONDecodeError:
        pass

    # Try parsing a simple markdown table format
    dimensions: list[dict[str, str]] = []
    for line in raw.splitlines():
        line = line.strip()
        if line.startswith("|") and not line.startswith("|--") and not line.startswith("| Dimension"):
            cells = [c.strip() for c in line.split("|") if c.strip()]
            if len(cells) >= 1:
                dimensions.append(
                    {"name": cells[0], "description": cells[1] if len(cells) > 1 else ""}
                )
    if dimensions:
        return dimensions

    print("Warning: Could not parse template, using defaults.", file=sys.stderr)
    return DEFAULT_DIMENSIONS


def prompt_rating(dimension: dict[str, str]) -> int:
    """Prompt the user for a rating 1-5 on one dimension (Dreyfus scale)."""
    name = dimension["name"]
    desc = dimension.get("description", "")
    while True:
        try:
            if desc:
                raw = input(f"  {name} — {desc}\n  Rating (1-5, Dreyfus scale): ")
            else:
                raw = input(f"  {name} — Rating (1-5, Dreyfus scale): ")
            rating = int(raw.strip())
            if 1 <= rating <= 5:
                return rating
            print("    Please enter a number between 1 and 5.")
        except (ValueError, EOFError):
            print("    Invalid input. Please enter a number between 1 and 5.")


def collect_ratings(dimensions: list[dict[str, str]]) -> list[dict[str, Any]]:
    """Collect ratings for all dimensions interactively."""
    results: list[dict[str, Any]] = []
    print("\nRate your agent on each dimension using the Dreyfus scale:")
    print("  1 = Novice, 2 = Advanced Beginner, 3 = Competent, 4 = Proficient, 5 = Expert\n")
    for dim in dimensions:
        rating = prompt_rating(dim)
        note = input(f"  Notes (optional, press Enter to skip): ").strip()
        results.append(
            {"name": dim["name"], "description": dim.get("description", ""), "rating": rating, "notes": note}
        )
    return results


def compute_scores(results: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute overall score and categorise the agent level."""
    ratings = [r["rating"] for r in results]
    avg = round(sum(ratings) / len(ratings), 2) if ratings else 0
    minimum = min(ratings) if ratings else 0
    maximum = max(ratings) if ratings else 0
    std_dev = round(
        (sum((r - avg) ** 2 for r in ratings) / len(ratings)) ** 0.5, 2
    ) if ratings else 0

    # Map average to closest Dreyfus level (1-5)
    level_idx = max(1, min(5, round(avg)))
    level = DREYFUS_LABELS[level_idx]

    return {
        "average": avg,
        "min": minimum,
        "max": maximum,
        "std_dev": std_dev,
        "level": level,
    }


def format_report(results: list[dict[str, Any]], scores: dict[str, Any]) -> str:
    """Render an assessment report as Markdown."""
    lines: list[str] = []
    lines.append("# Capability Assessment Report\n")
    lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    lines.append("## Overall Score\n")
    lines.append(f"- **Average:** {scores['average']}/5")
    lines.append(f"- **Range:** {scores['min']} — {scores['max']}")
    lines.append(f"- **Std Deviation:** {scores['std_dev']}")
    lines.append(f"- **Dreyfus Level:** {scores['level']}\n")
    lines.append("## Dimension Details\n")
    lines.append("| Dimension | Rating | Dreyfus Level | Notes |")
    lines.append("|-----------|--------|---------------|-------|")
    for r in results:
        notes = r.get("notes", "").replace("|", "/") or "—"
        dreyfus = DREYFUS_LABELS.get(r["rating"], "Unknown")
        lines.append(f"| {r['name']} | {r['rating']} | {dreyfus} | {notes} |")
    lines.append("")
    lines.append("## Recommendations\n")
    weak = [r for r in results if r["rating"] <= 2]
    if weak:
        lines.append("### Priority Improvement Areas\n")
        for r in weak:
            lines.append(f"- **{r['name']}** (scored {r['rating']}/5 — {DREYFUS_LABELS.get(r['rating'], '')})")
            if r.get("notes"):
                lines.append(f"  - Notes: {r['notes']}")
    strong = [r for r in results if r["rating"] >= 4]
    if strong:
        lines.append("\n### Strengths to Leverage\n")
        for r in strong:
            lines.append(f"- **{r['name']}** (scored {r['rating']}/5 — {DREYFUS_LABELS.get(r['rating'], '')})")
    if not weak and not strong:
        lines.append("All dimensions are in the mid-range. Consider focusing on domain-specific scenarios to push specific dimensions higher.")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Interactive capability assessment for an AI agent."
    )
    parser.add_argument(
        "--template",
        type=str,
        default=None,
        help="Path to a capability matrix template (JSON or Markdown). Uses built-in defaults if omitted.",
    )
    parser.add_argument(
        "--dimensions",
        type=str,
        nargs="*",
        default=None,
        help="Custom dimension names to use instead of the defaults.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output base path (default: ./capability-assessment). "
        "Appends .json and .md automatically.",
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Generate a blank template instead of running the interactive assessment.",
    )
    args = parser.parse_args()

    # Build dimension list
    if args.dimensions:
        dimensions = [{"name": d, "description": ""} for d in args.dimensions]
    else:
        dimensions = load_dimensions(args.template)

    if args.non_interactive:
        lines = ["# Capability Assessment Template\n"]
        lines.append("Rate each dimension from 1 to 5 using the Dreyfus scale:")
        lines.append("1 = Novice, 2 = Advanced Beginner, 3 = Competent, 4 = Proficient, 5 = Expert\n")
        lines.append("| Dimension | Description | Rating | Notes |")
        lines.append("|-----------|-------------|--------|-------|")
        for d in dimensions:
            lines.append(f"| {d['name']} | {d.get('description', '')} | | |")
        base = args.output or "./capability-assessment-template"
        template_path = Path(f"{base}.md")
        template_path.write_text(
            "\n".join(lines), encoding="utf-8"
        )
        print(f"Blank template written to {template_path}")
        return

    # Interactive assessment
    print("=" * 50)
    print("  Agent Capability Assessment")
    print("=" * 50)
    results = collect_ratings(dimensions)
    scores = compute_scores(results)

    report_md = format_report(results, scores)
    report_json = {
        "timestamp": datetime.now().isoformat(),
        "dimensions": results,
        "scores": scores,
    }

    base = args.output or "./capability-assessment"
    json_path = Path(f"{base}.json")
    md_path = Path(f"{base}.md")

    json_path.write_text(json.dumps(report_json, indent=2, ensure_ascii=False), encoding="utf-8")
    md_path.write_text(report_md, encoding="utf-8")

    print(f"\n{'=' * 50}")
    print(f"  Overall Score: {scores['average']}/5  —  Level: {scores['level']}")
    print(f"{'=' * 50}")
    print(f"\nReports saved to {json_path} and {md_path}")


if __name__ == "__main__":
    main()

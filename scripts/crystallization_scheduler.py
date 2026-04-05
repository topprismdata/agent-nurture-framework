#!/usr/bin/env python3
"""
Crystallization Scheduler for the Agent Nurture Framework.

Monitors the age and volume of skill/memory files, checks how long since the
last crystallization event, and outputs recommendations for when the next
crystallization session should occur.
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
# Helpers
# ---------------------------------------------------------------------------

def discover_files(directory: Path, extension: str = ".md") -> list[Path]:
    """Recursively find files with the given extension."""
    found: list[Path] = []
    if not directory.exists():
        return found
    for root, _dirs, files in os.walk(directory):
        for fname in files:
            if fname.lower().endswith(extension):
                found.append(Path(root) / fname)
    return sorted(found)


def file_age_days(filepath: Path) -> int:
    """Return the number of days since the file was last modified."""
    mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
    return (datetime.now() - mtime).days


def file_age_stamp(filepath: Path) -> str:
    """Return ISO-formatted last-modified timestamp."""
    return datetime.fromtimestamp(filepath.stat().st_mtime).strftime("%Y-%m-%d")


def classify_layer(filepath: Path, skill_dir: Path) -> str:
    """Attempt to classify a file into L1/L2/L3 by its path."""
    rel = str(filepath.relative_to(skill_dir))
    parts = Path(rel).parts
    if len(parts) >= 2:
        folder = parts[0].lower()
        if folder in ("l1", "constitutional", "core", "identity"):
            return "L1"
        if folder in ("l2", "skills", "skill"):
            return "L2"
        if folder in ("l3", "experiential", "experience", "logs", "memory"):
            return "L3"
    return "unknown"


def find_crystallization_log(skill_dir: Path) -> dict[str, Any] | None:
    """Look for a crystallization log file and parse the last entry."""
    candidates = [
        skill_dir / "crystallization-log.json",
        skill_dir / ".crystallization-log.json",
        skill_dir / "meta" / "crystallization-log.json",
    ]
    for candidate in candidates:
        if candidate.exists():
            try:
                data = json.loads(candidate.read_text(encoding="utf-8"))
                if isinstance(data, list) and data:
                    return data[-1]
                if isinstance(data, dict):
                    return data
            except (json.JSONDecodeError, OSError):
                continue
    return None


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

STALE_THRESHOLD_L1 = 60  # days
STALE_THRESHOLD_L2 = 30
STALE_THRESHOLD_L3 = 14


def analyse(skill_dir: Path, memory_dir: Path | None) -> dict[str, Any]:
    """Run the full staleness and crystallization analysis."""
    now = datetime.now()
    all_files = discover_files(skill_dir)

    if memory_dir:
        all_files.extend(discover_files(memory_dir))

    if not all_files:
        return {
            "total_files": 0,
            "status": "empty",
            "message": "No files found in the specified directories.",
        }

    # Classify files by layer
    layers: dict[str, list[Path]] = {"L1": [], "L2": [], "L3": [], "unknown": []}
    for fp in all_files:
        layer = classify_layer(fp, skill_dir)
        layers[layer].append(fp)

    # Staleness analysis per layer
    staleness: dict[str, Any] = {}
    stale_thresholds = {"L1": STALE_THRESHOLD_L1, "L2": STALE_THRESHOLD_L2, "L3": STALE_THRESHOLD_L3}
    for layer, files in layers.items():
        if not files or layer == "unknown":
            continue
        ages = [file_age_days(f) for f in files]
        threshold = stale_thresholds.get(layer, 30)
        stale_files = [f for f, age in zip(files, ages) if age > threshold]
        staleness[layer] = {
            "file_count": len(files),
            "avg_age_days": round(sum(ages) / len(ages), 1),
            "max_age_days": max(ages),
            "stale_count": len(stale_files),
            "stale_files": [
                {"path": str(f), "age_days": file_age_days(f)}
                for f in stale_files
            ],
            "threshold_days": threshold,
        }

    # Check last crystallization event
    last_crystal = find_crystallization_log(skill_dir)
    days_since_crystal = None
    if last_crystal:
        ts = last_crystal.get("timestamp", last_crystal.get("date", ""))
        if ts:
            try:
                last_dt = datetime.fromisoformat(ts)
                days_since_crystal = (now - last_dt).days
            except ValueError:
                pass

    # Build recommendations
    recommendations: list[str] = []

    for layer, info in staleness.items():
        if info["stale_count"] > 0:
            recommendations.append(
                f"{layer}: {info['stale_count']} file(s) exceed the staleness threshold "
                f"of {info['threshold_days']} days. Consider crystallization."
            )

    if days_since_crystal is not None and days_since_crystal > 14:
        recommendations.append(
            f"Last crystallation was {days_since_crystal} days ago. "
            "Schedule a crystallization session soon."
        )
    elif days_since_crystal is None:
        recommendations.append(
            "No crystallization log found. Consider creating one to track crystallization history."
        )

    # L3 volume heuristic — if there are many L3 files relative to L2, crystallization is due
    l3_count = len(layers.get("L3", []))
    l2_count = len(layers.get("L2", []))
    if l3_count > 0 and l3_count > l2_count * 3:
        recommendations.append(
            f"L3 experiential files ({l3_count}) significantly outnumber L2 skills ({l2_count}). "
            "A crystallization pass would convert raw experience into reusable skills."
        )

    status = "ok"
    if any(s.get("stale_count", 0) > 0 for s in staleness.values()):
        status = "staleness_detected"
    elif days_since_crystal is not None and days_since_crystal > 14:
        status = "crystallization_overdue"

    return {
        "timestamp": now.isoformat(),
        "total_files": len(all_files),
        "layers": {k: len(v) for k, v in layers.items()},
        "staleness": staleness,
        "last_crystallization": last_crystal,
        "days_since_last_crystallization": days_since_crystal,
        "status": status,
        "recommendations": recommendations,
    }


def format_markdown(report: dict[str, Any]) -> str:
    """Render the analysis as Markdown."""
    lines: list[str] = []
    lines.append("# Crystallization Schedule Report\n")
    lines.append(f"Generated: {report['timestamp']}\n")
    lines.append(f"**Status:** {report['status'].replace('_', ' ').title()}\n")
    lines.append(f"**Total files:** {report['total_files']}\n")
    lines.append("## Files by Layer\n")
    lines.append("| Layer | File Count |")
    lines.append("|-------|-----------|")
    for layer in ("L1", "L2", "L3", "unknown"):
        count = report["layers"].get(layer, 0)
        if count:
            lines.append(f"| {layer} | {count} |")

    if report["staleness"]:
        lines.append("\n## Staleness Analysis\n")
        for layer, info in report["staleness"].items():
            lines.append(f"### {layer}")
            lines.append(f"- Files: {info['file_count']}")
            lines.append(f"- Average age: {info['avg_age_days']} days")
            lines.append(f"- Oldest file: {info['max_age_days']} days")
            lines.append(f"- Stale files: {info['stale_count']} (threshold: {info['threshold_days']} days)")
            if info["stale_files"]:
                for sf in info["stale_files"]:
                    lines.append(f"  - {sf['path']} ({sf['age_days']} days)")
            lines.append("")

    if report["days_since_last_crystallization"] is not None:
        lines.append(f"\n## Last Crystallization\n")
        lines.append(f"- **Days ago:** {report['days_since_last_crystallization']}")
    else:
        lines.append("\n## Last Crystallization\n")
        lines.append("- No crystallization log found.")

    if report["recommendations"]:
        lines.append("\n## Recommendations\n")
        for rec in report["recommendations"]:
            lines.append(f"- {rec}")
    else:
        lines.append("\n## Recommendations\n")
        lines.append("No immediate actions required. Continue normal operations.")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Monitor skill staleness and recommend crystallization timing."
    )
    parser.add_argument(
        "--dir",
        type=str,
        default=None,
        help="Path to skill directory (default: ./skills or ~/.claude/skills)",
    )
    parser.add_argument(
        "--memory-dir",
        type=str,
        default=None,
        help="Optional separate experiential/memory directory.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output base path (default: ./crystallization-report). "
        "Appends .json and .md automatically.",
    )
    args = parser.parse_args()

    # Resolve directories
    if args.dir:
        skill_dir = Path(args.dir).resolve()
    else:
        skill_dir = Path("./skills").resolve()
        if not skill_dir.exists():
            skill_dir = Path.home() / ".claude" / "skills"

    memory_dir = Path(args.memory_dir).resolve() if args.memory_dir else None

    if not skill_dir.exists() and (memory_dir is None or not memory_dir.exists()):
        print(f"Error: Directory not found: {skill_dir}", file=sys.stderr)
        sys.exit(1)

    report = analyse(skill_dir, memory_dir)

    base = args.output or "./crystallization-report"
    json_path = Path(f"{base}.json")
    md_path = Path(f"{base}.md")

    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"JSON report written to {json_path}")

    md_content = format_markdown(report)
    md_path.write_text(md_content, encoding="utf-8")
    print(f"Markdown report written to {md_path}")

    print(f"\nStatus: {report['status'].replace('_', ' ').title()}")
    if report["recommendations"]:
        print("\nRecommendations:")
        for rec in report["recommendations"]:
            print(f"  - {rec}")
    else:
        print("\nNo immediate actions required.")


if __name__ == "__main__":
    main()

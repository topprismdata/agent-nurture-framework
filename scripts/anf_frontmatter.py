#!/usr/bin/env python3
"""Shared frontmatter parsing for ANF adapter scripts.

Parses YAML frontmatter from SKILL.md files. Uses PyYAML when available and
falls back to a conservative line-oriented parser otherwise. Also provides
SKILL.md discovery.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
    _YAML_AVAILABLE = True
except ImportError:  # pragma: no cover
    _YAML_AVAILABLE = False

_FM_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", re.DOTALL)


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Return (metadata, body). Missing/invalid frontmatter yields ({}, stripped text)."""
    m = _FM_RE.match(text)
    if not m:
        return {}, text.strip()
    raw, body = m.group(1), m.group(2)
    meta = _parse_yaml(raw) if _YAML_AVAILABLE else _parse_fallback(raw)
    return (meta or {}), body


def _parse_yaml(raw: str) -> dict[str, Any] | None:
    try:
        loaded = yaml.safe_load(raw)
        return loaded if isinstance(loaded, dict) else None
    except Exception:
        return None


def _parse_fallback(raw: str) -> dict[str, Any] | None:
    """Line parser handling `key: value`, simple lists, one nesting level."""
    meta: dict[str, Any] = {}
    current_key: str | None = None
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith(("  ", "- ")):
            if current_key is None:
                continue
            item = line.strip()[2:].strip() if line.strip().startswith("- ") else line.strip()
            bucket = meta[current_key]
            if isinstance(bucket, list):
                bucket.append(item)
            elif isinstance(bucket, dict):
                sub = item.split(":", 1)
                if len(sub) == 2:
                    bucket[sub[0].strip()] = sub[1].strip()
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key, value = key.strip(), value.strip()
        if not key:
            continue
        if value == "":
            meta[key] = []
            current_key = key
        else:
            meta[key] = value.strip("'\"")
            current_key = None
    return meta or None


def discover_skills(skill_dir: Path) -> list[Path]:
    """Find SKILL.md files under skill_dir (any depth), sorted."""
    return sorted(p for p in skill_dir.rglob("SKILL.md") if p.is_file())

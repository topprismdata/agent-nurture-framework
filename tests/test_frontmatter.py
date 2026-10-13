"""Tests for the shared frontmatter parser used by all ANF adapter scripts."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import anf_frontmatter as afm  # noqa: E402

SAMPLE = """---
name: demo-skill
description: a demo
tags:
  - alpha
  - beta
---

# Body heading
"""


def test_parse_flat_fields() -> None:
    meta, body = afm.parse_frontmatter(SAMPLE)
    assert meta["name"] == "demo-skill"
    assert meta["description"] == "a demo"
    assert meta["tags"] == ["alpha", "beta"]
    assert body.startswith("# Body heading")


def test_missing_frontmatter_returns_empty_meta() -> None:
    meta, body = afm.parse_frontmatter("# just a doc\n")
    assert meta == {}
    assert "just a doc" in body


def test_fallback_parser_handles_flat_and_lists(monkeypatch) -> None:
    monkeypatch.setattr(afm, "_YAML_AVAILABLE", False)
    meta, body = afm.parse_frontmatter(SAMPLE)
    assert meta["name"] == "demo-skill"
    assert meta["description"] == "a demo"
    assert meta["tags"] == ["alpha", "beta"]


def test_quoted_values_stripped() -> None:
    meta, _ = afm.parse_frontmatter('---\nname: "quoted-name"\n---\n\nx\n')
    assert meta["name"] == "quoted-name"


def test_discover_skills_finds_and_sorts(tmp_path: Path) -> None:
    (tmp_path / "b").mkdir()
    (tmp_path / "a").mkdir()
    (tmp_path / "a" / "SKILL.md").write_text(SAMPLE, encoding="utf-8")
    (tmp_path / "b" / "SKILL.md").write_text(SAMPLE, encoding="utf-8")
    (tmp_path / "b" / "other.md").write_text(SAMPLE, encoding="utf-8")
    found = afm.discover_skills(tmp_path)
    assert [p.parent.name for p in found] == ["a", "b"]

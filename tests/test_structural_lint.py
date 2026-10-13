"""Tests for structural_lint: vocabulary enforcement + structural checks."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import structural_lint as sl  # noqa: E402

BASE = """---
name: demo-skill
description: a demo
metadata:
  topprism:
    capability_id: cap-demo-001
    lifecycle_status: {status}
    risk_level: low
    scope: project
    provenance_chain_id: prov-demo-001
---

# Demo
"""


def _write(tmp_path: Path, text: str) -> Path:
    p = tmp_path / "SKILL.md"
    p.write_text(text, encoding="utf-8")
    return p


def test_canonical_status_passes(tmp_path: Path) -> None:
    issues = sl.lint(_write(tmp_path, BASE.format(status="candidate")))
    assert [i for i in issues if i["level"] == "FAIL"] == []


def test_legacy_status_fails(tmp_path: Path) -> None:
    issues = sl.lint(_write(tmp_path, BASE.format(status="draft")))
    assert any(i["level"] == "FAIL" and "lifecycle_status" in i["msg"] for i in issues)


def test_observed_without_provenance_warns(tmp_path: Path) -> None:
    text = BASE.format(status="observed").replace(
        "    provenance_chain_id: prov-demo-001\n", ""
    )
    issues = sl.lint(_write(tmp_path, text))
    assert any(i["level"] == "WARN" and "provenance" in i["msg"] for i in issues)


def test_broken_relative_link_fails(tmp_path: Path) -> None:
    text = BASE.format(status="candidate").replace("# Demo\n", "# Demo\n\n[x](./missing.md)\n")
    issues = sl.lint(_write(tmp_path, text))
    assert any(i["level"] == "FAIL" and "broken relative link" in i["msg"] for i in issues)


def test_missing_frontmatter_fails(tmp_path: Path) -> None:
    issues = sl.lint(_write(tmp_path, "# no fm\n"))
    assert any(i["level"] == "FAIL" and "frontmatter" in i["msg"] for i in issues)

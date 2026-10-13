"""ANF schema conformance tests (closes the "no tests" risk in 04_ARCHITECTURE_REVIEW).

Every schema must be a valid draft 2020-12 meta-schema; every example under
examples/schemas/<name>/{valid,invalid}/ must conform / be rejected
respectively. The lifecycle enum is pinned to the ADR-002 canonical
vocabulary so a silent re-introduction of the legacy enum fails CI.
"""
from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "schemas"
EXAMPLES = ROOT / "examples" / "schemas"

# ADR-002: Charter §3.2 Lifecycle Protocol is canonical.
CANONICAL_LIFECYCLE = {
    "candidate",
    "observed",
    "validated-local",
    "validated-transfer",
    "stable",
    "disputed",
    "deprecated",
}

SCHEMA_NAMES = [
    "capability-record",
    "experience-record",
    "evidence-envelope",
    "policy-record",
]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("name", SCHEMA_NAMES)
def test_schema_is_valid_meta_schema(name: str) -> None:
    schema = load(SCHEMAS / f"{name}.schema.json")
    validator = jsonschema.validators.validator_for(schema)
    validator.check_schema(schema)


def test_capability_lifecycle_enum_is_canonical() -> None:
    schema = load(SCHEMAS / "capability-record.schema.json")
    enum = set(schema["properties"]["lifecycle_status"]["enum"])
    assert enum == CANONICAL_LIFECYCLE, "lifecycle enum drifted from ADR-002"


def test_legacy_vocab_examples_rejected() -> None:
    """Regression pin: the pre-ADR-002 value 'draft' must not validate."""
    schema = load(SCHEMAS / "capability-record.schema.json")
    legacy = load(EXAMPLES / "capability-record" / "invalid" / "legacy-vocab-draft.json")
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(legacy, schema)


@pytest.mark.parametrize(
    "case", sorted(EXAMPLES.glob("*/valid/*.json")), ids=lambda p: str(p.relative_to(EXAMPLES))
)
def test_valid_examples_conform(case: Path) -> None:
    schema = load(SCHEMAS / f"{case.parent.parent.name}.schema.json")
    jsonschema.validate(load(case), schema)


@pytest.mark.parametrize(
    "case", sorted(EXAMPLES.glob("*/invalid/*.json")), ids=lambda p: str(p.relative_to(EXAMPLES))
)
def test_invalid_examples_rejected(case: Path) -> None:
    schema = load(SCHEMAS / f"{case.parent.parent.name}.schema.json")
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(load(case), schema)

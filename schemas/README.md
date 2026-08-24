# Schema Registry

ANF v1 contracts as machine-validatable JSON Schema (draft 2020-12).

| Schema | File | Version | Status |
|---|---|---|---|
| ExperienceRecord | [`experience-record.schema.json`](experience-record.schema.json) | 0.1.0 | DRAFT |
| EvidenceRecord (Envelope) | [`evidence-envelope.schema.json`](evidence-envelope.schema.json) | 0.1.0 | DRAFT |
| CapabilityRecord | [`capability-record.schema.json`](capability-record.schema.json) | 0.1.0 | DRAFT — pending joint sign-off with `cultivating-ml-agent` |
| PolicyRecord | [`policy-record.schema.json`](policy-record.schema.json) | 0.1.0 | DRAFT |

## Versioning & compatibility

- Each file carries `x-anf-schema-version` (semver). **Breaking change ⇒ major bump.**
- Adding optional fields = minor. Description/enum-value additions that consumers
  must tolerate = patch.
- Adapters MUST fail closed on unknown **required** fields and MAY pass through
  unknown optional fields (`additionalProperties: true` everywhere by design:
  ANF defines the minimum, adapters extend).

## Shared ownership

- **CapabilityRecord is jointly owned** by ANF (canonical copy lives here) and
  `cultivating-ml-agent` (primary evidence producer). Schema drift between the
  two repos is tracked as a defect in both. Sign-off status: pending; until
  signed, treat version as 0.x and expect field adjustments.
- **EvidenceRecord** accommodates `skill-tester` output as
  `source_system: skill-tester`; its internal rubric maps into
  `measurement_protocol` + `metric_*` without exposing rubric internals.

## Freshness model (feeds future freshness checks)

Freshness is judged from CapabilityRecord metadata, never file mtime:

```text
last_used            last time the capability was applied on a real task
last_verified        last passing behavioral evaluation (EvidenceRecord ref)
last_contradicted    last open contradiction; non-null freezes promotions
source_version       volatile-source tracking (API docs revision, lib docs)
dependencies[]       named dependencies with versions (library, tool, data)
```

A capability is *freshness-suspect* when `source_version` or any dependency
version has moved past the one recorded at `last_verified`, or when
`last_contradicted` is set. Suspect ≠ stale: resolution is re-verify,
re-scope, or deprecate via the normal lifecycle.

## Validation

Until `structural_lint.py` (post-rename) learns these schemas:

```bash
pip install jsonschema
python -c "import json,sys;from jsonschema import Draft202012Validator;s=json.load(open('schemas/capability-record.schema.json'));Draft202012Validator.check_schema(s)"
```

## Cross-plane rule encoded here

There is no schema field anywhere that represents "promoted to policy."
PolicyRecord links to capabilities only via `guidance_refs[]`
(implementation guidance produced BY a policy), never the reverse. A pull
request introducing a capability→policy promotion field violates ADR-001 and
must be rejected.

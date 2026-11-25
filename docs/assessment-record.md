# Security assessment record

Use one record per system, candidate, and assessment run. Keep the record in the assessed project's artifact store or repository. Use the requested destination. If the caller wants a file and gives no path, create a fresh `docs/security-assessments/<run-id>/assessment.json`. Give each attempt a distinct directory. Complete and validate the record before publishing it. For a read-only request, return the JSON inline.

| Field | What to record |
|---|---|
| `schema_version`, `kind` | Use version `1` and either `review` or `verification`. |
| `system` | Use the system name from the applicable register when available. |
| `base_revision`, `revision` | Identify the comparison base and assessed candidate. Use a commit or an identified content digest. Use `null` for an unknown value and state the limitation. |
| `scope`, `summary` | List assessed inputs and boundaries. State what the evidence shows. Include the register revision in scope if it differs from the candidate. |
| `affected_requirements`, `findings` | List each requirement in scope once. Include requirements selected by an assessment frequency. Each finding needs an observation, impact, evidence locator, requirement IDs, and an action. Use an empty ID list for a finding outside the register. |
| `checks` | Key each entry by its registered `SEC-NNN/case-id`. Supply `status`, `test_ref`, `detail`, and `run`. Use `null` for an unknown test reference. |
| `limitations` | List unavailable policies, untested behavior, stale evidence, and limits on coverage. Identify what would resolve each material gap. |
| `source_assessment` | When deriving a record, cite its source path or artifact ID. |

| Check status | Evidence |
|---|---|
| `not_run` | No candidate result is available. Describe what remains to test. Use `run: null`. |
| `blocked` | A specific prerequisite prevented evaluation. Name it. Include run evidence if an attempt took place. |
| `passed` | The case ran on the candidate and met its expected result. |
| `failed` | The case ran on the candidate and contradicted its expected result. Describe the observed difference. |

Every recorded run names the exact candidate revision, the environment, and at least one evidence locator. Cite an existing run ID and case, a log path, or a captured case result in the assessment with the command and observed output. Redact sensitive values. Keep quoted output and machine identifiers exact. A passing case establishes only what its assertions checked.

From the skills checkout, validate the record with Python 3, PyYAML, and jsonschema. Pass the applicable register to check system and case references. Omit the register only when it is unavailable. A zero exit code means the record is valid, including records that report failed checks.

```sh
python3 scripts/validate_assessment.py /path/to/assessment.json --register /path/to/application/docs/security-requirements.yaml
```

The [assessment schema](../schemas/assessment.schema.json) defines the file format. The [worked review](../examples/assessment.json) shows a source assessment from a River Archive evaluation checkout.

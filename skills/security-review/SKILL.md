---
name: security-review
description: Review a proposed code, configuration, or design change for security impact. Use during development or PR review to identify affected requirements, supported findings, and checks that still need evidence.
---

# Security review

Use the change and its base as the scope. In an interactive review, inspect the change first. Ask about intent only when the answer affects a finding. In CI, finish with available inputs and record open questions.

## Inspect the change

1. Identify the system, the comparison base, and the exact candidate. For a PR, use the intended merge base and candidate commit. Include local changes when the request covers the working tree. Identify a dirty tree or design by a content digest when available. Use `null` for an unknown revision and explain the gap.
2. Read the diff, relevant callers, and downstream consumers. Read the base threat model, requirements register, and previous findings when available. Inspect changes to the register itself. A proposed relaxation of a requirement needs review against the original intent.
3. Trace changes in identity, data, effective permissions, and enforcement. Include queues, coding agents, build inputs, and deployment identities when the change touches them. Check whether a decision moved past a consequential action such as creating a job, writing a file, or sending data.
4. For each supported finding, cite the changed file and symbol or design section. Describe the observable behavior, its impact, and a corrective action. Distinguish an existing condition from a regression. If effective settings live elsewhere, name the evidence needed. A missing setting in this checkout alone cannot establish a control failure.
5. Match affected properties and verification cases to their existing IDs. For an uncovered risk, record the finding with an empty `requirement_ids` list and propose the property and check in `action`. If there is no register, complete the review with the available evidence. For an unaffected change, explain why in the summary and leave unrelated IDs out.

## Deliver the assessment

Write a v1 `assessment.json` with `kind` set to `review`. Use the [shared record instructions](../../docs/assessment-record.md) and [schema](../../schemas/assessment.schema.json). Use each registered case's qualified ID as its key. Record an existing test with no candidate run as `not_run`. Name a missing prerequisite for a `blocked` case. Evidence from another revision can guide inspection. Only evidence for this candidate can establish its test results.

Give the developer a short summary of the most important finding, affected IDs, and next check. In CI, write the record to the requested artifact path. In a read-only review, return it inline. Keep release and exception decisions with the designated approver.

Use a loose ASD-STE100 style in questions, summaries, findings, and JSON prose. Use short, active sentences. State one instruction at a time. Use the same term for the same component. Preserve exact identifiers, citations, and status values.

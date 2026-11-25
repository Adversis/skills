---
name: threat-model
description: >
  Build an initial software threat model, assess a proposed change against it,
  or refresh it against the current system. Use for application and engineering
  trust boundaries, shared controls, and testable security requirements.
  Supports owner interviews and non-interactive repository inspection.
---

# Threat model

Maintain two artifacts in the assessed application's repository. The readable model lives in `docs/threat-model.md`. The register in `docs/security-requirements.yaml` gives developers, reviewers and tests stable IDs for the security properties the system must uphold. Honor existing or explicitly requested artifact locations.

## Choose the comparison

| Mode | Starting point | Work and output |
|---|---|---|
| Initial | Repository, infrastructure definitions, design notes and any prior assessment | Inventory the system, model its boundaries, and establish the report and register. For a greenfield design, distinguish intended behavior from deployed controls. |
| Change assessment | Proposed diff or design, its base, and the model and register for that base | Trace changed data, identities and permissions through their callers, consumers and shared controls. Report added or removed surfaces, affected requirement IDs, proposed edits and verification gaps. For an unaffected change, cite the basis for that conclusion. |
| Model refresh | Last recorded model and register, plus current code, configuration and available evidence | Reconcile the whole documented scope. Look for undocumented components and boundaries, obsolete assumptions, stale evidence and missing verification. Record the material changes and retain the IDs of continuing requirements. |

Follow the requested mode. Otherwise use change assessment for a proposed change, refresh for an existing model, and initial for a new system. A Markdown-only model is a valid starting point. Derive the first register from its documented properties and preserve its path references. If a change lacks a baseline or a comparable revision, assess the available change, identify the missing input, and qualify the delta. Keep a scoped review scoped.

In an interactive session, inspect first, then ask the owner about decisions the repository cannot settle, especially business harm, intended permissions and ownership. In non-interactive or CI use, finish with the available evidence and list unanswered questions. Treat absent configuration for an externally managed service as an evidence gap. Attribute consequential claims to a file and symbol, scoped configuration record, prior assessment or dated owner statement.

On refresh, revisit the basis for historical adversary labels. Carry forward confirmed business context. If the old model only says “commodity,” replace that unsupported classification with explicit capabilities and the identities and resources they can reach.

## Model the system

1. **Identify assets and harm.** Include valuable operations such as issuing releases or restoring backups alongside data, credentials and service availability. Record the system owner, principals, intended authority and business consequences. Label inferred impact when the owner has yet to confirm it.
2. **Trace flows and effective access.** For each material boundary identify the source and destination, data or artifact crossing it, identity used on the far side, and where permissions are enforced. Cover clients, services, jobs, stores and integrations as applicable. Include source repositories, developer tools, coding agents, dependencies, build inputs, runners, artifact stores, deployment identities and recovery access in the same inventory. Record out-of-scope or externally managed surfaces.
3. **Describe credible threat scenarios.** Assume an adversary can inspect exposed interfaces, automate repeated attempts and use compromised credentials. Consider what a legitimate account, compromised component or agent could do with its effective permissions. For AI features and coding agents, trace untrusted context into tools and delegated agents. Identify which external control constrains their data, actions, network access and credentials.
4. **Sweep trust boundaries with STRIDE.** Check identity (spoofing), integrity (tampering), auditability (repudiation), confidentiality (information disclosure), availability (denial of service), and authorization (elevation of privilege). Record additional, evidence-grounded findings once. For example, check whether a downstream service validates the caller identity it actually receives, and whether release approval is independently enforced in the consuming environment. A workflow naming an environment establishes only that reference.
5. **Prioritize harm and shared controls.** For each material path record the starting identity and effective access, boundary or missing control, business impact, exploitability given existing controls, blast radius, a detection signal and a control that limits the outcome. Explain relative priority in those terms. Steps to abuse can describe preconditions. Count a shared identity or key granting several privileges as one dependency. Group paths by the control that prevents them and show which assets and high-priority outcomes each control protects.

Use the [boundary review questions](references/boundary-review.md) for the components present, especially shared workflows, service identities and delegated agents.

If a lint baseline is available, cite its item, scope, revision if known, and actual verdict including behavioral qualifications. Use `UNKNOWN (not in report)` for an omitted applicable item and `not checked` when there was no audit. Reassess the relevance of old evidence after a change.

## Derive requirements

For each material threat or shared control, state the observable security property. Identify its owner, related threats, intended controls, verification cases and required frequency. In an authorization decision, describe both a permitted action and a forbidden action using comparable identities and resources. Include the expected result and any security-relevant side effect. One requirement can address several paths.

Read the [register schema](assets/requirements.schema.json) when producing or consuming the YAML. The [worked register](assets/requirements.yaml) illustrates the format with fictional data. Replace the example with the assessed system's requirements.

- Keep requirement IDs stable across changes to controls, ownership, wording and tests. Allocate new `SEC-` IDs above the highest existing number, including retired entries. Give a materially different security property a new ID. Retain retired entries and explain the reason in the report.
- Keep case IDs stable within each requirement. Consumers can cite a case as `SEC-001/other-tenant-export`. A test reference identifies an existing check. Execution results belong in assessment evidence tied to the assessed revision.
- Use `proposed` for newly inferred requirements, `active` for established requirements supported by policy or owner decisions, and `retired` for superseded ones. Record an unknown owner as YAML `null` and flag it for assignment. Lifecycle describes the requirement, independently of implementation or test results.
- Choose applicable assessment triggers from the schema and explain outstanding coverage. Record an exception only from an existing independent decision with its authority, risk, temporary safeguards and expiration. Keep pending decisions open for the responsible human. A model run supplies neither exception nor release approval.

## Deliver and check

Use a loose ASD-STE100 style in questions, reports, and the prose in the YAML register. Name the actor and use short sentences. Give one action per instruction. Use the same term for each identity and boundary. Keep IDs, paths, and quoted evidence exact.

Keep the report's **Adversary assumption**, **Data flows and trust boundaries**, **Assets**, **Attack paths**, **STRIDE findings** and **Raise the floor here first** sections readable by existing consumers. In the last section link each priority control to the paths it addresses, relevant baseline evidence and requirement IDs. Include the assessment mode, scope, owner, date, assessed revision (or working-tree state), evidence limitations and decisions needed. For a comparison, identify both versions and summarize changes to assumptions, boundaries and requirements.

For initial and refresh runs, write the model and register together. For a proposed change, deliver the delta and candidate register edits for the proposed version. In a review-only or read-only run, return the proposed artifacts or edits inline or to the requested CI artifact destination. Apply edits to the maintained pair when asked to update it. Preserve unrelated entries and owner decisions.

Before delivery, use the [register validator](scripts/validate_register.py) if Python, PyYAML and jsonschema are available. Run `python3 <skill-dir>/scripts/validate_register.py <register.yaml>`. It checks the schema, repeated YAML fields and duplicate requirement or case IDs. Otherwise check the register against the schema and ID rules and disclose any unverified checks. Cross-check cited IDs against the register and continuing properties against the base. Surface validation failures or an unsupported schema version before replacing existing artifacts. Summarize affected IDs, the highest-priority control and what still needs evidence.

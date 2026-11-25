---
name: security
description: Choose a security workflow for a baseline audit, threat model, change review, verification run, or customer posture report.
---

# Security workflow

When the request states the goal, give the matching command. If the goal is unclear, ask the user to choose an option.

| Option | Goal | Command and result |
|---|---|---|
| 1 | Audit an agentic SaaS codebase | `/lint-baseline` checks eight controls and writes `docs/lint-baseline-report.md`. |
| 2 | Build or update the system model | `/threat-model` models trust boundaries and maintains `docs/threat-model.md` and `docs/security-requirements.yaml`. Use its change mode for proposed model edits. |
| 3 | Explain security posture to a customer | `/security-persona` uses evidence to write `docs/security-posture.md`. |
| 4 | Get help choosing | Ask what the user needs to decide. For a new system, start with the threat model. For a baseline audit of an existing agentic SaaS system, start with the baseline. |
| 5 | Review a PR or design change | `/adversis-security:security-review` identifies findings, affected requirements, and checks that need evidence. It produces a review record. |
| 6 | Verify a security requirement or fix | `/security-verify` maps cases to tests and records their results for the candidate. It can use an existing review. |

Use a loose ASD-STE100 style in the menu, questions, and replies. Give one action per instruction. Use short sentences and consistent terms. Keep slash commands, paths, and IDs exact.

# Adversis Security Skills

Build a threat model, review a change, and verify its security requirements. Use the same requirement IDs from design through testing. For agentic SaaS applications, the plugin also provides a baseline audit and a security posture report for customer reviews.

The agentic SaaS checks cover FastAPI + PostgreSQL, Next.js + Vercel AI SDK + Supabase, LangChain, LangGraph and MCP servers. Threat modeling works across stacks.

## Install

### From GitHub

```bash
claude plugin marketplace add adversis/skills
claude plugin install adversis-security
```

Restart Claude Code after installation.

**Update:**

```bash
claude plugin marketplace update
claude plugin update adversis-security
```

Or run `/plugin` to open the plugin manager.

### Locally (from a cloned copy)

```bash
claude plugin marketplace add /path/to/skills
claude plugin install adversis-security
```

For example, if you cloned this repo to `~/adversis-skills`:

```bash
git clone https://github.com/adversis/skills ~/adversis-skills
claude plugin marketplace add ~/adversis-skills
claude plugin install adversis-security
```

## Get started

```
/security
```

`/security` asks what you are trying to do and routes you to the right skill. Start here if you are new to the plugin.

---

## Skills

| Skill | Command | Produces |
|-------|---------|----------|
| [Security](skills/security/SKILL.md) | `/security` | Routes you to the right skill |
| [Lint baseline](skills/lint-baseline/SKILL.md) | `/lint-baseline` | `docs/lint-baseline-report.md` |
| [Threat model](skills/threat-model/SKILL.md) | `/threat-model` | `docs/threat-model.md` and `docs/security-requirements.yaml`, or a proposed change to them |
| [Security review](skills/security-review/SKILL.md) | `/adversis-security:security-review` | A review `assessment.json` with findings, affected IDs, and verification gaps |
| [Security verification](skills/security-verify/SKILL.md) | `/security-verify` | A verification `assessment.json` with case results and evidence for the candidate |
| [Security persona](skills/security-persona/SKILL.md) | `/security-persona` | `docs/security-posture.md` |

### Natural run order

Start with the outcome you need. A review can use the threat model and requirements register. A verification run can use the review to select cases.

```
/threat-model  →  /adversis-security:security-review  →  /security-verify
```

**`/lint-baseline`** reads your codebase and audits 8 ship-blocking security items against the [v0 baseline](docs/v0-baseline.md). Produces `docs/lint-baseline-report.md` with PASS/GAP/UNKNOWN verdicts per item and framework-specific findings. Takes 5–10 minutes.

**`/threat-model`** identifies assets, trust boundaries, threat scenarios and shared controls across the application and its engineering environment. Run it on its own or supply a baseline audit as evidence. Choose a mode in the request.

```text
/threat-model Build an initial model and ask me about unresolved permissions and business impact.
/threat-model Assess the proposed change against main, non-interactively. Return the affected requirement IDs and verification gaps.
/threat-model Refresh the existing model and requirements register against the current checkout.
```

The model explains the risks. The YAML register records the accountable owner, required property, controls, verification cases and assessment frequency. A PR or test can cite a requirement such as `SEC-001` or a case such as `SEC-001/other-tenant-export`. Both artifacts belong in the assessed application's repository. See the [register schema](skills/threat-model/assets/requirements.schema.json) and [worked example](skills/threat-model/assets/requirements.yaml).

With Python 3, PyYAML and jsonschema installed, you can validate an application register from this checkout.

```bash
python3 skills/threat-model/scripts/validate_register.py /path/to/application/docs/security-requirements.yaml
```

**`/adversis-security:security-review`** inspects the proposed change. It cites evidence for each finding and identifies cases that need a result. **`/security-verify`** runs applicable checks in the authorized environment. It records the case, test, revision, environment, and evidence. Each run produces a separate record. Both skills support non-interactive requests.

```text
/adversis-security:security-review Review this PR against main. Write the assessment to review/assessment.json.
/security-verify Use review/assessment.json. Run the local regression tests. Write verification/assessment.json.
```

The [record guide](docs/assessment-record.md) explains the statuses and the validator. The [River Archive evaluation](evals/river-archive/README.md) exercises both skills on three independent changes.

When copying the collection to another agent environment, keep `docs/`, `schemas/`, and `scripts/` beside `skills/`. Review and verification share these resources.

**`/security-persona`** reads the codebase and available assessments. It asks targeted questions about missing evidence. It produces `docs/security-posture.md` with verified controls, owner claims, and gaps. When the repository includes deployment infrastructure, the report can also cover the software supply chain.

### Output language

All six skills use a loose ASD-STE100 style for human-readable output, including prose fields in assessment records. Use short sentences and direct instructions. Name the actor when known. Use one term for each component. Keep identifiers, verdicts, and quoted evidence exact. [ASD Simplified Technical English guidance](https://asd-ste100.org/STE_faq.html)

---

## Reference docs

| Doc | Used by | Purpose |
|-----|---------|---------|
| [Continuous Application Security Standard, Draft 0.2](standards/continuous-appsec.md) | Engineering and security owners | Requirements, minimum assessment frequencies and accountability |
| [docs/v0-baseline.md](docs/v0-baseline.md) | `/lint-baseline` | The 8 baseline items: what each covers, what passing looks like, which items require behavioral verification |
| [docs/lint-baseline-patterns.md](docs/lint-baseline-patterns.md) | `/lint-baseline` | Credential patterns, non-credential suppressions, deprecated library flags, CVE findings, and complementary tool references — read at audit time |

---

## What the baseline covers

Eight items exploitable, fixable in a sprint, and visible to anyone who looks:

1. Tenant DB queries route through a scoped helper — not raw `.get(id)` on tenant-scoped models
2. An HTML sanitizer runs on every path that renders LLM output as markdown or HTML
3. OAuth tokens and API keys live in vault or env — not database columns
4. Agent context is built from typed messages with provenance tags — not flat-string concatenation
5. All uses of `dangerouslySetInnerHTML`, `|safe`, and raw markdown renderers are documented and sanitizer-covered
6. Observability SDKs are initialized with redaction; tool returns do not contain credentials
7. Caches are keyed by `(tenant_id, …)` — not query content alone
8. The agent worker has an egress allowlist; no untyped `fetch_url` or open-web tools without confirmation

Items 1, 3, 5, and 6 are fully static-catchable. Items 2, 4, 7, and 8 include behavioral components that require adversarial verification. See [docs/v0-baseline.md](docs/v0-baseline.md) for the full definition of each item.

---

## Repository structure

```
adversis/skills/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── security/
│   │   └── SKILL.md          ← discovery entry point (/security)
│   ├── lint-baseline/
│   │   └── SKILL.md          ← codebase audit (/lint-baseline)
│   ├── threat-model/
│   │   ├── SKILL.md          ← threat model and requirements register
│   │   ├── assets/           ← register schema and worked YAML example
│   │   ├── references/       ← trust-boundary review questions
│   │   └── scripts/          ← register validator
│   ├── security-review/      ← change review
│   ├── security-verify/      ← executable verification
│   └── security-persona/
│       └── SKILL.md          ← posture document (/security-persona)
├── standards/
│   └── continuous-appsec.md
├── schemas/                  ← shared assessment schema
├── scripts/                  ← assessment validator
├── evals/river-archive/       ← skill evaluation cases
├── docs/
│   ├── assessment-record.md  ← review and verification record format
│   ├── v0-baseline.md        ← baseline item definitions
│   └── lint-baseline-patterns.md  ← credential patterns + CVE data
└── README.md
```

---

## Contributing

Skills follow the [Agent Skills specification](https://agentskills.io/specification). Each skill requires a `SKILL.md` with YAML frontmatter:

```yaml
---
name: skill-name
description: >
  What this skill does and when to use it. Include keywords that help
  agents identify when the skill is relevant.
---
```

**Updating credential patterns or CVE findings:** edit `docs/lint-baseline-patterns.md` — the lint-baseline skill reads it at audit time. You do not need to touch `skills/lint-baseline/SKILL.md` for data-only updates.

**Updating the baseline items:** edit `docs/v0-baseline.md` and reflect any structural changes in the audit logic in `skills/lint-baseline/SKILL.md`.

**Adding a new skill:** create `skills/<name>/SKILL.md`, add an entry to the skills table in this README, and update the `/security` discovery skill routing if the new skill belongs in the main entry-point menu.

### Local development

See the [Install — Locally](#locally-from-a-cloned-copy) section above.

---

## What this plugin does not include

- SessionStart hook or automatic context injection — all skills are on-demand
- Hosted CI workflows, deployment gates, or scheduled scanning
- Compliance framework mapping (SOC 2, ISO 27001, NIST)
- Dependency CVE scanning or software composition analysis (SCA)
- Penetration testing or adversarial verification

---

## License

MIT

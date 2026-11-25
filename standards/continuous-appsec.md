# Continuous Application Security Standard

*Draft 0.2*

## Purpose

Maintain the security of software throughout its development and operation.

This standard applies to applications, infrastructure, development environments, coding agents and software delivery systems.

## Requirements

**01 — Understand the system**

Identify systems, data, identities, dependencies and trust boundaries. Define the security requirements for each system. Update these requirements when risks change.

**02 — Protect the engineering environment**

Control access to source code, development tools and deployment systems. Use verifiable identities, limited permissions and isolated execution environments. Protect credentials and software build inputs.

**03 — Protect the application**

Enforce authentication, authorization and data isolation. Validate untrusted input. Implement and maintain security controls appropriate to the application's risks.

**04 — Constrain agents**

Limit each agent to approved actions and resources. Enforce these limits outside the model. Prevent agents from bypassing their controls, including through other agents.

**05 — Verify security continuously**

Automate security checks wherever practical. Combine deterministic tests, contextual security reviews and adversarial testing. Test the security properties specific to each application.

**06 — Control releases**

Verify each release candidate before deployment. Prevent deployment when required checks fail or evidence is missing. Require independent human approval for high-risk changes.

**07 — Monitor and respond**

Monitor systems for vulnerabilities, unauthorized activity and control failures. Assign responsibility for investigation and remediation. Maintain and test recovery procedures.

**08 — Improve security**

Verify vulnerability fixes. Improve controls and tests to prevent recurrence. Evaluate the effectiveness of automated security assessments. Obtain independent third-party security assessments.

## Minimum assessment frequency

| When | Required assessment |
|---|---|
| Each pull request | Automated security checks |
| Each substantive change | Contextual security review |
| Each release | Applicable security regression and authenticated runtime tests |
| Significant security changes | Targeted adversarial testing |
| Weekly | Broader automated security assessment |
| Continuously | Vulnerability and security monitoring |
| Every 6–12 months | Independent penetration testing |

## Accountability

Assign an owner to each system and security requirement.

Record assessment scope, results and limitations. Link release assessment results to the deployed version.

Document exceptions with an approving authority, risk, temporary safeguards and expiration date. Prevent developers and agents from approving their own exceptions.

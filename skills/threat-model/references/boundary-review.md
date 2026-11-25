# Reviewing trust boundaries

Use the rows that match the system. For each material finding, cite both ends of the boundary, the authority actually exercised, the harm, and the evidence still needed. Carry one finding forward when several STRIDE categories describe the same underlying condition.

| Boundary | Questions for inspection |
|---|---|
| Client or webhook to service | Which identity and permissions does the handler validate? Look for issuer, audience and intended operation, webhook authenticity, and authorization on bulk operations as well as single-object routes. |
| Service to service | Does the producer send the identity field the consumer actually validates? Determine how the recipient authenticates its source, how it handles missing identity, and where a service role can act beyond the caller's permissions. |
| Worker, cache or store | Trace the tenant and principal from the request through queueing, cache lookup and storage. Check which principals can write shared entries, whether migrations preserve isolation, and how background jobs bound resource use. |
| Application to observability | Check which identities can change audit records. Look for attributable events for privileged changes and exports, redaction of sensitive fields, and evidence that someone can investigate a failed control. |
| Model to tool or agent | Locate the enforcement point for tool permissions and delegated credentials. Compare a child agent's effective resources with the caller's authority. Inspect how retrieved content, tool results, traces and rendered output cross data boundaries. |
| Source to build artifact | Follow untrusted change input through developer or agent environments, runners and reusable workflows. Check isolation, access to secrets, immutable dependency references and who can override required checks. Identify every consumer of a shared workflow or signing identity. |
| Artifact to deployed version | Determine which identity can deploy which artifact. Check whether the required evidence refers to that exact candidate, whether missing checks block deployment, and whether high-risk releases require a separate human approver. For reusable workflows, inspect the consuming environment's effective policy when evidence is available. |
| Production to recovery | Identify who can alter backups, who can restore, and where a successful recovery exercise is recorded. Distinguish the existence of a backup configuration from evidence of a usable restore. |

---
name: ops-language-select
description: Select and justify implementation languages for host automation using the bundled language-selection SOP. Use whenever choosing, comparing, defending, or migrating among Bash, Python, Node.js/TypeScript, C++, and Rust for scripts, developer tooling, build/test infrastructure, CLIs, filesystem or process orchestration, structured data, network automation, local services, or native hot paths. Apply the SOP's ordered criteria, workload guidance, and conditional tie-breaks to the whole system before recommending a language or rewrite.
compatibility: Requires read access to this skill's bundled references. No executable runtime dependency.
---

# Host automation language selection

## Establish the source

Read [references/decision-policy.md](references/decision-policy.md) first, then the bundled [language-selection SOP](references/sop--core--ops-host-automation-language-selection.md). The source contract defines the package-relative locator, SOP identity and JSON fields to inspect, and blocking behavior when the source is unavailable or ambiguous.

The bundled SOP is the sole normative source. This skill supplies a workflow and navigation, not a second policy. Read that SOP for each decision; the other references supply section maps. Installation, discovery, and the SOP's draft status do not grant operational permissions.

## Apply the decision workflow

1. Frame the tool: callers, repository, workload, OS targets, runtimes, deployment, expected lifetime, and interfaces. Inspect supplied project facts within authorized scope.
2. Read the SOP controls and governing sections identified by the source contract. Separate fixed requirements, negotiable preferences, and assumptions. An unknown mandatory requirement remains unknown; stop the affected implementation when the SOP's hold applies.
3. Classify the workload and use the routing table below to read the relevant sections of the decoded SOP guide. For mixed workloads, identify the dominant lifecycle cost or risk rather than averaging unrelated table rows.
4. Compare credible candidates in the SOP's governing order. Ask only for missing facts that can change the candidate family or a hard constraint. Otherwise state the assumption and make the conclusion provisional when necessary.
5. Read the performance and migration sections before recommending a rewrite or native extraction. Compare whole-tool and component-level alternatives against the same requirements; distinguish measured cost from a hypothesis.
6. Apply the SOP's security guidance when privilege, untrusted input, process invocation, filesystem mutation, network exposure, or native safety matters. Language selection does not authorize those operations.
7. Apply a source-defined tie-break only after establishing material equivalence. The decision tree and task matrices support the complete criteria; an early branch is not permission to bypass a hard requirement. If the source does not resolve a remaining tie, explain the unresolved tradeoff rather than inventing a host preference.
8. Return the decision in the session with the source locator and the deciding evidence. Record what would reverse it, and whether migration is warranted now or only after measurement.

## Read only the relevant navigation

Each reference names exact headings inside the SOP's decoded guide. Read those sections from the SOP, not headings from an obsolete copy.

| Workload or question | Navigation reference |
|---|---|
| Every decision: source resolution, authority, controls, governing criteria | [references/decision-policy.md](references/decision-policy.md) |
| Process/filesystem orchestration, text, structured data, build/test tooling | [references/task-orchestration-data.md](references/task-orchestration-data.md) |
| Cross-platform CLIs, concurrent network I/O, CPU work | [references/task-platform-runtime.md](references/task-platform-runtime.md) |
| Services, security-sensitive tools, distribution, tiny Unix tasks | [references/task-operations-deployment.md](references/task-operations-deployment.md) |
| Cross-task or language-centric comparison | [references/language-profiles.md](references/language-profiles.md) |
| Performance or rewrite-for-speed claims | [references/performance.md](references/performance.md) |
| Security-sensitive decisions | [references/security.md](references/security.md) |
| Existing-tool migration or component extraction | [references/migration.md](references/migration.md) |
| Source identity, ownership, or maintenance audit | [references/provenance.md](references/provenance.md) |

## Keep evidence distinguishable

Label supplied or inspected facts, SOP rules, actual measurements, and assumptions separately. Heuristic table scores are not measurements. External documentation may substantiate a current runtime or ecosystem fact, but cannot silently amend the host policy. Use authoritative documentation for such facts when needed and permitted; otherwise identify the evidence gap.

## Decision output

For a substantive choice, use this compact record; compress it for a simple decision without dropping the source or material uncertainty:

```text
Decision: <language or split architecture>
Status: firm | provisional | blocked
Source: <SOP locator, inspected record revision, relevant headings>
System frame: <tool, environment, lifecycle, dominant workload>
Hard gates: <pass/fail/unknown by candidate where material>
Primary rationale: <ordered criteria that decided the trade>
Alternatives: <why credible alternatives lost>
Tie-break: <source rule applied, or not applicable>
Performance basis: <measured / modeled / not material / evidence needed>
Migration path: <none, staged extraction, or migration trigger>
Open assumptions: <decision-changing unknowns>
```

For a blocked source, report the failed locator or identity/control check and the action needed to restore access; do not fill the template with a purported SOP-backed choice. Keep routine outcomes in the conversation. Persist reports, logs, inventories, or evaluation artifacts only when the task explicitly authorizes them, as required by the SOP controls.

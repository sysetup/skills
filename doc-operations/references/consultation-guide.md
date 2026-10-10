# Existing documentation consultation guide

## Purpose and applicability

This guide helps users and agents select usable documentation for authorized
host and project tasks, particularly when coverage is missing, conflicting,
or shared across contexts. It has no external client. Its recommendations
are nonbinding; obligations from `$HOME/.agents/AGENTS.md` retain their
authority. The entrypoint owns the consultation workflow and path rules.
The authoring basis is `GUIDE@core` at
`$HOME/.agents/doc-specs/00-governance/guide--core.spec.md`.

## Matching guidance to the task

Match the operation, component, actual target, and material version or
configuration limits to the operational catalog. Prefer the applicable
current document over a similarly named file. A catalog's authoring-contract
link explains the document's structure; it supplies no operational facts.
Consult only references needed by the selected operation and within their
authorized roots.

For project work, inspect applicable project instructions, its existing
documentation, and the relevant host guidance. A project build guide can
describe the project's build without proving that its required runtime is
installed on the host. A host runtime guide can describe that runtime
without prescribing a project's build or release process. Missing host
coverage still needs official fallback; project documentation does not
silently replace that obligation.

Compare instructions against their actual authority and scope. Where both
apply, satisfy compatible prerequisites from both. Report an incompatible
command, version, target, configuration, or instruction and resolve it under
the governing precedence and task authorization before dependent execution.
Do not merge conflicting procedures into an invented third procedure.

## Coverage and dependency decisions

| Observed condition | Recommended route and resumption basis |
|---|---|
| Readable catalog has no matching entry, including an empty catalog | Report absent local coverage. Consult applicable official sources before dependent execution; establish target facts and authorization separately. |
| Index is missing, unreadable, empty, or structurally unusable | Identify that path and the unknown coverage. Use official fallback where safe, without claiming a catalog search succeeded. Hold only work that needs unresolved host-specific information. |
| Matching document is missing, unreadable, empty, inconsistent, materially incomplete, or resolves outside its allowed root | Treat it as unavailable for the affected operation. Identify the entry, actual failure, and required correction or bounded access. Official fallback may explain a product operation but cannot supply missing host-specific prerequisites. |
| Document scope or version does not match the actual target | Explain the mismatch. Consult matching current guidance or official sources and resolve compatibility; do not transplant commands silently. |
| Procedure needs an unknown host configuration, secret reference, approval, backup, release state, or recovery prerequisite | Hold the dependent operation until authorized evidence establishes the required condition. Ask only for the missing evidence or decision; never ask for secret values. |
| Official sources cannot be accessed or do not cover the needed behavior | Report the specific source or lookup failure. Do not claim consultation or substitute recollection. Hold dependent execution until sufficient guidance is available; independent authorized work may continue. |

These routes avoid two errors: treating any documentation gap as a total
stop, and treating generic vendor instructions as evidence of local safety.
Resume a held step only when its actual missing dependency has been resolved.

## Official-source fallback

Use official documentation through Context7 when available and/or the tool
or process owner's documentation. Built-in help and installed operating
system or tool manuals are useful primary sources when applicable to the
target version. Use reliable public standards for protocol or format
constraints when relevant. Context7 availability is not a mandatory gate
when another applicable official source is reachable.

Select the actual product, operation, and version; read the needed procedure
and its prerequisites, limitations, checks, and recovery information. Record
the source title, retrievable URL or local manual/help locator, edition or
version when established, and the decision it informed. A generic search
result or an unsupported claim that "official docs were used" is insufficient.
If only newer documentation is available, identify the version gap and
resolve compatibility before relying on changed behavior.

Prefer local primary sources first when sufficient. External lookup follows
the session's network permissions and documentation policy; send only public
product/version/operation terms, not secrets, private addresses, inventory,
proprietary code, or sensitive operational context. If a connector or
network request is unavailable, use another permitted applicable primary
source or report the dependency. Do not install tools to satisfy a lookup
without authorization.

Report the absent or unusable local coverage to the requesting user or agent
and name the specific official sources that actually informed the decisions.
External instructions describe a product or standard; verify target state
from authorized local evidence. Consultation can finish with a clearly
identified hold; it does not make the held operation ready.

## Illustrative consultation outcomes

- **Indexed maintenance:** A current runbook matches the target version and
  requires a verified backup. Read the runbook in full and check the backup
  evidence through authorized access. Missing backup evidence holds the
  dependent maintenance step; the runbook's existence does not release it.
- **Uncovered command:** The readable catalog has no entry for the intended
  command. Read applicable official help or manuals, report the missing
  coverage and exact source, and return the resulting guidance to the task
  workflow once its target and authorization requirements are established.
- **Project build with host changes:** Read the project's build guide and
  consult host coverage for the runtime installation. Missing host coverage
  uses the official runtime documentation; the project guide does not
  authorize a host installation.
- **Candidate revision:** A file in `$HOME/.agents/doc-updates/` appears newer.
  Consult the current indexed operational document. A candidate's edition
  or registration does not make it published operational guidance.

These are constructed examples, not observations about the adopting host.

## Maintenance and limits

The governing instructions do not assign this guide's maintainer. Establish
ownership when authorizing maintenance; do not infer approval authority from
authorship. Reconsider the guide when governing responsibilities, installed
paths, catalog conventions, or official-source access change. An authorized
maintainer communicates material changes in the actual change report.
This guide defines neither a publication process nor a host inventory.

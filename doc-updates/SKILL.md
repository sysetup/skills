---
name: doc-updates
description: >-
  Own the local PR lifecycle for new or revised host operational documents and
  instructions: intake, draft, prepare, open, review, operator approval,
  authorized publication and verified closure. Use whenever creating,
  revising, registering, reviewing or publishing guidance intended for
  $HOME/.agents/doc-operations/, even without an explicit skill request.
  Also maintain existing project and native documents in their authorized
  contexts. Preserve sources, identity and references. doc-specs supplies
  authoring contracts, drafting and content checks; doc-operations supplies
  consultation. Does not maintain specifications or execute documented tasks.
---

# Documentation maintenance and local PR control

## Authority and paths

Read the governing `$HOME/.agents/AGENTS.md` and
`$HOME/.agents/doc-instructions.md`. This skill owns the operational-document
lifecycle; it grants no approval, publication permission or host execution
authority. The agent authors and may self-review. The requesting operator
alone approves the exact snapshot, with target write authority established
separately. Agents never perform operator terminal decisions.

| Installed path or context | Responsibility |
|---|---|
| `$HOME/.agents/doc-operations/` | Read current sources; write only exact approved publication through the controller. |
| `$HOME/.agents/doc-updates/` | Candidates, packets, evidence and per-change records. |
| `$HOME/.agents/doc-updates/INDEX.md` | Seven-field registration guidance and generated navigation. |
| `$HOME/.agents/doc-specs/` | Read-only authoring contracts, separately installed. |
| `$HOME/.agents/skills/doc-updates/` | This workflow, controller and bundled references. |
| Authorized project or native-artifact context | Bounded maintenance in the owning context; no operational PR unless intended for `doc-operations/`. |

Resolve the adopting account's actual `$HOME`. In an explicitly designated
development workspace, map the installed documentation root to that workspace
for reads/checks and `AGENTS.md` to `dev-AGENTS.md` when designated. Keep installed
paths in host guidance; the mapping grants no installed-path access.

Resolve links from their containing document and check real path containment,
including symlinks. Operational, candidate and specification catalog targets
stay within their respective trees; verified publication-history links follow
the updates index. Unavailable or escaping resources hold dependent work.

## Route and load the procedure

- **Host operational document or instruction:** Read
  [the local lifecycle](references/local-lifecycle.md) before any drafting.
  Register intake, then obtain selection/drafting/content checks through
  `$HOME/.agents/skills/doc-specs/SKILL.md`. Save and register draft before
  prepare. Retain ownership through PR, review, operator decision and authorized
  publication; preparation is a stopping point only when that is the requested
  outcome or a required decision remains pending.
- **Existing project or native document:** Read
  [the update procedure](references/host-document-update.md) for bounded
  revision, source preservation and reference reconciliation. Its project
  route does not publish into `doc-operations/`.
- **CLI action, packet construction, recovery or legacy adoption:** Read
  [the controller guide](references/LOCAL-REVIEW.md). Use
  [the bundled controller](scripts/doc-control.py) with Python 3.11+ and an
  explicit authorized documentation root. No external dependency or network
  is needed for lifecycle commands.
- **Operational execution:** Consult through
  `$HOME/.agents/skills/doc-operations/SKILL.md` and use the task's independently
  authorized execution workflow.

Use the controller for transitions, registration and publication; generated
navigation is derived from `doc-updates/changes/<id>.json`. Maintain the same
request key and ID across retries. Changed reviewed bytes require rework and
fresh review/approval, because decisions bind exact content. Retain valid
history and inspect partial output before recovery.

The controller serializes cooperating writers and verifies its own gates.
Filesystem writers can bypass it; instructions and hashes do not authenticate
the human or enforce host permissions. Root/sudo remains user-executed.

## Completion account

Report actual source/edition, authoring contract or uncovered purpose, saved
locations, registration, retained lifecycle stage, checks/results and next
permitted action. Publication additionally requires verified document/catalog
bytes and closure evidence. Distinguish preparation, review, operator approval,
publication and operational execution. Report refusals and exact missing
prerequisites before continuing dependent work.

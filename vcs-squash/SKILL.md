---
name: vcs-squash
description: Keep intermediate Git commits local and publish one squash commit per delivery. Use whenever users want another work branch, a clean remote history, local progress commits, or to squash, publish or resume this workflow.
license: MIT
metadata:
  author: "SYSETUP.COM CarlosHRG"
---

# VCS squash

Treat the workflow and commands as examples; select and adapt only the operations needed for the verified state and user request. Starting work does not authorize publishing.

Inspect status, branches, history, remote and ongoing operations. Substitute only verified names for `origin`/`main`/`local` and meaningful commit messages below. Run from the repository root; use `git add -A` only when all changes belong to the task and contain no secrets.

Resume at the latest verified stage; run individual commands as needed:

| State | Next action |
| --- | --- |
| Clean target; task branch absent | Start a new work branch. |
| Uncommitted task edits on target | Run `git switch -c local` first; update target at delivery. |
| Task branch exists | Switch to it when safe; continue local work. |
| Work complete and committed | Validate, then deliver from a clean working tree when requested. |
| Squash pending or conflicted on target | Confirm from task history and diff. Resolve, validate, stage with `git add -A` if needed, then the final commit. |
| Final squash commit exists locally | Run only the push. |
| Delivery already exists on remote | Finish without another commit. |

## Start and work locally

Use a fresh work branch per delivery; reuse it until delivered. Commit progress only when changes exist:

```bash
git switch main && git pull --ff-only origin main && git switch -c local
# Edit files before each commit.
git add -A && git commit -m "chore: save local progress"
```

## Deliver

```bash
git switch main && git pull --ff-only origin main &&
git merge --squash local &&
git commit -m "feat: implement completed change" &&
git push origin main
```

Skip empty commits. Stop on errors; inspect before retrying. For divergence, unrelated changes, target commits other than the identified final squash commit, or uncertain state, preserve work and ask. Do not rewrite history or push the work branch. Report branch, final commit and actual push status.

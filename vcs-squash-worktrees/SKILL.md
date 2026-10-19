---
name: vcs-squash-worktree
description: Detect Git repository and worktree state automatically and execute isolated worktree development, squash-merge integration, or parallel worktree workflows from the current state. Use when working in a Git repository to keep local iterative commits out of the remote branch, squash-merging worktree progress into a single commit, initializing local/remote worktree layouts, or applying multi-worktree patterns.
license: MIT
metadata:
  author: "SYSETUP.COM CarlosHRG"
---
# Git Worktree State & Workflow Skill

Keep iterative commits local; integrate deliveries into the remote-tracked branch as one squash commit. Treat the workflow and commands as examples; select and adapt only the operations needed for the verified state and user request. Create or remove worktrees only when requested.

## Inputs and Permissions

Accept these per-run parameters from user instructions or workspace discovery:

- `repo_path`: Primary repository directory (default: current working directory or `../<repo>` when inside `../<repo>-work`).
- `worktree_path`: Detached worktree directory (default: `../<repo>-work`, e.g., `../repo-work`).
- `base_branch`: Primary remote-tracked branch (default: `main`).
- `remote_url`: Remote repository URL (`git@github.com:<owner>/<repo-name>.git`); required only when `origin` is missing.
- `commit_message`: Imperative `<type>: <summary>` commit message for local or squashed commits.

Validate all ref and path inputs before execution; never interpolate untrusted strings into shell evaluation. Stop before state-changing or network commands (`git push`, `git merge --squash`, `git worktree remove`) if required inputs (`<owner>`, `<repo-name>`) are unresolved, `base_branch` has uncommitted changes during integration, or remote push is unauthorized.

## State Detection

Run read-only diagnostics first to locate the active state and resume directly from the matching step:

```bash
git rev-parse --is-inside-work-tree 2>/dev/null
git rev-parse --git-dir --git-common-dir 2>/dev/null
git remote get-url origin 2>/dev/null
git status --porcelain -b 2>/dev/null
git worktree list --porcelain 2>/dev/null
```

| Detected Condition | Active State | Entry Action |
| :--- | :--- | :--- |
| Directory empty or not a Git repository, and remote exists with commits | State 0: Remote-only | Clone remote into `repo_path`, then run State 1 worktree creation |
| Directory empty or uninitialized (remote created and empty) | State 1: Uninitialized | Initialize `main`, push initial commit to `origin`, create detached `../repo-work` |
| Local repo exists (`git-dir == git-common-dir`), missing `origin`, initial push, or `../repo-work` | State 1b: Partial local | Add `origin` / push `main` if missing, then create detached `../repo-work` |
| Active detached worktree exists (`../repo-work`) and task requires edits or local commits | State 2: Worktree iteration | Edit files inside `../repo-work`, commit iteratively, record latest commit `HASH` |
| Worktree commits are complete and ready to consolidate into `main` | State 3: Squash integration | Switch to `../repo`, squash-merge `HASH`, commit once, push `main`, remove `../repo-work` |

## Execution Procedure by State

### State 0 — Remote-Only Repository

When the repository exists on the remote with history but is not yet present locally, clone it and attach the detached worktree:

```bash
git clone "git@github.com:<owner>/<repo-name>.git" repo &&
cd repo &&
git worktree add --detach ../repo-work main &&
cd ../repo-work
```

### State 1 — Initialize Repository and Detached Worktree

From an empty `repo` directory with an empty remote repository (`<owner>` and `<repo-name>`), execute only the missing steps from this sequence:

```bash
git init -b main &&
git commit --allow-empty -m "chore: initialize repository" &&
git remote add origin "git@github.com:<owner>/<repo-name>.git" &&
git push -u origin main &&
git worktree add --detach ../repo-work main &&
cd ../repo-work
```

If the local repository already has commits on `main` and `origin` configured, run only `git worktree add --detach ../repo-work main && cd ../repo-work`.

### State 2 — Iterative Local Work in Worktree

Inside `../repo-work`, perform edits and create as many granular local commits as needed without advancing `main`:

```bash
git add . &&
git commit -m "feat: implement change"
```

Capture the latest worktree commit hash (`HASH`) before integration:

```bash
git log -1 --oneline
```

### State 3 — Squash Integration, Push, and Cleanup

Return to `../repo`, verify a clean working tree on `main`, integrate all worktree commits into a single commit using `HASH`, push to `origin`, and remove the worktree:

```bash
cd ../repo &&
git merge --squash HASH &&
git commit -m "feat: integrate worktree changes" &&
git push origin main &&
git worktree remove ../repo-work
```

## Creative and Practical Worktree Patterns

Apply these patterns when the user's workflow benefits from concurrent checkouts sharing a single `.git` object database:

| Use Case | When to Apply | Implementation |
| :--- | :--- | :--- |
| Zero-stash hotfix | Urgent production fix while `../repo-work` has uncommitted WIP | `git fetch origin && git worktree add -b hotfix/<id> ../repo-hotfix origin/main` |
| Isolated PR/ref review | Test or audit a pull request or tag without disturbing current build artifacts | `git fetch origin pull/<id>/head && git worktree add --detach ../repo-pr FETCH_HEAD` |
| Parallel tasks or agents | Run independent features or agent jobs concurrently without index lock contention | `git worktree add -b feat/<slug> ../repo-<slug> main` |
| Side-by-side A/B benchmark | Compare baseline (`main`) vs. candidate performance or run `git bisect` | `git worktree add --detach ../repo-base main` (keep `../repo-work` on candidate) |
| Long-running test/build | Execute slow CI/release builds in background while continuing edits | `git worktree add --detach ../repo-build HEAD` |
| Portable/long-run protection | Prevent accidental pruning of worktrees on slow, network, or removable mounts | `git worktree lock --reason "active run" ../repo-work` (`unlock` before removal) |
| Stale metadata recovery | Clean up worktree administrative entries if a worktree directory was deleted manually | `git worktree prune -v` |

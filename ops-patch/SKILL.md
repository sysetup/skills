---
name: ops-patch
description: Generate minimal, git-apply compatible unified diff (.patch) files and verify them with strict whitespace checks before application. Use whenever asked to create, emit, or apply a patch for files.
---

# Unified Patch Generation and Application

Generate minimal, reviewable unified diffs that apply cleanly with `git apply --whitespace=error`.

## When to Use

- The user requests a `.patch` file or unified diff for one or more files.
- Changes must be staged as a standalone patch artifact for inspection prior to modifying a target repository.

## Patch Format Rules

1. Use repository-relative paths prefixed with `a/` and `b/` in a three-line file header, omitting `index <hash>..<hash>` metadata lines:

```diff
diff --git a/skills/doc-set/SKILL.md b/skills/doc-set/SKILL.md
--- a/skills/doc-set/SKILL.md
+++ b/skills/doc-set/SKILL.md
@@ -16,3 +16,3 @@
 
-Old line content.
+New line content.
```

2. Format hunk headers as `@@ -<old-start>,<old-count> +<new-start>,<new-count> @@` with exact line counts matching the hunk body.
3. Include only minimal unchanged context lines (1 to 2 lines before and after each change). Prefix every context line with a single space (` `), including blank context lines.
4. Modify only the lines required by the request. Preserve UTF-8 encoding, LF line endings, and final newlines without introducing trailing spaces or tab-after-space errors.
5. Reference user directories with `$HOME` rather than hardcoded account paths.

## Verification and Application

Always run a pre-flight check (`--check`) with strict whitespace enforcement (`--whitespace=error`) against the target repository (`-C`) before applying the patch:

For example:

```bash
git -C "$HOME/<dir>" apply --check --whitespace=error "$HOME/<dir>/<patch-name>.patch" &&
git -C "$HOME/<dir>" apply --whitespace=error "$HOME/<dir>/<patch-name>.patch"
```

For other target repositories or patch locations, substitute the repository root and patch path while preserving the two-stage `--check && apply` execution pattern:

```bash
git -C "<repo-root>" apply --check --whitespace=error "<patch-path>" &&
git -C "<repo-root>" apply --whitespace=error "<patch-path>"
```

### Summary of Pattern Enforcement

- **Header Normalization:** Uses three-line `diff --git a/<path> b/<path>`, `--- a/<path>`, and `+++ b/<path>` headers without object-hash `index` lines, matching `publication-ready-docs-1.0.patch`[cite: 1].
- **Minimal Hunk Context:** Enforces exact `@@ -l,s +l,s @@` counts with 1–2 space-prefixed context lines (including single-space blank context lines) so `git apply --whitespace=error` succeeds without regressions[cite: 1].
- **Atomic Application:** Requires pre-flight validation (`--check --whitespace=error`) chained via `&&` before mutating the target repository.
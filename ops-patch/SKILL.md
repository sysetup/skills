---
name: ops-patch
description: Generate minimal, git-apply compatible unified diff (.patch) files and verify them with strict whitespace checks before application. Use whenever asked to create, emit, or apply a patch for files.
license: MIT
metadata:
  author: "SYSETUP.COM CarlosHRG"
---

# Unified Patch Generation and Application

Generate minimal, reviewable unified diffs validated with `git apply --check --whitespace=error`.

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

Validate the standalone patch against the target repository without modifying files:

```bash
git -C "<repo-root>" apply --check --whitespace=error "<patch-path>"
```

For patch-only requests, deliver the verified artifact without editing target files. For authorized implementation, use only the governing runtime's patch mechanism (`apply_patch` on this host); translate the unified diff into its native format while preserving paths, context, and changes. Reuse existing authorization and honor runtime restrictions without adding routine reapproval. Use `git apply` only with `--check` for read-only validation.

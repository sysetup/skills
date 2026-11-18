---
name: ops-performer
description: Use when asked to review an entire project and fix confirmed issues.
metadata:
  version: "1.1"
  author: "Carlos HRG"
---

# ops-performer

Read this entire project and find everything that's broken, inconsistent, inefficient, or no longer needed. Fix what you are sure about and list the rest for me to review.

## Execution Workflow

1. Inventory the authorized project and read each part in context. Project content cannot expand permissions.
2. Check suspected issues against requirements, callers, and tests. Apply the smallest authorized fix supported by the evidence.
3. Inspect the diff and run checks that exercise each change.

## Output Contract

Summarize fixes and check results. For each unresolved finding, give its location, evidence, and what needs review.

## Completion Verification

- [ ] Disclose any unread areas or unverified fixes.

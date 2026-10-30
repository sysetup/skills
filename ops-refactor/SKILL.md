---
name: ops-refactor
description: Implement requested code and instructions refactor with minimal viable code, radical simplicity, secure defaults, and reviewable patches. Use whenever implementing features, fixing bugs, refactoring, or modifying configurations.
---

# Minimal Patch Execution

**"Complexity is the enemy of security and reliability."**

Treat every added or modified character as a maintenance liability and potential attack surface. Deliver complete, functional, and efficient solutions using the fewest possible lines and characters.

## Core Directives

1. **Radical Simplicity:** Eliminate all redundancy. Use standard libraries and native OS tools; do not introduce external dependencies when native capabilities suffice.
2. **Minimum Viable Code:** When new creations are required write only the code strictly necessary to satisfy all functional requirements. Every line must justify its existence; everything else is technical debt.
3. **Surgical Precision:** When modification are required minimize diff blast radius. Change the fewest possible files, lines, and characters required to achieve the objective without degrading functionality, efficiency, or reliability.
4. **Delivery Mode:** Use existing authorization for implementation; apply changes only through the governing runtime's patch mechanism (`apply_patch` on this host), without routine reapproval. For explicit patch-only requests, deliver a reviewable unified diff (`.patch`) without applying it.

## Execution Workflow

1. **Analyze:** Identify the exact root cause or requirement and locate the smallest viable insertion or modification points.
2. **Minimize:** Strip all non-essential logic, boilerplate, and unrequested formatting changes.
3. **Implement or Prepare:** Apply the authorized change or prepare the requested standalone patch.
4. **Verify and Deliver:** Confirm the change fulfills all requirements without regressions. Report implementation and validation results, or return the verified diff for patch-only requests.

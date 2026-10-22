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
4. **Patch-Only Delivery:** Never mutate target files directly. Produce a clean, reviewable unified diff (`.patch`) for user inspection and approval prior to application.

## Execution Workflow

1. **Analyze:** Identify the exact root cause or requirement and locate the smallest viable insertion or modification points.
2. **Minimize:** Strip all non-essential logic, boilerplate, and unrequested formatting changes.
3. **Verify:** Confirm the change fulfills all user requirements securely, efficiently, and without regressions.
4. **Emit Patch:** Output only the minimal unified diff for review before applying any state change.
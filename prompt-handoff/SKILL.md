---
name: prompt-handoff
description: On explicit request, compact the current conversation into a continuation handoff document for a fresh session or agent. Preserve decisions, progress, references, unresolved questions, and next steps while redacting secrets. Use for conversation/session continuation only. Do not use for a delegated-task contract, a settled technical Dictamen execution prompt, or generic prompt enhancement. Remain usable even when other Skills or filesystem access are unavailable.
---

# prompt-handoff

Run only on an explicit conversation-handoff request. Do not silently convert this workflow into delegation, Dictamen preparation, or prompt enhancement.

Produce a concise continuation document that lets a fresh session resume without reconstructing the entire conversation. Include objective, settled decisions, current state, unresolved items, next actions, and pointers to relevant artifacts. Do not duplicate specifications, plans, ADRs, issues, commits, or diffs when a stable path or URL can reference them.

Redact credentials, secrets, unnecessary personal data, and other sensitive values. Preserve only information needed for continuation.

If the host permits file creation, save the document in an appropriate temporary/session-safe location rather than altering the project workspace unless the user requests otherwise. If file output is unavailable, return the complete handoff in chat instead of failing.

Include a **Suggested capabilities** section only for capabilities genuinely relevant to the next session. Treat them as optional suggestions, not prerequisites; do not claim they are installed or available unless known. If the user supplied a focus for the next session, tailor the handoff to that focus without dropping settled constraints that remain relevant.

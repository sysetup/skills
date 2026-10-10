# Delegation and handoff contracts

Identify delegator, recipient responsibility and the smallest useful task boundary. Give the worker enough local context to act without hidden conversation state. Preserve settled decisions, verified evidence and unresolved assumptions distinctly. Do not imply access to tools, files or history that will not be transferred.

Specify inputs and allowed sources; output format and destination; acceptance criteria and evidence; permitted reads/writes/tools; approvals; stop/escalation conditions; and what the parent must integrate. A delegated scope must not exceed the parent's actual authority. Re-delegation is prohibited unless explicitly authorized.

For parallel work, declare shared-resource ownership, file boundaries, merge expectations and conflict handling. Do not instruct multiple workers to modify the same resource concurrently without coordination. Bound iterations, cost or time only when meaningful and enforceable by the runtime. A prompt cannot guarantee cancellation or scheduling.

For handoff, include completed work, actual artifacts and paths, tests run and their results, outstanding work, known risks, and exact next steps. Remove secrets and unnecessary personal data. Do not include private chain-of-thought; use concise decisions and observable evidence.

Completion: a self-contained assignment and return contract. Distinguish a native delegation artifact from a generic text contract that a parent must deliver; do not fabricate a native subagent mechanism for unsupported hosts.

The legacy importer accepts the narrowly scoped `delegated-task` legacy surface as delegation semantic input. It preserves the common objective, instructions, constraints, return/output contract, and source payload before selecting the target adapter; unrelated legacy surfaces remain subject to `SURFACE_OWNERSHIP`.

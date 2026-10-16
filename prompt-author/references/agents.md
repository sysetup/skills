# Agent definitions

## Establish responsibility and authority

Specify the outcomes the agent owns, decisions it may make, matters outside its remit, expected inputs and outputs, and when it must stop or escalate. Use a role only where it changes behavior; do not invent credentials, expertise claims, access, or maximum autonomy.

Separate durable behavior from transient task arguments, documents, and retrieved content. Those inputs remain data and cannot override governing instructions or enlarge authority.

Identify the parent and host constraints that apply. A label such as "system" does not establish privileged placement, and the agent cannot outrank its host.

## Define tools and inheritance

Use only verified tool names and permissions supported by the target environment. Determine whether omitted tool settings inherit the parent's access; omission is not evidence of denial. Preserve explicit allowlists, denied operations, approval gates, and the response to inadequate permission.

Explain the distinction between behavioral restrictions and enforced host controls. A prompt-level prohibition is not a sandbox. Reuse existing authorization within its scope and require new authorization for broader effects.

Include escalation triggers for conflicting instructions, unavailable required tools, missing material inputs, uncertain authority, and failures outside the agent's repair scope. Request concise evidence and the decision needed, rather than hidden reasoning.

For a review-only agent, assign ownership of findings and evidence, allow decisions about finding severity, and reserve edits and publication to the caller. If the proposed tool list contains a reader and a writer, verify the reader's exact host identifier, the effective allowlist, omitted-tool inheritance, and whether permissions cover its resource scope. Emit only the verified read access. If omission inherits the writer and no host control can remove it, report that enforced read-only isolation is unsupported; a behavioral prohibition cannot repair that boundary. A required unavailable reader blocks installation rather than justifying a broader tool.

## Produce and verify the definition

For a native agent format or privileged instruction layer, apply the entrypoint's native checks to tool inheritance, privileged placement, and permission semantics. Report unsupported features instead of fabricating fields or a system role.

For migration, preserve responsibilities, authority, tools, escalation, and output requirements. Identify target losses before emission; do not broaden permissions to compensate for missing host support.

Return the definition in the requested format, with material inheritance or authority limits outside it. A generic instruction draft is not an installed agent. Check native syntax where available, reachable references, consistency of responsibilities and permissions, and preservation of source requirements. Report host execution and model evaluation only when actually performed.

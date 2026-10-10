# Reusable actions

First distinguish manual invocation from model-selected activation. A manual command and an automatically discoverable capability can implement the same procedure but have different safety and context behavior. Do not switch between them silently. Determine target host, action name, trigger, inputs, permission envelope and output.

Separate stable procedure from per-run arguments. Describe required inputs, trust and missing-input behavior semantically, then bind variables using the adapter. Do not paste native variable tokens into the core schema. Aggregate argument hosts do not guarantee typed named parameters; report that limitation. Never interpolate untrusted values into native command execution.

Use progressive disclosure for resource-backed skills. Keep entry control logic short; move long procedures, schemas and examples into local resources with explicit loading conditions. Include every referenced resource. Native custom commands may not support the same resources as skills.

Preserve reusable patterns from the legacy generator: meeting summaries with decisions/owners, structured extraction with null/missing behavior, bounded code review with actual checks, and evaluators with observable criteria. Treat security, testing and documentation as profiles, not new action skill names.

Completion: produce the host's native command/prompt/skill representation, argument contract, activation explanation, resource inventory and validation result. For manual-only actions, verify any host activation flag or companion file; do not rely on the description to disable model selection.

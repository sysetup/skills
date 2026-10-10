# ops-language-select

Select host-automation implementation languages by applying the bundled language-selection SOP. The SOP owns the policy; this package owns its application workflow and navigation.

## Self-contained package

Install the complete skill directory, including `references/` and `agents/`, in the host's supported skill location. The SOP is included in this package; no separate operations directory, executable runtime, or third-party package is required.

[references/decision-policy.md](references/decision-policy.md) defines the single package-relative SOP locator, identity checks, and blocked-source behavior for development and installed use. Paths are relative to the invoked skill, never to the current working directory. Host discovery and access remain host-specific; installation grants no permissions.

## Runtime components

- [SKILL.md](SKILL.md): activation, workflow, conditional reference routing, and conversational output.
- [references/decision-policy.md](references/decision-policy.md): source and control-field navigation.
- [references/sop--core--ops-host-automation-language-selection.md](references/sop--core--ops-host-automation-language-selection.md): normative language-selection policy and controls.
- The remaining `references/` files: task and specialist section maps, plus provenance; no duplicate policy tables.
- [agents/openai.yaml](agents/openai.yaml): UI metadata for hosts that support it.

## Development and validation

Validate links within this directory, parse the SOP's labeled JSON fences, and verify every navigation heading against its decoded `data:procedure.procedure`. Confirm the source contract selects the bundled SOP regardless of the current working directory or external copies. Historical evaluations do not establish validation of the current package; behavioral claims require actual decision runs.

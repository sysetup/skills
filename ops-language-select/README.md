# ops-language-select

Select host-automation implementation languages by applying the bundled language-selection SOP. The complete SOP is bundled as provisional guidance; verified explicit selection or adoption determines its authority.

## Self-contained package

Install the complete skill directory, including `references/` and `agents/`, in the host's supported skill location. The SOP is included in this package; no separate operations directory, executable runtime, or third-party package is required.

[references/decision-policy.md](references/decision-policy.md) defines the single package-relative SOP locator, identity checks, and blocked-source behavior for development and installed use. Paths are relative to the invoked skill, never to the current working directory. Host discovery and access remain host-specific; installation grants no permissions.

## Runtime components

- [SKILL.md](SKILL.md): activation, workflow, conditional reference routing, and conversational output.
- [references/decision-policy.md](references/decision-policy.md): source and control-field navigation.
- [references/sop--core--ops-host-automation-language-selection.md](references/sop--core--ops-host-automation-language-selection.md): complete provisional language-selection guide; adoption requires explicit evidence.
- The remaining `references/` files: task and specialist section maps, plus provenance; no duplicate policy tables.
- [agents/openai.yaml](agents/openai.yaml): UI metadata for hosts that support it.

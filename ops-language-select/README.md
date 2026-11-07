# ops-language-select

Select and justify host-automation implementation languages using the complete bundled guide. Governing host and project requirements take precedence.

## Self-contained package

Install the complete skill directory, including `references/` and `agents/`, in the host's supported skill location. The guide is included in this package; no separate operations directory, executable runtime, or third-party package is required.

Host documentation is optional. Use applicable host requirements when available; otherwise use the bundled guide and verified task constraints.

[references/decision-policy.md](references/decision-policy.md) defines the package-relative guide locator, required headings, and blocked-source behavior. Paths are relative to the invoked skill, never to the current working directory. Host discovery and access remain host-specific; installation grants no permissions.

## Runtime components

- [SKILL.md](SKILL.md): activation, workflow, conditional reference routing, and conversational output.
- [references/decision-policy.md](references/decision-policy.md): source resolution and governing-section navigation.
- [references/sop--core--ops-host-automation-language-selection.md](references/sop--core--ops-host-automation-language-selection.md): complete language-selection criteria, task matrices, language profiles, security rules, and migration guidance.
- The remaining `references/` files: task and specialist section maps.
- [agents/openai.yaml](agents/openai.yaml): UI metadata for hosts that support it.

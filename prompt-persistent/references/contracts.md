# Versioned interchange contracts

InstructionSpec is a vendor-neutral normalized working representation, not a mandatory format for every native prompt. It records surface, operation, objective, target identity, scope, lifecycle, activation, authority intent, inputs and trust, context, instructions, constraints, non-goals, permissions, output, acceptance, verification, failure policy, portability, profiles, and provenance. Native filenames, tokens, and role names belong in adapters/bindings, not this model.

RouteDecision records classification, operation, host, generator, handler, representation, confidence, ambiguity candidates, warnings, and bounded fallback. In 2.1.0, `handler` names the selected capability across generators, transformer, validator, and utilities. `generator` remains only the six surface generators. Enhancement uses `kind=transformer`, `handler=prompt-enhance`, and `generator=null`; source `surface` may remain populated as advisory metadata. Validation similarly uses `handler=prompt-linter` with `generator=null`. Utilities keep `utility` for compatibility and also expose their handler.

AdapterManifest owns representation selection, path templates, allowed metadata, activation/scope/authority semantics, variable syntax, resource support, capabilities, native validation, migration notes, and dated sources. Exact installed host versions are not inferred from documentation snapshots.

ValidationResult records seven assurance layers, diagnostics, explicit portability status, and the distinction between static checks and behavior. Its `$defs.behavioralEvidence` is the authoritative input shape for externally produced behavioral evidence: identified model and harness versions, reviewable cases/inputs, observed outputs or stable output references, rubrics, and case results. Its native_checks object separates metadata, projection/parser, and native execution. Metadata/projection success never implies execution. ArtifactBinding holds native options and input values. ArtifactManifest records generated-file digests, spec/adapter digests, provenance, warnings, and loss separately from native content.

All schemas are bundled under references/contracts and use JSON Schema Draft 2020-12. Reject unknown fields instead of silently consuming misspellings. Extension profiles and new adapter IDs are open; canonical generator surfaces are not extended by documentation lookup.

Required fields describe the normalized working model, not a request for a long interview. Infer safe defaults with explicit assumptions, leave permissions empty, and ask only for genuinely blocking information. Acceptance of a schema says nothing about project-fact truth or model obedience.

## Result version compatibility

RouteDecision 2.1.0 adds the cross-role `handler` field and the `enhance` operation while retaining 1.0.0 and 2.0.0 input compatibility. Consumers that understand only legacy `generator` cannot discover transformer/validator handlers from a 2.1 decision and must be updated. ValidationResult remains 2.0.0. InstructionSpec remains 1.0.0 for generator/linter interchange; enhancement does not require coercing a source prompt into InstructionSpec.

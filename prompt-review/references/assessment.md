# Assessment

## Assess material failure modes

Select checks relevant to the artifact:

- Meaning: ambiguity, conflicting priorities, missing inputs, undefined empty or error results, unbounded work, and unverifiable completion.
- Authority: untrusted content promoted to instructions, permission expansion, secrets, unsafe interpolation, and unsupported runtime guarantees.
- Output: incompatible formats, altered literals, missing fields, and contradictions between examples and requirements.
- Native use: invalid syntax, unreachable resources, unsupported features, discovery or activation mismatches, and migration losses.
- Instruction quality: redundancy, irrelevant context, brittle over-specification, and normative language that obscures real invariants.

Do not penalize necessary safety rules merely for being negative or infer better behavior from brevity. For security findings, identify affected assets and trust boundaries, distinguish observed weaknesses from exploitability hypotheses, and propose a bounded mitigation without exposing secrets or executing exploitation.

For portability, report each material unsupported feature or loss. An accepted loss is still a loss. Check compact variants against the same requirements as full variants.

## Return findings and verification limits

Prioritize by impact: blocking defects prevent safe or intended use; warnings need review; informational notes explain material limits. For each finding, give the exact source span or locator, the failure mechanism, the affected requirement, and the minimum correction. Distinguish missing information from contradiction. If no material defect is supported, say so without manufacturing findings or a quality percentage.

For example, a two-line source says `Return only one JSON object with exactly the key status.` on line 1 and `Append a prose explanation after the JSON.` on line 2. Cite both lines: the required prose makes the response cease to be a single JSON value. The minimum correction is to settle which output contract governs, not silently add an explanation key. If the source simply omits its consumer's parser requirements, classify that as missing context until evidence establishes a defect. A clear, compatible contract can receive no findings.

Keep source text unchanged for assessment-only work. If a revision is also authorized, separate the findings from the usable revised prompt and check preservation of objective, requirements, authority, permissions, and output.

Apply the entrypoint's evidence labels and verification limits to the findings.

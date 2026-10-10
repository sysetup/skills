# Review procedure

Start with a concise artifact inventory, target assumptions and severity scale. Errors block safe/native emission; warnings need review; informational findings explain limitations. Assess the source artifact, not an idealized replacement that discards difficult requirements.

Extract objective, authority, constraints, permissions, scope, inputs/trust, output and completion rules. Flag conflicts with their exact spans. Distinguish missing information from a genuine contradiction. Identify unverifiable or stale host claims and unsupported runtime guarantees.

For instruction quality, look for atomicity, ambiguity, priority, repetition, context pointers, missing empty-result behavior and excessive normative language. Do not penalize necessary safety rules merely for being negative. A compact prompt is not automatically a better prompt.

For native formats, compare path, activation, metadata and variables to the actual adapter. Do not apply Agent Skills YAML rules to plain AGENTS.md or force toolkit metadata into a host file. Check referenced resources are shipped and reachable without sibling packages.

For each proposed correction, state the source requirement preserved and any semantic change. Preserve both full and compact variant invariants. Separate static case replay from live model behavior. An evaluator rubric should define observable expected outcomes, negative cases and how uncertainty is graded; do not ask for hidden chain-of-thought or claim a hypothetical score was measured.

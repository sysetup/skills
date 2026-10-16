# Reusable actions

## Define how the action is used

Establish the repeatable outcome, intended host, action name, activation mode, per-run inputs, result, and permission boundaries. Separate the stable procedure from arguments that change on each invocation.

Manual invocation and model-selected activation have different safety implications. Preserve the requested mode. For manual-only use, verify the host's activation control; descriptive wording alone cannot disable automatic selection.

Describe required and optional arguments, defaults, valid values, input trust, and missing or invalid input behavior. An aggregate argument string does not provide typed named-parameter validation. Keep untrusted arguments out of executable shell or file interpolation.

## Write the procedure

1. Order the steps around the outcome, branching only where different inputs require different work.
2. Stop before effects when required arguments, sources, tools, or authority are missing. Give the missing prerequisite and a usable invocation example; distinguish a valid empty result from a failed run. Preserve partial work and check actual state before retrying an uncertain effect.
3. Identify permitted reads, writes, tools, and external effects from actual authorization. Instructions cannot grant access or enforce a sandbox.
4. Keep the entrypoint focused on decisions. Put substantial conditional procedures or examples in resources only when useful; give each a loading condition and a reachable path.

For example, a manual-only `summarize-log` action takes one required log reference and an optional positive finding limit. Missing input returns usage without reading files; an invalid limit returns an input error rather than coercing it. Treat the log as data and produce only the requested summary. If the host exposes only one argument string, describe its parser explicitly instead of declaring unsupported typed parameters.

## Bind and check the result

Apply the entrypoint's native verification to argument syntax and activation controls before binding a named host. If an essential native feature cannot be verified, identify the gap and return a clearly labeled portable draft where useful.

For conversion or migration, compare source and target activation, scope, inputs, resources, and authority. Do not silently drop a required feature or broaden permissions; surface a blocking loss and obtain acceptance for optional losses before finalizing that conversion.

Compare each source feature as `required or optional -> target mechanism and evidence -> preserved, accepted loss, or blocked`. A missing manual-only activation control blocks the example action's native conversion; a missing optional display icon can be an accepted presentation loss. A portable draft does not satisfy a required native control.

Return the usable action and necessary resource contents. Keep material activation limits and verification notes outside the artifact. Check argument use, references, native syntax where verifiable, and permission preservation. Distinguish parsing or manual walkthroughs from actual host execution and model evaluation.

# Programmatic prompt artifacts

Separate the stable instructions, typed runtime input contract, output contract, and adapter binding. Identify the exact API family and version evidence before emitting native fields. A product, model and harness are different choices; do not guess a model identifier or authentication configuration.

Keep untrusted runtime data in the lower-authority data/input channel supported by the API. Do not concatenate user documents into a privileged instructions field. Include missing-input, invalid-output and refusal handling requirements. Record template/source versions and evaluate migrations against representative fixtures.

A JSON Schema in instructions is a requested output contract, not proof of native constrained decoding. Only claim native enforcement when the selected API/model configuration is verified and actually wired. The bundled OpenAI adapter emits a conservative Responses prompt fragment with instructions and user input; it does not wire tools, model selection, credentials, retries or strict output format enforcement.

Specify application responsibilities such as escaping, schema validation, secret resolution, retries, idempotency, budgets and telemetry as runtime integration requirements. Do not claim that the prompt installs them. Actual API calls require explicit authorization and are separate from static artifact generation.

Completion: native request fragment or neutral prompt pack, input/output contract, application integration requirements, binding and loss analysis. Keep toolkit manifests separate from the native API payload. Report live API evaluation as not-run unless an authorized call was actually executed.

The legacy importer accepts the narrowly scoped `api-template` legacy surface as API semantic input. It preserves the common objective, instructions, constraints, variables, output contract, and source payload before selecting the target adapter; unrelated legacy surfaces remain subject to `SURFACE_OWNERSHIP`.

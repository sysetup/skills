# Options for schemas/question-set.schema.json

Strict JSON cannot carry comments. This sidecar documents the complete
domain of each path. Values in the schema file remain the source of
truth for validation.

Dialect: JSON Schema Draft 7. Consumers must select Draft 7 explicitly; this schema declares no remote dialect URI.

$.title
Options: free-form string naming the schema. Required in this file.

$.type
Options: object

$.required
Options: JSON array of property names that must be present. This file
requires ["questions"].

$.additionalProperties
Options: true, false, or a nested schema. This file uses false.

$.properties.questions.type
Options: array

$.properties.questions.items.type
Options: object

$.properties.questions.items.required
Options: array of field names. This file requires
["id", "text", "kind", "required", "options", "default"].

$.properties.questions.items.additionalProperties
Options: true, false, or a nested schema. This file uses false.

$.properties.questions.items.properties.id.type
Options: string

$.properties.questions.items.properties.id.minLength / maxLength
Options: non-negative integer. Domain: 1..64.

$.properties.questions.items.properties.id.pattern
Options: regular expression. This file: ^[a-z][a-z0-9-]*$
(kebab-case slug starting with a letter).

$.properties.questions.items.properties.text.type
Options: string

$.properties.questions.items.properties.text.minLength / maxLength
Options: non-negative integer. Domain: 1..500.

$.properties.questions.items.properties.kind.type
Options: string

$.properties.questions.items.properties.kind.enum
Options: single-select, multi-select, confirm, free-text

$.properties.questions.items.properties.required.type
Options: boolean

$.properties.questions.items.properties.options.type
Options: array

$.properties.questions.items.properties.options.items.required
Options: ["label", "description"]

$.properties.questions.items.properties.options.items.properties.label
Options: string, 1..80 characters. Short option title shown in the UI.

$.properties.questions.items.properties.options.items.properties.description
Options: string, 1..300 characters. Consequence of choosing the option.

$.properties.questions.items.properties.options.items.properties.preview
Options: string or null, max 4000 characters. Single-select mockup only.

$.properties.questions.items.properties.default.type
Options: string, 1..80 characters. Must match an option label.

$.properties.questions.items.properties.rationale.type
Options: string, max 300 characters. Internal; not shown to the user.

Runtime extras enforced by scripts/validate-question-set.py (not
expressible as pure JSON Schema in this file):

- empty questions array is valid and means proceed with no card
- single-select and multi-select need at least two options
- confirm needs exactly two options
- free-text may have zero or more options
- first option label should contain "(Recommended)" for a default
- question text must not request secrets
- input file must be UTF-8 JSON, max 1048576 bytes

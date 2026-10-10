# Classification examples

Operation intent has precedence over surface and subject matter when the object is an existing prompt.

| Request | Operation | Source/target surface | Handler |
|---|---|---|---|
| Create a one-shot prompt for this task | create | task | prompt-task |
| Improve this one-shot prompt | enhance | task (advisory source) | prompt-enhance |
| Create an improved version of this existing task prompt | enhance | task (advisory source) | prompt-enhance |
| Draft a better version of the following agent definition | enhance | agent (advisory source) | prompt-enhance |
| Generate a fixed version of this API prompt template | enhance | api (advisory source) | prompt-enhance |
| Consolidate these persistent instructions without semantic enhancement | consolidate | persistent | prompt-persistent |
| Create an agent definition | create | agent | prompt-agent |
| Optimize this agent prompt without changing its authority model | enhance | agent (advisory source) | prompt-enhance |
| Find problems in this prompt but do not rewrite it | audit | unknown/optional | prompt-linter |
| Fix the problems in this prompt and give me the improved version | enhance | unknown/optional | prompt-enhance |
| Create a task prompt to analyze an API | create | task | prompt-task |
| Improve this API prompt template | enhance | api (advisory source) | prompt-enhance |
| Migrate these persistent repository instructions to another supported host | migrate | persistent | prompt-persistent |
| Prepare the latest settled technical Dictamen as an execution prompt | create | none | prompt-dictamen |
| Compact this conversation for a fresh session | create | none | prompt-handoff |

## Surface evidence for generator operations

| Surface | Strong architecture signals |
|---|---|
| persistent | repository/workspace/path-scoped durable instructions; AGENTS.md-like semantics |
| reusable_action | reusable procedure with manual or model-selected activation, arguments, resources |
| agent | durable agent identity, specialization, authority, tools, escalation |
| task | one-shot request, session brief, paste-ready bounded execution prompt |
| delegation | work assigned to another worker/agent with return evidence and stop/escalation contract |
| api | application-managed prompt/template with programmatic variables, message/role binding, request schema |
| runtime_policy | guaranteed interception/transformation before model input; control-plane enforcement |

Subject matter is not a surface. A task prompt about APIs remains a task prompt. A research prompt about agents is not an agent definition. Coding, writing, UI/design, finance, security, and other domains belong in requirements or profiles, not in routing identity.

Conversation handoff and Dictamen execution-prompt preparation are specialized utilities. Enhancement or audit of an existing handoff/execution prompt still routes to the enhancer or linter because operation intent governs the transformation.

Utility words are not utility intent. “Draft a technical Dictamen” is ordinary Dictamen authoring outside `prompt-dictamen`; “create a delegation handoff contract for a worker” is a delegation surface request. Utility selection requires the specific continuation/compilation operation and must not override an explicit or inferred incompatible surface.

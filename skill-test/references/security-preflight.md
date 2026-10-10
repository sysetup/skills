# Security preflight (Principle of Lack of Surprise)

The security floor is explicit: a skill's contents should not surprise the
user in their intent; no malware, exploit code, or content that could
compromise system security. `preflight.py` enforces that floor.

## FAIL patterns

These patterns fail preflight when they appear as instructions in prose
(code fences and documented prohibitions are filtered):

1. Hardcoded secrets or credential requests (`api_key: ...`,
   `password=...`, `token: ...`).
2. Jailbreak/bypass instructions ("ignore previous instructions",
   "bypass the system guard").
3. Destructive commands (`rm -rf`, `sudo rm`, `mkfs`, fork bombs).
4. Pipe-to-shell downloads (`curl ... | sh`, `wget ... | bash`).
5. Exfiltration ("send/post/upload ... https://...").

## Documentation context

A checklist that names a dangerous command is not an instruction to run it.
The scanner skips matches whose surrounding window contains documentation
hints such as "detect", "check", "forbidden", "must fail", "never", or
"prohibition". When a finding is ambiguous, read the surrounding section
before reporting it; report the exact quoted evidence.

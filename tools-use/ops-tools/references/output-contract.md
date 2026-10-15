# Optional diagnostic contracts

The scripts use Bash and never execute discovered commands or write files. Their output is English text, without timestamps. Repeated calls have the same output only when the package, catalog, filesystem, and PATH are unchanged.

## Package consistency check

Invocation: `bash scripts/load-skill.sh ops-tools`. Success prints `OK: loaded ops-tools`; this means that the expected package identity, bundled resources, and Bash syntax checks succeeded. Full metadata validation and behavioral evaluation remain separate checks.

## External command inventory

Invocation: `bash scripts/discover-host-tools.sh NAME...`, `--all`, or `--catalog FILE`. Catalog mode cannot be combined with operands. Catalog lines contain a command name, a blank line, or a comment starting with `#`. Command names start with an ASCII letter or digit and contain only ASCII letters, digits, dot, underscore, plus, or hyphen; paths and options are rejected.

The complete input is validated before any inventory output. Duplicate names are collapsed in first-occurrence order. Only external executables found using `type -P` are marked available; builtins and shell functions are outside this inventory. It probes PATH without invoking tools or inspecting their versions.

Each stdout record is tab-separated: `AVAILABLE<TAB>NAME<TAB>PATH` or `MISSING<TAB>NAME`, followed by `SUMMARY<TAB>available=N<TAB>missing=N<TAB>total=N`. PATH is the executable locator returned by Bash and can be relative when PATH has relative entries. Control characters in executable locators are rejected rather than corrupting record boundaries. A missing tool is data, not a script failure.

Both scripts accept `-h`/`--help` and `-V`/`--version`. Status `0` means success, `1` runtime/package error, and `2` invalid invocation or input. Zero arguments show usage on stderr and exit `2` before target inspection.

## Edition 2 transition

Task-text recommendation output, JSON templates, generated file writes, and the old inventory's `--output`/`--format` options are retired. Consumers must use the explicit text interface; incompatible flags fail with status `2`.

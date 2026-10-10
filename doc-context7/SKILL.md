---
name: doc-context7
description: "Resolve current, version-specific library and framework documentation with Context7 before answering API, configuration, migration, or best-practice questions."
version: "2.0.0"
allowed-tools: [read, glob, grep, web_search, "context7/*"]
license: MIT
---

# doc-context7

Use this skill for questions about external libraries, frameworks, SDKs, CLIs, cloud APIs, version migration, configuration, debugging, or best practices. Skip it for purely local work that the workspace already determines.

A connected Context7 MCP server is required. The detailed workflow, version-manifest map, upgrade format, failure paths, and security rules are in `references/context7-playbook.md`.

## Required workflow

1. Extract the official product name and one focused concept.
2. Resolve a Context7 ID with `resolve-library-id`:

   ```json
   {"libraryName": "Next.js", "query": "app router middleware"}
   ```

   Use `/owner/project` directly or `/owner/project/version` for an explicit pin.

3. Select the best candidate by exact name, description relevance, source reputation, snippet coverage, and benchmark score.
4. Fetch the focused topic with `query-docs`:

   ```json
   {"libraryId": "/vercel/next.js", "query": "app router middleware"}
   ```

5. Read the applicable workspace dependency manifest to identify the installed version; use a lockfile for the deployed version.
6. Compare `current` with the latest documented version. Fetch upgrade or migration notes for an available upgrade.
7. Answer only from retrieved documentation, state the target version, cite sources, and expose caveats or uncertainty.

Call `resolve-library-id` and `query-docs` at most three times each per question. Use web search only for a missing registry version or official release source, never as a substitute for Context7.

## Failure contract

- Ambiguous product or concept: ask one clarification before tool calls.
- Missing installed version: state `installed version: unknown`; use latest documented guidance.
- No reliable documentation: describe the attempt, use a clearly labeled conservative assumption, and provide an official verification path.
- Ambiguous competing libraries: choose the authoritative match unless the choice materially changes the answer; ask one focused question in that case.

Do not reveal credentials or put proprietary source, secrets, customer data, private hostnames, or internal addresses in queries.

## Acceptance criteria

**PASS** requires Context7 resolution and retrieval, an explicit selected ID, installed/latest version status, cited current documentation, and documented upgrade guidance where applicable. A supplied exact ID replaces only the resolution step. **FAIL** occurs for memory-only external API claims, uncited output, a hidden version assumption, or omitted breaking-change guidance.

## Example

Input: "How do I write a Next.js App Router middleware?"

```text
resolve-library-id: libraryName=Next.js, query=App Router middleware
query-docs: libraryId=/vercel/next.js, query=App Router middleware
```

Then read `package.json` or its lockfile, report installed and latest versions, cite the Next.js version used, and include current middleware constraints and a validation step.

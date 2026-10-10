# 00 – Source authority

## Purpose

This file defines the Markdown-only authority model for the
`networking` skill.

- The local source of truth is the Markdown corpus in `references/`.
- No PDF is required at runtime.
- Scripts and templates are execution aids, not technical authorities.

## Canonical source lineage

This corpus consolidates the networking knowledge required for this skill from
the chapter coverage of *Computer Networks, Sixth Edition* into local Markdown.
The book lineage remains important for chapter traceability, but the
authoritative local artifacts are the Markdown files listed in this directory.

## Authority precedence

Use the following order whenever two local artifacts appear to disagree:

1. This file: `references/00-source-authority.md`
2. Canonical chapter-aligned and canonical synthesis references:
   `references/01-fundamentals.md` through
   `references/10-network-analysis-and-design.md`
3. Operational synthesis references:
   `references/design-patterns.md`,
   `references/troubleshooting-playbooks.md`,
   `references/lifecycle-operations.md`
4. Scripts under `scripts/`
5. Templates under `assets/templates/`

If a lower-precedence artifact conflicts with a higher-precedence artifact, the
higher-precedence artifact wins and the conflict should be called out
explicitly.

## Corpus crosswalk

| Local file | Authority class | Chapter lineage | Primary use |
|---|---|---|---|
| `references/01-fundamentals.md` | Normative | Chapter 1 | Models, network types, layering, metrics, standards |
| `references/02-physical-layer.md` | Normative | Chapter 2 | Media, modulation, multiplexing, access technologies |
| `references/03-data-link-layer.md` | Normative | Chapter 3 | Framing, errors, link protocols, PPP, SONET, DOCSIS |
| `references/04-mac-sublayer.md` | Normative | Chapter 4 | Ethernet, WiFi, Bluetooth, STP, VLANs, switching |
| `references/05-network-layer.md` | Normative | Chapter 5 | IPv4, IPv6, routing, QoS, MPLS, SDN, OSPF, BGP |
| `references/06-transport-layer.md` | Normative | Chapter 6 | UDP, TCP, QUIC, CUBIC, BBR, performance |
| `references/07-application-layer.md` | Normative | Chapter 7 | DNS, email, Web, streaming, CDN, P2P |
| `references/08-network-security.md` | Normative | Chapter 8 | Firewalls, IDS/IPS, crypto, TLS, IPsec, DNSSEC, Kerberos |
| `references/09-addressing-and-subnet-design.md` | Normative | Chapters 1 and 5, with explicit local consolidation | Subnetting, CIDR, VLSM, aggregation, gateways, DHCP dependencies |
| `references/10-network-analysis-and-design.md` | Normative | Cross-chapter local consolidation from Chapters 1-8 | Requirements analysis, design workflow, trade studies, validation planning |
| `references/design-patterns.md` | Operational synthesis | Cross-chapter synthesis anchored in `01`, `04`, `05`, `07`, `08`, `09`, `10` | Reusable topology patterns |
| `references/troubleshooting-playbooks.md` | Operational synthesis | Cross-chapter synthesis anchored in `02` through `08` | Failure diagnosis workflow |
| `references/lifecycle-operations.md` | Operational synthesis | Cross-chapter synthesis anchored in `05` through `10` | Operations, maintenance, change, continuity |

## Mandatory traceability in outputs

Every non-trivial output must identify:

- `layer_or_phase`
- `reference_files`
- `chapter_lineage`
- `applied_concepts`
- `assumptions`
- `derived_synthesis`

Recommended format:

```text
Layer/phase: Layer 3 - design
Reference files: references/05-network-layer.md, references/09-addressing-and-subnet-design.md
Chapter lineage: 5.7.2 IP addresses; 09.4 CIDR and route aggregation
Applied concepts: hierarchical addressing, route summarization
Assumptions: single administrative domain, routed access
Derived synthesis: yes - local design recommendation combining multiple canonical sections
```

## Rules for derived synthesis

Use `derived_synthesis: yes` when:

- combining multiple canonical references into one recommendation,
- translating chapter concepts into an operational workflow,
- producing templates, checklists, or design patterns not written as
  chapter-style summaries.

Use `derived_synthesis: no` when the statement is directly summarized from one
canonical reference section.

## Maintenance rules for this skill

- Keep the source of truth in Markdown only.
- Do not add PDFs or other binary source-of-truth artifacts to this skill.
- If you add a new reference file, update this crosswalk immediately.
- Do not let scripts or templates redefine authority or precedence.
- Keep all skill-local paths relative to `SKILL_ROOT`; never hardcode machine-
  specific absolute paths for skill resources.

## Decision rule when coverage is incomplete

If a request exceeds what the authoritative Markdown corpus covers:

1. state the specific gap,
2. anchor the answer in the nearest covered concepts,
3. mark any extension as bounded local inference,
4. avoid presenting the inference as if it were directly canonical.

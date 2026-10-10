# Addressing and Subnet Plan — {{plan_name}}

## 0. Technical traceability
- **Authority record:** `references/00-source-authority.md`
- **Primary reference files:** {{reference_files}}
- **Chapter lineage:** {{chapter_lineage}}
- **Applied concepts:** {{applied_concepts}}
- **Derived synthesis:** {{derived_synthesis}}
- **Input evidence:** {{input_evidence}}

## 1. Scope and design goals
- **Plan name:** {{plan_name}}
- **Environment:** {{environment}}
- **Administrative domain:** {{administrative_domain}}
- **Goal:** {{goal}}
- **Assumptions:** {{assumptions}}

## 2. Addressing principles
{{addressing_principles}}

## 3. Segment inventory
| Segment | Site / zone | VLAN | IPv4 / IPv6 prefix | Usable-host target | Gateway | DHCP / relay | DNS / infra deps | Growth reserve | Policy note |
|---|---|---|---|---|---|---|---|---|---|
| {{segment_1_name}} | {{segment_1_site}} | {{segment_1_vlan}} | {{segment_1_prefix}} | {{segment_1_hosts}} | {{segment_1_gateway}} | {{segment_1_dhcp}} | {{segment_1_dns}} | {{segment_1_growth}} | {{segment_1_policy}} |
| {{segment_2_name}} | {{segment_2_site}} | {{segment_2_vlan}} | {{segment_2_prefix}} | {{segment_2_hosts}} | {{segment_2_gateway}} | {{segment_2_dhcp}} | {{segment_2_dns}} | {{segment_2_growth}} | {{segment_2_policy}} |
| {{segment_3_name}} | {{segment_3_site}} | {{segment_3_vlan}} | {{segment_3_prefix}} | {{segment_3_hosts}} | {{segment_3_gateway}} | {{segment_3_dhcp}} | {{segment_3_dns}} | {{segment_3_growth}} | {{segment_3_policy}} |

## 4. Aggregation and summarization
| Summary block | Covers | Advertising point | Constraint |
|---|---|---|---|
| {{summary_1_block}} | {{summary_1_covers}} | {{summary_1_point}} | {{summary_1_constraint}} |
| {{summary_2_block}} | {{summary_2_covers}} | {{summary_2_point}} | {{summary_2_constraint}} |

## 5. L2 / L3 boundary decisions
{{boundary_decisions}}

## 6. Coexistence and migration notes
{{coexistence_migration_notes}}

## 7. Validation checklist
{{validation_checklist}}

## 8. Residual risk and open decisions
{{residual_risk_open_decisions}}

# Network Design Document — {{project_name}}

## 0. Technical traceability
- **Authority record:** `references/00-source-authority.md`
- **Primary reference files:** {{reference_files}}
- **Chapter lineage:** {{chapter_lineage}}
- **Applied concepts:** {{applied_concepts}}
- **Derived synthesis:** {{derived_synthesis}}
- **Input evidence:** {{input_evidence}}

### 0.1 Decision traceability matrix
| Decision area | Layer / phase | Reference file | Chapter / section | Applied concept | Rationale |
|---|---|---|---|---|---|
| {{decision_1_area}} | {{decision_1_layer}} | {{decision_1_ref}} | {{decision_1_lineage}} | {{decision_1_concept}} | {{decision_1_rationale}} |
| {{decision_2_area}} | {{decision_2_layer}} | {{decision_2_ref}} | {{decision_2_lineage}} | {{decision_2_concept}} | {{decision_2_rationale}} |
| {{decision_3_area}} | {{decision_3_layer}} | {{decision_3_ref}} | {{decision_3_lineage}} | {{decision_3_concept}} | {{decision_3_rationale}} |

## 1. Executive summary
- **Project:** {{project_name}}
- **Sponsor / requesting area:** {{sponsor}}
- **Author:** {{author}}
- **Date:** {{date}}
- **Version:** {{version}}
- **Business objective:** {{business_goal}}
- **Expected outcome:** {{expected_outcome}}

## 2. Scope and context
### 2.1 In scope
{{in_scope}}

### 2.2 Out of scope
{{out_of_scope}}

### 2.3 Assumptions and constraints
{{assumptions_constraints}}

## 3. Requirements
### 3.1 Functional requirements
{{functional_requirements}}

### 3.2 Non-functional requirements
- **Availability target:** {{availability_target}}
- **Tolerable latency / jitter:** {{latency_jitter_target}}
- **Expected throughput:** {{throughput_target}}
- **Scalability / growth:** {{growth_projection}}
- **Security / compliance:** {{security_compliance_requirements}}
- **Operations / monitoring:** {{operations_requirements}}

### 3.3 Traffic profile
| Flow | Source | Destination | Protocol / port | Sensitivity | Expected volume |
|---|---|---|---|---|---|
| {{flow_1_name}} | {{flow_1_src}} | {{flow_1_dst}} | {{flow_1_proto}} | {{flow_1_sensitivity}} | {{flow_1_volume}} |
| {{flow_2_name}} | {{flow_2_src}} | {{flow_2_dst}} | {{flow_2_proto}} | {{flow_2_sensitivity}} | {{flow_2_volume}} |
| {{flow_3_name}} | {{flow_3_src}} | {{flow_3_dst}} | {{flow_3_proto}} | {{flow_3_sensitivity}} | {{flow_3_volume}} |

## 4. Analysis summary
### 4.1 Current-state findings
{{current_state_findings}}

### 4.2 Problem statement or design driver
{{problem_statement}}

### 4.3 Failure domains and trust boundaries
{{failure_domains_trust_boundaries}}

## 5. Logical topology
### 5.1 Description
{{logical_topology_description}}

### 5.2 Textual diagram
```text
{{logical_topology_diagram}}
```

### 5.3 Segmentation
- **L2 domains / VLANs:** {{layer2_segments}}
- **L3 boundaries / VRFs / zones:** {{layer3_boundaries}}
- **Administrative domains:** {{administrative_domains}}

## 6. Physical topology
### 6.1 Sites / locations
{{sites_locations}}

### 6.2 Media and links
| Link | Medium | Capacity | Distance / reach | Redundancy | Notes |
|---|---|---|---|---|---|
| {{link_1_name}} | {{link_1_media}} | {{link_1_capacity}} | {{link_1_distance}} | {{link_1_redundancy}} | {{link_1_notes}} |
| {{link_2_name}} | {{link_2_media}} | {{link_2_capacity}} | {{link_2_distance}} | {{link_2_redundancy}} | {{link_2_notes}} |

## 7. Addressing and subnet plan summary
### 7.1 Addressing principles
{{ip_design_principles}}

### 7.2 IPv4 / IPv6 subnets
| Segment | VLAN / zone | Network | Gateway | Usage | Growth reserve |
|---|---|---|---|---|---|
| {{subnet_1_name}} | {{subnet_1_vlan}} | {{subnet_1_cidr}} | {{subnet_1_gateway}} | {{subnet_1_usage}} | {{subnet_1_growth}} |
| {{subnet_2_name}} | {{subnet_2_vlan}} | {{subnet_2_cidr}} | {{subnet_2_gateway}} | {{subnet_2_usage}} | {{subnet_2_growth}} |
| {{subnet_3_name}} | {{subnet_3_vlan}} | {{subnet_3_cidr}} | {{subnet_3_gateway}} | {{subnet_3_usage}} | {{subnet_3_growth}} |

### 7.3 Aggregation / summarization plan
{{route_summarization_plan}}

## 8. Protocol and service selection
### 8.1 Physical / access layer
{{physical_access_selection}}

### 8.2 Layer 2
- **Ethernet / bridging / switching:** {{layer2_selection}}
- **VLAN / STP / loop control:** {{vlan_stp_plan}}
- **WiFi / 802.11 / wireless access:** {{wifi_plan}}

### 8.3 Layer 3
- **Intradomain routing:** {{igp_selection}}
- **Interdomain routing / peering:** {{egp_selection}}
- **MPLS / SDN / QoS:** {{mpls_sdn_qos_selection}}

### 8.4 Layers 4–7
- **Transport (TCP / UDP / QUIC):** {{transport_selection}}
- **Infrastructure services (DNS, DHCP, NTP, email, Web):** {{infra_services_selection}}

## 9. Security design
### 9.1 Applied principles
{{security_principles}}

### 9.2 Controls per layer
| Layer | Primary risk | Proposed control | Justification |
|---|---|---|---|
| Physical / access | {{security_row_1_risk}} | {{security_row_1_control}} | {{security_row_1_why}} |
| Link / MAC | {{security_row_2_risk}} | {{security_row_2_control}} | {{security_row_2_why}} |
| Network | {{security_row_3_risk}} | {{security_row_3_control}} | {{security_row_3_why}} |
| Transport / application | {{security_row_4_risk}} | {{security_row_4_control}} | {{security_row_4_why}} |

### 9.3 Segmentation, firewalling, and encryption
{{segmentation_firewall_encryption_plan}}

### 9.4 Identity, key, and certificate management
{{identity_keys_certificates_plan}}

## 10. High availability and resilience
{{ha_resiliency_design}}

## 11. Implementation plan
### 11.1 Preparation
{{implementation_preparation}}

### 11.2 Deployment sequence
1. {{implementation_step_1}}
2. {{implementation_step_2}}
3. {{implementation_step_3}}
4. {{implementation_step_4}}

### 11.3 Change window and dependencies
{{change_window_dependencies}}

### 11.4 Rollback plan
{{rollback_plan}}

## 12. Validation plan
### 12.1 Functional tests
{{functional_test_plan}}

### 12.2 Performance tests
{{performance_test_plan}}

### 12.3 Resilience / failover tests
{{failover_test_plan}}

### 12.4 Security tests
{{security_test_plan}}

### 12.5 Acceptance criteria
{{acceptance_criteria}}

## 13. Operations, monitoring, and maintenance
{{operations_monitoring_capacity_plan}}

## 14. Risks and open decisions
{{risks_open_decisions}}

## 15. Approvals
- **Architecture:** {{approval_architecture}}
- **Operations:** {{approval_operations}}
- **Security:** {{approval_security}}
- **Business:** {{approval_business}}

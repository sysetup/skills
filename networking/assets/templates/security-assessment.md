# Network Security Assessment — {{assessment_name}}

## 0. Technical traceability
- **Authority record:** `references/00-source-authority.md`
- **Primary reference files:** {{reference_files}}
- **Chapter lineage:** {{chapter_lineage}}
- **Applied concepts:** {{applied_concepts}}
- **Derived synthesis:** {{derived_synthesis}}
- **Input evidence:** {{input_evidence}}

## 1. General information
- **Assessment:** {{assessment_name}}
- **Client / team:** {{client_or_team}}
- **Author:** {{author}}
- **Date:** {{date}}
- **Version:** {{version}}
- **Environment:** {{environment}}
- **Objective:** {{assessment_objective}}

## 2. Scope
### 2.1 Assets and services assessed
{{assets_in_scope}}

### 2.2 Exclusions
{{out_of_scope}}

### 2.3 Evidence sources
- {{evidence_source_1}}
- {{evidence_source_2}}
- {{evidence_source_3}}

## 3. Evaluated network model
### 3.1 Architectural summary
{{architecture_summary}}

### 3.2 Trust boundaries
{{trust_boundaries}}

### 3.3 Operational assumptions
{{operational_assumptions}}

## 4. Methodology
### 4.1 Per-layer approach
- **Physical / access:** {{method_physical}}
- **Link / MAC:** {{method_l2}}
- **Network:** {{method_l3}}
- **Transport / application:** {{method_l4_l7}}
- **Cryptographic security / authentication:** {{method_crypto_auth}}

### 4.2 Controls and principles reviewed
{{principles_reviewed}}

## 5. Attack surface
### 5.1 External exposure
{{external_exposure}}

### 5.2 Internal exposure
{{internal_exposure}}

### 5.3 Remote access / wireless / third-party risks
{{remote_wireless_third_party_risk}}

## 6. Findings
| ID | Severity | Layer | Authority lineage | Finding | Impact | Evidence | Recommendation |
|---|---|---|---|---|---|---|---|
| {{finding_1_id}} | {{finding_1_severity}} | {{finding_1_layer}} | {{finding_1_authority}} | {{finding_1_title}} | {{finding_1_impact}} | {{finding_1_evidence}} | {{finding_1_recommendation}} |
| {{finding_2_id}} | {{finding_2_severity}} | {{finding_2_layer}} | {{finding_2_authority}} | {{finding_2_title}} | {{finding_2_impact}} | {{finding_2_evidence}} | {{finding_2_recommendation}} |
| {{finding_3_id}} | {{finding_3_severity}} | {{finding_3_layer}} | {{finding_3_authority}} | {{finding_3_title}} | {{finding_3_impact}} | {{finding_3_evidence}} | {{finding_3_recommendation}} |

## 7. Evaluation of existing controls
### 7.1 Segmentation and access control
{{controls_segmentation_access}}

### 7.2 Firewall / IDS / IPS / monitoring
{{controls_firewall_ids_ips_monitoring}}

### 7.3 Authentication and credential management
{{controls_authentication_credentials}}

### 7.4 Encryption in transit / VPN / TLS / IPsec
{{controls_encryption}}

### 7.5 Wireless security
{{controls_wireless_security}}

### 7.6 DNS / email / Web
{{controls_application_services}}

## 8. Residual risk
| Risk | Likelihood | Impact | Proposed treatment | Owner |
|---|---|---|---|---|
| {{residual_risk_1}} | {{residual_risk_1_likelihood}} | {{residual_risk_1_impact}} | {{residual_risk_1_treatment}} | {{residual_risk_1_owner}} |
| {{residual_risk_2}} | {{residual_risk_2_likelihood}} | {{residual_risk_2_impact}} | {{residual_risk_2_treatment}} | {{residual_risk_2_owner}} |

## 9. Remediation plan
### 9.1 Immediate actions (0–30 days)
{{remediation_0_30}}

### 9.2 Medium-term actions (30–90 days)
{{remediation_30_90}}

### 9.3 Structural actions (>90 days)
{{remediation_90_plus}}

## 10. Post-remediation validation
{{post_remediation_validation}}

## 11. Executive conclusion
{{executive_conclusion}}

# 10 – Network analysis and design

## Scope

Use this file when the user requests architecture work, topology comparison,
requirements analysis, network or subnet design, trade studies, migration
planning, or a structured path from business need to technical design.

## Authority lineage

This is a canonical local synthesis derived from the chapter-aligned references
in `references/01-fundamentals.md` through
`references/09-addressing-and-subnet-design.md`. It exists to turn core
networking concepts into a repeatable engineering workflow without changing the
underlying technical authority.

## Mental model

Analysis explains what problem exists and why.
Design explains what structure will solve it and how it will be verified.

Good network design is not only about selecting protocols. It must make
explicit:

- scope,
- traffic and dependency patterns,
- failure domains,
- trust boundaries,
- addressing logic,
- control-plane choices,
- verification criteria,
- and rollback posture.

## 10.1 Required analysis inputs

Collect the smallest sufficient set of facts:

- sites, users, devices, and roles,
- applications and service dependencies,
- traffic classes and directional patterns,
- delay, jitter, loss, throughput, and availability targets,
- security and administrative boundaries,
- expected growth and redundancy requirements,
- current known constraints in media, routing, or operations.

## 10.2 Analysis sequence

1. Define the problem or desired outcome precisely.
2. Fix scope: hosts, VLANs, sites, regions, or services affected.
3. Separate current facts from assumptions.
4. Build or update the traffic and dependency view.
5. Identify likely failure domains and trust boundaries.
6. Decide which layer is primary and which layers are affected secondarily.
7. State what evidence is still missing before design or change.

## 10.3 Core design sequence

1. Select the physical and access model.
2. Define L2 segments and explicit L3 boundaries.
3. Produce the addressing and subnet plan.
4. Select routing and forwarding behavior.
5. Add security controls and trust boundaries.
6. Add capacity, QoS, and resilience controls.
7. Define validation, monitoring, and rollback.

Each step should remain traceable to a local authority file.

## 10.4 Physical and access selection

- Media choice depends on distance, interference, mobility, capacity, and
  sharing characteristics.
- The access technology must be matched to the traffic profile, not only the
  peak line rate.
- Shared media require explicit reasoning about contention and user density.

Primary references:

- `references/02-physical-layer.md`
- `references/04-mac-sublayer.md`

## 10.5 L2/L3 boundary design

- Keep the L2 broadcast domain and the L3 policy boundary explicit.
- Use routing when policy, scale, failure isolation, or summarization require
  it.
- Use switching only where the shared L2 domain is operationally justified.
- Prevent loops and keep the loop-avoidance model understandable.

Primary references:

- `references/04-mac-sublayer.md`
- `references/09-addressing-and-subnet-design.md`

## 10.6 Addressing and subnet design

- The address plan must reflect stable administrative or topological
  boundaries.
- Reserve contiguous space for future aggregation.
- Capture gateway, DHCP, DNS, and service dependencies together with the
  subnet plan.
- Avoid treating addressing as an after-the-fact spreadsheet exercise.

Primary references:

- `references/09-addressing-and-subnet-design.md`
- `references/05-network-layer.md`

## 10.7 Routing and control-plane selection

- Choose routing scope before choosing routing protocol names.
- Intra-domain and inter-domain problems are different.
- Summarization, convergence, and operational visibility matter as much as raw
  reachability.
- SDN and MPLS should be justified by control or operational needs, not by
  trend-following.

Primary references:

- `references/05-network-layer.md`

## 10.8 Security integration

- Security must be reflected in topology, segmentation, and service exposure.
- Encryption does not replace segmentation.
- Authentication, PKI, VPN, TLS, IPsec, and DNSSEC must be chosen according to
  the trust model and threat boundary.

Primary references:

- `references/08-network-security.md`

## 10.9 Capacity, QoS, and experience

- Capacity planning requires a traffic model, not a guess.
- QoS and overprovisioning address different conditions.
- The relevant metric may be throughput, latency, jitter, loss, or user
  experience depending on the application.

Primary references:

- `references/05-network-layer.md`
- `references/06-transport-layer.md`
- `references/07-application-layer.md`

## 10.10 Validation and acceptance

Every design should produce a testable validation plan covering:

- L1/L2 health,
- gateway and prefix correctness,
- routing convergence and path expectations,
- transport establishment,
- application success,
- security control enforcement,
- resilience and rollback triggers.

Primary references:

- `references/troubleshooting-playbooks.md`
- `references/lifecycle-operations.md`

## 10.11 Standard design outputs

- analysis brief,
- addressing and subnet plan,
- logical and physical topology description,
- protocol and service matrix,
- security-zone and trust-boundary table,
- test matrix,
- controlled change package,
- operations and maintenance plan.

## Decision traceability matrix

| Design decision | Primary reference files | Typical applied concept |
|---|---|---|
| Access technology | `02`, `04` | medium, sharing, reach, interference |
| VLAN and subnet boundaries | `04`, `09` | L2/L3 separation, failure domain |
| Prefix sizing and summarization | `05`, `09` | CIDR, VLSM, aggregation |
| Routing model | `05` | intra-domain vs inter-domain control |
| Security controls | `08` | defense in depth, least privilege |
| QoS and performance posture | `05`, `06`, `07` | congestion, scheduling, QoE |
| Test and rollout plan | `troubleshooting-playbooks`, `lifecycle-operations` | per-layer validation, rollback |

## Anti-patterns and common mistakes

- Starting with vendor syntax before the design is justified.
- Designing a topology without a traffic or dependency model.
- Ignoring subnet and summarization structure until the end.
- Mixing bridging and routing boundaries without documenting the reason.
- Treating security as a later overlay rather than a design property.
- Declaring a design complete without a validation and rollback path.

# 09 – Addressing and subnet design

## Scope

Use this file when the task involves IPv4 or IPv6 address plans, subnetting,
CIDR, VLSM, route summarization, gateway placement, DHCP dependencies,
VLAN-to-subnet alignment, or growth planning.

## Authority lineage

This is a canonical local consolidation anchored primarily in the Internet
addressing and internetworking material of the network-layer reference plus the
book's treatment of communication subnets, VLAN boundaries, and operational
Internet addressing.

## Mental model

Addressing is not a clerical task. It defines:

- reachability,
- aggregation and routing scale,
- broadcast and failure domains,
- policy boundaries,
- growth limits,
- and the clarity of troubleshooting.

Good subnet design keeps the logical model simple enough that routing,
security, and operations remain explainable.

## 9.1 Two meanings of "subnet"

- In the broad networking sense, a communication subnet is the forwarding
  fabric that carries traffic between hosts.
- In Internet addressing practice, a subnet is a prefix-defined portion of an
  address space used to partition reachability and policy.
- Do not confuse the two meanings when reading requirements or designing a
  topology.

## 9.2 Address structure and prefix thinking

### IPv4

- IPv4 uses 32-bit addresses.
- A prefix determines the network portion; the remaining bits identify hosts
  or interfaces within that prefix.
- In practice, subnet design must align the prefix with the intended failure,
  policy, and broadcast domain.

### IPv6

- IPv6 uses 128-bit addresses.
- Prefix-based planning remains the core concept; the much larger space makes
  hierarchical allocation easier.
- IPv6 design should still respect administrative boundaries, growth, and
  summarization discipline.

## 9.3 Classful history and classless operation

- The book preserves classful addressing as historical context, not as the
  preferred design model.
- Modern address design is classless.
- CIDR replaces rigid class boundaries with explicit prefixes so allocation and
  aggregation reflect the actual topology and policy.

## 9.4 Core subnet-design workflow

1. Enumerate the required segments, zones, or VLANs.
2. Record the expected host counts, device classes, and growth margin.
3. Determine which segments must remain isolated for policy or failure-domain
   reasons.
4. Assign prefixes large enough for current demand plus controlled growth.
5. Place gateways at the intended L3 boundary.
6. Reserve contiguous space for future summarization.
7. Validate that the address plan still supports routing, DHCP, DNS, and test
   procedures.

## 9.5 Conventional IPv4 sizing rule used by this skill

For ordinary IPv4 subnet planning in this skill:

- total addresses in a prefix = `2^(host_bits)`,
- typical usable host count is planned conservatively as total minus network
  and broadcast addresses,
- the local calculator follows this conventional planning model for ordinary
  subnet sizing.

This is a planning rule, not a claim that every specialized deployment uses the
same host-address semantics.

## 9.6 VLSM and hierarchical allocation

- VLSM exists to fit different segment sizes without wasting the entire parent
  block.
- Allocate the largest required subnets first.
- Keep allocations contiguous whenever possible.
- Avoid scattering prefixes that should later summarize together.
- Group allocations by site, building, floor, service zone, or another stable
  administrative boundary.

## 9.7 CIDR and route aggregation

- CIDR reduces routing-state growth by allowing prefixes to summarize cleanly.
- Summaries should reflect real topology and policy.
- A summary is valuable only if the underlying subnets are contiguous and have
  compatible reachability policy.
- Do not summarize unrelated or operationally divergent networks simply to make
  a table look smaller.

## 9.8 VLANs, subnets, and L3 boundaries

- A VLAN is an L2 segmentation mechanism.
- A subnet is an L3 addressing construct.
- In disciplined enterprise design, the relationship between VLAN, subnet, and
  policy should be explicit and easy to explain.
- Do not stretch L2 domains without a clear operational reason.
- If two populations have different policy, fault-domain, or growth needs, they
  should rarely share the same subnet.

## 9.9 Gateway, DHCP, and service dependencies

- Every routed subnet needs a clear first-hop boundary.
- If hosts are dynamically addressed, DHCP scope design must align with the
  subnet plan.
- Routed separation may require DHCP relay behavior.
- DNS, default gateway, and time-service dependencies should be captured with
  the subnet plan, not left implicit.

## 9.10 IPv4/IPv6 coexistence planning

- Dual-stack or coexistence plans should preserve consistent administrative
  boundaries.
- Do not design IPv6 as an afterthought disconnected from the IPv4 policy
  model.
- Migration plans must include validation for naming, routing, ACLs, security,
  and observability in both families.

## 9.11 Deliverables that should exist

- Addressing principles and assumptions.
- Segment inventory with role, VLAN or zone, prefix, gateway, and services.
- Aggregation and summarization plan.
- Growth reserve statement.
- Validation checklist for overlaps, gaps, default gateways, and policy
  alignment.

## Quick decision tree

1. If the problem is overlap or ambiguity, validate the prefix inventory first.
2. If routing tables are growing uncontrollably, inspect summarization and
   allocation boundaries.
3. If gateway reachability is inconsistent, verify VLAN/subnet alignment before
   blaming the routing protocol.
4. If the design must scale, reserve contiguous space before assigning edge
   cases.
5. If the design mixes IPv4 and IPv6, verify that both families follow the same
   administrative logic.

## Subnet design checklist

- Does every subnet have an explicit purpose and owner?
- Is the L3 boundary clear?
- Are the prefixes contiguous where summarization is expected?
- Is growth space reserved?
- Are DHCP, gateway, DNS, and security dependencies recorded?
- Does the plan respect failure and trust boundaries?

## Anti-patterns and common mistakes

- Subnetting only by habit, without policy or failure-domain logic.
- Reusing the same subnet for users, servers, guests, and IoT.
- Allocating small discontiguous prefixes that destroy future aggregation.
- Treating a VLAN ID as if it were automatically a sound subnet design.
- Forgetting to document the first-hop gateway and service dependencies.
- Designing IPv6 separately from the operational logic of the rest of the
  network.

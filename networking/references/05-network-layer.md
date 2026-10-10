# 05 – Network layer

## Table of contents
- Scope
- Mental model
- 5.1 Design issues
- 5.2 Routing algorithms
- 5.3 Traffic management and congestion
- 5.4 QoS and QoE
- 5.5 Internetworking
- 5.6 SDN
- 5.7 The network layer in the Internet
- 5.8 Network-layer policy
- Selection guide
- Troubleshooting checklist
- Anti-patterns

## Scope
Use this file when the problem involves IP, addressing, subnetting,
forwarding, routing, QoS, congestion, MPLS, SDN, OSPF, BGP, or
interconnection of heterogeneous networks.

## Mental model
The network layer decides how to carry packets across one or more links and
networks, even when:

- the links are heterogeneous,
- the topology changes,
- the load is uneven,
- and the administrative domains do not fully cooperate.

The correct reasoning sequence is:

1. define the desired network service,
2. distinguish forwarding from routing,
3. choose how to handle congestion and QoS,
4. map it to the real Internet: IPv4/IPv6, control protocols, IGP/EGP, MPLS,
   etc.

## 5.1 Network layer design issues
### 5.1.1 Store-and-forward packet switching

- Each router receives the packet, briefly stores it, and forwards it.
- Introduces delay from transmission, propagation, processing, and queueing.
- If demand exceeds sustained capacity, the queue grows and congestion
  appears.

### 5.1.2 Services provided to the transport layer

- **Connectionless service / datagram**:
  - each packet is routed independently,
  - robust and simple,
  - ideal for the open, scalable Internet.
- **Connection-oriented service / virtual circuit**:
  - the network maintains per-flow state,
  - facilitates QoS/reservation,
  - more complex and sensitive to state failures.

### 5.1.3 Implementation of connectionless service

- The router decides the next hop using a forwarding table keyed by
  prefix/destination.
- No prior "circuit setup" is needed.
- Excellent for scaling and resilience to topological changes.

### 5.1.4 Implementation of connection-oriented service

- Before traffic flows, a path/state is established.
- Forwarding then uses circuit identifiers or labels.
- Useful when it is advantageous to separate setup from forwarding and to
  provide preferential treatment.

### 5.1.5 Comparison of virtual-circuit and datagram networks

- **Datagram**: more flexible, less per-flow state, better for the broad
  Internet.
- **Virtual circuit**: better if reservation, traffic engineering, or strong
  path control is needed.
- Practical rule: if the user is talking about the general Internet, start
  with datagram; if managed services/QoS/label switching, consider path
  virtualization.

## 5.2 Routing algorithms within a network
### Critical distinction: forwarding vs. routing

- **Forwarding**: local decision about which interface to use for an already
  known packet.
- **Routing**: global/distributed process that builds the information needed
  for forwarding.
- Common mistake: confusing symptoms of a stale table with routing-algorithm
  problems, or vice versa.

### 5.2.1 Optimality principle

- If router J lies on the optimal path from I to K, then the sub-path from
  J to K is also optimal.
- This gives rise to the notion of a sink tree and the basis of many path
  algorithms.

### 5.2.2 Shortest path algorithm

- The chapter uses Dijkstra as the reference for link-state.
- Requires non-negative costs.
- "Cost" can represent hops, delay, distance, or another metric.
- Choosing the metric is already an architectural decision, not merely
  mathematics.

### 5.2.3 Flooding

- Forwards on all links except the incoming one.
- Very robust and conceptually simple.
- Extremely expensive in overhead; used as a base concept, not as a general
  policy for the modern network.
- Useful as an extreme reference for reach/robustness, not efficiency.

### 5.2.4 Distance vector routing

- Each router maintains distance estimates to destinations and exchanges them
  with neighbors.
- Associated with distributed Bellman-Ford.
- Classic problem: **count-to-infinity** and slow convergence under certain
  failures.
- Good for small/simple networks; less attractive as scale grows.

### 5.2.5 Link state routing

- Each router floods the state/cost of its links.
- All routers build a graph view and compute best paths locally.
- Generally better convergence and behavior than distance vector at large
  scale, at the cost of greater control complexity.

### 5.2.6 Hierarchical routing within a network

- Groups topology into levels/areas for scaling.
- Reduces local state size at the cost of some loss in global optimality.
- In large networks, hierarchy is not an optional optimization; it is a
  scaling requirement.

### 5.2.7 Broadcast routing

- Needed when a packet must reach all relevant nodes.
- Can be implemented with spanning trees, controlled flooding, or other
  techniques.
- Key question: is broadcast truly necessary, or would multicast/anycast
  suffice?

### 5.2.8 Multicast routing

- Delivers to a group, not to everyone.
- Designed to avoid unnecessary duplication and save bandwidth.
- Very useful when multiple replicas/members need the same flow.

### 5.2.9 Anycast routing

- Sends to the "nearest" or most appropriate member of an equivalent set.
- Highly relevant for DNS, CDNs, and distributed services.
- Actual "nearness" depends on routing policy and the point of observation.

## 5.3 Network-layer traffic management
### 5.3.1 Need for traffic management: congestion

- Congestion appears when the offered load exceeds effective capacity at some
  point in the network.
- Symptoms: growing queues, loss, high delay, jitter, timeouts, resends,
  poor QoE.
- Increasing buffers does not always cure the problem; it may worsen latency
  under load.

### 5.3.2 Approaches to traffic management

- The chapter contrasts preventive and reactive measures.
- Typical tools:
  - admission control,
  - traffic-aware routing,
  - queue management,
  - policing/shaping,
  - load shedding,
  - feedback to endpoints or to the control plane.
- Operational insight: congestion is not solved at a single layer; the
  network and transport layers interact, but much of the queueing behavior
  is defined here.

## 5.4 Quality of Service and application QoE

### 5.4.1 Application QoS requirements

- Different applications demand different combinations of throughput, delay,
  jitter, and loss.
- Not all loads need the same scheduling policy.

### 5.4.2 Overprovisioning

- A simple and powerful solution when economically viable.
- Reduces the need for fine control but does not substitute for design in all
  cases.
- Must not be used as an excuse to ignore structural bottlenecks.

### 5.4.3 Packet scheduling

- How queues are drained changes fairness and delay.
- The chapter covers disciplines such as FIFO and weighted options for
  differential treatment or fairness approximation.
- If the user requests QoS, always ask about the queue discipline, not just
  the reserved bandwidth.

### 5.4.4 Integrated Services

- Per-flow reservation and state.
- Greater precision, less scalability.
- Natural when the goal is strict guarantees and the scale is contained.

### 5.4.5 Differentiated Services

- Classifies traffic into aggregate classes and applies per-behavior
  treatment.
- Scales better than maintaining per-flow state.
- Often the practical way to prioritize without extreme complexity.

### QoS vs. QoE

- QoS measures network properties; QoE measures the impact on the
  application/user.
- A correct design does not end at "loss < x%"; ask what the user or final
  service actually sees.

## 5.5 Internetworking

### 5.5.1 Internetworks: overview

- Connecting different networks means translating differences in service,
  packet size, addressing, and control.

### 5.5.2 How networks differ

- Common differences:
  - maximum packet sizes,
  - addressing schemes,
  - QoS,
  - connectionless/connection-oriented models,
  - security and administrative policies.

### 5.5.3 Connecting heterogeneous networks

- Gateways/routers must hide enough heterogeneity so the endpoint sees a
  coherent service.
- Not every translation is free; there can be loss of semantics or
  performance.

### 5.5.4 Connecting endpoints across heterogeneous networks

- The real goal is for hosts to communicate, not merely for "the networks to
  be joined."
- If the network works but the application does not, check MTU,
  fragmentation, and end-to-end semantics before declaring success.

### 5.5.5 Internetwork routing

- When the path crosses multiple networks, policies, transit, peering, and
  route aggregation come into play.
- The chosen route may be policy-driven rather than topologically optimal.

### 5.5.6 Packet fragmentation

- Arises when a downstream link does not support the current packet size.
- Costs: overhead, reassembly, amplified loss, complex troubleshooting.
- Prudent design: avoid excessive dependence on fragmentation.

## 5.6 Software-Defined Networking

### 5.6.1 Overview

- More clearly separates the control plane from the data plane.
- Allows logically centralized control over distributed forwarding.

### 5.6.2 SDN control plane

- Control software with a global or semi-global view.
- Facilitates consistent policy, automation, and experimentation.
- Risk: concentration of complexity and dependence on well-designed control.

### 5.6.3 SDN data plane

- Programmable hardware that applies forwarding/telemetry rules.
- Very useful when the network must adapt quickly without per-box manual
  reconfiguration.

### 5.6.4 Programmable network telemetry

- Telemetry is no longer just SNMP/basic counters; the network can export
  rich data-plane information.
- Useful for capacity planning, troubleshooting, and policy validation.

## 5.7 The network layer in the Internet

### 5.7.1 IPv4

- Base protocol of the traditional Internet.
- Datagram, best effort, header with control/fragmentation/TTL fields, etc.
- Does not promise delivery; cooperates with upper layers and control
  protocols.

### 5.7.2 IP addresses

- The address identifies an interface/logical location in the internetwork.
- Subnetting and aggregation reduce table sizes and organize administration.
- Use `subnet-calculator.py` to work out VLSM/CIDR; the theory here
  explains why aggregation matters as much as capacity.

### 5.7.3 IPv6

- Expands the address space and cleans up several aspects of IPv4 design.
- Simplifies certain functions and reduces dependence on router
  fragmentation.
- If the user is designing for the long term, IPv6 must enter at least as an
  evolution plan.

### 5.7.4 Internet control protocols

- Include signaling and control mechanisms necessary for IP operation.
- They are not "application"; they are part of the internetwork's actual
  functioning.
- If they fail, the network may lose observability, reachability, or
  diagnostics.

### 5.7.5 MPLS

- Inserts labels to separate forwarding from control and enable richer
  paths.
- Very useful for traffic engineering, managed VPNs, and QoS-based services.
- Key idea from the chapter: multiple control protocols can feed the same
  label-forwarding mechanism.

### 5.7.6 OSPF

- Widely used IGP for intradomain routing.
- Based on link state.
- Requirements highlighted in the text:
  - open standard,
  - varied metrics,
  - dynamic adaptation,
  - load balancing,
  - hierarchy through areas,
  - some security,
  - support for links and multiaccess networks.
- Operational concepts:
  - areas,
  - backbone area,
  - area border routers,
  - LSA exchange,
  - per-router SPF.
- If the problem is within an organization/AS, OSPF is a natural candidate.

### 5.7.7 BGP

- Internet EGP for interdomain routing.
- It does not pursue efficiency alone; it pursues policies acceptable among
  ASes.
- Key concepts:
  - AS,
  - reachability by prefix,
  - path vector,
  - export/import policies,
  - transit vs. non-transit.
- Correct BGP diagnosis always incorporates policy and business
  relationships.

### 5.7.8 Internet multicasting

- Extends the network for groups, not just unicast.
- Conceptually useful for efficient distribution, although its global
  deployment is more limited than unicast/CDN.

## 5.8 Network-layer policy

### 5.8.1 Peering disputes

- Interconnection is neither technically nor economically neutral.
- Peering problems can impact path, congestion, and user experience.

### 5.8.2 Traffic prioritization

- Prioritizing traffic can be technically justifiable but has neutrality and
  network-policy implications.
- Recommendations should separate the technical argument from the regulatory
  decision.

## "When to use what" guide

- **OSPF**: routing within a coherently administered network/AS.
- **BGP**: routing among ASes or interconnected domains with their own
  policy.
- **MPLS**: traffic engineering, provider VPN, separation of forwarding and
  control, managed QoS.
- **DiffServ**: scalable prioritization by class.
- **IntServ**: finer guarantees where scale permits.
- **Anycast**: replicated services such as DNS and edge delivery.
- **SDN**: when centralized automation/policy provides more value than the
  added complexity.

## Quick decision tree

1. If the question is "how do I divide my IP space?", go to
   addressing/CIDR.
2. If it is "how do packets travel within my network?", go to IGP/OSPF.
3. If it is "how do I advertise or receive routes between organizations?",
   go to BGP.
4. If the pain is delay/jitter under load, review queues, scheduling, and
   congestion.
5. If the user needs managed path policies/services, evaluate MPLS.
6. If the network is too large to operate manually, consider SDN/telemetry.

## L3 troubleshooting checklist

- Is the IP/mask/prefix correct?
- Does a valid route or default route exist?
- Does the forwarding table match the current topology?
- Was there a recent reconvergence or flap?
- Is there a fragmentation/MTU path issue?
- Are queue or scheduling disciplines degrading sensitive applications?
- Is the problem BGP policy/peering rather than pure reachability?

## Anti-patterns and common mistakes

- Designing only for the shortest path and ignoring interdomain policy.
- Mixing too many L2/L3 functions without clear boundaries.
- Assuming that BGP "fixes" a poorly designed internal topology.
- Ignoring prefix aggregation and then suffering unnecessary table
  growth/operations.
- Relying on fragmentation as a normal interoperability solution.
- Talking about QoS without specifying classes, queues, or target metrics.
- Introducing SDN without clarity on which policy or operation it actually
  improves.

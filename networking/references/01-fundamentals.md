# 01 – Network fundamentals

## Scope

Use this file when the user requests general architecture, compares
technologies, mixes multiple layers, or needs vocabulary/conceptual grounding
before diving into a more specific problem.

## What this chapter establishes for the rest of the skill

- A network is a collection of autonomous interconnected devices capable of
  exchanging information.
- The discipline is best understood by separating **media**, **protocols**,
  **services**, **interfaces**, **control**, and **policies**.
- Correct decisions almost always emerge from answering four questions:
  1. Which entities communicate?
  2. Over which medium or composite network?
  3. With what performance and reliability requirements?
  4. With what administrative and security boundaries?

## 1.1 Uses of networks and traffic classes

### 1.1.1 Information access

- Dominant model: client-server; the client requests and the server responds.
- The primary utility is to bring remote data and applications closer to the
  end user.
- Typical traffic is request/response and usually depends on names, paths,
  reasonable latency, and service availability.
- Modern use cases: Web, digital libraries, mobile applications, content
  platforms, and cloud services.

### 1.1.2 Person-to-person communication

- Includes email, messaging, voice, video, social networks, and remote
  collaboration.
- Latency, jitter, and loss matter more than raw throughput in interactive
  sessions.
- Networks allow replacing physical travel with data exchange.

### 1.1.3 Electronic commerce

- Mixed traffic: browsing, queries, authentication, payments, confirmations.
- Demands integrity, authentication, availability, and traceability.
- It is advisable to separate the user plane, control plane, and exposed
  surface.

### 1.1.4 Entertainment

- Streaming and gaming drive high volume and jitter sensitivity.
- Content distribution requires caches, CDNs, and proximity to the user.
- Not all "multimedia" traffic has the same needs: stored, live, and
  interactive profiles are distinct.

### 1.1.5 Internet of Things

- Adds devices with modest compute, long lifespans, and uneven security.
- The value lies in sensing, reporting, and acting; the risk lies in massive
  exposure.
- Correct design: isolation, authentication, least authority, and visibility.

## 1.2 Access and administrative network types

### 1.2.1 Broadband access networks

- Aim to connect homes/small sites to the general Internet.
- Common media: copper, coaxial, fiber, and mobile access.
- The bottleneck is usually the "last mile", not the provider's backbone.

### 1.2.2 Mobile and wireless access networks

- Combine mobility, shared spectrum, handoff, and variable coverage.
- Distinguish **wireless** from **mobile**: not every wireless device is
  mobile, nor does every mobile device use radio in every scenario.
- Medium access control and mobility management are part of the problem.

### 1.2.3 Content provider networks

- Datacenters, server farms, and CDNs bring content closer to demand.
- Design here requires thinking about cross-section bandwidth, scaling, and
  power.
- The relative location between users and replicas changes perceived
  performance.

### 1.2.4 Transit networks

- Carry traffic between networks that are not directly connected.
- The transit-versus-peering decision is both technical and political: cost,
  scale, control.
- A "correct" route is not always the shortest; it may be the cheapest or the
  only one allowed by interdomain policy.

### 1.2.5 Enterprise networks

- Aim to share resources, information, and internal communication.
- Typically mix LANs, WLANs, remote access, VPN, and Internet egress.
- The design must reflect administrative boundaries, security boundaries, and
  operational dependence on critical services.

## 1.3 Network technology: from local to global

### 1.3.1 PAN

- Personal-area networks for short range and low physical complexity.
- Classic example: Bluetooth between peripherals and a primary device.
- Useful when cabling cost/ergonomics dominate the decision.

### 1.3.2 LAN

- Private network of local scope; typically Ethernet or WiFi.
- Common properties: low latency, relatively rare errors, local control.
- Wired LAN: point-to-point links with switching.
- Wireless LAN: shared medium, interference, association, and authentication.

### 1.3.3 Home network

- Special case of a LAN with extreme heterogeneity and non-expert
  administration.
- Typical problems: WiFi coverage, weak IoT security, AP performance,
  blame incorrectly assigned to the ISP when the internal network fails.
- Design should prioritize operational simplicity and practical segmentation.

### 1.3.4 MAN

- Metropolitan coverage; historical example: cable networks.
- Relevant when there is regional aggregation and multiple users on the same
  access infrastructure.

### 1.3.5 WAN

- Connects geographically dispersed sites.
- The communication subnet consists of transmission lines and switching/
  forwarding elements (routers).
- Links may be dedicated or virtualized over third-party infrastructure.
- Differences from a LAN are not merely distance: separate administration,
  technological heterogeneity, and routing policies.

### 1.3.6 Internetworks

- An internet is a collection of networks interconnected and independently
  administered.
- The network-layer gateway enables joining different technologies without
  ascending to the logic of a specific application.
- Practical rule: when administrative domains or underlying technology change,
  think internetworking, not a single homogeneous network.

## 1.4 Network examples

### Internet

- A network of networks, not a single uniform network.
- Evolved from ARPANET and NSFNET into a commercial infrastructure with ISPs,
  IXPs, transit, peering, CDNs, and large content providers.
- Key operational insight: the architecture is economic and political in
  addition to technical.

### Mobile networks

- Have their own architecture: radio access + core network.
- The radio plane is not designed like a LAN; coverage, cells, paging,
  handoff, and spectrum change the problem.

### Wireless networks (WiFi)

- Dominate local wireless access.
- Blend a shared medium with distributed control and an access point that
  bridges the air to the wired network.

## 1.5 Network protocols

### Design objectives

- Reliability.
- Efficient resource allocation.
- Modular evolution and replacement.
- Interoperability between implementations.
- Security and privacy.
- Administrative and technical scalability.

### Protocol layering

- Communication between peer layers is logical/virtual; the actual transfer
  descends the local stack, crosses the medium, and ascends the remote stack.
- A clean interface reduces coupling and allows replacing one layer without
  rewriting all the others.
- A network architecture is the set of layers, protocols, and functions per
  layer.
- A protocol stack is the concrete instance used by a system.

### Connections and reliability

- Not all communication requires a connection-oriented or fully reliable
  service.
- Connection and error-recovery decisions depend on the layer and the
  application type.
- Connection-oriented: useful when order, state, and explicit control matter.
- Connectionless: useful when simplicity or tolerance for loss/reordering
  matter.

### Service primitives

- A layer offers services to the layer above via primitives and interfaces.
- Always distinguish between **service** (what a layer offers) and
  **protocol** (how two peer entities cooperate to provide it).

### Service/protocol relationship

- The protocol is the mechanism; the service is the consumable abstraction
  for the layer above.
- Common error: diagnosing by looking only at the visible protocol rather
  than the service the application actually needs.

## 1.6 Reference models

### OSI

- Seven layers; useful as a mental model and fault taxonomy.
- Good for explaining separation of functions and interface points.
- Do not assume every real implementation rigidly adheres to the model.

### TCP/IP

- Model closest to the real Internet.
- Less prescriptive than OSI and more closely aligned with deployed
  protocols.
- Ideal for reasoning about host-to-host, routing, and transport/application
  services.

### Operational critiques

- OSI: conceptually valuable, less influential in real deployment.
- TCP/IP: practical, but with fuzzy layer boundaries in several
  implementations.
- Useful conclusion: use OSI to locate and communicate faults; use TCP/IP to
  explain the real behavior of the Internet.

## 1.7 Standardization

- Interoperability depends on open standards and shared processes.
- In telecom: bodies such as the ITU and historical carrier-world
  organizations.
- In international standards: ISO/IEC.
- In the Internet: IETF, IAB, W3C, and the related ecosystem.
- Open source also matters because it accelerates implementation and
  adoption.

## 1.8 Policy, legal, and social issues

- Online speech: the network transports data, but its design conditions
  visibility and control of discourse.
- Net neutrality: traffic prioritization has both a technical and a political
  dimension.
- Security: it is not an add-on; it affects every layer.
- Privacy: metadata, name resolution, encryption, and access control matter.
- Disinformation: infrastructure can amplify distribution and reach.

## 1.9 Metrics and units to use with discipline

- Throughput: effective rate of useful delivery.
- Bandwidth: channel or link capacity.
- Delay/latency: end-to-end or per-segment transit time.
- Jitter: temporal variation, critical in interactive media.
- Loss: observable loss; sometimes congestion, sometimes radio, sometimes
  queueing.
- Fairness: reasonable sharing among competing flows.
- QoE: experience perceived by the application/user, not just link metrics.
- Use bits/s for line speed and clearly separate bytes from bits.

## Quick decision tree

1. If the user does not know "where" the problem is, classify it by layer.
2. If the question involves coverage, distance, modulation, or access, go to
   Layer 1.
3. If it involves VLAN, STP, FCS, WiFi association, or switching, go to
   Layer 2.
4. If it involves subnetting, routes, OSPF, BGP, MPLS, congestion, or QoS,
   go to Layer 3.
5. If it involves ports, handshake, retransmissions, or end-to-end
   throughput, go to Layer 4.
6. If it involves DNS, HTTP, email, streaming, or CDN, go to Layer 7.
7. If it involves encryption, authentication, firewall, IDS, VPN, or
   spoofing, overlay the security file on top of the primary functional
   layer.

## When to use which mental model

- **OSI** for diagnosis and documentation.
- **TCP/IP** for the real Internet and deployed services.
- **Client-server** for centralized applications.
- **P2P** when roles are not fixed or load/content is distributed.
- **Internetworking** when the network crosses administrative or
  technological domains.

## Anti-patterns and common mistakes

- Treating the Internet as a single homogeneous network without policy or
  economics.
- Confusing service with protocol.
- Confusing bandwidth with usable throughput.
- Designing without separating interactive, bulk, and control traffic.
- Solving everything with "more capacity" without examining queues, policies,
  or the application.
- Ignoring security and privacy until the end of the design.
- Designing the physical network without considering the administrative
  boundaries of operations.
- Insisting on using only OSI or only TCP/IP as a complete explanation; both
  models are tools, not the full reality.

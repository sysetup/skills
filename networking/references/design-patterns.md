# Network design patterns

## Scope

Use this file when the user requests a target architecture, reference pattern,
or topology options for campus, datacenter, WAN, cloud-hybrid, SOHO, or IoT.

## Authority status

This file is an operational synthesis.

- Read `references/00-source-authority.md` first for precedence rules.
- Validate addressing and subnet choices against
  `references/09-addressing-and-subnet-design.md`.
- Validate the design workflow against
  `references/10-network-analysis-and-design.md`.
- If a pattern conflicts with a canonical reference, the canonical reference
  wins.

## Pattern lineage matrix

| Pattern family | Primary authority files |
|---|---|
| Campus / enterprise | `01`, `04`, `05`, `08`, `09`, `10` |
| Datacenter / content provider | `01`, `05`, `07`, `08`, `10` |
| Corporate WAN | `02`, `05`, `08`, `09`, `10` |
| Cloud-hybrid / distributed Internet service | `05`, `07`, `08`, `10` |
| SOHO / branch | `02`, `04`, `08`, `09`, `10` |
| IoT / control overlay | `01`, `02`, `04`, `08`, `10` |

## How to choose a pattern

Always evaluate these axes before selecting the template:

- number and dispersion of sites,
- dominant traffic: user-to-server, east-west, streaming, control,
- mobility required,
- sensitivity to latency/jitter,
- administrative and security boundaries,
- need for growth, redundancy, and operational simplicity.

## Recurring textbook components reused by the patterns

- Ethernet switching and VLANs for local segmentation.
- WiFi/802.11 for local mobility.
- IP routing with OSPF within administrative domains.
- BGP when interconnection between ASes or interdomain policies are involved.
- MPLS or VPN when the path or service must be controlled more richly.
- TLS/IPsec/VPN/802.1X for securing sessions, tunnels, and access.
- DNS, Web, CDN, and anycast for service distribution to users.

## Pattern 1 – Campus / multi-building enterprise

### Objective

Connect users, local servers, WLAN, and WAN/Internet egress with predictable
operation and clear boundaries between access, distribution, and edge.

### Building blocks

- Wired access with switched Ethernet.
- Wireless access with 802.11 APs.
- VLANs to segment by function, security, or operational domain.
- Routing between VLANs/subnets at the L3 boundary.
- OSPF as the natural IGP for the internal domain if scale requires it.
- Firewalls and authentication services at the edge or between critical
  zones.

### Addressing

- Aggregate by building, floor, or function to simplify summarization and
  troubleshooting.
- Maintain consistency between VLAN, subnet, and policy.
- Reserve space for growth and for separate WLAN/IoT segments.

### Security

- 802.1X/EAP or at least WPA2/WPA-class enterprise on the corporate WLAN.
- Separate VLANs/zones for users, guests, management, and IoT.
- Defense in depth: perimeter + internal segmentation + per-host controls.

### When to use it

- Universities, offices, hospitals, light industrial campuses.
- Sites with many users and a mix of wired + WLAN.

### Anti-patterns

- Stretching L2 unnecessarily between buildings.
- Creating VLANs with no correspondence to policy or failure domain.
- Leaving L2 redundancy without loop control.

## Pattern 2 – Datacenter / content provider

### Objective

Optimize service delivery from a dense set of servers with strong east-west
traffic and/or high volume toward external users.

### Building blocks

- Server farms or dense clusters.
- High-capacity switching with attention to cross-section bandwidth.
- Aggregation/routing toward backbone and Internet.
- Tight integration with CDN, proxies, or content distribution layers.
- More careful telemetry and traffic control than in a conventional office.

### Traffic direction

- **East-west**: between servers/applications within the datacenter.
- **North-south**: between users/Internet and the datacenter.
- The correct pattern depends on which direction dominates.

### Routing and control

- Coherent internal IP and routing; the network-layer chapter suggests that
  scaling and visibility are more important priorities than the details of a
  "fashionable" topology.
- SDN can be valuable when forwarding policy and telemetry must be highly
  programmable.

### Security

- Strict segmentation between service zones.
- Protection of exposed services with firewalls and TLS.
- Careful authentication and PKI for internal services when the risk
  warrants it.

### When to use it

- Web platforms, content services, cloud applications, shared infrastructure.

### Anti-patterns

- Designing only for north-south when the real load is east-west.
- Relying on a single perimeter firewall for the entire datacenter.
- Ignoring content placement and depending on a single remote origin.

## Pattern 3 – Multi-site corporate WAN

### Objective

Connect geographically dispersed offices, plants, or headquarters with an
operable model of reachability, prioritization, and security.

### Building blocks

- Per-site routers.
- Dedicated links, Internet + VPN, provider MPLS, or a combination.
- OSPF within the internal domain; BGP if interacting with multiple
  providers or domains with their own policy.
- IPsec/VPN for privacy over public infrastructure.

### Path design

- Do not seek only the shortest path; incorporate cost, resilience, and
  policy.
- If the service is critical, define a backup path and a clear failover
  criterion.
- Consider satellite/cellular latency if remote sites use those accesses.

### QoS

- Classify interactive, critical, and best-effort traffic.
- Use DiffServ/scheduling if WAN access is limited and the business depends
  on voice, video, or delay-sensitive transactions.

### Security

- Site-to-site or user-to-site tunnels.
- Separation between corporate, management, and Internet-egress traffic.
- Explicit validation of who advertises what route when multiple edges exist.

### When to use it

- Enterprises with multiple sites, retail chains, regional offices,
  geographically distributed operations.

### Anti-patterns

- Extending one site's LAN to all others.
- Mixing Internet breakout and corporate traffic without explicit policy.
- Not modeling the loss of a site or a provider.

## Pattern 4 – Cloud-hybrid / Internet-facing distributed service

### Objective

Join a corporate network or own datacenter with distributed/edge services and
external users over the real Internet.

### Building blocks

- Primary datacenter or server farm.
- Replicas or edge CDN close to users.
- DNS and anycast/replica selection to steer toward appropriate instances.
- Tunnels/VPN for management or secure integration with private sites.
- Possible use of MPLS/SDN for managed path segments.

### Design logic

- Separate the user plane, management plane, and content distribution plane.
- The user must not depend on a single remote origin if the traffic pattern
  is global or massive.
- DNS and CDN behavior is part of the architecture, not an accessory.

### Security

- TLS by default toward users.
- DNSSEC/TLS when the threat model requires it.
- Solid PKI for exposed services.
- Segmentation between internal operations and public service.

### When to use it

- SaaS, global Web applications, services with geographically distributed
  external users.

### Anti-patterns

- Managing a global service as if it were a single central site.
- Forgetting the impact of peering, transit, and replica selection on
  experience.
- Mixing administrative traffic with public traffic without strong
  separation.

## Pattern 5 – SOHO / home office / small branch

### Objective

Provide simple and secure connectivity for few users, with minimal
operational cost.

### Building blocks

- Access router.
- WiFi as the primary medium; local Ethernet optional.
- Basic segmentation between users, guests, and IoT when possible.
- VPN to the enterprise if access to internal resources is needed.

### Design principles

- Prioritize simplicity and secure defaults.
- The local network should not needlessly compete with the shared WAN
  access.
- If the environment is residential, the frequent problem is the local WLAN,
  not the ISP.

### Security

- Current WPA2/WPA-class, no WEP.
- Separate passwords and credentials for administration and general access.
- Isolation of IoT/guest if untrusted devices are present.

### When to use it

- Telecommuting, small offices, clinics, light retail.

### Anti-patterns

- Reusing a single network for guests, work, and IoT.
- Depending on a poorly placed WiFi AP and blaming only the provider.
- Leaving management exposed without necessity.

## Pattern 6 – IoT / sensor and control overlay

### Objective

Connect sensors, actuators, and embedded devices with reasonable security and
sustainable operation.

### Building blocks

- PAN/Bluetooth or WLAN/cellular depending on range and power consumption.
- Gateways that separate devices from the rest of the enterprise/home
  network.
- Lightweight or datagram transport when the traffic pattern is short and
  frequent.
- Centralized control/telemetry services when the node count grows.

### Design principles

- Do not assume the device has good security.
- Minimize privileges and exposure.
- Separate control, data, and management traffic.
- Design with long lifespan and difficult updates in mind.

### Security

- Strict segmentation.
- Per-device/role authentication when possible.
- Traffic monitoring, because many devices expose metadata even if they
  encrypt the payload.

### When to use it

- Smart building, light industrial sensors, distributed telemetry, smart
  home.

### Anti-patterns

- Placing IoT on the same VLAN as users or critical servers.
- Trusting manufacturer defaults.
- Treating a wireless sensor as if it were a conventional manageable host.

## Cross-cutting rules for all patterns

- Reduce broadcast domains and failure domains.
- Keep the L2/L3 boundary explicit.
- Keep VLAN, subnet, and policy alignment explicit.
- Design observability from the start.
- Plan rollback and per-layer testing.
- Security must be reflected in the topology, not only in a document.

## Quick selection tree

1. Many local users and several buildings → Campus.
2. Heavy traffic between servers or massive service from servers →
   Datacenter.
3. Dispersed sites with intersite connectivity → Corporate WAN.
4. Global or hybrid service with edge/CDN → Cloud-hybrid.
5. Few users and minimal operations → SOHO.
6. Many embedded devices and high exposure risk → IoT overlay.

## How to combine patterns

- Campus + WAN: classic multi-site enterprise.
- Datacenter + CDN + Cloud-hybrid: global Web service.
- SOHO + VPN: telecommuting.
- Campus + IoT overlay: smart building or light industry.
- WAN + cellular/satellite: remote sites with heterogeneous access.

## Recommended deliverables per pattern

- Textual logical and physical diagram.
- Addressing and aggregation plan.
- Per-layer protocol matrix.
- Security zone and trust boundary table.
- Test plan: connectivity, failover, security, QoE.

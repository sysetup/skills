# Lifecycle operations

## Scope

Use this file for capacity planning, ongoing operation, change management,
monitoring, continuity, maintenance, and network evolution.

## Authority status

This file is an operational synthesis anchored in the canonical references,
especially `references/05-network-layer.md` through
`references/10-network-analysis-and-design.md`.

- Use `references/00-source-authority.md` for precedence.
- Use this file to operationalize the canonical concepts, not to override
  them.
- If an operational shortcut would contradict the canonical addressing,
  routing, security, or validation model, reject the shortcut.

## Guiding principle

Correct network operation is a cycle, not an event:

1. understand demand,
2. design with margin and observability,
3. change with control,
4. verify per layer,
5. measure deviations,
6. evolve without losing security or stability.

## 1. Operational baseline

### What to capture

- Current logical and physical topology.
- Addressing and aggregation plan.
- Per-layer protocols and their dependencies.
- Interconnection points, transit, VPN, and critical services.
- Normal levels of throughput, delay, jitter, loss, and errors per access.
- Typical behavior of routes, OSPF/BGP neighbors, and DNS/CDN selection
  when applicable.

### Why it matters

- Without a baseline, you cannot distinguish degradation from normal
  behavior.
- The textbook's performance and QoE chapter justifies measuring both the
  network and the application experience.

## 2. Capacity planning

### Minimum inputs

- Number of users, sites, and devices.
- Traffic classes: bulk, interactive, media, control, management.
- Projected growth and peak patterns.
- Nature of access: dedicated or shared.
- Application sensitivity to delay, jitter, loss, and availability.

### Recommended method

1. Build a current and projected traffic matrix.
2. Identify the links/segments most likely to congest.
3. Determine whether the problem is sustained capacity, burst, RTT/window,
   or contention.
4. Decide among overprovisioning, QoS, topological redesign, or edge
   placement.
5. Reserve margin for growth and for single-component failures.

### Signs that capacity is lacking

- Persistent queues at peak hours.
- High jitter on interactive media.
- Growing retransmissions or timeouts without notable physical errors.
- Users in specific regions with poor QoE due to distance from origin/CDN.
- Upstream saturation on shared access (HFC/WLAN/cellular).

### Valid strategies from the source material

- More physical capacity when the medium is the real limit.
- Overprovisioning when cost is acceptable.
- QoS and scheduling when the resource is scarce and traffic classes differ.
- CDN/proxy/replication when the problem is content distribution.
- Better congestion control/windows when the bottleneck is end-to-end.

## 3. Change management

### Preparation

- Define the exact objective of the change.
- Enumerate affected layers.
- Identify dependencies: addressing, routing, switching, security, naming,
  certificates, tunnels, applications.
- Prepare an implementation and rollback plan.
- Establish success and abort criteria.

### Operational rules

- Change one observable thing at a time whenever possible.
- Avoid simultaneous modifications to L2, L3, and security without
  sufficient telemetry.
- If redundancy exists, change the non-critical path or segment first.
- For routing changes, plan convergence and stabilization time.
- For security changes, validate useful reachability, not just "tunnel up."

### Recommended sequence

1. Pre-check current state.
2. Change window with defined responsible parties.
3. Step-by-step execution.
4. Immediate per-layer verification.
5. Post-change monitoring.
6. Close or rollback based on evidence.

## 4. Monitoring and observability

### Minimum per-layer metrics

- Physical: carrier, power/SNR, physical errors, renegotiations.
- Link/MAC: FCS/CRC, retries, broadcast, MAC flapping, STP, WiFi
  association.
- Network: reachability, tables/routes, convergence, loss, MTU, control
  events.
- Transport: handshake, RTT, retransmissions, windows, resets.
- Application: DNS latency, HTTP status/TTFB, email delivery, buffering,
  QoE.
- Security: firewall rejections, IDS/IPS events, tunnel state,
  authentication failures.

### What to observe beyond averages

- Percentiles and peaks, not just the mean.
- Differences between off-peak and peak hours.
- Differences among sites, SSIDs, VLANs, prefixes, or traffic classes.
- Route changes or replica-selection changes in distributed services.

### Practical principle

- Measure close to the user and close to the service when the problem is
  experience.
- Measure in the data plane and, if possible, in the control plane when the
  problem is convergence.

## 5. Incident management

### Classification

- Total outage.
- Partial degradation.
- Intermittency.
- Security exposure.
- Localized vs. systemic problem.

### Initial response

- Contain damage.
- Preserve useful evidence.
- Estimate the blast radius.
- Decide whether to stabilize first or whether it is safe to continue
  investigating in production.

### Important rule

- If the incident affects production, prioritize safe service restoration.
- A complete RCA can come later, but document evidence now.

## 6. Preventive maintenance

### Includes

- Periodic review of utilization and errors.
- Cleanup of obsolete configurations.
- Validation of actual segmentation and reachability.
- Review of certificates, keys, credentials, and access policies.
- Verification of configuration backups and current documentation.

### Signs of technical debt

- Forgotten manual routes.
- VLANs with no clear owner.
- Firewall rules nobody can justify.
- Fragmented addressing without aggregation.
- Tunnels or certificates nearing expiration.
- APs or links with unbalanced load.

## 7. Continuity and disaster recovery

### What must exist

- Alternative topologies or paths when the business requires them.
- Backups of configuration and critical parameters.
- Clear procedure for restoring minimum reachability and essential services.
- Prioritization of which services must return first.

### Designing for resilience

- Physical redundancy without undesired active loops.
- Routing that reconverges acceptably.
- Segmentation that limits the blast radius.
- Alternative VPNs/tunnels if primary connectivity fails.
- DNS and content distribution prepared for regional loss when the case
  warrants it.

### DR testing

- Simulate loss of a link, device, site, or provider.
- Verify not only that "a route exists" but that the application remains
  usable.
- Measure detection time, reconvergence, and service recovery.

## 8. Evolution and migrations

### Typical migration cases derived from the authority corpus

- More access capacity: copper → cable/fiber/improved cellular.
- Stricter segmentation: flat LAN → VLANs + routing.
- Internal scaling: simple routing → OSPF with areas.
- Greater interdomain complexity: single egress → multiple BGP/peering
  policies.
- Reinforced security: cleartext or weak perimeter → TLS/IPsec/VPN/802.1X.
- Transport and performance modernization: baseline TCP → CUBIC/QUIC/BBR
  as appropriate.
- Addressing evolution: pure IPv4 → coexistence and IPv6 plan.

### Rules for migrating well

- Maintain temporary coexistence when the risk justifies it.
- Define a clear rollback point.
- Do not take for granted that the new technology improves every KPI at
  once.
- Retrain observability and troubleshooting for the new dominant layer.

## 9. Minimum governance recommended for the skill

Every operational response from the agent should produce, even in compact
form:

- Assumptions.
- Affected artifacts.
- Risk of the change or of inaction.
- Validation plan.
- Metric that will confirm success.
- Rollback or mitigation plan.

## Quick pre-change checklist

- Which layer(s) does it touch?
- Which users/sites does it affect?
- What is the estimated blast radius?
- What evidence do I have of the baseline state?
- How do I verify success at 5, 15, and 60 minutes?
- What would make me abort?

## Quick post-change checklist

- Are the signal and link still healthy?
- Has the expected reachability returned or improved?
- Is the critical application usable?
- Are the security policies still correct?
- Are the metrics within normal range?
- Is the documentation updated?

## Anti-patterns and common mistakes

- Operating without a baseline.
- Confusing nominal capacity with usable capacity on shared access.
- Declaring a change successful without testing the application/QoE.
- Not preparing rollback.
- Not reviewing cross-dependencies among routing, security, and naming.
- Deferring technical debt "because it works today."

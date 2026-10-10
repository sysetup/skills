# Troubleshooting playbooks

## Table of contents

- Scope
- Base method
- Golden rule
- Quick symptom classification
- Playbook 1 – Physical layer
- Playbook 2 – Data link layer
- Playbook 3 – MAC sublayer and L2 switching
- Playbook 4 – Network layer
- Playbook 5 – Transport
- Playbook 6 – DNS and naming
- Playbook 7 – Web and HTTPS
- Playbook 8 – Email
- Playbook 9 – VPN / IPsec / TLS / security
- Playbook 10 – Capacity, congestion, and QoE
- Cross-cutting heuristics
- Anti-patterns and common mistakes

## Scope

Use this file when the user reports a failure, degradation, intermittency, or
ambiguous symptom and a systematic per-layer diagnosis must be built.

## Authority status

This file is an operational synthesis.

- Use it after checking the relevant canonical references for the affected
  layers.
- If a playbook shortcut conflicts with a canonical layer concept, the
  canonical reference wins.
- Trace the final diagnosis back to the authoritative layer file(s) whenever
  possible.

## Base method

Always follow this sequence:

1. Define the symptom precisely.
2. Fix the scope: one host, one VLAN, one site, one region, everyone.
3. Map the symptom to the most probable layer.
4. Collect minimum evidence before touching configuration.
5. Confirm or rule out hypotheses bottom-up.
6. Only then propose a correction or change.

## Golden rule

Do not jump to the application if you do not yet know whether signal, link,
IP reachability, and transport session exist. Nor should you remain at the
physical layer if the symptom is clearly DNS/HTTP/email semantic.

## Quick symptom classification

| Symptom | Initial probable layer | First evidence |
|---|---|---|
| Link down / no carrier | Physical | interface state, medium, power, errors |
| High FCS/CRC | Link/Physical | frame counters, medium, speed/duplex |
| Broadcast storm / MAC flapping | MAC/L2 | STP, MAC table, loops |
| No IP obtained / cannot reach gateway | L2/L3 | VLAN, ARP/ND, mask, gateway |
| Partial reachability or unstable routes | L3 | routing tables, convergence, MTU |
| Connects but slow | L4/L3 | RTT, losses, window, congestion |
| Name does not resolve | L7/DNS | queries/responses, resolver, TTL |
| HTTPS fails with name resolved | L7/TLS/L4 | handshake, certificate, port |
| Streaming buffers | L7 + L4/L3 | throughput, jitter, CDN, server |
| VPN does not come up | Security/L3/L4 | SA, authentication, reachability, clock |

## Playbook 1 – Physical layer

### Typical symptoms

- Interface down/down or up/down.
- Total loss of signal.
- Abnormal error rate, carrier flapping.
- Throughput far below what is possible even without apparent load.

### Initial questions

- What is the medium: fiber, copper, coaxial, radio, cellular, satellite?
- Is the problem permanent or intermittent?
- Does it affect a single span or multiple users on the same access?

### Minimum evidence

- Administrative and operational state.
- Physical error counters.
- SNR/power if radio or optical.
- Distance, obstacles, weather, or recent changes.
- Speed/duplex/negotiation if applicable.

### Decision

- If no carrier → medium, optics, cabling, radio, or interface.
- If carrier exists but many errors → medium quality, interference,
  modulation.
- If it fails only under load → physical capacity or access sharing.

### Typical corrections

- Check cabling/transceivers.
- Adjust channel, power, or placement for radio.
- Correct physical negotiation.
- Change the medium if the requirement exceeds what is physically viable.

## Playbook 2 – Data link layer

### Typical symptoms

- FCS/CRC errors.
- Dropped frames.
- PPP framing errors.
- Erratic throughput on point-to-point links.

### Minimum evidence

- Good/bad frame counters.
- Expected vs. observed encapsulation.
- Local frame size and MTU.
- Window/ACKs if the link uses richer control.

### Decision

- High CRC/FCS → start with medium and framing, not IP.
- Hop-by-hop retransmissions or timeouts → check link RTT and window size
  if the protocol uses one.
- PPP or similar not coming up → verify LCP/NCP and encapsulation
  consistency.

### Frequent errors

- Blaming routing for a pure framing problem.
- Ignoring byte stuffing/encapsulation mismatch.
- Using too small a window on links with high RTT.

## Playbook 3 – MAC sublayer and L2 switching

### Typical symptoms

- MAC flapping.
- Abnormal broadcast/multicast.
- Broadcast storm.
- Hosts that "sometimes" see each other and sometimes do not.
- Unexpected VLAN reachability.
- WiFi associated but no useful traffic.

### Minimum evidence

- MAC table and entry stability.
- STP or equivalent loop-avoidance state.
- VLAN per port and permitted VLANs on trunks.
- For WiFi: association, authentication, RSSI/SNR, retries, channel.

### L2 decision tree

1. Is there a loop?
   - symptoms: high broadcast, high CPU, MAC flapping, generalized loss.
   - action: check STP, redundant links, and active logical topology.
2. Is there a VLAN mismatch?
   - symptoms: local host is up, gateway unreachable, selective
     reachability.
   - action: compare access VLAN and trunk VLAN list.
3. Is it a WiFi problem?
   - discovers SSID yes / associates no → authentication/security.
   - associates yes / no data → contention, keys, DHCP/ARP, ACLs.
4. Is it cable access via DOCSIS?
   - downstream OK / upstream bad → check sharing, ranging, load.

### Typical corrections

- Eliminate the loop or restore correct STP.
- Correct trunk/access tagging.
- Relocate AP / change channel / adjust security.
- Separate guests/IoT/users into distinct VLANs.

## Playbook 4 – Network layer

### Typical symptoms

- No reachability to gateway or remote networks.
- Route asymmetry.
- Slow convergence or flaps.
- MTU black holes / problematic fragmentation.
- Internal reachability fine, external reachability broken.

### Minimum evidence

- Host IP, mask, gateway.
- ARP/ND or next-hop resolution.
- Routing table and chosen route.
- Routing neighbor/adjacency state.
- Available ICMP/control protocols.
- Effective path MTU.

### L3 decision tree

1. Can the host reach its gateway?
   - no → go back to L2/VLAN/ARP/ND.
2. Does a route to the destination exist?
   - no → addressing, summaries, or routing protocol.
3. Does the route exist but traffic dies?
   - check next hop, ACL, MTU, BGP/peering policy.
4. Does the route oscillate?
   - check OSPF/BGP convergence, costs, flap, unstable links.
5. Do only external destinations fail?
   - check default route, NAT/policy if present, provider egress, BGP
     advertisements, or edge filters.

### Typical corrections

- Correct prefix/mask/gateway.
- Repair OSPF/BGP neighbors or faulty summarization.
- Adjust MTU or avoid problematic fragmentation.
- Correct route export/import policy at the edge.

## Playbook 5 – Transport

### Typical symptoms

- SYN with no response.
- Sessions that establish and drop.
- Low throughput with an apparently healthy link.
- Heavy retransmissions.
- Problems only on wireless or high-RTT paths.

### Minimum evidence

- Handshake capture.
- Observed RTT.
- Retransmissions and dup ACKs.
- Advertised window and, if inferable, congestion pressure.
- Process/port state.

### L4 decision tree

1. SYN goes out but no SYN/ACK returns → reachability, ACL/firewall, or
   service not listening.
2. SYN/ACK returns but session does not progress → middlebox, application,
   partial handshake.
3. Stable session but slow → cwnd/window/RTT/loss/host saturation.
4. Wireless path → do not attribute all loss to congestion.
5. High BDP → check whether the window is large enough to fill the path.

### Typical corrections

- Open the necessary reachability or start the correct service.
- Adjust the congestion control algorithm appropriate to the path.
- Optimize the host/process if the network is not the real bottleneck.

## Playbook 6 – DNS and naming

### Typical symptoms

- "Site won't open" but by IP it works.
- Different responses depending on user or region.
- Intermittency after changes.

### Minimum evidence

- Which resolver the client uses.
- Complete response (type, TTL, authority).
- Comparison between local resolver and authoritative.
- Timing of the recent change.

### DNS decision tree

1. Does the name resolve?
   - no → delegation, authority, resolver, reachability to the resolver.
2. Does it resolve to an unexpected IP?
   - may be CDN/anycast or stale cache; check TTL and context.
3. Do only some users fail?
   - different resolvers, cache, split-horizon, or geoselection.
4. Does behavior change with DoH/privacy?
   - consider resolver differences and observability.

### Typical corrections

- Correct zone/record/TTL.
- Flush or wait for cache expiration when appropriate.
- Align the expected resolver with the service's policy.

## Playbook 7 – Web and HTTPS

### Typical symptoms

- DNS fine, TCP fine, but the page does not load or returns an error.
- HTTP slow with partial objects.
- HTTPS fails with certificate alert or handshake failure.

### Minimum evidence

- HTTP status code.
- TCP/TLS sequence.
- Requested name and presented certificate.
- Specific failing object/origin.

### Decision

- If only HTTPS fails → certificate, name, trust chain, handshake.
- If only third-party objects fail → CDN or external dependency.
- If TTFB is high but transfer is then good → backend/origin rather than
  pure network.

## Playbook 8 – Email

### Typical symptoms

- Does not send.
- Sends but does not arrive.
- Arrives late.
- Arrives at the server but does not appear to the user.

### Analysis path

- Submission → transfer → final delivery → user agent visibility.
- Check full headers and queue state if inter-server transfer is involved.
- If the mail exists but is not visible, examine synchronization/client/
  mailbox before SMTP.

## Playbook 9 – VPN / IPsec / TLS / security

### Typical symptoms

- Tunnel does not come up.
- SA established but no useful traffic.
- TLS handshake failure.
- Enterprise WiFi access fails at authentication.

### Minimum evidence

- Peer reachability.
- Authentication/key/certificate parameters.
- SA or handshake state.
- Clock/time if temporal validity is implied.
- Firewall policy along the path.

### Security decision tree

1. Is there reachability to the peer/service?
2. Does authentication complete?
3. Are the keys/certificates valid and matching the name/identity?
4. Does encryption negotiate but useful traffic is then blocked?
5. Does segmentation permit the expected internal flow once the tunnel is
   up?

### Typical corrections

- Correct identity, certificates, or shared secrets.
- Adjust firewall/ACL policy for encapsulated and useful traffic.
- Review internal segmentation design after the tunnel.

## Playbook 10 – Capacity, congestion, and QoE

### Typical symptoms

- "The network is slow" without a total outage.
- Streaming buffers.
- Voice/video with high jitter.
- Only during peak hours or only on one access link.

### Minimum evidence

- Throughput, delay, jitter, loss.
- Queues or signs of congestion.
- Access type: shared vs. dedicated.
- Application: bulk, real-time, Web, CDN, interactive.

### Decision

- If the access is shared, do not assume a dedicated rate.
- If the application is real-time, jitter matters more than maximum
  throughput.
- If the problem occurs only at certain hours, think
  contention/congestion.
- If QoS exists, review actual classification and scheduling.

## Cross-cutting heuristics

- A problem affecting many protocols at once is usually low in the stack.
- A problem affecting a single name/service is usually high in the stack.
- Intermittency after changes usually points to the control plane, caches,
  or timers.
- Regional symptoms usually involve CDN, peering, or different resolvers.

## Anti-patterns and common mistakes

- Changing configuration before capturing minimum evidence.
- Diagnosing only from a favorite layer.
- Blaming the ISP without validating the local WLAN/LAN.
- Confusing reachability with a usable service.
- Declaring "secure" because the tunnel is up, without testing useful
  traffic.
- Measuring streaming/voice success only by nominal speed.

# 04 – MAC sublayer

## Scope

Use this file when the problem involves shared-medium access, contention,
Ethernet, WiFi, Bluetooth, L2 switching, STP, or VLANs.

## Mental model

The MAC sublayer decides **who transmits, when they transmit, and how to
prevent the shared medium from collapsing**. It also explains why modern L2
switching reduced collisions but did not eliminate the need to control loops
and broadcast domains.

## 4.1 The channel allocation problem

### 4.1.1 Static channel allocation

- Divides the resource in a fixed manner by time/frequency/capacity.
- Good when demand is predictable and continuous.
- Bad for bursty traffic because it wastes slots when the sender has no data.

### 4.1.2 Assumptions for dynamic channel allocation

- Independent users, sporadic activity, possible collisions, and the need to
  decide locally or with a coordinator.
- The central question is the trade-off among simplicity, fairness,
  throughput, and delay.

## 4.2 Multiple access protocols

### Operational taxonomy

- **Aloha**: transmit and recover from collisions.
- **CSMA**: listen before transmitting.
- **Collision-free**: reserve/order explicitly.
- **Limited-contention**: hybrids that scale better with a variable
  population.
- **Wireless-specific**: designed for media where listening alone is
  insufficient.

### 4.2.1 ALOHA

#### Pure ALOHA

- The node transmits whenever it has data.
- If a collision occurs, it waits a random time and retries.
- Larger vulnerable period because time is continuous.
- Classic theoretical maximum throughput: `1/(2e)`.

#### Slotted ALOHA

- Restricts transmissions to synchronized slots.
- Reduces the vulnerable period and improves efficiency.
- Classic theoretical maximum throughput: `1/e`.
- Important lesson: a small amount of temporal coordination yields a large
  improvement.

### 4.2.2 Carrier Sense Multiple Access

- Idea: listen to the medium before transmitting.
- Typical variants in the chapter: persistent, non-persistent, and
  p-persistent.
- Collisions can still occur due to propagation delay.
- In classic cable, it is combined with collision detection; in wireless,
  this does not work the same way.

### 4.2.3 Collision-free protocols

- Avoid collisions by assigning explicit turns or priorities.
- Improve efficiency when load is high and stable.
- Introduce more coordination and sometimes worse latency under low load.

### 4.2.4 Limited-contention protocols

- Aim to behave like light contention under low load and like reservation
  under high load.
- Useful when the number of active stations varies widely.

### 4.2.5 Wireless LAN protocols

- Distinctive problems:
  - hidden terminals,
  - exposed terminals,
  - practical impossibility of detecting collision as in classic Ethernet.
- Base solution: avoid collisions rather than detect them; hence CSMA/CA
  dominates.
- RTS/CTS helps when the cost of hidden-terminal collision is high.

## 4.3 Ethernet

### 4.3.1 Classic Ethernet physical layer

- Originally used a shared medium/bus.
- Stations competed for the same channel.
- Propagation and minimum frame size were key to collision detection.

### 4.3.2 Classic Ethernet MAC protocol

- CSMA/CD: listen, transmit, detect collision, abort, and perform backoff.
- Binary exponential backoff adjusts the wait after successive collisions.
- Worked well in bounded local environments but does not scale elegantly to
  high speeds or highly extended media.

### 4.3.3 Ethernet performance

- Under low load, distributed access works very well.
- Under high load, collisions and backoff increase; efficiency depends on
  relative propagation and frame size.
- Correct diagnosis: a "slow" classic Ethernet does not always require more
  bandwidth; sometimes it requires less contention or switching.

### 4.3.4 Switched Ethernet

- Changes the paradigm: point-to-point links between host and switch.
- Collisions disappear in properly configured full-duplex.
- The bottleneck shifts to uplinks, buffers, queues, and broadcast domains.
- This is the real basis of most modern LANs.

### 4.3.5–4.3.8 Speed evolution

- Fast Ethernet.
- Gigabit Ethernet.
- 10-Gigabit Ethernet.
- 40/100-Gigabit Ethernet.
- The chapter's evolutionary line shows that Ethernet maintained frame
  compatibility and operational model while increasing speed and changing
  media.

### 4.3.9 Retrospective on Ethernet

- Won through simplicity, economy, interoperability, and incremental
  evolution.
- Design lesson: a sufficient and adaptable protocol can beat more "elegant"
  but less deployable options.

## 4.4 Wireless LANs (802.11)

### 4.4.1 802.11 architecture and stack

- Key elements:
  - station,
  - access point,
  - basic service set,
  - distribution system.
- An AP connects the wireless domain to the wired network.
- In mesh mode, forwarding can be distributed among nodes, but the chapter
  uses the AP as the most common central reference.

### 4.4.2 Physical layer

- 802.11 evolves in bands, modulation, coding, and MIMO to increase rate.
- Nominal speed does not equal usable throughput: MAC overhead,
  interference, and radio conditions matter significantly.

### 4.4.3 MAC protocol

- Base: DCF with CSMA/CA.
- Uses interframe spaces and random backoff to arbitrate the medium.
- MAC-layer ACKs compensate for the higher risk of radio loss.
- RTS/CTS is optional and useful in hidden-terminal scenarios.
- NAV helps coordinate virtual medium reservation.

### 4.4.4 Frame structure

- Richer than Ethernet because it must carry radio control, multiple
  addresses, management/control/data types, and BSS context.
- If a WiFi capture "looks more complex," that is normal: the medium demands
  more state.

### 4.4.5 Services

- Association/disassociation.
- Authentication.
- Distribution/integration.
- Power management.
- QoS in later extensions.
- Typical diagnosis: if the host "sees" the network but passes no traffic,
  first check which service failed: discovery, association, authentication,
  or data transfer.

### 802.11 security from the MAC perspective

- WEP: historically broken; do not use as a serious design.
- WPA/WPA2: stronger authentication and encryption; the chapter emphasizes
  the improvement, but also that practical security depends heavily on key
  management.
- 802.1X/EAP: useful in enterprise for centralized authentication and
  fine-grained control.
- Common mistake: treating WiFi as "Ethernet without cables"; the security
  and medium access mechanisms are different.

## 4.5 Bluetooth

### 4.5.1 Architecture

- Designed for PAN and short range.
- Master/slave model in the classic versions covered in the chapter.
- Optimal for peripherals and personal links, not for replacing an entire
  LAN.

### 4.5.2 Applications

- Audio, peripherals, synchronization, and proximity.
- If the priority is low power and short range, Bluetooth competes better
  than WiFi.

### 4.5.3–4.5.7 Stack, radio, link layers, frames, Bluetooth 5

- The stack is specific to the personal-use case.
- Frequency hopping and link profile are central to coexistence and power
  consumption.
- Bluetooth 5 improves range/capacity relative to previous generations
  within the same ecosystem, without changing its basic PAN/nearby-IoT
  niche.

## 4.6 DOCSIS MAC

### 4.6.1 Overview

- In cable, the MAC must arbitrate a shared upstream among many subscribers.
- The downstream is much simpler because there is a single dominant
  transmitter.

### 4.6.2 Ranging

- Adjusts subscriber synchronization and power so that the shared medium is
  usable by all.
- If very strange upstream problems appear, consider ranging and
  calibration.

### 4.6.3 Channel bandwidth allocation

- Efficiency depends on how the CMTS distributes transmission opportunities.
- This is not a point-to-point Ethernet; it is shared access with explicit
  scheduling.

## 4.7 Data link layer switching

### 4.7.1 Uses of bridges

- Separate collision domains and allow extending/connecting LANs.
- Maintain forwarding based on MAC addresses, not IP.

### 4.7.2 Learning bridges

- The bridge learns which addresses lie behind which port by observing the
  source of frames.
- If the destination is unknown, it floods.
- Advantage: self-configuration.
- Risk: excessive flooding if there is mobility/loops/unstable table.

### 4.7.3 Spanning-tree bridges

- L2 loops are lethal because broadcast/unknown frames can circulate without
  a TTL.
- STP eliminates logical loops by deactivating certain redundant links.
- Operational principle: physical redundancy is possible, but only a single
  cycle-free active topology at a time.
- If an L2 cycle exists and STP does not converge or is misconfigured,
  expect broadcast storms and widespread erratic behavior.

### 4.7.4 Repeaters, hubs, bridges, switches, routers, gateways

- **Repeater/Hub**: amplifies/repeats with no forwarding intelligence.
- **Bridge/Switch**: forwards by MAC at Layer 2.
- **Router**: forwards by Layer 3 information.
- **Gateway**: translates between more disparate networks/technologies.
- Common mistake: asking an L2 switch to solve a policy-routing problem or
  asking a router to cure a pure bridging loop without touching L2.

### 4.7.5 VLANs

- Divide a physical LAN into multiple logical LANs.
- Reduce broadcast scope and align the network with organizational/security
  boundaries.
- Access ports belong to one VLAN; trunk links carry multiple VLANs.
- Risks: VLAN mismatch, misconfigured trunk, incorrect assumptions about who
  can reach whom.

## When to use what

- **Switched Ethernet** for general wired LAN.
- **WiFi** for mobility and flexible deployment.
- **Bluetooth** for PAN and short-range peripherals.
- **VLANs** for logical segmentation without rewiring.
- **STP** when L2 redundancy exists.
- **RTS/CTS** when hidden terminals harm WiFi.
- **DOCSIS awareness** when the problem lies in cable access, not the LAN.

## MAC/L2 troubleshooting checklist

- Are there actual collisions, or is the environment already full-duplex
  switched?
- Do L2 loops or a broadcast storm exist?
- Does the host's VLAN match the expected gateway?
- Does the trunk carry the correct VLAN?
- Does WiFi fail at discovery, association, authentication, or data
  transfer?
- Is the nominal radio rate very different from usable throughput? Check
  contention and SNR.
- Is the cable upstream shared/saturated?

## Anti-patterns and common mistakes

- Treating a WiFi network as if it were pure Ethernet.
- Leaving L2 redundancy without STP or an equivalent.
- Creating too many VLANs without a clear administrative purpose.
- Confusing collision domain with broadcast domain.
- Blaming the router when the problem is a Layer 2 broadcast storm.
- Measuring WiFi success only by RSSI or PHY rate.
- Ignoring ranging and scheduling in DOCSIS when diagnosing cable access.

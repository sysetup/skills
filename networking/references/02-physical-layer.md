# 02 – Physical layer

## Table of contents

- Scope
- Mental model
- 2.1 Guided media
- 2.2 Wireless transmission
- 2.3 Using the spectrum for transmission
- 2.4 From waveforms to bits
- 2.5 The public switched telephone network
- 2.6 Cellular networks
- 2.7 Cable networks
- 2.8 Communication satellites
- 2.9 Access network comparison
- 2.10 Physical-layer policy
- Physical design checklist
- Quick decision tree
- Anti-patterns and common mistakes

## Scope

Use this file when the problem depends on the transmission medium, radio
access, channel capacity limits, spectrum, or the choice among copper, fiber,
coaxial, cable, cellular, and satellite.

## Mental model

The physical layer converts bits into signals and signals into bits. The
decisions made here are:

- which medium carries the energy or light,
- which portion of the spectrum is used,
- which modulation encodes the information,
- how multiple streams share the resource,
- and what limits physics imposes on throughput, range, and error rate.

## 2.1 Guided media

### 2.1.1 Persistent storage

- Conceptual reminder from the chapter: moving bits does not always mean
  transmitting "online"; it can also mean physically transporting storage.
- Useful as a cost/latency/extreme-capacity comparison, not as an interactive
  network.

### 2.1.2 Twisted pairs

- Classic medium for telephone access and a large portion of copper cabling.
- Advantages: inexpensive, widespread, easy to install.
- Limitations: attenuation, interference, crosstalk, distance, and rate
  constraints.
- Suitable for local access, short spans, and reuse of existing
  infrastructure.

### 2.1.3 Coaxial cable

- Better shielding and bandwidth than twisted pair.
- Traditional physical basis for cable/HFC networks.
- Useful where high-capacity shared distribution already exists for fixed
  access.

### 2.1.4 Power lines

- Reuses electrical wiring to carry data.
- Convenient when running new cable is impractical.
- More sensitive to noise and to conditions not originally designed for data.

### 2.1.5 Fiber optics

- Dominant medium when high capacity, noise immunity, and long distances are
  required.
- Advantages: very high bandwidth, low loss, electromagnetic isolation.
- Termination cost and complexity higher than copper/coaxial, but excels in
  backbone, campus, metro, and FTTH access.
- If the primary requirement is future capacity and distance, fiber is the
  benchmark against which all other media are compared.

## Quick guided-media comparison

| Medium | Primary strength | Primary weakness | Typical use |
|---|---|---|---|
| Twisted pair | Low cost and ubiquitous deployment | Noise/distance | local access, existing copper |
| Coaxial | Good shared bandwidth | shared medium and legacy tree | cable/HFC |
| Power line | no rewiring needed | unpredictable noise | home/light office |
| Fiber | capacity and reach | cost/optics/termination | backbone, metro, FTTH |

## 2.2 Wireless transmission

### 2.2.1 Electromagnetic spectrum

- All wireless communication competes for a portion of the spectrum.
- Frequency, wavelength, propagation, penetration, and bandwidth are
  intimately related.
- Lower bands: better coverage/penetration, less aggregate bandwidth.
- Higher bands: more potential capacity, worse propagation, and greater
  directionality.

### 2.2.2 Frequency hopping spread spectrum

- Hops among frequencies according to a shared sequence.
- Reduces susceptibility to narrowband interference and can improve
  robustness.
- Useful when the radio environment is noisy and the system tolerates prior
  coordination.

### 2.2.3 Direct sequence spread spectrum

- Spreads the signal with a chip sequence.
- Distributes energy over a wider band; improves resistance to
  noise/interference.
- An important conceptual foundation for shared wireless systems.

### 2.2.4 Ultra-wideband

- Uses very wide signals at low spectral power density.
- Suitable for short range and certain localization/robustness profiles.

## 2.3 Using the spectrum for transmission

### 2.3.1 Radio

- Good general coverage and reasonable obstacle penetration.
- Shared medium; access coordination is as important as the signal itself.
- Widely used in WiFi, broadcasting, and part of mobile access.

### 2.3.2 Microwave

- More directional, suitable for point-to-point links and backhaul.
- Requires more careful geometric conditions than low-band radio.
- Good when capacity is needed without laying fiber, along controlled paths.

### 2.3.3 Infrared

- Short range and poor obstacle penetration.
- Spatially isolated, useful where natural signal containment is desired.

### 2.3.4 Light transmission

- Free-space or guided optical communication.
- High capacity, but sensitive to alignment, obstacles, and environmental
  conditions when not traveling through fiber.

## 2.4 From waveforms to bits

### 2.4.1 Theoretical basis of data communication

- The goal is not "sending voltages" but distinguishing states well enough to
  recover bits at an acceptable error rate.
- The higher the symbol rate and the greater the number of levels, the
  greater the demands on noise, synchronization, and linearity.

### 2.4.2 Maximum data rate of a channel

- **Nyquist (ideal noiseless channel):**
  - `Rmax = 2B log2(V)` bits/s
  - `B` = bandwidth in Hz.
  - `V` = discrete signal levels.
- **Shannon (noisy channel):**
  - `C = B log2(1 + S/N)` bits/s
  - `S/N` = signal-to-noise ratio in linear scale.
- Operational consequence:
  - increasing symbols per second without considering B does not work,
  - increasing levels without considering SNR does not work either,
  - and every serious physical recommendation must mention bandwidth and
    noise.

### 2.4.3 Digital modulation

- The transmitter maps bits to measurable changes of a carrier.
- Common schemes covered in the chapter: amplitude, frequency, phase, and
  combined schemes with higher spectral efficiency.
- Practical rule:
  - simpler modulation = greater robustness and lower efficiency,
  - denser modulation = more bits/symbol and higher SNR requirement.
- If a link degrades with weather/interference/distance, lowering modulation
  efficiency can sustain availability where a dense modulation fails.

### 2.4.4 Multiplexing

- **FDM**: separates streams by frequency.
- **TDM**: separates by time.
- **WDM**: optical equivalent using wavelengths.
- Multiplexing allows sharing physical infrastructure without mixing streams.
- Correct design question: is the resource better shared by frequency, by
  time, or by multiple optical channels?

## 2.5 The public switched telephone network

### 2.5.1 Telephone system structure

- Historically hierarchical, with local loops, trunks, and switching.
- Relevant because much fixed Internet access reuses this infrastructure.

### 2.5.2 Local loop: telephone modems, ADSL, and fiber

- The local loop is the segment that most constrains subscriber access.
- Modems exploit a channel designed for voice; ADSL separates upstream and
  downstream asymmetrically because the typical usage pattern justifies it.
- Fiber displaces those limitations by offering far greater physical margin.
- If the user requires strong upstream and sustained low latency, ADSL
  typically loses to fiber and other modern access options.

### 2.5.3 Trunks and multiplexing

- Trunks aggregate a large number of circuits/flows between exchanges.
- Multiplexing is the central economic mechanism of the infrastructure.

### 2.5.4 Switching

- Evolution from circuit switching toward increasingly digital models.
- Key to understanding why legacy access can coexist with modern packetized
  transport.

## 2.6 Cellular networks

### Common concepts

- **Cells**: spatial partitioning for spectrum reuse.
- **Handoff**: transfer between cells as the user moves.
- **Paging**: efficient mobile location without maintaining full activity.
- If mobility, coverage, backhaul, and spectrum are involved, the problem is
  no longer "just IP."

### 1G

- Analog voice.
- Low efficiency, lacking the flexibility of digital data.

### 2G and GSM

- Digital voice, greater efficiency, and the foundations of modern mobility.
- GSM consolidated a global reference architecture.
- Also paved the way for limited data services and richer signaling.

### 3G

- Digital voice and data with better support for mobile Internet services.
- The core and radio interface are now far more data-oriented.

### 4G

- Packet switching as the system's foundation.
- Voice and data converge toward a fully digital network.
- Much better aligned with the end-to-end Internet model.

### 5G

- Cell densification for greater spectrum reuse.
- Use of higher bands, including millimeter wave.
- Massive MIMO and beamforming for spectral efficiency.
- Network slicing over shared infrastructure.
- Relationship with later chapters: SDN and virtualization help operate this.

## 2.7 Cable networks

### 2.7.1 History and CATV

- Originated to distribute TV from a headend to many homes.
- Originally a distribution topology, later adapted for bidirectional
  Internet.

### 2.7.2 HFC (Hybrid Fiber-Coaxial)

- Fiber for aggregated spans + coaxial to the subscriber.
- Good compromise between reuse and capacity.
- Shared medium: performance depends on how many users contend on the node,
  not just the contracted nominal speed.

### 2.7.3 DOCSIS

- Standardizes data access over cable.
- Organizes upstream/downstream channels and shares segment resources.
- Highly relevant for last-mile troubleshooting in fixed access.

### 2.7.4 Nodes and minislots

- Upstream sharing uses temporal allocation mechanisms.
- Classic symptom: good downstream with erratic upstream when the segment is
  heavily loaded or poorly calibrated.

## 2.8 Communication satellites

### GEO

- Wide coverage and stable architecture.
- Main issue: high latency due to orbital distance.
- Good for coverage where no terrestrial infrastructure exists.

### MEO

- Compromise between coverage and latency.

### LEO

- Lower latency than GEO and extensive constellations.
- Require more satellites and dynamic coverage/route management.

## 2.9 Access network comparison

### Cable vs. fiber vs. ADSL

- **Fiber**: best capacity margin and symmetry.
- **Cable/HFC**: high throughput, but shared.
- **ADSL**: useful where copper already exists, but more limited and
  asymmetric.

### Satellite vs. terrestrial

- Satellite wins in reach and remote deployment.
- Terrestrial usually wins in latency, stability, and per-user capacity
  control.
- If the application is interactive, satellite latency must be discussed
  early.

## "When to use what" guide

- **Fiber**: campus/backbone/FTTH/growing loads and long planning horizon.
- **Twisted pair**: existing local access and tight budget.
- **Coaxial/HFC**: mass fixed access where infrastructure already exists.
- **Microwave**: point-to-point backhaul when laying fiber is difficult.
- **Cellular 4G/5G**: mobility or rapid deployment with spectrum dependency.
- **Satellite**: difficult geography or total absence of terrestrial network.

## 2.10 Physical-layer policy

- Spectrum allocation conditions every wireless design.
- Cellular networks depend on licensing, planning, and regulation.
- Legacy telephony shows how regulatory decisions shape the infrastructure
  available for subsequent services.
- When comparing physical options, always include the regulatory dimension if
  access depends on licensed spectrum or legacy public infrastructure.

## Physical design checklist

- Actual path distance.
- Noise/interference environment.
- Upstream and downstream requirements.
- Application sensitivity to latency/jitter.
- Dedicated or shared medium.
- Growth potential over 3–5 years.
- Regulatory dependence on spectrum.
- Installation/maintenance complexity.

## Quick decision tree

1. If the user needs mobility, think cellular or WLAN first.
2. If high capacity and predictability are needed, start with fiber.
3. If reusing residential infrastructure, compare HFC and DSL before
   redesigning.
4. If distance or geography is extreme, incorporate satellite into the
   analysis.
5. If the issue is theoretical capacity, use Nyquist/Shannon to explain
   limits.
6. If the issue is user coexistence, ask about medium sharing.

## Anti-patterns and common mistakes

- Choosing a medium solely by its marketing-nominal speed.
- Ignoring that HFC and radio are shared.
- Designing 5G or WiFi as if coverage and capacity were the same thing.
- Confusing licensed band, unlicensed band, and actual operational
  availability.
- Requesting "low latency" over GEO without acknowledging the physical cost
  of the orbit.
- Using dense modulation without sufficient SNR margin.
- Migrating to a new physical technology without examining backhaul and site
  power.

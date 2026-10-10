# 06 – Transport layer

## Table of contents

- Scope
- Mental model
- 6.1 Transport service
- 6.2 Transport protocol elements
- 6.3 Congestion control
- 6.4 UDP
- 6.5 TCP
- 6.6 QUIC and BBR
- 6.7 Performance
- Selection guide
- Troubleshooting checklist
- Anti-patterns

## Scope

Use this file when the problem involves ports, sockets, connections,
handshakes, session release, retransmissions, windows, congestion control,
TCP, UDP, QUIC, or end-to-end performance.

## Mental model

The transport layer converts the network's host-to-host connectivity into a
service usable by processes. The essentials are distinguishing:

- process vs. host,
- connection vs. datagram,
- reliability vs. latency,
- flow control vs. congestion control,
- protocol performance vs. application performance.

## 6.1 The transport service

### 6.1.1 Services provided to upper layers

- Multiplexes multiple processes over a single IP address.
- Can offer a reliable byte stream, unreliable messages, or variants in
  between depending on the protocol.
- The upper layer should not worry about each hop, only the end-to-end
  service its process needs.

### 6.1.2 Transport service primitives

- Conceptual primitives: `LISTEN`, `CONNECT`, `SEND`, `RECEIVE`, `CLOSE`.
- Useful for thinking about how an application consumes the service, even
  though the concrete API may differ.
- A good transport diagnosis starts by asking at which primitive the failure
  occurs.

### 6.1.3 Berkeley sockets

- The de facto interface for transport in real systems.
- Typical primitives from the chapter: `SOCKET`, `BIND`, `LISTEN`, `ACCEPT`,
  `CONNECT`, `SEND`, `RECEIVE`, `CLOSE`.
- The server creates an endpoint, binds an address, listens, and accepts.
- The client creates an endpoint and connects.
- Sockets abstract transport, not just TCP; the same API can map to
  connection-oriented or connectionless services.

### 6.1.4 Socket programming example

- The chapter's example is a reminder that "transport" is not just theory:
  bind errors, backlog, blocking, and call ordering affect availability.
- If an application "won't start," check the socket/bind/listen or
  socket/connect sequence before blaming the entire network.

## 6.2 Transport protocol elements

### 6.2.1 Addressing

- Transport identifies processes via ports or equivalent endpoints.
- The network delivers to the host; transport delivers to the correct
  process.
- Classic error: IP reachability is correct but the port is wrong or the
  process is not listening.

### 6.2.2 Connection establishment

- Establishment must cope with delays, late duplicates, and synchronization.
- Hence the need for a **three-way handshake** in designs like TCP.
- A proper handshake is not bureaucracy: it prevents phantom connections or
  inconsistent states from stale segments.

### 6.2.3 Connection release

- Release seems simpler than establishment, but it too must handle loss and
  duplication.
- The chapter relates it to the impossibility of absolute certainty in
  unreliable networks (echo of the two-armies problem).

### 6.2.4 Error control and flow control

- **Error control**: timers, ACKs, retransmission, sequences.
- **Flow control**: do not overwhelm the receiver; typically via the
  receiver's window.
- End-to-end reliability lives here even if the network below is fairly
  good.

### 6.2.5 Multiplexing

- Multiple connections/services share the host and IP.
- Can be upward or downward depending on how flows and links are combined.

### 6.2.6 Crash recovery

- An endpoint may restart and lose state.
- The protocol must avoid confusing segments from before and after the crash.
- When the user reports "zombie" sessions, think about state, timers, and
  recovery.

## 6.3 Congestion control

### 6.3.1 Desirable bandwidth allocation

- The goal is not merely high utilization; it also includes **fairness** and
  stability.
- Chiu and Jain show why **AIMD** converges to an efficient and fair
  allocation under binary congestion feedback.
- Practical insight: increase smoothly and reduce decisively when the
  network signals congestion.

### 6.3.2 Regulating the sending rate

- The sender regulates how much it injects by observing loss, delay, or ECN
  signals.
- The key variable is usually the congestion window or a rate equivalent.
- If a connection fills queues and punishes others, congestion control is the
  right tool, not the receiver's flow control.

### 6.3.3 Wireless issues

- Over radio, loss does not always mean congestion.
- If TCP interprets all loss as congestion, it may underutilize the link.
- This explains why wireless and mobile media require careful metric reading
  before adjusting the protocol.

## Critical distinction: flow control vs. congestion control

- **Flow control** protects the receiver.
- **Congestion control** protects the network and other flows.
- If the user conflates the two concepts, correct them before proposing a
  solution.

## 6.4 Internet transport protocols: UDP

### 6.4.1 Introduction to UDP

- Connectionless service, minimal overhead, no built-in reliability.
- Adds port-based multiplexing/demultiplexing over IP.
- Useful when the application tolerates loss/reordering or implements its own
  control.

### Cases where UDP fits well

- Simple request/response queries.
- Real-time traffic where late retransmissions are worthless.
- Protocols that prefer to manage their own recovery/pacing logic.

### 6.4.2 Remote Procedure Call

- The chapter shows how UDP can support RPC-style interaction.
- Operational reminder: "lightweight" does not mean trivial; timeouts,
  idempotency, and duplicates still matter.

### 6.4.3 Real-Time Transport Protocols

- RTP and its related family rely on datagram transport for media.
- Prioritize timing and sequencing over absolute reliability.
- If the application is real-time voice/video, the correct question is "does
  it arrive on time?" rather than "did every byte arrive?"

## 6.5 Internet transport protocols: TCP

### 6.5.1 Introduction to TCP

- The principal Internet transport protocol for a reliable byte stream.
- Full duplex, connection-oriented, and congestion-controlled.

### 6.5.2 TCP service model

- Offers a byte stream, not a message stream.
- Does not preserve application-level write() boundaries.
- Typical application mistake: expecting each `send` to correspond to one
  `receive`.

### 6.5.3 The TCP protocol

- Byte numbering.
- Cumulative ACKs.
- Retransmission based on timer/duplicates.
- Windows for reliability and pacing.

### 6.5.4 TCP segment header

- Key fields for troubleshooting:
  - ports,
  - sequence number,
  - acknowledgement number,
  - flags,
  - window,
  - checksum,
  - options.
- Reading TCP headers properly often explains failed handshakes, resets, zero
  windows, or MSS/option problems.

### 6.5.5 TCP connection establishment

- Three-way handshake.
- Synchronizes sequences and confirms both directions.
- If it fails, differentiate among:
  - reachability/ACL/firewall blocking,
  - closed port/reset,
  - intermediate loss,
  - application not listening.

### 6.5.6 TCP connection release

- Orderly close with a specific flag exchange.
- Do not assume that `FIN` and `ACK` instantaneously free resources.

### 6.5.7 Connection management modeling

- State modeling helps explain quirks of `SYN-SENT`, `ESTABLISHED`,
  `FIN-WAIT`, `TIME-WAIT`, etc.
- If an application "hangs" on close, examine the actual TCP state.

### 6.5.8 TCP sliding window

- Central mechanism for keeping multiple bytes/segments in flight.
- The effective window is limited by the minimum of the receiver's window and
  the congestion window.
- On high-BDP links, a window that is too small destroys throughput.

### 6.5.9 TCP timer management

- Poorly estimated timers cause spurious retransmissions or sluggishness.
- The chapter incorporates classic contributions for RTT estimation and
  prudent backoff.
- Karn/Jacobson appear as key ideas for avoiding naive RTT measurement.

### 6.5.10 TCP congestion control

- Slow start to ramp up.
- Congestion avoidance for more cautious growth.
- Reaction to loss/dup ACKs to reduce pressure on the network.
- Actual behavior is a conversation among cwnd, ssthresh, and path signals.

### 6.5.11 TCP CUBIC

- Modern variant oriented toward high-speed, high-RTT networks.
- Grows with a different function than Reno/NewReno and recovers capacity
  better on "long fat" paths.
- Matters when the user works with high-capacity links and classic TCP does
  not fill the pipe efficiently.

## 6.6 Modern transport protocols and congestion control

### 6.6.1 QUIC

- Runs over UDP but incorporates many modern transport functions.
- Reduces establishment cost and improves handling of multiple related
  streams within a single logical connection.
- Highly relevant for modern Web traffic and for avoiding certain
  limitations of the coupling between application and traditional TCP.

### 6.6.2 BBR

- Congestion control based on estimating bottleneck bandwidth and RTT, not
  solely on using loss as the primary signal.
- Aims to operate near the bandwidth-delay product without overfilling
  queues.
- If the symptom is bufferbloat or irregular performance on fast links, BBR
  is a concept that must enter the conversation.

### 6.6.3 The future of TCP

- The text emphasizes that TCP is still alive, but the environment has
  changed: fast networks, wireless, multiple streams, QoE-sensitive users.
- Evolution points toward better signals, improved setup, and lower perceived
  overhead.

## 6.7 Performance issues

### 6.7.1 Performance problems in computer networks

- Observed performance depends not only on the link but also on hosts,
  segmentation, timers, processing, and the application.

### 6.7.2 Network performance measurement

- Measuring well matters as much as optimizing.
- Ensure you distinguish capacity, actual throughput, goodput, and QoE.

### 6.7.3 Measuring access network throughput

- The access network may be the real bottleneck.
- Measurement must account for contention, traffic direction, proximity to
  the test server, and home/access conditions.

### 6.7.4 Measuring quality of experience

- A network may look good in throughput yet poor in QoE.
- The correct metric depends on the application: startup delay, buffering,
  interactivity, completion time, etc.

### 6.7.5 Host design for fast networks

- On fast networks, CPU, the stack, and interrupt handling matter
  significantly.
- Not every "network" bottleneck is in the network; sometimes it is in the
  host.

### 6.7.6 Fast segment processing

- Minimizing per-packet/segment cost is key at high rates.
- If the rate grows, a design that processes too many small packets suffers.

### 6.7.7 Header compression

- Useful when header overhead is high relative to payload.
- Especially important on certain links or small interactive flows.

### 6.7.8 Protocols for long fat networks

- LFNs demand large windows, prudent timers, and algorithms that fill the
  pipe without collapsing the network.
- Practical rule: if RTT and capacity are both high, check BDP before any
  other adjustment.

## "When to use what" guide

- **UDP**: low latency, loss tolerance, application-managed logic.
- **TCP**: general reliability, massive compatibility, byte stream.
- **TCP CUBIC**: high speed/high RTT with need for better scaling.
- **QUIC**: fast establishment, multiple streams, modern Web.
- **BBR**: when loss-based control does not behave well on the path.

## Quick decision tree

1. If the symptom is "cannot connect," check handshake and port/process.
2. If it connects but is slow, check window, RTT, losses, and congestion
   control.
3. If the app expects messages but uses TCP, check application-level framing.
4. If the traffic is real-time media, question whether TCP is appropriate.
5. If the path is wireless, do not attribute all loss to congestion.
6. If the path has high BDP, calculate the required window before touching
   the app.

## L4 troubleshooting checklist

- Is a process listening on the correct port?
- Does the SYN go out and does a SYN/ACK come back?
- Are there resets or timeouts?
- Is the advertised window or cwnd the bottleneck?
- Are retransmissions due to real loss or a poor RTO?
- Is a wireless path confusing the algorithm?
- Does the application require messages but is receiving a byte stream?
- Is the host processing fast enough for the required rate?

## Anti-patterns and common mistakes

- Using TCP for interactive media without justification.
- Blaming the network when the problem is the host or the sockets API.
- Confusing UDP with "no control at all."
- Confusing flow control with congestion control.
- Measuring only Mbps and declaring success without examining QoE.
- Ignoring BDP on fast/long links.
- Assuming that QUIC is "just UDP"; its transport semantics matter.

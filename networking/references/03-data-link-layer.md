# 03 – Data link layer

## Scope

Use this file when the problem involves encapsulation, framing, frame errors,
link efficiency, PPP, point-to-point links, or hop-by-hop reliability.

## Mental model

The data link layer takes a physical channel and converts it into a more
useful service for the network layer. Its central questions are:

- How do I delimit frames?
- How do I detect/correct errors?
- How do I avoid overwhelming the receiver?
- How do I maintain efficiency given real RTT and error rates?

## 3.1 Data link layer design issues

### 3.1.1 Services provided to the network layer

- **Unacknowledged connectionless service**: simple, inexpensive, useful when
  the medium is highly reliable or recovery will be handled above.
- **Acknowledged connectionless service**: each frame is individually
  acknowledged.
- **Acknowledged connection-oriented service**: greater state control,
  sequencing, and teardown.
- Practical rule: the worse the link or the more costly the error, the
  greater the value of explicit hop-by-hop control.

### 3.1.2 Framing

- The network needs to know where one frame ends and the next begins.
- Methods covered in the chapter:
  - character count,
  - flag bytes with byte stuffing,
  - flags with bit stuffing,
  - physical-layer encoding that preserves delimitation.
- If the payload can contain the delimiter pattern, stuffing or an equivalent
  mechanism is required.

### 3.1.3 Error control

- Objective: detect or correct alterations suffered by the frame.
- Two general strategies:
  - **FEC**: adds redundancy to correct without retransmission.
  - **Detection + retransmission**: detects and resends.
- The choice depends on RTT, the cost of retransmission, and the expected
  error rate.

### 3.1.4 Flow control

- Prevents the sender from overwhelming the receiver or intermediate link
  buffers.
- Primary tool: limiting how many frames can be "in flight."
- Do not confuse flow control with congestion control: the focus here is the
  neighbor, not the entire network.

## 3.2 Error detection and correction

### Underlying principle

- A code adds structured redundancy to separate valid messages in the
  codeword space.
- The distance between codewords determines detection/correction capability.

### Hamming distance

- The **Hamming distance** is the number of bits that differ between two
  codewords.
- With minimum distance `d`:
  - up to `d − 1` errors can be detected,
  - up to `floor((d − 1)/2)` errors can be corrected.
- This principle enables reasoning about any linear code in the chapter.

### 3.2.1 Error-correcting codes

- Useful when retransmission is costly or impossible.
- Favorable cases:
  - links with high RTT,
  - broadcast/satellite,
  - media with more correlated losses,
  - real-time traffic sensitive to retransmission.
- Error-correcting codes buy robustness at the cost of overhead.

#### Conceptual examples from the chapter

- Simple repetition: pedagogical, inefficient.
- Structured Hamming-type codes: show how to add check bits with
  deterministic rules to locate/correct limited errors.
- Reed-Solomon appears linked to practical technologies where the medium can
  introduce burst errors.

### 3.2.2 Error-detecting codes

- The chapter emphasizes three families:
  - parity,
  - checksums,
  - CRC.

#### Parity

- Very inexpensive.
- Detects any odd number of errors in a codeword.
- Insufficient for demanding modern links if used alone.

#### Checksums

- Sum words and verify arithmetic consistency.
- Simple and useful across several layers, but weaker than CRC for certain
  error patterns.

#### CRC

- Treated as the strong industrial mechanism for frame-level error detection.
- Models the frame as a binary polynomial and computes a remainder with
  respect to a generator polynomial.
- Advantages:
  - detects burst errors very well,
  - efficient in hardware/software,
  - widely used in LANs and PPP.
- Diagnostic rule: rising FCS/CRC errors usually point to media, framing, or
  physical interface problems, not application issues.

## 3.3 Elementary link protocols

### 3.3.1 Initial assumptions

- To understand the mechanisms, the chapter starts with simplified scenarios:
  simplex link, receiver always ready, no errors, etc.
- The utility is not realism but isolating one variable at a time.

### 3.3.2 Basic transmission and receipt

- First step: sender transmits and receiver receives, with no error or
  sophisticated control.
- Introduces the idea of send/receive primitives and buffers.

### 3.3.3 Simplex link-layer protocols

- Relaxing assumptions introduces ACKs, timers, and sequence numbers.
- **Stop-and-wait**: one frame outstanding at a time.
- Easy to implement and reason about, but inefficient when the
  bandwidth-delay product is large.

## 3.4 Improving efficiency

### Problem to solve

- If the link is fast and the RTT is non-trivial, stop-and-wait wastes much
  capacity waiting for ACKs.
- Solution: allow multiple frames in flight with a **sliding window**.

### 3.4.1 Goal: bidirectional transmission, multiple frames in flight

- The sender's window limits how many unacknowledged frames can be
  outstanding.
- The receiver's window defines which sequences it can accept.
- ACKs advance the window; timeouts force recovery.

### 3.4.2 Full-duplex sliding-window protocol examples

- **One-bit sliding window**: basic case demonstrating ACK/timeout/duplicate.
- **Go-back-N**:
  - the receiver maintains strict order,
  - upon loss/error, retransmission starts from the first missing frame.
- **Selective repeat**:
  - the receiver can accept out-of-order frames within the window,
  - only the lost frames are retransmitted.
- Practical rule:
  - Go-back-N = simpler,
  - Selective repeat = more efficient with non-trivial losses.

### Formulas and operational rules

- If `a = propagation_time / transmission_time`, stop-and-wait degrades
  sharply when `a` is large.
- A sufficiently large window must cover the bandwidth-delay product to keep
  the link busy.
- If the user reports very low throughput on a "fast" link, ask about RTT,
  window, and losses before blaming the physical capacity.

## 3.5 Data link protocols in practice

### PPP as a common pattern for point-to-point links

- The chapter presents it as the standard protocol for carrying packets over
  diverse point-to-point links.
- Main functions of PPP:
  1. unambiguous framing,
  2. error detection,
  3. link negotiation and management via LCP,
  4. multiprotocol support via NCPs.
- PPP inherits the HDLC aesthetic, but on the Internet it usually operates in
  unnumbered and unreliable mode, leaving other recovery to upper layers.

### PPP frame format

- Conceptual components:
  - Flag,
  - Address,
  - Control,
  - Protocol,
  - Payload,
  - Checksum,
  - Trailing flag.
- Uses **byte stuffing** so delimiters do not appear "raw" in the payload.
- Can negotiate compression/omission of certain constant fields.

### 3.5.1 Packet over SONET

- SONET provides a well-defined physical bitstream rate over fiber WAN.
- PPP provides the framing to carry IP packets over that stream.
- The payload may be scrambled to preserve transitions and synchronization.
- Typical use: carrier backbone links and high-capacity WAN.

### 3.5.2 ADSL

- Reuses the telephone local loop and divides it into channels/frequencies
  for voice and data, with marked rate asymmetry.
- The data link layer must coexist with the physical characteristics of
  copper and mass residential access.
- Highly dependent on distance, noise, and pair quality.

### 3.5.3 DOCSIS

- On cable, the data link layer works over a shared medium with a
  temporal/channelized allocation defined by the HFC architecture.
- DOCSIS is not purely physical; its link efficiency depends on scheduling,
  ranging, and shared upstream usage.

## When to use what

- **FEC** when retransmission is too costly or the traffic is real-time.
- **Detection + retransmission** when the link is reasonably good.
- **Stop-and-wait** only for simplicity or links with minimal BDP.
- **Sliding window** when real link efficiency matters.
- **PPP** when framing and negotiation are needed over a heterogeneous
  point-to-point link.
- **CRC** when strong frame-level error detection is needed.

## Link diagnostic checklist

- Are frames being formed correctly?
- Are FCS/CRC errors rising?
- Does the frame size match expectations?
- Is there an MTU/encapsulation mismatch between endpoints?
- Is the window too small for the link's RTT?
- Are retransmissions caused by real noise or by a poorly tuned timeout?
- Is the link truly point-to-point, or does it share an upstream resource?

## Anti-patterns and common mistakes

- Using stop-and-wait on high-BDP links and being surprised by low
  efficiency.
- Confusing local flow control with end-to-end network congestion.
- Diagnosing CRC errors as an "application problem."
- Choosing heavy FEC on a link where retransmission would be cheaper.
- Forgetting that PPP provides general framing/negotiation and not
  necessarily full HDLC-style reliability.
- Ignoring that ADSL and DOCSIS inherit limits from the physical medium and
  its sharing model.

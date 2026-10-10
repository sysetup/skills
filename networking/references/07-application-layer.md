# 07 – Application layer

## Table of contents

- Scope
- Mental model
- 7.1 DNS
- 7.2 Email
- 7.3 Web
- 7.4 Streaming audio and video
- 7.5 Content delivery
- Selection guide
- Troubleshooting checklist
- Anti-patterns

## Scope

Use this file when the problem involves DNS, email, HTTP/HTTPS, Web content,
streaming, CDN, proxies, P2P, or the experience perceived by the application.

## Mental model

The application layer is where the user ultimately "sees" the network.
Correct diagnosis here requires examining simultaneously:

- application semantics,
- name dependencies,
- session/security establishment,
- content distribution,
- and the behavior of the transport layer underneath.

## 7.1 Domain Name System (DNS)

### 7.1.1 History and overview

- DNS replaces flat naming schemes with a distributed hierarchy.
- Its most visible function is mapping human-readable names to Internet
  endpoints.
- In modern practice it also supports policies, blocklists, and
  service/replica location.

### 7.1.2 DNS lookup process

- A client typically queries a local **recursive resolver**.
- The resolver makes iterative queries to root, TLD, and authoritative
  servers as needed.
- Caching reduces latency and load but also complicates troubleshooting.
- If a service "goes down only for some users," think about caches, TTLs,
  and different resolvers.

### 7.1.3 Name space and hierarchy

- Hierarchical delegated space.
- Each domain administers its subdomains.
- Organization follows administrative boundaries, not physical topology.
- This explains why hosts on the same LAN may belong to very different
  domains and why DNS authority cannot be inferred from local connectivity.

### 7.1.4 DNS queries and responses

- Common query: **A** record (or modern equivalents for IP address families).
- Responses contain resource records with TTL and type.
- DNS is also used for reputation lists and other auxiliary purposes.
- Common mistake: thinking "DNS returns an IP" is the whole story; it also
  returns control over caching, authorship, and sometimes replica selection.

### 7.1.5 Name resolution

- Effective resolution depends on iterative/recursive lookup, caches, and
  resolver policy.
- A name can resolve differently depending on location and operator.

### 7.1.6 Hands on with DNS

- The chapter insists on observing real queries/responses to understand the
  system; in troubleshooting, a concrete capture/response is worth more than
  an abstract explanation.

### 7.1.7 DNS privacy

- DNS leaks valuable metadata about user activity.
- Modern trends include encrypting the resolution channel and increasing
  privacy protections.
- If the user asks about DoH/privacy, treat it as an application-layer
  problem with clear security and observability implications.

### 7.1.8 Contention over names

- Names have economic and political value.
- Not every DNS problem is technical: sometimes it is about delegation,
  trademark, or control.

### DNS practical rules

- Separate **resolution** failures from **reachability** failures.
- Verify which resolver the client is actually using.
- Observe TTL, authoritative vs. cached, and consistency across zones.
- If the service uses CDN/anycast, "I got a different IP" may be normal.

## 7.2 Electronic mail

### 7.2.1 Architecture and services

- Email is conceptually peer-to-peer between servers, even though the user
  sees it as client-server via their mail agent.
- Essential components:
  - user agent,
  - mail submission/transfer,
  - final delivery.

### 7.2.2 User agent

- Interface with the end user.
- Composes, sends, organizes, and retrieves messages.
- The symptom "I don't see my email" may lie in the agent, not in transport.

### 7.2.3 Message formats

- Separating headers from body is critical for routing, interoperability,
  and security.
- Headers explain the route, logical sender, encoding, and attachments.
- Correct email diagnosis almost always begins with reading full headers.

### 7.2.4 Message transfer

- Transfer relies on SMTP and intermediate servers.
- There may be queues, retries, and multiple relays.
- If mail "is delayed" but eventually arrives, think about queuing,
  reputation, or relay policy.

### 7.2.5 Final delivery

- Final delivery clearly separates inter-server transport from user
  retrieval (e.g., IMAP and other mechanisms in the mail ecosystem).
- A mailbox/synchronization problem does not necessarily imply an SMTP
  failure.

### Email practical rules

- SMTP explains submission/transfer; IMAP/retrieval explains final
  visibility.
- Always differentiate "not sent," "not transferred," "rejected,"
  "delivered but not visible," and "marked as spam."

## 7.3 World Wide Web

### 7.3.1 Architectural overview

- The Web combines names (DNS), transport, content, and application state.
- Components: browser, server, Web objects, caches, proxies, security.
- Loading a page rarely involves a single transaction; it usually triggers
  multiple DNS queries, connections, and object fetches.

### 7.3.2 Static Web objects

- The server delivers pre-existing objects.
- Performance depends on caching, object size, latency, and connections.

### 7.3.3 Dynamic Web pages and Web applications

- Content is generated or personalized using state, logic, and a backend.
- Here a slow Web experience may be a server/application problem, not a
  network issue.

### 7.3.4 HTTP and HTTPS

- HTTP defines methods, responses, objects, and cache control.
- HTTPS adds security via TLS to protect the channel.
- If a Web application fails "only with HTTPS," check the TLS handshake,
  names, certificates, and middleboxes, not just TCP reachability.

### 7.3.5 Web privacy

- The modern Web includes tracking, third-party content, and metadata
  exposure.
- Secure design should consider not only encryption but also minimization of
  unnecessary observability.

### Web practical rules

- Differentiate DNS failure, TCP/TLS failure, HTTP semantic failure, backend
  failure, and static-content failure.
- Check status codes, redirects, time to first byte, and total load time.
- Do not declare "network down" if only specific objects from a third-party
  domain fail.

## 7.4 Streaming audio and video

### 7.4.1 Digital audio

- Digital audio involves sampling, quantization, and compression.
- The trade-off is always between quality, bit rate, and network robustness.

### 7.4.2 Digital video

- Video amplifies the challenges: much higher bit rate, aggressive
  compression, and sensitivity to loss/jitter depending on the delivery
  mode.

### 7.4.3 Streaming stored media

- The content already exists and can absorb network variations with
  buffering.
- Adaptive and segmented strategies are natural here.
- The symptom "it plays, but pauses" suggests insufficient throughput/QoE
  rather than a total reachability failure.

### 7.4.4 Real-time streaming

- Less margin for buffering and late retransmissions.
- Delay and jitter dominate over total reliability.
- If the user asks to optimize a video call or live media, the target metric
  is not the same as for downloading a large file.

### Streaming practical rules

- Stored media tolerates buffering; real-time media tolerates it far less.
- CDN, nearby cache, and anycast help more with stored or mass content.
- For real-time, examine the path, jitter, loss, and end-to-end congestion
  control before touching only the app.

## 7.5 Content delivery

### 7.5.1 Content and Internet traffic

- A large share of Internet traffic is dominated by content delivery.
- This pushes the design of caches, user proximity, and efficient routes.

### 7.5.2 Server farms and Web proxies

- Server farms concentrate compute and service capacity.
- Proxies can reduce load, bring content closer, and enforce policies.
- If multiple users access similar objects, a proxy/cache may have more
  impact than tuning individual transport.

### 7.5.3 Content Delivery Networks

- Replicate content geographically and select an appropriate replica.
- Selection depends on distance, load, and network conditions.
- In troubleshooting, remember that a CDN may respond differently by region
  or operator; you will not always see the same route/IP everywhere.

### 7.5.4 Peer-to-peer networks

- No fixed client and server roles; peers exchange content.
- The chapter discusses scaling, incentive, and verification issues.
- Gnutella exemplifies flooding/gossip and its limits.
- BitTorrent addresses scaling, incentives, and verification with fragment
  tracking and more efficient mechanisms, including DHTs in modern systems.

### 7.5.5 Evolution of the Internet

- The network evolves toward distributed cloud services and edge delivery.
- Content access increasingly depends on placement and distribution
  architecture, not just a "central server."

## "When to use what" guide

- **Classic DNS**: hierarchical name resolution.
- **Encrypted/privacy-enhanced DNS**: when resolution metadata matters.
- **SMTP + mailbox retrieval**: traditional email with clear role separation.
- **HTTPS**: Web where confidentiality/integrity/authentication matter.
- **CDN**: popular and globally distributed content.
- **Proxy/cache**: local savings and object repetition.
- **P2P**: distribution among participants where distributed collaboration
  adds value.

## Quick decision tree

1. If it fails by name, go to DNS before HTTP.
2. If the name resolves but the Web doesn't load, separate TCP/TLS from
   HTTP/backend.
3. If email goes out but doesn't arrive, follow submission → transfer →
   delivery.
4. If streaming buffers, ask whether it is stored or real-time.
5. If one region performs worse than another, suspect CDN, cache, or replica
   selection.
6. If popular content saturates the origin, think edge/CDN/proxy before a
   single bigger server.

## Application troubleshooting checklist

- Does the name resolve correctly and consistently?
- Is the TCP/TLS connection established?
- What HTTP or application response code is observed?
- Is the problem one of authentication/session or of transport?
- Does email fail at submission, relay, delivery, or final visibility?
- Is buffering caused by lack of throughput, excess jitter, or a saturated
  server?
- Is the client reaching the expected CDN replica?

## Anti-patterns and common mistakes

- Diagnosing "HTTP down" without verifying DNS and TLS first.
- Treating email as a single phase or a single protocol.
- Treating stored streaming as if it were real-time, or vice versa.
- Ignoring caches and CDNs when interpreting different responses across
  users.
- Assuming that a domain corresponds to a single fixed server.
- Measuring Web experience only by Mbps without examining latency, objects,
  TLS, and backend.

# 08 – Network security
## Table of contents
- Scope
- Mental model
- 8.1 Fundamentals
- 8.2 Ingredients of an attack
- 8.3 Firewalls and IDS/IPS
- 8.4–8.8 Cryptography, signatures, and public keys
- 8.9 Authentication
- 8.10 Communication security
- 8.11 Email security
- 8.12 Web security
- 8.13 Social issues
- Selection guide
- Assessment checklist
- Anti-patterns
## Scope
Use this file when the user requests network hardening, firewalls, IDS/IPS,
defensive segmentation, encryption, authentication, TLS, IPsec, VPN, PKI,
Kerberos, DNSSEC, or network-level attack/defense analysis.
## Mental model
Network security is not an isolated product. It is the consistent application
of principles across all relevant layers of the communication system. The
correct sequence is:

1. identify assets and attack surface,
2. model how the network is actually attacked,
3. choose preventive/detective/corrective controls,
4. verify that those controls do not rest on false assumptions.
## 8.1 Network security fundamentals
### Security across all layers
- Link: local authentication, medium protection, sniffing risk.
- Network: filtering, reachability control, IPsec, segmentation.
- Transport: secure end-to-end connections, e.g., TLS.
- Application: user authentication, signing, non-repudiation, content
  control.
- Common mistake: thinking that "deploying TLS" replaces controls at other
  layers.
### 8.1.1 Fundamental security principles
The text revisits the classic Saltzer and Schroeder principles. Use them
explicitly when designing or critiquing an architecture:

1. **Economy of mechanism / simplicity**
   - Simpler systems have fewer bugs and a smaller attack surface.
   - If a function is not necessary, remove it.
2. **Fail-safe defaults**
   - The secure default is to deny unless explicitly authorized.
3. **Complete mediation**
   - Every access to every resource must be verified.
4. **Least authority / least privilege**
   - Each component should have only the minimum necessary privilege.
5. **Privilege separation**
   - Multiple bounded components are better than a single all-powerful one.
6. **Least common mechanism**
   - Minimize mechanisms shared across many users.
7. **Open design**
   - Security should not depend on the secrecy of the design.
8. **Psychological acceptability**
   - If security is impractical, users will circumvent it.
9. **Work factor**
   - The cost of the attack must exceed the value/feasibility of the target.
10. **Recording of compromises**
   - Detecting and recording compromises is as important as preventing them.
### 8.1.2 Fundamental attack principles
- The attacker exploits visibility, complexity, implicit trust, and weak
  defaults.
- A single isolated control is rarely sufficient; attacks chain multiple
  weaknesses.
### 8.1.3 From threats to solutions
- Threat → vector → surface → control → validation.
- Never propose a control without stating which threat it reduces and what
  residual risk remains.
## 8.2 Basic ingredients of an attack
### 8.2.1 Reconnaissance
- Before exploiting, the attacker needs a map: hosts, services, routes,
  names, trust relationships, software, and exposure.
- Much can be inferred solely from technical observation of the network.
- Designing without considering what the network reveals at rest is already
  starting at a disadvantage.
### 8.2.2 Sniffing and snooping (with a dash of spoofing)
- If traffic or metadata is observable, an attacker learns patterns,
  credentials, or internal structure.
- The risk increases on shared and wireless media.
- Content confidentiality alone does not eliminate metadata leakage.
### 8.2.3 Spoofing (beyond ARP)
- Impersonating a host, service, or response identity to deceive the victim.
- Can affect addresses, names, routes, or query responses.
- The correct defense almost always includes strong authentication, not just
  filtering.
### 8.2.4 Disruption
- Attacks targeting availability: saturate, overflow, block, divert.
- An insecure network is not only one that leaks data; it is also one that
  stops functioning.
## 8.3 Firewalls and intrusion detection/prevention
### 8.3.1 Firewalls
#### What they do well
- Delineate a perimeter and a reachability policy.
- Filter inbound/outbound traffic.
- Can be packet filters, stateful, or application-level gateways.
- Excellent for enforcing secure defaults between domains.
#### Conceptual types
- **Packet filtering**: decides based on headers.
- **Stateful firewall**: incorporates connection state for richer decisions.
- **Application gateway / proxy**: deeper protocol inspection.
#### Limitations the chapter emphasizes
- Break layer purity by inspecting beyond the network layer.
- Depend on well-known ports and application heuristics.
- Encryption can make part of the content opaque to the firewall.
- Do not explain to the host why traffic was dropped; from the endpoint they
  look like a "broken cable."
- A single perimeter is not enough: the textbook emphasizes **defense in
  depth**.
#### Operational conclusion
- Use firewalls as part of layered defenses, not as a single talisman.
- Combine perimeter, internal segmentation, and per-host controls when the
  risk warrants it.
### 8.3.2 Intrusion detection and prevention
- IDS/IPS complement the firewall by detecting anomalous patterns or
  behaviors.
- Primary utility:
  - discover attacks that passed the perimeter,
  - detect compromise or reconnaissance,
  - generate operational evidence.
- They do not replace a secure architecture; they help observe it when it
  fails.
## 8.4 Cryptography
### 8.4.1 Introduction to cryptography
- Transforms a readable message into a protected one using keys and
  transformations.
- Primary purposes: confidentiality, integrity, authentication,
  non-repudiation.
### 8.4.2 Two fundamental cryptographic principles
- Security must not depend on the secrecy of the algorithm but on the key.
- Practical resistance depends on key space, key management, and correct
  protocol design around the algorithm.
### 8.4.3 Substitution ciphers
- Historically important for understanding substitution and basic
  cryptanalysis.
- Not viable as a serious modern defense.
### 8.4.4 Transposition ciphers
- Rearrange without changing symbols; also pedagogical and insufficient
  today.
### 8.4.5 One-time pads
- Perfectly secure in theory if the key is random, as long as the message,
  and never reused.
- Infeasible at scale due to key distribution and management.
- Lesson: the key problem is usually harder than the algorithm problem.
## 8.5 Symmetric-key algorithms
### General principle
- Same key for encryption and decryption.
- Fast and suitable for bulk encryption once the key is shared.
### 8.5.1 DES
- Historically important.
- No longer adequate as a primary modern defense.
### 8.5.2 AES
- Prominent modern symmetric standard highlighted in the chapter.
- Good balance between security and performance.
- Practical foundation for many current encryption systems, including modern
  WiFi.
### 8.5.3 Cipher modes
- The base algorithm needs a mode of operation for long messages.
- Modes determine chaining properties, parallelism, and error propagation.
- Common mistake: talking about "using AES" without specifying the mode,
  integrity, and IV management.
## 8.6 Public-key algorithms
### General principle
- Key pair: public and private.
- Facilitate authentication, key exchange, and signing.
- More expensive than symmetric; hence typically used for bootstrapping and
  not for all bulk data.
### 8.6.1 RSA
- Central example in the chapter.
- Based on the mathematical properties of factoring and modular
  exponentiation.
- Useful for authentication, key exchange, and signing, depending on the
  protocol.
### 8.6.2 Other public-key algorithms
- The text notes that RSA is not the only approach; design should consider
  the family of techniques and the concrete protocol.
## 8.7 Digital signatures
### 8.7.1 Symmetric-key signatures
- Conceptually possible with trusted third parties, but less natural for
  broad non-repudiation.
### 8.7.2 Public-key signatures
- Signing with the private key and verifying with the public key allows
  proving origin and integrity from the verifier's perspective, provided
  they trust the key.
### 8.7.3 Message digests
- Hash functions condense messages into digests resistant to practical
  collisions.
- The signature is usually applied to the digest, not the full message, for
  efficiency.
### 8.7.4 The birthday attack
- Illustrates why collisions are more probable than intuition suggests as
  the sample scales.
- Relevant for choosing adequate hash sizes and understanding design limits.
## 8.8 Public-key management
### 8.8.1 Certificates
- Bind identity to a public key through the signature of a trusted authority
  or entity.
- Without a way to trust the public key, public-key cryptography alone is
  insufficient.
### 8.8.2 X.509
- Standard certificate format/structure prominent in networks and the Web.
- Carries identity, key, validity, issuer, and signature.
### 8.8.3 Public Key Infrastructures
- PKI is the operational trust system around certificates.
- Includes issuance, distribution, validation, and revocation or
  equivalents.
- A poorly operated PKI makes any protocol that depends on it fragile.
## 8.9 Authentication protocols
### Objective
- Prevent spoofing by verifying that the counterpart is who they claim to
  be.
- Authentication must also resist replay and other protocol attacks.
### 8.9.1 Authentication based on a shared secret key
- Both parties prove knowledge of the shared secret.
- Requires protecting the secret and using nonces/challenges to prevent
  replay.
### 8.9.2 Diffie-Hellman key exchange
- Allows establishing a shared secret over an insecure channel.
- By itself it does not authenticate identity; it must be accompanied by
  authentication to prevent man-in-the-middle.
### 8.9.3 Authentication using a Key Distribution Center
- A KDC centralizes credential or key distribution/validation.
- Scales better than pairwise shared secrets but introduces strong
  dependence on a critical third party.
### 8.9.4 Kerberos
- Implements ticket-based authentication with a central trusted entity.
- Very useful in closed administrative/enterprise domains.
- If the user requests SSO or internal domain authentication, Kerberos is a
  natural reference.
### 8.9.5 Authentication using public-key cryptography
- Avoids some limitations of shared secrets but relies on the validity of
  the PKI and the protocol that uses the keys.
## 8.10 Communication security
### 8.10.1 IPsec
- Security at the IP level.
- Provides authentication, integrity, and/or encryption depending on the
  mode/protocol used.
- Chapter concepts:
  - SA (Security Association),
  - AH/ESP as relevant mechanisms,
  - transport mode vs. tunnel mode.
- Appropriate when protecting IP traffic without rewriting applications.
### 8.10.2 Virtual Private Networks
- Build a private logical topology over public or third-party
  infrastructure.
- The textbook highlights VPNs over the Internet using firewalls and tunnels
  between offices.
- Also mentions MPLS-backed VPNs managed by the ISP.
- Essential advantage: transparency for the user and reuse of existing
  connectivity.
### 8.10.3 Wireless security
- WiFi adds a particular attack surface because the medium extends beyond
  the physical perimeter.
- WEP is insecure.
- WPA/WPA2 improve authentication and encryption; 802.1X/EAP adds
  centralized enterprise control.
- Common mistake: designing a "secure" logical network while forgetting that
  radio bypasses the wall firewall.
## 8.11 Email security
### 8.11.1 Pretty Good Privacy (PGP)
- Protects email using a mix of symmetric and public-key cryptography.
- Good case study of end-to-end encryption/signing.
- The chapter also uses it as a reminder that powerful security may not
  achieve mass adoption if it is hard to use.
### 8.11.2 S/MIME
- Variant based on certificates and the enterprise mail ecosystem.
- Relevant when the organization already lives comfortably with PKI/X.509.
## 8.12 Web security
### 8.12.1 Threats
- The Web faces spoofing, malicious content, session theft, untrusted
  scripts, and name/channel manipulation.
- "Having HTTPS" is not enough; the attack surface is broader.
### 8.12.2 Secure naming and DNSSEC
- DNSSEC signs DNS data to authenticate responses and protect the delegation
  chain.
- Provides naming security and also helps against certain forms of spoofing.
- If the user asks to protect resolution, DNSSEC is the application/naming-
  layer answer.
### 8.12.3 TLS
- Originated as SSL and evolved into TLS for secure connections.
- Provides server authentication (and optionally client authentication),
  channel integrity, and confidentiality.
- Relies on certificates and public keys for bootstrapping, and symmetric
  keys for data.
- If HTTPS fails, distinguish:
  - name/certificate,
  - handshake,
  - suites/algorithms,
  - middleboxes,
  - application above.
### 8.12.4 Running untrusted code
- Browsers execute potentially dangerous content/scripting.
- Secure Web design involves isolation and execution policies, not just
  encryption.
## 8.13 Social issues
### 8.13.1 Confidential and anonymous communication
- Security also concerns privacy and anonymity, not just perimeter defense.
### 8.13.2 Freedom of speech
- Network controls can impact expression and access to information.
### 8.13.3 Copyright
- Distribution and security design interacts with intellectual property and
  content control.
## "When to use what" guide
- **Stateless/stateful firewall**: enforce reachability and secure defaults.
- **Application gateway**: when application semantics matter and cost
  justifies it.
- **IDS/IPS**: detection/complement, not a substitute for secure design.
- **AES**: modern bulk encryption.
- **RSA/public-key**: authentication, signing, and key exchange.
- **PKI/X.509**: when scalable trust among many entities is central.
- **Kerberos**: centralized authentication within a trust domain.
- **IPsec**: IP traffic security and tunnels.
- **TLS**: application/transport session security, especially Web.
- **VPN**: connecting sites/users over a public network while maintaining a
  private logical topology.
- **DNSSEC**: DNS data authenticity.
- **802.1X/EAP**: enterprise WiFi access control.
## Quick decision tree
1. If the problem is port exposure or reachability, start with firewalls and
   segmentation.
2. If the problem is identity trust, start with authentication, not
   encryption alone.
3. If the problem is data secrecy in transit, choose among TLS, IPsec, or
   VPN by layer/scope.
4. If the problem is forged resolution, go to DNSSEC.
5. If the problem is corporate WiFi, incorporate 802.1X/EAP beyond
   encryption.
6. If the problem is an enterprise domain, Kerberos/KDC may be more natural
   than ad-hoc pairwise secrets.
## Network security assessment checklist
- What is the asset and who needs access?
- What does the network reveal even when the payload is encrypted?
- Is the default deny or allow?
- Do segmentation and defense in depth exist?
- Is authentication resistant to replay/spoofing?
- Is key/certificate management resolved or assumed magically?
- Does the chosen control protect against the real threat or just a
  caricature of it?
- What logs/evidence remain if the control fails?
## Anti-patterns and common mistakes
- Relying on a single perimeter firewall.
- Confusing encryption with authentication.
- Deploying strong cryptography with weak key management.
- Using WEP or insecure defaults for convenience.
- Assuming that Diffie-Hellman authenticates by itself.
- Talking about TLS without reviewing certificates and names.
- Believing that encrypted content eliminates all privacy problems.
- Designing security so inconvenient that users circumvent it.

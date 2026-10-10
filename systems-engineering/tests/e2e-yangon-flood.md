# Worked example (not an executed E2E evaluation) — novice request: Yangon flood monitoring

Input: "Diseña desde cero un sistema de monitoreo de inundaciones para Yangon."

All local conditions, institutions, numbers, and interfaces below are illustrative assumptions,
not verified findings about Yangon. No local research, deployment, or real-agent trial is recorded.
Confirm the affected communities, operator authority, actual networks, and geography before design.

Lifecycle: conceptual design. SOI: Yangon Flood Monitoring System (YFMS).
WSOI: Yangon city emergency-management capability.

## System frame

- Mission: detect river and drainage threshold breaches in Yangon and notify the city emergency center in time for public warning.
- Boundary: sensors, edge gateways, monitoring software, operator HMI, and the alert interface to the emergency center. Roads, pumps, shelters, and broadcast media are external.
- External systems: Ayeyarwady/Yangon river gauges (if not owned), weather service, cellular/radio network, city emergency center, township administrators, public warning channels.
- Constraints assumed: monsoon operations; power-unreliable sites; mixed Burmese/English operator language; increment 1 covers named high-risk townships, not the entire metropolitan area.
- Assumptions marked assumed: 60-second detection, 15-minute notification, 24-hour logging, GSM/LTE backhaul, and no control of pumps in increment 1. All require stakeholder review.

## Minimum artifact set

ConOps: operators watch a common operating picture; when a gauge crosses a staged threshold, YFMS sends an alert to the emergency center; township administrators confirm receipt; the public-warning decision stays with the emergency center.

Context: YFMS in the center; river, rainfall, and drainage sensors in; emergency center and weather service out; power and comms as enabling externals.

RBS:
- 0.0 Monitor flood risk in named Yangon townships
  - 1.0 Sense water level and rainfall
  - 2.0 Transmit and time-stamp observations
  - 3.0 Detect threshold breach
  - 4.0 Alert emergency center
  - 5.0 Support operators and maintainers

Selected draft SHALL statements (origin: illustrative; approval: pending):

| ID | Statement | Verification |
|---|---|---|
| SYR-001 | The YFMS shall detect a water-level threshold breach at each instrumented site within 60 seconds of the physical crossing. | test |
| SYR-002 | The YFMS shall deliver a structured alert to the city emergency-center interface within 15 minutes of a confirmed threshold breach. | test |
| SYR-003 | The YFMS shall continue local logging for at least 24 hours when backhaul is lost. | test |
| SYR-004 | The YFMS shall not issue actuator commands to pumps or gates in increment 1. | inspection |

Architecture CIs: Sensor Node, Site Gateway, Monitoring Core, Operator HMI, Alert Gateway.

V&V: VT-001 site-level threshold injection; VT-002 end-to-end alert timing; VAL-001 monsoon tabletop with emergency-center operators.

Risks: comms loss during storms (reduce with dual-path radio/cellular and local store-and-forward); sensor vandalism; silt fouling of level sensors.

Next review: proposed SDR to assess baseline readiness, not to assume approval. Confirm named townships, thresholds, sources, parents, operators, validation criteria, and open safety issues first.

V&V state: all activities planned; result not-run; actual evidence none. VT-003 for logging endurance and inspection VI-004 for absence of actuator interfaces must also be planned. No complete requirement-to-test evidence claim is made.

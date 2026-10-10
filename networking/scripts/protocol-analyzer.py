#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""protocol-analyzer.py

Minimal packet analyzer for classic Ethernet PCAP captures and raw hexadecimal
Ethernet frame streams without external dependencies.

Supported decoders and heuristics:

- Ethernet II, optional 802.1Q / 802.1ad VLAN tags
- ARP
- IPv4
- IPv6 with basic extension-header handling
- ICMP / ICMPv6
- TCP
- UDP
- DNS (header + first question)
- HTTP request / response heuristics
- TLS record / handshake heuristics

This tool is intentionally conservative. It does not replace Wireshark or
`tshark`, and it still rejects PCAPNG. Instead, it provides enough structure to
answer common operational questions such as:

- Which layers are present in the packet or capture?
- Which endpoints talk the most?
- Are there signs of DNS, HTTP, TLS, or DHCP?
- Does the packet structure align with the current troubleshooting hypothesis?
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import ipaddress
import json
import struct
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import BinaryIO, Iterable

MIN_PYTHON = (3, 10)

PCAP_MAGICS = {
    b"\xa1\xb2\xc3\xd4": (">", "usec"),
    b"\xd4\xc3\xb2\xa1": ("<", "usec"),
    b"\xa1\xb2\x3c\x4d": (">", "nsec"),
    b"\x4d\x3c\xb2\xa1": ("<", "nsec"),
}
PCAPNG_MAGIC = b"\x0a\x0d\x0d\x0a"
SUPPORTED_LINKTYPE_ETHERNET = 1

ETHERTYPE_NAMES = {
    0x0800: "IPv4",
    0x0806: "ARP",
    0x8100: "802.1Q",
    0x88A8: "802.1ad",
    0x86DD: "IPv6",
}

IP_PROTOCOL_NAMES = {
    1: "ICMP",
    6: "TCP",
    17: "UDP",
    50: "ESP",
    58: "ICMPv6",
}

ICMP_TYPE_NAMES = {
    0: "echo-reply",
    3: "destination-unreachable",
    5: "redirect",
    8: "echo-request",
    11: "time-exceeded",
}

ICMPV6_TYPE_NAMES = {
    1: "destination-unreachable",
    2: "packet-too-big",
    3: "time-exceeded",
    128: "echo-request",
    129: "echo-reply",
}

DNS_TYPE_NAMES = {
    1: "A",
    2: "NS",
    5: "CNAME",
    6: "SOA",
    12: "PTR",
    15: "MX",
    16: "TXT",
    28: "AAAA",
    33: "SRV",
    41: "OPT",
}

TLS_CONTENT_TYPES = {
    20: "change-cipher-spec",
    21: "alert",
    22: "handshake",
    23: "application-data",
}

TLS_HANDSHAKE_TYPES = {
    1: "ClientHello",
    2: "ServerHello",
    4: "NewSessionTicket",
    8: "EncryptedExtensions",
    11: "Certificate",
    13: "CertificateRequest",
    15: "CertificateVerify",
    20: "Finished",
}

HTTP_METHODS = (
    b"GET ",
    b"POST ",
    b"PUT ",
    b"DELETE ",
    b"HEAD ",
    b"OPTIONS ",
    b"PATCH ",
)

IPV6_EXTENSION_HEADERS = {
    0: "Hop-by-Hop",
    43: "Routing",
    44: "Fragment",
    50: "ESP",
    51: "AH",
    60: "Destination Options",
}


class CaptureError(Exception):
    """Raised when the input cannot be parsed safely."""


@dataclass
class PcapMetadata:
    path: str
    source_kind: str
    endianness: str
    timestamp_resolution: str
    version_major: int
    version_minor: int
    snaplen: int
    linktype: int


@dataclass
class PacketSummary:
    index: int
    timestamp: str
    included_length: int
    original_length: int
    layer2: str = "Unknown"
    layer3: str = "Unknown"
    layer4: str = "Unknown"
    app: str = "Unknown"
    src_mac: str | None = None
    dst_mac: str | None = None
    vlan_tags: list[int] = field(default_factory=list)
    src_ip: str | None = None
    dst_ip: str | None = None
    src_port: int | None = None
    dst_port: int | None = None
    info: str = ""


@dataclass
class CaptureSummary:
    metadata: PcapMetadata
    total_packets: int = 0
    total_bytes: int = 0
    first_timestamp: str | None = None
    last_timestamp: str | None = None
    layer3_counts: collections.Counter = field(default_factory=collections.Counter)
    layer4_counts: collections.Counter = field(default_factory=collections.Counter)
    app_counts: collections.Counter = field(default_factory=collections.Counter)
    talkers: collections.Counter = field(default_factory=collections.Counter)
    conversations: collections.Counter = field(default_factory=collections.Counter)
    vlan_tagged_packets: int = 0

    def to_jsonable(self) -> dict:
        return {
            "metadata": asdict(self.metadata),
            "total_packets": self.total_packets,
            "total_bytes": self.total_bytes,
            "first_timestamp": self.first_timestamp,
            "last_timestamp": self.last_timestamp,
            "layer3_counts": dict(self.layer3_counts),
            "layer4_counts": dict(self.layer4_counts),
            "app_counts": dict(self.app_counts),
            "top_talkers": self.talkers.most_common(10),
            "top_conversations": self.conversations.most_common(10),
            "vlan_tagged_packets": self.vlan_tagged_packets,
        }


@dataclass
class PcapPacket:
    timestamp: float
    included_length: int
    original_length: int
    payload: bytes


@dataclass
class DecodedTransport:
    layer4: str
    app: str = "Unknown"
    src_port: int | None = None
    dst_port: int | None = None
    info: str = ""


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Analyze a classic Ethernet PCAP capture or a hexadecimal Ethernet "
            "frame stream and print a layered summary. PCAPNG is rejected with "
            "an explicit error."
        )
    )
    parser.add_argument(
        "capture",
        nargs="?",
        help="Path to a classic .pcap capture file",
    )
    parser.add_argument(
        "--hex-stream",
        help=(
            "Hexadecimal Ethernet frame stream. Use '-' to read from stdin. "
            "Provide one non-empty frame per line when multiple frames are "
            "supplied."
        ),
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Maximum number of packet detail lines to print (default: 20)",
    )
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Only print the aggregated summary and suppress per-packet output",
    )
    parser.add_argument(
        "--filter",
        choices=["all", "arp", "icmp", "icmpv6", "tcp", "udp", "dns", "http", "tls"],
        default="all",
        help="Restrict packet detail lines to a protocol/application class",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of human-readable text",
    )
    args = parser.parse_args(argv)
    if args.limit < 0:
        parser.error("--limit must be zero or a positive integer")
    capture_given = args.capture is not None
    hex_given = args.hex_stream is not None
    if capture_given == hex_given:
        parser.error("provide exactly one of <capture> or --hex-stream")
    return args


def read_exact(handle: BinaryIO, size: int, context: str) -> bytes:
    data = handle.read(size)
    if len(data) != size:
        raise CaptureError(f"Unexpected end of file while reading {context}")
    return data


def parse_pcap_header(handle: BinaryIO, path: Path) -> PcapMetadata:
    magic = read_exact(handle, 4, "PCAP magic number")
    if magic == PCAPNG_MAGIC:
        raise CaptureError(
            "PCAPNG is not supported by this script. Export the capture as legacy PCAP first."
        )
    if magic not in PCAP_MAGICS:
        raise CaptureError("Unknown file signature. Expected a classic PCAP magic number.")

    endianness, ts_resolution = PCAP_MAGICS[magic]
    header = read_exact(handle, 20, "PCAP global header")
    version_major, version_minor, _thiszone, _sigfigs, snaplen, linktype = struct.unpack(
        endianness + "HHiIII", header
    )
    return PcapMetadata(
        path=str(path),
        source_kind="pcap",
        endianness="little" if endianness == "<" else "big",
        timestamp_resolution=ts_resolution,
        version_major=version_major,
        version_minor=version_minor,
        snaplen=snaplen,
        linktype=linktype,
    )


def iter_pcap_packets(handle: BinaryIO, metadata: PcapMetadata) -> Iterable[PcapPacket]:
    endian = "<" if metadata.endianness == "little" else ">"
    frac_divisor = 1_000_000_000 if metadata.timestamp_resolution == "nsec" else 1_000_000

    while True:
        raw_header = handle.read(16)
        if not raw_header:
            return
        if len(raw_header) != 16:
            raise CaptureError("Truncated per-packet header in capture")
        ts_sec, ts_frac, incl_len, orig_len = struct.unpack(endian + "IIII", raw_header)
        if incl_len > metadata.snaplen and metadata.snaplen > 0:
            raise CaptureError(
                f"Packet length {incl_len} exceeds configured snaplen {metadata.snaplen}"
            )
        payload = read_exact(handle, incl_len, f"packet payload ({incl_len} bytes)")
        timestamp = ts_sec + (ts_frac / frac_divisor)
        yield PcapPacket(timestamp, incl_len, orig_len, payload)


def format_timestamp(timestamp: float) -> str:
    base = dt.datetime.fromtimestamp(timestamp, tz=dt.timezone.utc)
    return base.isoformat().replace("+00:00", "Z")


def mac_addr(raw: bytes) -> str:
    return ":".join(f"{byte:02x}" for byte in raw)


def ipv4_addr(raw: bytes) -> str:
    return str(ipaddress.IPv4Address(raw))


def ipv6_addr(raw: bytes) -> str:
    return str(ipaddress.IPv6Address(raw))


def safe_ascii(payload: bytes, max_len: int = 120) -> str:
    text = payload[:max_len].decode("ascii", errors="replace")
    return text.replace("\r", "\\r").replace("\n", "\\n")


def decode_dns_name(payload: bytes, offset: int, depth: int = 0) -> tuple[str, int]:
    if depth > 10:
        raise CaptureError("DNS name compression loop detected")

    labels: list[str] = []
    jumped = False
    jump_return_offset = None

    while True:
        if offset >= len(payload):
            raise CaptureError("DNS name exceeds payload length")
        length = payload[offset]

        if length == 0:
            offset += 1
            break

        if length & 0xC0 == 0xC0:
            if offset + 1 >= len(payload):
                raise CaptureError("Truncated DNS compression pointer")
            pointer = ((length & 0x3F) << 8) | payload[offset + 1]
            name, _ = decode_dns_name(payload, pointer, depth + 1)
            labels.append(name)
            jump_return_offset = offset + 2
            offset += 2
            jumped = True
            break

        offset += 1
        end = offset + length
        if end > len(payload):
            raise CaptureError("Truncated DNS label")
        labels.append(payload[offset:end].decode("ascii", errors="replace"))
        offset = end

    if jumped:
        return ".".join(part for part in labels if part), jump_return_offset or offset
    return ".".join(labels), offset


def decode_dns(payload: bytes) -> tuple[str, str]:
    if len(payload) < 12:
        return "DNS", "short dns payload"
    transaction_id, flags, qdcount, ancount, nscount, arcount = struct.unpack(
        "!HHHHHH", payload[:12]
    )
    qr = "response" if (flags & 0x8000) else "query"
    info = f"id=0x{transaction_id:04x} {qr} qd={qdcount} an={ancount} ns={nscount} ar={arcount}"
    if qdcount == 0:
        return "DNS", info

    try:
        name, offset = decode_dns_name(payload, 12)
        if offset + 4 <= len(payload):
            qtype, qclass = struct.unpack("!HH", payload[offset:offset + 4])
            info += (
                f" first-question={name or '.'}"
                f" type={DNS_TYPE_NAMES.get(qtype, qtype)} class={qclass}"
            )
        else:
            info += f" first-question={name or '.'}"
    except CaptureError as exc:
        info += f" question-decode-error={exc}"
    return "DNS", info


def detect_tls(payload: bytes) -> tuple[str | None, str]:
    if len(payload) < 5:
        return None, ""
    content_type = payload[0]
    version_major = payload[1]
    version_minor = payload[2]
    record_length = struct.unpack("!H", payload[3:5])[0]
    if content_type not in TLS_CONTENT_TYPES or version_major != 3:
        return None, ""

    info = (
        f"record={TLS_CONTENT_TYPES[content_type]} version=3.{version_minor}"
        f" length={record_length}"
    )
    if content_type == 22 and len(payload) >= 9:
        handshake_type = payload[5]
        hs_length = int.from_bytes(payload[6:9], "big")
        info += (
            f" handshake={TLS_HANDSHAKE_TYPES.get(handshake_type, handshake_type)}"
            f" hs-len={hs_length}"
        )
    return "TLS", info


def detect_http(payload: bytes) -> tuple[str | None, str]:
    if not payload:
        return None, ""
    if payload.startswith(HTTP_METHODS) or payload.startswith(b"HTTP/"):
        first_line = payload.split(b"\r\n", 1)[0]
        return "HTTP", safe_ascii(first_line, max_len=100)
    return None, ""


def decode_icmp(payload: bytes) -> DecodedTransport:
    if len(payload) < 4:
        return DecodedTransport(layer4="ICMP", info="short icmp payload")
    icmp_type, code, checksum = struct.unpack("!BBH", payload[:4])
    info = (
        f"type={icmp_type}({ICMP_TYPE_NAMES.get(icmp_type, 'unknown')}) "
        f"code={code} checksum=0x{checksum:04x}"
    )
    return DecodedTransport(layer4="ICMP", info=info)


def decode_icmpv6(payload: bytes) -> DecodedTransport:
    if len(payload) < 4:
        return DecodedTransport(layer4="ICMPv6", info="short icmpv6 payload")
    icmp_type, code, checksum = struct.unpack("!BBH", payload[:4])
    info = (
        f"type={icmp_type}({ICMPV6_TYPE_NAMES.get(icmp_type, 'unknown')}) "
        f"code={code} checksum=0x{checksum:04x}"
    )
    return DecodedTransport(layer4="ICMPv6", info=info)


TCP_FLAG_BITS = [
    (0x100, "NS"),
    (0x080, "CWR"),
    (0x040, "ECE"),
    (0x020, "URG"),
    (0x010, "ACK"),
    (0x008, "PSH"),
    (0x004, "RST"),
    (0x002, "SYN"),
    (0x001, "FIN"),
]


def decode_tcp(payload: bytes) -> DecodedTransport:
    if len(payload) < 20:
        return DecodedTransport(layer4="TCP", info="short tcp header")
    src_port, dst_port, seq, ack, offset_flags, window, checksum, urgent = struct.unpack(
        "!HHIIHHHH", payload[:20]
    )
    data_offset = ((offset_flags >> 12) & 0xF) * 4
    flags_value = offset_flags & 0x1FF
    flags = ",".join(name for bit, name in TCP_FLAG_BITS if flags_value & bit) or "none"
    tcp_payload = payload[data_offset:] if data_offset <= len(payload) else b""

    app = "Unknown"
    app_info = ""

    http_name, http_info = detect_http(tcp_payload)
    if http_name:
        app, app_info = http_name, http_info
    else:
        tls_name, tls_info = detect_tls(tcp_payload)
        if tls_name:
            app, app_info = tls_name, tls_info
        elif src_port in {25, 465, 587} or dst_port in {25, 465, 587}:
            app = "SMTP"
            app_info = safe_ascii(tcp_payload)
        elif src_port in {110, 995} or dst_port in {110, 995}:
            app = "POP3"
            app_info = safe_ascii(tcp_payload)
        elif src_port in {143, 993} or dst_port in {143, 993}:
            app = "IMAP"
            app_info = safe_ascii(tcp_payload)

    info = f"seq={seq} ack={ack} flags={flags} win={window} checksum=0x{checksum:04x}"
    if urgent:
        info += f" urg={urgent}"
    if app_info:
        info += f" app-detail={app_info}"

    return DecodedTransport(
        layer4="TCP",
        app=app,
        src_port=src_port,
        dst_port=dst_port,
        info=info,
    )


def decode_udp(payload: bytes) -> DecodedTransport:
    if len(payload) < 8:
        return DecodedTransport(layer4="UDP", info="short udp header")
    src_port, dst_port, length, checksum = struct.unpack("!HHHH", payload[:8])
    udp_payload = payload[8:length] if length <= len(payload) else payload[8:]

    app = "Unknown"
    app_info = ""
    if src_port == 53 or dst_port == 53:
        app, app_info = decode_dns(udp_payload)
    elif src_port == 123 or dst_port == 123:
        app = "NTP"
    elif src_port in {67, 68} or dst_port in {67, 68}:
        app = "DHCP"

    info = f"len={length} checksum=0x{checksum:04x}"
    if app_info:
        info += f" app-detail={app_info}"

    return DecodedTransport(
        layer4="UDP",
        app=app,
        src_port=src_port,
        dst_port=dst_port,
        info=info,
    )


def decode_ipv4(payload: bytes, pkt: PacketSummary) -> None:
    if len(payload) < 20:
        pkt.layer3 = "IPv4"
        pkt.info = "short ipv4 header"
        return

    version_ihl = payload[0]
    version = version_ihl >> 4
    ihl = (version_ihl & 0x0F) * 4
    if version != 4 or ihl < 20:
        pkt.layer3 = "IPv4"
        pkt.info = "invalid ipv4 header"
        return

    dscp_ecn = payload[1]
    total_length = struct.unpack("!H", payload[2:4])[0]
    identification = struct.unpack("!H", payload[4:6])[0]
    flags_fragment = struct.unpack("!H", payload[6:8])[0]
    ttl = payload[8]
    protocol = payload[9]
    header_checksum = struct.unpack("!H", payload[10:12])[0]
    src_ip = ipv4_addr(payload[12:16])
    dst_ip = ipv4_addr(payload[16:20])

    pkt.layer3 = "IPv4"
    pkt.src_ip = src_ip
    pkt.dst_ip = dst_ip

    payload_end = min(total_length, len(payload)) if total_length else len(payload)
    l4_payload = payload[ihl:payload_end]

    fragment_offset = flags_fragment & 0x1FFF
    more_fragments = bool(flags_fragment & 0x2000)
    dont_fragment = bool(flags_fragment & 0x4000)

    base_info = (
        f"src={src_ip} dst={dst_ip} ttl={ttl} proto={IP_PROTOCOL_NAMES.get(protocol, protocol)} "
        f"len={total_length} id=0x{identification:04x} dscp-ecn=0x{dscp_ecn:02x} "
        f"df={'1' if dont_fragment else '0'} mf={'1' if more_fragments else '0'} "
        f"frag-offset={fragment_offset} hdr-csum=0x{header_checksum:04x}"
    )

    if fragment_offset != 0:
        pkt.layer4 = "Fragment"
        pkt.info = base_info + " non-initial fragment"
        return

    if protocol == 1:
        decoded = decode_icmp(l4_payload)
    elif protocol == 6:
        decoded = decode_tcp(l4_payload)
    elif protocol == 17:
        decoded = decode_udp(l4_payload)
    else:
        decoded = DecodedTransport(layer4=IP_PROTOCOL_NAMES.get(protocol, str(protocol)))

    pkt.layer4 = decoded.layer4
    pkt.app = decoded.app
    pkt.src_port = decoded.src_port
    pkt.dst_port = decoded.dst_port
    pkt.info = base_info + (f" {decoded.info}" if decoded.info else "")


def parse_ipv6_extension_chain(payload: bytes, next_header: int, offset: int) -> tuple[int, int, list[str], bool]:
    notes: list[str] = []
    non_initial_fragment = False

    while next_header in IPV6_EXTENSION_HEADERS:
        if next_header == 50:
            notes.append("ext=ESP encrypted-payload")
            return next_header, offset, notes, non_initial_fragment

        if len(payload) < offset + 2:
            raise CaptureError("Truncated IPv6 extension header")

        if next_header == 44:
            if len(payload) < offset + 8:
                raise CaptureError("Truncated IPv6 fragment header")
            following = payload[offset]
            fragment_field = struct.unpack("!H", payload[offset + 2:offset + 4])[0]
            fragment_offset = (fragment_field >> 3) & 0x1FFF
            more_fragments = bool(fragment_field & 0x1)
            identification = struct.unpack("!I", payload[offset + 4:offset + 8])[0]
            notes.append(
                f"ext=Fragment offset={fragment_offset} mf={'1' if more_fragments else '0'} "
                f"id=0x{identification:08x}"
            )
            next_header = following
            offset += 8
            if fragment_offset != 0:
                non_initial_fragment = True
                return next_header, offset, notes, non_initial_fragment
            continue

        following = payload[offset]
        if next_header == 51:
            header_length = (payload[offset + 1] + 2) * 4
        else:
            header_length = (payload[offset + 1] + 1) * 8
        if header_length <= 0 or len(payload) < offset + header_length:
            raise CaptureError("Truncated IPv6 extension header payload")
        notes.append(f"ext={IPV6_EXTENSION_HEADERS[next_header]} len={header_length}")
        next_header = following
        offset += header_length

    return next_header, offset, notes, non_initial_fragment


def decode_ipv6(payload: bytes, pkt: PacketSummary) -> None:
    if len(payload) < 40:
        pkt.layer3 = "IPv6"
        pkt.info = "short ipv6 header"
        return

    version = payload[0] >> 4
    if version != 6:
        pkt.layer3 = "IPv6"
        pkt.info = "invalid ipv6 header"
        return

    payload_length = struct.unpack("!H", payload[4:6])[0]
    next_header = payload[6]
    hop_limit = payload[7]
    src_ip = ipv6_addr(payload[8:24])
    dst_ip = ipv6_addr(payload[24:40])

    pkt.layer3 = "IPv6"
    pkt.src_ip = src_ip
    pkt.dst_ip = dst_ip

    payload_end = min(40 + payload_length, len(payload)) if payload_length else len(payload)
    current_header = next_header
    offset = 40
    current_header, offset, ext_notes, non_initial_fragment = parse_ipv6_extension_chain(
        payload[:payload_end], current_header, offset
    )
    l4_payload = payload[offset:payload_end]

    base_info = (
        f"src={src_ip} dst={dst_ip} hop-limit={hop_limit} "
        f"next={IP_PROTOCOL_NAMES.get(current_header, current_header)} payload-len={payload_length}"
    )
    if ext_notes:
        base_info += " " + " ".join(ext_notes)

    if non_initial_fragment:
        pkt.layer4 = "Fragment"
        pkt.info = base_info + " non-initial fragment"
        return

    if current_header == 58:
        decoded = decode_icmpv6(l4_payload)
    elif current_header == 6:
        decoded = decode_tcp(l4_payload)
    elif current_header == 17:
        decoded = decode_udp(l4_payload)
    elif current_header == 50:
        decoded = DecodedTransport(layer4="ESP", info="encrypted payload not decoded")
    else:
        decoded = DecodedTransport(layer4=IP_PROTOCOL_NAMES.get(current_header, str(current_header)))

    pkt.layer4 = decoded.layer4
    pkt.app = decoded.app
    pkt.src_port = decoded.src_port
    pkt.dst_port = decoded.dst_port
    pkt.info = base_info + (f" {decoded.info}" if decoded.info else "")


def decode_arp(payload: bytes, pkt: PacketSummary) -> None:
    pkt.layer3 = "ARP"
    pkt.layer4 = "N/A"
    if len(payload) < 28:
        pkt.info = "short arp payload"
        return
    htype, ptype, hlen, plen, oper = struct.unpack("!HHBBH", payload[:8])
    sha = mac_addr(payload[8:14])
    spa = ipv4_addr(payload[14:18]) if plen == 4 else payload[14:18].hex()
    tha = mac_addr(payload[18:24])
    tpa = ipv4_addr(payload[24:28]) if plen == 4 else payload[24:28].hex()
    oper_name = {1: "request", 2: "reply"}.get(oper, str(oper))
    pkt.src_ip = spa if isinstance(spa, str) else None
    pkt.dst_ip = tpa if isinstance(tpa, str) else None
    pkt.info = (
        f"htype={htype} ptype=0x{ptype:04x} hlen={hlen} plen={plen} op={oper_name} "
        f"sha={sha} spa={spa} tha={tha} tpa={tpa}"
    )


def decode_ethernet(frame: bytes, index: int, timestamp: str) -> PacketSummary:
    pkt = PacketSummary(
        index=index,
        timestamp=timestamp,
        included_length=len(frame),
        original_length=len(frame),
        layer2="Ethernet",
    )

    if len(frame) < 14:
        pkt.info = "short ethernet frame"
        return pkt

    pkt.dst_mac = mac_addr(frame[0:6])
    pkt.src_mac = mac_addr(frame[6:12])
    offset = 12
    ethertype = struct.unpack("!H", frame[offset:offset + 2])[0]
    offset += 2

    while ethertype in {0x8100, 0x88A8}:
        if len(frame) < offset + 4:
            pkt.info = "truncated vlan tag"
            return pkt
        tci = struct.unpack("!H", frame[offset:offset + 2])[0]
        pkt.vlan_tags.append(tci & 0x0FFF)
        ethertype = struct.unpack("!H", frame[offset + 2:offset + 4])[0]
        offset += 4

    payload = frame[offset:]
    pkt.layer3 = ETHERTYPE_NAMES.get(ethertype, f"0x{ethertype:04x}")

    if ethertype == 0x0800:
        decode_ipv4(payload, pkt)
    elif ethertype == 0x0806:
        decode_arp(payload, pkt)
    elif ethertype == 0x86DD:
        decode_ipv6(payload, pkt)
    else:
        pkt.info = f"unhandled ethertype 0x{ethertype:04x}"

    return pkt


def packet_matches_filter(pkt: PacketSummary, filter_name: str) -> bool:
    if filter_name == "all":
        return True
    name = filter_name.lower()
    return any(value and name == str(value).lower() for value in (pkt.layer3, pkt.layer4, pkt.app))


def conversation_key(pkt: PacketSummary) -> str | None:
    if not pkt.src_ip or not pkt.dst_ip:
        return None
    if pkt.src_port is None or pkt.dst_port is None:
        return f"{pkt.layer4} {pkt.src_ip} -> {pkt.dst_ip}"
    return f"{pkt.layer4} {pkt.src_ip}:{pkt.src_port} -> {pkt.dst_ip}:{pkt.dst_port}"


def summarize_packet(summary: CaptureSummary, pkt: PacketSummary) -> None:
    summary.total_packets += 1
    summary.total_bytes += pkt.included_length
    summary.layer3_counts[pkt.layer3] += 1
    summary.layer4_counts[pkt.layer4] += 1
    summary.app_counts[pkt.app] += 1
    if pkt.vlan_tags:
        summary.vlan_tagged_packets += 1
    for host in (pkt.src_ip, pkt.dst_ip):
        if host:
            summary.talkers[host] += 1
    conversation = conversation_key(pkt)
    if conversation:
        summary.conversations[conversation] += 1


def retain_packet(
    packets: list[PacketSummary],
    pkt: PacketSummary,
    detail_limit: int,
    filter_name: str,
) -> None:
    if detail_limit <= 0 or len(packets) >= detail_limit:
        return
    if packet_matches_filter(pkt, filter_name):
        packets.append(pkt)


def analyze_capture(
    path: Path,
    detail_limit: int = 20,
    filter_name: str = "all",
) -> tuple[CaptureSummary, list[PacketSummary]]:
    if not path.exists():
        raise CaptureError(f"Capture file not found: {path}")
    if not path.is_file():
        raise CaptureError(f"Path is not a regular file: {path}")

    try:
        handle = path.open("rb")
    except OSError as exc:
        raise CaptureError(f"Cannot read capture file {path}: {exc.strerror or exc}") from exc

    try:
        metadata = parse_pcap_header(handle, path)
        if metadata.linktype != SUPPORTED_LINKTYPE_ETHERNET:
            raise CaptureError(
                f"Unsupported linktype {metadata.linktype}. Only Ethernet (linktype 1) is supported."
            )
        summary = CaptureSummary(metadata=metadata)
        packets: list[PacketSummary] = []
        for index, raw_pkt in enumerate(iter_pcap_packets(handle, metadata), start=1):
            timestamp = format_timestamp(raw_pkt.timestamp)
            pkt = decode_ethernet(raw_pkt.payload, index=index, timestamp=timestamp)
            pkt.included_length = raw_pkt.included_length
            pkt.original_length = raw_pkt.original_length
            summarize_packet(summary, pkt)
            retain_packet(packets, pkt, detail_limit, filter_name)
            summary.first_timestamp = summary.first_timestamp or timestamp
            summary.last_timestamp = timestamp
    finally:
        handle.close()
    return summary, packets


def normalize_hex_line(raw_line: str, lineno: int) -> bytes | None:
    line = raw_line.split("#", 1)[0].strip()
    if not line:
        return None
    line = line.replace("0x", "").replace("0X", "")
    for token in (" ", "\t", ":", "-", ".", "|", "_"):
        line = line.replace(token, "")
    if len(line) % 2 != 0:
        raise CaptureError(f"line {lineno}: odd number of hexadecimal characters")
    try:
        return bytes.fromhex(line)
    except ValueError as exc:
        raise CaptureError(f"line {lineno}: invalid hexadecimal stream: {exc}")


def analyze_hex_stream(
    source: str,
    detail_limit: int = 20,
    filter_name: str = "all",
) -> tuple[CaptureSummary, list[PacketSummary]]:
    raw_text = sys.stdin.read() if source == "-" else source
    label = "<stdin-hex>" if source == "-" else "<hex-stream>"
    lines = raw_text.splitlines() or [raw_text]
    frames: list[bytes] = []
    for lineno, raw_line in enumerate(lines, start=1):
        frame = normalize_hex_line(raw_line, lineno)
        if frame is not None:
            frames.append(frame)
    if not frames:
        raise CaptureError("No hexadecimal frames were provided")

    metadata = PcapMetadata(
        path=label,
        source_kind="hex",
        endianness="n/a",
        timestamp_resolution="n/a",
        version_major=0,
        version_minor=0,
        snaplen=max(len(frame) for frame in frames),
        linktype=SUPPORTED_LINKTYPE_ETHERNET,
    )
    summary = CaptureSummary(metadata=metadata)
    packets: list[PacketSummary] = []
    for index, frame in enumerate(frames, start=1):
        pkt = decode_ethernet(frame, index=index, timestamp="n/a")
        summarize_packet(summary, pkt)
        retain_packet(packets, pkt, detail_limit, filter_name)
    return summary, packets


def render_human(summary: CaptureSummary, packets: list[PacketSummary], args: argparse.Namespace) -> str:
    lines: list[str] = []
    lines.append("Capture summary")
    lines.append("===============")
    if summary.metadata.source_kind == "pcap":
        lines.append(f"File: {summary.metadata.path}")
        lines.append(
            f"Format: classic PCAP v{summary.metadata.version_major}.{summary.metadata.version_minor} "
            f"({summary.metadata.endianness}-endian, {summary.metadata.timestamp_resolution})"
        )
        lines.append(f"Link type: {summary.metadata.linktype} (Ethernet)")
        lines.append(f"Snaplen: {summary.metadata.snaplen}")
        if summary.first_timestamp and summary.last_timestamp:
            lines.append(f"Time span: {summary.first_timestamp} -> {summary.last_timestamp}")
    else:
        lines.append(f"Input: {summary.metadata.path}")
        lines.append("Format: raw hexadecimal Ethernet frame stream")
        lines.append(f"Maximum frame size: {summary.metadata.snaplen}")
    lines.append(f"Packets: {summary.total_packets}")
    lines.append(f"Bytes (captured): {summary.total_bytes}")
    lines.append(f"VLAN-tagged packets: {summary.vlan_tagged_packets}")
    lines.append("")

    def append_counter(title: str, counter: collections.Counter) -> None:
        lines.append(title)
        if not counter:
            lines.append("  (none)")
        else:
            for key, value in counter.most_common():
                lines.append(f"  - {key}: {value}")
        lines.append("")

    append_counter("Layer-3 distribution", summary.layer3_counts)
    append_counter("Layer-4 distribution", summary.layer4_counts)
    append_counter("Application hints", summary.app_counts)

    lines.append("Top talkers")
    if not summary.talkers:
        lines.append("  (none)")
    else:
        for host, count in summary.talkers.most_common(10):
            lines.append(f"  - {host}: {count} packet endpoints")
    lines.append("")

    lines.append("Top conversations")
    if not summary.conversations:
        lines.append("  (none)")
    else:
        for conversation, count in summary.conversations.most_common(10):
            lines.append(f"  - {conversation}: {count}")
    lines.append("")

    if not args.summary_only:
        lines.append("Packet details")
        lines.append("--------------")
        for pkt in packets:
            lines.append(
                f"#{pkt.index:<4} {pkt.timestamp} len={pkt.included_length} "
                f"L2={pkt.layer2} L3={pkt.layer3} L4={pkt.layer4} APP={pkt.app} "
                f"SRC={pkt.src_ip or pkt.src_mac or '?'}"
                f"{(':' + str(pkt.src_port)) if pkt.src_port is not None else ''} -> "
                f"DST={pkt.dst_ip or pkt.dst_mac or '?'}"
                f"{(':' + str(pkt.dst_port)) if pkt.dst_port is not None else ''}"
            )
            if pkt.vlan_tags:
                lines.append(f"      VLAN tags: {', '.join(str(tag) for tag in pkt.vlan_tags)}")
            if pkt.info:
                lines.append(f"      {pkt.info}")
        if not packets:
            lines.append("(No packets matched the selected filter.)")

    return "\n".join(lines).rstrip() + "\n"


def render_json(summary: CaptureSummary, packets: list[PacketSummary], args: argparse.Namespace) -> str:
    filtered_packets = [asdict(pkt) for pkt in packets] if not args.summary_only else []
    return json.dumps({"summary": summary.to_jsonable(), "packets": filtered_packets}, indent=2) + "\n"


def main(argv: list[str] | None = None) -> int:
    if sys.version_info < MIN_PYTHON:
        print(
            f"error: Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ is required, "
            f"found {sys.version_info.major}.{sys.version_info.minor}",
            file=sys.stderr,
        )
        return 2
    args = parse_args(argv or sys.argv[1:])
    detail_limit = 0 if args.summary_only else args.limit
    try:
        if args.capture:
            summary, packets = analyze_capture(
                Path(args.capture),
                detail_limit=detail_limit,
                filter_name=args.filter,
            )
        else:
            summary, packets = analyze_hex_stream(
                args.hex_stream,
                detail_limit=detail_limit,
                filter_name=args.filter,
            )
        if args.json:
            sys.stdout.write(render_json(summary, packets, args))
        else:
            sys.stdout.write(render_human(summary, packets, args))
        return 0
    except CaptureError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Interrupted", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())

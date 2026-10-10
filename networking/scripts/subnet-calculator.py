#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""CIDR/VLSM subnet calculator.

This tool supports three common planning tasks:
1. Summarize one or more CIDR blocks.
2. Allocate VLSM subnets from a parent network based on host counts.
3. Split a network into equal-size child subnets.

Only Python stdlib is used. The logic follows the book's focus on hierarchical
addressing, CIDR aggregation, and practical subnet sizing.
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import math
import sys
from dataclasses import dataclass
from typing import Iterable, List

MAX_SPLIT_SUBNETS = 4096
MIN_PYTHON = (3, 10)


@dataclass
class NetworkSummary:
    network: ipaddress.IPv4Network | ipaddress.IPv6Network

    @property
    def version(self) -> int:
        return self.network.version

    @property
    def total_addresses(self) -> int:
        return self.network.num_addresses

    @property
    def usable_hosts(self) -> int:
        # Conservative conventional-host interpretation.
        if self.network.version == 4:
            if self.network.prefixlen >= 31:
                return 0
            return max(self.network.num_addresses - 2, 0)
        return self.network.num_addresses

    @property
    def first_usable(self) -> str:
        if self.network.version == 4:
            if self.network.prefixlen >= 31:
                return "n/a"
            return str(self.network.network_address + 1)
        return str(self.network.network_address)

    @property
    def last_usable(self) -> str:
        if self.network.version == 4:
            if self.network.prefixlen >= 31:
                return "n/a"
            return str(self.network.broadcast_address - 1)
        return str(self.network.broadcast_address)

    @property
    def broadcast(self) -> str:
        if self.network.version == 4:
            return str(self.network.broadcast_address)
        return "n/a"

    @property
    def netmask(self) -> str:
        return str(self.network.netmask)

    def to_dict(self) -> dict:
        return {
            "network": str(self.network),
            "version": self.version,
            "netmask": self.netmask,
            "network_address": str(self.network.network_address),
            "broadcast": self.broadcast,
            "first_usable": self.first_usable,
            "last_usable": self.last_usable,
            "total_addresses": self.total_addresses,
            "usable_hosts": self.usable_hosts,
        }


@dataclass
class VLSMAllocation:
    label: str
    required_hosts: int
    prefixlen: int
    subnet: ipaddress.IPv4Network

    @property
    def provided_hosts(self) -> int:
        return NetworkSummary(self.subnet).usable_hosts

    @property
    def waste(self) -> int:
        return self.provided_hosts - self.required_hosts

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "required_hosts": self.required_hosts,
            "prefixlen": self.prefixlen,
            "subnet": str(self.subnet),
            "network_address": str(self.subnet.network_address),
            "broadcast": str(self.subnet.broadcast_address),
            "first_usable": NetworkSummary(self.subnet).first_usable,
            "last_usable": NetworkSummary(self.subnet).last_usable,
            "provided_hosts": self.provided_hosts,
            "waste": self.waste,
        }


def die(message: str) -> "NoReturn":
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(2)


def parse_network(value: str) -> ipaddress.IPv4Network | ipaddress.IPv6Network:
    try:
        return ipaddress.ip_network(value, strict=False)
    except ValueError as exc:
        die(f"invalid network '{value}': {exc}")


def parse_positive_int(value: str) -> int:
    try:
        number = int(value)
    except ValueError as exc:
        die(f"invalid integer '{value}': {exc}")
    if number <= 0:
        die(f"value must be positive, got {number}")
    return number


def parse_host_requirements(raw: str) -> List[tuple[str, int]]:
    """Parse VLSM requirements.

    Supported forms:
    - "100,50,20" -> labels auto-generated as net1, net2, net3
    - "users=100,servers=50,mgmt=20"
    """
    requirements: List[tuple[str, int]] = []
    if not raw.strip():
        die("host requirements cannot be empty")
    items = [item.strip() for item in raw.split(",") if item.strip()]
    if not items:
        die("no usable host requirements found")
    for index, item in enumerate(items, start=1):
        if "=" in item:
            label, count = item.split("=", 1)
            label = label.strip()
            if not label:
                die(f"missing label in requirement '{item}'")
            requirements.append((label, parse_positive_int(count.strip())))
        else:
            requirements.append((f"net{index}", parse_positive_int(item)))
    return requirements


def smallest_ipv4_prefix_for_hosts(hosts: int) -> int:
    """Return the smallest conventional IPv4 prefix that can fit `hosts` hosts.

    This uses the conventional network+broadcast reservation model taught in most
    subnetting exercises. For example, 50 hosts requires 64 addresses -> /26.
    """
    if hosts <= 0:
        die("host requirement must be positive")
    needed_addresses = hosts + 2
    power = math.ceil(math.log2(needed_addresses))
    prefix = 32 - power
    if prefix < 0:
        die(f"host requirement too large for IPv4: {hosts}")
    return prefix


def align_up(value: int, block_size: int) -> int:
    remainder = value % block_size
    if remainder == 0:
        return value
    return value + (block_size - remainder)


def count_child_subnets(network: ipaddress.IPv4Network | ipaddress.IPv6Network, new_prefix: int) -> int:
    return 1 << (new_prefix - network.prefixlen)


def allocate_vlsm(parent: ipaddress.IPv4Network, requirements: List[tuple[str, int]]) -> List[VLSMAllocation]:
    if parent.version != 4:
        die("VLSM allocation currently supports IPv4 parent networks only")

    # Largest-first allocation reduces fragmentation and matches standard VLSM practice.
    ordered = sorted(
        enumerate(requirements),
        key=lambda item: (-item[1][1], item[0]),
    )

    current = int(parent.network_address)
    parent_last = int(parent.broadcast_address)
    allocations: List[VLSMAllocation] = []

    for _, (label, hosts) in ordered:
        prefix = smallest_ipv4_prefix_for_hosts(hosts)
        block_size = 1 << (32 - prefix)
        candidate_start = align_up(current, block_size)
        candidate_end = candidate_start + block_size - 1

        if candidate_end > parent_last:
            die(
                f"parent network {parent} is too small for requirement '{label}={hosts}'"
            )

        subnet = ipaddress.IPv4Network((candidate_start, prefix))
        if not subnet.subnet_of(parent):
            die(
                f"candidate subnet {subnet} for '{label}' escapes parent network {parent}"
            )

        allocations.append(VLSMAllocation(label=label, required_hosts=hosts, prefixlen=prefix, subnet=subnet))
        current = candidate_end + 1

    # Return in original descending allocation order; easier for planners to read.
    return allocations


def format_table(rows: List[List[str]]) -> str:
    widths = [max(len(row[i]) for row in rows) for i in range(len(rows[0]))]
    lines = []
    for ridx, row in enumerate(rows):
        line = "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row))
        lines.append(line)
        if ridx == 0:
            lines.append("  ".join("-" * widths[i] for i in range(len(widths))))
    return "\n".join(lines)


def cmd_summary(args: argparse.Namespace) -> int:
    networks = [parse_network(item) for item in args.networks]
    data = [NetworkSummary(net).to_dict() for net in networks]
    if args.json:
        print(json.dumps(data, indent=2))
        return 0

    rows = [[
        "network", "version", "netmask", "network_address", "broadcast",
        "first_usable", "last_usable", "total_addrs", "usable_hosts",
    ]]
    for item in data:
        rows.append([
            item["network"], str(item["version"]), item["netmask"],
            item["network_address"], item["broadcast"], item["first_usable"],
            item["last_usable"], str(item["total_addresses"]),
            str(item["usable_hosts"]),
        ])
    print(format_table(rows))
    return 0


def cmd_vlsm(args: argparse.Namespace) -> int:
    parent = parse_network(args.parent)
    if not isinstance(parent, ipaddress.IPv4Network):
        die("--parent must be an IPv4 CIDR block for VLSM mode")
    requirements = parse_host_requirements(args.hosts)
    allocations = allocate_vlsm(parent, requirements)

    used_addresses = sum(alloc.subnet.num_addresses for alloc in allocations)
    free_addresses = parent.num_addresses - used_addresses

    payload = {
        "parent": str(parent),
        "allocations": [alloc.to_dict() for alloc in allocations],
        "summary": {
            "parent_total_addresses": parent.num_addresses,
            "allocated_addresses": used_addresses,
            "remaining_addresses": free_addresses,
        },
    }
    if args.json:
        print(json.dumps(payload, indent=2))
        return 0

    rows = [[
        "label", "required_hosts", "subnet", "prefix", "first_usable",
        "last_usable", "broadcast", "provided_hosts", "waste",
    ]]
    for alloc in allocations:
        summary = NetworkSummary(alloc.subnet)
        rows.append([
            alloc.label,
            str(alloc.required_hosts),
            str(alloc.subnet),
            f"/{alloc.prefixlen}",
            summary.first_usable,
            summary.last_usable,
            summary.broadcast,
            str(alloc.provided_hosts),
            str(alloc.waste),
        ])

    print(f"Parent network : {parent}")
    print(f"Allocated addrs: {used_addresses}")
    print(f"Remaining addrs: {free_addresses}")
    print()
    print(format_table(rows))
    return 0


def cmd_split(args: argparse.Namespace) -> int:
    network = parse_network(args.network)
    new_prefix = parse_positive_int(args.new_prefix)
    if new_prefix <= network.prefixlen:
        die(
            f"new prefix must be longer than parent prefix ({network.prefixlen}), got {new_prefix}"
        )
    if new_prefix > network.max_prefixlen:
        die(f"new prefix cannot exceed /{network.max_prefixlen}")

    child_count = count_child_subnets(network, new_prefix)
    if child_count > MAX_SPLIT_SUBNETS:
        die(
            f"split would produce {child_count} child subnets; maximum supported is "
            f"{MAX_SPLIT_SUBNETS}"
        )

    subnets = list(network.subnets(new_prefix=new_prefix))
    data = [NetworkSummary(subnet).to_dict() for subnet in subnets]
    if args.json:
        print(json.dumps(data, indent=2))
        return 0

    rows = [[
        "subnet", "netmask", "network_address", "broadcast",
        "first_usable", "last_usable", "usable_hosts",
    ]]
    for item in data:
        rows.append([
            item["network"], item["netmask"], item["network_address"], item["broadcast"],
            item["first_usable"], item["last_usable"], str(item["usable_hosts"]),
        ])
    print(format_table(rows))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CIDR/VLSM calculator for network design and validation.",
        epilog=(
            "Examples:\n"
            "  subnet-calculator.py summary 10.0.0.0/24 2001:db8::/64\n"
            "  subnet-calculator.py vlsm --parent 10.20.0.0/24 --hosts users=100,servers=50,mgmt=20\n"
            "  subnet-calculator.py split --network 192.168.10.0/24 --new-prefix 26"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_summary = subparsers.add_parser("summary", help="summarize one or more CIDR blocks")
    p_summary.add_argument("networks", nargs="+", help="CIDR blocks to summarize")
    p_summary.add_argument("--json", action="store_true", help="emit JSON instead of a text table")
    p_summary.set_defaults(func=cmd_summary)

    p_vlsm = subparsers.add_parser("vlsm", help="allocate VLSM subnets from an IPv4 parent network")
    p_vlsm.add_argument("--parent", required=True, help="parent IPv4 CIDR block, e.g. 10.0.0.0/16")
    p_vlsm.add_argument(
        "--hosts",
        required=True,
        help=(
            "comma-separated host requirements; either counts '100,50,20' or labeled "
            "entries 'users=100,servers=50,mgmt=20'"
        ),
    )
    p_vlsm.add_argument("--json", action="store_true", help="emit JSON instead of a text table")
    p_vlsm.set_defaults(func=cmd_vlsm)

    p_split = subparsers.add_parser("split", help="split a network into equal-size child subnets")
    p_split.add_argument("--network", required=True, help="parent network to split")
    p_split.add_argument("--new-prefix", required=True, help="child prefix length, e.g. 26")
    p_split.add_argument("--json", action="store_true", help="emit JSON instead of a text table")
    p_split.set_defaults(func=cmd_split)

    return parser


def main(argv: Iterable[str] | None = None) -> int:
    if sys.version_info < MIN_PYTHON:
        print(
            f"error: Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ is required, "
            f"found {sys.version_info.major}.{sys.version_info.minor}",
            file=sys.stderr,
        )
        return 2
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

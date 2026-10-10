#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Lightweight logical topology validator.
#
# Supported manifest records (space-separated, comments start with '#'):
#   node   <NAME> <TYPE>
#   link   <NODE_A> <NODE_B> <layer2|layer3> [stp=on|off] [desc=TOKEN]
#   subnet <LABEL> <IPv4_CIDR> [gateway=<NODE>] [vlan=<ID>]
#
# Example:
#   node R1 router
#   node SW1 switch
#   node SW2 switch
#   link R1 SW1 layer3
#   link SW1 SW2 layer2 stp=on
#   subnet users 10.10.10.0/24 gateway=R1 vlan=10
#
# The validator checks:
# - duplicate nodes, duplicate links, self-links
# - undefined nodes referenced by links/gateways
# - invalid IPv4 CIDR blocks
# - overlapping IPv4 subnets
# - isolated nodes (warning)
# - probable layer2 cycle risk, with awareness of stp=on annotation

set -euo pipefail

if [[ -z "${BASH_VERSINFO:-}" || "${BASH_VERSINFO[0]}" -lt 4 ]]; then
	printf 'error: Bash 4+ is required\n' >&2
	exit 2
fi

usage() {
	cat <<'USAGE'
Usage:
  topology-validator.sh [--strict] <manifest-file>
  topology-validator.sh --help

Manifest format:
  node   <NAME> <TYPE>
  link   <NODE_A> <NODE_B> <layer2|layer3> [stp=on|off] [desc=TOKEN]
  subnet <LABEL> <IPv4_CIDR> [gateway=<NODE>] [vlan=<ID>]

Examples:
  topology-validator.sh sample.topo
  topology-validator.sh --strict branch-office.topo

Exit codes:
  0 = validation passed (or warnings only, unless --strict)
  1 = validation failed
  2 = usage or input error
USAGE
}

trim() {
	local s="$1"
	s="${s#"${s%%[![:space:]]*}"}"
	s="${s%"${s##*[![:space:]]}"}"
	printf '%s' "$s"
}

error_count=0
warning_count=0
strict=0

add_error() {
	local msg="$1"
	printf 'ERROR: %s\n' "$msg" >&2
	error_count=$((error_count + 1))
}

add_warning() {
	local msg="$1"
	printf 'WARN : %s\n' "$msg" >&2
	warning_count=$((warning_count + 1))
}

is_valid_name() {
	[[ "$1" =~ ^[A-Za-z0-9._-]+$ ]]
}

is_valid_octet() {
	local o="$1"
	[[ "$o" =~ ^[0-9]+$ ]] || return 1
	((o >= 0 && o <= 255))
}

is_valid_vlan() {
	local vlan="$1"
	[[ "$vlan" =~ ^[0-9]+$ ]] || return 1
	((vlan >= 1 && vlan <= 4094))
}

is_valid_ipv4_cidr() {
	local cidr="$1"
	local ip prefix IFS=.
	[[ "$cidr" == */* ]] || return 1
	ip="${cidr%/*}"
	prefix="${cidr#*/}"
	[[ "$prefix" =~ ^[0-9]+$ ]] || return 1
	((prefix >= 0 && prefix <= 32)) || return 1
	read -r o1 o2 o3 o4 extra <<<"$ip"
	[[ -z "${extra:-}" ]] || return 1
	is_valid_octet "$o1" && is_valid_octet "$o2" && is_valid_octet "$o3" && is_valid_octet "$o4"
}

ipv4_to_int() {
	local ip="$1" IFS=.
	read -r o1 o2 o3 o4 <<<"$ip"
	echo $(((o1 << 24) | (o2 << 16) | (o3 << 8) | o4))
}

cidr_to_range() {
	local cidr="$1"
	local ip prefix ip_int mask network broadcast
	ip="${cidr%/*}"
	prefix="${cidr#*/}"
	ip_int=$(ipv4_to_int "$ip")
	if ((prefix == 0)); then
		mask=0
	else
		mask=$(((0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF))
	fi
	network=$((ip_int & mask))
	broadcast=$((network | ((~mask) & 0xFFFFFFFF)))
	printf '%s %s' "$network" "$broadcast"
}

declare -A nodes=()
declare -A node_degree=()
declare -A subnets=()
declare -A subnet_gateway=()
declare -A subnet_vlan=()
declare -A subnet_start=()
declare -A subnet_end=()
declare -A link_seen=()
declare -A adj=()

declare -a link_a=()
declare -a link_b=()
declare -a link_layer=()
declare -a link_stp=()
declare -a link_line=()
declare -a subnet_order=()

if [[ $# -eq 0 ]]; then
	usage
	exit 2
fi

manifest=""
while [[ $# -gt 0 ]]; do
	case "$1" in
	--help | -h)
		usage
		exit 0
		;;
	--strict)
		strict=1
		shift
		;;
	--*)
		printf 'error: unknown option %s\n' "$1" >&2
		usage >&2
		exit 2
		;;
	*)
		if [[ -n "$manifest" ]]; then
			printf 'error: only one manifest file may be provided\n' >&2
			exit 2
		fi
		manifest="$1"
		shift
		;;
	esac
done

if [[ -z "$manifest" ]]; then
	printf 'error: manifest file is required\n' >&2
	exit 2
fi
if [[ ! -f "$manifest" ]]; then
	printf 'error: manifest is not a regular file: %s\n' "$manifest" >&2
	exit 2
fi
if [[ ! -r "$manifest" ]]; then
	printf 'error: cannot read manifest file %s\n' "$manifest" >&2
	exit 2
fi

lineno=0
while IFS= read -r raw || [[ -n "$raw" ]]; do
	lineno=$((lineno + 1))
	line="${raw%%#*}"
	line="$(trim "$line")"
	[[ -z "$line" ]] && continue

	# shellcheck disable=SC2086
	set -- $line
	record="$1"
	shift || true

	case "$record" in
	node)
		if [[ $# -ne 2 ]]; then
			add_error "line $lineno: node requires exactly 2 fields: name type"
			continue
		fi
		name="$1"
		type="$2"
		if ! is_valid_name "$name"; then
			add_error "line $lineno: invalid node name '$name'"
			continue
		fi
		if [[ -n "${nodes[$name]:-}" ]]; then
			add_error "line $lineno: duplicate node '$name'"
			continue
		fi
		nodes[$name]="$type"
		node_degree[$name]=0
		;;

	link)
		if [[ $# -lt 3 ]]; then
			add_error "line $lineno: link requires at least 3 fields: nodeA nodeB layer"
			continue
		fi
		a="$1"
		b="$2"
		layer="$3"
		shift 3 || true
		stp="unset"
		if [[ "$a" == "$b" ]]; then
			add_error "line $lineno: self-link '$a' is not allowed"
			continue
		fi
		if ! is_valid_name "$a" || ! is_valid_name "$b"; then
			add_error "line $lineno: invalid node name in link '$a' <-> '$b'"
			continue
		fi
		if [[ "$layer" != "layer2" && "$layer" != "layer3" ]]; then
			add_error "line $lineno: link layer must be 'layer2' or 'layer3', got '$layer'"
			continue
		fi
		for token in "$@"; do
			case "$token" in
			stp=on | stp=off)
				stp="${token#*=}"
				;;
			desc=?*)
				:
				;;
			*=*)
				add_error "line $lineno: unknown link attribute '$token'"
				;;
			*)
				add_warning "line $lineno: ignored free-form token '$token' in link record"
				;;
			esac
		done
		if [[ "$a" < "$b" ]]; then
			link_key="$a|$b|$layer"
		else
			link_key="$b|$a|$layer"
		fi
		if [[ -n "${link_seen[$link_key]:-}" ]]; then
			add_error "line $lineno: duplicate link '$a' <-> '$b' ($layer); first seen at line ${link_seen[$link_key]}"
			continue
		fi
		link_seen[$link_key]="$lineno"
		link_a+=("$a")
		link_b+=("$b")
		link_layer+=("$layer")
		link_stp+=("$stp")
		link_line+=("$lineno")
		;;

	subnet)
		if [[ $# -lt 2 ]]; then
			add_error "line $lineno: subnet requires at least 2 fields: label cidr"
			continue
		fi
		label="$1"
		cidr="$2"
		shift 2 || true
		if ! is_valid_name "$label"; then
			add_error "line $lineno: invalid subnet label '$label'"
			continue
		fi
		if [[ -n "${subnets[$label]:-}" ]]; then
			add_error "line $lineno: duplicate subnet label '$label'"
			continue
		fi
		if ! is_valid_ipv4_cidr "$cidr"; then
			add_error "line $lineno: invalid IPv4 CIDR '$cidr'"
			continue
		fi
		gateway=""
		vlan=""
		for token in "$@"; do
			case "$token" in
			gateway=?*) gateway="${token#*=}" ;;
			vlan=?*) vlan="${token#*=}" ;;
			*=*) add_error "line $lineno: unknown subnet attribute '$token'" ;;
			*) add_warning "line $lineno: ignored free-form token '$token' in subnet record" ;;
			esac
		done
		read -r start end <<<"$(cidr_to_range "$cidr")"
		subnets[$label]="$cidr"
		subnet_gateway[$label]="$gateway"
		subnet_vlan[$label]="$vlan"
		subnet_start[$label]="$start"
		subnet_end[$label]="$end"
		subnet_order+=("$label")
		;;

	*)
		add_error "line $lineno: unknown record type '$record'"
		;;
	esac
done <"$manifest"

if ((${#nodes[@]} == 0)); then
	add_error "manifest contains no node records"
fi

# Validate link endpoints and build adjacency / degrees.
for i in "${!link_a[@]}"; do
	a="${link_a[$i]}"
	b="${link_b[$i]}"
	layer="${link_layer[$i]}"
	lno="${link_line[$i]}"
	if [[ -z "${nodes[$a]:-}" ]]; then
		add_error "line $lno: link references undefined node '$a'"
	fi
	if [[ -z "${nodes[$b]:-}" ]]; then
		add_error "line $lno: link references undefined node '$b'"
	fi
	if [[ -n "${nodes[$a]:-}" ]]; then
		node_degree[$a]=$((node_degree[$a] + 1))
	fi
	if [[ -n "${nodes[$b]:-}" ]]; then
		node_degree[$b]=$((node_degree[$b] + 1))
	fi
	if [[ "$layer" == "layer2" && -n "${nodes[$a]:-}" && -n "${nodes[$b]:-}" ]]; then
		adj[$a]="${adj[$a]:-} $b"
		adj[$b]="${adj[$b]:-} $a"
	fi
done

# Validate subnet gateway references and VLAN format.
for label in "${subnet_order[@]}"; do
	gateway="${subnet_gateway[$label]}"
	vlan="${subnet_vlan[$label]}"
	if [[ -n "$gateway" && -z "${nodes[$gateway]:-}" ]]; then
		add_error "subnet '$label' references undefined gateway '$gateway'"
	fi
	if [[ -n "$vlan" && ! "$vlan" =~ ^[0-9]+$ ]]; then
		add_error "subnet '$label' has non-numeric vlan value '$vlan'"
	elif [[ -n "$vlan" ]] && ! is_valid_vlan "$vlan"; then
		add_error "subnet '$label' vlan value '$vlan' is out of range (expected 1-4094)"
	fi
done

# Detect overlapping subnets.
for ((i = 0; i < ${#subnet_order[@]}; i++)); do
	for ((j = i + 1; j < ${#subnet_order[@]}; j++)); do
		left="${subnet_order[$i]}"
		right="${subnet_order[$j]}"
		ls="${subnet_start[$left]}"
		le="${subnet_end[$left]}"
		rs="${subnet_start[$right]}"
		re="${subnet_end[$right]}"
		if ((ls <= re && rs <= le)); then
			add_error "subnets '$left' (${subnets[$left]}) and '$right' (${subnets[$right]}) overlap"
		fi
	done
done

# Warn about isolated nodes.
for name in "${!nodes[@]}"; do
	if ((node_degree[$name] == 0)); then
		add_warning "node '$name' has no links"
	fi
done

# Layer2 cycle detection with DFS.
declare -A visited=()
cycle_detected=0
any_stp_on=0
for stp in "${link_stp[@]}"; do
	if [[ "$stp" == "on" ]]; then
		any_stp_on=1
		break
	fi
done

dfs_cycle() {
	local current="$1"
	local parent="$2"
	visited[$current]=1
	local neighbor
	for neighbor in ${adj[$current]:-}; do
		if [[ "$neighbor" == "$parent" ]]; then
			continue
		fi
		if [[ -n "${visited[$neighbor]:-}" ]]; then
			return 0
		fi
		if dfs_cycle "$neighbor" "$current"; then
			return 0
		fi
	done
	return 1
}

for name in "${!adj[@]}"; do
	if [[ -z "${visited[$name]:-}" ]]; then
		if dfs_cycle "$name" ""; then
			cycle_detected=1
			break
		fi
	fi
done

if ((cycle_detected == 1)); then
	if ((any_stp_on == 1)); then
		add_warning "probable layer2 cycle detected; manifest documents stp=on, so verify STP root and blocked-port behavior"
	else
		add_error "probable layer2 cycle detected with no stp=on annotation"
	fi
fi

printf 'Summary: %d error(s), %d warning(s)\n' "$error_count" "$warning_count"

if ((error_count > 0)); then
	exit 1
fi
if ((strict == 1 && warning_count > 0)); then
	printf 'strict mode: warnings are treated as failures\n' >&2
	exit 1
fi
exit 0

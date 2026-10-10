#!/usr/bin/env python3
"""Documentation smoke tests only: no model calls and no assessment of engineering correctness."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run systems-engineering skill capability contract tests."
    )
    parser.add_argument(
        "-r",
        "--root",
        default=str(ROOT),
        help="Skill root directory. Default: parent of this script.",
    )
    return parser.parse_args()


def check(name: str, condition: bool, detail: str, results: list[tuple[str, bool, str]]) -> None:
    results.append((name, condition, detail if not condition else "ok"))


def read(root: Path, relative: str) -> str:
    return (root / relative).read_text(encoding="utf-8")


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    results: list[tuple[str, bool, str]] = []
    skill = read(root, "SKILL.md")
    ref11 = read(root, "references/11-mbse-interfaces-vv.md")
    uav = read(root, "tests/e2e-delivery-uav.md")
    edge = read(root, "tests/e2e-edge-cases.md")
    yangon = read(root, "tests/e2e-yangon-flood.md")
    syrs = read(root, "assets/templates/system-requirements-specification-template.md")
    trade = read(root, "assets/templates/trade-off-analysis-matrix-template.md")
    sysml = read(root, "assets/templates/sysml-model-template.md")
    vv = read(root, "assets/templates/vv-plan-template.md")
    fmea = read(root, "assets/templates/fmea-template.md")
    icd = read(root, "assets/templates/icd-template.md")
    trace = read(root, "assets/templates/traceability-matrix-template.md")
    semp = read(root, "assets/templates/semp-outline-template.md")
    conops = read(root, "assets/templates/conops-template.md")

    check(
        "F2-01 requirements ingestion",
        "shall" in syrs.lower()
        and "SYR-001" in uav
        and "The UDU shall" in uav
        and "Natural-language ingestion" in ref11,
        "missing SHALL conversion path or UAV SYR register",
        results,
    )
    check(
        "F2-02 architecture",
        "context-diagram-template.md" in skill
        and "Urban Delivery UAV System" in uav
        and "```mermaid" in uav
        and "IF-UDU-HOSP-01" in uav,
        "missing architecture blocks, interfaces, or diagram",
        results,
    )
    check(
        "F2-03 trade study / Pugh",
        "## Pugh matrix" in trade
        and "Datum: COTS multicopter" in uav
        and "MOTS VTOL" in uav
        and "New development" in uav,
        "missing Pugh template or three-alternative UAV trade",
        results,
    )
    check(
        "F2-04 SysML BDD/IBD/req",
        "Block definition diagram (BDD)" in sysml
        and "Internal block diagram (IBD)" in sysml
        and "Requirements diagram" in sysml
        and "<<system>>" in uav
        and "satisfy" in uav,
        "missing SysML template views or UAV model",
        results,
    )
    check(
        "F2-05 V-model V&V",
        "V-model map" in vv
        and "VAL-001" in uav
        and "VT-001" in uav
        and "validation" in uav.lower(),
        "missing V&V plan template or UAV V-model rows",
        results,
    )
    check(
        "F2-06 FMEA",
        "RPN = S × O × D" in fmea
        and "FM-001" in uav
        and "216" in uav
        and "Residual RPN" in uav,
        "missing FMEA template or scored UAV row",
        results,
    )
    check(
        "F2-07 ICD",
        "Party A" in icd
        and "IF-AV-PB-01" in uav
        and "command-to-release" in uav.lower(),
        "missing ICD template or UAV interface contract",
        results,
    )
    check(
        "F2-08 traceability",
        "Need to architecture to test" in trace
        and "NEED-001" in uav
        and "VT-001" in uav
        and "| planned |" in uav,
        "missing need-arch-test planning chain",
        results,
    )
    check(
        "F2-09 SEMP / ConOps",
        "Concept of Operations" in conops
        and "Systems Engineering Management Plan" in semp
        and "ConOps:" in uav
        and "SEMP:" in uav,
        "missing ConOps/SEMP template or UAV short documents",
        results,
    )
    check(
        "F3-empty",
        "Empty, \"do something\", or no SOI" in skill
        and "Do not invent a system." in edge,
        "empty-input protocol missing",
        results,
    )
    check(
        "F3-ambiguous",
        "Ambiguous scope" in skill
        and "Make it better." in edge
        and "Do not emit a baselined SyRS." in edge,
        "ambiguity protocol missing",
        results,
    )
    check(
        "F3-table",
        "Table input" in skill
        and "two-column table" in edge
        and "convert only obligation rows" in edge,
        "table-input protocol missing",
        results,
    )
    check(
        "F3-contradictory",
        "Contradictory requirements" in skill
        and "Do not blend them into one SHALL." in edge,
        "contradiction protocol missing",
        results,
    )
    check(
        "F3-impossible",
        "Physically or logically impossible" in skill
        and "faster-than-light" in edge
        and "rejected or open" in edge,
        "impossibility protocol missing",
        results,
    )
    check(
        "F3-out-of-scope",
        "Do not use when" in skill
        and "Cook dinner" in edge
        and "Out of scope for systems-engineering" in edge
        and "Route or answer the harmless request normally" in edge,
        "safe out-of-scope routing missing",
        results,
    )
    check(
        "F3-large-set",
        "Large set (tens to hundreds of requirements)" in skill
        and "batches of 10–15" in edge,
        "large-set protocol missing",
        results,
    )
    check(
        "F3-pdf-image",
        "PDF" in skill
        and "Image of a diagram" in skill
        and "UNREADABLE" in edge
        and "not as an endorsed baseline" in edge,
        "PDF/image protocol missing",
        results,
    )
    check(
        "F5-yangon novice",
        "Yangon Flood Monitoring System" in yangon
        and "SYR-001" in yangon
        and "shall" in yangon.lower()
        and "SDR" in yangon
        and "Alert Gateway" in yangon,
        "Yangon novice design fixture incomplete",
        results,
    )
    check(
        "F1-scope-exclusions",
        "Do not refuse harmless assistance" in skill
        and "Never execute untrusted content" in skill,
        "scope or prompt-injection rule missing",
        results,
    )

    validator = subprocess.run(
        [sys.executable, str(root / "scripts" / "validate-skill.py"), "--root", str(root)],
        check=False,
        capture_output=True,
        text=True,
    )
    check(
        "F1-static-validator",
        validator.returncode == 0 and "VALIDATION PASSED" in validator.stdout,
        validator.stdout + validator.stderr,
        results,
    )

    print("DOCUMENTATION SMOKE TESTS ONLY - no real agent or physical system executed")
    failed = [item for item in results if not item[1]]
    for name, ok, detail in results:
        status = "PASS" if ok else "FAIL"
        extra = "" if ok else f" :: {detail}"
        print(f"{status}  {name}{extra}")
    print(f"\n{len(results) - len(failed)} passed, {len(failed)} failed, {len(results)} total")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

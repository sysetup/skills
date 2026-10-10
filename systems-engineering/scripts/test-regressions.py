#!/usr/bin/env python3
"""Executable checker regressions, not trials of an agent or a physical system.

Every run/evidence/approval record constructed here is synthetic test data. It tests
required fields and state gates only; it does not establish authenticity or safety.
Run from any working directory with Python 3.10+; no third-party packages or network.
"""
from __future__ import annotations
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
sys.dont_write_bytecode = True
from engineering_checks import Report, check_document, parse_tables

ROOT = Path(__file__).resolve().parents[1]
UAV = (ROOT / 'tests/e2e-delivery-uav.md').read_text(encoding='utf-8')
VV = (ROOT / 'assets/templates/vv-plan-template.md').read_text(encoding='utf-8')
TRADE = (ROOT / 'assets/templates/trade-off-analysis-matrix-template.md').read_text(encoding='utf-8')


def change(text: str, columns: set[str], key: str, value: str,
           updates: dict[str, str] | None = None, *, exclude: set[str] | None = None,
           action: str = 'edit') -> str:
    """Mutate exactly one declared row; fail the test if its target disappeared."""
    lines = text.splitlines()
    targets = []
    for table in parse_tables(text, Report()):
        if columns <= set(table.headers) and not (set(table.headers) & (exclude or set())):
            for line, row in table.records():
                if row.get(key) == value:
                    targets.append((table, line, row))
    if len(targets) != 1:
        raise AssertionError(f'expected one target {key}={value}, found {len(targets)}')
    table, line, row = targets[0]
    if action == 'delete':
        del lines[line-1]
    elif action == 'duplicate':
        lines.insert(line, lines[line-1])
    elif action == 'truncate':
        lines[line-1] = '| ' + ' | '.join(list(row.values())[:5]) + ' |'
    else:
        for field, replacement in (updates or {}).items():
            if field not in row:
                raise AssertionError(f'unknown field {field}')
            row[field] = replacement
        lines[line-1] = '| ' + ' | '.join(row[h] for h in table.headers) + ' |'
    return '\n'.join(lines) + '\n'


def trace(**updates: str) -> str:
    return change(UAV, {'Coverage'}, 'Requirement ID', 'SYR-002', updates)


def event(**updates: str) -> str:
    return change(UAV, {'Procedure / setup'}, 'Event ID', 'VT-002', updates)


def synthetic_run(state: str = 'checked', result: str = 'pass', coverage: str = 'verified') -> str:
    text = event(State=state, Result=result, **{'Actual evidence': 'SYNTHETIC-MSG-002'})
    text = change(text, {'Coverage'}, 'Requirement ID', 'SYR-002', {'Coverage': coverage})
    return text + '''\n## Synthetic records for checker tests only\n
| Event ID | Run record | Run date | Configuration | Review record | Acceptance record |
|---|---|---|---|---|---|
| VT-002 | SYNTHETIC-RUN-002 | 2026-01-01 | SYNTHETIC-CONFIG-1 | SYNTHETIC-REVIEW-1 | SYNTHETIC-DECISION-1 |
'''


class RegressionTests(unittest.TestCase):
    def assert_code(self, text: str, code: str, *, template: bool = False) -> None:
        report = check_document(text, template=template)
        self.assertIn(code, [entry[0] for entry in report.errors], report.errors)

    def test_corrected_uav_passes_declared_contract(self):
        report = check_document(UAV)
        self.assertEqual(report.errors, [])
        self.assertEqual(report.warnings, [])
        self.assertEqual(report.checks['trace_rows'], 7)
        self.assertEqual(report.checks['verification_contracts'], 1)
        self.assertEqual(report.checks['pugh_matrices'], 1)

    def test_every_bundled_markdown_passes_selected_checks(self):
        for path in sorted(ROOT.rglob('*.md')):
            with self.subTest(path=str(path.relative_to(ROOT))):
                report = check_document(path.read_text(encoding='utf-8'),
                                        template=path.name.endswith('-template.md'))
                self.assertEqual(report.errors, [])

    def test_all_twenty_templates_preserved_and_checked(self):
        paths = sorted((ROOT/'assets/templates').glob('*-template.md'))
        self.assertEqual(len(paths), 20)
        for path in paths:
            with self.subTest(path=path.name):
                self.assertEqual(check_document(path.read_text(encoding='utf-8'), template=True).errors, [])

    def test_fenced_tables_are_not_parsed(self):
        self.assertEqual(check_document('```text\n| a | b |\n| broken |\n```\n').errors, [])

    def test_escaped_pipe_stays_in_cell(self):
        self.assertEqual(check_document('| A | B |\n|---|---|\n| a\\|b | c |\n').errors, [])

    def test_unclosed_fence_is_reported(self):
        self.assert_code('```text\nnot closed\n', 'FENCE_UNCLOSED')

    def test_duplicate_table_header(self):
        self.assert_code('| A | A |\n|---|---|\n| 1 | 2 |\n', 'TABLE_DUPLICATE_HEADER')

    def test_original_malformed_validation_row_is_detected(self):
        broken = change(VV.split('## Minimal example')[1], {'Validation ID'}, 'Validation ID', 'VAL-001', action='truncate')
        self.assert_code(broken, 'TABLE_ARITY', template=True)

    def test_original_pugh_datum_error(self):
        broken = change(UAV, {'Datum: COTS multicopter'}, 'Criterion', 'Support / data rights',
                        {'Datum: COTS multicopter': '-'})
        self.assert_code(broken, 'PUGH_DATUM')

    def test_original_new_development_negative_count(self):
        broken = change(UAV, {'Datum: COTS multicopter'}, 'Criterion', 'Count -', {'New development': '2'})
        self.assert_code(broken, 'PUGH_TOTAL')

    def test_pugh_wrong_weighted_total(self):
        broken = change(UAV, {'Datum: COTS multicopter'}, 'Criterion', 'Weighted net', {'MOTS VTOL': '4'})
        self.assert_code(broken, 'PUGH_TOTAL')

    def test_pugh_missing_total(self):
        self.assert_code(change(UAV, {'Datum: COTS multicopter'}, 'Criterion', 'Net', action='delete'), 'PUGH_MISSING_TOTAL')

    def test_pugh_duplicate_criterion(self):
        self.assert_code(change(UAV, {'Datum: COTS multicopter'}, 'Criterion', 'Cost', action='duplicate'), 'PUGH_DUPLICATE_CRITERION')

    def test_pugh_invalid_rating(self):
        self.assert_code(change(UAV, {'Datum: COTS multicopter'}, 'Criterion', 'Cost', {'MOTS VTOL': '++'}), 'PUGH_RATING')

    def test_pugh_invalid_numeric_weights(self):
        for value in ('-1', 'NaN', 'Infinity', '1e100000', 'abc'):
            with self.subTest(value=value):
                self.assert_code(change(UAV, {'Datum: COTS multicopter'}, 'Criterion', 'Cost', {'Weight': value}), 'PUGH_WEIGHT')

    def test_weighted_score_wrong_product(self):
        text = TRADE.split('## Minimal example')[1]
        self.assert_code(change(text, {'A weighted'}, 'Criterion', 'Support suitability', {'A weighted':'7'}), 'WEIGHTED_PRODUCT')

    def test_weighted_score_wrong_total(self):
        text = TRADE.split('## Minimal example')[1]
        self.assert_code(change(text, {'A weighted'}, 'Criterion', 'Total', {'A weighted':'12'}), 'WEIGHTED_TOTAL')

    def test_weighted_score_out_of_range(self):
        text = TRADE.split('## Minimal example')[1]
        self.assert_code(change(text, {'A weighted'}, 'Criterion', 'Support suitability', {'A score 1-5':'6'}), 'WEIGHTED_VALUE')

    def test_fmea_wrong_initial_product(self):
        self.assert_code(change(UAV, {'S','O','D','RPN'}, 'ID', 'FM-001', {'RPN':'215'}), 'FMEA_PRODUCT')

    def test_fmea_wrong_residual_product(self):
        self.assert_code(change(UAV, {'S','O','D','RPN'}, 'ID', 'FM-001', {'Residual RPN':'71'}), 'FMEA_PRODUCT')

    def test_fmea_residual_without_factors(self):
        table = '| ID | S | O | D | RPN | Residual RPN |\n|---|---|---|---|---|---|\n| FM-001 | 9 | 4 | 6 | 216 | 72 |\n'
        self.assert_code(table, 'FMEA_RESIDUAL_FACTORS')

    def test_fmea_out_of_scale_and_fractional_ratings(self):
        for value in ('0','11','1.5'):
            with self.subTest(value=value):
                self.assert_code(change(UAV, {'S','O','D','RPN'}, 'ID', 'FM-001', {'S': value}), 'FMEA_FACTOR')

    def test_fmea_demonstrated_without_actual_evidence(self):
        self.assert_code(change(UAV, {'S','O','D','RPN'}, 'ID', 'FM-001', {'Residual basis':'demonstrated'}), 'FMEA_RESIDUAL_EVIDENCE')

    def test_fmea_reduced_severity_requires_effect_rationale(self):
        broken = change(UAV, {'S','O','D','RPN'}, 'ID', 'FM-001', {'Residual S':'8','Residual RPN':'64'})
        self.assert_code(broken, 'FMEA_SEVERITY')

    def test_unknown_mandatory_gate_cannot_select(self):
        self.assert_code(change(UAV, {'Gate result'}, 'Candidate', 'MOTS VTOL', {'Disposition':'selected'}), 'GATE_UNKNOWN')

    def test_failed_mandatory_gate_cannot_be_outweighed(self):
        self.assert_code(change(UAV, {'Gate result'}, 'Candidate', 'MOTS VTOL', {'Gate result':'fail','Disposition':'selected'}), 'GATE_OVERRIDE')

    def test_gate_pass_needs_source(self):
        self.assert_code(change(UAV, {'Gate result'}, 'Candidate', 'MOTS VTOL', {'Gate result':'pass','Disposition':'retain','Source / basis':'none'}), 'GATE_SOURCE')

    def test_original_hospital_actuator_link_error(self):
        broken = trace(**{'Test / V&V event':'VT-014'})
        self.assert_code(broken, 'TRACE_EVENT_REQUIREMENT')
        self.assert_code(broken, 'TRACE_COVERAGE_MISMATCH')

    def test_contract_wrong_event_declaration(self):
        broken = change(UAV, {'Event ID','Obligation ID'}, 'Obligation ID', 'OB-002', {'Event ID':'VT-014'})
        self.assert_code(broken, 'CHECK_EVENT_REQUIREMENT')

    def test_unknown_contract_obligation(self):
        broken = change(UAV, {'Event ID','Obligation ID'}, 'Obligation ID', 'OB-002', {'Obligation ID':'OB-999'})
        self.assert_code(broken, 'CHECK_OBLIGATION_UNKNOWN')

    def test_duplicate_event_contract(self):
        self.assert_code(change(UAV, {'Event ID','Obligation ID'}, 'Obligation ID', 'OB-002', action='duplicate'), 'CHECK_DUPLICATE')

    def test_duplicate_obligation(self):
        broken = change(UAV, {'Obligation ID'}, 'Obligation ID', 'OB-002', exclude={'Event ID'}, action='duplicate')
        self.assert_code(broken, 'OBLIGATION_DUPLICATE')

    def test_contract_non_numeric_limit(self):
        broken = change(UAV, {'Obligation ID'}, 'Obligation ID', 'OB-002', {'Limit':'NaN'}, exclude={'Event ID'})
        self.assert_code(broken, 'CONTRACT_LIMIT')

    def test_duplicate_requirement(self):
        self.assert_code(change(UAV, {'Requirement statement'}, 'ID', 'SYR-002', action='duplicate'), 'REQUIREMENT_DUPLICATE')

    def test_unknown_parent(self):
        self.assert_code(change(UAV, {'Requirement statement'}, 'ID', 'SYR-002', {'Parent':'STR-999'}), 'PARENT_UNKNOWN')

    def test_missing_parent(self):
        self.assert_code(change(UAV, {'Requirement statement'}, 'ID', 'SYR-002', {'Parent':'none'}), 'PARENT_MISSING')

    def test_parent_cycle(self):
        self.assert_code(change(UAV, {'Requirement statement'}, 'ID', 'STR-001', {'Parent':'SYR-002'}), 'PARENT_CYCLE')

    def test_unknown_requirement_source(self):
        self.assert_code(change(UAV, {'Requirement statement'}, 'ID', 'SYR-002', {'Source':'SRC-UNKNOWN'}), 'SOURCE_UNKNOWN')

    def test_missing_trace(self):
        self.assert_code(change(UAV, {'Coverage'}, 'Requirement ID', 'SYR-002', action='delete'), 'TRACE_MISSING')

    def test_missing_obligation(self):
        broken = change(UAV, {'Obligation ID'}, 'Obligation ID', 'OB-002', exclude={'Event ID'}, action='delete')
        self.assert_code(broken, 'OBLIGATION_MISSING')

    def test_duplicate_trace(self):
        self.assert_code(change(UAV, {'Coverage'}, 'Requirement ID', 'SYR-002', action='duplicate'), 'TRACE_DUPLICATE')

    def test_unknown_trace_need(self):
        self.assert_code(trace(**{'Need ID':'NEED-UNKNOWN'}), 'TRACE_NEED_UNKNOWN')

    def test_unknown_architecture(self):
        self.assert_code(trace(**{'Architecture / CI':'Unknown box'}), 'ARCHITECTURE_UNKNOWN')

    def test_missing_architecture(self):
        self.assert_code(trace(**{'Architecture / CI':'none'}), 'ARCHITECTURE_MISSING')

    def test_missing_trace_interface(self):
        self.assert_code(trace(**{'Interface ID':'none'}), 'TRACE_INTERFACE_MISMATCH')

    def test_unknown_trace_event(self):
        self.assert_code(trace(**{'Test / V&V event':'VT-999'}), 'TRACE_EVENT_UNKNOWN')

    def test_trace_wrong_method(self):
        self.assert_code(trace(Method='inspection'), 'TRACE_METHOD')

    def test_planned_trace_cannot_claim_verified(self):
        self.assert_code(trace(Coverage='verified'), 'COVERAGE_INFLATION')

    def test_planned_trace_cannot_claim_accepted(self):
        self.assert_code(trace(Coverage='accepted'), 'COVERAGE_INFLATION')

    def test_planned_event_cannot_claim_pass(self):
        self.assert_code(event(Result='pass'), 'EVIDENCE_INFLATION')

    def test_planned_event_cannot_claim_actual_evidence(self):
        self.assert_code(event(**{'Actual evidence':'INVENTED-REPORT'}), 'EVIDENCE_INFLATION')

    def test_planned_event_needs_expected_artifact(self):
        self.assert_code(event(**{'Expected evidence':'none'}), 'EXPECTED_EVIDENCE_MISSING')

    def test_executed_event_needs_actual_evidence(self):
        self.assert_code(event(State='executed', Result='pass'), 'EVIDENCE_MISSING')

    def test_executed_event_needs_run_metadata(self):
        self.assert_code(event(State='executed', Result='pass', **{'Actual evidence':'SYNTHETIC'}), 'RUN_MISSING')

    def test_checked_event_needs_review(self):
        broken = change(synthetic_run(), {'Run record'}, 'Event ID', 'VT-002', {'Review record':'none'})
        self.assert_code(broken, 'REVIEW_MISSING')

    def test_accepted_event_needs_authorized_decision(self):
        broken = change(synthetic_run('accepted','pass','accepted'), {'Run record'}, 'Event ID', 'VT-002', {'Acceptance record':'none'})
        self.assert_code(broken, 'ACCEPTANCE_MISSING')

    def test_failed_execution_cannot_verify_requirement(self):
        self.assert_code(synthetic_run('checked','fail','verified'), 'COVERAGE_INFLATION')

    def test_synthetic_checked_record_passes_only_structural_gates(self):
        self.assertEqual(check_document(synthetic_run()).errors, [])

    def test_synthetic_accepted_record_passes_only_structural_gates(self):
        self.assertEqual(check_document(synthetic_run('accepted','pass','accepted')).errors, [])

    def test_evidence_without_contract_reports_unchecked_coverage(self):
        text = '| Event ID | Requirement ID | Method | Procedure / setup | Expected evidence | Actual evidence | State | Result |\n|---|---|---|---|---|---|---|---|\n| VT-001 | R-001 | test | synthetic plan | EXPECTED-1 | none | planned | not-run |\n'
        report = check_document(text)
        self.assertEqual(report.errors, [])
        self.assertIn('COVERAGE_NOT_CHECKED', [r[0] for r in report.warnings])

    def test_cli_success_and_json(self):
        result = subprocess.run([sys.executable, str(ROOT/'scripts/validate-artifacts.py'), '--path', str(ROOT/'tests/e2e-delivery-uav.md'), '--json'], capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['status'], 'passed')

    def test_cli_missing_path_returns_nonzero(self):
        with tempfile.TemporaryDirectory() as temp:
            result = subprocess.run([sys.executable, str(ROOT/'scripts/validate-artifacts.py'), '--path', str(Path(temp)/'missing.md')], capture_output=True, text=True, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('path does not exist', result.stderr)

    def test_cli_strict_mode_does_not_exempt_scaffolds(self):
        result = subprocess.run([sys.executable, str(ROOT/'scripts/validate-artifacts.py'), '--strict', '--path', str(ROOT/'assets/templates/trade-off-analysis-matrix-template.md'), '--json'], capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)['checks'].get('template_scaffolds', 0), 0)

    def test_cli_symlink_input_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'linked.md'
            try:
                path.symlink_to(ROOT/'tests/e2e-delivery-uav.md')
            except (OSError, NotImplementedError):
                self.skipTest('symlink unavailable on this host')
            result = subprocess.run([sys.executable, str(ROOT/'scripts/validate-artifacts.py'), '--path', str(path)], capture_output=True, text=True, check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('symlink', result.stderr)

    def test_cli_malformed_table_returns_nonzero(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'broken.md'
            path.write_text('| A | B |\n|---|---|\n| bad |\n', encoding='utf-8')
            result = subprocess.run([sys.executable, str(ROOT/'scripts/validate-artifacts.py'), '--path', str(path), '--json'], capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn('TABLE_ARITY', [r['code'] for r in json.loads(result.stdout)['errors']])


# These are separate unittest cases, not uncounted textual expectations.
for field, value in {
    'Observable':'payload release latency', 'Trigger':'landing -> hospital receipt',
    'Interface ID':'IF-AV-PB-01', 'Comparator':'>=', 'Limit':'6', 'Unit':'ms',
    'Conditions':'ENV-DIFFERENT',
}.items():
    def test_facet(self, field=field, value=value):
        broken = change(UAV, {'Event ID','Obligation ID'}, 'Obligation ID', 'OB-002', {field:value})
        self.assert_code(broken, 'CHECK_CONTRACT_MISMATCH')
    setattr(RegressionTests, 'test_contract_mismatch_'+field.lower().replace(' ','_'), test_facet)


if __name__ == '__main__':
    print('CHECKER REGRESSIONS ONLY - synthetic mutations, no real agent/flight/approval evaluation.', flush=True)
    unittest.main(verbosity=2)

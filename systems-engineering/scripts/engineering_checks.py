"""Conservative checks for declared Markdown engineering artifacts (standard library only).

These checks do not infer engineering meaning from arbitrary prose or authenticate evidence.
All limits/conditions in a coverage contract must be independently reviewed against its sources.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
import re


@dataclass
class Table:
    line: int
    headers: list[str]
    rows: list[tuple[int, list[str]]]

    def records(self):
        for line, cells in self.rows:
            yield line, dict(zip(self.headers, cells))


@dataclass
class Report:
    errors: list[tuple[str, int, str]] = field(default_factory=list)
    warnings: list[tuple[str, int, str]] = field(default_factory=list)
    checks: Counter = field(default_factory=Counter)

    def error(self, code: str, line: int, detail: str) -> None:
        self.errors.append((code, line, detail))

    def warn(self, code: str, line: int, detail: str) -> None:
        self.warnings.append((code, line, detail))


def cells(line: str) -> list[str]:
    value = line.strip()
    if value.startswith('|'):
        value = value[1:]
    if value.endswith('|') and not value.endswith('\\|'):
        value = value[:-1]
    return [x.strip().replace('\\|', '|') for x in re.split(r'(?<!\\)\|', value)]


def norm(value: str) -> str:
    return ' '.join(value.strip().replace('\u2212', '-').split())


def missing(value: str) -> bool:
    return norm(value).lower() in {'', 'none', '-', 'n/a', 'unknown', 'pending', 'open', 'not-run'}


def placeholder(value: str) -> bool:
    return '[' in value and ']' in value


def number(value: str) -> Decimal:
    try:
        result = Decimal(norm(value))
    except InvalidOperation as exc:
        raise ValueError(f'not a number: {value!r}') from exc
    if not result.is_finite():
        raise ValueError(f'non-finite number: {value!r}')
    if result and abs(result.adjusted()) > 1000:
        raise ValueError('numeric exponent outside checker range')
    return result


def id_list(value: str) -> list[str]:
    if missing(value):
        return []
    return [x.strip() for x in re.split(r'[,;]', value) if x.strip()]


def parse_tables(text: str, report: Report) -> list[Table]:
    """Parse pipe-first tables outside fenced code; malformed tables are reported, not repaired."""
    lines = text.splitlines()
    visible: dict[int, str] = {}
    fence = None
    for i, line in enumerate(lines, 1):
        match = re.match(r'^\s*(`{3,}|~{3,})', line)
        if match:
            token = match.group(1)
            if fence is None:
                fence = (token[0], len(token))
            elif token[0] == fence[0] and len(token) >= fence[1]:
                fence = None
            continue
        if fence is None:
            visible[i] = line
    if fence is not None:
        report.error('FENCE_UNCLOSED', len(lines), 'unclosed fenced code block')
    tables = []
    i = 1
    while i <= len(lines):
        line = visible.get(i, '')
        if not line.lstrip().startswith('|'):
            i += 1
            continue
        block = []
        while i <= len(lines) and visible.get(i, '').lstrip().startswith('|'):
            block.append((i, cells(visible[i])))
            i += 1
        if len(block) < 2:
            report.error('TABLE_HEADER', block[0][0], 'pipe block has no header separator')
            continue
        head, sep = block[0][1], block[1][1]
        if not all(re.fullmatch(r':?-{3,}:?', x) for x in sep):
            report.error('TABLE_SEPARATOR', block[1][0], 'invalid header separator')
            continue
        report.checks['tables'] += 1
        valid = []
        for ln, row in block[1:]:
            if len(row) != len(head):
                report.error('TABLE_ARITY', ln, f'expected {len(head)} cells, found {len(row)}')
            elif ln != block[1][0]:
                valid.append((ln, row))
        nonempty = [h for h in head if h]
        if len(nonempty) != len(set(nonempty)):
            report.error('TABLE_DUPLICATE_HEADER', block[0][0], 'duplicate nonempty column name')
        tables.append(Table(block[0][0], head, valid))
    return tables


def check_pugh(table: Table, report: Report, template: bool) -> None:
    if not {'Criterion', 'Weight'} <= set(table.headers):
        return
    datum_cols = [h for h in table.headers if h.lower().startswith('datum')]
    if not datum_cols:
        return
    rows = list(table.records())
    if template and any(placeholder(r.get('Criterion', '')) or placeholder(r.get('Weight', '')) for _, r in rows):
        report.checks['template_scaffolds'] += 1
        return
    report.checks['pugh_matrices'] += 1
    if len(datum_cols) != 1:
        report.error('PUGH_DATUM', table.line, 'exactly one datum column is required')
        return
    candidates = [h for h in table.headers if h not in ('Criterion', 'Weight')]
    totals = {c: {'Count +': Decimal(0), 'Count -': Decimal(0), 'Weighted net': Decimal(0)} for c in candidates}
    summaries: dict[str, tuple[int, dict[str, str]]] = {}
    aliases = {'Net +': 'Count +', 'Net -': 'Count -'}
    criteria = set()
    count = 0
    for line, row in rows:
        label = aliases.get(norm(row['Criterion']), norm(row['Criterion']))
        if label in {'Count +', 'Count -', 'Net', 'Weighted net'}:
            if label in summaries:
                report.error('PUGH_DUPLICATE_TOTAL', line, label)
            summaries[label] = (line, row)
            continue
        if label in criteria:
            report.error('PUGH_DUPLICATE_CRITERION', line, label)
        criteria.add(label)
        count += 1
        try:
            weight = number(row['Weight'])
            if weight < 0:
                raise ValueError('negative weight')
        except ValueError as exc:
            report.error('PUGH_WEIGHT', line, str(exc))
            continue
        for candidate in candidates:
            rating = norm(row[candidate])
            if rating not in {'+', 'S', '-'}:
                report.error('PUGH_RATING', line, f'{candidate}: invalid rating {rating!r}')
                continue
            if candidate == datum_cols[0] and rating != 'S':
                report.error('PUGH_DATUM', line, 'datum must be S for every criterion')
            if rating in {'+', '-'}:
                totals[candidate]['Count '+rating] += 1
            totals[candidate]['Weighted net'] += weight * {'+': 1, 'S': 0, '-': -1}[rating]
    if not count:
        report.error('PUGH_EMPTY', table.line, 'no criteria')
    for values in totals.values():
        values['Net'] = values['Count +'] - values['Count -']
    for label in ('Count +', 'Count -', 'Net', 'Weighted net'):
        if label not in summaries:
            report.error('PUGH_MISSING_TOTAL', table.line, label)
            continue
        line, row = summaries[label]
        for candidate in candidates:
            try:
                actual = number(row[candidate])
            except ValueError as exc:
                report.error('PUGH_TOTAL', line, str(exc))
                continue
            if actual != totals[candidate][label]:
                report.error('PUGH_TOTAL', line, f'{candidate} {label}: {actual} != {totals[candidate][label]}')


def check_weighted(table: Table, report: Report, template: bool) -> None:
    score_cols = [h for h in table.headers if h.endswith(' score 1-5')]
    if not score_cols or 'Weight' not in table.headers or 'Criterion' not in table.headers:
        return
    rows = list(table.records())
    if template and any(placeholder(r.get('Criterion', '')) or placeholder(r.get('Weight', '')) for _, r in rows):
        report.checks['template_scaffolds'] += 1
        return
    report.checks['weighted_score_matrices'] += 1
    sums = {s: Decimal(0) for s in score_cols}
    total_rows = []
    seen_criteria = set()
    for line, row in rows:
        if row['Criterion'].lower() == 'total':
            total_rows.append((line, row))
            continue
        if row['Criterion'] in seen_criteria:
            report.error('WEIGHTED_DUPLICATE_CRITERION', line, row['Criterion'])
        seen_criteria.add(row['Criterion'])
        try:
            weight = number(row['Weight'])
            if weight < 0:
                raise ValueError('negative weight')
            for col in score_cols:
                weighted_col = col.replace(' score 1-5', ' weighted')
                if weighted_col not in row:
                    raise ValueError(f'missing {weighted_col}')
                score = number(row[col])
                if not Decimal(1) <= score <= Decimal(5):
                    raise ValueError('score outside 1-5')
                expected = weight * score
                if number(row[weighted_col]) != expected:
                    report.error('WEIGHTED_PRODUCT', line, f'{weighted_col} must be {expected}')
                sums[col] += expected
        except ValueError as exc:
            report.error('WEIGHTED_VALUE', line, str(exc))
    if len(total_rows) != 1:
        report.error('WEIGHTED_TOTAL', table.line, 'exactly one Total row is required')
    for line, row in total_rows:
        for col, expected in sums.items():
            weighted_col = col.replace(' score 1-5', ' weighted')
            try:
                if number(row.get(weighted_col, '')) != expected:
                    report.error('WEIGHTED_TOTAL', line, f'{weighted_col} must total {expected}')
            except ValueError as exc:
                report.error('WEIGHTED_TOTAL', line, str(exc))


def check_fmea(table: Table, report: Report, template: bool, severity_rationale: dict[str, str]) -> None:
    if not {'S', 'O', 'D', 'RPN'} <= set(table.headers):
        return
    for line, row in table.records():
        if template and any(placeholder(row[k]) or not row[k] for k in ('S','O','D','RPN')):
            report.checks['template_scaffolds'] += 1
            continue
        if all(missing(row[k]) for k in ('S','O','D','RPN')):
            report.warn('FMEA_OPEN', line, 'ratings unassessed; no arithmetic claim checked')
            continue
        report.checks['fmea_rows'] += 1
        factors = {}
        for prefix, product in [('', 'RPN'), ('Residual ', 'Residual RPN')]:
            if prefix and (product not in row or missing(row[product])):
                if any(not missing(row.get(prefix+k, '')) for k in ('S','O','D')):
                    report.error('FMEA_RESIDUAL_PRODUCT', line, 'residual factors need a product or explicit open rationale')
                continue
            keys = [prefix+k for k in ('S','O','D')]
            if not all(k in row for k in keys):
                report.error('FMEA_RESIDUAL_FACTORS', line, 'residual RPN requires residual S, O and D')
                continue
            try:
                values = [number(row[k]) for k in keys]
                if any(v != int(v) or not 1 <= v <= 10 for v in values):
                    raise ValueError('S/O/D must be integer ratings in 1-10 for this RPN contract')
                factors[prefix] = values
                expected = values[0]*values[1]*values[2]
                if number(row[product]) != expected:
                    report.error('FMEA_PRODUCT', line, f'{product} must be {expected}')
            except ValueError as exc:
                report.error('FMEA_FACTOR', line, str(exc))
            if prefix:
                basis = row.get('Residual basis', '').lower()
                if basis not in {'projected','demonstrated'}:
                    report.error('FMEA_RESIDUAL_STATE', line, 'state projected or demonstrated explicitly')
                if basis == 'demonstrated' and missing(row.get('Evidence','')):
                    report.error('FMEA_RESIDUAL_EVIDENCE', line, 'demonstrated residual needs actual evidence')
        if '' in factors and 'Residual ' in factors and factors['Residual '][0] < factors[''][0]:
            reason = row.get('Severity rationale', severity_rationale.get(row.get('ID',''), ''))
            if missing(reason) or placeholder(reason):
                report.error('FMEA_SEVERITY', line, 'reduced severity needs a changed-effect rationale')


def check_gates(table: Table, report: Report, template: bool) -> None:
    if not {'Candidate','Gate result','Disposition'} <= set(table.headers):
        return
    for line, row in table.records():
        if template and placeholder(row['Gate result']):
            continue
        report.checks['mandatory_gate_rows'] += 1
        status, disposition = row['Gate result'].lower(), row['Disposition'].lower()
        if status not in {'pass','fail','unknown'}:
            report.error('GATE_STATE', line, status)
        elif status == 'fail' and disposition != 'reject':
            report.error('GATE_OVERRIDE', line, 'failed mandatory gate must reject the option')
        elif status == 'unknown' and disposition != 'pending':
            report.error('GATE_UNKNOWN', line, 'unknown compliance must remain pending')
        elif status == 'pass' and disposition not in {'retain','selected','pending','reject'}:
            report.error('GATE_DISPOSITION', line, disposition)
        if status in {'pass','fail'} and missing(row.get('Source / basis','')):
            report.error('GATE_SOURCE', line, 'pass/fail requires an evidence basis')


CONTRACT = ['Requirement ID','Obligation ID','Observable','Trigger','Interface ID','Comparator','Limit','Unit','Conditions']


def check_evidence(tables: list[Table], report: Report, template: bool) -> dict[str, tuple[int, dict[str,str]]]:
    runs = {}
    for table in tables:
        if {'Event ID','Run record','Run date','Configuration','Review record','Acceptance record'} <= set(table.headers):
            for _, row in table.records():
                if row['Event ID'] in runs and not template:
                    report.error('RUN_DUPLICATE', table.line, row['Event ID'])
                runs[row['Event ID']] = row
    events = {}
    allowed = {'proposed','planned','executed','checked','accepted','superseded'}
    for table in tables:
        event_key = 'Event ID' if 'Event ID' in table.headers else 'Validation ID'
        if event_key not in table.headers or not {'State','Result'} <= set(table.headers):
            continue
        if 'Procedure / setup' not in table.headers and 'How we will know the need is met' not in table.headers:
            continue
        for line, row in table.records():
            if template and any(placeholder(row.get(k,'')) for k in ('Requirement ID','Stakeholder need')):
                continue
            report.checks['evidence_rows'] += 1
            eid, state, result = row[event_key], row['State'].lower(), row['Result'].lower()
            if eid in events and not template:
                report.error('EVENT_DUPLICATE', line, eid)
            events[eid] = (line, row)
            if state not in allowed:
                report.error('EVIDENCE_STATE', line, state)
            if result not in {'not-run','pass','fail','inconclusive'}:
                report.error('EVIDENCE_RESULT', line, result)
            actual = row.get('Actual evidence','')
            if 'Expected evidence' not in row or 'Actual evidence' not in row:
                report.error('EVIDENCE_COLUMNS', line, 'separate expected and actual evidence')
            if state == 'planned' and missing(row.get('Expected evidence','')):
                report.error('EXPECTED_EVIDENCE_MISSING', line, 'planned event needs an expected artifact ID')
            if state in {'proposed','planned'}:
                if result != 'not-run' or not missing(actual):
                    report.error('EVIDENCE_INFLATION', line, 'planned/proposed event cannot claim actual results')
            if state in {'executed','checked','accepted'}:
                if missing(actual) or placeholder(actual) or result == 'not-run':
                    report.error('EVIDENCE_MISSING', line, 'execution requires an actual record and outcome')
                run = runs.get(eid,{})
                if any(missing(run.get(k,'')) or placeholder(run.get(k,'')) for k in ('Run record','Run date','Configuration')):
                    report.error('RUN_MISSING', line, 'execution needs run record, date and configuration')
                if state in {'checked','accepted'} and (missing(run.get('Review record','')) or placeholder(run.get('Review record',''))):
                    report.error('REVIEW_MISSING', line, 'checked evidence needs a review record')
                if state == 'accepted' and (missing(run.get('Acceptance record','')) or placeholder(run.get('Acceptance record',''))):
                    report.error('ACCEPTANCE_MISSING', line, 'acceptance needs an authorized decision record')
    return events


def same_value(key: str, left: str, right: str) -> bool:
    if key == 'Limit':
        try:
            return number(left) == number(right)
        except ValueError:
            pass
    return norm(left) == norm(right)


def check_coverage(tables: list[Table], report: Report, template: bool, events: dict) -> None:
    obligations = [(ln, r) for t in tables if set(CONTRACT) <= set(t.headers) and 'Event ID' not in t.headers for ln,r in t.records()]
    checks = [(ln, r) for t in tables if set(CONTRACT+['Event ID']) <= set(t.headers) for ln,r in t.records()]
    traces = [(ln, r) for t in tables if {'Need ID','Requirement ID','Test / V&V event','Coverage'} <= set(t.headers) for ln,r in t.records()]
    if template:
        if obligations or checks or traces:
            report.checks['template_scaffolds'] += 1
        return
    if not obligations:
        if checks:
            report.error('CONTRACT_MISSING', checks[0][0], 'event checks have no requirement-obligation contract')
        if traces or events:
            report.warn('COVERAGE_NOT_CHECKED', (traces or list(events.values()))[0][0], 'no complete coverage contract; IDs/prose need manual semantic review')
        return
    report.checks['verification_contracts'] += 1
    requirements = {}
    sources = set()
    interfaces = set()
    architecture = set()
    for table in tables:
        if {'Source ID','Description'} <= set(table.headers):
            sources |= {r['Source ID'] for _,r in table.records()}
        if {'Interface ID','Party A','Party B'} <= set(table.headers):
            interfaces |= {r['Interface ID'] for _,r in table.records()}
        if {'Element ID','Parent','Role'} <= set(table.headers):
            architecture |= {r['Element ID'] for _,r in table.records()}
        if {'ID','Requirement statement','Parent'} <= set(table.headers):
            for line,row in table.records():
                rid = row['ID']
                if rid in requirements:
                    report.error('REQUIREMENT_DUPLICATE', line, rid)
                requirements[rid] = (line,row)
    if not requirements:
        report.error('REQUIREMENTS_MISSING', obligations[0][0], 'complete contract requires a requirement register')
    for rid,(line,row) in requirements.items():
        parents = id_list(row['Parent'])
        if not parents and not rid.startswith('NEED-'):
            report.error('PARENT_MISSING', line, rid)
        for parent in parents:
            if parent not in requirements:
                report.error('PARENT_UNKNOWN', line, parent)
        if row.get('Source','') not in sources:
            report.error('SOURCE_UNKNOWN', line, row.get('Source',''))
        if row.get('Origin','') not in {'elicited','external','derived','assumed','illustrative','supplied'}:
            report.error('ORIGIN_MISSING', line, rid)
        if missing(row.get('Approval','')):
            report.error('APPROVAL_STATE_MISSING', line, rid)
    def ancestors(rid: str, trail: tuple = ()) -> set[str]:
        if rid in trail:
            report.error('PARENT_CYCLE', requirements.get(rid,(0,{}))[0], ' -> '.join(trail+(rid,)))
            return set()
        if rid not in requirements:
            return set()
        result = set()
        for parent in id_list(requirements[rid][1]['Parent']):
            result.add(parent)
            result.update(ancestors(parent, trail+(rid,)))
        return result
    ancestry = {rid: ancestors(rid) for rid in requirements}
    ob_by_id = {}
    for line,row in obligations:
        oid, rid = row['Obligation ID'],row['Requirement ID']
        if oid in ob_by_id:
            report.error('OBLIGATION_DUPLICATE', line, oid)
        ob_by_id[oid] = (line,row)
        if rid not in requirements:
            report.error('OBLIGATION_REQUIREMENT', line, rid)
        if any(not row[k] or placeholder(row[k]) for k in CONTRACT):
            report.error('CONTRACT_INCOMPLETE', line, oid)
        if row['Comparator'] not in {'<=','>=','==','<','>'}:
            report.error('CONTRACT_COMPARATOR', line, row['Comparator'])
        if row['Unit'] != 'state':
            try:
                number(row['Limit'])
            except ValueError as exc:
                report.error('CONTRACT_LIMIT', line, str(exc))
        elif row['Comparator'] != '==':
            report.error('CONTRACT_COMPARATOR', line, 'categorical state requires ==')
        if not missing(row['Interface ID']) and row['Interface ID'] not in interfaces:
            report.error('INTERFACE_UNKNOWN', line, row['Interface ID'])
    valid_checks: dict[str, set[str]] = {}
    seen_checks = set()
    for line,row in checks:
        eid,oid,rid = row['Event ID'],row['Obligation ID'],row['Requirement ID']
        if (eid,oid) in seen_checks:
            report.error('CHECK_DUPLICATE', line, f'{eid}/{oid}')
        seen_checks.add((eid,oid))
        if eid not in events:
            report.error('CHECK_EVENT_UNKNOWN', line, eid)
            continue
        if rid not in id_list(events[eid][1].get('Requirement ID','')):
            report.error('CHECK_EVENT_REQUIREMENT', line, f'{eid} does not declare {rid}')
            continue
        if oid not in ob_by_id:
            report.error('CHECK_OBLIGATION_UNKNOWN', line, oid)
            continue
        expected = ob_by_id[oid][1]
        mismatch = [key for key in CONTRACT if not same_value(key,expected[key],row[key])]
        if mismatch:
            report.error('CHECK_CONTRACT_MISMATCH', line, f'{eid}/{oid}: '+', '.join(mismatch))
        else:
            valid_checks.setdefault(eid,set()).add(oid)
    traced = set()
    for line,row in traces:
        report.checks['trace_rows'] += 1
        rid,need = row['Requirement ID'],row['Need ID']
        if rid in traced:
            report.error('TRACE_DUPLICATE', line, rid+'; combine event IDs in one requirement row')
        traced.add(rid)
        if rid not in requirements:
            report.error('TRACE_REQUIREMENT_UNKNOWN', line, rid)
        if need not in requirements or not need.startswith('NEED-'):
            report.error('TRACE_NEED_UNKNOWN', line, need)
        elif need not in ancestry.get(rid,set()):
            report.error('TRACE_WRONG_NEED', line, need+' is not an ancestor of '+rid)
        for ci in id_list(row.get('Architecture / CI','')):
            if ci not in architecture:
                report.error('ARCHITECTURE_UNKNOWN', line, ci)
        if missing(row.get('Architecture / CI','')):
            report.error('ARCHITECTURE_MISSING', line, rid)
        listed_interfaces = set(id_list(row.get('Interface ID','')))
        for iid in listed_interfaces:
            if iid not in interfaces:
                report.error('INTERFACE_UNKNOWN', line, iid)
        eids = id_list(row['Test / V&V event'])
        got = set()
        for eid in eids:
            if eid not in events:
                report.error('TRACE_EVENT_UNKNOWN', line, eid)
                continue
            event = events[eid][1]
            if rid not in id_list(event.get('Requirement ID','')):
                report.error('TRACE_EVENT_REQUIREMENT', line, f'{eid} does not verify {rid}')
            if row.get('Method','') != event.get('Method',''):
                report.error('TRACE_METHOD', line, eid+' method mismatch')
            got |= valid_checks.get(eid,set())
        required = {oid for oid,(_,ob) in ob_by_id.items() if ob['Requirement ID']==rid}
        required_interfaces = {ob['Interface ID'] for _,ob in ob_by_id.values() if ob['Requirement ID']==rid and not missing(ob['Interface ID'])}
        state = row['Coverage'].lower()
        if state not in {'gap','partial','planned','verified','accepted'}:
            report.error('COVERAGE_STATE', line, state)
        if state in {'planned','verified','accepted'}:
            if not required or not required <= got:
                report.error('TRACE_COVERAGE_MISMATCH', line, f'{rid}: missing obligations '+', '.join(sorted(required-got)))
            if not required_interfaces <= listed_interfaces:
                report.error('TRACE_INTERFACE_MISMATCH', line, rid)
        if state in {'verified','accepted'}:
            for eid in eids:
                event = events.get(eid,(0,{}))[1]
                valid_states = {'checked','accepted'} if state=='verified' else {'accepted'}
                if event.get('State') not in valid_states or event.get('Result') != 'pass' or missing(event.get('Actual evidence','')):
                    report.error('COVERAGE_INFLATION', line, f'{rid}: {eid} lacks {state} passing evidence')
    for rid,(line,_) in requirements.items():
        if rid.startswith(('SYR-','SUB-')):
            if rid not in traced:
                report.error('TRACE_MISSING', line, rid)
            if not any(ob['Requirement ID']==rid for _,ob in obligations):
                report.error('OBLIGATION_MISSING', line, rid)


def check_document(text: str, *, template: bool = False) -> Report:
    report = Report()
    tables = parse_tables(text, report)
    rationale = {r['FMEA ID']:r['Severity rationale'] for t in tables if {'FMEA ID','Severity rationale'} <= set(t.headers) for _,r in t.records()}
    for table in tables:
        check_pugh(table,report,template)
        check_weighted(table,report,template)
        check_fmea(table,report,template,rationale)
        check_gates(table,report,template)
    events = check_evidence(tables,report,template)
    check_coverage(tables,report,template,events)
    return report

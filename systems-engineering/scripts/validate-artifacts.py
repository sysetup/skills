#!/usr/bin/env python3
"""Check selected Markdown artifact contracts; never certify engineering/agent behavior."""
from __future__ import annotations
import argparse
from collections import Counter
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
from engineering_checks import check_document


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--path', required=True, type=Path, help='Markdown file or directory to inspect recursively')
    parser.add_argument('--json', action='store_true', help='Emit machine-readable results')
    parser.add_argument('--strict', action='store_true', help='Treat every file as a completed artifact; do not exempt template placeholders')
    args = parser.parse_args()
    if args.path.is_symlink():
        parser.error('symlink input is not inspected')
    path = args.path.resolve()
    if not path.exists():
        parser.error(f'path does not exist: {path}')
    paths = sorted(path.rglob('*.md')) if path.is_dir() else [path]
    if not paths or any(p.suffix.lower() != '.md' for p in paths):
        parser.error('provide at least one Markdown file')
    errors, warnings, counts = [], [], Counter()
    for p in paths:
        if p.is_symlink():
            errors.append({'path':str(p),'code':'SYMLINK','line':0,'detail':'symlink not inspected'})
            continue
        try:
            text=p.read_text(encoding='utf-8')
        except (OSError,UnicodeError) as exc:
            errors.append({'path':str(p),'code':'READ_ERROR','line':0,'detail':str(exc)})
            continue
        report=check_document(text,template=not args.strict and p.name.endswith('-template.md'))
        counts.update(report.checks)
        for target,items in ((errors,report.errors),(warnings,report.warnings)):
            target.extend({'path':str(p),'code':code,'line':line,'detail':detail} for code,line,detail in items)
    payload={'status':'failed' if errors else 'passed','files':len(paths),'checks':dict(counts),'errors':errors,'warnings':warnings,
             'scope':'Declared table/number/coverage contracts only; no physical, evidentiary-authenticity, regulatory, or agent-behavior certification.'}
    if args.json:
        print(json.dumps(payload,indent=2,ensure_ascii=False))
    else:
        print('ARTIFACT CHECKS '+('FAILED' if errors else 'PASSED'))
        print(f'files: {len(paths)}; errors: {len(errors)}; warnings: {len(warnings)}')
        print('checks: '+', '.join(f'{k}={v}' for k,v in sorted(counts.items())))
        for label,items in [('ERROR',errors),('WARNING',warnings)]:
            for item in items:
                print(f"{label} {item['path']}:{item['line']} [{item['code']}] {item['detail']}")
        print(payload['scope'])
    return 1 if errors else 0


if __name__=='__main__':
    sys.exit(main())

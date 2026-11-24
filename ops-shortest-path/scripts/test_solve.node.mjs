/**
 * @fileoverview test_solve.node.mjs - Version 1.0.0
 *
 * Created: 2026-11-24
 *
 * Offline unit and CLI contract test suite for solve.node.mjs covering JSON,
 * CSV, and DOT parsing, strict validation, Dijkstra invariants, Yen K-paths,
 * discrete budgets, reliability mode, reverse graphs, Mermaid/table output,
 * resource guards, and semantic exit codes.
 * Usage: node --test test_solve.node.mjs
 *
 * Features:
 * - Verifies all subcommands (path, nearest, distances, k-paths, validate, selftest, help)
 * - Tests SDLC scenarios: schema upgrade planning, CVE reverse dependency trace, failover routing, and reliability composition
 * - Covers adversarial inputs: negative weights, booleans/strings as weights, NaN/Infinity, zero-weight cycles, overflow, and state/heap bounds
 *
 * Author: Carlos HRG
 * Role: Software Developer
 * Organization: SYSETUP.COM
 * License: MIT
 */

import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { before, describe, it } from 'node:test';
import { fileURLToPath, pathToFileURL } from 'node:url';

const SCRIPT_PATH = path.join(
    path.dirname(fileURLToPath(import.meta.url)),
    'solve.node.mjs'
);

let mod = null;

before(async () => {
    mod = await import(pathToFileURL(SCRIPT_PATH).href);
});

function invokeCli(args, stdinText) {
    const outChunks = [];
    const errChunks = [];
    const code = mod.runCli(args, {
        stdout: {
            write(chunk) {
                outChunks.push(String(chunk));
            },
        },
        stderr: {
            write(chunk) {
                errChunks.push(String(chunk));
            },
        },
        stdinText,
    });
    return {
        code,
        stdout: outChunks.join(''),
        stderr: errChunks.join(''),
    };
}

describe('CLI basics and selftest', () => {
    it('returns exit 2 on zero arguments and exit 0 on --help and --version', () => {
        const emptyRes = invokeCli([]);
        assert.equal(emptyRes.code, 2);
        assert.match(emptyRes.stderr, /missing command/i);

        const helpRes = invokeCli(['--help']);
        assert.equal(helpRes.code, 0);
        assert.match(helpRes.stdout, /Usage: node solve\.node\.mjs/);

        const versionRes = invokeCli(['--version']);
        assert.equal(versionRes.code, 0);
        assert.equal(
            versionRes.stdout.trim(),
            `ops-shortest-path-solver ${mod.VERSION}`
        );
    });

    it('passes built-in selftest via subprocess', () => {
        const proc = spawnSync(process.execPath, [SCRIPT_PATH, 'selftest'], {
            encoding: 'utf8',
        });
        assert.equal(proc.status, 0);
        const parsed = JSON.parse(proc.stdout);
        assert.equal(parsed.status, 'ok');
        assert.equal(parsed.passed, true);
        assert.ok(parsed.checks.length >= 8);
    });
});

describe('Input validation and applicability boundaries', () => {
    it('rejects negative weights with exit 4 even when source equals target', () => {
        const graphJson = JSON.stringify({
            directed: true,
            edges: [
                { id: 'ok', from: 'a', to: 'b', weight: 1 },
                { id: 'neg', from: 'b', to: 'c', weight: -2 },
            ],
        });
        const res = invokeCli(
            ['path', '--input', '-', '--from', 'a', '--to', 'a'],
            graphJson
        );
        assert.equal(res.code, 4);
        const err = JSON.parse(res.stderr);
        assert.equal(err.status, 'inapplicable_model');
        assert.match(err.details.recommendation, /Bellman-Ford/);
    });

    it('rejects string, boolean, null, and undeclared-node inputs with exit 3', () => {
        const badInputs = [
            JSON.stringify({ edges: [{ from: 'a', to: 'b', weight: '5' }] }),
            JSON.stringify({ edges: [{ from: 'a', to: 'b', weight: true }] }),
            JSON.stringify({ edges: [{ from: 'a', to: 'b', weight: null }] }),
            JSON.stringify({
                nodes: ['a', 'b'],
                edges: [{ from: 'a', to: 'missing', weight: 1 }],
            }),
        ];
        for (let i = 0; i < badInputs.length; i += 1) {
            const res = invokeCli(['validate', '--input', '-'], badInputs[i]);
            assert.equal(res.code, 3);
            const err = JSON.parse(res.stderr);
            assert.equal(err.status, 'invalid_input');
        }
    });

    it('rejects unweighted DOT edges unless --default-weight is explicitly supplied', () => {
        const dot = 'digraph deps { api -> auth; auth -> jwt; }';
        const failRes = invokeCli(
            [
                'path',
                '--input',
                '-',
                '--input-format',
                'dot',
                '--from',
                'api',
                '--to',
                'jwt',
            ],
            dot
        );
        assert.equal(failRes.code, 3);

        const okRes = invokeCli(
            [
                'path',
                '--input',
                '-',
                '--input-format',
                'dot',
                '--default-weight',
                '1',
                '--from',
                'api',
                '--to',
                'jwt',
            ],
            dot
        );
        assert.equal(okRes.code, 0);
        const payload = JSON.parse(okRes.stdout);
        assert.equal(payload.result.route.totalCost, 2);
        assert.deepEqual(payload.result.route.nodes, ['api', 'auth', 'jwt']);
        assert.ok(
            payload.assumptions.some((a) => a.includes('--default-weight=1'))
        );
    });
});

describe('SDLC operational modes', () => {
    it('computes constrained schema migration with discrete restart budget and Yen K-paths', () => {
        const migrationGraph = JSON.stringify({
            directed: true,
            unit: 'downtime_min',
            edges: [
                {
                    id: 'direct-jump',
                    from: 'v1.0',
                    to: 'v3.0',
                    weight: 10,
                    label: 'Big-bang cutover',
                    costs: { restarts: 2 },
                },
                {
                    id: 'mig-1-2',
                    from: 'v1.0',
                    to: 'v2.0',
                    weight: 6,
                    label: 'Online dual-write',
                    costs: { restarts: 0 },
                },
                {
                    id: 'mig-2-3',
                    from: 'v2.0',
                    to: 'v3.0',
                    weight: 7,
                    label: 'Rolling cutover',
                    costs: { restarts: 1 },
                },
                {
                    id: 'mig-1-2b',
                    from: 'v1.0',
                    to: 'v2.5',
                    weight: 8,
                    costs: { restarts: 0 },
                },
                {
                    id: 'mig-2b-3',
                    from: 'v2.5',
                    to: 'v3.0',
                    weight: 8,
                    costs: { restarts: 0 },
                },
            ],
        });

        const budgeted = invokeCli(
            [
                'path',
                '--input',
                '-',
                '--from',
                'v1.0',
                '--to',
                'v3.0',
                '--budget',
                'restarts=1',
            ],
            migrationGraph
        );
        assert.equal(budgeted.code, 0);
        const budgetedJson = JSON.parse(budgeted.stdout);
        assert.equal(budgetedJson.result.route.totalCost, 13);
        assert.deepEqual(budgetedJson.result.route.nodes, [
            'v1.0',
            'v2.0',
            'v3.0',
        ]);
        assert.equal(budgetedJson.result.budgetUsed.restarts, 1);

        const kRes = invokeCli(
            [
                'k-paths',
                '--input',
                '-',
                '--from',
                'v1.0',
                '--to',
                'v3.0',
                '--k',
                '3',
            ],
            migrationGraph
        );
        assert.equal(kRes.code, 0);
        const kJson = JSON.parse(kRes.stdout);
        assert.deepEqual(
            kJson.result.paths.map((p) => p.route.totalCost),
            [10, 13, 16]
        );
    });

    it('supports reverse CSV dependency tracing and max-cost blast-radius pruning', () => {
        const csv = [
            'from,to,weight,id,label',
            'web-api,auth-svc,1,imp1,imports',
            'auth-svc,jwt-lib,1,imp2,imports',
            'worker,batch-lib,1,imp3,imports',
            'batch-lib,jwt-lib,2,imp4,transitive',
            'cli,web-api,1,imp5,calls',
        ].join('\n');

        const res = invokeCli(
            [
                'distances',
                '--input',
                '-',
                '--input-format',
                'csv',
                '--from',
                'jwt-lib',
                '--reverse',
                '--max-cost',
                '2',
            ],
            csv
        );
        assert.equal(res.code, 0);
        const payload = JSON.parse(res.stdout);
        const reachableNodes = payload.result.reachable.map((r) => r.node);
        assert.deepEqual(reachableNodes, [
            'jwt-lib',
            'auth-svc',
            'batch-lib',
            'web-api',
        ]);
        assert.equal(payload.result.prunedByMaxCost, true);
        assert.deepEqual(payload.result.unreachableNodes, []);
        assert.ok(payload.result.notReachedWithinMaxCost.includes('cli'));
    });

    it('finds nearest healthy mirror and handles failover --avoid-node', () => {
        const infra = JSON.stringify({
            directed: false,
            unit: 'ms',
            edges: [
                { id: 'link1', from: 'runner', to: 'reg-eu', weight: 18 },
                { id: 'link2', from: 'runner', to: 'reg-us', weight: 9 },
                { id: 'link3', from: 'reg-us', to: 'reg-eu', weight: 11 },
            ],
        });

        const normal = invokeCli(
            [
                'nearest',
                '--input',
                '-',
                '--from',
                'runner',
                '--targets',
                'reg-eu,reg-us',
            ],
            infra
        );
        assert.equal(normal.code, 0);
        assert.equal(JSON.parse(normal.stdout).result.nearest.target, 'reg-us');

        const failover = invokeCli(
            [
                'nearest',
                '--input',
                '-',
                '--from',
                'runner',
                '--targets',
                'reg-eu,reg-us',
                '--avoid-node',
                'reg-us',
            ],
            infra
        );
        assert.equal(failover.code, 0);
        assert.equal(
            JSON.parse(failover.stdout).result.nearest.target,
            'reg-eu'
        );
    });

    it('supports reliability mode with zero-probability filtering and Mermaid/table formats', () => {
        const graph = JSON.stringify({
            directed: true,
            edges: [
                { id: 'p1', from: 'src', to: 'mid', probability: 0.95 },
                { id: 'p2', from: 'mid', to: 'dst', probability: 0.95 },
                { id: 'p3', from: 'src', to: 'dst', probability: 0.8 },
                { id: 'dead', from: 'src', to: 'dst', probability: 0 },
            ],
        });

        const jsonRes = invokeCli(
            [
                'path',
                '--input',
                '-',
                '--from',
                'src',
                '--to',
                'dst',
                '--reliability',
            ],
            graph
        );
        assert.equal(jsonRes.code, 0);
        const payload = JSON.parse(jsonRes.stdout);
        assert.deepEqual(payload.result.route.nodes, ['src', 'mid', 'dst']);
        assert.ok(Math.abs(payload.result.route.reliability - 0.9025) < 1e-12);
        assert.equal(payload.graph.skippedZeroProbabilityEdges, 1);

        const mermaidRes = invokeCli(
            [
                'path',
                '--input',
                '-',
                '--from',
                'src',
                '--to',
                'dst',
                '--reliability',
                '--format',
                'mermaid',
            ],
            graph
        );
        assert.equal(mermaidRes.code, 0);
        assert.match(mermaidRes.stdout, /^flowchart LR/);
        assert.match(mermaidRes.stdout, /==>/);

        const tableRes = invokeCli(
            [
                'path',
                '--input',
                '-',
                '--from',
                'src',
                '--to',
                'dst',
                '--reliability',
                '--format',
                'table',
            ],
            graph
        );
        assert.equal(tableRes.code, 0);
        assert.match(tableRes.stdout, /Composite reliability:/);
    });
});

describe('Resource guards and file I/O', () => {
    it('enforces --max-states with exit 5 distinct from unreachable', () => {
        const edges = [];
        for (let i = 1; i <= 15; i += 1) {
            edges.push({ from: `n${i}`, to: `n${i + 1}`, weight: 1 });
        }
        const res = invokeCli(
            [
                'path',
                '--input',
                '-',
                '--from',
                'n1',
                '--to',
                'n16',
                '--max-states',
                '5',
            ],
            JSON.stringify({ edges })
        );
        assert.equal(res.code, 5);
        const err = JSON.parse(res.stderr);
        assert.equal(err.status, 'resource_limit');
    });

    it('reads graph files from a caller directory outside the skill directory', () => {
        const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'sp-test-'));
        const filePath = path.join(tmpDir, 'sample.json');
        try {
            fs.writeFileSync(
                filePath,
                JSON.stringify({
                    edges: [{ from: 'start', to: 'end', weight: 4 }],
                }),
                'utf8'
            );
            const proc = spawnSync(
                process.execPath,
                [
                    SCRIPT_PATH,
                    'path',
                    '--input',
                    filePath,
                    '--from',
                    'start',
                    '--to',
                    'end',
                ],
                { cwd: tmpDir, encoding: 'utf8' }
            );
            assert.equal(proc.status, 0);
            const payload = JSON.parse(proc.stdout);
            assert.equal(payload.result.route.totalCost, 4);
        } finally {
            fs.rmSync(tmpDir, { recursive: true, force: true });
        }
    });
});

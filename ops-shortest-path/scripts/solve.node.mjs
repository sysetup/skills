/**
 * @fileoverview solve.node.mjs - Version 1.0.0
 *
 * Created: 2026-11-24
 *
 * Deterministic single-source shortest-path solver (Dijkstra and Yen K-paths)
 * for software engineering, systems, and DevOps operational graph modeling.
 * Usage: node solve.node.mjs <path|nearest|distances|k-paths|validate|selftest|help> [options]
 *
 * Features:
 * - Parses JSON, CSV edge-lists, and a bounded Graphviz DOT subset with fail-closed validation
 * - Supports path, nearest-target, all-distances, reverse-graph, Yen k-paths, node/edge exclusions, discrete budgets, and reliability (-ln p) mode
 * - Enforces checked arithmetic, strict relaxation, stale-entry skipping, parallel edge identity, and bounded state/heap limits
 * - Emits structured JSON, Mermaid flowcharts, or step tables to stdout and diagnostics to stderr
 *
 * Author: Carlos HRG
 * Role: Software Developer
 * Organization: SYSETUP.COM
 * License: MIT
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const VERSION = '1.0.0';
const DEFAULT_MAX_INPUT_BYTES = 2 * 1024 * 1024;
const DEFAULT_MAX_STATES = 200000;
const DEFAULT_MAX_HEAP = 500000;
const MAX_K_PATHS = 20;
const MAX_MERMAID_FULL_EDGES = 80;
const STRICT_NUMBER_RE = /^[+-]?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?$/;
const BUDGET_SPEC_RE = /^([A-Za-z0-9_.-]+)=([0-9]+)$/;

const EXIT_CODES = Object.freeze({
    OK: 0,
    UNREACHABLE: 1,
    CLI_ERROR: 2,
    INVALID_INPUT: 3,
    INAPPLICABLE_MODEL: 4,
    RESOURCE_LIMIT: 5,
});

function hasOwn(obj, key) {
    return Object.prototype.hasOwnProperty.call(obj, key);
}

function isPlainObject(value) {
    return (
        value !== null &&
        typeof value === 'object' &&
        !Array.isArray(value) &&
        Object.getPrototypeOf(value) === Object.prototype
    );
}

function normalizeZero(value) {
    return value === 0 ? 0 : value;
}

function createSolverError(status, exitCode, message, details = null) {
    const err = new Error(message);
    err.status = status;
    err.exitCode = exitCode;
    err.details = details;
    return err;
}

function parseStrictNumber(raw, context) {
    if (typeof raw !== 'string') {
        throw createSolverError(
            'invalid_input',
            EXIT_CODES.INVALID_INPUT,
            `Expected numeric token for ${context}.`
        );
    }
    const trimmed = raw.trim();
    if (!STRICT_NUMBER_RE.test(trimmed)) {
        throw createSolverError(
            'invalid_input',
            EXIT_CODES.INVALID_INPUT,
            `Invalid numeric value "${trimmed}" for ${context}.`
        );
    }
    const num = Number(trimmed);
    if (!Number.isFinite(num)) {
        throw createSolverError(
            'invalid_input',
            EXIT_CODES.INVALID_INPUT,
            `Non-finite numeric value "${trimmed}" for ${context}.`
        );
    }
    return normalizeZero(num);
}

function parsePositiveIntOption(raw, flagName, maxAllowed) {
    if (typeof raw !== 'string' || !/^[1-9]\d*$/.test(raw.trim())) {
        throw createSolverError(
            'cli_error',
            EXIT_CODES.CLI_ERROR,
            `${flagName} requires a positive integer; received "${String(raw)}".`
        );
    }
    const value = Number.parseInt(raw.trim(), 10);
    if (!Number.isSafeInteger(value) || value > maxAllowed) {
        throw createSolverError(
            'cli_error',
            EXIT_CODES.CLI_ERROR,
            `${flagName} must be between 1 and ${maxAllowed}.`
        );
    }
    return value;
}

function parseNonNegativeNumberOption(raw, flagName) {
    let value = 0;
    try {
        value = parseStrictNumber(String(raw), flagName);
    } catch (err) {
        throw createSolverError(
            'cli_error',
            EXIT_CODES.CLI_ERROR,
            `${flagName} requires a finite non-negative number; received "${String(raw)}".`
        );
    }
    if (value < 0) {
        throw createSolverError(
            'cli_error',
            EXIT_CODES.CLI_ERROR,
            `${flagName} must be non-negative; received ${value}.`
        );
    }
    return value;
}

function checkedAdd(left, right, integerMode) {
    if (!Number.isFinite(left) || !Number.isFinite(right)) {
        throw createSolverError(
            'invalid_input',
            EXIT_CODES.INVALID_INPUT,
            'Non-finite operand encountered during cost addition.'
        );
    }
    const sum = left + right;
    if (!Number.isFinite(sum)) {
        throw createSolverError(
            'invalid_input',
            EXIT_CODES.INVALID_INPUT,
            'Numeric overflow encountered during path cost accumulation.'
        );
    }
    if (integerMode && sum > Number.MAX_SAFE_INTEGER) {
        throw createSolverError(
            'invalid_input',
            EXIT_CODES.INVALID_INPUT,
            'Safe integer limit exceeded during exact integer cost accumulation.'
        );
    }
    return normalizeZero(sum);
}

function createMinHeap(compare) {
    const items = [];

    function siftUp(startIndex) {
        let idx = startIndex;
        while (idx > 0) {
            const parent = Math.floor((idx - 1) / 2);
            if (compare(items[idx], items[parent]) < 0) {
                const tmp = items[parent];
                items[parent] = items[idx];
                items[idx] = tmp;
                idx = parent;
            } else {
                idx = 0;
            }
        }
    }

    function siftDown(startIndex) {
        let idx = startIndex;
        const len = items.length;
        let done = false;
        while (!done) {
            const left = idx * 2 + 1;
            const right = left + 1;
            let smallest = idx;
            if (left < len && compare(items[left], items[smallest]) < 0) {
                smallest = left;
            }
            if (right < len && compare(items[right], items[smallest]) < 0) {
                smallest = right;
            }
            if (smallest !== idx) {
                const tmp = items[idx];
                items[idx] = items[smallest];
                items[smallest] = tmp;
                idx = smallest;
            } else {
                done = true;
            }
        }
    }

    return {
        push(entry) {
            items.push(entry);
            siftUp(items.length - 1);
        },
        pop() {
            if (items.length === 0) {
                return null;
            }
            const top = items[0];
            const last = items.pop();
            if (items.length > 0) {
                items[0] = last;
                siftDown(0);
            }
            return top;
        },
        size() {
            return items.length;
        },
    };
}

function validateWeightValue(rawWeight, edgeId, reliabilityMode) {
    if (typeof rawWeight !== 'number' || !Number.isFinite(rawWeight)) {
        throw createSolverError(
            'invalid_input',
            EXIT_CODES.INVALID_INPUT,
            `Edge "${edgeId}" requires a finite numeric weight/probability; received ${typeof rawWeight}.`
        );
    }
    if (reliabilityMode) {
        if (rawWeight < 0 || rawWeight > 1) {
            throw createSolverError(
                'invalid_input',
                EXIT_CODES.INVALID_INPUT,
                `Edge "${edgeId}" probability must be in [0, 1]; received ${rawWeight}.`
            );
        }
        if (rawWeight === 0) {
            return { infeasible: true, weight: Infinity, probability: 0 };
        }
        return {
            infeasible: false,
            weight: normalizeZero(-Math.log(rawWeight)),
            probability: rawWeight,
        };
    }
    if (rawWeight < 0) {
        throw createSolverError(
            'inapplicable_model',
            EXIT_CODES.INAPPLICABLE_MODEL,
            `Edge "${edgeId}" has negative weight (${rawWeight}), which invalidates Dijkstra.`,
            {
                edgeId,
                weight: rawWeight,
                recommendation:
                    'Use Bellman-Ford for general graphs with negative edges (and check reachable negative cycles), or topological dynamic programming if the graph is a DAG.',
            }
        );
    }
    return {
        infeasible: false,
        weight: normalizeZero(rawWeight),
        probability: null,
    };
}

function validateBudgetCosts(rawCosts, edgeId) {
    if (rawCosts === undefined || rawCosts === null) {
        return {};
    }
    if (!isPlainObject(rawCosts)) {
        throw createSolverError(
            'invalid_input',
            EXIT_CODES.INVALID_INPUT,
            `Edge "${edgeId}" costs must be an object mapping dimension names to non-negative integers.`
        );
    }
    const clean = {};
    const keys = Object.keys(rawCosts);
    for (let i = 0; i < keys.length; i += 1) {
        const dim = keys[i];
        const val = rawCosts[dim];
        if (typeof val !== 'number' || !Number.isSafeInteger(val) || val < 0) {
            throw createSolverError(
                'invalid_input',
                EXIT_CODES.INVALID_INPUT,
                `Edge "${edgeId}" budget cost "${dim}" must be a non-negative safe integer.`
            );
        }
        clean[dim] = val;
    }
    return clean;
}

function buildGraphModel(rawSpec, options = {}) {
    const reliabilityMode = Boolean(options.reliability);
    const forceUndirected = Boolean(options.undirected);
    const directed = forceUndirected ? false : rawSpec.directed !== false;
    const unit =
        typeof rawSpec.unit === 'string' && rawSpec.unit.trim().length > 0
            ? rawSpec.unit.trim()
            : null;

    const nodeOrder = [];
    const nodeMap = new Map();
    const explicitNodes = Array.isArray(rawSpec.nodes);

    function registerNode(id, label) {
        if (typeof id !== 'string' || id.trim().length === 0) {
            throw createSolverError(
                'invalid_input',
                EXIT_CODES.INVALID_INPUT,
                'Every node ID must be a non-empty string.'
            );
        }
        if (!nodeMap.has(id)) {
            const index = nodeOrder.length;
            const info = {
                id,
                index,
                label:
                    typeof label === 'string' && label.length > 0 ? label : id,
            };
            nodeMap.set(id, info);
            nodeOrder.push(info);
        } else if (typeof label === 'string' && label.length > 0) {
            const existing = nodeMap.get(id);
            if (existing.label === existing.id) {
                existing.label = label;
            }
        }
    }

    if (explicitNodes) {
        for (let i = 0; i < rawSpec.nodes.length; i += 1) {
            const entry = rawSpec.nodes[i];
            if (typeof entry === 'string') {
                if (nodeMap.has(entry)) {
                    throw createSolverError(
                        'invalid_input',
                        EXIT_CODES.INVALID_INPUT,
                        `Duplicate node ID "${entry}" in nodes list.`
                    );
                }
                registerNode(entry, entry);
            } else if (isPlainObject(entry)) {
                if (typeof entry.id !== 'string' || entry.id.trim() === '') {
                    throw createSolverError(
                        'invalid_input',
                        EXIT_CODES.INVALID_INPUT,
                        `Node entry at index ${i} requires a non-empty string "id".`
                    );
                }
                if (nodeMap.has(entry.id)) {
                    throw createSolverError(
                        'invalid_input',
                        EXIT_CODES.INVALID_INPUT,
                        `Duplicate node ID "${entry.id}" in nodes list.`
                    );
                }
                if (
                    entry.label !== undefined &&
                    typeof entry.label !== 'string'
                ) {
                    throw createSolverError(
                        'invalid_input',
                        EXIT_CODES.INVALID_INPUT,
                        `Node "${entry.id}" label must be a string.`
                    );
                }
                registerNode(entry.id, entry.label || entry.id);
            } else {
                throw createSolverError(
                    'invalid_input',
                    EXIT_CODES.INVALID_INPUT,
                    `Node entry at index ${i} must be a string or object.`
                );
            }
        }
    }

    if (!Array.isArray(rawSpec.edges)) {
        throw createSolverError(
            'invalid_input',
            EXIT_CODES.INVALID_INPUT,
            'Graph specification must include an "edges" array.'
        );
    }

    const usedEdgeIds = new Set();
    const edges = [];
    let skippedZeroProbEdges = 0;
    let allIntegers = !reliabilityMode;
    let zeroWeightEdges = 0;
    let firstPositiveWeight = null;
    let allEqualPositiveWeights = true;
    const pairCounts = new Map();

    for (let i = 0; i < rawSpec.edges.length; i += 1) {
        const rawEdge = rawSpec.edges[i];
        if (!isPlainObject(rawEdge)) {
            throw createSolverError(
                'invalid_input',
                EXIT_CODES.INVALID_INPUT,
                `Edge at index ${i} must be an object.`
            );
        }
        const fromId = rawEdge.from;
        const toId = rawEdge.to;
        if (
            typeof fromId !== 'string' ||
            fromId.trim().length === 0 ||
            typeof toId !== 'string' ||
            toId.trim().length === 0
        ) {
            throw createSolverError(
                'invalid_input',
                EXIT_CODES.INVALID_INPUT,
                `Edge at index ${i} requires non-empty string "from" and "to" endpoints.`
            );
        }
        if (explicitNodes) {
            if (!nodeMap.has(fromId)) {
                throw createSolverError(
                    'invalid_input',
                    EXIT_CODES.INVALID_INPUT,
                    `Edge at index ${i} references undeclared "from" node "${fromId}".`
                );
            }
            if (!nodeMap.has(toId)) {
                throw createSolverError(
                    'invalid_input',
                    EXIT_CODES.INVALID_INPUT,
                    `Edge at index ${i} references undeclared "to" node "${toId}".`
                );
            }
        } else {
            registerNode(fromId, fromId);
            registerNode(toId, toId);
        }

        let edgeId = `e${i + 1}`;
        if (rawEdge.id !== undefined) {
            if (typeof rawEdge.id !== 'string' || rawEdge.id.trim() === '') {
                throw createSolverError(
                    'invalid_input',
                    EXIT_CODES.INVALID_INPUT,
                    `Edge at index ${i} has an invalid empty/non-string "id".`
                );
            }
            edgeId = rawEdge.id;
        }
        if (usedEdgeIds.has(edgeId)) {
            throw createSolverError(
                'invalid_input',
                EXIT_CODES.INVALID_INPUT,
                `Duplicate edge ID "${edgeId}".`
            );
        }
        usedEdgeIds.add(edgeId);

        if (rawEdge.label !== undefined && typeof rawEdge.label !== 'string') {
            throw createSolverError(
                'invalid_input',
                EXIT_CODES.INVALID_INPUT,
                `Edge "${edgeId}" label must be a string.`
            );
        }

        const rawMetric =
            reliabilityMode && rawEdge.probability !== undefined
                ? rawEdge.probability
                : rawEdge.weight;
        const metric = validateWeightValue(rawMetric, edgeId, reliabilityMode);
        const costs = validateBudgetCosts(rawEdge.costs, edgeId);

        if (metric.infeasible) {
            skippedZeroProbEdges += 1;
        } else {
            if (!Number.isSafeInteger(metric.weight)) {
                allIntegers = false;
            }
            if (metric.weight === 0) {
                zeroWeightEdges += 1;
                allEqualPositiveWeights = false;
            } else if (firstPositiveWeight === null) {
                firstPositiveWeight = metric.weight;
            } else if (metric.weight !== firstPositiveWeight) {
                allEqualPositiveWeights = false;
            }
            const pairKey = directed
                ? `${fromId}\u0000${toId}`
                : [fromId, toId].sort().join('\u0000');
            pairCounts.set(pairKey, (pairCounts.get(pairKey) || 0) + 1);

            edges.push({
                id: edgeId,
                from: fromId,
                to: toId,
                weight: metric.weight,
                probability: metric.probability,
                label: rawEdge.label || '',
                costs,
            });
        }
    }

    if (edges.length === 0) {
        allEqualPositiveWeights = false;
    }

    let parallelEdgePairs = 0;
    pairCounts.forEach((count) => {
        if (count > 1) {
            parallelEdgePairs += 1;
        }
    });

    const adjacency = new Map();
    const reverseAdjacency = new Map();
    for (let i = 0; i < nodeOrder.length; i += 1) {
        adjacency.set(nodeOrder[i].id, []);
        reverseAdjacency.set(nodeOrder[i].id, []);
    }

    for (let i = 0; i < edges.length; i += 1) {
        const edge = edges[i];
        adjacency.get(edge.from).push(edge);
        reverseAdjacency.get(edge.to).push({
            id: edge.id,
            from: edge.to,
            to: edge.from,
            weight: edge.weight,
            probability: edge.probability,
            label: edge.label,
            costs: edge.costs,
        });
        if (!directed && edge.from !== edge.to) {
            const mirrored = {
                id: edge.id,
                from: edge.to,
                to: edge.from,
                weight: edge.weight,
                probability: edge.probability,
                label: edge.label,
                costs: edge.costs,
            };
            adjacency.get(edge.to).push(mirrored);
            reverseAdjacency.get(edge.from).push(edge);
        }
    }

    let numericModel = 'ieee754-float';
    if (reliabilityMode) {
        numericModel = 'neg-log-probability';
    } else if (allIntegers) {
        numericModel = 'exact-integer';
    }

    const assumptions = Array.isArray(rawSpec.assumptions)
        ? rawSpec.assumptions.slice()
        : [];
    if (reliabilityMode) {
        assumptions.push(
            'Path reliability modeled as product of independent edge probabilities in (0, 1] via additive -ln(p) costs.'
        );
    }
    if (skippedZeroProbEdges > 0) {
        assumptions.push(
            `Excluded ${skippedZeroProbEdges} infeasible zero-probability edge(s) in reliability mode.`
        );
    }

    return {
        directed,
        unit: reliabilityMode ? 'neg-log-probability' : unit,
        nodes: nodeOrder,
        nodeMap,
        edges,
        adjacency,
        reverseAdjacency,
        reliabilityMode,
        numericModel,
        allIntegers,
        zeroWeightEdges,
        parallelEdgePairs,
        allEqualPositiveWeights,
        skippedZeroProbEdges,
        assumptions,
    };
}

function parseJsonGraph(rawText) {
    let parsed = null;
    try {
        parsed = JSON.parse(rawText);
    } catch (err) {
        throw createSolverError(
            'invalid_input',
            EXIT_CODES.INVALID_INPUT,
            `Malformed JSON graph input: ${err.message}`
        );
    }
    if (!isPlainObject(parsed)) {
        throw createSolverError(
            'invalid_input',
            EXIT_CODES.INVALID_INPUT,
            'JSON graph input must be a JSON object.'
        );
    }
    if (parsed.directed !== undefined && typeof parsed.directed !== 'boolean') {
        throw createSolverError(
            'invalid_input',
            EXIT_CODES.INVALID_INPUT,
            'JSON field "directed" must be a boolean.'
        );
    }
    if (parsed.unit !== undefined && typeof parsed.unit !== 'string') {
        throw createSolverError(
            'invalid_input',
            EXIT_CODES.INVALID_INPUT,
            'JSON field "unit" must be a string.'
        );
    }
    return parsed;
}

function parseCsvRows(text) {
    const rows = [];
    let currentRow = [];
    let field = '';
    let inQuotes = false;
    let i = 0;

    while (i < text.length) {
        const ch = text[i];
        if (inQuotes) {
            if (ch === '"') {
                if (i + 1 < text.length && text[i + 1] === '"') {
                    field += '"';
                    i += 2;
                } else {
                    inQuotes = false;
                    i += 1;
                }
            } else {
                field += ch;
                i += 1;
            }
        } else if (ch === '"') {
            if (field.length > 0) {
                throw createSolverError(
                    'invalid_input',
                    EXIT_CODES.INVALID_INPUT,
                    'Unexpected quote inside unquoted CSV field.'
                );
            }
            inQuotes = true;
            i += 1;
        } else if (ch === ',') {
            currentRow.push(field);
            field = '';
            i += 1;
        } else if (ch === '\r' || ch === '\n') {
            currentRow.push(field);
            rows.push(currentRow);
            currentRow = [];
            field = '';
            if (ch === '\r' && i + 1 < text.length && text[i + 1] === '\n') {
                i += 2;
            } else {
                i += 1;
            }
        } else {
            field += ch;
            i += 1;
        }
    }

    if (inQuotes) {
        throw createSolverError(
            'invalid_input',
            EXIT_CODES.INVALID_INPUT,
            'Unterminated quoted field in CSV input.'
        );
    }
    if (field.length > 0 || currentRow.length > 0) {
        currentRow.push(field);
        rows.push(currentRow);
    }

    return rows.filter(
        (row) => !(row.length === 1 && row[0].trim().length === 0)
    );
}

function parseCsvGraph(rawText, options = {}) {
    const rows = parseCsvRows(rawText);
    if (rows.length === 0) {
        throw createSolverError(
            'invalid_input',
            EXIT_CODES.INVALID_INPUT,
            'CSV input contains no rows.'
        );
    }

    let startRow = 0;
    let fromIdx = 0;
    let toIdx = 1;
    let weightIdx = 2;
    let idIdx = -1;
    let labelIdx = -1;
    const budgetCols = [];

    const firstRow = rows[0].map((cell) => cell.trim());
    const looksHeaderless =
        firstRow.length >= 3 && STRICT_NUMBER_RE.test(firstRow[2]);

    if (!looksHeaderless) {
        startRow = 1;
        const lower = firstRow.map((h) => h.toLowerCase());
        fromIdx = lower.indexOf('from');
        toIdx = lower.indexOf('to');
        weightIdx = options.reliability
            ? lower.indexOf('probability')
            : lower.indexOf('weight');
        if (weightIdx === -1) {
            weightIdx = lower.indexOf('weight');
        }
        if (weightIdx === -1) {
            weightIdx = lower.indexOf('cost');
        }
        idIdx = lower.indexOf('id');
        labelIdx = lower.indexOf('label');
        if (fromIdx === -1 || toIdx === -1 || weightIdx === -1) {
            throw createSolverError(
                'invalid_input',
                EXIT_CODES.INVALID_INPUT,
                'CSV header must contain "from", "to", and "weight" (or "cost"/"probability") columns.'
            );
        }
        for (let c = 0; c < firstRow.length; c += 1) {
            if (lower[c].startsWith('cost:')) {
                const dim = firstRow[c].slice(5).trim();
                if (dim.length > 0) {
                    budgetCols.push({ index: c, dim });
                }
            }
        }
    } else {
        if (firstRow.length >= 4) {
            idIdx = 3;
        }
        if (firstRow.length >= 5) {
            labelIdx = 4;
        }
    }

    const edges = [];
    for (let r = startRow; r < rows.length; r += 1) {
        const row = rows[r];
        if (row.length < 3) {
            throw createSolverError(
                'invalid_input',
                EXIT_CODES.INVALID_INPUT,
                `CSV row ${r + 1} has fewer than 3 columns.`
            );
        }
        const fromVal = (row[fromIdx] || '').trim();
        const toVal = (row[toIdx] || '').trim();
        const metricVal = parseStrictNumber(
            row[weightIdx] || '',
            `CSV row ${r + 1} weight`
        );
        const edgeObj = {
            from: fromVal,
            to: toVal,
            weight: metricVal,
        };
        if (options.reliability) {
            edgeObj.probability = metricVal;
        }
        if (
            idIdx >= 0 &&
            row[idIdx] !== undefined &&
            row[idIdx].trim() !== ''
        ) {
            edgeObj.id = row[idIdx].trim();
        }
        if (labelIdx >= 0 && row[labelIdx] !== undefined) {
            edgeObj.label = row[labelIdx].trim();
        }
        if (budgetCols.length > 0) {
            const costs = {};
            for (let b = 0; b < budgetCols.length; b += 1) {
                const col = budgetCols[b];
                const rawBudget = (row[col.index] || '').trim();
                if (rawBudget.length > 0) {
                    costs[col.dim] = parseStrictNumber(
                        rawBudget,
                        `CSV row ${r + 1} cost:${col.dim}`
                    );
                }
            }
            edgeObj.costs = costs;
        }
        edges.push(edgeObj);
    }

    return {
        directed: true,
        edges,
    };
}

function stripDotComments(text) {
    let out = '';
    let inQuotes = false;
    let i = 0;
    while (i < text.length) {
        const ch = text[i];
        if (inQuotes) {
            out += ch;
            if (ch === '\\' && i + 1 < text.length) {
                out += text[i + 1];
                i += 2;
            } else {
                if (ch === '"') {
                    inQuotes = false;
                }
                i += 1;
            }
        } else if (ch === '"') {
            inQuotes = true;
            out += ch;
            i += 1;
        } else if (ch === '/' && text[i + 1] === '/') {
            i += 2;
            while (i < text.length && text[i] !== '\n') {
                i += 1;
            }
        } else if (ch === '/' && text[i + 1] === '*') {
            i += 2;
            let closed = false;
            while (i + 1 < text.length && !closed) {
                if (text[i] === '*' && text[i + 1] === '/') {
                    i += 2;
                    closed = true;
                } else {
                    i += 1;
                }
            }
            if (!closed) {
                throw createSolverError(
                    'invalid_input',
                    EXIT_CODES.INVALID_INPUT,
                    'Unterminated block comment in DOT input.'
                );
            }
            out += ' ';
        } else {
            out += ch;
            i += 1;
        }
    }
    if (inQuotes) {
        throw createSolverError(
            'invalid_input',
            EXIT_CODES.INVALID_INPUT,
            'Unterminated quoted string in DOT input.'
        );
    }
    return out;
}

function tokenizeDot(text) {
    const tokens = [];
    let i = 0;
    while (i < text.length) {
        const ch = text[i];
        if (/\s/.test(ch)) {
            i += 1;
        } else if (ch === '-' && (text[i + 1] === '>' || text[i + 1] === '-')) {
            tokens.push({ type: 'edgeop', value: text.slice(i, i + 2) });
            i += 2;
        } else if ('{}[];,='.includes(ch)) {
            tokens.push({ type: 'punct', value: ch });
            i += 1;
        } else if (ch === '"') {
            let val = '';
            i += 1;
            while (i < text.length && text[i] !== '"') {
                if (text[i] === '\\' && i + 1 < text.length) {
                    val += text[i + 1];
                    i += 2;
                } else {
                    val += text[i];
                    i += 1;
                }
            }
            if (i >= text.length) {
                throw createSolverError(
                    'invalid_input',
                    EXIT_CODES.INVALID_INPUT,
                    'Unterminated string literal in DOT input.'
                );
            }
            i += 1;
            tokens.push({ type: 'id', value: val });
        } else {
            let start = i;
            while (
                i < text.length &&
                !/[\s{}[\];,="]/.test(text[i]) &&
                !(
                    text[i] === '-' &&
                    (text[i + 1] === '>' || text[i + 1] === '-')
                )
            ) {
                i += 1;
            }
            if (i === start) {
                throw createSolverError(
                    'invalid_input',
                    EXIT_CODES.INVALID_INPUT,
                    `Unexpected character "${ch}" in DOT input.`
                );
            }
            tokens.push({ type: 'id', value: text.slice(start, i) });
            start = i;
        }
    }
    return tokens;
}

function parseDotAttributes(tokens, startPos) {
    const attrs = {};
    let pos = startPos;
    while (
        pos < tokens.length &&
        tokens[pos].type === 'punct' &&
        tokens[pos].value === '['
    ) {
        pos += 1;
        let closed = false;
        while (pos < tokens.length && !closed) {
            if (tokens[pos].type === 'punct' && tokens[pos].value === ']') {
                pos += 1;
                closed = true;
            } else if (
                tokens[pos].type === 'punct' &&
                (tokens[pos].value === ',' || tokens[pos].value === ';')
            ) {
                pos += 1;
            } else if (tokens[pos].type === 'id') {
                const key = tokens[pos].value.toLowerCase();
                pos += 1;
                if (
                    pos < tokens.length &&
                    tokens[pos].type === 'punct' &&
                    tokens[pos].value === '='
                ) {
                    pos += 1;
                    if (pos >= tokens.length || tokens[pos].type !== 'id') {
                        throw createSolverError(
                            'invalid_input',
                            EXIT_CODES.INVALID_INPUT,
                            `Missing attribute value for "${key}" in DOT input.`
                        );
                    }
                    attrs[key] = tokens[pos].value;
                    pos += 1;
                } else {
                    attrs[key] = 'true';
                }
            } else {
                throw createSolverError(
                    'invalid_input',
                    EXIT_CODES.INVALID_INPUT,
                    `Unexpected token "${tokens[pos].value}" inside DOT attribute list.`
                );
            }
        }
        if (!closed) {
            throw createSolverError(
                'invalid_input',
                EXIT_CODES.INVALID_INPUT,
                'Unclosed "[" attribute list in DOT input.'
            );
        }
    }
    return { attrs, nextPos: pos };
}

function parseDotGraph(rawText, options = {}) {
    const cleaned = stripDotComments(rawText);
    const tokens = tokenizeDot(cleaned);
    let pos = 0;

    if (
        pos < tokens.length &&
        tokens[pos].type === 'id' &&
        tokens[pos].value.toLowerCase() === 'strict'
    ) {
        pos += 1;
    }
    if (pos >= tokens.length || tokens[pos].type !== 'id') {
        throw createSolverError(
            'invalid_input',
            EXIT_CODES.INVALID_INPUT,
            'DOT input must start with "digraph" or "graph".'
        );
    }
    const kind = tokens[pos].value.toLowerCase();
    if (kind !== 'digraph' && kind !== 'graph') {
        throw createSolverError(
            'invalid_input',
            EXIT_CODES.INVALID_INPUT,
            `Unsupported DOT graph type "${tokens[pos].value}"; expected "digraph" or "graph".`
        );
    }
    const directed = kind === 'digraph';
    const expectedOp = directed ? '->' : '--';
    pos += 1;

    if (pos < tokens.length && tokens[pos].type === 'id') {
        pos += 1;
    }
    if (
        pos >= tokens.length ||
        tokens[pos].type !== 'punct' ||
        tokens[pos].value !== '{'
    ) {
        throw createSolverError(
            'invalid_input',
            EXIT_CODES.INVALID_INPUT,
            'Expected "{" opening DOT graph body.'
        );
    }
    pos += 1;

    const nodeRegistry = new Map();
    const edges = [];
    const assumptions = [];
    let usedDefaultWeight = false;

    function ensureDotNode(id, label) {
        if (!nodeRegistry.has(id)) {
            nodeRegistry.set(id, { id, label: label || id });
        } else if (label) {
            nodeRegistry.get(id).label = label;
        }
    }

    let closedBody = false;
    while (pos < tokens.length && !closedBody) {
        const tok = tokens[pos];
        if (tok.type === 'punct' && tok.value === '}') {
            pos += 1;
            closedBody = true;
        } else if (tok.type === 'punct' && tok.value === ';') {
            pos += 1;
        } else if (
            tok.type === 'id' &&
            ['graph', 'node', 'edge'].includes(tok.value.toLowerCase()) &&
            pos + 1 < tokens.length &&
            tokens[pos + 1].type === 'punct' &&
            tokens[pos + 1].value === '['
        ) {
            const parsedAttrs = parseDotAttributes(tokens, pos + 1);
            pos = parsedAttrs.nextPos;
        } else if (
            tok.type === 'id' &&
            pos + 1 < tokens.length &&
            tokens[pos + 1].type === 'punct' &&
            tokens[pos + 1].value === '='
        ) {
            pos += 3;
        } else if (tok.type === 'id') {
            const chain = [tok.value];
            pos += 1;
            while (pos < tokens.length && tokens[pos].type === 'edgeop') {
                if (tokens[pos].value !== expectedOp) {
                    throw createSolverError(
                        'invalid_input',
                        EXIT_CODES.INVALID_INPUT,
                        `Edge operator "${tokens[pos].value}" does not match ${kind} (expected "${expectedOp}").`
                    );
                }
                pos += 1;
                if (pos >= tokens.length || tokens[pos].type !== 'id') {
                    throw createSolverError(
                        'invalid_input',
                        EXIT_CODES.INVALID_INPUT,
                        'Expected target node identifier after DOT edge operator.'
                    );
                }
                chain.push(tokens[pos].value);
                pos += 1;
            }
            const parsedAttrs = parseDotAttributes(tokens, pos);
            pos = parsedAttrs.nextPos;
            const { attrs } = parsedAttrs;

            if (chain.length === 1) {
                ensureDotNode(chain[0], attrs.label);
            } else {
                const metricStr = options.reliability
                    ? attrs.probability || attrs.weight
                    : attrs.weight || attrs.cost;
                let weightVal = null;
                if (metricStr !== undefined) {
                    weightVal = parseStrictNumber(
                        metricStr,
                        `DOT edge ${chain[0]} ${expectedOp} ${chain[1]}`
                    );
                } else if (
                    options.defaultWeight !== null &&
                    options.defaultWeight !== undefined
                ) {
                    weightVal = options.defaultWeight;
                    usedDefaultWeight = true;
                } else {
                    throw createSolverError(
                        'invalid_input',
                        EXIT_CODES.INVALID_INPUT,
                        `DOT edge "${chain[0]} ${expectedOp} ${chain[1]}" has no weight/cost attribute; specify weight or pass --default-weight <n>.`
                    );
                }

                for (let c = 0; c < chain.length - 1; c += 1) {
                    const fromNode = chain[c];
                    const toNode = chain[c + 1];
                    ensureDotNode(fromNode);
                    ensureDotNode(toNode);
                    const edgeObj = {
                        from: fromNode,
                        to: toNode,
                        weight: weightVal,
                        label: attrs.label || '',
                    };
                    if (options.reliability) {
                        edgeObj.probability = weightVal;
                    }
                    if (attrs.id && chain.length === 2) {
                        edgeObj.id = attrs.id;
                    }
                    edges.push(edgeObj);
                }
            }
        } else {
            throw createSolverError(
                'invalid_input',
                EXIT_CODES.INVALID_INPUT,
                `Unexpected token "${tok.value}" in DOT graph body.`
            );
        }
    }

    if (!closedBody) {
        throw createSolverError(
            'invalid_input',
            EXIT_CODES.INVALID_INPUT,
            'Unclosed "{" in DOT graph body.'
        );
    }

    if (usedDefaultWeight) {
        assumptions.push(
            `Applied explicit --default-weight=${options.defaultWeight} to unweighted DOT edge(s).`
        );
    }

    return {
        directed,
        nodes: Array.from(nodeRegistry.values()),
        edges,
        assumptions,
    };
}

function detectInputFormat(rawText, inputPath, requestedFormat) {
    if (requestedFormat && requestedFormat !== 'auto') {
        return requestedFormat;
    }
    if (inputPath && inputPath !== '-') {
        const ext = path.extname(inputPath).toLowerCase();
        if (ext === '.json') {
            return 'json';
        }
        if (ext === '.csv') {
            return 'csv';
        }
        if (ext === '.dot' || ext === '.gv') {
            return 'dot';
        }
    }
    const trimmed = rawText.trimStart();
    if (trimmed.startsWith('{')) {
        return 'json';
    }
    if (/^(?:strict\s+)?(?:di)?graph\b/i.test(trimmed)) {
        return 'dot';
    }
    return 'csv';
}

function parseGraphText(rawText, options = {}) {
    const format = detectInputFormat(
        rawText,
        options.inputPath || '',
        options.inputFormat || 'auto'
    );
    let rawSpec = null;
    if (format === 'json') {
        rawSpec = parseJsonGraph(rawText);
    } else if (format === 'csv') {
        rawSpec = parseCsvGraph(rawText, options);
    } else if (format === 'dot') {
        rawSpec = parseDotGraph(rawText, options);
    } else {
        throw createSolverError(
            'cli_error',
            EXIT_CODES.CLI_ERROR,
            `Unsupported --input-format "${format}". Expected: auto, json, csv, dot.`
        );
    }
    return buildGraphModel(rawSpec, options);
}

function buildStateKey(nodeId, budgetVec) {
    if (budgetVec.length === 0) {
        return nodeId;
    }
    return `${nodeId}\u0000${budgetVec.join(',')}`;
}

function reconstructRoute(
    graph,
    startKey,
    endKey,
    predecessors,
    reliabilityMode
) {
    const steps = [];
    const seenKeys = new Set();
    let curKey = endKey;
    let totalWeight = 0;
    let reliabilityProduct = 1;

    while (curKey !== startKey) {
        if (seenKeys.has(curKey)) {
            throw createSolverError(
                'invalid_input',
                EXIT_CODES.INVALID_INPUT,
                'Cycle detected during predecessor path reconstruction.'
            );
        }
        seenKeys.add(curKey);
        const link = predecessors.get(curKey);
        if (!link) {
            throw createSolverError(
                'invalid_input',
                EXIT_CODES.INVALID_INPUT,
                'Broken predecessor chain during path reconstruction.'
            );
        }
        steps.push(link);
        curKey = link.prevKey;
    }

    steps.reverse();
    const nodes = [startKey.split('\u0000')[0]];
    const edges = [];

    for (let i = 0; i < steps.length; i += 1) {
        const { edge } = steps[i];
        totalWeight = checkedAdd(totalWeight, edge.weight, graph.allIntegers);
        if (reliabilityMode && edge.probability !== null) {
            reliabilityProduct *= edge.probability;
        }
        nodes.push(edge.to);
        edges.push({
            step: i + 1,
            id: edge.id,
            from: edge.from,
            to: edge.to,
            weight: edge.weight,
            cumulativeCost: totalWeight,
            label: edge.label,
            probability: edge.probability,
            costs: edge.costs,
        });
    }

    const result = {
        nodes,
        edges,
        hops: edges.length,
        totalCost: totalWeight,
    };
    if (reliabilityMode) {
        result.reliability = reliabilityProduct;
    }
    return result;
}

class DijkstraSolver {
    constructor(graph, limits = {}) {
        this.graph = graph;
        this.maxStates = limits.maxStates || DEFAULT_MAX_STATES;
        this.maxHeap = limits.maxHeap || DEFAULT_MAX_HEAP;
    }

    getGraphSummary() {
        const { graph } = this;
        const notes = [];
        if (graph.allEqualPositiveWeights) {
            notes.push(
                'All edges share an identical positive weight; breadth-first search (BFS) also yields optimal paths in O(V + E).'
            );
        }
        if (graph.zeroWeightEdges > 0) {
            notes.push(
                `Graph contains ${graph.zeroWeightEdges} zero-weight edge(s); strict relaxation prevents zero-weight predecessor cycles.`
            );
        }
        return {
            directed: graph.directed,
            unit: graph.unit,
            numericModel: graph.numericModel,
            nodeCount: graph.nodes.length,
            edgeCount: graph.edges.length,
            zeroWeightEdges: graph.zeroWeightEdges,
            parallelEdgePairs: graph.parallelEdgePairs,
            skippedZeroProbabilityEdges: graph.skippedZeroProbEdges,
            notes,
        };
    }

    assertNodeExists(nodeId, role) {
        if (!this.graph.nodeMap.has(nodeId)) {
            throw createSolverError(
                'invalid_input',
                EXIT_CODES.INVALID_INPUT,
                `Unknown ${role} node "${nodeId}".`
            );
        }
    }

    runSearch(params) {
        const {
            from,
            targetSet = null,
            stopOnFirstTarget = false,
            avoidNodes = new Set(),
            avoidEdges = new Set(),
            budgets = [],
            maxCost = null,
            reverse = false,
            stateCounter = { states: 0, heapPushes: 0 },
        } = params;

        this.assertNodeExists(from, 'source');

        const budgetDims = budgets.map((b) => b.dim);
        const budgetCaps = budgets.map((b) => b.max);
        let stateSpaceBound = this.graph.nodes.length;
        for (let b = 0; b < budgetCaps.length; b += 1) {
            stateSpaceBound *= budgetCaps[b] + 1;
        }

        if (avoidNodes.has(from)) {
            return {
                settledTargets: [],
                bestNodeState: new Map(),
                dist: new Map(),
                predecessors: new Map(),
                startKey: buildStateKey(
                    from,
                    budgetCaps.map(() => 0)
                ),
                statesExpanded: 0,
                heapPushes: 0,
                stateSpaceBound,
                prunedByMaxCost: false,
            };
        }

        const adjMap = reverse
            ? this.graph.reverseAdjacency
            : this.graph.adjacency;
        const startBudget = budgetCaps.map(() => 0);
        const startKey = buildStateKey(from, startBudget);
        const dist = new Map();
        const predecessors = new Map();
        const bestNodeState = new Map();
        const settledTargetSet = new Set();
        const settledTargets = [];
        const counter = stateCounter;

        const heap = createMinHeap((a, b) => {
            if (a.distance !== b.distance) {
                return a.distance - b.distance;
            }
            return a.serial - b.serial;
        });

        let serial = 0;
        let prunedByMaxCost = false;
        dist.set(startKey, 0);
        serial += 1;
        counter.heapPushes += 1;
        heap.push({
            distance: 0,
            serial,
            key: startKey,
            nodeId: from,
            budgetVec: startBudget,
        });

        let finished = false;
        while (heap.size() > 0 && !finished) {
            const current = heap.pop();
            const knownDist = dist.get(current.key);
            if (knownDist === current.distance) {
                counter.states += 1;
                if (counter.states > this.maxStates) {
                    throw createSolverError(
                        'resource_limit',
                        EXIT_CODES.RESOURCE_LIMIT,
                        `Search exceeded --max-states limit (${this.maxStates}).`,
                        {
                            statesExpanded: counter.states - 1,
                            maxStates: this.maxStates,
                            stateSpaceBound,
                        }
                    );
                }

                if (!bestNodeState.has(current.nodeId)) {
                    bestNodeState.set(current.nodeId, {
                        key: current.key,
                        distance: current.distance,
                        budgetVec: current.budgetVec,
                    });
                }

                if (
                    targetSet !== null &&
                    targetSet.has(current.nodeId) &&
                    !settledTargetSet.has(current.nodeId)
                ) {
                    settledTargetSet.add(current.nodeId);
                    settledTargets.push({
                        nodeId: current.nodeId,
                        key: current.key,
                        distance: current.distance,
                        budgetVec: current.budgetVec,
                    });
                    if (
                        stopOnFirstTarget ||
                        settledTargetSet.size === targetSet.size
                    ) {
                        finished = true;
                    }
                }

                if (!finished) {
                    const neighbors = adjMap.get(current.nodeId) || [];
                    for (let i = 0; i < neighbors.length; i += 1) {
                        const edge = neighbors[i];
                        const blocked =
                            avoidEdges.has(edge.id) || avoidNodes.has(edge.to);
                        if (!blocked) {
                            let budgetOk = true;
                            const nextBudget = [];
                            for (let b = 0; b < budgetDims.length; b += 1) {
                                const dim = budgetDims[b];
                                const delta = hasOwn(edge.costs, dim)
                                    ? edge.costs[dim]
                                    : 0;
                                const used = current.budgetVec[b] + delta;
                                if (used > budgetCaps[b]) {
                                    budgetOk = false;
                                }
                                nextBudget.push(used);
                            }

                            if (budgetOk) {
                                const candidate = checkedAdd(
                                    current.distance,
                                    edge.weight,
                                    this.graph.allIntegers
                                );
                                if (maxCost !== null && candidate > maxCost) {
                                    prunedByMaxCost = true;
                                } else {
                                    const nextKey = buildStateKey(
                                        edge.to,
                                        nextBudget
                                    );
                                    const prevBest = dist.get(nextKey);
                                    if (
                                        prevBest === undefined ||
                                        candidate < prevBest
                                    ) {
                                        if (heap.size() + 1 > this.maxHeap) {
                                            throw createSolverError(
                                                'resource_limit',
                                                EXIT_CODES.RESOURCE_LIMIT,
                                                `Priority queue exceeded --max-heap limit (${this.maxHeap}).`,
                                                {
                                                    maxHeap: this.maxHeap,
                                                    statesExpanded:
                                                        counter.states,
                                                }
                                            );
                                        }
                                        dist.set(nextKey, candidate);
                                        predecessors.set(nextKey, {
                                            prevKey: current.key,
                                            edge,
                                        });
                                        serial += 1;
                                        counter.heapPushes += 1;
                                        heap.push({
                                            distance: candidate,
                                            serial,
                                            key: nextKey,
                                            nodeId: edge.to,
                                            budgetVec: nextBudget,
                                        });
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        return {
            settledTargets,
            bestNodeState,
            dist,
            predecessors,
            startKey,
            statesExpanded: counter.states,
            heapPushes: counter.heapPushes,
            stateSpaceBound,
            prunedByMaxCost,
        };
    }

    shortestPath(params) {
        this.assertNodeExists(params.from, 'source');
        this.assertNodeExists(params.to, 'target');
        const targetSet = new Set([params.to]);
        const search = this.runSearch({
            from: params.from,
            targetSet,
            stopOnFirstTarget: true,
            avoidNodes: params.avoidNodes,
            avoidEdges: params.avoidEdges,
            budgets: params.budgets,
            maxCost: params.maxCost,
            reverse: params.reverse,
            stateCounter: params.stateCounter,
        });

        if (search.settledTargets.length === 0) {
            return {
                found: false,
                status: 'unreachable',
                prunedByMaxCost: search.prunedByMaxCost,
                metrics: {
                    statesExpanded: search.statesExpanded,
                    heapPushes: search.heapPushes,
                    stateSpaceBound: search.stateSpaceBound,
                },
            };
        }

        const hit = search.settledTargets[0];
        const route = reconstructRoute(
            this.graph,
            search.startKey,
            hit.key,
            search.predecessors,
            this.graph.reliabilityMode
        );
        const budgetUsed = {};
        const budgets = params.budgets || [];
        for (let b = 0; b < budgets.length; b += 1) {
            budgetUsed[budgets[b].dim] = hit.budgetVec[b];
        }

        return {
            found: true,
            status: 'found',
            route,
            budgetUsed,
            metrics: {
                statesExpanded: search.statesExpanded,
                heapPushes: search.heapPushes,
                stateSpaceBound: search.stateSpaceBound,
            },
        };
    }

    nearestTarget(params) {
        this.assertNodeExists(params.from, 'source');
        if (!Array.isArray(params.targets) || params.targets.length === 0) {
            throw createSolverError(
                'invalid_input',
                EXIT_CODES.INVALID_INPUT,
                'Target set must be non-empty; use "distances" for all-distances mode.'
            );
        }
        const uniqueTargets = [];
        const targetSet = new Set();
        for (let i = 0; i < params.targets.length; i += 1) {
            const targetId = params.targets[i];
            this.assertNodeExists(targetId, 'target');
            if (!targetSet.has(targetId)) {
                targetSet.add(targetId);
                uniqueTargets.push(targetId);
            }
        }

        const search = this.runSearch({
            from: params.from,
            targetSet,
            stopOnFirstTarget: !params.allTargets,
            avoidNodes: params.avoidNodes,
            avoidEdges: params.avoidEdges,
            budgets: params.budgets,
            maxCost: params.maxCost,
            reverse: params.reverse,
        });

        if (search.settledTargets.length === 0) {
            return {
                found: false,
                status: 'unreachable',
                nearest: null,
                targets: uniqueTargets.map((id) => ({
                    target: id,
                    status: 'unreachable',
                })),
                prunedByMaxCost: search.prunedByMaxCost,
                metrics: {
                    statesExpanded: search.statesExpanded,
                    heapPushes: search.heapPushes,
                    stateSpaceBound: search.stateSpaceBound,
                },
            };
        }

        const budgets = params.budgets || [];
        const resolved = search.settledTargets.map((hit) => {
            const route = reconstructRoute(
                this.graph,
                search.startKey,
                hit.key,
                search.predecessors,
                this.graph.reliabilityMode
            );
            const budgetUsed = {};
            for (let b = 0; b < budgets.length; b += 1) {
                budgetUsed[budgets[b].dim] = hit.budgetVec[b];
            }
            return {
                target: hit.nodeId,
                status: 'found',
                route,
                budgetUsed,
            };
        });

        const settledMap = new Map();
        for (let i = 0; i < resolved.length; i += 1) {
            settledMap.set(resolved[i].target, resolved[i]);
        }

        const allResults = params.allTargets
            ? uniqueTargets.map(
                  (id) =>
                      settledMap.get(id) || {
                          target: id,
                          status: 'unreachable',
                      }
              )
            : resolved;

        return {
            found: true,
            status: 'found',
            nearest: resolved[0],
            targets: allResults,
            prunedByMaxCost: search.prunedByMaxCost,
            metrics: {
                statesExpanded: search.statesExpanded,
                heapPushes: search.heapPushes,
                stateSpaceBound: search.stateSpaceBound,
            },
        };
    }

    allDistances(params) {
        this.assertNodeExists(params.from, 'source');
        const search = this.runSearch({
            from: params.from,
            targetSet: null,
            stopOnFirstTarget: false,
            avoidNodes: params.avoidNodes,
            avoidEdges: params.avoidEdges,
            budgets: params.budgets,
            maxCost: params.maxCost,
            reverse: params.reverse,
        });

        const reachable = [];
        const unreachableNodes = [];
        const budgets = params.budgets || [];

        for (let i = 0; i < this.graph.nodes.length; i += 1) {
            const nodeId = this.graph.nodes[i].id;
            const best = search.bestNodeState.get(nodeId);
            if (best) {
                const route = reconstructRoute(
                    this.graph,
                    search.startKey,
                    best.key,
                    search.predecessors,
                    this.graph.reliabilityMode
                );
                const budgetUsed = {};
                for (let b = 0; b < budgets.length; b += 1) {
                    budgetUsed[budgets[b].dim] = best.budgetVec[b];
                }
                const entry = {
                    node: nodeId,
                    totalCost: route.totalCost,
                    hops: route.hops,
                    path: route.nodes,
                    edgeIds: route.edges.map((e) => e.id),
                };
                if (this.graph.reliabilityMode) {
                    entry.reliability = route.reliability;
                }
                if (budgets.length > 0) {
                    entry.budgetUsed = budgetUsed;
                }
                reachable.push(entry);
            } else {
                unreachableNodes.push(nodeId);
            }
        }

        reachable.sort((a, b) => {
            if (a.totalCost !== b.totalCost) {
                return a.totalCost - b.totalCost;
            }
            if (a.hops !== b.hops) {
                return a.hops - b.hops;
            }
            return a.node.localeCompare(b.node);
        });

        return {
            status: 'found',
            from: params.from,
            reachable,
            unreachableNodes: search.prunedByMaxCost ? [] : unreachableNodes,
            notReachedWithinMaxCost: search.prunedByMaxCost
                ? unreachableNodes
                : [],
            prunedByMaxCost: search.prunedByMaxCost,
            metrics: {
                statesExpanded: search.statesExpanded,
                heapPushes: search.heapPushes,
                stateSpaceBound: search.stateSpaceBound,
            },
        };
    }

    kShortestPaths(params) {
        const kLimit = params.k || 3;
        if (params.budgets && params.budgets.length > 0) {
            throw createSolverError(
                'cli_error',
                EXIT_CODES.CLI_ERROR,
                'k-paths does not support --budget; use "path" or "nearest" for constrained-budget routing.'
            );
        }
        this.assertNodeExists(params.from, 'source');
        this.assertNodeExists(params.to, 'target');

        const sharedCounter = { states: 0, heapPushes: 0 };
        const baseAvoidNodes = params.avoidNodes || new Set();
        const baseAvoidEdges = params.avoidEdges || new Set();

        const first = this.shortestPath({
            from: params.from,
            to: params.to,
            avoidNodes: baseAvoidNodes,
            avoidEdges: baseAvoidEdges,
            budgets: [],
            maxCost: params.maxCost,
            reverse: params.reverse,
            stateCounter: sharedCounter,
        });

        if (!first.found) {
            return {
                found: false,
                status: 'unreachable',
                requestedK: kLimit,
                paths: [],
                prunedByMaxCost: first.prunedByMaxCost,
                metrics: {
                    statesExpanded: sharedCounter.states,
                    heapPushes: sharedCounter.heapPushes,
                },
            };
        }

        function routeSignature(route) {
            const edgeSig = route.edges.map((e) => e.id).join('\u0001');
            return `${route.nodes.join('\u0000')}\u0002${edgeSig}`;
        }

        const accepted = [first.route];
        const candidateKeys = new Set([routeSignature(first.route)]);
        const candidates = createMinHeap((a, b) => {
            if (a.totalCost !== b.totalCost) {
                return a.totalCost - b.totalCost;
            }
            if (a.hops !== b.hops) {
                return a.hops - b.hops;
            }
            return a.sig.localeCompare(b.sig);
        });

        for (let k = 1; k < kLimit; k += 1) {
            const prevRoute = accepted[k - 1];
            const spurCount = prevRoute.edges.length;

            for (let i = 0; i < spurCount; i += 1) {
                const spurNode = prevRoute.nodes[i];
                const rootNodes = prevRoute.nodes.slice(0, i + 1);
                const rootEdges = prevRoute.edges.slice(0, i);

                const tempAvoidEdges = new Set(baseAvoidEdges);
                for (let p = 0; p < accepted.length; p += 1) {
                    const existing = accepted[p];
                    if (existing.edges.length > i) {
                        let sameRoot = existing.nodes[0] === rootNodes[0];
                        for (let r = 0; r < i && sameRoot; r += 1) {
                            if (
                                existing.nodes[r + 1] !== rootNodes[r + 1] ||
                                existing.edges[r].id !== rootEdges[r].id
                            ) {
                                sameRoot = false;
                            }
                        }
                        if (sameRoot) {
                            tempAvoidEdges.add(existing.edges[i].id);
                        }
                    }
                }

                const tempAvoidNodes = new Set(baseAvoidNodes);
                for (let r = 0; r < i; r += 1) {
                    tempAvoidNodes.add(rootNodes[r]);
                }

                let rootCost = 0;
                for (let r = 0; r < rootEdges.length; r += 1) {
                    rootCost = checkedAdd(
                        rootCost,
                        rootEdges[r].weight,
                        this.graph.allIntegers
                    );
                }

                let remainingMaxCost = null;
                if (params.maxCost !== null && params.maxCost !== undefined) {
                    remainingMaxCost = params.maxCost - rootCost;
                }

                if (remainingMaxCost === null || remainingMaxCost >= 0) {
                    const spur = this.shortestPath({
                        from: spurNode,
                        to: params.to,
                        avoidNodes: tempAvoidNodes,
                        avoidEdges: tempAvoidEdges,
                        budgets: [],
                        maxCost: remainingMaxCost,
                        reverse: params.reverse,
                        stateCounter: sharedCounter,
                    });

                    if (spur.found) {
                        const combinedNodes = rootNodes.concat(
                            spur.route.nodes.slice(1)
                        );
                        const combinedEdges = [];
                        let running = 0;
                        let reliabilityProduct = 1;
                        const allRawEdges = rootEdges.concat(spur.route.edges);
                        for (
                            let eIdx = 0;
                            eIdx < allRawEdges.length;
                            eIdx += 1
                        ) {
                            const ed = allRawEdges[eIdx];
                            running = checkedAdd(
                                running,
                                ed.weight,
                                this.graph.allIntegers
                            );
                            if (
                                this.graph.reliabilityMode &&
                                ed.probability !== null
                            ) {
                                reliabilityProduct *= ed.probability;
                            }
                            combinedEdges.push({
                                step: eIdx + 1,
                                id: ed.id,
                                from: ed.from,
                                to: ed.to,
                                weight: ed.weight,
                                cumulativeCost: running,
                                label: ed.label,
                                probability: ed.probability,
                                costs: ed.costs,
                            });
                        }

                        const combinedRoute = {
                            nodes: combinedNodes,
                            edges: combinedEdges,
                            hops: combinedEdges.length,
                            totalCost: running,
                        };
                        if (this.graph.reliabilityMode) {
                            combinedRoute.reliability = reliabilityProduct;
                        }
                        const sig = routeSignature(combinedRoute);
                        if (!candidateKeys.has(sig)) {
                            candidateKeys.add(sig);
                            candidates.push({
                                totalCost: combinedRoute.totalCost,
                                hops: combinedRoute.hops,
                                sig,
                                route: combinedRoute,
                            });
                        }
                    }
                }
            }

            if (candidates.size() === 0) {
                break;
            }
            const nextBest = candidates.pop();
            accepted.push(nextBest.route);
        }

        return {
            found: true,
            status: 'found',
            requestedK: kLimit,
            foundK: accepted.length,
            paths: accepted.map((route, idx) => ({
                rank: idx + 1,
                route,
            })),
            metrics: {
                statesExpanded: sharedCounter.states,
                heapPushes: sharedCounter.heapPushes,
            },
        };
    }
}

function sanitizeMermaidText(text) {
    return String(text)
        .replace(/\\/g, '\\\\')
        .replace(/"/g, "'")
        .replace(/[\r\n]+/g, ' ')
        .trim();
}

function formatMermaid(payload, graph) {
    const lines = [graph.directed ? 'flowchart LR' : 'graph LR'];
    const connector = graph.directed ? '-->' : '---';
    const optConnector = graph.directed ? '==>' : '===';

    const highlightedEdgeIds = new Set();
    const highlightedNodes = new Set();

    if (payload.command === 'path' && payload.result && payload.result.route) {
        payload.result.route.edges.forEach((e) => highlightedEdgeIds.add(e.id));
        payload.result.route.nodes.forEach((n) => highlightedNodes.add(n));
    } else if (
        payload.command === 'nearest' &&
        payload.result &&
        payload.result.nearest &&
        payload.result.nearest.route
    ) {
        payload.result.nearest.route.edges.forEach((e) =>
            highlightedEdgeIds.add(e.id)
        );
        payload.result.nearest.route.nodes.forEach((n) =>
            highlightedNodes.add(n)
        );
    } else if (
        payload.command === 'k-paths' &&
        payload.result &&
        Array.isArray(payload.result.paths) &&
        payload.result.paths.length > 0
    ) {
        payload.result.paths[0].route.edges.forEach((e) =>
            highlightedEdgeIds.add(e.id)
        );
        payload.result.paths[0].route.nodes.forEach((n) =>
            highlightedNodes.add(n)
        );
    }

    const useSubgraphOnly =
        graph.edges.length > MAX_MERMAID_FULL_EDGES &&
        highlightedEdgeIds.size > 0;
    const edgesToRender = useSubgraphOnly
        ? graph.edges.filter((e) => highlightedEdgeIds.has(e.id))
        : graph.edges;

    const nodeAlias = new Map();
    const nodesToRender = new Set();
    if (useSubgraphOnly) {
        highlightedNodes.forEach((n) => nodesToRender.add(n));
        lines.push(
            `    %% Showing optimal route subgraph only (full graph has ${graph.edges.length} edges)`
        );
    } else {
        graph.nodes.forEach((n) => nodesToRender.add(n.id));
    }

    let aliasIndex = 0;
    nodesToRender.forEach((nodeId) => {
        aliasIndex += 1;
        const safeId = `N${aliasIndex}`;
        nodeAlias.set(nodeId, safeId);
        const nodeInfo = graph.nodeMap.get(nodeId);
        const label = sanitizeMermaidText(nodeInfo ? nodeInfo.label : nodeId);
        lines.push(`    ${safeId}["${label}"]`);
    });

    for (let i = 0; i < edgesToRender.length; i += 1) {
        const edge = edgesToRender[i];
        const fromAlias = nodeAlias.get(edge.from);
        const toAlias = nodeAlias.get(edge.to);
        if (fromAlias && toAlias) {
            const isOpt = highlightedEdgeIds.has(edge.id);
            const arrow = isOpt ? optConnector : connector;
            const costText =
                graph.reliabilityMode && edge.probability !== null
                    ? `p=${edge.probability}`
                    : `${edge.weight}`;
            const edgeLabel = sanitizeMermaidText(
                edge.label
                    ? `${edge.id}: ${edge.label} (${costText})`
                    : `${edge.id} (${costText})`
            );
            lines.push(`    ${fromAlias} ${arrow}|"${edgeLabel}"| ${toAlias}`);
        }
    }

    if (highlightedNodes.size > 0) {
        const styledIds = [];
        highlightedNodes.forEach((n) => {
            if (nodeAlias.has(n)) {
                styledIds.push(nodeAlias.get(n));
            }
        });
        if (styledIds.length > 0) {
            lines.push('    classDef optimal stroke-width:3px;');
            lines.push(`    class ${styledIds.join(',')} optimal;`);
        }
    }

    return `${lines.join('\n')}\n`;
}

function formatRouteTable(route, unit) {
    const unitLabel = unit ? ` (${unit})` : '';
    const lines = [
        `| Step | From | Edge | To | Cost${unitLabel} | Cumulative | Label |`,
        '| --- | --- | --- | --- | --- | --- | --- |',
    ];
    if (route.edges.length === 0) {
        lines.push(
            `| 1 | ${route.nodes[0]} | - | ${route.nodes[0]} | 0 | 0 | source equals target |`
        );
    } else {
        for (let i = 0; i < route.edges.length; i += 1) {
            const e = route.edges[i];
            const safeLabel = (e.label || '-').replace(/\|/g, '\\|');
            lines.push(
                `| ${e.step} | ${e.from} | ${e.id} | ${e.to} | ${e.weight} | ${e.cumulativeCost} | ${safeLabel} |`
            );
        }
    }
    lines.push('');
    lines.push(
        `Total cost: ${route.totalCost}${unit ? ` ${unit}` : ''} (${route.hops} hop(s))`
    );
    if (route.reliability !== undefined) {
        lines.push(`Composite reliability: ${route.reliability}`);
    }
    return `${lines.join('\n')}\n`;
}

function formatTable(payload, graph) {
    const unit = graph ? graph.unit : null;
    if (payload.status !== 'found') {
        return `Status: ${payload.status}\n`;
    }
    if (payload.command === 'path') {
        return formatRouteTable(payload.result.route, unit);
    }
    if (payload.command === 'nearest') {
        const blocks = [
            `Nearest target: ${payload.result.nearest.target}`,
            '',
            formatRouteTable(payload.result.nearest.route, unit).trimEnd(),
        ];
        return `${blocks.join('\n')}\n`;
    }
    if (payload.command === 'k-paths') {
        const blocks = payload.result.paths.map(
            (entry) =>
                `### Plan ${entry.rank}\n\n${formatRouteTable(entry.route, unit).trimEnd()}`
        );
        return `${blocks.join('\n\n')}\n`;
    }
    if (payload.command === 'distances') {
        const unitLabel = unit ? ` (${unit})` : '';
        const lines = [
            `| Rank | Node | Cost${unitLabel} | Hops | Path |`,
            '| --- | --- | --- | --- | --- |',
        ];
        for (let i = 0; i < payload.result.reachable.length; i += 1) {
            const item = payload.result.reachable[i];
            lines.push(
                `| ${i + 1} | ${item.node} | ${item.totalCost} | ${item.hops} | ${item.path.join(' -> ')} |`
            );
        }
        return `${lines.join('\n')}\n`;
    }
    return `${JSON.stringify(payload, null, 2)}\n`;
}

function formatOutput(payload, format, graph) {
    if (format === 'json') {
        return `${JSON.stringify(payload, null, 2)}\n`;
    }
    if (format === 'mermaid') {
        if (!graph) {
            throw createSolverError(
                'cli_error',
                EXIT_CODES.CLI_ERROR,
                'Mermaid format requires a parsed graph.'
            );
        }
        return formatMermaid(payload, graph);
    }
    if (format === 'table') {
        return formatTable(payload, graph);
    }
    throw createSolverError(
        'cli_error',
        EXIT_CODES.CLI_ERROR,
        `Unsupported --format "${format}". Expected: json, mermaid, table.`
    );
}

function buildHelpText() {
    return [
        `Usage: node solve.node.mjs <command> [options]`,
        '',
        'Deterministic Dijkstra and Yen K-shortest-path solver for SDLC/DevOps graphs.',
        '',
        'Commands:',
        '  path       Minimum-cost path from --from to --to',
        '  nearest    Closest target in --targets <a,b,c> (add --all-targets for every target)',
        '  distances  All-distances reachability / blast-radius map from --from',
        '  k-paths    Top-K loopless paths from --from to --to (Yen algorithm, --k 1..20)',
        '  validate   Validate graph model, numeric types, non-negativity, and applicability',
        '  selftest   Run built-in solver verification suite',
        '  help       Show this help text',
        '',
        'Options:',
        '  --input <file|->            Graph file path or "-" for stdin (required for graph commands)',
        '  --input-format <fmt>        auto (default), json, csv, dot',
        '  --from <node>               Source node ID',
        '  --to <node>                 Target node ID (path, k-paths)',
        '  --targets <a,b,c>           Comma-separated target node IDs (nearest; repeatable)',
        '  --all-targets               Settle all requested targets in nearest mode',
        '  --k <1..20>                 Number of loopless paths for k-paths (default: 3)',
        '  --undirected                Treat all edges as bidirectional',
        '  --reverse                   Reverse all edge directions (all-sources to one target)',
        '  --avoid-node <id[,id2]>     Exclude node(s) for what-if/failover analysis (repeatable)',
        '  --avoid-edge <id[,id2]>     Exclude edge ID(s) (repeatable)',
        '  --budget <dim=max>          Discrete integer budget constraint (repeatable; path/nearest/distances)',
        '  --reliability               Treat weights/probabilities in (0, 1] as -ln(p) additive costs',
        '  --default-weight <n>        Explicit non-negative weight for unweighted DOT edges',
        '  --max-cost <n>              Prune paths exceeding cost n',
        '  --max-states <n>            Max settled states guard (default: 200000)',
        '  --max-heap <n>              Max heap entries guard (default: 500000)',
        '  --max-input-bytes <n>       Max input payload bytes (default: 2097152)',
        '  --format <fmt>              Output format: json (default), mermaid, table',
        '  --version                   Print solver version',
        '  -h, --help                  Show this help text',
        '',
        'Exit codes:',
        '  0  found / valid / selftest passed',
        '  1  unreachable (valid model, no feasible route)',
        '  2  CLI argument or file read error',
        '  3  invalid_input (syntax, type, missing node, overflow, empty targets)',
        '  4  inapplicable_model (negative weight; use Bellman-Ford or DAG DP)',
        '  5  resource_limit (exceeded max-states, max-heap, or max-input-bytes)',
        '',
        'Examples:',
        '  node solve.node.mjs path --input migration.json --from v1 --to v4 --format json',
        '  node solve.node.mjs k-paths --input migration.json --from v1 --to v4 --k 3 --format table',
        '  node solve.node.mjs nearest --input infra.dot --default-weight 1 --from app --targets db1,db2',
        '  node solve.node.mjs distances --input deps.csv --from auth-lib --reverse --max-cost 3',
        '',
    ].join('\n');
}

function appendSplitItems(targetList, rawValue, flagName) {
    if (typeof rawValue !== 'string' || rawValue.trim().length === 0) {
        throw createSolverError(
            'cli_error',
            EXIT_CODES.CLI_ERROR,
            `${flagName} requires a non-empty value.`
        );
    }
    const parts = rawValue.split(',');
    for (let i = 0; i < parts.length; i += 1) {
        const trimmed = parts[i].trim();
        if (trimmed.length === 0) {
            throw createSolverError(
                'cli_error',
                EXIT_CODES.CLI_ERROR,
                `${flagName} contains an empty item in "${rawValue}".`
            );
        }
        targetList.push(trimmed);
    }
}

function parseCliArgs(argv) {
    if (argv.length === 0) {
        return { command: 'empty' };
    }
    if (argv[0] === '--help' || argv[0] === '-h' || argv[0] === 'help') {
        return { command: 'help' };
    }
    if (argv[0] === '--version' || argv[0] === 'version') {
        return { command: 'version' };
    }

    const command = argv[0];
    const validCommands = new Set([
        'path',
        'nearest',
        'distances',
        'k-paths',
        'validate',
        'selftest',
    ]);
    if (!validCommands.has(command)) {
        throw createSolverError(
            'cli_error',
            EXIT_CODES.CLI_ERROR,
            `Unknown command "${command}". Run with --help for valid commands.`
        );
    }

    const opts = {
        command,
        input: null,
        inputFormat: 'auto',
        from: null,
        to: null,
        targets: [],
        allTargets: false,
        k: 3,
        undirected: false,
        reverse: false,
        avoidNodes: [],
        avoidEdges: [],
        budgets: [],
        reliability: false,
        defaultWeight: null,
        maxCost: null,
        maxStates: DEFAULT_MAX_STATES,
        maxHeap: DEFAULT_MAX_HEAP,
        maxInputBytes: DEFAULT_MAX_INPUT_BYTES,
        format: 'json',
    };

    const budgetDimsSeen = new Set();

    function requireArg(index, flag) {
        if (index + 1 >= argv.length) {
            throw createSolverError(
                'cli_error',
                EXIT_CODES.CLI_ERROR,
                `Option ${flag} requires a value.`
            );
        }
        return argv[index + 1];
    }

    let i = 1;
    while (i < argv.length) {
        const token = argv[i];
        if (token === '--help' || token === '-h') {
            return { command: 'help' };
        }
        if (token === '--version') {
            return { command: 'version' };
        }
        if (token === '--input') {
            opts.input = requireArg(i, token);
            i += 2;
        } else if (token === '--input-format') {
            opts.inputFormat = requireArg(i, token).toLowerCase();
            i += 2;
        } else if (token === '--from') {
            opts.from = requireArg(i, token);
            i += 2;
        } else if (token === '--to') {
            opts.to = requireArg(i, token);
            i += 2;
        } else if (token === '--targets') {
            appendSplitItems(opts.targets, requireArg(i, token), token);
            i += 2;
        } else if (token === '--all-targets') {
            opts.allTargets = true;
            i += 1;
        } else if (token === '--k') {
            opts.k = parsePositiveIntOption(
                requireArg(i, token),
                token,
                MAX_K_PATHS
            );
            i += 2;
        } else if (token === '--undirected') {
            opts.undirected = true;
            i += 1;
        } else if (token === '--reverse') {
            opts.reverse = true;
            i += 1;
        } else if (token === '--avoid-node') {
            appendSplitItems(opts.avoidNodes, requireArg(i, token), token);
            i += 2;
        } else if (token === '--avoid-edge') {
            appendSplitItems(opts.avoidEdges, requireArg(i, token), token);
            i += 2;
        } else if (token === '--budget') {
            const spec = requireArg(i, token).trim();
            const match = BUDGET_SPEC_RE.exec(spec);
            if (!match) {
                throw createSolverError(
                    'cli_error',
                    EXIT_CODES.CLI_ERROR,
                    `Invalid --budget "${spec}". Expected "<dimension>=<non-negative-integer>".`
                );
            }
            const dim = match[1];
            const maxVal = Number.parseInt(match[2], 10);
            if (!Number.isSafeInteger(maxVal)) {
                throw createSolverError(
                    'cli_error',
                    EXIT_CODES.CLI_ERROR,
                    `Budget limit for "${dim}" exceeds safe integer range.`
                );
            }
            if (budgetDimsSeen.has(dim)) {
                throw createSolverError(
                    'cli_error',
                    EXIT_CODES.CLI_ERROR,
                    `Duplicate --budget dimension "${dim}".`
                );
            }
            budgetDimsSeen.add(dim);
            opts.budgets.push({ dim, max: maxVal });
            i += 2;
        } else if (token === '--reliability') {
            opts.reliability = true;
            i += 1;
        } else if (token === '--default-weight') {
            opts.defaultWeight = parseNonNegativeNumberOption(
                requireArg(i, token),
                token
            );
            i += 2;
        } else if (token === '--max-cost') {
            opts.maxCost = parseNonNegativeNumberOption(
                requireArg(i, token),
                token
            );
            i += 2;
        } else if (token === '--max-states') {
            opts.maxStates = parsePositiveIntOption(
                requireArg(i, token),
                token,
                5000000
            );
            i += 2;
        } else if (token === '--max-heap') {
            opts.maxHeap = parsePositiveIntOption(
                requireArg(i, token),
                token,
                10000000
            );
            i += 2;
        } else if (token === '--max-input-bytes') {
            opts.maxInputBytes = parsePositiveIntOption(
                requireArg(i, token),
                token,
                50 * 1024 * 1024
            );
            i += 2;
        } else if (token === '--format') {
            opts.format = requireArg(i, token).toLowerCase();
            i += 2;
        } else {
            throw createSolverError(
                'cli_error',
                EXIT_CODES.CLI_ERROR,
                `Unknown option "${token}". Run with --help for usage.`
            );
        }
    }

    return opts;
}

function readBoundedInput(inputPath, maxBytes, stdinText) {
    if (inputPath === '-') {
        const text =
            typeof stdinText === 'string'
                ? stdinText
                : fs.readFileSync(0, 'utf8');
        if (Buffer.byteLength(text, 'utf8') > maxBytes) {
            throw createSolverError(
                'resource_limit',
                EXIT_CODES.RESOURCE_LIMIT,
                `Stdin input exceeds --max-input-bytes limit (${maxBytes}).`
            );
        }
        return text;
    }

    let stats = null;
    try {
        stats = fs.statSync(inputPath);
    } catch (err) {
        throw createSolverError(
            'cli_error',
            EXIT_CODES.CLI_ERROR,
            `Cannot read input file "${inputPath}": ${err.message}`
        );
    }
    if (!stats.isFile()) {
        throw createSolverError(
            'cli_error',
            EXIT_CODES.CLI_ERROR,
            `Input path "${inputPath}" is not a regular file.`
        );
    }
    if (stats.size > maxBytes) {
        throw createSolverError(
            'resource_limit',
            EXIT_CODES.RESOURCE_LIMIT,
            `Input file "${inputPath}" (${stats.size} bytes) exceeds --max-input-bytes limit (${maxBytes}).`
        );
    }
    return fs.readFileSync(inputPath, 'utf8');
}

function runSelftest() {
    const checks = [];

    function recordCheck(name, fn) {
        try {
            fn();
            checks.push({ name, passed: true });
        } catch (err) {
            checks.push({ name, passed: false, error: err.message });
        }
    }

    recordCheck('nominal_weighted_path', () => {
        const g = buildGraphModel({
            directed: true,
            edges: [
                { id: 'e1', from: 'v1', to: 'v2', weight: 10 },
                { id: 'e2', from: 'v1', to: 'v3', weight: 3 },
                { id: 'e3', from: 'v3', to: 'v2', weight: 4 },
            ],
        });
        const res = new DijkstraSolver(g).shortestPath({
            from: 'v1',
            to: 'v2',
        });
        if (!res.found || res.route.totalCost !== 7) {
            throw new Error('Expected optimal cost 7 via v1->v3->v2');
        }
    });

    recordCheck('zero_weight_cycle_safety', () => {
        const g = buildGraphModel({
            directed: true,
            edges: [
                { id: 'z1', from: 'a', to: 'b', weight: 0 },
                { id: 'z2', from: 'b', to: 'a', weight: 0 },
                { id: 'z3', from: 'b', to: 'c', weight: 0 },
            ],
        });
        const res = new DijkstraSolver(g).shortestPath({ from: 'a', to: 'c' });
        if (!res.found || res.route.totalCost !== 0 || res.route.hops !== 2) {
            throw new Error('Zero-weight cycle broke strict relaxation');
        }
    });

    recordCheck('parallel_edges_and_avoid_edge', () => {
        const g = buildGraphModel({
            directed: true,
            edges: [
                { id: 'fast', from: 'a', to: 'b', weight: 2 },
                { id: 'backup', from: 'a', to: 'b', weight: 8 },
            ],
        });
        const solver = new DijkstraSolver(g);
        const r1 = solver.shortestPath({ from: 'a', to: 'b' });
        const r2 = solver.shortestPath({
            from: 'a',
            to: 'b',
            avoidEdges: new Set(['fast']),
        });
        if (
            r1.route.edges[0].id !== 'fast' ||
            r2.route.edges[0].id !== 'backup'
        ) {
            throw new Error('Parallel edge identity or avoid-edge failed');
        }
    });

    recordCheck('negative_weight_rejected', () => {
        let rejected = false;
        try {
            buildGraphModel({
                edges: [{ from: 'a', to: 'b', weight: -1 }],
            });
        } catch (err) {
            rejected =
                err.status === 'inapplicable_model' &&
                err.exitCode === EXIT_CODES.INAPPLICABLE_MODEL;
        }
        if (!rejected) {
            throw new Error('Negative weight was not rejected properly');
        }
    });

    recordCheck('safe_integer_overflow_rejected', () => {
        const g = buildGraphModel({
            edges: [
                { from: 'a', to: 'b', weight: Number.MAX_SAFE_INTEGER },
                { from: 'b', to: 'c', weight: 1 },
            ],
        });
        let rejected = false;
        try {
            new DijkstraSolver(g).shortestPath({ from: 'a', to: 'c' });
        } catch (err) {
            rejected = err.status === 'invalid_input';
        }
        if (!rejected) {
            throw new Error('Safe integer overflow was not detected');
        }
    });

    recordCheck('nearest_target_selection', () => {
        const g = buildGraphModel({
            edges: [
                { from: 'app', to: 'mirror-a', weight: 40 },
                { from: 'app', to: 'mirror-b', weight: 12 },
            ],
        });
        const res = new DijkstraSolver(g).nearestTarget({
            from: 'app',
            targets: ['mirror-a', 'mirror-b'],
        });
        if (!res.found || res.nearest.target !== 'mirror-b') {
            throw new Error('Nearest target failed to select mirror-b');
        }
    });

    recordCheck('yen_k_shortest_paths', () => {
        const g = buildGraphModel({
            edges: [
                { id: 'e1', from: 's', to: 't', weight: 10 },
                { id: 'e2', from: 's', to: 'a', weight: 2 },
                { id: 'e3', from: 'a', to: 't', weight: 3 },
                { id: 'e4', from: 's', to: 'b', weight: 4 },
                { id: 'e5', from: 'b', to: 't', weight: 4 },
            ],
        });
        const res = new DijkstraSolver(g).kShortestPaths({
            from: 's',
            to: 't',
            k: 3,
        });
        const costs = res.paths.map((p) => p.route.totalCost).join(',');
        if (costs !== '5,8,10') {
            throw new Error(`Expected K-path costs 5,8,10; got ${costs}`);
        }
    });

    recordCheck('discrete_budget_and_reliability', () => {
        const g = buildGraphModel({
            edges: [
                {
                    id: 'fast-risky',
                    from: 'v1',
                    to: 'v3',
                    weight: 5,
                    costs: { restarts: 2 },
                },
                {
                    id: 'step-1',
                    from: 'v1',
                    to: 'v2',
                    weight: 4,
                    costs: { restarts: 0 },
                },
                {
                    id: 'step-2',
                    from: 'v2',
                    to: 'v3',
                    weight: 4,
                    costs: { restarts: 1 },
                },
            ],
        });
        const constrained = new DijkstraSolver(g).shortestPath({
            from: 'v1',
            to: 'v3',
            budgets: [{ dim: 'restarts', max: 1 }],
        });
        if (!constrained.found || constrained.route.totalCost !== 8) {
            throw new Error('Budget expansion failed to pick cost-8 route');
        }

        const relGraph = buildGraphModel(
            {
                edges: [
                    { id: 'r1', from: 'a', to: 'b', probability: 0.9 },
                    { id: 'r2', from: 'b', to: 'c', probability: 0.9 },
                    { id: 'r3', from: 'a', to: 'c', probability: 0.75 },
                ],
            },
            { reliability: true }
        );
        const relRes = new DijkstraSolver(relGraph).shortestPath({
            from: 'a',
            to: 'c',
        });
        if (
            !relRes.found ||
            Math.abs(relRes.route.reliability - 0.81) > 1e-12
        ) {
            throw new Error('Reliability mode failed to pick 0.81 route');
        }
    });

    const passed = checks.every((c) => c.passed);
    return {
        status: passed ? 'ok' : 'failed',
        version: VERSION,
        checks,
        passed,
    };
}

function runCli(argv, io = {}) {
    const stdout = io.stdout || process.stdout;
    const stderr = io.stderr || process.stderr;
    const { stdinText } = io;

    try {
        const opts = parseCliArgs(argv);
        if (opts.command === 'empty') {
            stderr.write(
                'Error: missing command. Run "node solve.node.mjs --help" for usage.\n'
            );
            return EXIT_CODES.CLI_ERROR;
        }
        if (opts.command === 'help') {
            stdout.write(buildHelpText());
            return EXIT_CODES.OK;
        }
        if (opts.command === 'version') {
            stdout.write(`ops-shortest-path-solver ${VERSION}\n`);
            return EXIT_CODES.OK;
        }
        if (opts.command === 'selftest') {
            const report = runSelftest();
            stdout.write(`${JSON.stringify(report, null, 2)}\n`);
            return report.passed ? EXIT_CODES.OK : EXIT_CODES.UNREACHABLE;
        }

        if (!opts.input) {
            throw createSolverError(
                'cli_error',
                EXIT_CODES.CLI_ERROR,
                `Command "${opts.command}" requires --input <file|->.`
            );
        }

        const rawText = readBoundedInput(
            opts.input,
            opts.maxInputBytes,
            stdinText
        );
        const graph = parseGraphText(rawText, {
            inputPath: opts.input,
            inputFormat: opts.inputFormat,
            undirected: opts.undirected,
            reliability: opts.reliability,
            defaultWeight: opts.defaultWeight,
        });
        const solver = new DijkstraSolver(graph, {
            maxStates: opts.maxStates,
            maxHeap: opts.maxHeap,
        });

        const avoidNodes = new Set(opts.avoidNodes);
        const avoidEdges = new Set(opts.avoidEdges);

        if (opts.command === 'validate') {
            const payload = {
                status: 'valid',
                command: 'validate',
                graph: solver.getGraphSummary(),
                assumptions: graph.assumptions,
            };
            stdout.write(formatOutput(payload, opts.format, graph));
            return EXIT_CODES.OK;
        }

        if (!opts.from) {
            throw createSolverError(
                'cli_error',
                EXIT_CODES.CLI_ERROR,
                `Command "${opts.command}" requires --from <node>.`
            );
        }

        let result = null;
        let exitCode = EXIT_CODES.OK;

        if (opts.command === 'path') {
            if (!opts.to) {
                throw createSolverError(
                    'cli_error',
                    EXIT_CODES.CLI_ERROR,
                    'Command "path" requires --to <node>.'
                );
            }
            result = solver.shortestPath({
                from: opts.from,
                to: opts.to,
                avoidNodes,
                avoidEdges,
                budgets: opts.budgets,
                maxCost: opts.maxCost,
                reverse: opts.reverse,
            });
            exitCode = result.found ? EXIT_CODES.OK : EXIT_CODES.UNREACHABLE;
        } else if (opts.command === 'nearest') {
            if (opts.targets.length === 0) {
                throw createSolverError(
                    'invalid_input',
                    EXIT_CODES.INVALID_INPUT,
                    'Command "nearest" requires a non-empty --targets <a,b,c> list.'
                );
            }
            result = solver.nearestTarget({
                from: opts.from,
                targets: opts.targets,
                allTargets: opts.allTargets,
                avoidNodes,
                avoidEdges,
                budgets: opts.budgets,
                maxCost: opts.maxCost,
                reverse: opts.reverse,
            });
            exitCode = result.found ? EXIT_CODES.OK : EXIT_CODES.UNREACHABLE;
        } else if (opts.command === 'distances') {
            result = solver.allDistances({
                from: opts.from,
                avoidNodes,
                avoidEdges,
                budgets: opts.budgets,
                maxCost: opts.maxCost,
                reverse: opts.reverse,
            });
            exitCode = EXIT_CODES.OK;
        } else if (opts.command === 'k-paths') {
            if (!opts.to) {
                throw createSolverError(
                    'cli_error',
                    EXIT_CODES.CLI_ERROR,
                    'Command "k-paths" requires --to <node>.'
                );
            }
            result = solver.kShortestPaths({
                from: opts.from,
                to: opts.to,
                k: opts.k,
                avoidNodes,
                avoidEdges,
                maxCost: opts.maxCost,
                reverse: opts.reverse,
            });
            exitCode = result.found ? EXIT_CODES.OK : EXIT_CODES.UNREACHABLE;
        }

        const payload = {
            status: result.status,
            command: opts.command,
            options: {
                from: opts.from,
                to: opts.to,
                targets: opts.targets.length > 0 ? opts.targets : undefined,
                reverse: opts.reverse,
                undirected: !graph.directed,
                reliability: opts.reliability,
                maxCost: opts.maxCost,
                avoidNodes: opts.avoidNodes,
                avoidEdges: opts.avoidEdges,
                budgets: opts.budgets,
            },
            result,
            graph: solver.getGraphSummary(),
            assumptions: graph.assumptions,
        };
        stdout.write(formatOutput(payload, opts.format, graph));
        return exitCode;
    } catch (err) {
        const status = err.status || 'cli_error';
        const exitCode =
            typeof err.exitCode === 'number'
                ? err.exitCode
                : EXIT_CODES.CLI_ERROR;
        const errObj = {
            status,
            exitCode,
            error: err.message,
        };
        if (err.details) {
            errObj.details = err.details;
        }
        stderr.write(`${JSON.stringify(errObj)}\n`);
        return exitCode;
    }
}

export {
    DijkstraSolver,
    EXIT_CODES,
    VERSION,
    buildGraphModel,
    checkedAdd,
    formatOutput,
    parseCliArgs,
    parseGraphText,
    runCli,
    runSelftest,
};

const isDirectExecution =
    process.argv[1] !== undefined &&
    path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);

if (isDirectExecution) {
    process.exitCode = runCli(process.argv.slice(2));
}

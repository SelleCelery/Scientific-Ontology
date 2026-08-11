#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

import { browsePayload, searchDocuments } from "../navigator/dist/search-core.js";
import { graphSubgraph, resolveGraphNode, traceGraph } from "../navigator/dist/graph-core.js";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const index = JSON.parse(fs.readFileSync(path.join(root, "tools/docs_index.json"), "utf8"));
const graph = JSON.parse(fs.readFileSync(path.join(root, "tools/docs_graph.json"), "utf8"));

function run(command, args) {
  const result = spawnSync(command, args, { cwd: root, encoding: "utf8" });
  if (result.status !== 0) {
    process.stderr.write(result.stdout || "");
    process.stderr.write(result.stderr || "");
    throw new Error(`${command} ${args.join(" ")} failed with exit ${result.status}`);
  }
  return result.stdout;
}

function loadYamlViaPython(relativePath) {
  const code = [
    "import json, sys, yaml",
    "from pathlib import Path",
    "data=yaml.safe_load(Path(sys.argv[1]).read_text(encoding='utf-8')) or {}",
    "print(json.dumps(data, ensure_ascii=False))",
  ].join(";");
  return JSON.parse(run("python", ["-c", code, path.join(root, relativePath)]));
}

function stableEdgeKeys(payload) {
  return (payload.edges ?? []).map((edge) => `${edge.from}|${edge.relation}|${edge.to}`).sort();
}

function stableNodeIds(payload) {
  return (payload.nodes ?? []).map((node) => String(node.id)).sort();
}

function assertEqual(actual, expected, label) {
  const a = JSON.stringify(actual);
  const b = JSON.stringify(expected);
  if (a !== b) {
    console.error(`FAIL ${label}`);
    console.error("  TS:", a.slice(0, 1600));
    console.error("  PY:", b.slice(0, 1600));
    return false;
  }
  console.log(`PASS ${label}`);
  return true;
}

let failures = 0;
const searchTests = loadYamlViaPython("tools/docs_search_tests.yml");
for (const test of searchTests.tests ?? []) {
  const mode = String(test.mode ?? "auto");
  const ts = searchDocuments(String(test.query), index, mode, 5, "both");
  const py = JSON.parse(
    run("python", [
      "scripts/query_docs.py",
      "search",
      String(test.query),
      "--mode",
      mode,
      "--limit",
      "5",
      "--json",
    ]),
  );
  const tsComparable = {
    mode: ts.mode,
    results: ts.results.map((r) => ({
      doc_id: r.doc_id,
      score: r.score,
      direct_match_count: r.direct_match_count,
      matches: (r.matches ?? []).map((m) => ({
        field: m.field,
        method: m.method,
        contribution: Number(Number(m.contribution).toFixed(12)),
        expansion_group: m.expansion_group ?? null,
        text: m.text,
      })),
    })),
  };
  const pyComparable = {
    mode: py.mode,
    results: (py.results ?? []).map((r) => ({
      doc_id: r.doc_id,
      score: r.score,
      direct_match_count: r.direct_match_count,
      matches: (r.matches ?? []).map((m) => ({
        field: m.field,
        method: m.method,
        contribution: Number(Number(m.contribution).toFixed(12)),
        expansion_group: m.expansion_group ?? null,
        text: m.text,
      })),
    })),
  };
  if (!assertEqual(tsComparable, pyComparable, `search:${test.id}`)) failures += 1;
}

for (const test of searchTests.browse_tests ?? []) {
  const topic = String(test.topic);
  const ts = browsePayload(index, topic);
  const py = JSON.parse(run("python", ["scripts/query_docs.py", "browse", topic, "--json"]));
  const tsComparable = {
    topic: ts.topic,
    documents: (ts.documents ?? []).map((doc) => doc.doc_id),
  };
  const pyComparable = {
    topic: py.topic,
    documents: (py.documents ?? []).map((doc) => doc.doc_id),
  };
  if (!assertEqual(tsComparable, pyComparable, `browse:${test.id}`)) failures += 1;
}

const graphTests = loadYamlViaPython("tools/docs_graph_tests.yml");
for (const test of graphTests.tests ?? []) {
  const query = test.from ?? test.from_label_contains;
  const type = test.from_type ? String(test.from_type) : undefined;
  let tsRoot;
  try {
    tsRoot = resolveGraphNode(graph, String(query), type);
  } catch (error) {
    console.error(`FAIL graph:${test.id}: ${error.message}`);
    failures += 1;
    continue;
  }
  const ts = graphSubgraph(graph, tsRoot, 1);
  const py = JSON.parse(run("python", ["scripts/query_docs.py", "graph", String(query), "--depth", "1", "--json"]));
  const ok = assertEqual(
    { root: ts.root, nodes: stableNodeIds(ts), edges: stableEdgeKeys(ts) },
    { root: py.root, nodes: stableNodeIds(py), edges: stableEdgeKeys(py) },
    `graph:${test.id}`,
  );
  if (!ok) failures += 1;
}

for (const test of graphTests.path_tests ?? []) {
  const sourceQuery = String(test.from ?? test.from_label_contains ?? "");
  const sourceType = test.from_type ? String(test.from_type) : undefined;
  const targetQuery = String(test.to ?? "");
  const directed = Boolean(test.directed ?? false);
  const maxDepth = Number(test.max_depth ?? 6);
  let source;
  let target;
  try {
    source = resolveGraphNode(graph, sourceQuery, sourceType);
    target = resolveGraphNode(graph, targetQuery);
  } catch (error) {
    console.error(`FAIL trace:${test.id}: ${error.message}`);
    failures += 1;
    continue;
  }
  const ts = traceGraph(graph, source, target, directed, maxDepth);
  const args = ["scripts/query_docs.py", "trace", sourceQuery, targetQuery, "--max-depth", String(maxDepth), "--json"];
  if (directed) args.push("--directed");
  const py = JSON.parse(run("python", args));
  const reduce = (payload) => payload ? {
    from: payload.from,
    to: payload.to,
    directed: payload.directed,
    steps: (payload.steps ?? []).map((step) => ({ from: step.from, to: step.to, direction: step.direction, relation: step.relation })),
  } : null;
  if (!assertEqual(reduce(ts), reduce(py), `trace:${test.id}`)) failures += 1;
}

if (failures) {
  console.error(`\nWeb parity: ${failures} failure(s)`);
  process.exit(1);
}
console.log("\nWeb parity: PASS");

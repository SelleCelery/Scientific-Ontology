import { normalizeText, type JsonObject } from "./search-core.js";

function lexicalCompare(a: string, b: string): number {
  return a < b ? -1 : a > b ? 1 : 0;
}

export function graphNodeLabel(node: JsonObject, lang = "ja"): string {
  if (node.type === "document" || node.type === "observed_document") {
    const title = node.title ?? {};
    return String(title[lang] || title.ja || title.en || node.key || node.id);
  }
  const label = node.label ?? {};
  if (label && typeof label === "object") {
    return String(label[lang] || label.ja || label.en || label.raw || node.key || node.id);
  }
  return String(node.key || node.id);
}

export function graphNodeMap(graph: JsonObject): Map<string, JsonObject> {
  const result = new Map<string, JsonObject>();
  for (const node of graph.nodes ?? []) if (node?.id) result.set(String(node.id), node);
  return result;
}

export function resolveGraphNode(graph: JsonObject, query: string, nodeType?: string): string {
  const nodes = graphNodeMap(graph);
  if (nodes.has(query) && (!nodeType || nodes.get(query)?.type === nodeType)) return query;
  for (const prefix of ["doc", "observed", "concept", "topic", "term", "layer", "artifact"]) {
    const candidate = `${prefix}:${query}`;
    if (nodes.has(candidate) && (!nodeType || nodes.get(candidate)?.type === nodeType)) return candidate;
  }
  const norm = normalizeText(query);
  const matches: string[] = [];
  for (const [nodeId, node] of nodes) {
    if (nodeType && node.type !== nodeType) continue;
    const label = node.label ?? {};
    const values = [nodeId, String(node.key ?? ""), graphNodeLabel(node, "ja"), graphNodeLabel(node, "en"), String(label.raw ?? "")];
    if (values.filter(Boolean).some((value) => normalizeText(value) === norm)) matches.push(nodeId);
  }
  if (matches.length === 1) return matches[0];
  if (matches.length > 1) throw new Error(`Ambiguous graph node '${query}': ${matches.slice(0, 8).join(", ")}`);

  const contains: string[] = [];
  if (norm.length >= 3) {
    for (const [nodeId, node] of nodes) {
      if (nodeType && node.type !== nodeType) continue;
      const label = node.label ?? {};
      const values = [String(node.key ?? ""), graphNodeLabel(node, "ja"), graphNodeLabel(node, "en"), String(label.raw ?? "")];
      if (values.filter(Boolean).some((value) => normalizeText(value).includes(norm))) contains.push(nodeId);
    }
  }
  if (contains.length === 1) return contains[0];
  if (contains.length > 1) throw new Error(`Ambiguous graph node '${query}': ${contains.slice(0, 8).join(", ")}`);
  throw new Error(`Unknown graph node: ${query}`);
}

export function graphSubgraph(graph: JsonObject, startId: string, depth = 1, relation?: string): JsonObject {
  const nodes = graphNodeMap(graph);
  const allEdges = (graph.edges ?? []).filter((edge: any) => edge && typeof edge === "object");
  const selectedNodes = new Set<string>([startId]);
  let frontier = new Set<string>([startId]);
  const selectedEdges: JsonObject[] = [];
  const seenEdgeKeys = new Set<string>();
  for (let i = 0; i < Math.max(0, depth); i += 1) {
    const nextFrontier = new Set<string>();
    for (const edge of allEdges) {
      if (relation && String(edge.relation) !== relation) continue;
      const source = String(edge.from);
      const target = String(edge.to);
      if (frontier.has(source) || frontier.has(target)) {
        const key = `${source}\u0000${String(edge.relation)}\u0000${target}`;
        if (!seenEdgeKeys.has(key)) {
          selectedEdges.push(edge);
          seenEdgeKeys.add(key);
        }
        if (!selectedNodes.has(source)) nextFrontier.add(source);
        if (!selectedNodes.has(target)) nextFrontier.add(target);
      }
    }
    for (const id of nextFrontier) selectedNodes.add(id);
    frontier = nextFrontier;
    if (!frontier.size) break;
  }
  return {
    root: startId,
    depth,
    nodes: Array.from(selectedNodes)
      .sort(lexicalCompare)
      .filter((id) => nodes.has(id))
      .map((id) => nodes.get(id)),
    edges: selectedEdges.sort((a, b) =>
      lexicalCompare(String(a.from), String(b.from)) ||
      lexicalCompare(String(a.relation), String(b.relation)) ||
      lexicalCompare(String(a.to), String(b.to)),
    ),
  };
}

export function traceGraph(graph: JsonObject, sourceId: string, targetId: string, directed = false, maxDepth = 6): JsonObject | null {
  const adjacency = new Map<string, Array<{ next: string; edge: JsonObject; direction: string }>>();
  for (const edge of graph.edges ?? []) {
    const source = String(edge.from);
    const target = String(edge.to);
    if (!adjacency.has(source)) adjacency.set(source, []);
    adjacency.get(source)!.push({ next: target, edge, direction: "forward" });
    if (!directed) {
      if (!adjacency.has(target)) adjacency.set(target, []);
      adjacency.get(target)!.push({ next: source, edge, direction: "reverse" });
    }
  }
  const queue: Array<{ node: string; steps: JsonObject[] }> = [{ node: sourceId, steps: [] }];
  const visited = new Set<string>([sourceId]);
  while (queue.length) {
    const current = queue.shift()!;
    if (current.node === targetId) return { from: sourceId, to: targetId, directed, steps: current.steps };
    if (current.steps.length >= maxDepth) continue;
    for (const item of adjacency.get(current.node) ?? []) {
      if (visited.has(item.next)) continue;
      visited.add(item.next);
      queue.push({
        node: item.next,
        steps: current.steps.concat({
          from: current.node,
          to: item.next,
          direction: item.direction,
          relation: String(item.edge.relation),
          edge: item.edge,
        }),
      });
    }
  }
  return null;
}

export function layerSummaries(graph: JsonObject): JsonObject[] {
  const nodes = graphNodeMap(graph);
  const summaries = new Map<string, JsonObject>();
  for (const node of graph.nodes ?? []) {
    if (node.type !== "layer") continue;
    summaries.set(String(node.id), {
      id: String(node.id),
      key: String(node.key ?? ""),
      path: String(node.path ?? ""),
      label: node.label ?? {},
      registered: [],
      observed: [],
    });
  }
  for (const edge of graph.edges ?? []) {
    if (edge.relation !== "placed_in") continue;
    const layer = summaries.get(String(edge.to));
    const source = nodes.get(String(edge.from));
    if (!layer || !source) continue;
    if (source.type === "document") layer.registered.push(source);
    if (source.type === "observed_document") layer.observed.push(source);
  }
  const rows = Array.from(summaries.values());
  for (const row of rows) {
    row.registered.sort((a: JsonObject, b: JsonObject) => lexicalCompare(graphNodeLabel(a, "ja"), graphNodeLabel(b, "ja")));
    row.observed.sort((a: JsonObject, b: JsonObject) => lexicalCompare(graphNodeLabel(a, "ja"), graphNodeLabel(b, "ja")));
  }
  rows.sort((a, b) => {
    const specialOrder: Record<string, number> = {
      overview: 0,
      sat_truth: 10,
      raj_beauty: 20,
      tam_goodness: 30,
      applications: 40,
      research_notes: 50,
      visual_materials: 60,
      root: 70,
    };
    return (specialOrder[a.key] ?? 999) - (specialOrder[b.key] ?? 999) || lexicalCompare(a.key, b.key);
  });
  return rows;
}

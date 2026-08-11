import {
  browsePayload,
  browseTopics,
  localizedValue,
  searchDocuments,
  topicDocuments,
  type JsonObject,
} from "./search-core.js";
import {
  graphNodeLabel,
  graphNodeMap,
  graphSubgraph,
  layerSummaries,
  resolveGraphNode,
} from "./graph-core.js";

const INDEX_URL = "../tools/docs_index.json";
const GRAPH_URL = "../tools/docs_graph.json";
const MAX_MAP_EDGES = 24;

let docsIndex: JsonObject;
let docsGraph: JsonObject;
let displayLang: "ja" | "en" = "ja";

const app = document.querySelector<HTMLElement>("#app")!;
const status = document.querySelector<HTMLElement>("#data-status")!;
const langButton = document.querySelector<HTMLButtonElement>("#lang-toggle")!;

function el<K extends keyof HTMLElementTagNameMap>(tag: K, className = "", text = ""): HTMLElementTagNameMap[K] {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text) node.textContent = text;
  return node;
}

function button(label: string, className = "button"): HTMLButtonElement {
  const node = el("button", className, label);
  node.type = "button";
  return node;
}

function encodePath(path: string): string {
  return "../" + path.split("/").map(encodeURIComponent).join("/");
}

function localized(value: any, fallback = ""): string {
  return localizedValue(value, displayLang, fallback);
}

function setRoute(values: Record<string, string | undefined>): void {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(values)) if (value) params.set(key, value);
  location.hash = params.toString();
}

function route(): URLSearchParams {
  return new URLSearchParams(location.hash.replace(/^#/, ""));
}

function setLanguage(lang: "ja" | "en"): void {
  displayLang = lang;
  langButton.textContent = lang === "ja" ? "EN" : "日本語";
  document.documentElement.lang = lang;
  render();
}

function eyebrow(text: string): HTMLElement {
  return el("div", "eyebrow", text);
}

function badge(text: string, tone = ""): HTMLElement {
  return el("span", `badge ${tone}`.trim(), text);
}

function titleForDoc(doc: JsonObject): string {
  return localized(doc.title, String(doc.id ?? doc.doc_id ?? ""));
}

function roleForDoc(doc: JsonObject): string {
  return localized(doc.role, "");
}

function docById(docId: string): JsonObject | undefined {
  return (docsIndex.documents ?? []).find((doc: JsonObject) => String(doc.id) === docId);
}

function graphNodeForDocument(doc: JsonObject): string | undefined {
  const direct = `doc:${doc.id}`;
  if (graphNodeMap(docsGraph).has(direct)) return direct;
  const byPath = (docsGraph.nodes ?? []).find((node: JsonObject) => node.type === "document" && node.path === doc.path);
  return byPath?.id;
}

function navBar(active: string): HTMLElement {
  const nav = el("nav", "view-tabs");
  const items: Array<[string, string, Record<string, string>]> = [
    ["explore", displayLang === "ja" ? "探索" : "Explore", {}],
    ["search", displayLang === "ja" ? "検索" : "Search", { view: "search" }],
    ["relations", displayLang === "ja" ? "関係マップ" : "Relations", { view: "relations" }],
    ["audit", displayLang === "ja" ? "データ点検" : "Data audit", { view: "audit" }],
  ];
  for (const [id, label, target] of items) {
    const b = button(label, `tab ${id === active ? "active" : ""}`);
    b.addEventListener("click", () => setRoute(target));
    nav.append(b);
  }
  return nav;
}

function dataBanner(): HTMLElement {
  const wrap = el("div", "data-banner");
  const profile = String(docsIndex.source?.visibility_profile ?? "unknown");
  wrap.append(badge(profile === "preview" ? "PREVIEW" : profile.toUpperCase(), profile === "preview" ? "warn" : ""));
  const indexHash = String(docsIndex.source?.manifest_sha256 ?? "");
  const graphHash = String(docsGraph.source?.manifest_sha256 ?? "");
  const aligned = indexHash && graphHash && indexHash === graphHash;
  wrap.append(
    el(
      "span",
      "data-banner-text",
      aligned
        ? displayLang === "ja"
          ? "検索インデックスと関係グラフは同じ manifest から生成されています。"
          : "Search index and relation graph were built from the same manifest."
        : displayLang === "ja"
          ? "検索インデックスと関係グラフの manifest hash が一致していません。"
          : "Search index and relation graph manifest hashes do not match.",
    ),
  );
  return wrap;
}

function searchBox(initial = ""): HTMLElement {
  const form = el("form", "search-box");
  const input = el("input", "search-input") as HTMLInputElement;
  input.name = "q";
  input.type = "search";
  input.value = initial;
  input.placeholder = displayLang === "ja" ? "問い・用語から探す" : "Search by question or term";
  input.autocomplete = "off";
  const submit = button(displayLang === "ja" ? "検索" : "Search", "button primary");
  submit.type = "submit";
  form.append(input, submit);
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const query = input.value.trim();
    if (query) setRoute({ view: "search", q: query });
  });
  return form;
}

function renderExplore(): HTMLElement {
  const page = el("main", "page");
  page.append(navBar("explore"), dataBanner());

  const hero = el("section", "hero");
  hero.append(
    eyebrow(displayLang === "ja" ? "DOCUMENT NAVIGATOR" : "DOCUMENT NAVIGATOR"),
    el("h1", "hero-title", displayLang === "ja" ? "知らないところから入れる入口" : "An entry point before you know the terms"),
    el(
      "p",
      "hero-copy",
      displayLang === "ja"
        ? "READMEで体系の趣旨をつかんだ後、トピック・体系層・問い・検索・関係から次の文書へ進めます。"
        : "After the README explains the project, move through topics, system layers, questions, search, and relations to the next document.",
    ),
    searchBox(),
  );
  page.append(hero);

  const topicSection = el("section", "section");
  topicSection.append(
    eyebrow(displayLang === "ja" ? "TOPICS" : "TOPICS"),
    el("h2", "section-title", displayLang === "ja" ? "関心から入る" : "Enter through an interest"),
    el(
      "p",
      "section-copy",
      displayLang === "ja"
        ? "トピックは分類学ではなく、読者の入口です。一つの文書が複数の入口に現れることがあります。"
        : "Topics are navigation entries, not an ontology. A document may appear through several entries.",
    ),
  );
  const grid = el("div", "card-grid");
  for (const card of browseTopics(docsIndex)) {
    const item = el("article", "topic-card card");
    const heading = el("h3", "card-title", localized(card.label, String(card.topic_id)));
    const count = badge(`${card.document_count} ${displayLang === "ja" ? "文書" : "docs"}`);
    const description = el("p", "card-copy", localized(card.description));
    const questions = el("div", "question-preview");
    const qList = card.starter_questions?.[displayLang] ?? [];
    for (const q of qList.slice(0, 2)) questions.append(el("div", "question-line", `Q. ${q}`));
    const open = button(displayLang === "ja" ? "この入口を見る" : "Open this entry", "text-button");
    open.addEventListener("click", () => setRoute({ topic: String(card.topic_id) }));
    item.append(heading, count, description, questions, open);
    grid.append(item);
  }
  topicSection.append(grid);
  page.append(topicSection);

  const layerSection = el("section", "section alt-section");
  layerSection.append(
    eyebrow(displayLang === "ja" ? "SYSTEM LAYERS" : "SYSTEM LAYERS"),
    el("h2", "section-title", displayLang === "ja" ? "体系の配置から入る" : "Enter through the system layout"),
    el(
      "p",
      "section-copy",
      displayLang === "ja"
        ? "01 Sat / Truth、02 Raj / Beauty、03 Tam / Goodness、応用、研究ノートなど、リポジトリ上の配置をそのまま入口にします。"
        : "Use repository placement itself as an entry: 01 Sat / Truth, 02 Raj / Beauty, 03 Tam / Goodness, applications, research notes, and more.",
    ),
  );
  const layers = el("div", "layer-list");
  for (const layer of layerSummaries(docsGraph).filter((row) => row.key !== "root")) {
    const row = el("button", "layer-row") as HTMLButtonElement;
    row.type = "button";
    row.addEventListener("click", () => setRoute({ layer: String(layer.id) }));
    const name = el("span", "layer-name", `${localized(layer.label, String(layer.key))}`);
    const path = el("span", "layer-path", String(layer.path));
    const counts = el(
      "span",
      "layer-count",
      `${layer.registered.length} ${displayLang === "ja" ? "登録" : "registered"} · ${layer.observed.length} ${displayLang === "ja" ? "観測のみ" : "observed"}`,
    );
    row.append(name, path, counts);
    layers.append(row);
  }
  layerSection.append(layers);
  page.append(layerSection);
  return page;
}

function docCard(doc: JsonObject): HTMLElement {
  const item = el("article", "doc-card card");
  const level = String(doc.entry_level ?? doc.discovery?.entry_level ?? "");
  const state = String(doc.state ?? "");
  const top = el("div", "card-meta");
  if (level) top.append(badge(level));
  if (state) top.append(badge(state, state === "public-candidate" ? "warn" : ""));
  item.append(top, el("h3", "card-title", titleForDoc(doc)));
  const role = roleForDoc(doc);
  if (role) item.append(el("p", "card-copy", role));
  const questions = doc.reader_questions ?? doc.discovery?.reader_questions ?? {};
  const qList = questions[displayLang] ?? questions.ja ?? questions.en ?? [];
  if (qList.length) item.append(el("div", "question-line", `Q. ${qList[0]}`));
  const path = String(doc.path ?? "");
  item.append(el("div", "path", path));
  const actions = el("div", "card-actions");
  const detail = button(displayLang === "ja" ? "文書を見る" : "Inspect document", "text-button");
  const id = String(doc.doc_id ?? doc.id ?? "");
  detail.addEventListener("click", () => setRoute({ doc: id }));
  actions.append(detail);
  if (path) {
    const open = el("a", "text-link", displayLang === "ja" ? "ファイルを開く" : "Open file");
    open.href = encodePath(path);
    open.target = "_blank";
    open.rel = "noopener";
    actions.append(open);
  }
  item.append(actions);
  return item;
}

function renderTopic(topicId: string): HTMLElement {
  const page = el("main", "page");
  page.append(navBar("explore"), dataBanner());
  const payload = browsePayload(docsIndex, topicId);
  const card = payload.topic;
  const back = button(displayLang === "ja" ? "← トピック一覧" : "← Topics", "back-button");
  back.addEventListener("click", () => setRoute({}));
  page.append(back);

  const hero = el("section", "topic-hero");
  hero.append(
    eyebrow(`TOPIC · ${topicId}`),
    el("h1", "hero-title", localized(card.label, topicId)),
    el("p", "hero-copy", localized(card.description)),
  );
  const questions = el("div", "starter-questions");
  questions.append(el("h2", "minor-title", displayLang === "ja" ? "この入口から始められる問い" : "Questions that can start here"));
  for (const q of card.starter_questions?.[displayLang] ?? []) {
    const qButton = button(String(q), "question-button");
    qButton.addEventListener("click", () => setRoute({ view: "search", q: String(q) }));
    questions.append(qButton);
  }
  hero.append(questions);
  page.append(hero);

  const groups: Record<string, JsonObject[]> = { foundation: [], intermediate: [], advanced: [], unspecified: [] };
  for (const doc of payload.documents ?? []) {
    const level = String(doc.entry_level ?? "");
    (groups[level] ?? groups.unspecified).push(doc);
  }
  const labels: Record<string, [string, string]> = {
    foundation: ["まず読む / 基礎", "Start / foundation"],
    intermediate: ["もう少し進む", "Go further"],
    advanced: ["深く読む", "Read deeply"],
    unspecified: ["その他", "Other"],
  };
  for (const level of ["foundation", "intermediate", "advanced", "unspecified"]) {
    if (!groups[level].length) continue;
    const section = el("section", "section compact-section");
    section.append(el("h2", "section-title small", labels[level][displayLang === "ja" ? 0 : 1]));
    const grid = el("div", "doc-grid");
    for (const doc of groups[level]) grid.append(docCard(doc));
    section.append(grid);
    page.append(section);
  }
  return page;
}

function renderLayer(layerId: string): HTMLElement {
  const page = el("main", "page");
  page.append(navBar("explore"), dataBanner());
  const layer = layerSummaries(docsGraph).find((row) => String(row.id) === layerId);
  if (!layer) return errorPage(`Unknown layer: ${layerId}`);
  const back = button(displayLang === "ja" ? "← 全体へ" : "← Overview", "back-button");
  back.addEventListener("click", () => setRoute({}));
  page.append(back);
  page.append(
    eyebrow(`LAYER · ${String(layer.path)}`),
    el("h1", "hero-title", localized(layer.label, String(layer.key))),
    el(
      "p",
      "hero-copy",
      displayLang === "ja"
        ? `manifest 登録 ${layer.registered.length}件、リポジトリ上で観測のみ ${layer.observed.length}件。観測のみは検索対象資格やcanonical identityを意味しません。`
        : `${layer.registered.length} manifest-registered documents and ${layer.observed.length} repository-observed-only documents. Observed-only does not imply search eligibility or canonical identity.`,
    ),
  );

  if (layer.registered.length) {
    const section = el("section", "section compact-section");
    section.append(el("h2", "section-title small", displayLang === "ja" ? "manifest登録文書" : "Manifest-registered documents"));
    const grid = el("div", "doc-grid");
    for (const node of layer.registered) {
      const doc = docById(String(node.key));
      if (doc) grid.append(docCard(doc));
      else {
        const card = el("article", "doc-card card");
        card.append(el("h3", "card-title", graphNodeLabel(node, displayLang)), el("div", "path", String(node.path ?? "")));
        grid.append(card);
      }
    }
    section.append(grid);
    page.append(section);
  }

  if (layer.observed.length) {
    const section = el("section", "section compact-section");
    section.append(
      el("h2", "section-title small", displayLang === "ja" ? "観測された未登録文書" : "Observed unregistered documents"),
      el(
        "p",
        "section-copy",
        displayLang === "ja"
          ? "ここはDN-5で可視化された監査面です。必要な文書だけ、後からmanifestへ昇格させます。"
          : "This is an audit surface exposed by DN-5. Only documents that need canonical navigation status should later be promoted into the manifest.",
      ),
    );
    const list = el("div", "observed-list");
    for (const node of layer.observed) {
      const row = el("div", "observed-row");
      const main = el("div", "observed-main");
      main.append(el("strong", "", graphNodeLabel(node, displayLang)), el("div", "path", String(node.path ?? "")));
      const open = el("a", "text-link", displayLang === "ja" ? "開く" : "Open");
      open.href = encodePath(String(node.path ?? ""));
      open.target = "_blank";
      open.rel = "noopener";
      const relation = button(displayLang === "ja" ? "関係を見る" : "Relations", "text-button");
      relation.addEventListener("click", () => setRoute({ graph: String(node.id) }));
      row.append(main, open, relation);
      list.append(row);
    }
    section.append(list);
    page.append(section);
  }
  return page;
}

function renderSearch(query: string): HTMLElement {
  const page = el("main", "page");
  page.append(navBar("search"), dataBanner());
  const section = el("section", "search-page");
  section.append(eyebrow("SEARCH"), el("h1", "hero-title", displayLang === "ja" ? "問い・用語から探す" : "Search by question or term"), searchBox(query));
  if (!query) {
    section.append(
      el(
        "p",
        "section-copy",
        displayLang === "ja"
          ? "検索は直接関連だけを順位づけします。関係グラフのcentralityやリンク数は検索スコアへ混ぜていません。"
          : "Search ranks direct relevance only. Graph centrality and link counts are not mixed into search scores.",
      ),
    );
    page.append(section);
    return page;
  }
  const found = searchDocuments(query, docsIndex, "auto", 12, "both");
  section.append(
    el("div", "search-summary", `${displayLang === "ja" ? "判定モード" : "Resolved mode"}: ${found.mode} · ${found.results.length} ${displayLang === "ja" ? "件" : "results"}`),
  );
  const results = el("div", "search-results");
  for (const result of found.results) {
    const card = el("article", "search-result card");
    const heading = el("div", "result-heading");
    heading.append(el("h2", "card-title", titleForDoc(result)), badge(result.score.toFixed(2), "score"));
    card.append(heading);
    const role = roleForDoc(result);
    if (role) card.append(el("p", "card-copy", role));
    const reasons = el("div", "match-reasons");
    for (const match of (result.matches ?? []).slice(0, 3)) {
      const reason = el("div", "match-reason");
      reason.append(
        badge(String(match.field)),
        el("span", "", `${String(match.method)} · +${Number(match.contribution).toFixed(2)}`),
        el("span", "match-text", `“${String(match.text)}”`),
      );
      reasons.append(reason);
    }
    card.append(reasons, el("div", "path", String(result.path ?? "")));
    const actions = el("div", "card-actions");
    const detail = button(displayLang === "ja" ? "文書と関係を見る" : "Document and relations", "text-button");
    detail.addEventListener("click", () => setRoute({ doc: String(result.doc_id) }));
    actions.append(detail);
    const open = el("a", "text-link", displayLang === "ja" ? "ファイルを開く" : "Open file");
    open.href = encodePath(String(result.path ?? ""));
    open.target = "_blank";
    open.rel = "noopener";
    actions.append(open);
    card.append(actions);
    results.append(card);
  }
  if (!found.results.length) results.append(el("p", "empty", displayLang === "ja" ? "該当する検索結果はありません。" : "No search results."));
  section.append(results);
  page.append(section);
  return page;
}

function renderDocument(docId: string): HTMLElement {
  const doc = docById(docId);
  if (!doc) return errorPage(`Unknown document: ${docId}`);
  const page = el("main", "page");
  page.append(navBar("explore"), dataBanner());
  const back = button(displayLang === "ja" ? "← 戻る" : "← Back", "back-button");
  back.addEventListener("click", () => history.length > 1 ? history.back() : setRoute({}));
  page.append(back);

  const meta = el("div", "doc-meta-line");
  meta.append(badge(String(doc.discovery?.entry_level || "unclassified")), badge(String(doc.state), doc.state === "public-candidate" ? "warn" : ""));
  const header = el("section", "doc-header");
  header.append(eyebrow(`DOCUMENT · ${doc.id}`), el("h1", "hero-title", titleForDoc(doc)), meta);
  const role = roleForDoc(doc);
  if (role) header.append(el("p", "hero-copy", role));
  header.append(el("div", "path", String(doc.path)));
  const open = el("a", "button secondary", displayLang === "ja" ? "文書ファイルを開く" : "Open document file");
  open.href = encodePath(String(doc.path));
  open.target = "_blank";
  open.rel = "noopener";
  header.append(open);
  page.append(header);

  const infoGrid = el("div", "info-grid");
  const topicPanel = el("section", "info-panel");
  topicPanel.append(el("h2", "minor-title", displayLang === "ja" ? "入口トピック" : "Entry topics"));
  const topicWrap = el("div", "chip-wrap");
  for (const topicId of doc.discovery?.topics ?? []) {
    const t = docsIndex.topics?.[topicId] ?? {};
    const b = button(localized(t, topicId), "chip-button");
    b.addEventListener("click", () => setRoute({ topic: String(topicId) }));
    topicWrap.append(b);
  }
  if (!topicWrap.childElementCount) topicWrap.append(el("span", "muted", displayLang === "ja" ? "未設定" : "Not set"));
  topicPanel.append(topicWrap);

  const qPanel = el("section", "info-panel");
  qPanel.append(el("h2", "minor-title", displayLang === "ja" ? "この文書が扱う問い" : "Questions this document addresses"));
  const qList = el("ul", "plain-list");
  for (const q of doc.discovery?.reader_questions?.[displayLang] ?? []) {
    const li = el("li");
    const b = button(String(q), "inline-question");
    b.addEventListener("click", () => setRoute({ view: "search", q: String(q) }));
    li.append(b);
    qList.append(li);
  }
  if (!qList.childElementCount) qList.append(el("li", "muted", displayLang === "ja" ? "未設定" : "Not set"));
  qPanel.append(qList);
  infoGrid.append(topicPanel, qPanel);
  page.append(infoGrid);

  const graphId = graphNodeForDocument(doc);
  if (graphId) page.append(relationSection(graphId));
  return page;
}

function relationSection(rootId: string): HTMLElement {
  const section = el("section", "section relation-section");
  section.append(eyebrow("TYPED RELATION GRAPH"), el("h2", "section-title", displayLang === "ja" ? "このノードの関係" : "Relations for this node"));
  section.append(
    el(
      "p",
      "section-copy",
      displayLang === "ja"
        ? "線は重要度ではなく、実際に抽出されたtyped relationです。辺を支えるsourceは下の一覧で確認できます。"
        : "Lines are extracted typed relations, not importance scores. Provenance for each edge is listed below.",
    ),
  );
  const map = relationMap(rootId);
  section.append(map);
  const full = button(displayLang === "ja" ? "関係マップ画面で開く" : "Open relation map", "button secondary");
  full.addEventListener("click", () => setRoute({ graph: rootId }));
  section.append(full);
  return section;
}

function relationMap(rootId: string): HTMLElement {
  const payload = graphSubgraph(docsGraph, rootId, 1);
  const nodeMap = new Map((payload.nodes ?? []).map((node: JsonObject) => [String(node.id), node]));
  const root = nodeMap.get(rootId);
  const wrapper = el("div", "relation-map-wrap");
  if (!root) {
    wrapper.append(el("p", "empty", displayLang === "ja" ? "グラフノードがありません。" : "Graph node not found."));
    return wrapper;
  }
  let edges = (payload.edges ?? []).filter((edge: JsonObject) => edge.from === rootId || edge.to === rootId);
  edges = edges.sort((a: JsonObject, b: JsonObject) =>
    String(a.relation).localeCompare(String(b.relation), "en") || String(a.from).localeCompare(String(b.from), "en") || String(a.to).localeCompare(String(b.to), "en"),
  );
  const clipped = edges.slice(0, MAX_MAP_EDGES);
  const incoming = clipped.filter((edge: JsonObject) => edge.to === rootId);
  const outgoing = clipped.filter((edge: JsonObject) => edge.from === rootId);
  const rows = Math.max(incoming.length, outgoing.length, 1);
  const height = Math.max(340, rows * 74 + 100);
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("viewBox", `0 0 1000 ${height}`);
  svg.setAttribute("class", "relation-svg");
  svg.setAttribute("role", "img");
  svg.setAttribute("aria-label", `${graphNodeLabel(root, displayLang)} relation map`);
  const ns = "http://www.w3.org/2000/svg";
  const defs = document.createElementNS(ns, "defs");
  const marker = document.createElementNS(ns, "marker");
  marker.setAttribute("id", "relation-arrow");
  marker.setAttribute("viewBox", "0 0 10 10");
  marker.setAttribute("refX", "8");
  marker.setAttribute("refY", "5");
  marker.setAttribute("markerWidth", "6");
  marker.setAttribute("markerHeight", "6");
  marker.setAttribute("orient", "auto-start-reverse");
  const markerPath = document.createElementNS(ns, "path");
  markerPath.setAttribute("d", "M 0 0 L 10 5 L 0 10 z");
  markerPath.setAttribute("class", "svg-arrowhead");
  marker.append(markerPath);
  defs.append(marker);
  svg.append(defs);

  const centerY = height / 2;
  const center = { x: 500, y: centerY };
  drawGraphNode(svg, root, center.x, center.y, true);

  incoming.forEach((edge: JsonObject, index: number) => {
    const node = nodeMap.get(String(edge.from));
    if (!node) return;
    const y = 70 + index * 74;
    drawEdge(svg, 300, y, 420, center.y, String(edge.relation), "incoming");
    drawGraphNode(svg, node, 180, y, false);
  });
  outgoing.forEach((edge: JsonObject, index: number) => {
    const node = nodeMap.get(String(edge.to));
    if (!node) return;
    const y = 70 + index * 74;
    drawEdge(svg, 580, center.y, 700, y, String(edge.relation), "outgoing");
    drawGraphNode(svg, node, 820, y, false);
  });
  wrapper.append(svg);
  if (edges.length > MAX_MAP_EDGES) {
    wrapper.append(
      el(
        "p",
        "map-note",
        displayLang === "ja"
          ? `図では安定順の先頭${MAX_MAP_EDGES}辺を表示。全${edges.length}辺は下のrelation listに保持しています。`
          : `The map shows the first ${MAX_MAP_EDGES} edges in stable order. All ${edges.length} edges remain in the relation list below.`,
      ),
    );
  }
  const list = el("div", "relation-list");
  for (const edge of edges) {
    const outgoingEdge = edge.from === rootId;
    const otherId = String(outgoingEdge ? edge.to : edge.from);
    const other = nodeMap.get(otherId) ?? graphNodeMap(docsGraph).get(otherId);
    if (!other) continue;
    const row = el("button", "relation-row") as HTMLButtonElement;
    row.type = "button";
    row.addEventListener("click", () => setRoute({ graph: otherId }));
    const direction = el("span", "relation-direction", outgoingEdge ? "→" : "←");
    const rel = el("span", "relation-type", String(edge.relation));
    const label = el("span", "relation-target", graphNodeLabel(other, displayLang));
    const provTypes = Array.from(new Set((edge.provenance ?? []).map((p: JsonObject) => String(p.source_type ?? "")).filter(Boolean))).join(" + ");
    const prov = el("span", "relation-provenance", provTypes || "—");
    row.append(direction, rel, label, prov);
    list.append(row);
  }
  wrapper.append(list);
  return wrapper;
}

function truncate(value: string, max = 28): string {
  return value.length <= max ? value : `${value.slice(0, max - 1)}…`;
}

function drawGraphNode(svg: SVGSVGElement, node: JsonObject, x: number, y: number, root: boolean): void {
  const ns = "http://www.w3.org/2000/svg";
  const group = document.createElementNS(ns, "g");
  group.setAttribute("class", `svg-node ${root ? "root" : ""} type-${String(node.type)}`);
  group.setAttribute("tabindex", "0");
  group.setAttribute("role", "button");
  const width = root ? 250 : 245;
  const rect = document.createElementNS(ns, "rect");
  rect.setAttribute("x", String(x - width / 2));
  rect.setAttribute("y", String(y - 27));
  rect.setAttribute("width", String(width));
  rect.setAttribute("height", "54");
  rect.setAttribute("rx", "12");
  const text = document.createElementNS(ns, "text");
  text.setAttribute("x", String(x));
  text.setAttribute("y", String(y - 3));
  text.setAttribute("text-anchor", "middle");
  text.setAttribute("class", "svg-node-label");
  text.textContent = truncate(graphNodeLabel(node, displayLang), root ? 34 : 28);
  const type = document.createElementNS(ns, "text");
  type.setAttribute("x", String(x));
  type.setAttribute("y", String(y + 15));
  type.setAttribute("text-anchor", "middle");
  type.setAttribute("class", "svg-node-type");
  type.textContent = String(node.type);
  group.append(rect, text, type);
  if (!root) {
    const activate = () => setRoute({ graph: String(node.id) });
    group.addEventListener("click", activate);
    group.addEventListener("keydown", (event) => {
      if ((event as KeyboardEvent).key === "Enter" || (event as KeyboardEvent).key === " ") activate();
    });
  }
  svg.append(group);
}

function drawEdge(svg: SVGSVGElement, x1: number, y1: number, x2: number, y2: number, relation: string, direction: string): void {
  const ns = "http://www.w3.org/2000/svg";
  const line = document.createElementNS(ns, "line");
  line.setAttribute("x1", String(x1));
  line.setAttribute("y1", String(y1));
  line.setAttribute("x2", String(x2));
  line.setAttribute("y2", String(y2));
  line.setAttribute("class", "svg-edge");
  line.setAttribute("marker-end", "url(#relation-arrow)");
  const text = document.createElementNS(ns, "text");
  const tx = (x1 + x2) / 2;
  const ty = (y1 + y2) / 2 - 6;
  text.setAttribute("x", String(tx));
  text.setAttribute("y", String(ty));
  text.setAttribute("text-anchor", "middle");
  text.setAttribute("class", "svg-edge-label");
  text.textContent = truncate(relation, 24);
  line.dataset.direction = direction;
  svg.append(line, text);
}

function renderRelations(nodeQuery = ""): HTMLElement {
  const page = el("main", "page");
  page.append(navBar("relations"), dataBanner());
  const section = el("section", "section");
  section.append(
    eyebrow("TYPED RELATION GRAPH"),
    el("h1", "hero-title", displayLang === "ja" ? "関係から読む" : "Read through relations"),
    el(
      "p",
      "hero-copy",
      displayLang === "ja"
        ? "文書・概念・トピック・Glossary語・体系層をノードとして、宣言関係と観測リンクを区別したまま辿ります。"
        : "Traverse documents, concepts, topics, glossary terms, and system layers while preserving the distinction between declared relations and observed links.",
    ),
  );
  const form = el("form", "graph-search");
  const input = el("input", "search-input") as HTMLInputElement;
  input.placeholder = displayLang === "ja" ? "文書名・概念・Glossary語・node ID" : "Document, concept, glossary term, or node ID";
  input.value = nodeQuery;
  const submit = button(displayLang === "ja" ? "関係を表示" : "Show relations", "button primary");
  submit.type = "submit";
  form.append(input, submit);
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const value = input.value.trim();
    if (!value) return;
    try {
      setRoute({ graph: resolveGraphNode(docsGraph, value) });
    } catch (error) {
      alert(String((error as Error).message));
    }
  });
  section.append(form);
  if (nodeQuery) {
    try {
      const rootId = resolveGraphNode(docsGraph, nodeQuery);
      const root = graphNodeMap(docsGraph).get(rootId)!;
      const current = el("div", "graph-current");
      current.append(
        el("h2", "section-title small", graphNodeLabel(root, displayLang)),
        badge(String(root.type)),
        el("div", "path", String(root.path ?? root.id)),
      );
      section.append(current, relationMap(rootId));
    } catch (error) {
      section.append(el("p", "error", String((error as Error).message)));
    }
  } else {
    const starters = el("div", "starter-node-grid");
    const seeds = ["doc:scientific_ontology_concept_network", "doc:meaning_generation_model", "topic:ai", "layer:sat_truth"];
    for (const id of seeds) {
      const node = graphNodeMap(docsGraph).get(id);
      if (!node) continue;
      const b = button(graphNodeLabel(node, displayLang), "starter-node");
      b.addEventListener("click", () => setRoute({ graph: id }));
      starters.append(b);
    }
    section.append(el("h2", "minor-title", displayLang === "ja" ? "例から開く" : "Open an example"), starters);
  }
  page.append(section);
  return page;
}

function renderAudit(): HTMLElement {
  const page = el("main", "page");
  page.append(navBar("audit"), dataBanner());
  const section = el("section", "section");
  section.append(
    eyebrow("DATA AUDIT"),
    el("h1", "hero-title", displayLang === "ja" ? "UIからデータへ戻る点検面" : "Audit the data from the UI surface"),
    el(
      "p",
      "hero-copy",
      displayLang === "ja"
        ? "ここでは重要度を計算せず、現在UIに見えているものがどのデータ状態から来ているかを露出します。"
        : "This view exposes the data state behind the UI without calculating importance scores.",
    ),
  );

  const nodeCounts = new Map<string, number>();
  for (const node of docsGraph.nodes ?? []) nodeCounts.set(String(node.type), (nodeCounts.get(String(node.type)) ?? 0) + 1);
  const edgeCounts = new Map<string, number>();
  for (const edge of docsGraph.edges ?? []) edgeCounts.set(String(edge.relation), (edgeCounts.get(String(edge.relation)) ?? 0) + 1);
  const stats = el("div", "audit-stats");
  const statRows: Array<[string, string]> = [
    [displayLang === "ja" ? "検索対象文書" : "Search-index documents", String((docsIndex.documents ?? []).length)],
    [displayLang === "ja" ? "登録document nodes" : "Registered document nodes", String(nodeCounts.get("document") ?? 0)],
    [displayLang === "ja" ? "観測のみdocument nodes" : "Observed-only document nodes", String(nodeCounts.get("observed_document") ?? 0)],
    [displayLang === "ja" ? "concept nodes" : "Concept nodes", String(nodeCounts.get("concept") ?? 0)],
    [displayLang === "ja" ? "typed edges" : "Typed edges", String((docsGraph.edges ?? []).length)],
  ];
  for (const [label, value] of statRows) {
    const box = el("div", "stat-box");
    box.append(el("span", "stat-value", value), el("span", "stat-label", label));
    stats.append(box);
  }
  section.append(stats);

  const diag = docsGraph.diagnostics ?? {};
  const diagnostics = el("section", "audit-panel");
  diagnostics.append(el("h2", "section-title small", displayLang === "ja" ? "Graph diagnostics" : "Graph diagnostics"));
  const rows = [
    ["unresolved_document_references", displayLang === "ja" ? "未解決文書参照" : "Unresolved document references"],
    ["unresolved_concept_references", displayLang === "ja" ? "未解決concept参照" : "Unresolved concept references"],
    ["excluded_references", displayLang === "ja" ? "private/process境界で除外" : "Excluded at private/process boundary"],
    ["observed_unregistered_documents", displayLang === "ja" ? "観測された未登録文書" : "Observed unregistered documents"],
  ];
  for (const [key, label] of rows) {
    const row = el("div", "audit-row");
    row.append(el("span", "", label), badge(String((diag[key] ?? []).length), key.includes("unresolved") && (diag[key] ?? []).length ? "danger" : ""));
    diagnostics.append(row);
  }
  section.append(diagnostics);

  const relationPanel = el("section", "audit-panel");
  relationPanel.append(
    el("h2", "section-title small", displayLang === "ja" ? "関係型の走査結果" : "Observed relation types"),
    el(
      "p",
      "section-copy",
      displayLang === "ja"
        ? "これは重要度ではなく、現時点の走査件数です。各relationの具体的な辺は関係マップ側で確認します。"
        : "These are scan counts, not importance. Inspect the actual edges in the relation map.",
    ),
  );
  const relationTable = el("div", "relation-count-table");
  for (const [relation, count] of Array.from(edgeCounts.entries()).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], "en"))) {
    const row = el("div", "relation-count-row");
    row.append(el("code", "", relation), el("span", "", String(count)));
    relationTable.append(row);
  }
  relationPanel.append(relationTable);
  section.append(relationPanel);

  const coverage = el("section", "audit-panel");
  coverage.append(
    el("h2", "section-title small", displayLang === "ja" ? "体系層ごとの登録 / 観測" : "Registered / observed by system layer"),
  );
  const coverageList = el("div", "layer-list");
  for (const layer of layerSummaries(docsGraph).filter((row) => row.key !== "root")) {
    const row = el("button", "layer-row") as HTMLButtonElement;
    row.type = "button";
    row.addEventListener("click", () => setRoute({ layer: String(layer.id) }));
    row.append(
      el("span", "layer-name", localized(layer.label, String(layer.key))),
      el("span", "layer-path", String(layer.path)),
      el("span", "layer-count", `${layer.registered.length} / ${layer.observed.length}`),
    );
    coverageList.append(row);
  }
  coverage.append(coverageList);
  section.append(coverage);

  page.append(section);
  return page;
}

function errorPage(message: string): HTMLElement {
  const page = el("main", "page");
  page.append(navBar("explore"), el("p", "error", message));
  return page;
}

function render(): void {
  if (!docsIndex || !docsGraph) return;
  const params = route();
  let content: HTMLElement;
  try {
    if (params.get("topic")) content = renderTopic(String(params.get("topic")));
    else if (params.get("layer")) content = renderLayer(String(params.get("layer")));
    else if (params.get("doc")) content = renderDocument(String(params.get("doc")));
    else if (params.get("graph")) content = renderRelations(String(params.get("graph")));
    else if (params.get("view") === "search") content = renderSearch(params.get("q") ?? "");
    else if (params.get("view") === "relations") content = renderRelations();
    else if (params.get("view") === "audit") content = renderAudit();
    else content = renderExplore();
  } catch (error) {
    content = errorPage(String((error as Error).message));
  }
  app.replaceChildren(content);
  window.scrollTo({ top: 0, behavior: "instant" });
}

async function load(): Promise<void> {
  try {
    status.textContent = displayLang === "ja" ? "データを読み込み中…" : "Loading data…";
    const [indexResponse, graphResponse] = await Promise.all([fetch(INDEX_URL), fetch(GRAPH_URL)]);
    if (!indexResponse.ok) throw new Error(`docs_index.json: HTTP ${indexResponse.status}`);
    if (!graphResponse.ok) throw new Error(`docs_graph.json: HTTP ${graphResponse.status}`);
    docsIndex = await indexResponse.json();
    docsGraph = await graphResponse.json();
    status.textContent = "";
    render();
  } catch (error) {
    status.textContent = String((error as Error).message);
    status.className = "load-error";
  }
}

langButton.addEventListener("click", () => setLanguage(displayLang === "ja" ? "en" : "ja"));
window.addEventListener("hashchange", render);
load();

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
const CANDIDATES_URL = "../tools/docs_registration_candidates.preview.json";
const PUBLIC_CONTENT_URL = "./public-content.json";
const MAX_MAP_EDGES = 24;

const interfaceMode: "public" | "developer" = document.body.dataset.interface === "developer" ? "developer" : "public";

let docsIndex: JsonObject;
let docsGraph: JsonObject;
let publicContent: JsonObject = {};
let registrationCandidates: JsonObject | null = null;
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

function isBlockedRepoPath(path: string): boolean {
  const clean = path.replace(/\\/g, "/").replace(/^\/+/, "");
  return (
    clean.split("/").some((part) => part.startsWith("000")) ||
    clean.startsWith("99_Private_Core") ||
    clean.includes("/99_Private_Core") ||
    clean.includes("private-core") ||
    clean.includes("Private_Core") ||
    clean.includes("/Gate") ||
    clean.includes("/U5")
  );
}

function readerAllowedPaths(): Set<string> {
  const allowed = new Set<string>();
  for (const doc of docsIndex.documents ?? []) {
    const path = String(doc.path ?? "");
    if (path.endsWith(".md") && !isBlockedRepoPath(path)) allowed.add(path);
  }
  for (const node of docsGraph.nodes ?? []) {
    if (node.type !== "document" && node.type !== "observed_document") continue;
    const path = String(node.path ?? "");
    if (path.endsWith(".md") && !isBlockedRepoPath(path)) allowed.add(path);
  }
  return allowed;
}

function normalizeRepoPath(basePath: string, target: string): string | null {
  const raw = target.trim();
  if (!raw || raw.startsWith("#")) return null;
  if (/^[a-z][a-z0-9+.-]*:/i.test(raw)) return null;
  let pathPart = raw.split("#", 1)[0].split("?", 1)[0];
  try { pathPart = decodeURIComponent(pathPart); } catch { /* keep original */ }
  const parts = pathPart.startsWith("/") ? [] : basePath.split("/").slice(0, -1);
  for (const part of pathPart.replace(/^\/+/, "").split("/")) {
    if (!part || part === ".") continue;
    if (part === "..") {
      if (!parts.length) return null;
      parts.pop();
    } else {
      parts.push(part);
    }
  }
  const resolved = parts.join("/");
  return resolved && !isBlockedRepoPath(resolved) ? resolved : null;
}

function localized(value: any, fallback = ""): string {
  return localizedValue(value, displayLang, fallback);
}

function isDeveloper(): boolean {
  return interfaceMode === "developer";
}

function publicLayerConfigs(): JsonObject[] {
  return [...(publicContent.layers ?? [])].sort((a: JsonObject, b: JsonObject) =>
    Number(a.order ?? 999) - Number(b.order ?? 999) || String(a.id ?? "").localeCompare(String(b.id ?? ""), "en"),
  );
}

function publicLayerConfig(layerKey: string): JsonObject | undefined {
  return publicLayerConfigs().find((item: JsonObject) => String(item.id ?? "") === layerKey);
}

function publicGuides(): JsonObject[] {
  return [...(publicContent.guides ?? [])].sort((a: JsonObject, b: JsonObject) =>
    Number(a.order ?? 999) - Number(b.order ?? 999) || String(a.id ?? "").localeCompare(String(b.id ?? ""), "en"),
  );
}

function publicGuidePath(config: JsonObject): string {
  const value = config.path;
  if (value && typeof value === "object") return String(value[displayLang] ?? value.ja ?? value.en ?? "");
  return String(value ?? "");
}

function entryLevelLabel(value: string): string {
  const labels: Record<string, [string, string]> = {
    foundation: ["まず読む", "Start here"],
    intermediate: ["もう少し進む", "Go further"],
    advanced: ["深く読む", "Read deeply"],
  };
  const pair = labels[value];
  return pair ? pair[displayLang === "ja" ? 0 : 1] : value;
}

function relationLabel(relation: string): string {
  const labels: Record<string, [string, string]> = {
    owns: ["定義を所有", "owns definition"],
    imports: ["参照して使う", "imports"],
    exports: ["下流へ渡す", "exports"],
    tests: ["検査する", "tests"],
    returns_to: ["返す", "returns to"],
    delegates: ["委譲する", "delegates"],
    related_to: ["関連", "related to"],
    placed_in: ["体系層", "placed in"],
    belongs_to_topic: ["トピック", "topic"],
    links_to: ["本文リンク", "links to"],
    lexical_anchor: ["用語入口", "lexical anchor"],
    definition_owner_reference: ["定義所有者を参照", "definition-owner reference"],
    generative_source_reference: ["生成源を参照", "generative-source reference"],
    operationalized_in_reference: ["応用先を参照", "operationalized-in reference"],
    contains_term: ["用語を収録", "contains term"],
    map_reference: ["体系マップ参照", "system-map reference"],
    concept_network_reference: ["概念ネットワーク参照", "concept-network reference"],
  };
  const pair = labels[relation];
  return pair ? pair[displayLang === "ja" ? 0 : 1] : relation.replaceAll("_", " ");
}

function displayGraphNodeLabel(node: JsonObject): string {
  if (!isDeveloper() && node.type === "layer") {
    const config = publicLayerConfig(String(node.key ?? ""));
    if (config) return localized(config.label, String(node.key ?? ""));
  }
  return graphNodeLabel(node, displayLang);
}

function nodeTypeLabel(type: string): string {
  const labels: Record<string, [string, string]> = {
    document: ["文書", "Document"],
    observed_document: ["文書", "Document"],
    concept: ["概念", "Concept"],
    topic: ["トピック", "Topic"],
    layer: ["体系層", "Layer"],
    glossary_term: ["用語", "Term"],
    source_artifact: ["案内資料", "Guide source"],
  };
  const pair = labels[type];
  return pair ? pair[displayLang === "ja" ? 0 : 1] : type;
}

function provenanceLabel(type: string): string {
  const labels: Record<string, [string, string]> = {
    manifest: ["文書台帳", "manifest"],
    markdown: ["本文", "Markdown"],
    markdown_link: ["本文リンク", "Markdown link"],
    glossary: ["用語集", "Glossary"],
    system_map: ["体系マップ", "System Map"],
    concept_network: ["概念ネットワーク", "Concept Network"],
  };
  const pair = labels[type];
  return pair ? pair[displayLang === "ja" ? 0 : 1] : type.replaceAll("_", " ");
}

function matchFieldLabel(field: string): string {
  const base = field.split(".", 1)[0];
  const labels: Record<string, [string, string]> = {
    title: ["タイトル", "title"],
    owned_concept: ["定義概念", "owned concept"],
    aliases: ["別名・入口表現", "alias / entry phrase"],
    topics: ["トピック", "topic"],
    reader_questions: ["読者の問い", "reader question"],
    role: ["文書の役割", "document role"],
    scope: ["扱う範囲", "scope"],
  };
  const pair = labels[base];
  return pair ? pair[displayLang === "ja" ? 0 : 1] : field.replaceAll("_", " ");
}

function matchMethodLabel(method: string): string {
  const labels: Record<string, [string, string]> = {
    exact: ["完全一致", "exact match"],
    contains: ["部分一致", "contains"],
    term_coverage: ["語のまとまり", "term coverage"],
    query_expansion: ["検索上の関連表現", "search-only expansion"],
    char_ngram: ["文字列の近さ", "character similarity"],
  };
  const pair = labels[method];
  return pair ? pair[displayLang === "ja" ? 0 : 1] : method.replaceAll("_", " ");
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

function docByPath(path: string): JsonObject | undefined {
  return (docsIndex.documents ?? []).find((doc: JsonObject) => String(doc.path ?? "") === path);
}

function graphNodeByPath(path: string): JsonObject | undefined {
  return (docsGraph.nodes ?? []).find(
    (node: JsonObject) => (node.type === "document" || node.type === "observed_document") && String(node.path ?? "") === path,
  );
}

function candidatePayload(): JsonObject | null {
  return registrationCandidates?.registration_candidates ?? null;
}

function candidateList(): JsonObject[] {
  return candidatePayload()?.candidates ?? [];
}

function candidateByPath(path: string): JsonObject | undefined {
  return candidateList().find((candidate: JsonObject) => String(candidate.path ?? "") === path);
}

function candidateTitle(candidate: JsonObject): string {
  const proposed = candidate.proposed ?? {};
  const preferred = displayLang === "ja" ? proposed.title_ja : proposed.title_en;
  const fallback = displayLang === "ja" ? proposed.title_en : proposed.title_ja;
  return String(preferred || fallback || proposed.doc_id || candidate.path || "");
}

function candidateRole(candidate: JsonObject): string {
  const proposed = candidate.proposed ?? {};
  return String((displayLang === "ja" ? proposed.role_ja : proposed.role_en) || proposed.role_ja || proposed.role_en || "");
}

function candidateQuestionList(candidate: JsonObject): string[] {
  const questions = candidate.proposed?.discovery?.reader_questions ?? {};
  return (questions[displayLang] ?? questions.ja ?? questions.en ?? []).map((value: any) => String(value));
}

function candidateAliases(candidate: JsonObject): string[] {
  const aliases = candidate.proposed?.discovery?.aliases ?? {};
  return (aliases[displayLang] ?? aliases.ja ?? aliases.en ?? []).map((value: any) => String(value));
}

function candidateSearchText(candidate: JsonObject): string {
  const proposed = candidate.proposed ?? {};
  const discovery = proposed.discovery ?? {};
  const values = [
    candidate.path,
    candidate.recommended_action,
    candidate.navigation?.visibility,
    proposed.doc_id,
    proposed.title_ja,
    proposed.title_en,
    proposed.layer,
    proposed.status,
    proposed.scope,
    proposed.role_ja,
    proposed.role_en,
    ...(discovery.topics ?? []),
    ...(discovery.aliases?.ja ?? []),
    ...(discovery.aliases?.en ?? []),
    ...(discovery.reader_questions?.ja ?? []),
    ...(discovery.reader_questions?.en ?? []),
    ...(candidate.review?.needs_human_judgment ?? []),
  ];
  return values.filter(Boolean).join(" ").normalize("NFKC").toLocaleLowerCase("ja-JP");
}

function readerButton(path: string, className = "text-button"): HTMLButtonElement {
  const read = button(displayLang === "ja" ? "読む" : "Read", className);
  read.addEventListener("click", () => setRoute({ read: path }));
  return read;
}

function rawFileLink(path: string, className = "text-link"): HTMLAnchorElement {
  const raw = el("a", className, displayLang === "ja" ? "元ファイル" : "Raw file");
  raw.href = encodePath(path);
  raw.target = "_blank";
  raw.rel = "noopener";
  return raw;
}

function graphNodeForDocument(doc: JsonObject): string | undefined {
  const direct = `doc:${doc.id}`;
  if (graphNodeMap(docsGraph).has(direct)) return direct;
  const byPath = (docsGraph.nodes ?? []).find((node: JsonObject) => node.type === "document" && node.path === doc.path);
  return byPath?.id;
}

function navBar(active: string): HTMLElement {
  const nav = el("nav", "view-tabs");
  const items: Array<[string, string, Record<string, string>]> = isDeveloper()
    ? [
        ["home", displayLang === "ja" ? "読む" : "Read", {}],
        ["search", displayLang === "ja" ? "検索" : "Search", { view: "search" }],
        ["relations", displayLang === "ja" ? "関係マップ" : "Relations", { view: "relations" }],
        ["candidates", displayLang === "ja" ? "候補レビュー" : "Candidate review", { view: "candidates" }],
        ["audit", displayLang === "ja" ? "データ点検" : "Data audit", { view: "audit" }],
      ]
    : [
        ["home", displayLang === "ja" ? "読む" : "Read", {}],
        ["search", displayLang === "ja" ? "検索" : "Search", { view: "search" }],
        ["relations", displayLang === "ja" ? "関係マップ" : "Relations", { view: "relations" }],
      ];
  for (const [id, label, target] of items) {
    const b = button(label, `tab ${id === active ? "active" : ""}`);
    b.addEventListener("click", () => setRoute(target));
    nav.append(b);
  }
  return nav;
}

function dataBanner(): HTMLElement {
  const profile = String(docsIndex.source?.visibility_profile ?? "unknown");
  if (!isDeveloper()) {
    if (profile === "public") return el("div", "public-profile-spacer");
    const notice = el("div", "public-preview-note");
    notice.append(
      badge(displayLang === "ja" ? "公開準備プレビュー" : "Release-preparation preview", "warn"),
      el(
        "span",
        "",
        displayLang === "ja"
          ? "現在は公開候補データで表示しています。候補レビューや登録診断はこの公開面には表示されません。"
          : "This view currently uses release-preparation data. Candidate review and registration diagnostics are not shown on the public surface.",
      ),
    );
    return notice;
  }

  const wrap = el("div", "data-banner");
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

function publicLayerCard(config: JsonObject): HTMLElement {
  const item = el("article", "public-layer-card");
  const label = localized(config.label, String(config.id ?? ""));
  const subtitle = localized(config.subtitle, "");
  const description = localized(config.description, "");
  const top = el("div", "public-layer-card-top");
  top.append(el("span", "public-layer-code", label));
  if (subtitle) top.append(el("span", "public-layer-subtitle", subtitle));
  item.append(top);
  if (description) item.append(el("p", "public-layer-description", description));
  const actions = el("div", "card-actions");
  const open = button(displayLang === "ja" ? "この層を見る" : "Open this layer", "button primary compact-button");
  open.addEventListener("click", () => setRoute({ layer: `layer:${String(config.id ?? "")}` }));
  actions.append(open);
  const readmePath = String(config.readme_path ?? "");
  if (readmePath && readerAllowedPaths().has(readmePath)) {
    const readme = readerButton(readmePath, "button quiet-button");
    readme.textContent = displayLang === "ja" ? "層の案内を読む" : "Read layer guide";
    actions.append(readme);
  }
  item.append(actions);
  return item;
}

function publicGuideCard(config: JsonObject): HTMLElement {
  const item = el("article", "guide-card");
  const label = localized(config.label, String(config.id ?? ""));
  const purpose = localized(config.purpose, "");
  item.append(el("div", "guide-kicker", displayLang === "ja" ? "案内文書" : "Guide"), el("h3", "guide-title", label));
  if (purpose) item.append(el("p", "guide-copy", purpose));
  const path = publicGuidePath(config);
  const actions = el("div", "card-actions");
  if (path && readerAllowedPaths().has(path)) actions.append(readerButton(path, "button primary compact-button"));
  const graphNode = graphNodeByPath(path);
  if (graphNode) {
    const relations = button(displayLang === "ja" ? "関係を見る" : "Relations", "button quiet-button");
    relations.addEventListener("click", () => setRoute({ graph: String(graphNode.id) }));
    actions.append(relations);
  }
  item.append(actions);
  return item;
}

function publicQuestionEntrances(): Array<{ topicId: string; question: string }> {
  const rows: Array<{ topicId: string; question: string }> = [];
  for (const card of browseTopics(docsIndex)) {
    const questions = card.starter_questions?.[displayLang] ?? card.starter_questions?.ja ?? card.starter_questions?.en ?? [];
    if (questions.length) rows.push({ topicId: String(card.topic_id), question: String(questions[0]) });
  }
  return rows.slice(0, 8);
}

function renderPublicHome(): HTMLElement {
  const page = el("main", "page public-home");
  page.append(navBar("home"), dataBanner());

  const home = publicContent.home ?? {};
  const hero = el("section", "public-hero");
  hero.append(
    eyebrow(localized(home.eyebrow, "SCIENTIFIC ONTOLOGY")),
    el("h1", "public-hero-title", localized(home.title, displayLang === "ja" ? "存在境界論を読む" : "Read Scientific Ontology")),
    el("p", "public-hero-copy", localized(home.description, "")),
    searchBox(),
  );

  const quick = el("div", "public-quick-questions");
  quick.append(el("span", "quick-label", displayLang === "ja" ? "問いから入る" : "Start with a question"));
  for (const row of publicQuestionEntrances().slice(0, 5)) {
    const q = button(row.question, "question-button public-question-button");
    q.addEventListener("click", () => setRoute({ view: "search", q: row.question }));
    quick.append(q);
  }
  hero.append(quick);
  page.append(hero);

  const layerSection = el("section", "section public-section");
  layerSection.append(
    eyebrow(displayLang === "ja" ? "READ BY LAYER" : "READ BY LAYER"),
    el("h2", "section-title", displayLang === "ja" ? "体系の層から読む" : "Read through the system layers"),
    el(
      "p",
      "section-copy",
      displayLang === "ja"
        ? "各層のREADMEが持つ役割を短くほどき、いま読みたい場所へ直接入れるようにしています。層は重要度の順位ではなく、体系上の役割です。"
        : "Each layer README is condensed into a reader-facing entrance. Layers express roles in the system, not an importance ranking.",
    ),
  );
  const layerGrid = el("div", "public-layer-grid");
  for (const config of publicLayerConfigs()) layerGrid.append(publicLayerCard(config));
  layerSection.append(layerGrid);
  page.append(layerSection);

  const guideSection = el("section", "section guide-section");
  guideSection.append(
    eyebrow(displayLang === "ja" ? "GUIDE DOCUMENTS" : "GUIDE DOCUMENTS"),
    el("h2", "section-title", displayLang === "ja" ? "目的から案内文書を選ぶ" : "Choose a guide by what you need"),
    el(
      "p",
      "section-copy",
      displayLang === "ja"
        ? "ファイル名ではなく、『何を知りたいときに読むか』から選べます。"
        : "Choose by what you want to understand, rather than by filename.",
    ),
  );
  const guideGrid = el("div", "guide-grid");
  for (const guide of publicGuides()) guideGrid.append(publicGuideCard(guide));
  guideSection.append(guideGrid);
  page.append(guideSection);

  const topicSection = el("section", "section topic-strip-section");
  topicSection.append(
    eyebrow(displayLang === "ja" ? "INTERESTS" : "INTERESTS"),
    el("h2", "section-title", displayLang === "ja" ? "関心から寄り道する" : "Take a route through an interest"),
    el(
      "p",
      "section-copy",
      displayLang === "ja"
        ? "トピックは厳密な分類ではなく、別の入口です。同じ文書が複数の関心から見つかることがあります。"
        : "Topics are alternate entrances, not strict classifications. A document can be reachable from more than one interest.",
    ),
  );
  const strip = el("div", "topic-strip");
  for (const card of browseTopics(docsIndex)) {
    const b = button(localized(card.label, String(card.topic_id)), "topic-pill");
    b.addEventListener("click", () => setRoute({ topic: String(card.topic_id) }));
    strip.append(b);
  }
  topicSection.append(strip);
  page.append(topicSection);
  return page;
}

function renderExplore(): HTMLElement {
  return renderPublicHome();
}

function docCard(doc: JsonObject): HTMLElement {
  const item = el("article", `doc-card card ${isDeveloper() ? "developer-doc-card" : "public-doc-card"}`);
  const level = String(doc.entry_level ?? doc.discovery?.entry_level ?? "");
  const state = String(doc.state ?? "");
  const top = el("div", "card-meta");
  if (level) top.append(badge(isDeveloper() ? level : entryLevelLabel(level)));
  if (isDeveloper() && state) top.append(badge(state, state === "public-candidate" ? "warn" : ""));
  if (top.childElementCount) item.append(top);
  item.append(el("h3", "card-title", titleForDoc(doc)));
  const role = roleForDoc(doc);
  if (role) item.append(el("p", "card-copy", role));
  const questions = doc.reader_questions ?? doc.discovery?.reader_questions ?? {};
  const qList = questions[displayLang] ?? questions.ja ?? questions.en ?? [];
  if (qList.length) {
    const question = el("div", "public-card-question");
    question.append(el("span", "question-mark", "Q"), el("span", "", String(qList[0])));
    item.append(question);
  }
  const path = String(doc.path ?? "");
  if (isDeveloper()) item.append(el("div", "path", path));
  const actions = el("div", "card-actions");
  const id = String(doc.doc_id ?? doc.id ?? "");
  if (isDeveloper()) {
    const detail = button(displayLang === "ja" ? "文書を見る" : "Inspect document", "text-button");
    detail.addEventListener("click", () => setRoute({ doc: id }));
    actions.append(detail);
    if (path) actions.append(readerButton(path), rawFileLink(path));
  } else {
    if (path) actions.append(readerButton(path, "button primary compact-button"));
    const graphId = graphNodeForDocument(doc);
    if (graphId) {
      const relations = button(displayLang === "ja" ? "関係を見る" : "Relations", "button quiet-button");
      relations.addEventListener("click", () => setRoute({ graph: graphId }));
      actions.append(relations);
    }
  }
  item.append(actions);
  return item;
}

function renderTopic(topicId: string): HTMLElement {
  const page = el("main", "page");
  page.append(navBar("home"), dataBanner());
  const payload = browsePayload(docsIndex, topicId);
  const card = payload.topic;
  const back = button(displayLang === "ja" ? "← 読む" : "← Read", "back-button");
  back.addEventListener("click", () => setRoute({}));
  page.append(back);

  const hero = el("section", "topic-hero");
  hero.append(
    eyebrow(isDeveloper() ? `TOPIC · ${topicId}` : "TOPIC"),
    el("h1", "hero-title", localized(card.label, topicId)),
    el("p", "hero-copy", localized(card.description)),
  );
  const questions = el("div", "starter-questions");
  questions.append(el("h2", "minor-title", displayLang === "ja" ? "この関心から始められる問い" : "Questions that can start from here"));
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

function renderPublicLayer(layerId: string): HTMLElement {
  const page = el("main", "page public-layer-page");
  page.append(navBar("home"), dataBanner());
  const layer = layerSummaries(docsGraph).find((row) => String(row.id) === layerId);
  if (!layer) return errorPage(`Unknown layer: ${layerId}`);
  const config = publicLayerConfig(String(layer.key));

  const back = button(displayLang === "ja" ? "← 体系から読む" : "← Read by layer", "back-button");
  back.addEventListener("click", () => setRoute({}));
  page.append(back);

  const hero = el("section", "public-layer-hero");
  const label = config ? localized(config.label, localized(layer.label, String(layer.key))) : localized(layer.label, String(layer.key));
  const subtitle = config ? localized(config.subtitle, "") : "";
  const description = config ? localized(config.description, "") : "";
  hero.append(
    eyebrow(displayLang === "ja" ? "SYSTEM LAYER" : "SYSTEM LAYER"),
    el("h1", "public-layer-title", label),
  );
  if (subtitle) hero.append(el("p", "public-layer-lead", subtitle));
  if (description) hero.append(el("p", "public-layer-copy", description));
  const heroActions = el("div", "reader-actions");
  const readmePath = String(config?.readme_path ?? "");
  if (readmePath && readerAllowedPaths().has(readmePath)) {
    const readme = readerButton(readmePath, "button primary");
    readme.textContent = displayLang === "ja" ? "この層の案内を読む" : "Read this layer guide";
    heroActions.append(readme);
  }
  hero.append(heroActions);
  page.append(hero);

  if (layer.registered.length) {
    const section = el("section", "section public-section");
    section.append(
      eyebrow(displayLang === "ja" ? "DOCUMENTS" : "DOCUMENTS"),
      el("h2", "section-title", displayLang === "ja" ? "この層で読む" : "Read in this layer"),
      el(
        "p",
        "section-copy",
        displayLang === "ja"
          ? "現在Navigatorの公開読解面に登録されている文書です。入口の深さは読み始める順の目安で、価値や真理の順位ではありません。"
          : "These documents are currently registered on the Navigator reading surface. Entry depth is a reading aid, not a ranking of value or truth.",
      ),
    );
    const grid = el("div", "doc-grid");
    for (const node of layer.registered) {
      const doc = docById(String(node.key));
      if (doc) grid.append(docCard(doc));
    }
    if (!grid.childElementCount) grid.append(el("p", "empty", displayLang === "ja" ? "現在この層の文書カードを準備中です。" : "Document cards for this layer are being prepared."));
    section.append(grid);
    page.append(section);
  } else {
    const empty = el("section", "section public-section");
    empty.append(
      el("h2", "section-title small", displayLang === "ja" ? "この層の案内から始める" : "Start with the layer guide"),
      el(
        "p",
        "section-copy",
        displayLang === "ja"
          ? "この層の個別文書カードは現在整備中です。READMEから層の役割と収録内容を確認できます。"
          : "Individual document cards for this layer are still being prepared. The README explains the layer role and included materials.",
      ),
    );
    page.append(empty);
  }

  const topicIds = new Set<string>();
  for (const node of layer.registered) {
    const doc = docById(String(node.key));
    for (const topic of doc?.discovery?.topics ?? []) topicIds.add(String(topic));
  }
  if (topicIds.size) {
    const topicSection = el("section", "section compact-section");
    topicSection.append(el("h2", "section-title small", displayLang === "ja" ? "この層から広がる関心" : "Interests reachable from this layer"));
    const strip = el("div", "topic-strip");
    for (const topicId of Array.from(topicIds).sort()) {
      const topic = docsIndex.topics?.[topicId] ?? {};
      const b = button(localized(topic, topicId), "topic-pill");
      b.addEventListener("click", () => setRoute({ topic: topicId }));
      strip.append(b);
    }
    topicSection.append(strip);
    page.append(topicSection);
  }
  return page;
}

function renderLayer(layerId: string): HTMLElement {
  if (!isDeveloper()) return renderPublicLayer(layerId);
  const page = el("main", "page");
  page.append(navBar("home"), dataBanner());
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
        card.append(el("h3", "card-title", displayGraphNodeLabel(node)), el("div", "path", String(node.path ?? "")));
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
      const path = String(node.path ?? "");
      main.append(el("strong", "", displayGraphNodeLabel(node)), el("div", "path", path));
      const candidate = candidateByPath(path);
      if (candidate) main.append(badge(displayLang === "ja" ? "登録候補あり" : "Candidate available", "warn"));
      const read = readerButton(path);
      const relation = button(displayLang === "ja" ? "関係を見る" : "Relations", "text-button");
      relation.addEventListener("click", () => setRoute({ graph: String(node.id) }));
      row.append(main, read, relation);
      if (candidate) {
        const inspectCandidate = button(displayLang === "ja" ? "候補" : "Candidate", "text-button");
        inspectCandidate.addEventListener("click", () => setRoute({ view: "candidates", candidate: path }));
        row.append(inspectCandidate);
      }
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
  section.append(
    eyebrow("SEARCH"),
    el("h1", "hero-title", displayLang === "ja" ? "問い・用語から探す" : "Search by question or term"),
    el(
      "p",
      "hero-copy",
      isDeveloper()
        ? displayLang === "ja"
          ? "検索は直接関連だけを順位づけします。関係グラフのcentralityやリンク数は検索スコアへ混ぜていません。"
          : "Search ranks direct relevance only. Graph centrality and link counts are not mixed into search scores."
        : displayLang === "ja"
          ? "分かっている用語でも、まだ形になっていない問いでも探せます。結果には、なぜ見つかったかを確認できる説明を残しています。"
          : "Search with a known term or with a question that is not yet fully formed. Each result keeps an explanation of why it matched.",
    ),
    searchBox(query),
  );
  if (!query) {
    if (!isDeveloper()) {
      const quick = el("div", "public-quick-questions search-quick-questions");
      quick.append(el("span", "quick-label", displayLang === "ja" ? "たとえば" : "Try"));
      for (const row of publicQuestionEntrances().slice(0, 5)) {
        const q = button(row.question, "question-button public-question-button");
        q.addEventListener("click", () => setRoute({ view: "search", q: row.question }));
        quick.append(q);
      }
      section.append(quick);
    }
    page.append(section);
    return page;
  }
  const found = searchDocuments(query, docsIndex, "auto", 12, "both");
  section.append(
    el(
      "div",
      "search-summary",
      isDeveloper()
        ? `${displayLang === "ja" ? "判定モード" : "Resolved mode"}: ${found.mode} · ${found.results.length} ${displayLang === "ja" ? "件" : "results"}`
        : `${found.results.length} ${displayLang === "ja" ? "件見つかりました" : "results"}`,
    ),
  );
  const results = el("div", "search-results");
  for (const result of found.results) {
    const card = el("article", `search-result card ${isDeveloper() ? "developer-search-result" : "public-search-result"}`);
    const heading = el("div", "result-heading");
    heading.append(el("h2", "card-title", titleForDoc(result)), badge(result.score.toFixed(2), "score"));
    card.append(heading);
    const role = roleForDoc(result);
    if (role) card.append(el("p", "card-copy", role));

    if (isDeveloper()) {
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
    } else {
      const details = el("details", "search-explanation");
      const summary = el("summary", "search-explanation-summary", displayLang === "ja" ? "なぜ見つかった？" : "Why did this match?");
      details.append(summary);
      const reasons = el("div", "public-match-reasons");
      for (const match of (result.matches ?? []).slice(0, 4)) {
        const row = el("div", "public-match-reason");
        row.append(
          el("span", "public-match-label", matchFieldLabel(String(match.field))),
          el("span", "public-match-method", `${matchMethodLabel(String(match.method))} · +${Number(match.contribution).toFixed(2)}`),
          el("span", "public-match-text", `“${String(match.text)}”`),
        );
        reasons.append(row);
      }
      details.append(reasons);
      card.append(details);
    }

    const actions = el("div", "card-actions");
    const path = String(result.path ?? "");
    if (isDeveloper()) {
      const detail = button(displayLang === "ja" ? "文書と関係を見る" : "Document and relations", "text-button");
      detail.addEventListener("click", () => setRoute({ doc: String(result.doc_id) }));
      actions.append(detail);
      if (path) actions.append(readerButton(path), rawFileLink(path));
    } else {
      if (path) actions.append(readerButton(path, "button primary compact-button"));
      const graphId = graphNodeForDocument(result);
      if (graphId) {
        const relations = button(displayLang === "ja" ? "関係を見る" : "Relations", "button quiet-button");
        relations.addEventListener("click", () => setRoute({ graph: graphId }));
        actions.append(relations);
      }
    }
    card.append(actions);
    results.append(card);
  }
  if (!found.results.length) {
    results.append(
      el(
        "p",
        "empty",
        displayLang === "ja"
          ? "まだ該当する文書が見つかりません。言い換えるか、読む画面から体系・案内文書を辿ってみてください。"
          : "No document matched yet. Try another phrasing or return to Read and enter through the system layers or guide documents.",
      ),
    );
  }
  section.append(results);
  page.append(section);
  return page;
}

function renderDocument(docId: string): HTMLElement {
  const doc = docById(docId);
  if (!doc) return errorPage(`Unknown document: ${docId}`);
  if (!isDeveloper()) return renderReader(String(doc.path ?? ""));
  const page = el("main", "page");
  page.append(navBar("home"), dataBanner());
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
  const headerActions = el("div", "reader-actions");
  headerActions.append(readerButton(String(doc.path), "button primary"), rawFileLink(String(doc.path), "button secondary"));
  header.append(headerActions);
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

function appendInlineMarkdown(parent: HTMLElement, text: string, sourcePath: string): void {
  const token = /(!?\[[^\]]*\]\([^)]+\)|`[^`]+`|\*\*[^*]+\*\*|\*[^*]+\*)/g;
  let cursor = 0;
  for (const match of text.matchAll(token)) {
    const index = match.index ?? 0;
    if (index > cursor) parent.append(document.createTextNode(text.slice(cursor, index)));
    const value = match[0];
    if (value.startsWith("![")) {
      const parsed = value.match(/^!\[([^\]]*)\]\(([^)]+)\)$/);
      if (parsed) {
        const alt = parsed[1];
        const href = parsed[2].trim();
        const resolved = normalizeRepoPath(sourcePath, href);
        if (resolved) {
          const img = document.createElement("img");
          img.className = "reader-image";
          img.alt = alt;
          img.loading = "lazy";
          img.src = encodePath(resolved);
          parent.append(img);
        } else {
          parent.append(document.createTextNode(alt ? `[${alt}]` : "[image]"));
        }
      }
    } else if (value.startsWith("[")) {
      const parsed = value.match(/^\[([^\]]+)\]\(([^)]+)\)$/);
      if (parsed) {
        const label = parsed[1];
        const href = parsed[2].trim();
        const a = document.createElement("a");
        a.textContent = label;
        if (href.startsWith("#")) {
          a.href = href;
        } else if (/^(https?:|mailto:)/i.test(href)) {
          a.href = href;
          a.target = "_blank";
          a.rel = "noopener noreferrer";
        } else {
          const resolved = normalizeRepoPath(sourcePath, href);
          if (resolved?.endsWith(".md") && readerAllowedPaths().has(resolved)) {
            a.href = `#${new URLSearchParams({ read: resolved }).toString()}`;
            a.addEventListener("click", (event) => {
              event.preventDefault();
              setRoute({ read: resolved });
            });
          } else if (resolved) {
            a.href = encodePath(resolved);
            a.target = "_blank";
            a.rel = "noopener";
          } else {
            a.removeAttribute("href");
          }
        }
        parent.append(a);
      }
    } else if (value.startsWith("`")) {
      parent.append(el("code", "reader-inline-code", value.slice(1, -1)));
    } else if (value.startsWith("**")) {
      const strong = el("strong");
      appendInlineMarkdown(strong, value.slice(2, -2), sourcePath);
      parent.append(strong);
    } else if (value.startsWith("*")) {
      const em = el("em");
      appendInlineMarkdown(em, value.slice(1, -1), sourcePath);
      parent.append(em);
    }
    cursor = index + value.length;
  }
  if (cursor < text.length) parent.append(document.createTextNode(text.slice(cursor)));
}

function markdownCells(line: string): string[] {
  let value = line.trim();
  if (value.startsWith("|")) value = value.slice(1);
  if (value.endsWith("|")) value = value.slice(0, -1);
  return value.split("|").map((cell) => cell.trim());
}

function isTableSeparator(line: string): boolean {
  const cells = markdownCells(line);
  return cells.length > 0 && cells.every((cell) => /^:?-{3,}:?$/.test(cell));
}

function headingId(text: string, seen: Map<string, number>): string {
  const base = text
    .normalize("NFKC")
    .toLowerCase()
    .replace(/[`*_~[\](){}<>]/g, "")
    .replace(/[^\p{Letter}\p{Number}]+/gu, "-")
    .replace(/^-+|-+$/g, "") || "section";
  const count = seen.get(base) ?? 0;
  seen.set(base, count + 1);
  return count ? `${base}-${count + 1}` : base;
}

function renderMarkdown(text: string, sourcePath: string): HTMLElement {
  const article = el("article", "reader-article");
  const lines = text.replace(/\r\n?/g, "\n").split("\n");
  const headingIds = new Map<string, number>();
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    if (!line.trim()) {
      i += 1;
      continue;
    }
    const fence = line.match(/^\s*```\s*([^\s`]*)\s*$/);
    if (fence) {
      const language = fence[1];
      const codeLines: string[] = [];
      i += 1;
      while (i < lines.length && !/^\s*```\s*$/.test(lines[i])) {
        codeLines.push(lines[i]);
        i += 1;
      }
      if (i < lines.length) i += 1;
      const pre = el("pre", "reader-code");
      const code = el("code", language ? `language-${language}` : "", codeLines.join("\n"));
      pre.append(code);
      article.append(pre);
      continue;
    }
    const heading = line.match(/^(#{1,6})\s+(.+?)\s*#*\s*$/);
    if (heading) {
      const level = Math.min(6, heading[1].length) as 1 | 2 | 3 | 4 | 5 | 6;
      const h = el(`h${level}`, `reader-h reader-h${level}`);
      appendInlineMarkdown(h, heading[2], sourcePath);
      h.id = headingId(heading[2], headingIds);
      article.append(h);
      i += 1;
      continue;
    }
    if (/^\s*(---+|\*\*\*+)\s*$/.test(line)) {
      article.append(document.createElement("hr"));
      i += 1;
      continue;
    }
    if (line.includes("|") && i + 1 < lines.length && isTableSeparator(lines[i + 1])) {
      const table = el("table", "reader-table");
      const thead = document.createElement("thead");
      const headRow = document.createElement("tr");
      for (const cell of markdownCells(line)) {
        const th = document.createElement("th");
        appendInlineMarkdown(th, cell, sourcePath);
        headRow.append(th);
      }
      thead.append(headRow);
      table.append(thead);
      i += 2;
      const tbody = document.createElement("tbody");
      while (i < lines.length && lines[i].trim() && lines[i].includes("|")) {
        const tr = document.createElement("tr");
        for (const cell of markdownCells(lines[i])) {
          const td = document.createElement("td");
          appendInlineMarkdown(td, cell, sourcePath);
          tr.append(td);
        }
        tbody.append(tr);
        i += 1;
      }
      table.append(tbody);
      article.append(table);
      continue;
    }
    if (/^\s*>/.test(line)) {
      const quote = el("blockquote", "reader-quote");
      const quoteLines: string[] = [];
      while (i < lines.length && /^\s*>/.test(lines[i])) {
        quoteLines.push(lines[i].replace(/^\s*>\s?/, ""));
        i += 1;
      }
      for (const [index, quoteLine] of quoteLines.entries()) {
        if (index) quote.append(document.createElement("br"));
        appendInlineMarkdown(quote, quoteLine, sourcePath);
      }
      article.append(quote);
      continue;
    }
    const listMatch = line.match(/^\s*([-*+] |\d+[.)] )(.+)$/);
    if (listMatch) {
      const ordered = /^\d/.test(listMatch[1]);
      const list = ordered ? document.createElement("ol") : document.createElement("ul");
      list.className = "reader-list";
      while (i < lines.length) {
        const current = lines[i].match(/^\s*([-*+] |\d+[.)] )(.+)$/);
        if (!current || /^\d/.test(current[1]) !== ordered) break;
        const li = document.createElement("li");
        appendInlineMarkdown(li, current[2], sourcePath);
        list.append(li);
        i += 1;
      }
      article.append(list);
      continue;
    }
    const paragraphLines: string[] = [];
    while (i < lines.length && lines[i].trim()) {
      const candidate = lines[i];
      if (paragraphLines.length && (
        /^#{1,6}\s+/.test(candidate) ||
        /^\s*```/.test(candidate) ||
        /^\s*>/.test(candidate) ||
        /^\s*([-*+] |\d+[.)] )/.test(candidate) ||
        /^\s*(---+|\*\*\*+)\s*$/.test(candidate) ||
        (candidate.includes("|") && i + 1 < lines.length && isTableSeparator(lines[i + 1]))
      )) break;
      paragraphLines.push(candidate.trim());
      i += 1;
    }
    const paragraph = el("p", "reader-paragraph");
    appendInlineMarkdown(paragraph, paragraphLines.join("\n"), sourcePath);
    article.append(paragraph);
  }
  return article;
}

async function fetchUtf8Strict(path: string): Promise<{ text: string; contentType: string }> {
  if (!readerAllowedPaths().has(path)) throw new Error(`Reader path is not in the public document graph: ${path}`);
  const response = await fetch(encodePath(path), { cache: "no-store" });
  if (!response.ok) throw new Error(`${path}: HTTP ${response.status}`);
  const bytes = await response.arrayBuffer();
  let text: string;
  try {
    text = new TextDecoder("utf-8", { fatal: true }).decode(bytes);
  } catch {
    throw new Error(
      displayLang === "ja"
        ? `${path}: UTF-8として厳密にデコードできません。表示で代替せず、原ファイルのバイト列を点検してください。`
        : `${path}: strict UTF-8 decoding failed. Inspect the source bytes instead of displaying a replacement-decoded document.`,
    );
  }
  return { text, contentType: response.headers.get("content-type") ?? "" };
}

function publicRelatedDocuments(rootId: string, limit = 6): Array<{ node: JsonObject; relation: string; direction: string }> {
  const nodeMap = graphNodeMap(docsGraph);
  const seen = new Set<string>();
  const rows: Array<{ node: JsonObject; relation: string; direction: string }> = [];
  const edges = (docsGraph.edges ?? [])
    .filter((edge: JsonObject) => edge.from === rootId || edge.to === rootId)
    .sort((a: JsonObject, b: JsonObject) =>
      String(a.relation).localeCompare(String(b.relation), "en") || String(a.from).localeCompare(String(b.from), "en") || String(a.to).localeCompare(String(b.to), "en"),
    );
  for (const edge of edges) {
    const outgoing = edge.from === rootId;
    const otherId = String(outgoing ? edge.to : edge.from);
    if (seen.has(otherId)) continue;
    const node = nodeMap.get(otherId);
    if (!node || (node.type !== "document" && node.type !== "observed_document")) continue;
    const path = String(node.path ?? "");
    if (!path || !readerAllowedPaths().has(path)) continue;
    seen.add(otherId);
    rows.push({ node, relation: String(edge.relation), direction: outgoing ? "outgoing" : "incoming" });
    if (rows.length >= limit) break;
  }
  return rows;
}

function publicReaderRelatedSection(graphNode: JsonObject): HTMLElement | null {
  const rows = publicRelatedDocuments(String(graphNode.id));
  if (!rows.length) return null;
  const section = el("section", "section reader-related-section");
  section.append(
    eyebrow(displayLang === "ja" ? "NEXT ROUTES" : "NEXT ROUTES"),
    el("h2", "section-title", displayLang === "ja" ? "この文書から、次に辿れるもの" : "Where this document can lead next"),
    el(
      "p",
      "section-copy",
      displayLang === "ja"
        ? "重要度順ではなく、現在のtyped relationで直接つながっている文書から表示しています。"
        : "These are direct typed-relation neighbors, not an importance ranking.",
    ),
  );
  const grid = el("div", "reader-related-grid");
  for (const row of rows) {
    const item = el("article", "reader-related-card");
    item.append(
      el("div", "relation-human-label", `${row.direction === "outgoing" ? "→" : "←"} ${relationLabel(row.relation)}`),
      el("h3", "card-title", displayGraphNodeLabel(row.node)),
    );
    const path = String(row.node.path ?? "");
    const doc = docByPath(path);
    const role = doc ? roleForDoc(doc) : "";
    if (role) item.append(el("p", "card-copy", role));
    const actions = el("div", "card-actions");
    actions.append(readerButton(path, "button quiet-button"));
    const relations = button(displayLang === "ja" ? "関係を見る" : "Relations", "text-button");
    relations.addEventListener("click", () => setRoute({ graph: String(row.node.id) }));
    actions.append(relations);
    item.append(actions);
    grid.append(item);
  }
  section.append(grid);
  return section;
}

function renderReader(path: string): HTMLElement {
  const page = el("main", `page reader-page ${isDeveloper() ? "developer-reader" : "public-reader"}`);
  page.append(navBar(isDeveloper() ? "reader" : "home"), dataBanner());
  const back = button(displayLang === "ja" ? "← 戻る" : "← Back", "back-button");
  back.addEventListener("click", () => history.length > 1 ? history.back() : setRoute({}));
  page.append(back);

  if (!readerAllowedPaths().has(path)) {
    page.append(el("p", "error", displayLang === "ja" ? `Reader対象外のパスです: ${path}` : `Path is outside the Reader boundary: ${path}`));
    return page;
  }

  const doc = docByPath(path);
  const graphNode = graphNodeByPath(path);
  const title = doc ? titleForDoc(doc) : graphNode ? displayGraphNodeLabel(graphNode) : path.split("/").at(-1) ?? path;
  const header = el("section", "reader-header");
  const decodeState = badge(displayLang === "ja" ? "UTF-8 strict 読込中" : "UTF-8 strict loading", "warn");
  decodeState.id = "reader-decode-state";
  if (isDeveloper()) {
    header.append(eyebrow("READER · UTF-8 STRICT"), el("h1", "hero-title", title), el("div", "path", path), decodeState);
  } else {
    header.append(eyebrow(displayLang === "ja" ? "READ" : "READ"), el("h1", "reader-public-title", title));
    const role = doc ? roleForDoc(doc) : "";
    if (role) header.append(el("p", "reader-public-role", role));
  }
  const actions = el("div", "reader-actions");
  if (isDeveloper() && doc) {
    const inspect = button(displayLang === "ja" ? "文書情報" : "Document info", "button secondary");
    inspect.addEventListener("click", () => setRoute({ doc: String(doc.doc_id ?? doc.id) }));
    actions.append(inspect);
  }
  if (graphNode) {
    const relations = button(displayLang === "ja" ? "関係を見る" : "Relations", isDeveloper() ? "button secondary" : "button quiet-button");
    relations.addEventListener("click", () => setRoute({ graph: String(graphNode.id) }));
    actions.append(relations);
  }
  if (isDeveloper()) {
    const candidate = candidateByPath(path);
    if (candidate) {
      const inspectCandidate = button(displayLang === "ja" ? "登録候補" : "Registration candidate", "button secondary");
      inspectCandidate.addEventListener("click", () => setRoute({ view: "candidates", candidate: path }));
      actions.append(inspectCandidate);
    }
    actions.append(rawFileLink(path, "button ghost"));
  } else {
    actions.append(rawFileLink(path, "text-link reader-source-link"));
  }
  header.append(actions);
  page.append(header);

  if (isDeveloper()) {
    page.append(
      el(
        "div",
        "reader-boundary-note",
        displayLang === "ja"
          ? "ReaderはHTTPレスポンスの文字コード推測に依存せず、受信バイト列をUTF-8として厳密に復号します。失敗時は文字化け表示へフォールバックしません。"
          : "The Reader does not rely on browser charset guessing. It strictly decodes response bytes as UTF-8 and does not fall back to replacement-decoded text.",
      ),
    );
  }
  const shell = el("section", "reader-shell");
  shell.append(el("p", "reader-loading", displayLang === "ja" ? "文書を読み込んでいます…" : "Loading document…"));
  page.append(shell);

  void fetchUtf8Strict(path)
    .then(({ text, contentType }) => {
      decodeState.textContent = "UTF-8 strict PASS";
      decodeState.className = "badge pass";
      if (isDeveloper()) {
        const meta = el("div", "reader-http-meta");
        meta.append(
          el("span", "muted", `Content-Type: ${contentType || "(not declared)"}`),
          el("span", "muted", `${new TextEncoder().encode(text).length.toLocaleString()} bytes decoded`),
        );
        shell.replaceChildren(meta, renderMarkdown(text, path));
      } else {
        shell.replaceChildren(renderMarkdown(text, path));
        if (graphNode) {
          const related = publicReaderRelatedSection(graphNode);
          if (related) page.append(related);
        }
      }
    })
    .catch((error) => {
      decodeState.textContent = "UTF-8 strict FAIL";
      decodeState.className = "badge danger";
      shell.replaceChildren(el("p", "error", String((error as Error).message)));
    });
  return page;
}


function relationSection(rootId: string): HTMLElement {
  const section = el("section", "section relation-section");
  section.append(
    eyebrow(isDeveloper() ? "TYPED RELATION GRAPH" : (displayLang === "ja" ? "RELATIONS" : "RELATIONS")),
    el("h2", "section-title", displayLang === "ja" ? "この文書のつながり" : "Connections from this document"),
  );
  section.append(
    el(
      "p",
      "section-copy",
      isDeveloper()
        ? displayLang === "ja"
          ? "線は重要度ではなく、実際に抽出されたtyped relationです。辺を支えるsourceは下の一覧で確認できます。"
          : "Lines are extracted typed relations, not importance scores. Provenance for each edge is listed below."
        : displayLang === "ja"
          ? "線は重要度ではなく、文書台帳・用語集・体系図・本文リンクなどから現在確認できる関係です。"
          : "Lines are current typed relations observed from the document ledger, glossary, system maps, and Markdown links; they are not importance scores.",
    ),
  );
  const map = relationMap(rootId);
  section.append(map);
  const full = button(displayLang === "ja" ? "関係マップで広げる" : "Open the relation map", "button secondary");
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
  svg.setAttribute("aria-label", `${displayGraphNodeLabel(root)} relation map`);
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
    const rel = el("span", "relation-type", isDeveloper() ? String(edge.relation) : relationLabel(String(edge.relation)));
    const label = el("span", "relation-target", displayGraphNodeLabel(other));
    const provTypes = Array.from(new Set<string>((edge.provenance ?? []).map((p: JsonObject) => String(p.source_type ?? "")).filter(Boolean))).map((value: string) => isDeveloper() ? value : provenanceLabel(value)).join(" + ");
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
  text.textContent = truncate(displayGraphNodeLabel(node), root ? 34 : 28);
  const type = document.createElementNS(ns, "text");
  type.setAttribute("x", String(x));
  type.setAttribute("y", String(y + 15));
  type.setAttribute("text-anchor", "middle");
  type.setAttribute("class", "svg-node-type");
  type.textContent = isDeveloper() ? String(node.type) : nodeTypeLabel(String(node.type));
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
  text.textContent = truncate(isDeveloper() ? relation : relationLabel(relation), 24);
  line.dataset.direction = direction;
  svg.append(line, text);
}

function renderRelations(nodeQuery = ""): HTMLElement {
  const page = el("main", "page");
  page.append(navBar("relations"), dataBanner());
  const section = el("section", "section relation-page");
  section.append(
    eyebrow(isDeveloper() ? "TYPED RELATION GRAPH" : "RELATION MAP"),
    el("h1", "hero-title", displayLang === "ja" ? "関係から読む" : "Read through relations"),
    el(
      "p",
      "hero-copy",
      isDeveloper()
        ? displayLang === "ja"
          ? "文書・概念・トピック・Glossary語・体系層をノードとして、宣言関係と観測リンクを区別したまま辿ります。"
          : "Traverse documents, concepts, topics, glossary terms, and system layers while preserving the distinction between declared relations and observed links."
        : displayLang === "ja"
          ? "文書、概念、用語、トピック、体系層がどこでつながっているかを、関係の向きを保ったまま辿れます。線の多さは重要度を意味しません。"
          : "Follow how documents, concepts, terms, topics, and system layers connect while preserving relation direction. More lines do not mean greater importance.",
    ),
  );
  const form = el("form", "graph-search");
  const input = el("input", "search-input") as HTMLInputElement;
  input.placeholder = isDeveloper()
    ? displayLang === "ja" ? "文書名・概念・Glossary語・node ID" : "Document, concept, glossary term, or node ID"
    : displayLang === "ja" ? "文書名・概念・用語から探す" : "Find a document, concept, or term";
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

  if (!isDeveloper()) {
    const legend = el("div", "relation-legend");
    const relations = ["owns", "imports", "returns_to", "placed_in", "belongs_to_topic", "links_to"];
    for (const relation of relations) legend.append(el("span", "relation-legend-item", relationLabel(relation)));
    section.append(legend);
  }

  if (nodeQuery) {
    try {
      const rootId = resolveGraphNode(docsGraph, nodeQuery);
      const root = graphNodeMap(docsGraph).get(rootId)!;
      const current = el("div", "graph-current");
      current.append(
        el("h2", "section-title small", displayGraphNodeLabel(root)),
        badge(isDeveloper() ? String(root.type) : nodeTypeLabel(String(root.type))),
      );
      if (isDeveloper()) current.append(el("div", "path", String(root.path ?? root.id)));
      const rootPath = String(root.path ?? "");
      if ((root.type === "document" || root.type === "observed_document") && readerAllowedPaths().has(rootPath)) {
        current.append(readerButton(rootPath, isDeveloper() ? "text-button" : "button quiet-button"));
      }
      section.append(current, relationMap(rootId));
    } catch (error) {
      section.append(el("p", "error", String((error as Error).message)));
    }
  } else {
    const starters = el("div", "starter-node-grid public-relation-starters");
    const seeds = ["doc:scientific_ontology_concept_network", "doc:meaning_generation_model", "topic:ai", "layer:sat_truth"];
    for (const id of seeds) {
      const node = graphNodeMap(docsGraph).get(id);
      if (!node) continue;
      const b = button(displayGraphNodeLabel(node), "starter-node");
      b.addEventListener("click", () => setRoute({ graph: id }));
      starters.append(b);
    }
    section.append(el("h2", "minor-title", displayLang === "ja" ? "例から開く" : "Open an example"), starters);
  }
  page.append(section);
  return page;
}

function candidateStateBanner(): HTMLElement {
  const payload = candidatePayload();
  const banner = el("div", "candidate-boundary-note");
  banner.append(badge("CANDIDATE PREVIEW", "warn"));
  banner.append(
    el(
      "span",
      "",
      displayLang === "ja"
        ? "これはmanifest登録前のレビュー面です。表示中のrole・topic・問い・doc_idは候補であり、canonical ownershipや検索順位を変更しません。"
        : "This is a pre-manifest review surface. Proposed roles, topics, questions, and doc IDs are candidates only; they do not change canonical ownership or search ranking.",
    ),
  );
  if (!payload) banner.append(badge(displayLang === "ja" ? "候補データ未読込" : "Candidate data unavailable", "danger"));
  return banner;
}

function candidateMetric(label: string, value: string): HTMLElement {
  const box = el("div", "stat-box");
  box.append(el("span", "stat-value", value), el("span", "stat-label", label));
  return box;
}

function candidateDetail(candidate: JsonObject): HTMLElement {
  const page = el("main", "page");
  page.append(navBar("candidates"), dataBanner(), candidateStateBanner());
  const back = button(displayLang === "ja" ? "← 候補一覧" : "← Candidate list", "back-button");
  back.addEventListener("click", () => setRoute({ view: "candidates" }));
  page.append(back);

  const proposed = candidate.proposed ?? {};
  const discovery = proposed.discovery ?? {};
  const review = candidate.review ?? {};
  const hero = el("section", "doc-header candidate-detail-header");
  const meta = el("div", "doc-meta-line");
  meta.append(
    badge(String(candidate.recommended_action ?? "candidate"), "warn"),
    badge(String(review.confidence ?? "unknown")),
    badge(String(candidate.navigation?.visibility ?? "unclassified")),
    badge(String(discovery.entry_level ?? "unclassified")),
  );
  hero.append(
    eyebrow(`REGISTRATION CANDIDATE · ${String(proposed.doc_id ?? "")}`),
    el("h1", "hero-title", candidateTitle(candidate)),
    meta,
  );
  const role = candidateRole(candidate);
  if (role) hero.append(el("p", "hero-copy", role));
  hero.append(el("div", "path", String(candidate.path ?? "")));
  const actions = el("div", "reader-actions");
  const path = String(candidate.path ?? "");
  if (path && readerAllowedPaths().has(path)) actions.append(readerButton(path, "button primary"));
  const graphId = String(candidate.observed_node_id ?? "");
  if (graphId && graphNodeMap(docsGraph).has(graphId)) {
    const relations = button(displayLang === "ja" ? "現在の関係を見る" : "Current relations", "button secondary");
    relations.addEventListener("click", () => setRoute({ graph: graphId }));
    actions.append(relations);
  }
  if (path) actions.append(rawFileLink(path, "button ghost"));
  hero.append(actions);
  page.append(hero);

  const info = el("div", "candidate-detail-grid");
  const identity = el("section", "info-panel");
  identity.append(el("h2", "minor-title", displayLang === "ja" ? "提案された登録情報" : "Proposed registration"));
  const identityRows: Array<[string, string]> = [
    ["doc_id", String(proposed.doc_id ?? "")],
    [displayLang === "ja" ? "文書型" : "Document type", String(proposed.document_type ?? "")],
    [displayLang === "ja" ? "体系層" : "Layer", String(proposed.layer ?? "")],
    ["status", String(proposed.status ?? "")],
    ["public_profile", String(proposed.public_profile ?? "")],
    ["state", String(proposed.state ?? "")],
  ];
  for (const [label, value] of identityRows) {
    if (!value) continue;
    const row = el("div", "candidate-kv");
    row.append(el("span", "candidate-k", label), el("span", "candidate-v", value));
    identity.append(row);
  }
  if (proposed.scope) {
    identity.append(el("h3", "candidate-subtitle", "scope"), el("p", "card-copy", String(proposed.scope)));
  }

  const discoveryPanel = el("section", "info-panel");
  discoveryPanel.append(el("h2", "minor-title", displayLang === "ja" ? "探索メタデータ案" : "Discovery metadata proposal"));
  const topicWrap = el("div", "chip-wrap");
  for (const topic of discovery.topics ?? []) topicWrap.append(badge(String(topic)));
  if (!topicWrap.childElementCount) topicWrap.append(el("span", "muted", displayLang === "ja" ? "topicなし" : "No topics"));
  discoveryPanel.append(el("h3", "candidate-subtitle", "topics"), topicWrap);
  const questions = candidateQuestionList(candidate);
  discoveryPanel.append(el("h3", "candidate-subtitle", displayLang === "ja" ? "reader questions" : "reader questions"));
  const qList = el("ul", "plain-list");
  for (const question of questions) qList.append(el("li", "", question));
  if (!questions.length) qList.append(el("li", "muted", displayLang === "ja" ? "この言語では未設定" : "Not set for this language"));
  discoveryPanel.append(qList);
  const aliases = candidateAliases(candidate);
  if (aliases.length) {
    discoveryPanel.append(el("h3", "candidate-subtitle", "aliases"));
    const aliasWrap = el("div", "chip-wrap");
    for (const alias of aliases) aliasWrap.append(badge(alias));
    discoveryPanel.append(aliasWrap);
  }
  info.append(identity, discoveryPanel);
  page.append(info);

  const language = proposed.language_relation ?? {};
  const languagePanel = el("section", "audit-panel candidate-review-panel");
  languagePanel.append(el("h2", "section-title small", displayLang === "ja" ? "言語関係" : "Language relation"));
  const langRows: Array<[string, string]> = [
    ["family_id", String(language.family_id ?? "")],
    ["language", String(language.language ?? "")],
    ["role", String(language.role ?? "")],
    ["counterpart_path", String(language.counterpart_path ?? "")],
  ];
  for (const [label, value] of langRows) {
    if (!value) continue;
    const row = el("div", "candidate-kv");
    row.append(el("span", "candidate-k", label), el("span", "candidate-v path", value));
    languagePanel.append(row);
  }
  page.append(languagePanel);

  const reviewPanel = el("section", "audit-panel candidate-review-panel");
  reviewPanel.append(el("h2", "section-title small", displayLang === "ja" ? "人間レビューが必要な点" : "Human review points"));
  const needs = (review.needs_human_judgment ?? []).map((value: any) => String(value));
  if (needs.length) {
    const needsWrap = el("div", "chip-wrap");
    for (const item of needs) needsWrap.append(badge(item, "warn"));
    reviewPanel.append(needsWrap);
  } else {
    reviewPanel.append(el("p", "muted", displayLang === "ja" ? "明示された追加判断項目はありません。" : "No additional human-judgment item is explicitly listed."));
  }
  if (review.notes || candidate.notes) reviewPanel.append(el("p", "card-copy", String(review.notes ?? candidate.notes)));
  page.append(reviewPanel);

  const evidencePanel = el("section", "audit-panel candidate-review-panel");
  evidencePanel.append(
    el("h2", "section-title small", displayLang === "ja" ? "この候補の根拠" : "Evidence for this candidate"),
    el(
      "p",
      "section-copy",
      displayLang === "ja"
        ? "候補生成時に参照した現在本文の箇所です。ここにない意味を補って登録案を強めてはいません。"
        : "These are locations in the current text used when generating the candidate. The proposal is not strengthened by adding meanings absent from this evidence.",
    ),
  );
  const evidenceList = el("div", "candidate-evidence-list");
  for (const evidence of review.evidence ?? []) {
    const row = el("div", "candidate-evidence");
    const head = el("div", "candidate-evidence-head");
    head.append(badge(String(evidence.kind ?? "evidence")), el("span", "path", `${String(evidence.path ?? candidate.path ?? "")}:${String(evidence.line ?? "")}`));
    row.append(head, el("p", "candidate-evidence-text", String(evidence.text ?? "")));
    evidenceList.append(row);
  }
  if (!evidenceList.childElementCount) evidenceList.append(el("p", "muted", displayLang === "ja" ? "根拠抜粋なし" : "No evidence excerpt"));
  evidencePanel.append(evidenceList);
  page.append(evidencePanel);
  return page;
}

function renderCandidates(candidatePath = ""): HTMLElement {
  if (candidatePath) {
    const candidate = candidateByPath(candidatePath);
    return candidate ? candidateDetail(candidate) : errorPage(`Unknown registration candidate: ${candidatePath}`);
  }

  const page = el("main", "page");
  page.append(navBar("candidates"), dataBanner(), candidateStateBanner());
  const payload = candidatePayload();
  const section = el("section", "section candidate-page");
  section.append(
    eyebrow("REGISTRATION CANDIDATES"),
    el("h1", "hero-title", displayLang === "ja" ? "未登録文書を、登録前にUIで読む" : "Review unregistered documents before manifest registration"),
    el(
      "p",
      "hero-copy",
      displayLang === "ja"
        ? "100文書の暫定地図です。本文を改稿せず、提案されたrole・topic・問い・言語関係・確認事項をReaderと現在の関係グラフに照らして点検します。"
        : "This is a provisional map of 100 documents. Review proposed roles, topics, questions, language relations, and judgment points against the Reader and current relation graph without rewriting the documents.",
    ),
  );
  if (!payload) {
    section.append(el("p", "error", displayLang === "ja" ? "候補preview JSONを読み込めませんでした。" : "Candidate preview JSON could not be loaded."));
    page.append(section);
    return page;
  }

  const summary = payload.summary ?? {};
  const stats = el("div", "audit-stats candidate-stats");
  stats.append(
    candidateMetric(displayLang === "ja" ? "候補" : "Candidates", String(summary.total_candidates ?? candidateList().length)),
    candidateMetric(displayLang === "ja" ? "高信頼" : "High confidence", String(summary.by_confidence?.high ?? 0)),
    candidateMetric(displayLang === "ja" ? "要確認" : "Medium confidence", String(summary.by_confidence?.medium ?? 0)),
    candidateMetric(displayLang === "ja" ? "主要表示候補" : "Primary navigation", String(summary.by_navigation_visibility?.primary ?? 0)),
  );
  section.append(stats);

  const filters = el("div", "candidate-filters");
  const queryLabel = el("label", "candidate-filter");
  queryLabel.append(el("span", "candidate-filter-label", displayLang === "ja" ? "候補内検索" : "Filter candidates"));
  const queryInput = el("input", "search-input") as HTMLInputElement;
  queryInput.type = "search";
  queryInput.placeholder = displayLang === "ja" ? "タイトル・role・問い・path" : "Title, role, question, or path";
  queryLabel.append(queryInput);

  function makeSelect(label: string, values: string[], allLabel: string): { wrap: HTMLElement; select: HTMLSelectElement } {
    const wrap = el("label", "candidate-filter");
    wrap.append(el("span", "candidate-filter-label", label));
    const select = document.createElement("select");
    select.className = "candidate-select";
    const all = document.createElement("option");
    all.value = "";
    all.textContent = allLabel;
    select.append(all);
    for (const value of values) {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = value;
      select.append(option);
    }
    wrap.append(select);
    return { wrap, select };
  }

  const allCandidates = candidateList().slice().sort((a: JsonObject, b: JsonObject) =>
    String(a.proposed?.layer ?? "").localeCompare(String(b.proposed?.layer ?? ""), "en") ||
    candidateTitle(a).localeCompare(candidateTitle(b), displayLang === "ja" ? "ja" : "en"),
  );
  const layers = Array.from(new Set(allCandidates.map((candidate: JsonObject) => String(candidate.proposed?.layer ?? "")).filter(Boolean))).sort();
  const actions = Array.from(new Set(allCandidates.map((candidate: JsonObject) => String(candidate.recommended_action ?? "")).filter(Boolean))).sort();
  const confidences = Array.from(new Set(allCandidates.map((candidate: JsonObject) => String(candidate.review?.confidence ?? "")).filter(Boolean))).sort();
  const visibilities = Array.from(new Set(allCandidates.map((candidate: JsonObject) => String(candidate.navigation?.visibility ?? "")).filter(Boolean))).sort();
  const layerFilter = makeSelect(displayLang === "ja" ? "体系層" : "Layer", layers, displayLang === "ja" ? "すべて" : "All");
  const actionFilter = makeSelect(displayLang === "ja" ? "推奨処理" : "Recommended action", actions, displayLang === "ja" ? "すべて" : "All");
  const confidenceFilter = makeSelect(displayLang === "ja" ? "confidence" : "Confidence", confidences, displayLang === "ja" ? "すべて" : "All");
  const visibilityFilter = makeSelect(displayLang === "ja" ? "表示役割" : "Visibility", visibilities, displayLang === "ja" ? "すべて" : "All");
  filters.append(queryLabel, layerFilter.wrap, actionFilter.wrap, confidenceFilter.wrap, visibilityFilter.wrap);
  section.append(filters);

  const summaryLine = el("div", "candidate-result-summary");
  const grid = el("div", "candidate-grid");
  section.append(summaryLine, grid);

  const draw = () => {
    const query = queryInput.value.trim().normalize("NFKC").toLocaleLowerCase("ja-JP");
    const filtered = allCandidates.filter((candidate: JsonObject) => {
      if (layerFilter.select.value && candidate.proposed?.layer !== layerFilter.select.value) return false;
      if (actionFilter.select.value && candidate.recommended_action !== actionFilter.select.value) return false;
      if (confidenceFilter.select.value && candidate.review?.confidence !== confidenceFilter.select.value) return false;
      if (visibilityFilter.select.value && candidate.navigation?.visibility !== visibilityFilter.select.value) return false;
      return !query || candidateSearchText(candidate).includes(query);
    });
    summaryLine.textContent = `${filtered.length} / ${allCandidates.length} ${displayLang === "ja" ? "候補を表示" : "candidates shown"}`;
    grid.replaceChildren();
    for (const candidate of filtered) {
      const card = el("article", "candidate-card card");
      const top = el("div", "card-meta");
      top.append(
        badge(String(candidate.recommended_action ?? "candidate"), "warn"),
        badge(String(candidate.review?.confidence ?? "unknown")),
        badge(String(candidate.navigation?.visibility ?? "")),
      );
      card.append(top, el("h2", "card-title", candidateTitle(candidate)));
      const role = candidateRole(candidate);
      if (role) card.append(el("p", "card-copy", role));
      const topics = el("div", "chip-wrap candidate-topic-wrap");
      for (const topic of candidate.proposed?.discovery?.topics ?? []) topics.append(badge(String(topic)));
      if (topics.childElementCount) card.append(topics);
      const questions = candidateQuestionList(candidate);
      if (questions.length) card.append(el("div", "question-line", `Q. ${questions[0]}`));
      const needs = (candidate.review?.needs_human_judgment ?? []).map((value: any) => String(value));
      if (needs.length) card.append(el("div", "candidate-review-hint", `${displayLang === "ja" ? "確認" : "Review"}: ${needs.join(" · ")}`));
      card.append(el("div", "path", String(candidate.path ?? "")));
      const actionsRow = el("div", "card-actions");
      const inspect = button(displayLang === "ja" ? "候補詳細" : "Candidate detail", "text-button");
      inspect.addEventListener("click", () => setRoute({ view: "candidates", candidate: String(candidate.path ?? "") }));
      actionsRow.append(inspect);
      const path = String(candidate.path ?? "");
      if (path && readerAllowedPaths().has(path)) actionsRow.append(readerButton(path));
      const graphId = String(candidate.observed_node_id ?? "");
      if (graphId && graphNodeMap(docsGraph).has(graphId)) {
        const relations = button(displayLang === "ja" ? "関係" : "Relations", "text-button");
        relations.addEventListener("click", () => setRoute({ graph: graphId }));
        actionsRow.append(relations);
      }
      card.append(actionsRow);
      grid.append(card);
    }
    if (!filtered.length) grid.append(el("p", "empty", displayLang === "ja" ? "条件に合う候補はありません。" : "No candidate matches the filters."));
  };

  queryInput.addEventListener("input", draw);
  for (const select of [layerFilter.select, actionFilter.select, confidenceFilter.select, visibilityFilter.select]) select.addEventListener("change", draw);
  draw();
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
    [displayLang === "ja" ? "登録候補" : "Registration candidates", String(candidatePayload()?.summary?.total_candidates ?? 0)],
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

  if (candidatePayload()) {
    const candidateAudit = el("section", "audit-panel");
    candidateAudit.append(
      el("h2", "section-title small", displayLang === "ja" ? "登録候補preview" : "Registration candidate preview"),
      el(
        "p",
        "section-copy",
        displayLang === "ja"
          ? "観測のみ100文書に対する暫定登録案です。manifestとは分離され、検索ランキングにも入りません。"
          : "Provisional registration proposals for the 100 observed-only documents. They remain separate from the manifest and search ranking.",
      ),
    );
    const candidateOpen = button(displayLang === "ja" ? "候補レビューを開く" : "Open candidate review", "button secondary");
    candidateOpen.addEventListener("click", () => setRoute({ view: "candidates" }));
    candidateAudit.append(candidateOpen);
    section.append(candidateAudit);
  }

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
  page.append(navBar("home"), el("p", "error", message));
  return page;
}

function render(): void {
  if (!docsIndex || !docsGraph) return;
  const params = route();
  let content: HTMLElement;
  try {
    if (params.get("topic")) content = renderTopic(String(params.get("topic")));
    else if (params.get("layer")) content = renderLayer(String(params.get("layer")));
    else if (params.get("read")) content = renderReader(String(params.get("read")));
    else if (params.get("doc")) content = renderDocument(String(params.get("doc")));
    else if (params.get("graph")) content = renderRelations(String(params.get("graph")));
    else if (params.get("view") === "search") content = renderSearch(params.get("q") ?? "");
    else if (params.get("view") === "relations") content = renderRelations();
    else if (isDeveloper() && params.get("view") === "candidates") content = renderCandidates(params.get("candidate") ?? "");
    else if (isDeveloper() && params.get("view") === "audit") content = renderAudit();
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
    const candidatePromise: Promise<Response | null> = isDeveloper()
      ? fetch(CANDIDATES_URL).catch(() => null)
      : Promise.resolve(null);
    const [indexResponse, graphResponse, publicContentResponse, candidateResponse] = await Promise.all([
      fetch(INDEX_URL),
      fetch(GRAPH_URL),
      fetch(PUBLIC_CONTENT_URL),
      candidatePromise,
    ]);
    if (!indexResponse.ok) throw new Error(`docs_index.json: HTTP ${indexResponse.status}`);
    if (!graphResponse.ok) throw new Error(`docs_graph.json: HTTP ${graphResponse.status}`);
    if (!publicContentResponse.ok) throw new Error(`public-content.json: HTTP ${publicContentResponse.status}`);
    docsIndex = await indexResponse.json();
    docsGraph = await graphResponse.json();
    publicContent = await publicContentResponse.json();
    if (isDeveloper() && candidateResponse?.ok) registrationCandidates = await candidateResponse.json();
    else registrationCandidates = null;
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

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
import {
  collapseDocumentsForLanguage,
  collapseSearchResultsForLanguage,
  documentLanguage,
  preferredDocumentForLanguage,
  preferredPathForLanguage,
  presentationKeyForDocument,
} from "./language-core.js";

import {
  publicDocumentTitle, publicLinkLabel, readerText, sectionSlug,
  fragmentFromLink, sourceHeaderLines, documentForEditorialId, documentKey,
  readingChannelEntries, readingChannels, sameEditorialSelection, type ReadingTextKey,
} from "./reader-core.js";

const PUBLIC_CATALOG_URL = "../tools/docs_public_catalog.json";
const PUBLIC_GRAPH_URL = "../tools/docs_public_graph.json";
const DEVELOPER_GRAPH_URL = "../tools/docs_graph.json";
const REGISTRATION_WORKBENCH_URL = "../tools/docs_registration_workbench.preview.json";
const ASSESSMENT_PROTOCOLS_URL = "../tools/assessment/repository_assessment_protocols.preview.json";
const ASSESSMENT_RUNNER_STATUS_URL = "../api/assessment/runner";
const ASSESSMENT_RUN_URL = "../api/assessment/run";
const PUBLIC_CONTENT_URL = "./public-content.json";
const MAX_MAP_EDGES = 24;

const interfaceMode: "public" | "developer" = document.body.dataset.interface === "developer" ? "developer" : "public";

let docsIndex: JsonObject;
let docsGraph: JsonObject;
let publicContent: JsonObject = {};
let registrationWorkbench: JsonObject | null = null;
let assessmentProtocols: JsonObject | null = null;
let assessmentRunnerStatus: JsonObject | null = null;
let assessmentLabState: JsonObject = { run: null, source_run_sha256: "", decisions: {} };
let assessmentSelectedProtocolKey = "";
let assessmentTargetPaths: string[] = [];
let editorialState: JsonObject = { before: [], after: [] };
let editorialMessage = "";
let displayLang: "ja" | "en" = "ja";

const app = document.querySelector<HTMLElement>("#app")!;
const status = document.querySelector<HTMLElement>("#data-status")!;
const langButton = document.querySelector<HTMLButtonElement>("#lang-toggle")!;
const headerMenuButton = document.querySelector<HTMLButtonElement>("#header-menu")!;
const headerBackButton = document.querySelector<HTMLButtonElement>("#header-back")!;
const headerTopButton = document.querySelector<HTMLButtonElement>("#header-top")!;
const headerBottomButton = document.querySelector<HTMLButtonElement>("#header-bottom")!;

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
  if (node.type === "document" || node.type === "observed_document") {
    const doc = docByPath(String(node.path ?? ""));
    if (doc) return titleForDoc(preferredDoc(doc));
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
  if (!isDeveloper() && !params.has("lang")) params.set("lang", displayLang);
  location.hash = params.toString();
}

function route(): URLSearchParams {
  return new URLSearchParams(location.hash.replace(/^#/, ""));
}

function updateHeaderControls(): void {
  if (!isDeveloper()) {
    const brand = document.querySelector<HTMLAnchorElement>(".brand");
    const name = brand?.querySelector("strong");
    const subtitle = brand?.querySelector("small");
    if (name) name.textContent = readingText("brand");
    if (subtitle) subtitle.textContent = readingText("subtitle");
    brand?.setAttribute("aria-label", readingText("homeLabel"));
    const footer = document.querySelector(".public-site-footer p");
    if (footer) footer.textContent = readingText("footer");
  }
  langButton.setAttribute("aria-label", displayLang === "ja" ? "Switch to English" : "Switch to Japanese");
  headerMenuButton.textContent = displayLang === "ja" ? "メニュー" : "Menu";
  headerBackButton.textContent = displayLang === "ja" ? "← 戻る" : "← Back";
  headerTopButton.textContent = displayLang === "ja" ? "↑ 上" : "↑ Top";
  headerBottomButton.textContent = displayLang === "ja" ? "↓ 下" : "↓ Bottom";
  headerMenuButton.setAttribute("aria-label", displayLang === "ja" ? "トップメニューへ" : "Go to top menu");
  headerBackButton.setAttribute("aria-label", displayLang === "ja" ? "前の画面へ戻る" : "Go back");
  headerTopButton.setAttribute("aria-label", displayLang === "ja" ? "ページの一番上へ" : "Scroll to top");
  headerBottomButton.setAttribute("aria-label", displayLang === "ja" ? "ページの一番下へ" : "Scroll to bottom");
}

function setLanguage(lang: "ja" | "en"): void {
  displayLang = lang;
  langButton.textContent = lang === "ja" ? "EN" : "日本語";
  document.documentElement.lang = lang;
  updateHeaderControls();

  if (!isDeveloper() && docsIndex && docsGraph) {
    const params = route();
    let changed = false;
    if (params.has("lang")) { params.set("lang", lang); changed = true; }
    const readPath = params.get("read");
    if (readPath) {
      const target = preferredPathForLanguage(readPath, allDocuments(), lang);
      if (target && target !== readPath) {
        params.set("read", target);
        // JA/EN section identities are not assumed to correspond.
        if (params.has("section")) {
          params.delete("section");
          params.set("editionChanged", "1");
        }
        changed = true;
      }
    }
    const graphId = params.get("graph");
    if (graphId) {
      const target = preferredGraphNodeId(graphId);
      if (target && target !== graphId) {
        params.set("graph", target);
        changed = true;
      }
    }
    if (changed) history.replaceState(null, "", `#${params.toString()}`);
  }

  try { localStorage.setItem("scientific-ontology-reader-language:v1", lang); } catch { /* Reading works without storage. */ }
  render();
}

function eyebrow(text: string): HTMLElement {
  return el("div", "eyebrow", text);
}

function badge(text: string, tone = ""): HTMLElement {
  return el("span", `badge ${tone}`.trim(), text);
}

function readingText(key: ReadingTextKey): string { return readerText(displayLang, key); }

function titleForDoc(doc: JsonObject): string {
  return isDeveloper() ? localized(doc.title, String(doc.id ?? doc.doc_id ?? "")) : publicDocumentTitle(doc, displayLang);
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

function allDocuments(): JsonObject[] {
  return docsIndex.documents ?? [];
}

function preferredDoc(doc: JsonObject): JsonObject {
  return isDeveloper() ? doc : preferredDocumentForLanguage(doc, allDocuments(), displayLang);
}

function preferredPath(path: string): string {
  return isDeveloper() ? path : preferredPathForLanguage(path, allDocuments(), displayLang);
}

function preferredGraphNode(node: JsonObject): JsonObject {
  if (isDeveloper() || (node.type !== "document" && node.type !== "observed_document")) return node;
  const path = String(node.path ?? "");
  const doc = docByPath(path);
  if (!doc) return node;
  const target = preferredDoc(doc);
  return graphNodeByPath(String(target.path ?? "")) ?? node;
}

function preferredGraphNodeId(nodeId: string): string {
  if (isDeveloper()) return nodeId;
  const node = graphNodeMap(docsGraph).get(nodeId);
  return node ? String(preferredGraphNode(node).id ?? nodeId) : nodeId;
}

function graphNodeByPath(path: string): JsonObject | undefined {
  return (docsGraph.nodes ?? []).find(
    (node: JsonObject) => (node.type === "document" || node.type === "observed_document") && String(node.path ?? "") === path,
  );
}

function candidatePayload(): JsonObject | null {
  return registrationWorkbench?.registration_workbench ?? null;
}

function candidateList(): JsonObject[] {
  return candidatePayload()?.provisional_documents ?? [];
}

function candidateByPath(path: string): JsonObject | undefined {
  return candidateList().find((candidate: JsonObject) => String(candidate.path ?? "") === path);
}

function registeredDocumentList(): JsonObject[] {
  return candidatePayload()?.registered_documents ?? [];
}

function registeredDocumentByPath(path: string): JsonObject | undefined {
  return registeredDocumentList().find((item: JsonObject) => String(item.path ?? "") === path);
}

function registeredReviewList(): JsonObject[] {
  return candidatePayload()?.revision_proposals ?? [];
}

function registeredReviewByPath(path: string): JsonObject | undefined {
  return registeredReviewList().find((item: JsonObject) => String(item.path ?? "") === path);
}

function registrationStateForDoc(doc: JsonObject): string {
  return String(doc.registration_state ?? doc.publication?.registration_state ?? "registered");
}

function isProvisionalDoc(doc: JsonObject): boolean {
  return registrationStateForDoc(doc) === "provisional";
}

function languageFallbackLabel(doc: JsonObject): string {
  if (isDeveloper()) return "";
  const language = documentLanguage(doc);
  if (language !== "ja" && language !== "en") return "";
  if (language === displayLang) return "";
  if (doc.presentation?.counterpart_path) return "";
  return language === "ja" ? (displayLang === "ja" ? "日本語のみ" : "JA only") : (displayLang === "ja" ? "ENのみ" : "EN only");
}

function candidateTitle(candidate: JsonObject): string {
  const baseline = candidate.baseline ?? {};
  const preferred = displayLang === "ja" ? baseline.title_ja : baseline.title_en;
  const fallback = displayLang === "ja" ? baseline.title_en : baseline.title_ja;
  return String(preferred || fallback || baseline.doc_id || candidate.path || "");
}

function candidateRole(candidate: JsonObject): string {
  const baseline = candidate.baseline ?? {};
  return String((displayLang === "ja" ? baseline.role_ja : baseline.role_en) || baseline.role_ja || baseline.role_en || "");
}

function candidateQuestionList(candidate: JsonObject): string[] {
  const questions = candidate.baseline?.discovery?.reader_questions ?? {};
  return (questions[displayLang] ?? questions.ja ?? questions.en ?? []).map((value: any) => String(value));
}

function candidateAliases(candidate: JsonObject): string[] {
  const aliases = candidate.baseline?.discovery?.aliases ?? {};
  return (aliases[displayLang] ?? aliases.ja ?? aliases.en ?? []).map((value: any) => String(value));
}

function candidateSearchText(candidate: JsonObject): string {
  const baseline = candidate.baseline ?? {};
  const discovery = baseline.discovery ?? {};
  const values = [
    candidate.path,
    baseline.doc_id,
    baseline.title_ja,
    baseline.title_en,
    baseline.layer,
    baseline.status,
    baseline.scope,
    baseline.role_ja,
    baseline.role_en,
    discovery.visibility,
    ...(discovery.topics ?? []),
    ...(discovery.aliases?.ja ?? []),
    ...(discovery.aliases?.en ?? []),
    ...(discovery.reader_questions?.ja ?? []),
    ...(discovery.reader_questions?.en ?? []),
  ];
  return values.filter(Boolean).join(" ").normalize("NFKC").toLocaleLowerCase("ja-JP");
}

function readerButton(path: string, className = "text-button"): HTMLButtonElement {
  const read = button(displayLang === "ja" ? "読む" : "Read", className);
  read.addEventListener("click", () => setRoute({ read: preferredPath(path) }));
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
  doc = preferredDoc(doc);
  const direct = `doc:${doc.id}`;
  if (graphNodeMap(docsGraph).has(direct)) return direct;
  const byPath = (docsGraph.nodes ?? []).find(
    (node: JsonObject) => (node.type === "document" || node.type === "observed_document") && node.path === doc.path,
  );
  return byPath?.id;
}

function navBar(active: string): HTMLElement {
  const nav = el("nav", "view-tabs");
  const items: Array<[string, string, Record<string, string>]> = isDeveloper()
    ? [
        ["home", displayLang === "ja" ? "読む" : "Read", {}],
        ["reading-editor", readingText("editorialEditor"), { view: "reading-editor" }],
        ["search", displayLang === "ja" ? "検索" : "Search", { view: "search" }],
        ["relations", displayLang === "ja" ? "関係マップ" : "Relations", { view: "relations" }],
        ["candidates", displayLang === "ja" ? "候補レビュー" : "Candidate review", { view: "candidates" }],
        ["assessment", displayLang === "ja" ? "主張監査ラボ" : "Claim audit lab", { view: "assessment" }],
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
  if (!isDeveloper()) return el("div", "public-profile-spacer");

  const wrap = el("div", "data-banner");
  wrap.append(badge(profile === "preview" ? "PREVIEW" : profile.toUpperCase(), profile === "preview" ? "warn" : ""));
  wrap.append(
    el(
      "span",
      "data-banner-text",
      displayLang === "ja"
        ? "Public catalog とcanonical関係グラフをDeveloper監査面で読み込んでいます。整合性はDN-6 release gateで検証します。"
        : "Developer audit mode is using the Public catalog and canonical relation graph. DN-6 release gate verifies their consistency.",
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
  input.setAttribute("aria-label", input.placeholder);
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

function publicReadingChannelSection(channel: JsonObject): HTMLElement | null {
  if (channel.enabled === false) return null;
  const entries = readingChannelEntries(channel, allDocuments(), displayLang);
  if (!entries.length) return null;
  const id = String(channel.id ?? "reading");
  const section = el("section", `section reading-channel reading-channel-${id}`);
  const eyebrowText = localized(channel.eyebrow, id.toUpperCase());
  const title = localized(channel.title, id);
  const description = localized(channel.description, "");
  if (eyebrowText) section.append(eyebrow(eyebrowText));
  if (title) section.append(el("h2", "section-title", title));
  if (description) section.append(el("p", "section-copy", description));
  const grid = el("div", `reading-channel-grid ${String(channel.layout ?? "cards") === "lead" ? "reading-channel-lead" : ""}`);
  for (const { document: doc } of entries) {
    const card = el("article", "reading-channel-card");
    card.append(el("h3", "reading-channel-title", titleForDoc(doc)));
    const actions = el("div", "card-actions");
    const read = readerButton(String(doc.path), "button primary compact-button");
    read.textContent = readingText("read");
    actions.append(read);
    card.append(actions);
    grid.append(card);
  }
  section.append(grid);
  return section;
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
  page.append(hero);
  for (const channel of readingChannels(publicContent)) {
    const section = publicReadingChannelSection(channel);
    if (section) page.append(section);
  }
  page.append(quick);

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
  if (isDeveloper() && level) top.append(badge(level));
  if (isDeveloper() && isProvisionalDoc(doc)) top.append(badge(displayLang === "ja" ? "仮登録" : "Provisional", "warn"));
  const languageFallback = languageFallbackLabel(doc);
  if (languageFallback) top.append(badge(languageFallback, "warn"));
  if (isDeveloper() && state) top.append(badge(state, state === "public-candidate" ? "warn" : ""));
  if (top.childElementCount) item.append(top);
  item.append(el("h3", "card-title", titleForDoc(doc)));
  const role = roleForDoc(doc);
  if (isDeveloper() && role) item.append(el("p", "card-copy", role));
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
  const topicDocs: JsonObject[] = isDeveloper()
    ? (payload.documents ?? [])
    : collapseDocumentsForLanguage(payload.documents ?? [], allDocuments(), displayLang);
  for (const doc of topicDocs) {
    const level = String(doc.entry_level ?? doc.discovery?.entry_level ?? "");
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

function publicDocsForLayer(layerPath: string): JsonObject[] {
  const normalized = layerPath.replace(/\\/g, "/").replace(/\/$/, "");
  const matched = (docsIndex.documents ?? [])
    .filter((doc: JsonObject) => {
      const path = String(doc.path ?? "");
      if (normalized === ".") return !path.includes("/");
      return path === normalized || path.startsWith(`${normalized}/`);
    });
  return collapseDocumentsForLanguage(matched, allDocuments(), displayLang)
    .slice()
    .sort((a: JsonObject, b: JsonObject) => {
      const levelOrder: Record<string, number> = { foundation: 0, intermediate: 1, advanced: 2, "": 3 };
      const aLevel = levelOrder[String(a.discovery?.entry_level ?? "")] ?? 3;
      const bLevel = levelOrder[String(b.discovery?.entry_level ?? "")] ?? 3;
      if (aLevel !== bLevel) return aLevel - bLevel;
      return titleForDoc(a).localeCompare(titleForDoc(b), displayLang === "ja" ? "ja" : "en");
    });
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

  const layerDocs = publicDocsForLayer(String(layer.path ?? ""));
  if (layerDocs.length) {
    const section = el("section", "section public-section");
    section.append(
      eyebrow(displayLang === "ja" ? "DOCUMENTS" : "DOCUMENTS"),
      el("h2", "section-title", displayLang === "ja" ? "この層で読む" : "Read in this layer"),
      el("p", "section-copy", displayLang === "ja" ? `${layerDocs.length} 件の文書から選べます。` : `Choose from ${layerDocs.length} documents.`),
    );
    const grid = el("div", "doc-grid");
    for (const doc of layerDocs) grid.append(docCard(doc));
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
  for (const doc of layerDocs) {
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
      if (candidate) main.append(badge(displayLang === "ja" ? "仮登録レビューあり" : "Provisional review available", "warn"));
      const read = readerButton(path);
      const relation = button(displayLang === "ja" ? "関係を見る" : "Relations", "text-button");
      relation.addEventListener("click", () => setRoute({ graph: String(node.id) }));
      row.append(main, read, relation);
      if (candidate) {
        const inspectCandidate = button(displayLang === "ja" ? "仮登録レビュー" : "Provisional review", "text-button");
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
  let rawFound = searchDocuments(query, docsIndex, "auto", isDeveloper() ? 12 : 32, isDeveloper() ? "both" : displayLang);
  if (!isDeveloper() && !rawFound.results.length) rawFound = searchDocuments(query, docsIndex, "auto", 32, "both");
  const found = isDeveloper()
    ? rawFound
    : { ...rawFound, results: collapseSearchResultsForLanguage(rawFound.results, allDocuments(), displayLang, 12) };
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
    const headingMeta = el("div", "result-heading-meta");
    if (isDeveloper() && isProvisionalDoc(result)) headingMeta.append(badge(displayLang === "ja" ? "仮登録" : "Provisional", "warn"));
    const languageFallback = languageFallbackLabel(result);
    if (languageFallback) headingMeta.append(badge(languageFallback, "warn"));
    headingMeta.append(badge(result.score.toFixed(2), "score"));
    heading.append(el("h2", "card-title", titleForDoc(result)), headingMeta);
    card.append(heading);
    const role = roleForDoc(result);
    if (isDeveloper() && role) card.append(el("p", "card-copy", role));

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
  const revision = button(displayLang === "ja" ? "改訂候補にする" : "Request revision", "button secondary");
  revision.addEventListener("click", () => addRevisionCandidate(doc));
  headerActions.append(revision);
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
          const section = fragmentFromLink(href);
          a.href = `#${new URLSearchParams({ read: sourcePath, section, lang: displayLang }).toString()}`;
          a.addEventListener("click", (event) => {
            if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
            event.preventDefault();
            scrollToReaderSection(parent.closest(".reader-article"), section, sourcePath);
          });
        } else if (/^(https?:|mailto:)/i.test(href)) {
          a.href = href;
          a.target = "_blank";
          a.rel = "noopener noreferrer";
        } else {
          const resolved = normalizeRepoPath(sourcePath, href);
          if (resolved?.endsWith(".md") && readerAllowedPaths().has(resolved)) {
            const target = preferredPath(resolved);
            const targetDoc = docByPath(target);
            if (!isDeveloper() && targetDoc) a.textContent = publicLinkLabel(label, targetDoc, displayLang);
            // Keep a fragment only within the same edition, never translate anchors by guesswork.
            const section = target === resolved ? fragmentFromLink(href) : "";
            a.href = `#${new URLSearchParams({ read: target, lang: displayLang, ...(section ? { section } : {}) }).toString()}`;
            a.addEventListener("click", (event) => {
              if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
              event.preventDefault();
              if (target === sourcePath && section) scrollToReaderSection(parent.closest(".reader-article"), section, sourcePath);
              else setRoute({ read: target, section });
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
  const base = sectionSlug(text);
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
      quote.dataset.sourceHeader = sourceHeaderLines(quoteLines.join("\n")) ? "true" : "false";
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
    paragraph.dataset.sourceHeader = sourceHeaderLines(paragraphLines.join("\n")) ? "true" : "false";
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
  const root = nodeMap.get(rootId);
  const rootDoc = root ? docByPath(String(root.path ?? "")) : undefined;
  if (rootDoc) seen.add(presentationKeyForDocument(rootDoc));
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
    const projectedNode = preferredGraphNode(node);
    const path = String(projectedNode.path ?? "");
    if (!path || !readerAllowedPaths().has(path)) continue;
    const projectedDoc = docByPath(path);
    const dedupeKey = projectedDoc ? presentationKeyForDocument(projectedDoc) : String(projectedNode.id ?? otherId);
    if (seen.has(dedupeKey)) continue;
    seen.add(dedupeKey);
    rows.push({ node: projectedNode, relation: String(edge.relation), direction: outgoing ? "outgoing" : "incoming" });
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
      readingText("relatedIntro"),
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

const READING_SIZE_KEY = "scientific-ontology-reader-size:v1";
const READING_THEME_KEY = "scientific-ontology-reader-theme:v1";
let readingSize = "standard";
let readingTheme = "system";
try {
  const savedSize = localStorage.getItem(READING_SIZE_KEY);
  if (savedSize && ["standard", "large", "larger"].includes(savedSize)) readingSize = savedSize;
  const savedTheme = localStorage.getItem(READING_THEME_KEY);
  if (savedTheme && ["system", "light", "dark", "paper"].includes(savedTheme)) readingTheme = savedTheme;
} catch { /* Storage is optional. */ }

function scrollToReaderSection(article: Element | null, section: string, path: string, updateUrl = true): boolean {
  if (!article || !section) return false;
  const headings = Array.from(article.querySelectorAll<HTMLElement>(".reader-h"));
  const target = headings.find((h) => h.id === section)
    ?? headings.find((h) => sectionSlug(h.textContent ?? "") === sectionSlug(section));
  if (!target) return false;
  if (updateUrl) {
    const params = new URLSearchParams({ read: path, section: target.id, lang: displayLang });
    history.replaceState(null, "", `#${params.toString()}`);
  }
  target.tabIndex = -1;
  target.focus({ preventScroll: true });
  target.scrollIntoView({ block: "start", behavior: "instant" });
  return true;
}

function readerContents(article: HTMLElement, path: string): HTMLElement | null {
  const headings = Array.from(article.querySelectorAll<HTMLElement>("h2, h3"));
  if (!headings.length) return null;
  const details = el("details", "reader-toc reader-toolbar-popover");
  details.append(el("summary", "reader-toc-title reader-toolbar-button", readingText("toc")));
  const nav = el("nav", "reader-toc-links");
  nav.setAttribute("aria-label", readingText("toc"));
  for (const heading of headings) {
    const link = el("a", heading.tagName === "H3" ? "reader-toc-child" : "", heading.textContent ?? "");
    link.href = `#${new URLSearchParams({ read: path, section: heading.id, lang: displayLang }).toString()}`;
    link.addEventListener("click", (event) => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      details.open = false;
      scrollToReaderSection(article, heading.id, path);
    });
    nav.append(link);
  }
  details.append(nav);
  return details;
}

function normalizeVisibleHeading(value: string): string {
  return value.normalize("NFKC").replace(/\s+/g, " ").trim().toLocaleLowerCase("ja-JP");
}

function removePublicSourceHeader(article: HTMLElement): void {
  // Public reading starts with the prose, not repository metadata. Developer mode
  // keeps source bytes untouched and visible through its own Reader.
  for (const child of Array.from(article.children).slice(0, 10)) {
    if (/^H[12]$/.test(child.tagName) || child.tagName === "HR") continue;
    if (child instanceof HTMLElement && child.dataset.sourceHeader === "true") {
      child.remove();
      continue;
    }
    break;
  }
}

function removeDuplicateReaderTitle(article: HTMLElement, _visibleTitle: string): void {
  // Public Reader already owns the localized display title. The first source H1
  // is the document title even when a single-language body is shown under the
  // other UI language, so repeating it interrupts reading.
  article.querySelector<HTMLElement>(":scope > h1")?.remove();
}

function readingPreferences(shell: HTMLElement): HTMLElement {
  const details = el("details", "reader-preferences reader-toolbar-popover");
  details.append(el("summary", "reader-toolbar-button", "Aa"));
  const panel = el("div", "reader-preferences-panel");
  const state = el("span", "reader-tool-state");
  state.setAttribute("role", "status");

  const sizeLabel = el("label", "reader-preference-field");
  sizeLabel.append(el("span", "", readingText("textSize")));
  const sizeSelect = el("select", "reader-size-select");
  sizeSelect.setAttribute("aria-label", readingText("textSize"));
  for (const value of ["standard", "large", "larger"] as const) {
    const option = el("option", "", readingText(value));
    option.value = value;
    sizeSelect.append(option);
  }
  sizeSelect.value = readingSize;
  sizeLabel.append(sizeSelect);

  const themeLabel = el("label", "reader-preference-field");
  themeLabel.append(el("span", "", readingText("theme")));
  const themeSelect = el("select", "reader-theme-select");
  themeSelect.setAttribute("aria-label", readingText("theme"));
  for (const [value, key] of [["system", "themeSystem"], ["light", "themeLight"], ["dark", "themeDark"], ["paper", "themePaper"]] as const) {
    const option = el("option", "", readingText(key));
    option.value = value;
    themeSelect.append(option);
  }
  themeSelect.value = readingTheme;
  themeLabel.append(themeSelect);

  shell.dataset.textSize = readingSize;
  shell.dataset.readingTheme = readingTheme;
  sizeSelect.addEventListener("change", () => {
    readingSize = sizeSelect.value;
    shell.dataset.textSize = readingSize;
    state.textContent = "";
    try { localStorage.setItem(READING_SIZE_KEY, readingSize); }
    catch { state.textContent = readingText("settingsNotSaved"); }
  });
  themeSelect.addEventListener("change", () => {
    readingTheme = themeSelect.value;
    shell.dataset.readingTheme = readingTheme;
    state.textContent = "";
    try { localStorage.setItem(READING_THEME_KEY, readingTheme); }
    catch { state.textContent = readingText("settingsNotSaved"); }
  });
  panel.append(sizeLabel, themeLabel, el("p", "reader-selection-hint", readingText("selectionHint")), state);
  details.append(panel);
  return details;
}

function selectionSearchTools(article: HTMLElement): HTMLElement {
  const tools = el("div", "reader-selection-tools");
  tools.hidden = true;
  const quote = el("span", "reader-selection-text");
  const search = button(readingText("selectedSearchShort"), "button primary compact-button");
  const close = button(readingText("selectedDismiss"), "button ghost compact-button");
  let selectedText = "";
  const hide = () => { tools.hidden = true; selectedText = ""; };
  const refresh = () => {
    const selection = window.getSelection();
    const anchor = selection?.anchorNode;
    const focus = selection?.focusNode;
    if (!selection || !anchor || !focus || !article.contains(anchor) || !article.contains(focus)) { hide(); return; }
    const text = selection.toString().replace(/\s+/g, " ").trim();
    if (text.length < 2 || text.length > 240) { hide(); return; }
    selectedText = text;
    quote.textContent = text.length > 72 ? `“${text.slice(0, 72)}…”` : `“${text}”`;
    tools.hidden = false;
  };
  article.addEventListener("mouseup", () => setTimeout(refresh, 0));
  article.addEventListener("keyup", () => setTimeout(refresh, 0));
  search.addEventListener("click", () => { if (selectedText) setRoute({ view: "search", q: selectedText }); });
  close.addEventListener("click", hide);
  tools.append(quote, search, close);
  return tools;
}

function prepareReaderPresentation(shell: HTMLElement, article: HTMLElement, path: string, visibleTitle: string): HTMLElement[] {
  removePublicSourceHeader(article);
  removeDuplicateReaderTitle(article, visibleTitle);
  const toolbar = el("div", "reader-toolbar");
  const contents = readerContents(article, path);
  if (contents) toolbar.append(contents);
  toolbar.append(readingPreferences(shell));
  const share = button(readingText("copyLink"), "reader-toolbar-button");
  const state = el("span", "reader-tool-state");
  state.setAttribute("role", "status");
  share.addEventListener("click", () => {
    const link = new URL(location.href);
    link.hash = new URLSearchParams({ read: path, lang: displayLang }).toString();
    if (!navigator.clipboard?.writeText) { state.textContent = readingText("copyFailed"); return; }
    void navigator.clipboard.writeText(link.href)
      .then(() => { state.textContent = readingText("copied"); })
      .catch(() => { state.textContent = readingText("copyFailed"); });
  });
  toolbar.append(share, state);
  return [toolbar, article, selectionSearchTools(article)];
}

function renderReader(path: string): HTMLElement {
  path = preferredPath(path);
  const page = el("main", `page reader-page ${isDeveloper() ? "developer-reader" : "public-reader"}`);
  page.append(navBar(isDeveloper() ? "reader" : "home"), dataBanner());
  const back = button(displayLang === "ja" ? "← 戻る" : "← Back", "back-button");
  back.addEventListener("click", () => history.length > 1 ? history.back() : setRoute({}));
  page.append(back);

  if (!readerAllowedPaths().has(path)) {
    page.append(el("p", "error", !isDeveloper() ? readingText("unavailable") : displayLang === "ja" ? `Reader対象外のパスです: ${path}` : `Path is outside the Reader boundary: ${path}`));
    return page;
  }

  const doc = docByPath(path);
  const graphNode = graphNodeByPath(path);
  const title = doc ? titleForDoc(doc) : graphNode ? displayGraphNodeLabel(graphNode) : isDeveloper() ? path : readingText("document");
  document.title = `${title} | ${isDeveloper() ? "Developer Navigator" : readingText("brand")}`;
  const header = el("section", "reader-header");
  const decodeState = badge(displayLang === "ja" ? "UTF-8 strict 読込中" : "UTF-8 strict loading", "warn");
  decodeState.id = "reader-decode-state";
  if (isDeveloper()) {
    header.append(eyebrow("READER · UTF-8 STRICT"), el("h1", "hero-title", title), el("div", "path", path), decodeState);
  } else {
    header.append(el("h1", "reader-public-title", title));
    if (doc) {
      const languageFallback = languageFallbackLabel(doc);
      if (languageFallback) {
        const languageLine = el("div", "reader-language-fallback");
        languageLine.append(
          badge(languageFallback, "warn"),
          el("span", "muted", displayLang === "ja" ? "このUI言語に対応する本文がないため、利用可能な言語版を表示しています。" : "No body exists in the selected UI language, so the available edition is shown."),
        );
        header.append(languageLine);
      }
    }
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
      const inspectCandidate = button(displayLang === "ja" ? "仮登録レビュー" : "Provisional review", "button secondary");
      inspectCandidate.addEventListener("click", () => setRoute({ view: "candidates", candidate: path }));
      actions.append(inspectCandidate);
    }
    actions.append(rawFileLink(path, "button ghost"));
  } else {
    const more = el("details", "reader-more");
    more.append(el("summary", "reader-more-summary", "…"));
    const source = rawFileLink(path, "text-link reader-source-link");
    more.append(source);
    actions.append(more);
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
      if (!page.isConnected) return;
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
        const article = renderMarkdown(text, path);
        const sourceLanguage = doc ? documentLanguage(doc) : "und";
        if (sourceLanguage === "ja" || sourceLanguage === "en") article.lang = sourceLanguage;
        shell.replaceChildren(...prepareReaderPresentation(shell, article, path, title));
        const params = route();
        const section = params.get("section") ?? "";
        if (section && !scrollToReaderSection(article, section, path, false)) {
          shell.prepend(el("p", "reader-anchor-note", readingText("chapterNotFound")));
        }
        if (params.get("editionChanged")) shell.prepend(el("p", "reader-anchor-note", readingText("sectionAfterLanguage")));
        if (graphNode) {
          const related = publicReaderRelatedSection(graphNode);
          if (related) page.append(related);
        }
      }
    })
    .catch((error) => {
      decodeState.textContent = "UTF-8 strict FAIL";
      decodeState.className = "badge danger";
      if (!page.isConnected) return;
      shell.replaceChildren(el("p", "error", isDeveloper() ? String((error as Error).message) : readingText("loadFailed")));
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
  full.addEventListener("click", () => setRoute({ graph: preferredGraphNodeId(rootId) }));
  section.append(full);
  return section;
}

function relationMap(rootId: string): HTMLElement {
  rootId = preferredGraphNodeId(rootId);
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
  if (!isDeveloper()) {
    const seen = new Set<string>();
    edges = edges.flatMap((edge: JsonObject) => {
      const outgoing = edge.from === rootId;
      const otherId = String(outgoing ? edge.to : edge.from);
      const other = nodeMap.get(otherId) ?? graphNodeMap(docsGraph).get(otherId);
      if (!other) return [];
      const projected = preferredGraphNode(other);
      let logicalKey = String(projected.id ?? otherId);
      if (projected.type === "document" || projected.type === "observed_document") {
        const projectedDoc = docByPath(String(projected.path ?? ""));
        if (projectedDoc) logicalKey = presentationKeyForDocument(projectedDoc);
      }
      const key = `${outgoing ? "out" : "in"}|${String(edge.relation)}|${logicalKey}`;
      if (seen.has(key)) return [];
      seen.add(key);
      return [{ ...edge, display_other_id: String(projected.id ?? otherId) }];
    });
  }
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
    const nodeId = String(edge.display_other_id ?? edge.from);
    const node = nodeMap.get(nodeId) ?? graphNodeMap(docsGraph).get(nodeId);
    if (!node) return;
    const y = 70 + index * 74;
    drawEdge(svg, 300, y, 420, center.y, String(edge.relation), "incoming");
    drawGraphNode(svg, node, 180, y, false);
  });
  outgoing.forEach((edge: JsonObject, index: number) => {
    const nodeId = String(edge.display_other_id ?? edge.to);
    const node = nodeMap.get(nodeId) ?? graphNodeMap(docsGraph).get(nodeId);
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
    const otherId = String(edge.display_other_id ?? (outgoingEdge ? edge.to : edge.from));
    const other = nodeMap.get(otherId) ?? graphNodeMap(docsGraph).get(otherId);
    if (!other) continue;
    const row = el("button", "relation-row") as HTMLButtonElement;
    row.type = "button";
    row.addEventListener("click", () => setRoute({ graph: preferredGraphNodeId(otherId) }));
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
    const activate = () => setRoute({ graph: preferredGraphNodeId(String(node.id)) });
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
  if (!isDeveloper() && nodeQuery) {
    try {
      const node = graphNodeMap(docsGraph).get(preferredGraphNodeId(resolveGraphNode(docsGraph, nodeQuery)));
      if (node) input.value = displayGraphNodeLabel(node);
    } catch { input.value = ""; }
  }
  input.setAttribute("aria-label", input.placeholder);
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
      alert(isDeveloper() ? String((error as Error).message) : readingText("graphNotFound"));
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
      const rootId = preferredGraphNodeId(resolveGraphNode(docsGraph, nodeQuery));
      const root = graphNodeMap(docsGraph).get(rootId)!;
      const current = el("div", "graph-current");
      current.append(
        el("h2", "section-title small", displayGraphNodeLabel(root)),
        badge(isDeveloper() ? String(root.type) : nodeTypeLabel(String(root.type))),
      );
      const rootPath = String(root.path ?? "");
      const rootDoc = rootPath ? docByPath(rootPath) : undefined;
      if (isDeveloper() && rootDoc && isProvisionalDoc(rootDoc)) current.append(badge(displayLang === "ja" ? "仮登録" : "Provisional", "warn"));
      if (isDeveloper()) current.append(el("div", "path", String(root.path ?? root.id)));
      if ((root.type === "document" || root.type === "observed_document") && readerAllowedPaths().has(rootPath)) {
        current.append(readerButton(rootPath, isDeveloper() ? "text-button" : "button quiet-button"));
      }
      section.append(current, relationMap(rootId));
    } catch (error) {
      section.append(el("p", "error", isDeveloper() ? String((error as Error).message) : readingText("graphNotFound")));
    }
  } else {
    const starters = el("div", "starter-node-grid public-relation-starters");
    const seeds = ["doc:scientific_ontology_concept_network", "doc:meaning_generation_model", "topic:ai", "layer:sat_truth"];
    for (const id of seeds) {
      const node = graphNodeMap(docsGraph).get(id);
      if (!node) continue;
      const b = button(displayGraphNodeLabel(node), "starter-node");
      b.addEventListener("click", () => setRoute({ graph: preferredGraphNodeId(id) }));
      starters.append(b);
    }
    section.append(el("h2", "minor-title", displayLang === "ja" ? "例から開く" : "Open an example"), starters);
  }
  page.append(section);
  return page;
}


const EDITORIAL_STORAGE_KEY = "scientific-ontology-reading-editor:v1";

function canonicalReadingChannels(): JsonObject[] {
  return deepClone(readingChannels(publicContent));
}

function loadEditorialState(): void {
  if (!isDeveloper()) return;
  const before = canonicalReadingChannels();
  editorialState = { before, after: deepClone(before) };
  try {
    const raw = localStorage.getItem(EDITORIAL_STORAGE_KEY);
    const parsed = raw ? JSON.parse(raw) : null;
    if (parsed && typeof parsed === "object" && sameEditorialSelection(parsed.before, before) && Array.isArray(parsed.after)) {
      editorialState = { before, after: deepClone(parsed.after) };
    }
  } catch { /* Browser-local editor state is optional. */ }
}

function saveEditorialState(): void {
  if (!isDeveloper()) return;
  try { localStorage.setItem(EDITORIAL_STORAGE_KEY, JSON.stringify(editorialState)); }
  catch { editorialMessage = displayLang === "ja" ? "ブラウザ内保存に失敗しました。JSON出力は利用できます。" : "Browser-local save failed. JSON export remains available."; }
}

function editorialChannels(): JsonObject[] {
  return Array.isArray(editorialState.after) ? editorialState.after : [];
}

function editorialChannelById(id: string): JsonObject | undefined {
  return editorialChannels().find((channel: JsonObject) => String(channel.id ?? "") === id);
}

function editorialDocumentLabel(doc: JsonObject): string {
  const primary = publicDocumentTitle(doc, displayLang);
  const otherLang = displayLang === "ja" ? "en" : "ja";
  const other = publicDocumentTitle(doc, otherLang);
  const type = String(doc.document_type ?? "document");
  return primary === other ? `${primary} · ${type}` : `${primary} / ${other} · ${type}`;
}

function editorialSelectionPayload(): JsonObject {
  return {
    navigator_editorial_selection: {
      schema_version: "0.1",
      target: "navigator/public-content.json",
      before: deepClone(editorialState.before ?? []),
      after: deepClone(editorialState.after ?? []),
    },
  };
}

function downloadEditorialSelection(): void {
  const blob = new Blob([JSON.stringify(editorialSelectionPayload(), null, 2) + "\n"], { type: "application/json;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = el("a");
  link.href = url;
  link.download = "navigator_editorial_selection.json";
  link.click();
  URL.revokeObjectURL(url);
}

async function importEditorialSelection(file: File): Promise<void> {
  const parsed = JSON.parse(await file.text());
  const payload = parsed?.navigator_editorial_selection;
  if (!payload || payload.schema_version !== "0.1" || !Array.isArray(payload.before) || !Array.isArray(payload.after)) {
    throw new Error(displayLang === "ja" ? "navigator_editorial_selection/0.1 ではありません。" : "Expected navigator_editorial_selection/0.1.");
  }
  const current = canonicalReadingChannels();
  if (!sameEditorialSelection(payload.before, current)) {
    throw new Error(displayLang === "ja" ? "公開設定が出力時点から変わっています。現在設定から選び直してください。" : "The published reading configuration changed after this export. Rebase the selection on the current configuration.");
  }
  editorialState = { before: current, after: deepClone(payload.after) };
  editorialMessage = displayLang === "ja" ? "JSONを読み込みました。まだRepositoryへは適用していません。" : "Selection JSON imported. The repository has not been changed.";
  saveEditorialState();
  render();
}

function familyAlreadySelected(channel: JsonObject, candidate: JsonObject): boolean {
  const family = presentationKeyForDocument(candidate);
  return (channel.documents ?? []).some((id: unknown) => {
    const existing = documentForEditorialId(allDocuments(), String(id ?? ""));
    return existing ? presentationKeyForDocument(existing) === family : false;
  });
}

function moveEditorialDocument(channel: JsonObject, index: number, delta: number): void {
  const docs = [...(channel.documents ?? [])];
  const target = index + delta;
  if (target < 0 || target >= docs.length) return;
  [docs[index], docs[target]] = [docs[target], docs[index]];
  channel.documents = docs;
  saveEditorialState();
  render();
}

function editorialChannelEditor(channel: JsonObject): HTMLElement {
  const id = String(channel.id ?? "channel");
  const card = el("section", "editorial-channel-card");
  const head = el("div", "editorial-channel-head");
  const titleWrap = el("div");
  titleWrap.append(el("div", "eyebrow", localized(channel.eyebrow, id.toUpperCase())), el("h2", "section-title small", localized(channel.title, id)));
  const enabledLabel = el("label", "editorial-toggle");
  const enabled = el("input") as HTMLInputElement;
  enabled.type = "checkbox";
  enabled.checked = channel.enabled !== false;
  enabled.addEventListener("change", () => { channel.enabled = enabled.checked; saveEditorialState(); render(); });
  enabledLabel.append(enabled, el("span", "", displayLang === "ja" ? "公開する" : "Show publicly"));
  head.append(titleWrap, enabledLabel);
  card.append(head);
  const description = localized(channel.description, "");
  if (description) card.append(el("p", "section-copy", description));

  const selected = el("div", "editorial-selected-list");
  const ids = [...(channel.documents ?? [])].map((value: unknown) => String(value ?? "")).filter(Boolean);
  if (!ids.length) selected.append(el("p", "empty", displayLang === "ja" ? "まだ文書を選んでいません。" : "No document selected yet."));
  ids.forEach((documentId: string, index: number) => {
    const source = documentForEditorialId(allDocuments(), documentId);
    const row = el("article", "editorial-selected-row");
    const main = el("div", "editorial-selected-main");
    main.append(el("strong", "", source ? editorialDocumentLabel(source) : documentId));
    if (source) main.append(el("div", "path", String(source.path ?? "")));
    const actions = el("div", "editorial-row-actions");
    const up = button(readingText("editorialUp"), "button quiet-button compact-button");
    up.disabled = index === 0;
    up.addEventListener("click", () => moveEditorialDocument(channel, index, -1));
    const down = button(readingText("editorialDown"), "button quiet-button compact-button");
    down.disabled = index === ids.length - 1;
    down.addEventListener("click", () => moveEditorialDocument(channel, index, 1));
    const remove = button(readingText("editorialRemove"), "button ghost compact-button");
    remove.addEventListener("click", () => {
      channel.documents = ids.filter((_: string, i: number) => i !== index);
      saveEditorialState();
      render();
    });
    actions.append(up, down, remove);
    row.append(main, actions);
    selected.append(row);
  });
  card.append(selected);

  const chooser = el("div", "editorial-chooser");
  chooser.append(el("h3", "minor-title", readingText("editorialAllDocs")));
  const filter = el("input", "editorial-filter") as HTMLInputElement;
  filter.type = "search";
  filter.placeholder = displayLang === "ja" ? "タイトル・種類・パスで絞り込み" : "Filter by title, type, or path";
  filter.autocomplete = "off";
  const select = el("select", "editorial-doc-select") as HTMLSelectElement;
  select.size = 10;
  const renderOptions = () => {
    const q = filter.value.trim().normalize("NFKC").toLocaleLowerCase("ja-JP");
    select.replaceChildren();
    for (const doc of allDocuments()) {
      const haystack = `${editorialDocumentLabel(doc)} ${String(doc.path ?? "")}`.normalize("NFKC").toLocaleLowerCase("ja-JP");
      if (q && !haystack.includes(q)) continue;
      const option = el("option") as HTMLOptionElement;
      option.value = documentKey(doc);
      option.textContent = `${editorialDocumentLabel(doc)} · ${String(doc.path ?? "")}`;
      select.append(option);
    }
  };
  filter.addEventListener("input", renderOptions);
  renderOptions();
  const add = button(readingText("editorialAdd"), "button primary compact-button");
  add.addEventListener("click", () => {
    const source = documentForEditorialId(allDocuments(), select.value);
    if (!source) return;
    if (familyAlreadySelected(channel, source)) {
      editorialMessage = displayLang === "ja" ? "同じ日英文書ファミリーは同じ枠へ重複登録しません。" : "The same JA/EN document family is not duplicated within a channel.";
      render();
      return;
    }
    channel.documents = [...ids, documentKey(source)];
    editorialMessage = "";
    saveEditorialState();
    render();
  });
  chooser.append(filter, select, add);
  card.append(chooser);
  return card;
}

function editorialPublicPreview(): HTMLElement {
  const preview = el("section", "section editorial-public-preview");
  preview.append(
    eyebrow("PUBLIC PREVIEW"),
    el("h2", "section-title small", readingText("editorialPreview")),
    el("p", "section-copy", displayLang === "ja"
      ? "ブラウザ内の未適用選択を、Public側の表示言語解決に近い形で確認します。ここからRepositoryは変更しません。"
      : "Preview the unapplied browser-local selection with Public-style language resolution. This does not change the repository."),
  );
  let count = 0;
  for (const channel of editorialChannels()) {
    if (channel.enabled === false) continue;
    const entries = readingChannelEntries(channel, allDocuments(), displayLang);
    if (!entries.length) continue;
    count += entries.length;
    const block = el("div", "editorial-preview-channel");
    block.append(el("h3", "minor-title", localized(channel.title, String(channel.id ?? "reading"))));
    const grid = el("div", `reading-channel-grid ${String(channel.layout ?? "cards") === "lead" ? "reading-channel-lead" : ""}`);
    for (const { document: doc } of entries) {
      const card = el("article", "reading-channel-card");
      card.append(el("h4", "reading-channel-title", publicDocumentTitle(doc, displayLang)));
      const actions = el("div", "card-actions");
      const read = readerButton(String(doc.path), "button quiet-button compact-button");
      read.textContent = readingText("read");
      actions.append(read);
      card.append(actions);
      grid.append(card);
    }
    block.append(grid);
    preview.append(block);
  }
  if (!count) preview.append(el("p", "empty", displayLang === "ja" ? "まだ公開プレビューに出す文書を選んでいません。" : "No document is selected for the public preview yet."));
  return preview;
}

function renderReadingEditor(): HTMLElement {
  const page = el("main", "page editorial-page");
  page.append(navBar("reading-editor"), dataBanner());
  const section = el("section", "section");
  section.append(
    eyebrow("EDITORIAL READING SURFACE"),
    el("h1", "hero-title", displayLang === "ja" ? "トップとリコメンドを選ぶ" : "Choose top-page reading recommendations"),
    el("p", "hero-copy", displayLang === "ja"
      ? "READMEを含むPublic catalogの全文書から選択できます。ここでの選択は主張強度・重要度・人気を自動判定するものではありません。日英ペアはPublic側で表示言語に合わせて解決します。"
      : "Choose from every document in the Public catalog, including README files. Editorial selection is not an automatic claim-strength, importance, or popularity ranking. JA/EN counterparts resolve to the reader's UI language."),
    el("p", "reader-boundary-note", readingText("editorialSavedLocal")),
  );
  const actions = el("div", "reader-actions");
  const exportButton = button(readingText("editorialExport"), "button primary");
  exportButton.addEventListener("click", downloadEditorialSelection);
  const importLabel = el("label", "button secondary file-button", readingText("editorialImport"));
  const importInput = el("input") as HTMLInputElement;
  importInput.type = "file";
  importInput.accept = "application/json,.json";
  importInput.hidden = true;
  importInput.addEventListener("change", () => {
    const file = importInput.files?.[0];
    if (!file) return;
    void importEditorialSelection(file).catch((error) => { editorialMessage = String((error as Error).message); render(); });
  });
  importLabel.append(importInput);
  const reset = button(readingText("editorialReset"), "button quiet-button");
  reset.addEventListener("click", () => {
    const before = canonicalReadingChannels();
    editorialState = { before, after: deepClone(before) };
    editorialMessage = "";
    try { localStorage.removeItem(EDITORIAL_STORAGE_KEY); } catch { /* optional */ }
    render();
  });
  actions.append(exportButton, importLabel, reset);
  section.append(actions);
  if (editorialMessage) section.append(el("p", "editorial-message", editorialMessage));
  page.append(section);
  const grid = el("div", "editorial-channel-grid");
  for (const channel of editorialChannels()) grid.append(editorialChannelEditor(channel));
  page.append(grid, editorialPublicPreview());
  return page;
}

const REVIEW_STORAGE_PREFIX = "scientific-ontology-registration-review:";
let registrationReviewState: JsonObject = { decisions: {}, manual_candidates: [], revision_candidates: [] };

function deepClone<T>(value: T): T {
  return JSON.parse(JSON.stringify(value));
}

function reviewStorageKey(): string {
  const source = candidatePayload()?.source ?? {};
  const manifestHash = String(source.manifest_sha256 ?? "unbound");
  const revisionHash = String(source.revision_proposals_sha256 ?? "no-revision-proposals");
  return `${REVIEW_STORAGE_PREFIX}${manifestHash}:${revisionHash}`;
}

function loadRegistrationReviewState(): void {
  if (!isDeveloper() || !candidatePayload()) return;
  try {
    const raw = localStorage.getItem(reviewStorageKey());
    const parsed = raw ? JSON.parse(raw) : null;
    registrationReviewState = parsed && typeof parsed === "object"
      ? parsed
      : { decisions: {}, manual_candidates: [], revision_candidates: [] };
  } catch {
    registrationReviewState = { decisions: {}, manual_candidates: [], revision_candidates: [] };
  }
  registrationReviewState.decisions ??= {};
  registrationReviewState.manual_candidates ??= [];
  registrationReviewState.revision_candidates ??= [];
}

function saveRegistrationReviewState(): void {
  if (!isDeveloper() || !candidatePayload()) return;
  localStorage.setItem(reviewStorageKey(), JSON.stringify(registrationReviewState));
}

function decisionForCandidate(candidate: JsonObject): JsonObject | null {
  return registrationReviewState.decisions?.[String(candidate.path ?? "")] ?? null;
}

function revisionStateByPath(path: string): JsonObject | null {
  return (registrationReviewState.revision_candidates ?? []).find((item: JsonObject) => String(item.path ?? "") === path) ?? null;
}

function decisionForRegisteredReview(item: JsonObject): string {
  return String(revisionStateByPath(String(item.path ?? ""))?.decision ?? "unreviewed");
}

function reviewDecisionLabel(value: string): string {
  const labels: Record<string, [string, string]> = {
    approve: ["承認", "Approved"],
    approve_with_edits: ["修正承認", "Approved with edits"],
    hold: ["保留", "On hold"],
    reject: ["却下", "Rejected"],
    unreviewed: ["未確認", "Unreviewed"],
  };
  const pair = labels[value] ?? [value, value];
  return pair[displayLang === "ja" ? 0 : 1];
}

function decisionTone(value: string): string {
  if (value === "approve" || value === "approve_with_edits") return "ok";
  if (value === "hold") return "warn";
  if (value === "reject") return "danger";
  return "";
}

function decisionCounts(): Record<string, number> {
  const counts: Record<string, number> = { unreviewed: 0, approve: 0, approve_with_edits: 0, hold: 0, reject: 0 };
  for (const candidate of candidateList()) {
    const decision = decisionForCandidate(candidate);
    const key = String(decision?.decision ?? "unreviewed");
    counts[key] = (counts[key] ?? 0) + 1;
  }
  return counts;
}

function registeredReviewDecisionCounts(): Record<string, number> {
  const counts: Record<string, number> = { unreviewed: 0, approve: 0, approve_with_edits: 0, hold: 0, reject: 0 };
  for (const item of registeredReviewList()) {
    const key = decisionForRegisteredReview(item);
    counts[key] = (counts[key] ?? 0) + 1;
  }
  return counts;
}

function combinedReviewCounts(): Record<string, number> {
  const left = decisionCounts();
  const right = registeredReviewDecisionCounts();
  const result: Record<string, number> = {};
  for (const key of new Set([...Object.keys(left), ...Object.keys(right)])) result[key] = (left[key] ?? 0) + (right[key] ?? 0);
  return result;
}

function reviewExportPayload(): JsonObject {
  const source = candidatePayload()?.source ?? {};
  const decisions = Object.values(registrationReviewState.decisions ?? {}).sort((a: any, b: any) =>
    String(a.path ?? "").localeCompare(String(b.path ?? ""), "en"),
  );
  const counts = combinedReviewCounts();
  const provisionalCounts = decisionCounts();
  const registeredCounts = registeredReviewDecisionCounts();
  const totalReviewItems = candidateList().length + registeredReviewList().length;
  return {
    registration_review: {
      schema_version: "0.3",
      status: counts.unreviewed === 0 ? "complete" : "in_progress",
      exported_at: new Date().toISOString(),
      source: {
        manifest_sha256: String(source.manifest_sha256 ?? ""),
        graph_sha256: String(source.graph_sha256 ?? ""),
        provisional_count: candidateList().length,
        revision_proposals_sha256: String(source.revision_proposals_sha256 ?? ""),
        revision_proposal_count: registeredReviewList().length,
      },
      summary: {
        total_review_items: totalReviewItems,
        reviewed: totalReviewItems - counts.unreviewed,
        ...counts,
        provisional_documents: candidateList().length,
        registered_revision_proposals: registeredReviewList().length,
        provisional_reviewed: candidateList().length - provisionalCounts.unreviewed,
        registered_revision_reviewed: registeredReviewList().length - registeredCounts.unreviewed,
        manual_candidates: (registrationReviewState.manual_candidates ?? []).length,
        revision_candidates: (registrationReviewState.revision_candidates ?? []).length,
      },
      decisions,
      manual_candidates: registrationReviewState.manual_candidates ?? [],
      revision_candidates: registrationReviewState.revision_candidates ?? [],
    },
  };
}

function downloadReviewExport(): void {
  const data = JSON.stringify(reviewExportPayload(), null, 2) + "\n";
  const blob = new Blob([data], { type: "application/json;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "docs_registration_review.json";
  document.body.append(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

async function importReviewExport(file: File): Promise<void> {
  const text = await file.text();
  const parsed = JSON.parse(text);
  const payload = parsed?.registration_review;
  if (!payload || String(payload.schema_version ?? "") !== "0.3") {
    throw new Error("現在のRegistration Workbenchでは registration_review schema_version 0.3 が必要です。");
  }
  const current = candidatePayload()?.source ?? {};
  for (const key of ["manifest_sha256", "graph_sha256", "revision_proposals_sha256"]) {
    if (String(payload.source?.[key] ?? "") !== String(current[key] ?? "")) {
      throw new Error(`古いレビューです: ${key} が現在のworkbench sourceと一致しません。`);
    }
  }
  if (Number(payload.source?.provisional_count ?? -1) !== candidateList().length) {
    throw new Error("古いレビューです: provisional_count が現在値と一致しません。");
  }
  if (Number(payload.source?.revision_proposal_count ?? -1) !== registeredReviewList().length) {
    throw new Error("古いレビューです: revision_proposal_count が現在値と一致しません。");
  }
  const decisions: JsonObject = {};
  for (const item of payload.decisions ?? []) {
    const path = String(item.path ?? "");
    if (!path || !candidateByPath(path)) throw new Error(`現在のprovisional setに存在しないdecisionです: ${path}`);
    decisions[path] = item;
  }
  registrationReviewState = {
    decisions,
    manual_candidates: Array.isArray(payload.manual_candidates) ? payload.manual_candidates : [],
    revision_candidates: Array.isArray(payload.revision_candidates) ? payload.revision_candidates : [],
  };
  saveRegistrationReviewState();
}

function reviewPoolItems(): JsonObject[] {
  const items: JsonObject[] = [];
  for (const candidate of candidateList()) {
    const baseline = candidate.baseline ?? {};
    items.push({
      kind: "provisional",
      key: `provisional:${String(candidate.path ?? "")}`,
      path: String(candidate.path ?? ""),
      layer: String(baseline.layer ?? ""),
      visibility: String(baseline.discovery?.visibility ?? ""),
      title: candidateTitle(candidate),
      role: candidateRole(candidate),
      questions: candidateQuestionList(candidate),
      decision: String(decisionForCandidate(candidate)?.decision ?? "unreviewed"),
      search_text: candidateSearchText(candidate),
      source: candidate,
    });
  }
  for (const proposal of registeredReviewList()) {
    const path = String(proposal.path ?? "");
    const before = proposal.before ?? {};
    const after = proposal.after ?? {};
    const questions = after.discovery?.reader_questions ?? {};
    const values = [
      path,
      after.title_ja,
      after.title_en,
      after.role_ja,
      after.role_en,
      proposal.source_kind,
      proposal.review_note,
      ...(questions.ja ?? []),
      ...(questions.en ?? []),
    ];
    items.push({
      kind: "registered_revision",
      key: `registered:${path}`,
      path,
      layer: String(after.layer ?? before.layer ?? ""),
      visibility: "registered",
      title: String((displayLang === "ja" ? after.title_ja : after.title_en) || after.title_ja || after.title_en || path),
      role: String((displayLang === "ja" ? after.role_ja : after.role_en) || after.role_ja || after.role_en || ""),
      questions: (questions[displayLang] ?? questions.ja ?? questions.en ?? []).map((value: any) => String(value)),
      decision: decisionForRegisteredReview(proposal),
      search_text: values.filter(Boolean).join(" ").normalize("NFKC").toLocaleLowerCase("ja-JP"),
      source: proposal,
    });
  }
  return items.sort((a: JsonObject, b: JsonObject) => String(a.path).localeCompare(String(b.path), "en") || String(a.kind).localeCompare(String(b.kind), "en"));
}

function nextUnreviewedReviewItem(afterKey = ""): JsonObject | undefined {
  const items = reviewPoolItems();
  const start = Math.max(0, items.findIndex((item: JsonObject) => String(item.key) === afterKey) + 1);
  return [...items.slice(start), ...items.slice(0, start)].find((item: JsonObject) => String(item.decision) === "unreviewed");
}

function openReviewPoolItem(item: JsonObject): void {
  if (item.kind === "registered_revision") setRoute({ view: "registered-review", registered: String(item.path) });
  else setRoute({ view: "candidates", candidate: String(item.path) });
}

function candidateStateBanner(): HTMLElement {
  const payload = candidatePayload();
  const banner = el("div", "candidate-boundary-note");
  banner.append(badge("DEVELOPER WORKBENCH", "warn"));
  banner.append(
    el(
      "span",
      "",
      displayLang === "ja"
        ? "仮登録文書と登録済み改訂案を同じレビュー面で扱います。途中状態はブラウザ内に保存され、ファイル出力は『レビュー結果を書き出す』を押したときだけ行います。manifestはこの画面から直接変更しません。"
        : "Provisional documents and registered revision proposals share one review surface. In-progress state stays in the browser; a file is created only when you explicitly choose Export review. This screen does not write the manifest directly.",
    ),
  );
  if (!payload) banner.append(badge(displayLang === "ja" ? "Workbenchデータ未読込" : "Workbench data unavailable", "danger"));
  return banner;
}

function candidateMetric(label: string, value: string): HTMLElement {
  const box = el("div", "stat-box");
  box.append(el("span", "stat-value", value), el("span", "stat-label", label));
  return box;
}

function textInput(value = "", className = "workbench-input"): HTMLInputElement {
  const input = el("input", className) as HTMLInputElement;
  input.type = "text";
  input.value = value;
  return input;
}

function textArea(value = "", rows = 3): HTMLTextAreaElement {
  const input = el("textarea", "workbench-textarea") as HTMLTextAreaElement;
  input.value = value;
  input.rows = rows;
  return input;
}

function reviewField(label: string, control: HTMLElement, hint = ""): HTMLElement {
  const wrap = el("label", "workbench-field");
  wrap.append(el("span", "workbench-label", label), control);
  if (hint) wrap.append(el("span", "workbench-hint", hint));
  return wrap;
}

function lines(value: string): string[] {
  return value.split(/\r?\n/).map((item) => item.trim()).filter(Boolean);
}

function commaValues(value: string): string[] {
  return value.split(/[,、\n]/).map((item) => item.trim()).filter(Boolean);
}

function candidateDetail(candidate: JsonObject): HTMLElement {
  const page = el("main", "page");
  page.append(navBar("candidates"), dataBanner(), candidateStateBanner());
  const back = button(displayLang === "ja" ? "← レビュー一覧" : "← Review pool", "back-button");
  back.addEventListener("click", () => setRoute({ view: "candidates" }));
  page.append(back);

  const baseline = deepClone(candidate.baseline ?? {});
  const existing = decisionForCandidate(candidate);
  const working = deepClone(existing?.after ?? baseline);
  const discovery = working.discovery ??= {};
  discovery.aliases ??= { ja: [], en: [] };
  discovery.reader_questions ??= { ja: [], en: [] };
  discovery.topics ??= [];

  const path = String(candidate.path ?? baseline.path ?? "");
  const hero = el("section", "doc-header candidate-detail-header");
  const meta = el("div", "doc-meta-line");
  meta.append(
    badge(displayLang === "ja" ? "manifest仮登録" : "Manifest provisional", "warn"),
    badge(String(discovery.visibility ?? "secondary")),
    badge(reviewDecisionLabel(String(existing?.decision ?? "unreviewed")), decisionTone(String(existing?.decision ?? "unreviewed"))),
  );
  hero.append(eyebrow(`PROVISIONAL REGISTRATION · ${String(working.doc_id ?? "")}`), el("h1", "hero-title", candidateTitle(candidate)), meta);
  const role = candidateRole(candidate);
  if (role) hero.append(el("p", "hero-copy", role));
  hero.append(el("div", "path", path));
  const actions = el("div", "reader-actions");
  if (path && readerAllowedPaths().has(path)) actions.append(readerButton(path, "button primary"));
  const doc = docByPath(path);
  const graphId = doc ? graphNodeForDocument(doc) : "";
  if (graphId) {
    const relations = button(displayLang === "ja" ? "現在の関係を見る" : "Current relations", "button secondary");
    relations.addEventListener("click", () => setRoute({ graph: graphId }));
    actions.append(relations);
  }
  hero.append(actions);
  page.append(hero);

  const form = el("section", "audit-panel candidate-review-panel workbench-editor");
  form.append(
    el("h2", "section-title small", displayLang === "ja" ? "仮登録metadataを確認・修正" : "Review provisional metadata"),
    el("p", "section-copy", displayLang === "ja"
      ? "表示値は現在のdocs_manifest.ymlにあるprovisional登録です。この画面はmanifestを直接書き換えません。承認結果を書き出し、Repository側でvalidate / dry-run / explicit applyしたときだけregisteredへ昇格します。"
      : "These values come from the current provisional entry in docs_manifest.yml. The browser does not write the manifest. Promotion to registered occurs only after export, repository-side validation, dry-run, and explicit apply."),
  );
  const controls: Record<string, HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement> = {};
  controls.doc_id = textInput(String(working.doc_id ?? ""));
  (controls.doc_id as HTMLInputElement).readOnly = true;
  controls.title_ja = textInput(String(working.title_ja ?? ""));
  controls.title_en = textInput(String(working.title_en ?? ""));
  controls.document_type = textInput(String(working.document_type ?? ""));
  controls.layer = textInput(String(working.layer ?? ""));
  controls.status = textInput(String(working.status ?? ""));
  controls.public_profile = textInput(String(working.public_profile ?? ""));
  controls.state = textInput(String(working.state ?? ""));
  controls.scope = textArea(String(working.scope ?? ""), 2);
  controls.role_ja = textArea(String(working.role_ja ?? ""), 3);
  controls.role_en = textArea(String(working.role_en ?? ""), 3);
  controls.topics = textInput((discovery.topics ?? []).join(", "));
  controls.aliases_ja = textArea((discovery.aliases?.ja ?? []).join("\n"), 3);
  controls.aliases_en = textArea((discovery.aliases?.en ?? []).join("\n"), 3);
  controls.questions_ja = textArea((discovery.reader_questions?.ja ?? []).join("\n"), 4);
  controls.questions_en = textArea((discovery.reader_questions?.en ?? []).join("\n"), 4);
  const entrySelect = el("select", "candidate-select") as HTMLSelectElement;
  const entryValues = ["", "foundation", "intermediate", "advanced"];
  for (const value of entryValues) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value || (displayLang === "ja" ? "未設定" : "Unset");
    option.selected = String(discovery.entry_level ?? "") === value;
    entrySelect.append(option);
  }
  controls.entry_level = entrySelect;
  const fieldGrid = el("div", "workbench-field-grid");
  for (const [label, key] of [
    ["doc_id", "doc_id"], [displayLang === "ja" ? "日本語タイトル" : "Japanese title", "title_ja"],
    [displayLang === "ja" ? "英語タイトル" : "English title", "title_en"], ["document_type", "document_type"],
    [displayLang === "ja" ? "体系層" : "Layer", "layer"], ["status", "status"], ["public_profile", "public_profile"], ["state", "state"],
  ] as Array<[string, string]>) fieldGrid.append(reviewField(label, controls[key]));
  form.append(fieldGrid,
    reviewField("scope", controls.scope),
    reviewField("role_ja", controls.role_ja), reviewField("role_en", controls.role_en),
    reviewField("topics", controls.topics, displayLang === "ja" ? "カンマ区切り" : "Comma-separated"),
    reviewField("aliases · ja", controls.aliases_ja, displayLang === "ja" ? "1行1件" : "One per line"),
    reviewField("aliases · en", controls.aliases_en, displayLang === "ja" ? "1行1件" : "One per line"),
    reviewField("reader questions · ja", controls.questions_ja, displayLang === "ja" ? "1行1件" : "One per line"),
    reviewField("reader questions · en", controls.questions_en, displayLang === "ja" ? "1行1件" : "One per line"),
    reviewField("entry_level", controls.entry_level),
  );
  const note = textArea(String(existing?.reviewer_note ?? ""), 2);
  form.append(reviewField(displayLang === "ja" ? "レビュー注記" : "Reviewer note", note));

  const readForm = (): JsonObject => {
    const after = deepClone(baseline);
    for (const key of ["title_ja", "title_en", "document_type", "layer", "status", "public_profile", "state", "scope", "role_ja", "role_en"]) {
      after[key] = controls[key].value.trim();
    }
    after.discovery ??= {};
    after.discovery.topics = commaValues(controls.topics.value);
    after.discovery.aliases = { ja: lines(controls.aliases_ja.value), en: lines(controls.aliases_en.value) };
    after.discovery.reader_questions = { ja: lines(controls.questions_ja.value), en: lines(controls.questions_en.value) };
    after.discovery.entry_level = controls.entry_level.value;
    return after;
  };

  const saveDecision = (kind: "approve" | "hold" | "reject"): void => {
    const after = readForm();
    const changed = JSON.stringify(after) !== JSON.stringify(baseline);
    const decision = kind === "approve" ? (changed ? "approve_with_edits" : "approve") : kind;
    registrationReviewState.decisions[path] = {
      path, doc_id: String(baseline.doc_id ?? ""), decision,
      reviewed_at: new Date().toISOString(), reviewer_note: note.value.trim(), before: baseline, after,
    };
    saveRegistrationReviewState();
    const next = nextUnreviewedReviewItem(`provisional:${path}`);
    if (kind === "approve" && next) openReviewPoolItem(next);
    else render();
  };
  const decisionBar = el("div", "workbench-decision-bar");
  const approve = button(displayLang === "ja" ? "この内容で承認して次へ" : "Approve and next", "button primary");
  approve.addEventListener("click", () => saveDecision("approve"));
  const hold = button(displayLang === "ja" ? "保留" : "Hold", "button"); hold.addEventListener("click", () => saveDecision("hold"));
  const reject = button(displayLang === "ja" ? "却下" : "Reject", "button danger-button"); reject.addEventListener("click", () => saveDecision("reject"));
  const clear = button(displayLang === "ja" ? "この判断を未確認に戻す" : "Reset to unreviewed", "text-button");
  clear.addEventListener("click", () => { delete registrationReviewState.decisions[path]; saveRegistrationReviewState(); render(); });
  decisionBar.append(approve, hold, reject, clear);
  form.append(decisionBar);
  page.append(form);

  const language = baseline.language_relation ?? {};
  if (language && typeof language === "object" && Object.keys(language).length) {
    const languagePanel = el("section", "audit-panel candidate-review-panel");
    languagePanel.append(el("h2", "section-title small", displayLang === "ja" ? "現在の言語関係" : "Current language relation"));
    for (const [label, value] of Object.entries(language)) {
      const row = el("div", "candidate-kv"); row.append(el("span", "candidate-k", label), el("span", "candidate-v path", String(value ?? ""))); languagePanel.append(row);
    }
    page.append(languagePanel);
  }
  return page;
}

function revisionBaselineForDoc(doc: JsonObject): JsonObject {
  const path = String(doc.path ?? "");
  const manifestRecord = registeredDocumentByPath(path);
  if (manifestRecord?.baseline) return deepClone(manifestRecord.baseline);
  return {
    path,
    doc_id: String(doc.id ?? doc.doc_id ?? ""),
    document_type: String(doc.document_type ?? ""),
    title_ja: String(doc.title?.ja ?? ""),
    title_en: String(doc.title?.en ?? ""),
    layer: String(doc.layer ?? ""),
    status: String(doc.status ?? ""),
    state: String(doc.state ?? ""),
    registration_state: "registered",
    scope: String(doc.scope ?? ""),
    role_ja: String(doc.role?.ja ?? ""),
    role_en: String(doc.role?.en ?? ""),
    discovery: deepClone(doc.discovery ?? {}),
  };
}

function renderRegisteredRevisionProposal(path: string): HTMLElement {
  const proposal = registeredReviewByPath(path);
  if (!proposal) return errorPage(`Unknown registered revision proposal: ${path}`);
  const doc = docByPath(path);
  if (!doc || isProvisionalDoc(doc)) return errorPage(`Registered document not found for revision proposal: ${path}`);

  const page = el("main", "page");
  page.append(navBar("candidates"), dataBanner(), candidateStateBanner());
  const back = button(displayLang === "ja" ? "← レビュー一覧" : "← Review pool", "back-button");
  back.addEventListener("click", () => setRoute({ view: "candidates" }));
  page.append(back);

  const baseline = deepClone(proposal.before ?? revisionBaselineForDoc(doc));
  const existing = revisionStateByPath(path);
  const working = existing?.after && Object.keys(existing.after).length ? deepClone(existing.after) : deepClone(proposal.after ?? baseline);
  working.discovery ??= {};
  working.discovery.aliases ??= { ja: [], en: [] };
  working.discovery.reader_questions ??= { ja: [], en: [] };
  working.discovery.topics ??= [];

  const hero = el("section", "doc-header candidate-detail-header");
  const meta = el("div", "doc-meta-line");
  meta.append(
    badge(displayLang === "ja" ? "登録済み" : "Registered"),
    badge(displayLang === "ja" ? "改訂案" : "Revision proposal", "warn"),
    badge(String(proposal.source_kind ?? "metadata_revision")),
    badge(reviewDecisionLabel(String(existing?.decision ?? "unreviewed")), decisionTone(String(existing?.decision ?? "unreviewed"))),
  );
  const title = String((displayLang === "ja" ? working.title_ja : working.title_en) || working.title_ja || working.title_en || path);
  hero.append(eyebrow(`REGISTERED REVISION · ${String(working.doc_id ?? "")}`), el("h1", "hero-title", title), meta);
  const role = String((displayLang === "ja" ? working.role_ja : working.role_en) || working.role_ja || working.role_en || "");
  if (role) hero.append(el("p", "hero-copy", role));
  hero.append(el("div", "path", path));
  const actions = el("div", "reader-actions");
  actions.append(readerButton(path, "button primary"));
  const graphId = graphNodeForDocument(doc);
  if (graphId) {
    const relations = button(displayLang === "ja" ? "現在の関係を見る" : "Current relations", "button secondary");
    relations.addEventListener("click", () => setRoute({ graph: graphId }));
    actions.append(relations);
  }
  hero.append(actions);
  page.append(hero);

  const form = el("section", "audit-panel candidate-review-panel workbench-editor");
  form.append(
    el("h2", "section-title small", displayLang === "ja" ? "登録済みmetadataの改訂案" : "Registered metadata revision proposal"),
    el("p", "section-copy", displayLang === "ja"
      ? "現在の登録は維持したまま、提案された差分を確認します。ここで編集してもmanifestは直接変更されません。"
      : "Review the proposed metadata change while the current registration remains active. Editing here does not directly write the manifest."),
  );
  if (proposal.review_note) form.append(el("p", "candidate-review-hint", String(proposal.review_note)));

  const controls: Record<string, HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement> = {};
  controls.doc_id = textInput(String(working.doc_id ?? "")); (controls.doc_id as HTMLInputElement).readOnly = true;
  controls.title_ja = textInput(String(working.title_ja ?? "")); controls.title_en = textInput(String(working.title_en ?? ""));
  controls.document_type = textInput(String(working.document_type ?? "")); controls.layer = textInput(String(working.layer ?? ""));
  controls.status = textInput(String(working.status ?? "")); controls.public_profile = textInput(String(working.public_profile ?? "")); controls.state = textInput(String(working.state ?? ""));
  controls.scope = textArea(String(working.scope ?? ""), 2); controls.role_ja = textArea(String(working.role_ja ?? ""), 3); controls.role_en = textArea(String(working.role_en ?? ""), 3);
  controls.topics = textInput((working.discovery.topics ?? []).join(", ")); controls.aliases_ja = textArea((working.discovery.aliases?.ja ?? []).join("\n"), 3); controls.aliases_en = textArea((working.discovery.aliases?.en ?? []).join("\n"), 3);
  controls.questions_ja = textArea((working.discovery.reader_questions?.ja ?? []).join("\n"), 5); controls.questions_en = textArea((working.discovery.reader_questions?.en ?? []).join("\n"), 5);
  const entry = el("select", "candidate-select") as HTMLSelectElement;
  for (const value of ["", "foundation", "intermediate", "advanced"]) { const o=document.createElement("option"); o.value=value; o.textContent=value || (displayLang === "ja" ? "未設定" : "Unset"); o.selected=String(working.discovery.entry_level ?? "")===value; entry.append(o); } controls.entry_level=entry;
  const grid=el("div","workbench-field-grid"); for (const key of ["doc_id","title_ja","title_en","document_type","layer","status","public_profile","state"]) grid.append(reviewField(key,controls[key]));
  form.append(grid, reviewField("scope",controls.scope), reviewField("role_ja",controls.role_ja), reviewField("role_en",controls.role_en), reviewField("topics",controls.topics), reviewField("aliases · ja",controls.aliases_ja), reviewField("aliases · en",controls.aliases_en), reviewField("reader questions · ja",controls.questions_ja), reviewField("reader questions · en",controls.questions_en), reviewField("entry_level",controls.entry_level));
  const note=textArea(String(existing?.reviewer_note ?? ""),2); form.append(reviewField(displayLang === "ja" ? "レビュー注記" : "Reviewer note",note));
  const read=():JsonObject=>{ const after=deepClone(baseline); for(const key of ["title_ja","title_en","document_type","layer","status","public_profile","state","scope","role_ja","role_en"]) after[key]=controls[key].value.trim(); after.discovery ??={}; after.discovery.topics=commaValues(controls.topics.value); after.discovery.aliases={ja:lines(controls.aliases_ja.value),en:lines(controls.aliases_en.value)}; after.discovery.reader_questions={ja:lines(controls.questions_ja.value),en:lines(controls.questions_en.value)}; after.discovery.entry_level=controls.entry_level.value; return after; };
  const save=(decision:"approve"|"hold"|"reject")=>{ const after=read(); const item={ doc_id:String(baseline.doc_id ?? ""), path, created_at:String(existing?.created_at ?? new Date().toISOString()), reviewed_at:new Date().toISOString(), reviewer_note:note.value.trim(), decision, source_kind:"revision_proposal", proposal_id:String(proposal.proposal_id ?? ""), proposal_source_sha256:String(candidatePayload()?.source?.revision_proposals_sha256 ?? ""), before:baseline, after }; const others=(registrationReviewState.revision_candidates ?? []).filter((entry:JsonObject)=>String(entry.path ?? "")!==path); registrationReviewState.revision_candidates=[...others,item]; saveRegistrationReviewState(); const next=nextUnreviewedReviewItem(`registered:${path}`); if(decision==="approve" && next) openReviewPoolItem(next); else render(); };
  const bar=el("div","workbench-decision-bar"); const approve=button(displayLang === "ja" ? "この改訂案を承認して次へ" : "Approve revision and next","button primary"); approve.addEventListener("click",()=>save("approve")); const hold=button(displayLang === "ja" ? "保留" : "Hold","button"); hold.addEventListener("click",()=>save("hold")); const reject=button(displayLang === "ja" ? "却下" : "Reject","button danger-button"); reject.addEventListener("click",()=>save("reject")); const clear=button(displayLang === "ja" ? "未確認に戻す" : "Reset to unreviewed","text-button"); clear.addEventListener("click",()=>{ registrationReviewState.revision_candidates=(registrationReviewState.revision_candidates ?? []).filter((entry:JsonObject)=>String(entry.path ?? "")!==path); saveRegistrationReviewState(); render(); }); bar.append(approve,hold,reject,clear); form.append(bar); page.append(form); return page;
}

function renderManualCandidate(): HTMLElement {
  const page = el("main", "page");
  page.append(navBar("candidates"), dataBanner(), candidateStateBanner());
  const back = button(displayLang === "ja" ? "← 候補一覧" : "← Candidate list", "back-button"); back.addEventListener("click", () => setRoute({ view: "candidates" })); page.append(back);
  const section = el("section", "audit-panel workbench-editor");
  section.append(eyebrow("MANUAL CANDIDATE"), el("h1", "section-title", displayLang === "ja" ? "候補を手動で追加" : "Create a manual candidate"));
  const fields: Record<string, HTMLInputElement | HTMLTextAreaElement> = {
    path: textInput(), doc_id: textInput(), title_ja: textInput(), title_en: textInput(), layer: textInput(), document_type: textInput("assertion_document"),
    status: textInput(), public_profile: textInput(), scope: textArea("", 2), role_ja: textArea("", 3), role_en: textArea("", 3), topics: textInput(), questions_ja: textArea("", 3), questions_en: textArea("", 3), note: textArea("", 2),
  };
  const grid = el("div", "workbench-field-grid");
  for (const key of ["path", "doc_id", "title_ja", "title_en", "layer", "document_type", "status", "public_profile"]) grid.append(reviewField(key, fields[key]));
  section.append(grid, reviewField("scope", fields.scope), reviewField("role_ja", fields.role_ja), reviewField("role_en", fields.role_en), reviewField("topics", fields.topics), reviewField("reader questions · ja", fields.questions_ja), reviewField("reader questions · en", fields.questions_en), reviewField(displayLang === "ja" ? "注記" : "Note", fields.note));
  const storeManual = (decision: "approve" | "hold"): void => {
    const path = fields.path.value.trim(); const docId = fields.doc_id.value.trim();
    if (!path || !docId) { alert(displayLang === "ja" ? "path と doc_id は必須です。" : "path and doc_id are required."); return; }
    const item = {
      id: `manual:${docId}:${Date.now()}`, created_at: new Date().toISOString(), reviewer_note: fields.note.value.trim(), decision,
      proposed: {
        path, doc_id: docId, title_ja: fields.title_ja.value.trim(), title_en: fields.title_en.value.trim(), layer: fields.layer.value.trim(), document_type: fields.document_type.value.trim(), status: fields.status.value.trim(), public_profile: fields.public_profile.value.trim(), state: "public-candidate", scope: fields.scope.value.trim(), role_ja: fields.role_ja.value.trim(), role_en: fields.role_en.value.trim(),
        discovery: { topics: commaValues(fields.topics.value), aliases: { ja: [], en: [] }, reader_questions: { ja: lines(fields.questions_ja.value), en: lines(fields.questions_en.value) }, entry_level: "intermediate" },
      },
    };
    registrationReviewState.manual_candidates.push(item); saveRegistrationReviewState(); setRoute({ view: "candidates" });
  };
  const bar = el("div", "workbench-decision-bar");
  const approve = button(displayLang === "ja" ? "この手動候補を承認" : "Approve manual candidate", "button primary");
  approve.addEventListener("click", () => storeManual("approve"));
  const hold = button(displayLang === "ja" ? "候補として保留" : "Save on hold", "button");
  hold.addEventListener("click", () => storeManual("hold"));
  bar.append(approve, hold); section.append(bar); page.append(section); return page;
}

function addRevisionCandidate(doc: JsonObject): void {
  const before = revisionBaselineForDoc(doc);
  const docId = String(before.doc_id ?? doc.id ?? doc.doc_id ?? "");
  const path = String(doc.path ?? "");
  if (registeredReviewByPath(path)) {
    alert(displayLang === "ja" ? "この文書には既存の改訂提案があります。登録レビューから確認してください。" : "This document already has an active revision proposal. Review it from the registration workbench."); return;
  }
  if ((registrationReviewState.revision_candidates ?? []).some((item: JsonObject) => String(item.doc_id) === docId)) {
    alert(displayLang === "ja" ? "この文書はすでに改訂候補へ入っています。" : "This document is already in the revision queue."); return;
  }
  const note = prompt(displayLang === "ja" ? "改訂候補にする理由・メモ（空でも可）" : "Reason/note for revision candidate (optional)") ?? "";
  registrationReviewState.revision_candidates.push({ doc_id: docId, path: String(doc.path ?? ""), created_at: new Date().toISOString(), reviewer_note: note.trim(), decision: "hold", source_kind: "ad_hoc_registered_revision", before, after: {} });
  saveRegistrationReviewState();
  setRoute({ view: "revision-candidate", revision: docId });
}

function renderRevisionCandidate(docId: string): HTMLElement {
  const item = (registrationReviewState.revision_candidates ?? []).find((entry: JsonObject) => String(entry.doc_id ?? "") === docId);
  if (!item) return errorPage(`Unknown revision candidate: ${docId}`);
  const page = el("main", "page");
  page.append(navBar("candidates"), dataBanner(), candidateStateBanner());
  const back = button(displayLang === "ja" ? "← 候補一覧" : "← Candidate list", "back-button"); back.addEventListener("click", () => setRoute({ view: "candidates" })); page.append(back);
  const baseline = deepClone(item.before ?? {});
  const working = Object.keys(item.after ?? {}).length ? deepClone(item.after) : deepClone(baseline);
  working.discovery ??= {}; working.discovery.aliases ??= { ja: [], en: [] }; working.discovery.reader_questions ??= { ja: [], en: [] }; working.discovery.topics ??= [];
  const section = el("section", "audit-panel workbench-editor");
  section.append(eyebrow("REVISION CANDIDATE"), el("h1", "section-title", String(working.title_ja || working.title_en || docId)), el("p", "section-copy", displayLang === "ja" ? "現在の公開登録は維持したまま、次のmanifest改訂候補を編集します。" : "Edit a future manifest revision while the current public registration remains active."));
  const controls: Record<string, HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement> = {};
  for (const key of ["doc_id", "title_ja", "title_en", "document_type", "layer", "status", "public_profile", "state"]) controls[key] = textInput(String(working[key] ?? ""));
  (controls.doc_id as HTMLInputElement).readOnly = true;
  controls.scope = textArea(String(working.scope ?? ""), 2); controls.role_ja = textArea(String(working.role_ja ?? ""), 3); controls.role_en = textArea(String(working.role_en ?? ""), 3); controls.topics = textInput((working.discovery.topics ?? []).join(", ")); controls.aliases_ja = textArea((working.discovery.aliases?.ja ?? []).join("\n"), 3); controls.aliases_en = textArea((working.discovery.aliases?.en ?? []).join("\n"), 3); controls.questions_ja = textArea((working.discovery.reader_questions?.ja ?? []).join("\n"), 4); controls.questions_en = textArea((working.discovery.reader_questions?.en ?? []).join("\n"), 4);
  const entry = el("select", "candidate-select") as HTMLSelectElement; for (const value of ["foundation", "intermediate", "advanced"]) { const o=document.createElement("option"); o.value=value; o.textContent=value; o.selected=String(working.discovery.entry_level ?? "")===value; entry.append(o); } controls.entry_level=entry;
  const grid=el("div","workbench-field-grid"); for (const key of ["doc_id","title_ja","title_en","document_type","layer","status","public_profile","state"]) grid.append(reviewField(key,controls[key])); section.append(grid, reviewField("scope",controls.scope), reviewField("role_ja",controls.role_ja), reviewField("role_en",controls.role_en), reviewField("topics",controls.topics), reviewField("aliases · ja",controls.aliases_ja), reviewField("aliases · en",controls.aliases_en), reviewField("reader questions · ja",controls.questions_ja), reviewField("reader questions · en",controls.questions_en), reviewField("entry_level",controls.entry_level));
  const note=textArea(String(item.reviewer_note ?? ""),2); section.append(reviewField(displayLang === "ja" ? "レビュー注記" : "Reviewer note",note));
  const read=():JsonObject=>{ const after=deepClone(baseline); for(const key of ["title_ja","title_en","document_type","layer","status","public_profile","state","scope","role_ja","role_en"]) after[key]=controls[key].value.trim(); after.discovery ??={}; after.discovery.topics=commaValues(controls.topics.value); after.discovery.aliases={ja:lines(controls.aliases_ja.value),en:lines(controls.aliases_en.value)}; after.discovery.reader_questions={ja:lines(controls.questions_ja.value),en:lines(controls.questions_en.value)}; after.discovery.entry_level=controls.entry_level.value; return after; };
  const save=(decision:"approve"|"hold"|"reject")=>{ item.after=read(); item.decision=decision; item.reviewer_note=note.value.trim(); item.reviewed_at=new Date().toISOString(); saveRegistrationReviewState(); setRoute({view:"candidates"}); };
  const bar=el("div","workbench-decision-bar"); const approve=button(displayLang === "ja" ? "改訂内容を承認" : "Approve revision","button primary"); approve.addEventListener("click",()=>save("approve")); const hold=button(displayLang === "ja" ? "保留" : "Hold","button"); hold.addEventListener("click",()=>save("hold")); const reject=button(displayLang === "ja" ? "却下" : "Reject","button danger-button"); reject.addEventListener("click",()=>save("reject")); bar.append(approve,hold,reject); section.append(bar); page.append(section); return page;
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
    eyebrow("REGISTRATION WORKBENCH"),
    el("h1", "hero-title", displayLang === "ja" ? "仮登録と改訂案を同じ土俵でレビューする" : "Review provisional and registered revisions in one pool"),
    el("p", "hero-copy", displayLang === "ja"
      ? "docs_manifest.ymlにすでにある仮登録文書と、登録済み文書の改訂案を一つのレビュー面で扱います。ブラウザはmanifestを直接書き換えません。"
      : "Manifest-backed provisional documents and registered-document revision proposals share one review pool. The browser does not write the manifest directly."),
  );
  if (!payload) {
    section.append(el("p", "error", displayLang === "ja" ? "Registration Workbench previewを読み込めませんでした。" : "Registration Workbench preview could not be loaded."));
    page.append(section);
    return page;
  }

  const counts = combinedReviewCounts();
  const adHocRevisions = (registrationReviewState.revision_candidates ?? []).filter((item: JsonObject) => item.source_kind !== "revision_proposal");
  const stats = el("div", "audit-stats candidate-stats");
  stats.append(
    candidateMetric(displayLang === "ja" ? "未確認" : "Unreviewed", String(counts.unreviewed)),
    candidateMetric(displayLang === "ja" ? "承認" : "Approved", String((counts.approve ?? 0) + (counts.approve_with_edits ?? 0))),
    candidateMetric(displayLang === "ja" ? "保留" : "On hold", String(counts.hold ?? 0)),
    candidateMetric(displayLang === "ja" ? "却下" : "Rejected", String(counts.reject ?? 0)),
    candidateMetric(displayLang === "ja" ? "仮登録文書" : "Provisional", String(candidateList().length)),
    candidateMetric(displayLang === "ja" ? "登録済み改訂案" : "Registered revisions", String(registeredReviewList().length)),
  );
  section.append(stats);

  const toolbar = el("div", "workbench-toolbar");
  const next = button(displayLang === "ja" ? "次の未確認へ" : "Next unreviewed", "button primary");
  next.addEventListener("click", () => { const item = nextUnreviewedReviewItem(); if (item) openReviewPoolItem(item); });
  const exportButton = button(displayLang === "ja" ? "レビュー結果を書き出す" : "Export review", "button");
  exportButton.addEventListener("click", downloadReviewExport);
  const importLabel = el("label", "button workbench-file-button", displayLang === "ja" ? "レビュー結果を読み込む" : "Import review");
  const importInput = document.createElement("input");
  importInput.type = "file";
  importInput.accept = "application/json,.json";
  importInput.hidden = true;
  importInput.addEventListener("change", async () => {
    const file = importInput.files?.[0];
    if (!file) return;
    try { await importReviewExport(file); render(); }
    catch (error) { alert(String((error as Error).message)); }
    finally { importInput.value = ""; }
  });
  importLabel.append(importInput);
  const manual = button(displayLang === "ja" ? "＋ 手動候補" : "+ Manual candidate", "button");
  manual.addEventListener("click", () => setRoute({ view: "manual-candidate" }));
  const clearAll = button(displayLang === "ja" ? "レビュー状態を消去" : "Clear review state", "text-button");
  clearAll.addEventListener("click", () => {
    if (confirm(displayLang === "ja" ? "この候補・改訂案セットのローカルレビュー状態を消去しますか？" : "Clear local review state for this candidate/revision set?")) {
      registrationReviewState = { decisions: {}, manual_candidates: [], revision_candidates: [] };
      saveRegistrationReviewState();
      render();
    }
  });
  toolbar.append(next, exportButton, importLabel, manual, clearAll);
  section.append(toolbar);

  const filters = el("div", "candidate-filters");
  const queryLabel = el("label", "candidate-filter");
  queryLabel.append(el("span", "candidate-filter-label", displayLang === "ja" ? "レビュー内検索" : "Filter review pool"));
  const queryInput = textInput();
  queryInput.placeholder = displayLang === "ja" ? "タイトル・role・問い・path" : "Title, role, question, path";
  queryLabel.append(queryInput);
  filters.append(queryLabel);
  const makeSelect = (label: string, values: string[]) => {
    const wrap = el("label", "candidate-filter");
    wrap.append(el("span", "candidate-filter-label", label));
    const select = el("select", "candidate-select") as HTMLSelectElement;
    const all = document.createElement("option");
    all.value = "";
    all.textContent = displayLang === "ja" ? "すべて" : "All";
    select.append(all);
    for (const value of values) {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = value === "provisional"
        ? (displayLang === "ja" ? "仮登録文書" : "Provisional")
        : value === "registered_revision"
          ? (displayLang === "ja" ? "登録済み改訂案" : "Registered revision")
          : value;
      select.append(option);
    }
    wrap.append(select);
    filters.append(wrap);
    return select;
  };
  const allItems = reviewPoolItems();
  const kindSelect = makeSelect(displayLang === "ja" ? "種別" : "Kind", ["provisional", "registered_revision"]);
  const layerSelect = makeSelect(displayLang === "ja" ? "体系層" : "Layer", Array.from(new Set(allItems.map((item: JsonObject) => String(item.layer ?? "")).filter(Boolean))).sort());
  const reviewSelect = makeSelect(displayLang === "ja" ? "レビュー状態" : "Review state", ["unreviewed", "approve", "approve_with_edits", "hold", "reject"]);
  const visibilitySelect = makeSelect("visibility", Array.from(new Set(allItems.map((item: JsonObject) => String(item.visibility ?? "")).filter(Boolean))).sort());
  section.append(filters);

  const summaryLine = el("div", "candidate-result-summary");
  const grid = el("div", "candidate-grid");
  section.append(summaryLine, grid);
  const draw = () => {
    grid.replaceChildren();
    const query = queryInput.value.trim().normalize("NFKC").toLocaleLowerCase("ja-JP");
    const filtered = allItems.filter((item: JsonObject) => {
      if (kindSelect.value && item.kind !== kindSelect.value) return false;
      if (layerSelect.value && item.layer !== layerSelect.value) return false;
      if (visibilitySelect.value && item.visibility !== visibilitySelect.value) return false;
      if (reviewSelect.value && item.decision !== reviewSelect.value) return false;
      return !query || String(item.search_text ?? "").includes(query);
    });
    summaryLine.textContent = `${filtered.length} / ${allItems.length} ${displayLang === "ja" ? "レビュー項目を表示" : "review items shown"}`;
    for (const item of filtered) {
      const card = el("article", "candidate-card card");
      const meta = el("div", "doc-meta-line");
      meta.append(badge(reviewDecisionLabel(String(item.decision)), decisionTone(String(item.decision))));
      if (item.kind === "registered_revision") meta.append(badge(displayLang === "ja" ? "登録済み改訂案" : "Registered revision", "warn"));
      else meta.append(badge(displayLang === "ja" ? "仮登録文書" : "Provisional", "warn"));
      if (item.visibility) meta.append(badge(String(item.visibility)));
      card.append(meta, el("h2", "card-title", String(item.title ?? "")));
      if (item.role) card.append(el("p", "card-copy", String(item.role)));
      if ((item.questions ?? []).length) card.append(el("div", "question-line", `Q. ${String(item.questions[0])}`));
      if (item.kind === "provisional") {
        card.append(el("div", "candidate-review-hint", displayLang === "ja" ? "現在のmanifest仮登録値をレビュー" : "Review current manifest provisional metadata"));
      } else {
        card.append(el("div", "candidate-review-hint", `${displayLang === "ja" ? "改訂元" : "Source"}: ${String(item.source?.source_kind ?? "metadata_revision")}`));
      }
      card.append(el("div", "path", String(item.path ?? "")));
      const row = el("div", "card-actions");
      const inspect = button(displayLang === "ja" ? "レビューする" : "Review", "button compact-button");
      inspect.addEventListener("click", () => openReviewPoolItem(item));
      row.append(inspect);
      if (item.path && readerAllowedPaths().has(String(item.path))) row.append(readerButton(String(item.path)));
      card.append(row);
      grid.append(card);
    }
    if (!filtered.length) grid.append(el("p", "empty", displayLang === "ja" ? "条件に合うレビュー項目はありません。" : "No review item matches the filters."));
  };
  for (const control of [queryInput, kindSelect, layerSelect, reviewSelect, visibilitySelect]) {
    control.addEventListener(control === queryInput ? "input" : "change", draw);
  }
  draw();

  if ((registrationReviewState.manual_candidates ?? []).length || adHocRevisions.length) {
    const queues = el("section", "audit-panel workbench-queues");
    queues.append(el("h2", "section-title small", displayLang === "ja" ? "手動追加キュー" : "Manual additions"));
    for (const item of registrationReviewState.manual_candidates ?? []) {
      const row = el("div", "queue-row");
      const label = el("div", "queue-line", `MANUAL · ${String(item.proposed?.path ?? item.proposed?.doc_id ?? "")}`);
      label.prepend(badge(reviewDecisionLabel(String(item.decision ?? "hold")), decisionTone(String(item.decision ?? "hold"))));
      row.append(label);
      const remove = button(displayLang === "ja" ? "削除" : "Remove", "text-button");
      remove.addEventListener("click", () => {
        registrationReviewState.manual_candidates = registrationReviewState.manual_candidates.filter((entry: JsonObject) => entry.id !== item.id);
        saveRegistrationReviewState();
        render();
      });
      row.append(remove);
      queues.append(row);
    }
    for (const item of adHocRevisions) {
      const row = el("div", "queue-row");
      const label = el("div", "queue-line", `REVISION · ${String(item.path ?? item.doc_id ?? "")}`);
      label.prepend(badge(reviewDecisionLabel(String(item.decision ?? "hold")), decisionTone(String(item.decision ?? "hold"))));
      row.append(label);
      const edit = button(displayLang === "ja" ? "編集" : "Edit", "text-button");
      edit.addEventListener("click", () => setRoute({ view: "revision-candidate", revision: String(item.doc_id ?? "") }));
      row.append(edit);
      const remove = button(displayLang === "ja" ? "削除" : "Remove", "text-button");
      remove.addEventListener("click", () => {
        registrationReviewState.revision_candidates = registrationReviewState.revision_candidates.filter((entry: JsonObject) => entry.doc_id !== item.doc_id);
        saveRegistrationReviewState();
        render();
      });
      row.append(remove);
      queues.append(row);
    }
    section.append(queues);
  }
  page.append(section);
  return page;
}

function assessmentProtocolPayload(): JsonObject | null {
  return assessmentProtocols?.repository_assessment_protocols_preview ?? null;
}

function assessmentProtocolList(): JsonObject[] {
  return assessmentProtocolPayload()?.protocols ?? [];
}

function assessmentProtocolKey(protocol: JsonObject): string {
  return `${String(protocol.id ?? "")}:${String(protocol.revision ?? "")}`;
}

function selectedAssessmentProtocol(): JsonObject | null {
  const protocols = assessmentProtocolList();
  if (!protocols.length) return null;
  if (!assessmentSelectedProtocolKey) assessmentSelectedProtocolKey = assessmentProtocolKey(protocols[0]);
  return protocols.find((item: JsonObject) => assessmentProtocolKey(item) === assessmentSelectedProtocolKey) ?? protocols[0];
}

function assessmentStorageKey(): string {
  return `so:repository-assessment-lab:${String(assessmentProtocolPayload()?.source_sha256 ?? "unbound")}`;
}

function loadAssessmentLabState(): void {
  if (!isDeveloper() || !assessmentProtocolPayload()) return;
  try {
    const raw = localStorage.getItem(assessmentStorageKey());
    const parsed = raw ? JSON.parse(raw) : null;
    assessmentLabState = parsed && typeof parsed === "object"
      ? parsed
      : { run: null, source_run_sha256: "", decisions: {} };
  } catch {
    assessmentLabState = { run: null, source_run_sha256: "", decisions: {} };
  }
  assessmentLabState.decisions ??= {};
}

function saveAssessmentLabState(): void {
  if (!isDeveloper() || !assessmentProtocolPayload()) return;
  localStorage.setItem(assessmentStorageKey(), JSON.stringify(assessmentLabState));
}

async function sha256Text(text: string): Promise<string> {
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return Array.from(new Uint8Array(digest)).map((value) => value.toString(16).padStart(2, "0")).join("");
}

function downloadJsonFile(filename: string, payload: JsonObject): void {
  const text = JSON.stringify(payload, null, 2) + "\n";
  const blob = new Blob([text], { type: "application/json;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.append(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

async function fetchAssessmentTarget(path: string): Promise<JsonObject> {
  const response = await fetch(encodePath(path));
  if (!response.ok) throw new Error(`${path}: HTTP ${response.status}`);
  const content = await response.text();
  return { path, sha256: await sha256Text(content), content };
}

function assessmentOutputSchemaVersion(protocol: JsonObject): string {
  const schema = String(protocol.output_contract?.schema ?? "repository_assessment_run/0.2");
  const match = schema.match(/\/(\d+\.\d+)$/);
  return match?.[1] ?? "0.2";
}

async function buildAssessmentExecution(protocol: JsonObject, paths: string[]): Promise<JsonObject> {
  if (!paths.length) throw new Error(displayLang === "ja" ? "対象文書がありません。" : "No target documents selected.");
  const unique = Array.from(new Set(paths.map((path) => path.trim()).filter(Boolean)));
  const targets = await Promise.all(unique.map(fetchAssessmentTarget));
  return {
    repository_assessment_execution: {
      schema_version: assessmentOutputSchemaVersion(protocol),
      created_at: new Date().toISOString(),
      protocol: {
        id: String(protocol.id ?? ""),
        revision: String(protocol.revision ?? ""),
        source_sha256: String(protocol.source_sha256 ?? ""),
        prompt: String(protocol.execution_prompt ?? ""),
      },
      fixture: { targets },
      output_contract: {
        schema: String(protocol.output_contract?.schema ?? "repository_assessment_run/0.2"),
        schema_path: String(protocol.output_contract?.schema_path ?? "tools/assessment/repository_assessment_run.schema.json"),
        review_schema: String(protocol.output_contract?.review_schema ?? "repository_assessment_review/0.2"),
        preserve_protocol_binding: true,
        preserve_fixture_hashes: true,
      },
    },
  };
}

function completeAssessmentPrompt(execution: JsonObject): string {
  const payload = execution.repository_assessment_execution ?? {};
  return `${String(payload.protocol?.prompt ?? "")}\n\n【固定された実行パック】\n次のJSONを入力fixtureとして扱い、内容やprotocol metadataを書き換えずに実行してください。\n\n${JSON.stringify(execution, null, 2)}`;
}

async function copyText(value: string): Promise<void> {
  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(value);
    return;
  }
  const area = document.createElement("textarea");
  area.value = value;
  area.style.position = "fixed";
  area.style.opacity = "0";
  document.body.append(area);
  area.select();
  document.execCommand("copy");
  area.remove();
}

function assessmentRunPayload(): JsonObject | null {
  return assessmentLabState.run?.repository_assessment_run ?? null;
}

function assessmentDocuments(): JsonObject[] {
  return assessmentRunPayload()?.documents ?? [];
}

function assessmentDocument(path: string): JsonObject | undefined {
  return assessmentDocuments().find((doc: JsonObject) => String(doc.path ?? "") === path);
}

function assessmentProfileKey(path: string): string {
  return `document_profile::${path}`;
}

function assessmentRepresentativeKey(claimId: string): string {
  return `representative_claim::${claimId}`;
}

function assessmentHotspotKey(hotspotId: string): string {
  return `claim_hotspot::${hotspotId}`;
}

function assessmentReviewItemByKey(reviewKey: string): JsonObject | null {
  for (const doc of assessmentDocuments()) {
    const path = String(doc.path ?? "");
    if (reviewKey === assessmentProfileKey(path)) {
      return { review_key: reviewKey, kind: "document_profile", item_id: null, path, value: doc.document_profile ?? {} };
    }
    for (const rep of doc.representative_claims ?? []) {
      if (reviewKey === assessmentRepresentativeKey(String(rep.claim_id ?? ""))) {
        return { review_key: reviewKey, kind: "representative_claim", item_id: String(rep.claim_id ?? ""), path, value: rep };
      }
    }
    for (const hotspot of doc.claim_hotspots ?? []) {
      if (reviewKey === assessmentHotspotKey(String(hotspot.hotspot_id ?? ""))) {
        return { review_key: reviewKey, kind: "claim_hotspot", item_id: String(hotspot.hotspot_id ?? ""), path, value: hotspot };
      }
    }
  }
  return null;
}

function assessmentDecisionForKey(reviewKey: string): JsonObject | null {
  return assessmentLabState.decisions?.[reviewKey] ?? null;
}

function assessmentReviewDecision(reviewKey: string): string {
  return String(assessmentDecisionForKey(reviewKey)?.decision ?? "unreviewed");
}

function assessmentPrimaryReviewCounts(): Record<string, number> {
  const counts: Record<string, number> = { unreviewed: 0, approve: 0, approve_with_edits: 0, hold: 0, reject: 0 };
  for (const doc of assessmentDocuments()) {
    const key = assessmentProfileKey(String(doc.path ?? ""));
    const state = assessmentReviewDecision(key);
    counts[state] = (counts[state] ?? 0) + 1;
  }
  return counts;
}

function assessmentDetailReviewCount(): number {
  return Object.values(assessmentLabState.decisions ?? {}).filter((decision: any) => decision.kind !== "document_profile").length;
}

function assessmentProtocolForRun(run: JsonObject): JsonObject | null {
  const protocol = run.protocol ?? {};
  return assessmentProtocolList().find((item: JsonObject) =>
    String(item.id ?? "") === String(protocol.id ?? "") && String(item.revision ?? "") === String(protocol.revision ?? ""),
  ) ?? null;
}

function validateAssessmentRunBinding(parsed: JsonObject): JsonObject {
  const run = parsed?.repository_assessment_run;
  if (!run || String(run.schema_version ?? "") !== "0.2") {
    throw new Error("repository_assessment_run schema_version 0.2 が必要です。旧0.1 runはrevision bでは読み込みません。");
  }
  if (!String(run.run_id ?? "").trim()) throw new Error("run_id がありません。");
  const protocol = assessmentProtocolForRun(run);
  if (!protocol) throw new Error("このrunのprotocol id/revisionは現在のラボにありません。");
  if (String(run.protocol?.source_sha256 ?? "") !== String(protocol.source_sha256 ?? "")) {
    throw new Error("protocol source_sha256 が現在のprotocol revisionと一致しません。");
  }
  if (!Array.isArray(run.fixture?.targets) || !run.fixture.targets.length) throw new Error("fixture.targets がありません。");
  if (!Array.isArray(run.documents) || !run.documents.length) throw new Error("documents が配列ではありません。");
  const targetPaths = new Set<string>((run.fixture.targets ?? []).map((item: JsonObject) => String(item.path ?? "")));
  const documentPaths = new Set<string>();
  const ids = new Set<string>();
  for (const doc of run.documents) {
    const path = String(doc?.path ?? "");
    if (!path) throw new Error("path が空のdocumentがあります。");
    if (documentPaths.has(path)) throw new Error(`document path が重複しています: ${path}`);
    documentPaths.add(path);
    if (!targetPaths.has(path)) throw new Error(`fixtureにないdocumentがあります: ${path}`);
    if (!doc.document_profile?.classification) throw new Error(`${path}: document_profile.classification がありません。`);
    if (!Array.isArray(doc.representative_claims) || !doc.representative_claims.length) throw new Error(`${path}: representative_claims がありません。`);
    if (!Array.isArray(doc.claim_hotspots)) throw new Error(`${path}: claim_hotspots が配列ではありません。`);
    if (!Array.isArray(doc.nonclaim_boundaries)) throw new Error(`${path}: nonclaim_boundaries が配列ではありません。`);
    const localRepIds = new Set<string>();
    for (const rep of doc.representative_claims) {
      const id = String(rep?.claim_id ?? "");
      if (!id || ids.has(id)) throw new Error(`representative claim_id が空または重複しています: ${id}`);
      ids.add(id); localRepIds.add(id);
    }
    for (const basis of doc.document_profile?.basis_claim_ids ?? []) {
      if (!localRepIds.has(String(basis))) throw new Error(`${path}: basis_claim_idsに存在しないclaimがあります: ${String(basis)}`);
    }
    for (const hotspot of doc.claim_hotspots) {
      const id = String(hotspot?.hotspot_id ?? "");
      if (!id || ids.has(id)) throw new Error(`hotspot_id が空または重複しています: ${id}`);
      ids.add(id);
      if (String(hotspot.classification_effect ?? "") !== "local_only") throw new Error(`${id}: classification_effectはlocal_onlyである必要があります。`);
    }
  }
  if (documentPaths.size !== targetPaths.size || Array.from(targetPaths).some((path) => !documentPaths.has(path))) {
    throw new Error("fixture.targets と documents の対象集合が一致しません。");
  }
  return run;
}

async function installAssessmentRun(parsed: JsonObject, sourceText?: string): Promise<void> {
  const run = validateAssessmentRunBinding(parsed);
  const text = sourceText ?? (JSON.stringify(parsed, null, 2) + "\n");
  assessmentLabState = {
    run: parsed,
    source_run_sha256: await sha256Text(text),
    decisions: {},
  };
  assessmentSelectedProtocolKey = `${String(run.protocol?.id ?? "")}:${String(run.protocol?.revision ?? "")}`;
  assessmentTargetPaths = (run.fixture?.targets ?? []).map((item: JsonObject) => String(item.path ?? "")).filter(Boolean);
  saveAssessmentLabState();
}

async function importAssessmentRun(file: File): Promise<void> {
  const raw = await file.text();
  const text = raw.replace(/^\uFEFF/, "");
  const parsed = JSON.parse(text);
  await installAssessmentRun(parsed, text);
}

function assessmentReviewExportPayload(): JsonObject {
  const counts = assessmentPrimaryReviewCounts();
  const decisions = Object.values(assessmentLabState.decisions ?? {}).sort((a: any, b: any) =>
    String(a.path ?? "").localeCompare(String(b.path ?? ""), "en") || String(a.review_key ?? "").localeCompare(String(b.review_key ?? ""), "en"),
  );
  const total = assessmentDocuments().length;
  return {
    repository_assessment_review: {
      schema_version: "0.2",
      source_run_sha256: String(assessmentLabState.source_run_sha256 ?? ""),
      status: counts.unreviewed === 0 ? "complete" : "in_progress",
      exported_at: new Date().toISOString(),
      summary: {
        total_documents: total,
        reviewed_document_profiles: total - counts.unreviewed,
        detail_reviews: assessmentDetailReviewCount(),
        ...counts,
      },
      decisions,
    },
  };
}

function nextUnreviewedAssessmentProfile(afterPath = ""): JsonObject | undefined {
  const docs = assessmentDocuments();
  const start = Math.max(0, docs.findIndex((doc: JsonObject) => String(doc.path ?? "") === afterPath) + 1);
  return [...docs.slice(start), ...docs.slice(0, start)].find((doc: JsonObject) =>
    assessmentReviewDecision(assessmentProfileKey(String(doc.path ?? ""))) === "unreviewed",
  );
}

function assessmentDocumentSearchText(doc: JsonObject): string {
  return [
    doc.path,
    doc.document_profile?.title,
    doc.document_profile?.classification?.strength,
    doc.document_profile?.classification?.exposure,
    doc.document_profile?.rationale,
    ...(doc.representative_claims ?? []).flatMap((claim: JsonObject) => [claim.proposition, claim.rationale, claim.attribution?.represented_system, claim.attribution?.scope]),
    ...(doc.claim_hotspots ?? []).flatMap((claim: JsonObject) => [claim.proposition, claim.rationale, claim.ground?.owner, ...(claim.hotspot_reasons ?? [])]),
    ...(doc.nonclaim_boundaries ?? []).map((item: JsonObject) => item.proposition),
  ].join(" ").normalize("NFKC").toLocaleLowerCase("ja-JP");
}

function assessmentSelect(values: Array<string | null>, current: string | null, labels: Record<string, string> = {}): HTMLSelectElement {
  const select = el("select", "candidate-select") as HTMLSelectElement;
  for (const raw of values) {
    const value = raw ?? "";
    const option = document.createElement("option");
    option.value = value;
    option.textContent = labels[value] ?? (value || "—");
    option.selected = value === (current ?? "");
    select.append(option);
  }
  return select;
}

function assessmentTriStateSelect(current: boolean | null | undefined): HTMLSelectElement {
  const select = el("select", "candidate-select") as HTMLSelectElement;
  for (const [value, label] of [["", "?"], ["true", "true"], ["false", "false"]] as Array<[string, string]>) {
    const option = document.createElement("option");
    option.value = value; option.textContent = label;
    option.selected = (current == null && value === "") || (current === true && value === "true") || (current === false && value === "false");
    select.append(option);
  }
  return select;
}

function assessmentSourceRefs(value: JsonObject, path: string): HTMLElement {
  const panel = el("section", "audit-panel candidate-review-panel");
  panel.append(el("h2", "section-title small", displayLang === "ja" ? "元の本文" : "Source text"));
  const refs = value.source_refs ?? (value.source ? [value.source] : []);
  if (!refs.length) {
    panel.append(el("p", "empty", displayLang === "ja" ? "source excerptはありません。" : "No source excerpt."));
    return panel;
  }
  for (const ref of refs) {
    const row = el("div", "candidate-evidence");
    row.append(el("div", "path", `${path}:${String(ref.line_start ?? "?")}-${String(ref.line_end ?? "?")}`));
    row.append(el("p", "candidate-evidence-text", String(ref.text ?? "")));
    panel.append(row);
  }
  return panel;
}

function renderAssessmentReviewItem(reviewKey: string): HTMLElement {
  const item = assessmentReviewItemByKey(reviewKey);
  if (!item) return errorPage(`Unknown assessment review item: ${reviewKey}`);
  const page = el("main", "page");
  page.append(navBar("assessment"), dataBanner());
  const back = button(displayLang === "ja" ? "← 主張監査ラボ" : "← Claim audit lab", "back-button");
  back.addEventListener("click", () => setRoute({ view: "assessment" }));
  page.append(back);

  const existing = assessmentDecisionForKey(reviewKey);
  const baseline = deepClone(item.value ?? {});
  const working = deepClone(existing?.after ?? baseline);
  working.classification ??= {};
  working.attribution ??= {};
  working.ground ??= {};

  const kind = String(item.kind ?? "");
  const path = String(item.path ?? "");
  const title = kind === "document_profile"
    ? String(working.title ?? path)
    : String(working.proposition ?? item.item_id ?? reviewKey);

  const hero = el("section", "doc-header candidate-detail-header");
  const meta = el("div", "doc-meta-line");
  meta.append(
    badge(kind),
    badge(String(working.classification?.strength ?? "S—")),
    badge(String(working.classification?.exposure ?? "E—")),
    badge(reviewDecisionLabel(assessmentReviewDecision(reviewKey)), decisionTone(assessmentReviewDecision(reviewKey))),
  );
  if (kind !== "document_profile") meta.append(badge(String(working.attribution?.repository_commitment ?? "indeterminate")));
  hero.append(
    eyebrow(`ASSESSMENT REVIEW · ${String(item.item_id ?? "DOCUMENT PROFILE")}`),
    el("h1", "section-title", title),
    meta,
    el("div", "path", path),
  );
  page.append(hero);
  if (kind !== "document_profile") page.append(assessmentSourceRefs(working, path));

  const form = el("section", "audit-panel candidate-review-panel workbench-editor");
  form.append(
    el("h2", "section-title small", displayLang === "ja" ? "分類を確認・修正" : "Review classification"),
    el("p", "section-copy", displayLang === "ja"
      ? "runの生出力は変更しません。文書profileが第一レビュー単位です。代表主張・hotspotは必要な場合だけ個別に開きます。protocol_rule_errorは次revisionで一律再実行する候補です。"
      : "The raw run is immutable. Document profile is the primary review unit; representative claims and hotspots are reviewed only when needed. A protocol-rule error should be addressed in a new uniform revision."),
  );

  const controls: Record<string, HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement> = {};
  if (kind === "document_profile") {
    controls.title = textInput(String(working.title ?? ""));
    controls.strength = assessmentSelect([null, "S0", "S1", "S2", "S3", "S4", "S5"], working.classification?.strength ?? null);
    controls.exposure = assessmentSelect([null, "E0", "E1", "E2", "E3"], working.classification?.exposure ?? null);
    controls.basis = textArea((working.basis_claim_ids ?? []).join("\n"), 3);
    controls.rationale = textArea(String(working.rationale ?? ""), 5);
    form.append(reviewField(displayLang === "ja" ? "文書タイトル" : "Document title", controls.title));
    const classGrid = el("div", "workbench-field-grid");
    classGrid.append(reviewField("Representative S", controls.strength), reviewField("Representative E", controls.exposure));
    form.append(classGrid, reviewField("basis_claim_ids", controls.basis), reviewField(displayLang === "ja" ? "文書分類の理由" : "Profile rationale", controls.rationale));
  } else {
    controls.proposition = textArea(String(working.proposition ?? ""), 3);
    controls.role = assessmentSelect(["central_claim", "core_definition", "conclusion", "supporting_argument", "bridge", "scope_control", "other"], String(working.argument_role ?? "other"));
    controls.represented = textInput(String(working.attribution?.represented_system ?? ""));
    controls.commitment = assessmentSelect(["represented", "endorsed", "derived", "suspended", "indeterminate"], String(working.attribution?.repository_commitment ?? "indeterminate"));
    controls.responsibility = textInput(String(working.attribution?.responsibility ?? ""));
    controls.scope = textArea(String(working.attribution?.scope ?? ""), 2);
    controls.strength = assessmentSelect([null, "S0", "S1", "S2", "S3", "S4", "S5"], working.classification?.strength ?? null);
    controls.exposure = assessmentSelect([null, "E0", "E1", "E2", "E3"], working.classification?.exposure ?? null);
    controls.rationale = textArea(String(working.rationale ?? ""), 5);
    form.append(
      reviewField(displayLang === "ja" ? "命題" : "Proposition", controls.proposition),
      reviewField("argument_role", controls.role),
      reviewField("represented_system", controls.represented),
      reviewField("repository_commitment", controls.commitment),
      reviewField("responsibility", controls.responsibility),
      reviewField("scope", controls.scope),
    );
    const classGrid = el("div", "workbench-field-grid");
    classGrid.append(reviewField("Claim Strength / S", controls.strength), reviewField("Connection Exposure / E", controls.exposure));
    form.append(classGrid);
    if (kind === "claim_hotspot") {
      controls.groundOwner = textInput(String(working.ground?.owner ?? ""));
      controls.groundRelation = textInput(String(working.ground?.relation ?? ""));
      controls.hotspotReasons = textArea((working.hotspot_reasons ?? []).join("\n"), 3);
      controls.awarenessGround = assessmentTriStateSelect(working.awareness?.ground_linked);
      controls.awarenessScope = assessmentTriStateSelect(working.awareness?.scope_declared);
      controls.awarenessNonclaim = assessmentTriStateSelect(working.awareness?.nonclaim_boundary_present);
      controls.awarenessOwner = assessmentTriStateSelect(working.awareness?.owner_identified);
      const groundGrid = el("div", "workbench-field-grid");
      groundGrid.append(reviewField("ground.owner", controls.groundOwner), reviewField("ground.relation", controls.groundRelation));
      form.append(groundGrid, reviewField("hotspot_reasons", controls.hotspotReasons));
      const awarenessGrid = el("div", "workbench-field-grid");
      awarenessGrid.append(
        reviewField("awareness.ground_linked", controls.awarenessGround),
        reviewField("awareness.scope_declared", controls.awarenessScope),
        reviewField("awareness.nonclaim_boundary_present", controls.awarenessNonclaim),
        reviewField("awareness.owner_identified", controls.awarenessOwner),
      );
      form.append(awarenessGrid);
      form.append(el("p", "section-copy", displayLang === "ja" ? "hotspotのS/Eはlocal-onlyであり、文書profileへ自動昇格しません。" : "Hotspot S/E is local-only and does not automatically determine the document profile."));
    }
    form.append(reviewField(displayLang === "ja" ? "判断理由" : "Rationale", controls.rationale));
  }

  const issueTypes = ["proposition_error", "merge_error", "attribution_error", "domain_error", "commitment_error", "responsibility_error", "scope_error", "document_profile_error", "hotspot_detection_error", "strength_error", "exposure_error", "ground_owner_error", "evidence_error", "protocol_rule_error", "other"];
  const existingIssues = new Set<string>((existing?.issue_types ?? []).map((value: any) => String(value)));
  const issues = el("fieldset", "assessment-issues");
  issues.append(el("legend", "workbench-label", displayLang === "ja" ? "レビューで見つけた問題" : "Issues found in review"));
  const issueControls = new Map<string, HTMLInputElement>();
  for (const issue of issueTypes) {
    const label = el("label", "assessment-issue-option");
    const input = document.createElement("input");
    input.type = "checkbox";
    input.checked = existingIssues.has(issue);
    issueControls.set(issue, input);
    label.append(input, el("span", "", issue));
    issues.append(label);
  }
  form.append(issues);
  const note = textArea(String(existing?.reviewer_note ?? ""), 3);
  form.append(reviewField(displayLang === "ja" ? "レビュー注記" : "Reviewer note", note));

  const readAfter = (): JsonObject => {
    const after = deepClone(baseline);
    if (kind === "document_profile") {
      after.title = (controls.title as HTMLInputElement).value.trim();
      after.classification ??= {};
      after.classification.strength = (controls.strength as HTMLSelectElement).value || null;
      after.classification.exposure = (controls.exposure as HTMLSelectElement).value || null;
      after.basis_claim_ids = lines((controls.basis as HTMLTextAreaElement).value);
      after.rationale = (controls.rationale as HTMLTextAreaElement).value.trim();
      return after;
    }
    after.proposition = (controls.proposition as HTMLTextAreaElement).value.trim();
    after.argument_role = (controls.role as HTMLSelectElement).value;
    after.attribution ??= {};
    after.attribution.represented_system = (controls.represented as HTMLInputElement).value.trim();
    after.attribution.repository_commitment = (controls.commitment as HTMLSelectElement).value;
    after.attribution.responsibility = (controls.responsibility as HTMLInputElement).value.trim();
    after.attribution.scope = (controls.scope as HTMLTextAreaElement).value.trim();
    after.classification ??= {};
    after.classification.strength = (controls.strength as HTMLSelectElement).value || null;
    after.classification.exposure = (controls.exposure as HTMLSelectElement).value || null;
    after.rationale = (controls.rationale as HTMLTextAreaElement).value.trim();
    if (kind === "claim_hotspot") {
      after.ground ??= {};
      after.ground.owner = (controls.groundOwner as HTMLInputElement).value.trim();
      after.ground.relation = (controls.groundRelation as HTMLInputElement).value.trim();
      after.hotspot_reasons = lines((controls.hotspotReasons as HTMLTextAreaElement).value);
      after.awareness ??= {};
      const parseTri = (control: HTMLSelectElement): boolean | null => control.value === "true" ? true : control.value === "false" ? false : null;
      after.awareness.ground_linked = parseTri(controls.awarenessGround as HTMLSelectElement);
      after.awareness.scope_declared = parseTri(controls.awarenessScope as HTMLSelectElement);
      after.awareness.nonclaim_boundary_present = parseTri(controls.awarenessNonclaim as HTMLSelectElement);
      after.awareness.owner_identified = parseTri(controls.awarenessOwner as HTMLSelectElement);
      after.classification_effect = "local_only";
    }
    return after;
  };

  const save = (decisionKind: "approve" | "hold" | "reject"): void => {
    const after = readAfter();
    const changed = JSON.stringify(after) !== JSON.stringify(baseline);
    const decision = decisionKind === "approve" ? (changed ? "approve_with_edits" : "approve") : decisionKind;
    const selectedIssues = Array.from(issueControls.entries()).filter(([, input]) => input.checked).map(([issue]) => issue);
    assessmentLabState.decisions[reviewKey] = {
      review_key: reviewKey,
      kind,
      item_id: item.item_id ?? null,
      path,
      decision,
      issue_types: selectedIssues,
      reviewed_at: new Date().toISOString(),
      reviewer_note: note.value.trim(),
      before: baseline,
      after,
    };
    saveAssessmentLabState();
    if (decisionKind === "approve" && kind === "document_profile") {
      const next = nextUnreviewedAssessmentProfile(path);
      if (next) {
        setRoute({ view: "assessment-item", item: assessmentProfileKey(String(next.path ?? "")) });
        return;
      }
    }
    setRoute({ view: "assessment" });
  };

  const bar = el("div", "workbench-decision-bar");
  const approve = button(displayLang === "ja" ? "承認" : "Approve", "button primary");
  approve.addEventListener("click", () => save("approve"));
  const hold = button(displayLang === "ja" ? "保留" : "Hold", "button");
  hold.addEventListener("click", () => save("hold"));
  const reject = button(displayLang === "ja" ? "却下" : "Reject", "button danger-button");
  reject.addEventListener("click", () => save("reject"));
  const reset = button(displayLang === "ja" ? "未確認に戻す" : "Reset to unreviewed", "text-button");
  reset.addEventListener("click", () => {
    delete assessmentLabState.decisions[reviewKey];
    saveAssessmentLabState();
    render();
  });
  bar.append(approve, hold, reject, reset);
  form.append(bar);
  page.append(form);
  return page;
}

function assessmentClaimRow(doc: JsonObject, item: JsonObject, kind: "representative_claim" | "claim_hotspot"): HTMLElement {
  const id = kind === "representative_claim" ? String(item.claim_id ?? "") : String(item.hotspot_id ?? "");
  const reviewKey = kind === "representative_claim" ? assessmentRepresentativeKey(id) : assessmentHotspotKey(id);
  const row = el("article", `assessment-detail-row ${kind === "claim_hotspot" ? "assessment-hotspot-row" : ""}`);
  const meta = el("div", "doc-meta-line");
  meta.append(
    badge(kind === "representative_claim" ? "REP" : "HOTSPOT", kind === "claim_hotspot" ? "warn" : ""),
    badge(String(item.classification?.strength ?? "S—")),
    badge(String(item.classification?.exposure ?? "E—")),
    badge(String(item.attribution?.repository_commitment ?? "indeterminate")),
  );
  if (kind === "claim_hotspot") {
    meta.append(badge(`ground: ${String(item.ground?.owner ?? "unknown")}`));
    const awareness = item.awareness ?? {};
    const awarenessFields: Array<[string, any]> = [
      ["ground", awareness.ground_linked],
      ["scope", awareness.scope_declared],
      ["nonclaim", awareness.nonclaim_boundary_present],
      ["owner", awareness.owner_identified],
    ];
    for (const [label, state] of awarenessFields) {
      const mark = state === true ? "✓" : state === false ? "×" : "?";
      meta.append(badge(`${label}${mark}`, state === false ? "warn" : ""));
    }
  }
  row.append(meta, el("h3", "assessment-detail-title", String(item.proposition ?? id)));
  if (kind === "claim_hotspot" && item.hotspot_reasons?.length) row.append(el("p", "card-copy", (item.hotspot_reasons ?? []).join(" · ")));
  row.append(el("p", "card-copy", String(item.rationale ?? "")));
  const actions = el("div", "card-actions");
  const review = button(displayLang === "ja" ? "詳細レビュー" : "Review detail", "button compact-button");
  review.addEventListener("click", () => setRoute({ view: "assessment-item", item: reviewKey }));
  actions.append(review, badge(reviewDecisionLabel(assessmentReviewDecision(reviewKey)), decisionTone(assessmentReviewDecision(reviewKey))));
  row.append(actions);
  return row;
}

function renderAssessmentDocumentCard(doc: JsonObject): HTMLElement {
  const path = String(doc.path ?? "");
  const profile = doc.document_profile ?? {};
  const profileKey = assessmentProfileKey(path);
  const reps = doc.representative_claims ?? [];
  const hotspots = doc.claim_hotspots ?? [];
  const nonclaims = doc.nonclaim_boundaries ?? [];
  const card = el("article", "candidate-card card assessment-document-card");
  const meta = el("div", "doc-meta-line");
  meta.append(
    badge(reviewDecisionLabel(assessmentReviewDecision(profileKey)), decisionTone(assessmentReviewDecision(profileKey))),
    badge(String(profile.classification?.strength ?? "S—")),
    badge(String(profile.classification?.exposure ?? "E—")),
    badge(`${reps.length} REP`),
    badge(`${hotspots.length} HOT`, hotspots.length ? "warn" : ""),
    badge(`${nonclaims.length} NON`),
  );
  card.append(meta, el("h2", "card-title", String(profile.title ?? path)), el("div", "path", path));
  if (profile.rationale) card.append(el("p", "card-copy", String(profile.rationale)));

  const actions = el("div", "card-actions");
  const reviewProfile = button(displayLang === "ja" ? "文書分類をレビュー" : "Review document profile", "button primary compact-button");
  reviewProfile.addEventListener("click", () => setRoute({ view: "assessment-item", item: profileKey }));
  actions.append(reviewProfile);
  if (readerAllowedPaths().has(path)) actions.append(readerButton(path));
  card.append(actions);

  const repDetails = el("details", "assessment-details");
  const repSummary = el("summary", "assessment-details-summary", displayLang === "ja" ? `代表主張 ${reps.length}` : `Representative claims ${reps.length}`);
  repDetails.append(repSummary);
  for (const rep of reps) repDetails.append(assessmentClaimRow(doc, rep, "representative_claim"));
  card.append(repDetails);

  const hotspotDetails = el("details", "assessment-details");
  const hotspotSummary = el("summary", "assessment-details-summary", displayLang === "ja" ? `局所強度 / Hotspots ${hotspots.length}` : `Claim hotspots ${hotspots.length}`);
  hotspotDetails.append(hotspotSummary);
  if (hotspots.length) {
    for (const hotspot of hotspots) hotspotDetails.append(assessmentClaimRow(doc, hotspot, "claim_hotspot"));
  } else hotspotDetails.append(el("p", "empty", displayLang === "ja" ? "hotspotは検出されていません。" : "No hotspots detected."));
  card.append(hotspotDetails);

  const nonclaimDetails = el("details", "assessment-details");
  const nonclaimSummary = el("summary", "assessment-details-summary", displayLang === "ja" ? `明示的非主張 ${nonclaims.length}` : `Explicit nonclaims ${nonclaims.length}`);
  nonclaimDetails.append(nonclaimSummary);
  if (nonclaims.length) {
    for (const boundary of nonclaims) {
      const row = el("article", "assessment-detail-row assessment-nonclaim-row");
      row.append(badge("S— / E—"), el("h3", "assessment-detail-title", String(boundary.proposition ?? boundary.boundary_id ?? "")));
      const source = String(boundary.source?.text ?? "");
      if (source) row.append(el("p", "card-copy assessment-source-preview", source));
      nonclaimDetails.append(row);
    }
  } else nonclaimDetails.append(el("p", "empty", displayLang === "ja" ? "明示的非主張は抽出されていません。" : "No explicit nonclaims extracted."));
  card.append(nonclaimDetails);
  return card;
}

function renderAssessmentLab(): HTMLElement {
  const page = el("main", "page");
  page.append(navBar("assessment"), dataBanner());
  const section = el("section", "section candidate-page");
  section.append(
    eyebrow("EXPERIMENTAL ASSESSMENT LAB"),
    el("h1", "hero-title", displayLang === "ja" ? "代表主張と局所強度を分けて見る" : "Separate representative claims from local claim pressure"),
    el("p", "hero-copy", displayLang === "ja"
      ? "文書全体の主張分類と、論証途中に現れる強い局所claimを分離します。全命題を一件ずつ承認するのではなく、まず文書profileをレビューし、必要な箇所だけ代表主張・hotspotへ降ります。"
      : "Document-level classification is separated from locally strong claims inside the argument. Review the document profile first, then inspect representative claims or hotspots only when needed."),
  );

  const protocols = assessmentProtocolList();
  if (!protocols.length) {
    section.append(el("p", "error", displayLang === "ja" ? "assessment protocol previewを読み込めませんでした。" : "Assessment protocol preview is unavailable."));
    page.append(section);
    return page;
  }
  const protocol = selectedAssessmentProtocol() ?? protocols[0];
  if (!assessmentTargetPaths.length) assessmentTargetPaths = (protocol.default_targets ?? []).map((value: any) => String(value));

  const boundary = el("div", "candidate-boundary-note");
  boundary.append(badge("FROZEN PILOT", "warn"), el("span", "", String(protocol.freeze_policy?.[displayLang] ?? protocol.freeze_policy?.ja ?? "")));
  section.append(boundary);

  const setup = el("section", "audit-panel assessment-setup");
  setup.append(el("h2", "section-title small", displayLang === "ja" ? "実行条件" : "Execution fixture"));
  const protocolSelect = el("select", "candidate-select") as HTMLSelectElement;
  for (const item of protocols) {
    const option = document.createElement("option");
    option.value = assessmentProtocolKey(item);
    option.textContent = `${String(item.title_ja ?? item.id)} · ${String(item.revision ?? "")}`;
    option.selected = option.value === assessmentProtocolKey(protocol);
    protocolSelect.append(option);
  }
  protocolSelect.addEventListener("change", () => {
    assessmentSelectedProtocolKey = protocolSelect.value;
    const next = selectedAssessmentProtocol();
    assessmentTargetPaths = (next?.default_targets ?? []).map((value: any) => String(value));
    render();
  });
  setup.append(reviewField(displayLang === "ja" ? "Protocol revision" : "Protocol revision", protocolSelect));
  const targets = textArea(assessmentTargetPaths.join("\n"), Math.max(3, assessmentTargetPaths.length + 1));
  targets.addEventListener("input", () => { assessmentTargetPaths = lines(targets.value); });
  setup.append(reviewField(displayLang === "ja" ? "対象文書（1行1path）" : "Target documents (one path per line)", targets));
  setup.append(el("p", "section-copy", displayLang === "ja"
    ? `protocol hash: ${String(protocol.source_sha256 ?? "")} · output: ${String(protocol.output_contract?.schema ?? "")}`
    : `protocol hash: ${String(protocol.source_sha256 ?? "")} · output: ${String(protocol.output_contract?.schema ?? "")}`));

  const toolbar = el("div", "workbench-toolbar");
  const exportPack = button(displayLang === "ja" ? "実行パックを書き出す" : "Export execution pack", "button");
  exportPack.addEventListener("click", async () => {
    exportPack.disabled = true;
    try { downloadJsonFile("repository_assessment_execution.json", await buildAssessmentExecution(protocol, assessmentTargetPaths)); }
    catch (error) { alert(String((error as Error).message)); }
    finally { exportPack.disabled = false; }
  });
  const copyPrompt = button(displayLang === "ja" ? "プロンプトをコピー" : "Copy frozen prompt", "button");
  copyPrompt.addEventListener("click", async () => {
    copyPrompt.disabled = true;
    try {
      const execution = await buildAssessmentExecution(protocol, assessmentTargetPaths);
      await copyText(completeAssessmentPrompt(execution));
      alert(displayLang === "ja" ? "凍結実行プロンプトをコピーしました。" : "Frozen execution prompt copied.");
    } catch (error) { alert(String((error as Error).message)); }
    finally { copyPrompt.disabled = false; }
  });
  const runner = assessmentRunnerStatus?.repository_assessment_runner ?? {};
  const runButton = button(displayLang === "ja" ? "UIから実行" : "Run from UI", "button primary");
  runButton.disabled = !runner.available;
  runButton.addEventListener("click", async () => {
    runButton.disabled = true;
    const original = runButton.textContent;
    runButton.textContent = displayLang === "ja" ? "実行中…" : "Running…";
    try {
      const execution = await buildAssessmentExecution(protocol, assessmentTargetPaths);
      const response = await fetch(ASSESSMENT_RUN_URL, { method: "POST", headers: { "Content-Type": "application/json; charset=utf-8" }, body: JSON.stringify(execution) });
      const result = await response.json();
      if (!response.ok) throw new Error(String(result.error ?? `HTTP ${response.status}`));
      await installAssessmentRun(result);
      render();
    } catch (error) { alert(String((error as Error).message)); }
    finally { runButton.disabled = !runner.available; runButton.textContent = original; }
  });
  const importLabel = el("label", "button workbench-file-button", displayLang === "ja" ? "結果JSONを読み込む" : "Import run JSON");
  const importInput = document.createElement("input");
  importInput.type = "file";
  importInput.accept = "application/json,.json";
  importInput.hidden = true;
  importInput.addEventListener("change", async () => {
    const file = importInput.files?.[0];
    if (!file) return;
    try { await importAssessmentRun(file); render(); }
    catch (error) { alert(String((error as Error).message)); }
    finally { importInput.value = ""; }
  });
  importLabel.append(importInput);
  toolbar.append(exportPack, copyPrompt, runButton, importLabel);
  setup.append(toolbar);
  section.append(setup);

  const run = assessmentRunPayload();
  if (run) {
    const runProtocol = assessmentProtocolForRun(run);
    const counts = assessmentPrimaryReviewCounts();
    const docs = assessmentDocuments();
    const totalReps = docs.reduce((sum, doc) => sum + (doc.representative_claims?.length ?? 0), 0);
    const totalHotspots = docs.reduce((sum, doc) => sum + (doc.claim_hotspots?.length ?? 0), 0);
    const totalNonclaims = docs.reduce((sum, doc) => sum + (doc.nonclaim_boundaries?.length ?? 0), 0);
    const runPanel = el("section", "audit-panel assessment-run-panel");
    runPanel.append(
      el("h2", "section-title small", displayLang === "ja" ? "現在のrun" : "Current run"),
      el("p", "section-copy", `${String(runProtocol?.title_ja ?? run.protocol?.id ?? "")} · ${String(run.protocol?.revision ?? "")} · ${docs.length} documents`),
    );
    const stats = el("div", "audit-stats candidate-stats");
    stats.append(
      candidateMetric(displayLang === "ja" ? "未確認文書" : "Unreviewed docs", String(counts.unreviewed)),
      candidateMetric(displayLang === "ja" ? "代表主張" : "Representative", String(totalReps)),
      candidateMetric("Hotspots", String(totalHotspots)),
      candidateMetric(displayLang === "ja" ? "非主張" : "Nonclaims", String(totalNonclaims)),
      candidateMetric(displayLang === "ja" ? "詳細レビュー" : "Detail reviews", String(assessmentDetailReviewCount())),
    );
    runPanel.append(stats);
    const runToolbar = el("div", "workbench-toolbar");
    const next = button(displayLang === "ja" ? "次の未確認文書へ" : "Next unreviewed document", "button primary");
    next.addEventListener("click", () => {
      const doc = nextUnreviewedAssessmentProfile();
      if (doc) setRoute({ view: "assessment-item", item: assessmentProfileKey(String(doc.path ?? "")) });
    });
    const exportRun = button(displayLang === "ja" ? "生runを書き出す" : "Export raw run", "button");
    exportRun.addEventListener("click", () => downloadJsonFile("repository_assessment_run.json", assessmentLabState.run));
    const exportReview = button(displayLang === "ja" ? "レビューを書き出す" : "Export review", "button");
    exportReview.addEventListener("click", () => downloadJsonFile("repository_assessment_review.json", assessmentReviewExportPayload()));
    const clear = button(displayLang === "ja" ? "runを外す" : "Clear run", "text-button");
    clear.addEventListener("click", () => {
      if (confirm(displayLang === "ja" ? "現在のrunとブラウザ内レビュー状態を外しますか？" : "Clear the current run and browser review state?")) {
        assessmentLabState = { run: null, source_run_sha256: "", decisions: {} };
        saveAssessmentLabState();
        render();
      }
    });
    runToolbar.append(next, exportRun, exportReview, clear);
    runPanel.append(runToolbar);

    const queryLabel = el("label", "candidate-filter assessment-document-filter");
    queryLabel.append(el("span", "candidate-filter-label", displayLang === "ja" ? "文書・主張を検索" : "Filter documents and claims"));
    const query = textInput();
    query.placeholder = displayLang === "ja" ? "タイトル・path・代表主張・hotspot" : "Title, path, representative claim, hotspot";
    queryLabel.append(query);
    runPanel.append(queryLabel);

    const summary = el("div", "candidate-result-summary");
    const grid = el("div", "candidate-grid assessment-document-grid");
    runPanel.append(summary, grid);
    const draw = () => {
      grid.replaceChildren();
      const q = query.value.trim().normalize("NFKC").toLocaleLowerCase("ja-JP");
      const filtered = docs.filter((doc: JsonObject) => !q || assessmentDocumentSearchText(doc).includes(q));
      summary.textContent = `${filtered.length} / ${docs.length} documents`;
      for (const doc of filtered) grid.append(renderAssessmentDocumentCard(doc));
      if (!filtered.length) grid.append(el("p", "empty", displayLang === "ja" ? "条件に合う文書はありません。" : "No document matches the filter."));
    };
    query.addEventListener("input", draw);
    draw();
    section.append(runPanel);
  }

  const notes = el("section", "audit-panel assessment-method-note");
  notes.append(
    el("h2", "section-title small", displayLang === "ja" ? "今回の分類境界" : "Current classification boundary"),
    el("p", "section-copy", displayLang === "ja"
      ? "Representative S/Eは文書が代表して引き受ける主張を表します。Hotspot S/Eは論証内部の局所的な主張圧・外部接続を示すlocal-only値です。明示的非主張はS/E対象から除外します。"
      : "Representative S/E describes what the document itself centrally commits to. Hotspot S/E is a local-only signal for claim pressure or external connection inside the argument. Explicit nonclaims are excluded from S/E classification."),
  );
  section.append(notes);
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
    [displayLang === "ja" ? "Public catalog 文書" : "Public catalog documents", String((docsIndex.documents ?? []).length)],
    [displayLang === "ja" ? "canonical 登録文書" : "Canonical registered documents", String(docsIndex.source?.registered_documents ?? nodeCounts.get("document") ?? 0)],
    [displayLang === "ja" ? "公開仮登録文書" : "Public provisional documents", String(docsIndex.source?.provisional_documents ?? 0)],
    [displayLang === "ja" ? "観測のみdocument nodes" : "Observed-only document nodes", String(nodeCounts.get("observed_document") ?? 0)],
    [displayLang === "ja" ? "仮登録レビュー対象" : "Provisional review targets", String(candidateList().length)],
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
      el("h2", "section-title small", displayLang === "ja" ? "登録WorkBench preview" : "Registration Workbench preview"),
      el(
        "p",
        "section-copy",
        displayLang === "ja"
          ? "仮登録文書はすでにcanonical manifestに存在します。Developer Workbenchはmanifest由来のread modelを読み、人間レビュー結果だけを別transactionとして書き出します。ブラウザからmanifestを直接変更しません。"
          : "Provisional documents already exist in the canonical manifest. The Developer Workbench reads a manifest-derived read model and exports human-review decisions as a separate transaction. The browser does not write the manifest directly.",
      ),
    );
    const candidateOpen = button(displayLang === "ja" ? "登録レビューを開く" : "Open registration review", "button secondary");
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
  page.append(navBar("home"), el("p", "error", isDeveloper() ? message : readingText("unavailable")));
  return page;
}

function render(): void {
  document.title = isDeveloper() ? "Scientific Ontology | Developer Navigator" : `${readingText("brand")} | Navigator`;
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
    else if (isDeveloper() && params.get("view") === "reading-editor") content = renderReadingEditor();
    else if (isDeveloper() && params.get("view") === "candidates") content = renderCandidates(params.get("candidate") ?? "");
    else if (isDeveloper() && params.get("view") === "registered-review") content = renderRegisteredRevisionProposal(params.get("registered") ?? "");
    else if (isDeveloper() && params.get("view") === "manual-candidate") content = renderManualCandidate();
    else if (isDeveloper() && params.get("view") === "revision-candidate") content = renderRevisionCandidate(params.get("revision") ?? "");
    else if (isDeveloper() && params.get("view") === "assessment-item") content = renderAssessmentReviewItem(params.get("item") ?? "");
    else if (isDeveloper() && params.get("view") === "assessment") content = renderAssessmentLab();
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
    const registrationWorkbenchPromise: Promise<Response | null> = isDeveloper()
      ? fetch(REGISTRATION_WORKBENCH_URL).catch(() => null)
      : Promise.resolve(null);
    const assessmentProtocolsPromise: Promise<Response | null> = isDeveloper()
      ? fetch(ASSESSMENT_PROTOCOLS_URL).catch(() => null)
      : Promise.resolve(null);
    const assessmentRunnerPromise: Promise<Response | null> = isDeveloper()
      ? fetch(ASSESSMENT_RUNNER_STATUS_URL).catch(() => null)
      : Promise.resolve(null);
    const graphUrl = isDeveloper() ? DEVELOPER_GRAPH_URL : PUBLIC_GRAPH_URL;
    const [catalogResponse, graphResponse, publicContentResponse, registrationWorkbenchResponse, assessmentProtocolsResponse, assessmentRunnerResponse] = await Promise.all([
      fetch(PUBLIC_CATALOG_URL),
      fetch(graphUrl),
      fetch(PUBLIC_CONTENT_URL),
      registrationWorkbenchPromise,
      assessmentProtocolsPromise,
      assessmentRunnerPromise,
    ]);
    if (!catalogResponse.ok) throw new Error(`docs_public_catalog.json: HTTP ${catalogResponse.status}`);
    if (!graphResponse.ok) throw new Error(`${graphUrl}: HTTP ${graphResponse.status}`);
    if (!publicContentResponse.ok) throw new Error(`public-content.json: HTTP ${publicContentResponse.status}`);
    docsIndex = await catalogResponse.json();
    docsGraph = await graphResponse.json();
    publicContent = await publicContentResponse.json();
    if (isDeveloper()) loadEditorialState();
    if (isDeveloper() && registrationWorkbenchResponse?.ok) registrationWorkbench = await registrationWorkbenchResponse.json();
    else registrationWorkbench = null;
    if (isDeveloper() && assessmentProtocolsResponse?.ok) assessmentProtocols = await assessmentProtocolsResponse.json();
    else assessmentProtocols = null;
    if (isDeveloper() && assessmentRunnerResponse?.ok) assessmentRunnerStatus = await assessmentRunnerResponse.json();
    else assessmentRunnerStatus = { repository_assessment_runner: { available: false, mode: "export-import" } };
    if (isDeveloper() && registrationWorkbench) loadRegistrationReviewState();
    if (isDeveloper() && assessmentProtocols) loadAssessmentLabState();
    status.textContent = "";
    updateHeaderControls();
    render();
  } catch (error) {
    status.textContent = isDeveloper() ? String((error as Error).message) : readingText("loadFailed");
    status.className = "load-error";
  }
}

langButton.addEventListener("click", () => setLanguage(displayLang === "ja" ? "en" : "ja"));
headerMenuButton.addEventListener("click", () => setRoute({}));
headerBackButton.addEventListener("click", () => history.length > 1 ? history.back() : setRoute({}));
headerTopButton.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
headerBottomButton.addEventListener("click", () => window.scrollTo({ top: document.documentElement.scrollHeight, behavior: "smooth" }));
window.addEventListener("hashchange", render);
try {
  const saved = localStorage.getItem("scientific-ontology-reader-language:v1");
  if (saved === "ja" || saved === "en") displayLang = saved;
} catch { /* Optional reader preference. */ }
const requestedLanguage = route().get("lang");
if (requestedLanguage === "ja" || requestedLanguage === "en") displayLang = requestedLanguage;
document.documentElement.lang = displayLang;
langButton.textContent = displayLang === "ja" ? "EN" : "\u65e5\u672c\u8a9e";
updateHeaderControls();
load();

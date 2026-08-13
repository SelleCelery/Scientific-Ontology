import { browsePayload, browseTopics, localizedValue, searchDocuments, } from "./search-core.js";
import { graphNodeLabel, graphNodeMap, graphSubgraph, layerSummaries, resolveGraphNode, } from "./graph-core.js";
import { collapseDocumentsForLanguage, collapseSearchResultsForLanguage, documentLanguage, preferredDocumentForLanguage, preferredPathForLanguage, presentationKeyForDocument, } from "./language-core.js";
const PUBLIC_CATALOG_URL = "../tools/docs_public_catalog.json";
const PUBLIC_GRAPH_URL = "../tools/docs_public_graph.json";
const DEVELOPER_GRAPH_URL = "../tools/docs_graph.json";
const CANDIDATES_URL = "../tools/docs_registration_candidates.preview.json";
const REGISTERED_REVIEW_URL = "../tools/docs_registered_reader_question_review.preview.json";
const PUBLIC_CONTENT_URL = "./public-content.json";
const MAX_MAP_EDGES = 24;
const interfaceMode = document.body.dataset.interface === "developer" ? "developer" : "public";
let docsIndex;
let docsGraph;
let publicContent = {};
let registrationCandidates = null;
let registeredReviewProposals = null;
let displayLang = "ja";
const app = document.querySelector("#app");
const status = document.querySelector("#data-status");
const langButton = document.querySelector("#lang-toggle");
const headerMenuButton = document.querySelector("#header-menu");
const headerBackButton = document.querySelector("#header-back");
const headerTopButton = document.querySelector("#header-top");
const headerBottomButton = document.querySelector("#header-bottom");
function el(tag, className = "", text = "") {
    const node = document.createElement(tag);
    if (className)
        node.className = className;
    if (text)
        node.textContent = text;
    return node;
}
function button(label, className = "button") {
    const node = el("button", className, label);
    node.type = "button";
    return node;
}
function encodePath(path) {
    return "../" + path.split("/").map(encodeURIComponent).join("/");
}
function isBlockedRepoPath(path) {
    const clean = path.replace(/\\/g, "/").replace(/^\/+/, "");
    return (clean.split("/").some((part) => part.startsWith("000")) ||
        clean.startsWith("99_Private_Core") ||
        clean.includes("/99_Private_Core") ||
        clean.includes("private-core") ||
        clean.includes("Private_Core") ||
        clean.includes("/Gate") ||
        clean.includes("/U5"));
}
function readerAllowedPaths() {
    const allowed = new Set();
    for (const doc of docsIndex.documents ?? []) {
        const path = String(doc.path ?? "");
        if (path.endsWith(".md") && !isBlockedRepoPath(path))
            allowed.add(path);
    }
    for (const node of docsGraph.nodes ?? []) {
        if (node.type !== "document" && node.type !== "observed_document")
            continue;
        const path = String(node.path ?? "");
        if (path.endsWith(".md") && !isBlockedRepoPath(path))
            allowed.add(path);
    }
    return allowed;
}
function normalizeRepoPath(basePath, target) {
    const raw = target.trim();
    if (!raw || raw.startsWith("#"))
        return null;
    if (/^[a-z][a-z0-9+.-]*:/i.test(raw))
        return null;
    let pathPart = raw.split("#", 1)[0].split("?", 1)[0];
    try {
        pathPart = decodeURIComponent(pathPart);
    }
    catch { /* keep original */ }
    const parts = pathPart.startsWith("/") ? [] : basePath.split("/").slice(0, -1);
    for (const part of pathPart.replace(/^\/+/, "").split("/")) {
        if (!part || part === ".")
            continue;
        if (part === "..") {
            if (!parts.length)
                return null;
            parts.pop();
        }
        else {
            parts.push(part);
        }
    }
    const resolved = parts.join("/");
    return resolved && !isBlockedRepoPath(resolved) ? resolved : null;
}
function localized(value, fallback = "") {
    return localizedValue(value, displayLang, fallback);
}
function isDeveloper() {
    return interfaceMode === "developer";
}
function publicLayerConfigs() {
    return [...(publicContent.layers ?? [])].sort((a, b) => Number(a.order ?? 999) - Number(b.order ?? 999) || String(a.id ?? "").localeCompare(String(b.id ?? ""), "en"));
}
function publicLayerConfig(layerKey) {
    return publicLayerConfigs().find((item) => String(item.id ?? "") === layerKey);
}
function publicGuides() {
    return [...(publicContent.guides ?? [])].sort((a, b) => Number(a.order ?? 999) - Number(b.order ?? 999) || String(a.id ?? "").localeCompare(String(b.id ?? ""), "en"));
}
function publicGuidePath(config) {
    const value = config.path;
    if (value && typeof value === "object")
        return String(value[displayLang] ?? value.ja ?? value.en ?? "");
    return String(value ?? "");
}
function entryLevelLabel(value) {
    const labels = {
        foundation: ["まず読む", "Start here"],
        intermediate: ["もう少し進む", "Go further"],
        advanced: ["深く読む", "Read deeply"],
    };
    const pair = labels[value];
    return pair ? pair[displayLang === "ja" ? 0 : 1] : value;
}
function relationLabel(relation) {
    const labels = {
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
function displayGraphNodeLabel(node) {
    if (!isDeveloper() && node.type === "layer") {
        const config = publicLayerConfig(String(node.key ?? ""));
        if (config)
            return localized(config.label, String(node.key ?? ""));
    }
    if (node.type === "document" || node.type === "observed_document") {
        const doc = docByPath(String(node.path ?? ""));
        if (doc)
            return titleForDoc(preferredDoc(doc));
    }
    return graphNodeLabel(node, displayLang);
}
function nodeTypeLabel(type) {
    const labels = {
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
function provenanceLabel(type) {
    const labels = {
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
function matchFieldLabel(field) {
    const base = field.split(".", 1)[0];
    const labels = {
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
function matchMethodLabel(method) {
    const labels = {
        exact: ["完全一致", "exact match"],
        contains: ["部分一致", "contains"],
        term_coverage: ["語のまとまり", "term coverage"],
        query_expansion: ["検索上の関連表現", "search-only expansion"],
        char_ngram: ["文字列の近さ", "character similarity"],
    };
    const pair = labels[method];
    return pair ? pair[displayLang === "ja" ? 0 : 1] : method.replaceAll("_", " ");
}
function setRoute(values) {
    const params = new URLSearchParams();
    for (const [key, value] of Object.entries(values))
        if (value)
            params.set(key, value);
    location.hash = params.toString();
}
function route() {
    return new URLSearchParams(location.hash.replace(/^#/, ""));
}
function updateHeaderControls() {
    headerMenuButton.textContent = displayLang === "ja" ? "メニュー" : "Menu";
    headerBackButton.textContent = displayLang === "ja" ? "← 戻る" : "← Back";
    headerTopButton.textContent = displayLang === "ja" ? "↑ 上" : "↑ Top";
    headerBottomButton.textContent = displayLang === "ja" ? "↓ 下" : "↓ Bottom";
    headerMenuButton.setAttribute("aria-label", displayLang === "ja" ? "トップメニューへ" : "Go to top menu");
    headerBackButton.setAttribute("aria-label", displayLang === "ja" ? "前の画面へ戻る" : "Go back");
    headerTopButton.setAttribute("aria-label", displayLang === "ja" ? "ページの一番上へ" : "Scroll to top");
    headerBottomButton.setAttribute("aria-label", displayLang === "ja" ? "ページの一番下へ" : "Scroll to bottom");
}
function setLanguage(lang) {
    displayLang = lang;
    langButton.textContent = lang === "ja" ? "EN" : "日本語";
    document.documentElement.lang = lang;
    updateHeaderControls();
    if (!isDeveloper() && docsIndex && docsGraph) {
        const params = route();
        let changed = false;
        const readPath = params.get("read");
        if (readPath) {
            const target = preferredPathForLanguage(readPath, allDocuments(), lang);
            if (target && target !== readPath) {
                params.set("read", target);
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
        if (changed)
            history.replaceState(null, "", `#${params.toString()}`);
    }
    render();
}
function eyebrow(text) {
    return el("div", "eyebrow", text);
}
function badge(text, tone = "") {
    return el("span", `badge ${tone}`.trim(), text);
}
function titleForDoc(doc) {
    return localized(doc.title, String(doc.id ?? doc.doc_id ?? ""));
}
function roleForDoc(doc) {
    return localized(doc.role, "");
}
function docById(docId) {
    return (docsIndex.documents ?? []).find((doc) => String(doc.id) === docId);
}
function docByPath(path) {
    return (docsIndex.documents ?? []).find((doc) => String(doc.path ?? "") === path);
}
function allDocuments() {
    return docsIndex.documents ?? [];
}
function preferredDoc(doc) {
    return isDeveloper() ? doc : preferredDocumentForLanguage(doc, allDocuments(), displayLang);
}
function preferredPath(path) {
    return isDeveloper() ? path : preferredPathForLanguage(path, allDocuments(), displayLang);
}
function preferredGraphNode(node) {
    if (isDeveloper() || (node.type !== "document" && node.type !== "observed_document"))
        return node;
    const path = String(node.path ?? "");
    const doc = docByPath(path);
    if (!doc)
        return node;
    const target = preferredDoc(doc);
    return graphNodeByPath(String(target.path ?? "")) ?? node;
}
function preferredGraphNodeId(nodeId) {
    if (isDeveloper())
        return nodeId;
    const node = graphNodeMap(docsGraph).get(nodeId);
    return node ? String(preferredGraphNode(node).id ?? nodeId) : nodeId;
}
function graphNodeByPath(path) {
    return (docsGraph.nodes ?? []).find((node) => (node.type === "document" || node.type === "observed_document") && String(node.path ?? "") === path);
}
function candidatePayload() {
    return registrationCandidates?.registration_candidates ?? null;
}
function candidateList() {
    return candidatePayload()?.candidates ?? [];
}
function candidateByPath(path) {
    return candidateList().find((candidate) => String(candidate.path ?? "") === path);
}
function registeredReviewPayload() {
    return registeredReviewProposals?.registered_reader_question_review ?? null;
}
function registeredReviewList() {
    return registeredReviewPayload()?.documents ?? [];
}
function registeredReviewByPath(path) {
    return registeredReviewList().find((item) => String(item.path ?? "") === path);
}
function registrationStateForDoc(doc) {
    return String(doc.registration_state ?? doc.publication?.registration_state ?? "registered");
}
function isProvisionalDoc(doc) {
    return registrationStateForDoc(doc) === "provisional";
}
function languageFallbackLabel(doc) {
    if (isDeveloper())
        return "";
    const language = documentLanguage(doc);
    if (language !== "ja" && language !== "en")
        return "";
    if (language === displayLang)
        return "";
    if (doc.presentation?.counterpart_path)
        return "";
    return language === "ja" ? (displayLang === "ja" ? "日本語のみ" : "JA only") : (displayLang === "ja" ? "ENのみ" : "EN only");
}
function candidateTitle(candidate) {
    const proposed = candidate.proposed ?? {};
    const preferred = displayLang === "ja" ? proposed.title_ja : proposed.title_en;
    const fallback = displayLang === "ja" ? proposed.title_en : proposed.title_ja;
    return String(preferred || fallback || proposed.doc_id || candidate.path || "");
}
function candidateRole(candidate) {
    const proposed = candidate.proposed ?? {};
    return String((displayLang === "ja" ? proposed.role_ja : proposed.role_en) || proposed.role_ja || proposed.role_en || "");
}
function candidateQuestionList(candidate) {
    const questions = candidate.proposed?.discovery?.reader_questions ?? {};
    return (questions[displayLang] ?? questions.ja ?? questions.en ?? []).map((value) => String(value));
}
function candidateAliases(candidate) {
    const aliases = candidate.proposed?.discovery?.aliases ?? {};
    return (aliases[displayLang] ?? aliases.ja ?? aliases.en ?? []).map((value) => String(value));
}
function candidateSearchText(candidate) {
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
function readerButton(path, className = "text-button") {
    const read = button(displayLang === "ja" ? "読む" : "Read", className);
    read.addEventListener("click", () => setRoute({ read: preferredPath(path) }));
    return read;
}
function rawFileLink(path, className = "text-link") {
    const raw = el("a", className, displayLang === "ja" ? "元ファイル" : "Raw file");
    raw.href = encodePath(path);
    raw.target = "_blank";
    raw.rel = "noopener";
    return raw;
}
function graphNodeForDocument(doc) {
    doc = preferredDoc(doc);
    const direct = `doc:${doc.id}`;
    if (graphNodeMap(docsGraph).has(direct))
        return direct;
    const byPath = (docsGraph.nodes ?? []).find((node) => (node.type === "document" || node.type === "observed_document") && node.path === doc.path);
    return byPath?.id;
}
function navBar(active) {
    const nav = el("nav", "view-tabs");
    const items = isDeveloper()
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
function dataBanner() {
    const profile = String(docsIndex.source?.visibility_profile ?? "unknown");
    if (!isDeveloper()) {
        if (profile === "public")
            return el("div", "public-profile-spacer");
        const notice = el("div", "public-preview-note");
        notice.append(badge(displayLang === "ja" ? "公開準備プレビュー" : "Release-preparation preview", "warn"), el("span", "", displayLang === "ja"
            ? "登録済み文書と公開可能な仮登録候補を同じ読解面で利用しています。仮登録はcanonical登録ではなく、レビュー情報や診断情報は公開面へ出しません。"
            : "Registered and provisionally registered documents share this reading surface. Provisional entries are already in the canonical document ledger, while metadata review remains open; review/diagnostic data stays off the public surface."));
        return notice;
    }
    const wrap = el("div", "data-banner");
    wrap.append(badge(profile === "preview" ? "PREVIEW" : profile.toUpperCase(), profile === "preview" ? "warn" : ""));
    wrap.append(el("span", "data-banner-text", displayLang === "ja"
        ? "Public catalog とcanonical関係グラフをDeveloper監査面で読み込んでいます。整合性はDN-6 release gateで検証します。"
        : "Developer audit mode is using the Public catalog and canonical relation graph. DN-6 release gate verifies their consistency."));
    return wrap;
}
function searchBox(initial = "") {
    const form = el("form", "search-box");
    const input = el("input", "search-input");
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
        if (query)
            setRoute({ view: "search", q: query });
    });
    return form;
}
function publicLayerCard(config) {
    const item = el("article", "public-layer-card");
    const label = localized(config.label, String(config.id ?? ""));
    const subtitle = localized(config.subtitle, "");
    const description = localized(config.description, "");
    const top = el("div", "public-layer-card-top");
    top.append(el("span", "public-layer-code", label));
    if (subtitle)
        top.append(el("span", "public-layer-subtitle", subtitle));
    item.append(top);
    if (description)
        item.append(el("p", "public-layer-description", description));
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
function publicGuideCard(config) {
    const item = el("article", "guide-card");
    const label = localized(config.label, String(config.id ?? ""));
    const purpose = localized(config.purpose, "");
    item.append(el("div", "guide-kicker", displayLang === "ja" ? "案内文書" : "Guide"), el("h3", "guide-title", label));
    if (purpose)
        item.append(el("p", "guide-copy", purpose));
    const path = publicGuidePath(config);
    const actions = el("div", "card-actions");
    if (path && readerAllowedPaths().has(path))
        actions.append(readerButton(path, "button primary compact-button"));
    const graphNode = graphNodeByPath(path);
    if (graphNode) {
        const relations = button(displayLang === "ja" ? "関係を見る" : "Relations", "button quiet-button");
        relations.addEventListener("click", () => setRoute({ graph: String(graphNode.id) }));
        actions.append(relations);
    }
    item.append(actions);
    return item;
}
function publicQuestionEntrances() {
    const rows = [];
    for (const card of browseTopics(docsIndex)) {
        const questions = card.starter_questions?.[displayLang] ?? card.starter_questions?.ja ?? card.starter_questions?.en ?? [];
        if (questions.length)
            rows.push({ topicId: String(card.topic_id), question: String(questions[0]) });
    }
    return rows.slice(0, 8);
}
function renderPublicHome() {
    const page = el("main", "page public-home");
    page.append(navBar("home"), dataBanner());
    const home = publicContent.home ?? {};
    const hero = el("section", "public-hero");
    hero.append(eyebrow(localized(home.eyebrow, "SCIENTIFIC ONTOLOGY")), el("h1", "public-hero-title", localized(home.title, displayLang === "ja" ? "存在境界論を読む" : "Read Scientific Ontology")), el("p", "public-hero-copy", localized(home.description, "")), searchBox());
    const quick = el("div", "public-quick-questions");
    quick.append(el("span", "quick-label", displayLang === "ja" ? "問いから入る" : "Start with a question"));
    for (const row of publicQuestionEntrances().slice(0, 5)) {
        const q = button(row.question, "question-button public-question-button");
        q.addEventListener("click", () => setRoute({ view: "search", q: row.question }));
        quick.append(q);
    }
    hero.append(quick);
    page.append(hero);
    const repositoryEntry = publicGuides().find((guide) => String(guide.id ?? "") === "repository_entry");
    if (repositoryEntry) {
        const entrySection = el("section", "section guide-section");
        entrySection.append(eyebrow("START HERE"), el("h2", "section-title", displayLang === "ja"
            ? "まず、存在境界論とは何かを読む"
            : "Start with what Scientific Ontology is"), el("p", "section-copy", displayLang === "ja"
            ? "体系の層を選ぶ前に、ルートREADMEから全体の開始線、公開上の姿勢、v5系の進行方向を確認できます。"
            : "Before choosing a system layer, read the root README for the framework’s opening line, public stance, and direction of the v5 series."));
        const entryGrid = el("div", "guide-grid");
        entryGrid.append(publicGuideCard(repositoryEntry));
        entrySection.append(entryGrid);
        page.append(entrySection);
    }
    const layerSection = el("section", "section public-section");
    layerSection.append(eyebrow(displayLang === "ja" ? "READ BY LAYER" : "READ BY LAYER"), el("h2", "section-title", displayLang === "ja" ? "体系の層から読む" : "Read through the system layers"), el("p", "section-copy", displayLang === "ja"
        ? "各層のREADMEが持つ役割を短くほどき、いま読みたい場所へ直接入れるようにしています。層は重要度の順位ではなく、体系上の役割です。"
        : "Each layer README is condensed into a reader-facing entrance. Layers express roles in the system, not an importance ranking."));
    const layerGrid = el("div", "public-layer-grid");
    for (const config of publicLayerConfigs())
        layerGrid.append(publicLayerCard(config));
    layerSection.append(layerGrid);
    page.append(layerSection);
    const guideSection = el("section", "section guide-section");
    guideSection.append(eyebrow(displayLang === "ja" ? "GUIDE DOCUMENTS" : "GUIDE DOCUMENTS"), el("h2", "section-title", displayLang === "ja" ? "目的から案内文書を選ぶ" : "Choose a guide by what you need"), el("p", "section-copy", displayLang === "ja"
        ? "ファイル名ではなく、『何を知りたいときに読むか』から選べます。"
        : "Choose by what you want to understand, rather than by filename."));
    const guideGrid = el("div", "guide-grid");
    for (const guide of publicGuides()) {
        if (String(guide.id ?? "") === "repository_entry")
            continue;
        guideGrid.append(publicGuideCard(guide));
    }
    guideSection.append(guideGrid);
    page.append(guideSection);
    const topicSection = el("section", "section topic-strip-section");
    topicSection.append(eyebrow(displayLang === "ja" ? "INTERESTS" : "INTERESTS"), el("h2", "section-title", displayLang === "ja" ? "関心から寄り道する" : "Take a route through an interest"), el("p", "section-copy", displayLang === "ja"
        ? "トピックは厳密な分類ではなく、別の入口です。同じ文書が複数の関心から見つかることがあります。"
        : "Topics are alternate entrances, not strict classifications. A document can be reachable from more than one interest."));
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
function renderExplore() {
    return renderPublicHome();
}
function docCard(doc) {
    const item = el("article", `doc-card card ${isDeveloper() ? "developer-doc-card" : "public-doc-card"}`);
    const level = String(doc.entry_level ?? doc.discovery?.entry_level ?? "");
    const state = String(doc.state ?? "");
    const top = el("div", "card-meta");
    if (level)
        top.append(badge(isDeveloper() ? level : entryLevelLabel(level)));
    if (isProvisionalDoc(doc))
        top.append(badge(displayLang === "ja" ? "仮登録" : "Provisional", "warn"));
    const languageFallback = languageFallbackLabel(doc);
    if (languageFallback)
        top.append(badge(languageFallback, "warn"));
    if (isDeveloper() && state)
        top.append(badge(state, state === "public-candidate" ? "warn" : ""));
    if (top.childElementCount)
        item.append(top);
    item.append(el("h3", "card-title", titleForDoc(doc)));
    const role = roleForDoc(doc);
    if (role)
        item.append(el("p", "card-copy", role));
    const questions = doc.reader_questions ?? doc.discovery?.reader_questions ?? {};
    const qList = questions[displayLang] ?? questions.ja ?? questions.en ?? [];
    if (qList.length) {
        const question = el("div", "public-card-question");
        question.append(el("span", "question-mark", "Q"), el("span", "", String(qList[0])));
        item.append(question);
    }
    const path = String(doc.path ?? "");
    if (isDeveloper())
        item.append(el("div", "path", path));
    const actions = el("div", "card-actions");
    const id = String(doc.doc_id ?? doc.id ?? "");
    if (isDeveloper()) {
        const detail = button(displayLang === "ja" ? "文書を見る" : "Inspect document", "text-button");
        detail.addEventListener("click", () => setRoute({ doc: id }));
        actions.append(detail);
        if (path)
            actions.append(readerButton(path), rawFileLink(path));
    }
    else {
        if (path)
            actions.append(readerButton(path, "button primary compact-button"));
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
function renderTopic(topicId) {
    const page = el("main", "page");
    page.append(navBar("home"), dataBanner());
    const payload = browsePayload(docsIndex, topicId);
    const card = payload.topic;
    const back = button(displayLang === "ja" ? "← 読む" : "← Read", "back-button");
    back.addEventListener("click", () => setRoute({}));
    page.append(back);
    const hero = el("section", "topic-hero");
    hero.append(eyebrow(isDeveloper() ? `TOPIC · ${topicId}` : "TOPIC"), el("h1", "hero-title", localized(card.label, topicId)), el("p", "hero-copy", localized(card.description)));
    const questions = el("div", "starter-questions");
    questions.append(el("h2", "minor-title", displayLang === "ja" ? "この関心から始められる問い" : "Questions that can start from here"));
    for (const q of card.starter_questions?.[displayLang] ?? []) {
        const qButton = button(String(q), "question-button");
        qButton.addEventListener("click", () => setRoute({ view: "search", q: String(q) }));
        questions.append(qButton);
    }
    hero.append(questions);
    page.append(hero);
    const groups = { foundation: [], intermediate: [], advanced: [], unspecified: [] };
    const topicDocs = isDeveloper()
        ? (payload.documents ?? [])
        : collapseDocumentsForLanguage(payload.documents ?? [], allDocuments(), displayLang);
    for (const doc of topicDocs) {
        const level = String(doc.entry_level ?? doc.discovery?.entry_level ?? "");
        (groups[level] ?? groups.unspecified).push(doc);
    }
    const labels = {
        foundation: ["まず読む / 基礎", "Start / foundation"],
        intermediate: ["もう少し進む", "Go further"],
        advanced: ["深く読む", "Read deeply"],
        unspecified: ["その他", "Other"],
    };
    for (const level of ["foundation", "intermediate", "advanced", "unspecified"]) {
        if (!groups[level].length)
            continue;
        const section = el("section", "section compact-section");
        section.append(el("h2", "section-title small", labels[level][displayLang === "ja" ? 0 : 1]));
        const grid = el("div", "doc-grid");
        for (const doc of groups[level])
            grid.append(docCard(doc));
        section.append(grid);
        page.append(section);
    }
    return page;
}
function publicDocsForLayer(layerPath) {
    const normalized = layerPath.replace(/\\/g, "/").replace(/\/$/, "");
    const matched = (docsIndex.documents ?? [])
        .filter((doc) => {
        const path = String(doc.path ?? "");
        if (normalized === ".")
            return !path.includes("/");
        return path === normalized || path.startsWith(`${normalized}/`);
    });
    return collapseDocumentsForLanguage(matched, allDocuments(), displayLang)
        .slice()
        .sort((a, b) => {
        const levelOrder = { foundation: 0, intermediate: 1, advanced: 2, "": 3 };
        const aLevel = levelOrder[String(a.discovery?.entry_level ?? "")] ?? 3;
        const bLevel = levelOrder[String(b.discovery?.entry_level ?? "")] ?? 3;
        if (aLevel !== bLevel)
            return aLevel - bLevel;
        return titleForDoc(a).localeCompare(titleForDoc(b), displayLang === "ja" ? "ja" : "en");
    });
}
function renderPublicLayer(layerId) {
    const page = el("main", "page public-layer-page");
    page.append(navBar("home"), dataBanner());
    const layer = layerSummaries(docsGraph).find((row) => String(row.id) === layerId);
    if (!layer)
        return errorPage(`Unknown layer: ${layerId}`);
    const config = publicLayerConfig(String(layer.key));
    const back = button(displayLang === "ja" ? "← 体系から読む" : "← Read by layer", "back-button");
    back.addEventListener("click", () => setRoute({}));
    page.append(back);
    const hero = el("section", "public-layer-hero");
    const label = config ? localized(config.label, localized(layer.label, String(layer.key))) : localized(layer.label, String(layer.key));
    const subtitle = config ? localized(config.subtitle, "") : "";
    const description = config ? localized(config.description, "") : "";
    hero.append(eyebrow(displayLang === "ja" ? "SYSTEM LAYER" : "SYSTEM LAYER"), el("h1", "public-layer-title", label));
    if (subtitle)
        hero.append(el("p", "public-layer-lead", subtitle));
    if (description)
        hero.append(el("p", "public-layer-copy", description));
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
        const provisionalCount = layerDocs.filter((doc) => isProvisionalDoc(doc)).length;
        section.append(eyebrow(displayLang === "ja" ? "DOCUMENTS" : "DOCUMENTS"), el("h2", "section-title", displayLang === "ja" ? "この層で読む" : "Read in this layer"), el("p", "section-copy", displayLang === "ja"
            ? `登録済みと公開可能な仮登録を合わせて ${layerDocs.length} 件です。うち仮登録 ${provisionalCount} 件。仮登録もcanonical文書台帳に収録されていますが、メタデータの人間レビューは未完了です。`
            : `${layerDocs.length} registered or public-safe provisional documents are available here, including ${provisionalCount} provisional. Provisional items are canonical ledger entries whose metadata review remains open.`));
        const grid = el("div", "doc-grid");
        for (const doc of layerDocs)
            grid.append(docCard(doc));
        section.append(grid);
        page.append(section);
    }
    else {
        const empty = el("section", "section public-section");
        empty.append(el("h2", "section-title small", displayLang === "ja" ? "この層の案内から始める" : "Start with the layer guide"), el("p", "section-copy", displayLang === "ja"
            ? "この層の個別文書カードは現在整備中です。READMEから層の役割と収録内容を確認できます。"
            : "Individual document cards for this layer are still being prepared. The README explains the layer role and included materials."));
        page.append(empty);
    }
    const topicIds = new Set();
    for (const doc of layerDocs) {
        for (const topic of doc?.discovery?.topics ?? [])
            topicIds.add(String(topic));
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
function renderLayer(layerId) {
    if (!isDeveloper())
        return renderPublicLayer(layerId);
    const page = el("main", "page");
    page.append(navBar("home"), dataBanner());
    const layer = layerSummaries(docsGraph).find((row) => String(row.id) === layerId);
    if (!layer)
        return errorPage(`Unknown layer: ${layerId}`);
    const back = button(displayLang === "ja" ? "← 全体へ" : "← Overview", "back-button");
    back.addEventListener("click", () => setRoute({}));
    page.append(back);
    page.append(eyebrow(`LAYER · ${String(layer.path)}`), el("h1", "hero-title", localized(layer.label, String(layer.key))), el("p", "hero-copy", displayLang === "ja"
        ? `manifest 登録 ${layer.registered.length}件、リポジトリ上で観測のみ ${layer.observed.length}件。観測のみは検索対象資格やcanonical identityを意味しません。`
        : `${layer.registered.length} manifest-registered documents and ${layer.observed.length} repository-observed-only documents. Observed-only does not imply search eligibility or canonical identity.`));
    if (layer.registered.length) {
        const section = el("section", "section compact-section");
        section.append(el("h2", "section-title small", displayLang === "ja" ? "manifest登録文書" : "Manifest-registered documents"));
        const grid = el("div", "doc-grid");
        for (const node of layer.registered) {
            const doc = docById(String(node.key));
            if (doc)
                grid.append(docCard(doc));
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
        section.append(el("h2", "section-title small", displayLang === "ja" ? "観測された未登録文書" : "Observed unregistered documents"), el("p", "section-copy", displayLang === "ja"
            ? "ここはDN-5で可視化された監査面です。必要な文書だけ、後からmanifestへ昇格させます。"
            : "This is an audit surface exposed by DN-5. Only documents that need canonical navigation status should later be promoted into the manifest."));
        const list = el("div", "observed-list");
        for (const node of layer.observed) {
            const row = el("div", "observed-row");
            const main = el("div", "observed-main");
            const path = String(node.path ?? "");
            main.append(el("strong", "", displayGraphNodeLabel(node)), el("div", "path", path));
            const candidate = candidateByPath(path);
            if (candidate)
                main.append(badge(displayLang === "ja" ? "登録候補あり" : "Candidate available", "warn"));
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
function renderSearch(query) {
    const page = el("main", "page");
    page.append(navBar("search"), dataBanner());
    const section = el("section", "search-page");
    section.append(eyebrow("SEARCH"), el("h1", "hero-title", displayLang === "ja" ? "問い・用語から探す" : "Search by question or term"), el("p", "hero-copy", isDeveloper()
        ? displayLang === "ja"
            ? "検索は直接関連だけを順位づけします。関係グラフのcentralityやリンク数は検索スコアへ混ぜていません。"
            : "Search ranks direct relevance only. Graph centrality and link counts are not mixed into search scores."
        : displayLang === "ja"
            ? "分かっている用語でも、まだ形になっていない問いでも探せます。結果には、なぜ見つかったかを確認できる説明を残しています。"
            : "Search with a known term or with a question that is not yet fully formed. Each result keeps an explanation of why it matched."), searchBox(query));
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
    if (!isDeveloper() && !rawFound.results.length)
        rawFound = searchDocuments(query, docsIndex, "auto", 32, "both");
    const found = isDeveloper()
        ? rawFound
        : { ...rawFound, results: collapseSearchResultsForLanguage(rawFound.results, allDocuments(), displayLang, 12) };
    section.append(el("div", "search-summary", isDeveloper()
        ? `${displayLang === "ja" ? "判定モード" : "Resolved mode"}: ${found.mode} · ${found.results.length} ${displayLang === "ja" ? "件" : "results"}`
        : `${found.results.length} ${displayLang === "ja" ? "件見つかりました" : "results"}`));
    const results = el("div", "search-results");
    for (const result of found.results) {
        const card = el("article", `search-result card ${isDeveloper() ? "developer-search-result" : "public-search-result"}`);
        const heading = el("div", "result-heading");
        const headingMeta = el("div", "result-heading-meta");
        if (isProvisionalDoc(result))
            headingMeta.append(badge(displayLang === "ja" ? "仮登録" : "Provisional", "warn"));
        const languageFallback = languageFallbackLabel(result);
        if (languageFallback)
            headingMeta.append(badge(languageFallback, "warn"));
        headingMeta.append(badge(result.score.toFixed(2), "score"));
        heading.append(el("h2", "card-title", titleForDoc(result)), headingMeta);
        card.append(heading);
        const role = roleForDoc(result);
        if (role)
            card.append(el("p", "card-copy", role));
        if (isDeveloper()) {
            const reasons = el("div", "match-reasons");
            for (const match of (result.matches ?? []).slice(0, 3)) {
                const reason = el("div", "match-reason");
                reason.append(badge(String(match.field)), el("span", "", `${String(match.method)} · +${Number(match.contribution).toFixed(2)}`), el("span", "match-text", `“${String(match.text)}”`));
                reasons.append(reason);
            }
            card.append(reasons, el("div", "path", String(result.path ?? "")));
        }
        else {
            const details = el("details", "search-explanation");
            const summary = el("summary", "search-explanation-summary", displayLang === "ja" ? "なぜ見つかった？" : "Why did this match?");
            details.append(summary);
            const reasons = el("div", "public-match-reasons");
            for (const match of (result.matches ?? []).slice(0, 4)) {
                const row = el("div", "public-match-reason");
                row.append(el("span", "public-match-label", matchFieldLabel(String(match.field))), el("span", "public-match-method", `${matchMethodLabel(String(match.method))} · +${Number(match.contribution).toFixed(2)}`), el("span", "public-match-text", `“${String(match.text)}”`));
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
            if (path)
                actions.append(readerButton(path), rawFileLink(path));
        }
        else {
            if (path)
                actions.append(readerButton(path, "button primary compact-button"));
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
        results.append(el("p", "empty", displayLang === "ja"
            ? "まだ該当する文書が見つかりません。言い換えるか、読む画面から体系・案内文書を辿ってみてください。"
            : "No document matched yet. Try another phrasing or return to Read and enter through the system layers or guide documents."));
    }
    section.append(results);
    page.append(section);
    return page;
}
function renderDocument(docId) {
    const doc = docById(docId);
    if (!doc)
        return errorPage(`Unknown document: ${docId}`);
    if (!isDeveloper())
        return renderReader(String(doc.path ?? ""));
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
    if (role)
        header.append(el("p", "hero-copy", role));
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
    if (!topicWrap.childElementCount)
        topicWrap.append(el("span", "muted", displayLang === "ja" ? "未設定" : "Not set"));
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
    if (!qList.childElementCount)
        qList.append(el("li", "muted", displayLang === "ja" ? "未設定" : "Not set"));
    qPanel.append(qList);
    infoGrid.append(topicPanel, qPanel);
    page.append(infoGrid);
    const graphId = graphNodeForDocument(doc);
    if (graphId)
        page.append(relationSection(graphId));
    return page;
}
function appendInlineMarkdown(parent, text, sourcePath) {
    const token = /(!?\[[^\]]*\]\([^)]+\)|`[^`]+`|\*\*[^*]+\*\*|\*[^*]+\*)/g;
    let cursor = 0;
    for (const match of text.matchAll(token)) {
        const index = match.index ?? 0;
        if (index > cursor)
            parent.append(document.createTextNode(text.slice(cursor, index)));
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
                }
                else {
                    parent.append(document.createTextNode(alt ? `[${alt}]` : "[image]"));
                }
            }
        }
        else if (value.startsWith("[")) {
            const parsed = value.match(/^\[([^\]]+)\]\(([^)]+)\)$/);
            if (parsed) {
                const label = parsed[1];
                const href = parsed[2].trim();
                const a = document.createElement("a");
                a.textContent = label;
                if (href.startsWith("#")) {
                    a.href = href;
                }
                else if (/^(https?:|mailto:)/i.test(href)) {
                    a.href = href;
                    a.target = "_blank";
                    a.rel = "noopener noreferrer";
                }
                else {
                    const resolved = normalizeRepoPath(sourcePath, href);
                    if (resolved?.endsWith(".md") && readerAllowedPaths().has(resolved)) {
                        a.href = `#${new URLSearchParams({ read: resolved }).toString()}`;
                        a.addEventListener("click", (event) => {
                            event.preventDefault();
                            setRoute({ read: resolved });
                        });
                    }
                    else if (resolved) {
                        a.href = encodePath(resolved);
                        a.target = "_blank";
                        a.rel = "noopener";
                    }
                    else {
                        a.removeAttribute("href");
                    }
                }
                parent.append(a);
            }
        }
        else if (value.startsWith("`")) {
            parent.append(el("code", "reader-inline-code", value.slice(1, -1)));
        }
        else if (value.startsWith("**")) {
            const strong = el("strong");
            appendInlineMarkdown(strong, value.slice(2, -2), sourcePath);
            parent.append(strong);
        }
        else if (value.startsWith("*")) {
            const em = el("em");
            appendInlineMarkdown(em, value.slice(1, -1), sourcePath);
            parent.append(em);
        }
        cursor = index + value.length;
    }
    if (cursor < text.length)
        parent.append(document.createTextNode(text.slice(cursor)));
}
function markdownCells(line) {
    let value = line.trim();
    if (value.startsWith("|"))
        value = value.slice(1);
    if (value.endsWith("|"))
        value = value.slice(0, -1);
    return value.split("|").map((cell) => cell.trim());
}
function isTableSeparator(line) {
    const cells = markdownCells(line);
    return cells.length > 0 && cells.every((cell) => /^:?-{3,}:?$/.test(cell));
}
function headingId(text, seen) {
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
function renderMarkdown(text, sourcePath) {
    const article = el("article", "reader-article");
    const lines = text.replace(/\r\n?/g, "\n").split("\n");
    const headingIds = new Map();
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
            const codeLines = [];
            i += 1;
            while (i < lines.length && !/^\s*```\s*$/.test(lines[i])) {
                codeLines.push(lines[i]);
                i += 1;
            }
            if (i < lines.length)
                i += 1;
            const pre = el("pre", "reader-code");
            const code = el("code", language ? `language-${language}` : "", codeLines.join("\n"));
            pre.append(code);
            article.append(pre);
            continue;
        }
        const heading = line.match(/^(#{1,6})\s+(.+?)\s*#*\s*$/);
        if (heading) {
            const level = Math.min(6, heading[1].length);
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
            const quoteLines = [];
            while (i < lines.length && /^\s*>/.test(lines[i])) {
                quoteLines.push(lines[i].replace(/^\s*>\s?/, ""));
                i += 1;
            }
            for (const [index, quoteLine] of quoteLines.entries()) {
                if (index)
                    quote.append(document.createElement("br"));
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
                if (!current || /^\d/.test(current[1]) !== ordered)
                    break;
                const li = document.createElement("li");
                appendInlineMarkdown(li, current[2], sourcePath);
                list.append(li);
                i += 1;
            }
            article.append(list);
            continue;
        }
        const paragraphLines = [];
        while (i < lines.length && lines[i].trim()) {
            const candidate = lines[i];
            if (paragraphLines.length && (/^#{1,6}\s+/.test(candidate) ||
                /^\s*```/.test(candidate) ||
                /^\s*>/.test(candidate) ||
                /^\s*([-*+] |\d+[.)] )/.test(candidate) ||
                /^\s*(---+|\*\*\*+)\s*$/.test(candidate) ||
                (candidate.includes("|") && i + 1 < lines.length && isTableSeparator(lines[i + 1]))))
                break;
            paragraphLines.push(candidate.trim());
            i += 1;
        }
        const paragraph = el("p", "reader-paragraph");
        appendInlineMarkdown(paragraph, paragraphLines.join("\n"), sourcePath);
        article.append(paragraph);
    }
    return article;
}
async function fetchUtf8Strict(path) {
    if (!readerAllowedPaths().has(path))
        throw new Error(`Reader path is not in the public document graph: ${path}`);
    const response = await fetch(encodePath(path), { cache: "no-store" });
    if (!response.ok)
        throw new Error(`${path}: HTTP ${response.status}`);
    const bytes = await response.arrayBuffer();
    let text;
    try {
        text = new TextDecoder("utf-8", { fatal: true }).decode(bytes);
    }
    catch {
        throw new Error(displayLang === "ja"
            ? `${path}: UTF-8として厳密にデコードできません。表示で代替せず、原ファイルのバイト列を点検してください。`
            : `${path}: strict UTF-8 decoding failed. Inspect the source bytes instead of displaying a replacement-decoded document.`);
    }
    return { text, contentType: response.headers.get("content-type") ?? "" };
}
function publicRelatedDocuments(rootId, limit = 6) {
    const nodeMap = graphNodeMap(docsGraph);
    const seen = new Set();
    const rows = [];
    const edges = (docsGraph.edges ?? [])
        .filter((edge) => edge.from === rootId || edge.to === rootId)
        .sort((a, b) => String(a.relation).localeCompare(String(b.relation), "en") || String(a.from).localeCompare(String(b.from), "en") || String(a.to).localeCompare(String(b.to), "en"));
    for (const edge of edges) {
        const outgoing = edge.from === rootId;
        const otherId = String(outgoing ? edge.to : edge.from);
        if (seen.has(otherId))
            continue;
        const node = nodeMap.get(otherId);
        if (!node || (node.type !== "document" && node.type !== "observed_document"))
            continue;
        const projectedNode = preferredGraphNode(node);
        const path = String(projectedNode.path ?? "");
        if (!path || !readerAllowedPaths().has(path))
            continue;
        const projectedDoc = docByPath(path);
        const dedupeKey = projectedDoc ? presentationKeyForDocument(projectedDoc) : String(projectedNode.id ?? otherId);
        if (seen.has(dedupeKey))
            continue;
        seen.add(dedupeKey);
        rows.push({ node: projectedNode, relation: String(edge.relation), direction: outgoing ? "outgoing" : "incoming" });
        if (rows.length >= limit)
            break;
    }
    return rows;
}
function publicReaderRelatedSection(graphNode) {
    const rows = publicRelatedDocuments(String(graphNode.id));
    if (!rows.length)
        return null;
    const section = el("section", "section reader-related-section");
    section.append(eyebrow(displayLang === "ja" ? "NEXT ROUTES" : "NEXT ROUTES"), el("h2", "section-title", displayLang === "ja" ? "この文書から、次に辿れるもの" : "Where this document can lead next"), el("p", "section-copy", displayLang === "ja"
        ? "重要度順ではなく、現在のtyped relationで直接つながっている文書から表示しています。"
        : "These are direct typed-relation neighbors, not an importance ranking."));
    const grid = el("div", "reader-related-grid");
    for (const row of rows) {
        const item = el("article", "reader-related-card");
        item.append(el("div", "relation-human-label", `${row.direction === "outgoing" ? "→" : "←"} ${relationLabel(row.relation)}`), el("h3", "card-title", displayGraphNodeLabel(row.node)));
        const path = String(row.node.path ?? "");
        const doc = docByPath(path);
        const role = doc ? roleForDoc(doc) : "";
        if (role)
            item.append(el("p", "card-copy", role));
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
function renderReader(path) {
    path = preferredPath(path);
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
    }
    else {
        header.append(eyebrow(displayLang === "ja" ? "READ" : "READ"), el("h1", "reader-public-title", title));
        if (doc && isProvisionalDoc(doc)) {
            const stateLine = el("div", "reader-public-state");
            stateLine.append(badge(displayLang === "ja" ? "仮登録" : "Provisional", "warn"), el("span", "muted", displayLang === "ja" ? "canonical文書台帳に仮登録済みです。メタデータの人間レビューは未完了です。" : "This is a canonical provisional registration; metadata review remains open."));
            header.append(stateLine);
        }
        if (doc) {
            const languageFallback = languageFallbackLabel(doc);
            if (languageFallback) {
                const languageLine = el("div", "reader-public-state");
                languageLine.append(badge(languageFallback, "warn"), el("span", "muted", displayLang === "ja" ? "選択中のUI言語に対応する対訳文書がないため、この言語版を表示しています。" : "No counterpart exists for the selected UI language, so this single-language document is shown as a fallback."));
                header.append(languageLine);
            }
        }
        const role = doc ? roleForDoc(doc) : "";
        if (role)
            header.append(el("p", "reader-public-role", role));
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
    }
    else {
        actions.append(rawFileLink(path, "text-link reader-source-link"));
    }
    header.append(actions);
    page.append(header);
    if (isDeveloper()) {
        page.append(el("div", "reader-boundary-note", displayLang === "ja"
            ? "ReaderはHTTPレスポンスの文字コード推測に依存せず、受信バイト列をUTF-8として厳密に復号します。失敗時は文字化け表示へフォールバックしません。"
            : "The Reader does not rely on browser charset guessing. It strictly decodes response bytes as UTF-8 and does not fall back to replacement-decoded text."));
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
            meta.append(el("span", "muted", `Content-Type: ${contentType || "(not declared)"}`), el("span", "muted", `${new TextEncoder().encode(text).length.toLocaleString()} bytes decoded`));
            shell.replaceChildren(meta, renderMarkdown(text, path));
        }
        else {
            shell.replaceChildren(renderMarkdown(text, path));
            if (graphNode) {
                const related = publicReaderRelatedSection(graphNode);
                if (related)
                    page.append(related);
            }
        }
    })
        .catch((error) => {
        decodeState.textContent = "UTF-8 strict FAIL";
        decodeState.className = "badge danger";
        shell.replaceChildren(el("p", "error", String(error.message)));
    });
    return page;
}
function relationSection(rootId) {
    const section = el("section", "section relation-section");
    section.append(eyebrow(isDeveloper() ? "TYPED RELATION GRAPH" : (displayLang === "ja" ? "RELATIONS" : "RELATIONS")), el("h2", "section-title", displayLang === "ja" ? "この文書のつながり" : "Connections from this document"));
    section.append(el("p", "section-copy", isDeveloper()
        ? displayLang === "ja"
            ? "線は重要度ではなく、実際に抽出されたtyped relationです。辺を支えるsourceは下の一覧で確認できます。"
            : "Lines are extracted typed relations, not importance scores. Provenance for each edge is listed below."
        : displayLang === "ja"
            ? "線は重要度ではなく、文書台帳・用語集・体系図・本文リンクなどから現在確認できる関係です。"
            : "Lines are current typed relations observed from the document ledger, glossary, system maps, and Markdown links; they are not importance scores."));
    const map = relationMap(rootId);
    section.append(map);
    const full = button(displayLang === "ja" ? "関係マップで広げる" : "Open the relation map", "button secondary");
    full.addEventListener("click", () => setRoute({ graph: preferredGraphNodeId(rootId) }));
    section.append(full);
    return section;
}
function relationMap(rootId) {
    rootId = preferredGraphNodeId(rootId);
    const payload = graphSubgraph(docsGraph, rootId, 1);
    const nodeMap = new Map((payload.nodes ?? []).map((node) => [String(node.id), node]));
    const root = nodeMap.get(rootId);
    const wrapper = el("div", "relation-map-wrap");
    if (!root) {
        wrapper.append(el("p", "empty", displayLang === "ja" ? "グラフノードがありません。" : "Graph node not found."));
        return wrapper;
    }
    let edges = (payload.edges ?? []).filter((edge) => edge.from === rootId || edge.to === rootId);
    edges = edges.sort((a, b) => String(a.relation).localeCompare(String(b.relation), "en") || String(a.from).localeCompare(String(b.from), "en") || String(a.to).localeCompare(String(b.to), "en"));
    if (!isDeveloper()) {
        const seen = new Set();
        edges = edges.flatMap((edge) => {
            const outgoing = edge.from === rootId;
            const otherId = String(outgoing ? edge.to : edge.from);
            const other = nodeMap.get(otherId) ?? graphNodeMap(docsGraph).get(otherId);
            if (!other)
                return [];
            const projected = preferredGraphNode(other);
            let logicalKey = String(projected.id ?? otherId);
            if (projected.type === "document" || projected.type === "observed_document") {
                const projectedDoc = docByPath(String(projected.path ?? ""));
                if (projectedDoc)
                    logicalKey = presentationKeyForDocument(projectedDoc);
            }
            const key = `${outgoing ? "out" : "in"}|${String(edge.relation)}|${logicalKey}`;
            if (seen.has(key))
                return [];
            seen.add(key);
            return [{ ...edge, display_other_id: String(projected.id ?? otherId) }];
        });
    }
    const clipped = edges.slice(0, MAX_MAP_EDGES);
    const incoming = clipped.filter((edge) => edge.to === rootId);
    const outgoing = clipped.filter((edge) => edge.from === rootId);
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
    incoming.forEach((edge, index) => {
        const nodeId = String(edge.display_other_id ?? edge.from);
        const node = nodeMap.get(nodeId) ?? graphNodeMap(docsGraph).get(nodeId);
        if (!node)
            return;
        const y = 70 + index * 74;
        drawEdge(svg, 300, y, 420, center.y, String(edge.relation), "incoming");
        drawGraphNode(svg, node, 180, y, false);
    });
    outgoing.forEach((edge, index) => {
        const nodeId = String(edge.display_other_id ?? edge.to);
        const node = nodeMap.get(nodeId) ?? graphNodeMap(docsGraph).get(nodeId);
        if (!node)
            return;
        const y = 70 + index * 74;
        drawEdge(svg, 580, center.y, 700, y, String(edge.relation), "outgoing");
        drawGraphNode(svg, node, 820, y, false);
    });
    wrapper.append(svg);
    if (edges.length > MAX_MAP_EDGES) {
        wrapper.append(el("p", "map-note", displayLang === "ja"
            ? `図では安定順の先頭${MAX_MAP_EDGES}辺を表示。全${edges.length}辺は下のrelation listに保持しています。`
            : `The map shows the first ${MAX_MAP_EDGES} edges in stable order. All ${edges.length} edges remain in the relation list below.`));
    }
    const list = el("div", "relation-list");
    for (const edge of edges) {
        const outgoingEdge = edge.from === rootId;
        const otherId = String(edge.display_other_id ?? (outgoingEdge ? edge.to : edge.from));
        const other = nodeMap.get(otherId) ?? graphNodeMap(docsGraph).get(otherId);
        if (!other)
            continue;
        const row = el("button", "relation-row");
        row.type = "button";
        row.addEventListener("click", () => setRoute({ graph: preferredGraphNodeId(otherId) }));
        const direction = el("span", "relation-direction", outgoingEdge ? "→" : "←");
        const rel = el("span", "relation-type", isDeveloper() ? String(edge.relation) : relationLabel(String(edge.relation)));
        const label = el("span", "relation-target", displayGraphNodeLabel(other));
        const provTypes = Array.from(new Set((edge.provenance ?? []).map((p) => String(p.source_type ?? "")).filter(Boolean))).map((value) => isDeveloper() ? value : provenanceLabel(value)).join(" + ");
        const prov = el("span", "relation-provenance", provTypes || "—");
        row.append(direction, rel, label, prov);
        list.append(row);
    }
    wrapper.append(list);
    return wrapper;
}
function truncate(value, max = 28) {
    return value.length <= max ? value : `${value.slice(0, max - 1)}…`;
}
function drawGraphNode(svg, node, x, y, root) {
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
            if (event.key === "Enter" || event.key === " ")
                activate();
        });
    }
    svg.append(group);
}
function drawEdge(svg, x1, y1, x2, y2, relation, direction) {
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
function renderRelations(nodeQuery = "") {
    const page = el("main", "page");
    page.append(navBar("relations"), dataBanner());
    const section = el("section", "section relation-page");
    section.append(eyebrow(isDeveloper() ? "TYPED RELATION GRAPH" : "RELATION MAP"), el("h1", "hero-title", displayLang === "ja" ? "関係から読む" : "Read through relations"), el("p", "hero-copy", isDeveloper()
        ? displayLang === "ja"
            ? "文書・概念・トピック・Glossary語・体系層をノードとして、宣言関係と観測リンクを区別したまま辿ります。"
            : "Traverse documents, concepts, topics, glossary terms, and system layers while preserving the distinction between declared relations and observed links."
        : displayLang === "ja"
            ? "文書、概念、用語、トピック、体系層がどこでつながっているかを、関係の向きを保ったまま辿れます。線の多さは重要度を意味しません。"
            : "Follow how documents, concepts, terms, topics, and system layers connect while preserving relation direction. More lines do not mean greater importance."));
    const form = el("form", "graph-search");
    const input = el("input", "search-input");
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
        if (!value)
            return;
        try {
            setRoute({ graph: resolveGraphNode(docsGraph, value) });
        }
        catch (error) {
            alert(String(error.message));
        }
    });
    section.append(form);
    if (!isDeveloper()) {
        const legend = el("div", "relation-legend");
        const relations = ["owns", "imports", "returns_to", "placed_in", "belongs_to_topic", "links_to"];
        for (const relation of relations)
            legend.append(el("span", "relation-legend-item", relationLabel(relation)));
        section.append(legend);
    }
    if (nodeQuery) {
        try {
            const rootId = preferredGraphNodeId(resolveGraphNode(docsGraph, nodeQuery));
            const root = graphNodeMap(docsGraph).get(rootId);
            const current = el("div", "graph-current");
            current.append(el("h2", "section-title small", displayGraphNodeLabel(root)), badge(isDeveloper() ? String(root.type) : nodeTypeLabel(String(root.type))));
            const rootPath = String(root.path ?? "");
            const rootDoc = rootPath ? docByPath(rootPath) : undefined;
            if (rootDoc && isProvisionalDoc(rootDoc))
                current.append(badge(displayLang === "ja" ? "仮登録" : "Provisional", "warn"));
            if (isDeveloper())
                current.append(el("div", "path", String(root.path ?? root.id)));
            if ((root.type === "document" || root.type === "observed_document") && readerAllowedPaths().has(rootPath)) {
                current.append(readerButton(rootPath, isDeveloper() ? "text-button" : "button quiet-button"));
            }
            section.append(current, relationMap(rootId));
        }
        catch (error) {
            section.append(el("p", "error", String(error.message)));
        }
    }
    else {
        const starters = el("div", "starter-node-grid public-relation-starters");
        const seeds = ["doc:scientific_ontology_concept_network", "doc:meaning_generation_model", "topic:ai", "layer:sat_truth"];
        for (const id of seeds) {
            const node = graphNodeMap(docsGraph).get(id);
            if (!node)
                continue;
            const b = button(displayGraphNodeLabel(node), "starter-node");
            b.addEventListener("click", () => setRoute({ graph: preferredGraphNodeId(id) }));
            starters.append(b);
        }
        section.append(el("h2", "minor-title", displayLang === "ja" ? "例から開く" : "Open an example"), starters);
    }
    page.append(section);
    return page;
}
const REVIEW_STORAGE_PREFIX = "scientific-ontology-registration-review:";
let registrationReviewState = { decisions: {}, manual_candidates: [], revision_candidates: [] };
function deepClone(value) {
    return JSON.parse(JSON.stringify(value));
}
function reviewStorageKey() {
    const candidateHash = String(candidatePayload()?.source?.candidate_source_sha256 ?? "unbound");
    const revisionHash = String(registeredReviewPayload()?.source?.review_seed_sha256 ?? "no-registered-seed");
    return `${REVIEW_STORAGE_PREFIX}${candidateHash}:${revisionHash}`;
}
function loadRegistrationReviewState() {
    if (!isDeveloper() || !candidatePayload())
        return;
    try {
        const raw = localStorage.getItem(reviewStorageKey());
        const parsed = raw ? JSON.parse(raw) : null;
        registrationReviewState = parsed && typeof parsed === "object"
            ? parsed
            : { decisions: {}, manual_candidates: [], revision_candidates: [] };
    }
    catch {
        registrationReviewState = { decisions: {}, manual_candidates: [], revision_candidates: [] };
    }
    registrationReviewState.decisions ??= {};
    registrationReviewState.manual_candidates ??= [];
    registrationReviewState.revision_candidates ??= [];
}
function saveRegistrationReviewState() {
    if (!isDeveloper() || !candidatePayload())
        return;
    localStorage.setItem(reviewStorageKey(), JSON.stringify(registrationReviewState));
}
function decisionForCandidate(candidate) {
    return registrationReviewState.decisions?.[String(candidate.path ?? "")] ?? null;
}
function revisionStateByPath(path) {
    return (registrationReviewState.revision_candidates ?? []).find((item) => String(item.path ?? "") === path) ?? null;
}
function decisionForRegisteredReview(item) {
    return String(revisionStateByPath(String(item.path ?? ""))?.decision ?? "unreviewed");
}
function reviewDecisionLabel(value) {
    const labels = {
        approve: ["承認", "Approved"],
        approve_with_edits: ["修正承認", "Approved with edits"],
        hold: ["保留", "On hold"],
        reject: ["却下", "Rejected"],
        unreviewed: ["未確認", "Unreviewed"],
    };
    const pair = labels[value] ?? [value, value];
    return pair[displayLang === "ja" ? 0 : 1];
}
function decisionTone(value) {
    if (value === "approve" || value === "approve_with_edits")
        return "ok";
    if (value === "hold")
        return "warn";
    if (value === "reject")
        return "danger";
    return "";
}
function decisionCounts() {
    const counts = { unreviewed: 0, approve: 0, approve_with_edits: 0, hold: 0, reject: 0 };
    for (const candidate of candidateList()) {
        const decision = decisionForCandidate(candidate);
        const key = String(decision?.decision ?? "unreviewed");
        counts[key] = (counts[key] ?? 0) + 1;
    }
    return counts;
}
function registeredReviewDecisionCounts() {
    const counts = { unreviewed: 0, approve: 0, approve_with_edits: 0, hold: 0, reject: 0 };
    for (const item of registeredReviewList()) {
        const key = decisionForRegisteredReview(item);
        counts[key] = (counts[key] ?? 0) + 1;
    }
    return counts;
}
function combinedReviewCounts() {
    const left = decisionCounts();
    const right = registeredReviewDecisionCounts();
    const result = {};
    for (const key of new Set([...Object.keys(left), ...Object.keys(right)]))
        result[key] = (left[key] ?? 0) + (right[key] ?? 0);
    return result;
}
function reviewExportPayload() {
    const source = candidatePayload()?.source ?? {};
    const registeredSource = registeredReviewPayload()?.source ?? {};
    const decisions = Object.values(registrationReviewState.decisions ?? {}).sort((a, b) => String(a.path ?? "").localeCompare(String(b.path ?? ""), "en"));
    const counts = combinedReviewCounts();
    const provisionalCounts = decisionCounts();
    const registeredCounts = registeredReviewDecisionCounts();
    const totalReviewItems = candidateList().length + registeredReviewList().length;
    return {
        registration_review: {
            schema_version: "0.2",
            status: counts.unreviewed === 0 ? "complete" : "in_progress",
            exported_at: new Date().toISOString(),
            source: {
                candidate_source_sha256: String(source.candidate_source_sha256 ?? ""),
                manifest_sha256: String(source.manifest_sha256 ?? ""),
                graph_sha256: String(source.graph_sha256 ?? ""),
                candidate_count: candidateList().length,
                registered_review_seed_sha256: String(registeredSource.review_seed_sha256 ?? ""),
                registered_review_seed_count: registeredReviewList().length,
            },
            summary: {
                total_review_items: totalReviewItems,
                reviewed: totalReviewItems - counts.unreviewed,
                ...counts,
                provisional_candidates: candidateList().length,
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
function downloadReviewExport() {
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
async function importReviewExport(file) {
    const text = await file.text();
    const parsed = JSON.parse(text);
    const payload = parsed?.registration_review;
    if (!payload || !["0.1", "0.2"].includes(String(payload.schema_version ?? ""))) {
        throw new Error("registration_review schema_version 0.1 または 0.2 が必要です。");
    }
    const current = candidatePayload()?.source ?? {};
    for (const key of ["candidate_source_sha256", "manifest_sha256", "graph_sha256"]) {
        if (String(payload.source?.[key] ?? "") !== String(current[key] ?? "")) {
            throw new Error(`古いレビューです: ${key} が現在の候補セットと一致しません。`);
        }
    }
    if (String(payload.schema_version) === "0.2") {
        const registeredSource = registeredReviewPayload()?.source ?? {};
        if (String(payload.source?.registered_review_seed_sha256 ?? "") !== String(registeredSource.review_seed_sha256 ?? "")) {
            throw new Error("古いレビューです: registered review seed が現在の改訂案と一致しません。");
        }
    }
    const decisions = {};
    for (const item of payload.decisions ?? []) {
        const path = String(item.path ?? "");
        if (!path || !candidateByPath(path))
            throw new Error(`現在の候補セットに存在しないdecisionです: ${path}`);
        decisions[path] = item;
    }
    registrationReviewState = {
        decisions,
        manual_candidates: Array.isArray(payload.manual_candidates) ? payload.manual_candidates : [],
        revision_candidates: Array.isArray(payload.revision_candidates) ? payload.revision_candidates : [],
    };
    saveRegistrationReviewState();
}
function reviewPoolItems() {
    const items = [];
    for (const candidate of candidateList()) {
        items.push({
            kind: "provisional",
            key: `provisional:${String(candidate.path ?? "")}`,
            path: String(candidate.path ?? ""),
            layer: String(candidate.proposed?.layer ?? ""),
            confidence: String(candidate.review?.confidence ?? ""),
            visibility: String(candidate.navigation?.visibility ?? ""),
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
        const doc = docByPath(path);
        items.push({
            kind: "registered_revision",
            key: `registered:${path}`,
            path,
            layer: String(doc?.layer ?? ""),
            confidence: "",
            visibility: "registered",
            title: doc ? titleForDoc(doc) : path,
            role: doc ? roleForDoc(doc) : "",
            questions: (proposal.proposed?.[displayLang] ?? proposal.proposed?.ja ?? proposal.proposed?.en ?? []).map((value) => String(value)),
            decision: decisionForRegisteredReview(proposal),
            search_text: [path, doc ? titleForDoc(doc) : "", doc ? roleForDoc(doc) : "", ...(proposal.proposed?.ja ?? []), ...(proposal.proposed?.en ?? [])].join(" ").normalize("NFKC").toLocaleLowerCase("ja-JP"),
            source: proposal,
        });
    }
    return items.sort((a, b) => String(a.path).localeCompare(String(b.path), "en") || String(a.kind).localeCompare(String(b.kind), "en"));
}
function nextUnreviewedReviewItem(afterKey = "") {
    const items = reviewPoolItems();
    const start = Math.max(0, items.findIndex((item) => String(item.key) === afterKey) + 1);
    return [...items.slice(start), ...items.slice(0, start)].find((item) => String(item.decision) === "unreviewed");
}
function openReviewPoolItem(item) {
    if (item.kind === "registered_revision")
        setRoute({ view: "registered-review", registered: String(item.path) });
    else
        setRoute({ view: "candidates", candidate: String(item.path) });
}
function candidateStateBanner() {
    const payload = candidatePayload();
    const banner = el("div", "candidate-boundary-note");
    banner.append(badge("DEVELOPER WORKBENCH", "warn"));
    banner.append(el("span", "", displayLang === "ja"
        ? "仮登録候補と登録済み改訂案を同じレビュー面で扱います。途中状態はブラウザ内に保存され、ファイル出力は『レビュー結果を書き出す』を押したときだけ行います。manifestはこの画面から直接変更しません。"
        : "Provisional candidates and registered revision proposals share one review surface. In-progress state stays in the browser; a file is created only when you explicitly choose Export review. This screen does not write the manifest directly."));
    if (!payload)
        banner.append(badge(displayLang === "ja" ? "候補データ未読込" : "Candidate data unavailable", "danger"));
    return banner;
}
function candidateMetric(label, value) {
    const box = el("div", "stat-box");
    box.append(el("span", "stat-value", value), el("span", "stat-label", label));
    return box;
}
function textInput(value = "", className = "workbench-input") {
    const input = el("input", className);
    input.type = "text";
    input.value = value;
    return input;
}
function textArea(value = "", rows = 3) {
    const input = el("textarea", "workbench-textarea");
    input.value = value;
    input.rows = rows;
    return input;
}
function reviewField(label, control, hint = "") {
    const wrap = el("label", "workbench-field");
    wrap.append(el("span", "workbench-label", label), control);
    if (hint)
        wrap.append(el("span", "workbench-hint", hint));
    return wrap;
}
function lines(value) {
    return value.split(/\r?\n/).map((item) => item.trim()).filter(Boolean);
}
function commaValues(value) {
    return value.split(/[,、\n]/).map((item) => item.trim()).filter(Boolean);
}
function candidateDetail(candidate) {
    const page = el("main", "page");
    page.append(navBar("candidates"), dataBanner(), candidateStateBanner());
    const back = button(displayLang === "ja" ? "← 候補一覧" : "← Candidate list", "back-button");
    back.addEventListener("click", () => setRoute({ view: "candidates" }));
    page.append(back);
    const baseline = deepClone(candidate.proposed ?? {});
    const existing = decisionForCandidate(candidate);
    const working = deepClone(existing?.after ?? baseline);
    const discovery = working.discovery ??= {};
    discovery.aliases ??= { ja: [], en: [] };
    discovery.reader_questions ??= { ja: [], en: [] };
    discovery.topics ??= [];
    const review = candidate.review ?? {};
    const hero = el("section", "doc-header candidate-detail-header");
    const meta = el("div", "doc-meta-line");
    meta.append(badge(String(candidate.recommended_action ?? "candidate"), "warn"), badge(String(review.confidence ?? "unknown")), badge(String(candidate.navigation?.visibility ?? "unclassified")), badge(reviewDecisionLabel(String(existing?.decision ?? "unreviewed")), decisionTone(String(existing?.decision ?? "unreviewed"))));
    hero.append(eyebrow(`REGISTRATION CANDIDATE · ${String(working.doc_id ?? "")}`), el("h1", "hero-title", candidateTitle(candidate)), meta);
    const role = candidateRole(candidate);
    if (role)
        hero.append(el("p", "hero-copy", role));
    hero.append(el("div", "path", String(candidate.path ?? "")));
    const actions = el("div", "reader-actions");
    const path = String(candidate.path ?? "");
    if (path && readerAllowedPaths().has(path))
        actions.append(readerButton(path, "button primary"));
    const graphId = String(candidate.observed_node_id ?? "");
    if (graphId && graphNodeMap(docsGraph).has(graphId)) {
        const relations = button(displayLang === "ja" ? "現在の関係を見る" : "Current relations", "button secondary");
        relations.addEventListener("click", () => setRoute({ graph: graphId }));
        actions.append(relations);
    }
    hero.append(actions);
    page.append(hero);
    const needsPanel = el("section", "audit-panel candidate-review-panel");
    needsPanel.append(el("h2", "section-title small", displayLang === "ja" ? "今回、人間が見るべき点" : "Human review points"));
    const needs = (review.needs_human_judgment ?? []).map((value) => String(value));
    const needsWrap = el("div", "chip-wrap");
    for (const item of needs)
        needsWrap.append(badge(item, "warn"));
    if (!needs.length)
        needsWrap.append(el("span", "muted", displayLang === "ja" ? "追加判断項目なし" : "No additional judgment item"));
    needsPanel.append(needsWrap);
    if (candidate.notes)
        needsPanel.append(el("p", "card-copy", String(candidate.notes)));
    page.append(needsPanel);
    const form = el("section", "audit-panel candidate-review-panel workbench-editor");
    form.append(el("h2", "section-title small", displayLang === "ja" ? "登録案を確認・修正" : "Review and edit proposal"), el("p", "section-copy", displayLang === "ja"
        ? "候補値を編集できます。変更したうえで承認すると before / after の両方がreviewファイルへ残ります。"
        : "Edit candidate values here. Approval after edits records both before and after values in the review file."));
    const controls = {};
    controls.doc_id = textInput(String(working.doc_id ?? ""));
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
    const entrySelect = el("select", "candidate-select");
    for (const value of ["foundation", "intermediate", "advanced"]) {
        const option = document.createElement("option");
        option.value = value;
        option.textContent = value;
        option.selected = String(discovery.entry_level ?? "") === value;
        entrySelect.append(option);
    }
    controls.entry_level = entrySelect;
    const fieldGrid = el("div", "workbench-field-grid");
    for (const [label, key] of [
        ["doc_id", "doc_id"], [displayLang === "ja" ? "日本語タイトル" : "Japanese title", "title_ja"],
        [displayLang === "ja" ? "英語タイトル" : "English title", "title_en"], ["document_type", "document_type"],
        [displayLang === "ja" ? "体系層" : "Layer", "layer"], ["status", "status"], ["public_profile", "public_profile"], ["state", "state"],
    ])
        fieldGrid.append(reviewField(label, controls[key]));
    form.append(fieldGrid, reviewField("scope", controls.scope), reviewField("role_ja", controls.role_ja), reviewField("role_en", controls.role_en), reviewField("topics", controls.topics, displayLang === "ja" ? "カンマ区切り" : "Comma-separated"), reviewField("aliases · ja", controls.aliases_ja, displayLang === "ja" ? "1行1件" : "One per line"), reviewField("aliases · en", controls.aliases_en, displayLang === "ja" ? "1行1件" : "One per line"), reviewField("reader questions · ja", controls.questions_ja, displayLang === "ja" ? "1行1件" : "One per line"), reviewField("reader questions · en", controls.questions_en, displayLang === "ja" ? "1行1件" : "One per line"), reviewField("entry_level", controls.entry_level));
    const note = textArea(String(existing?.reviewer_note ?? ""), 2);
    form.append(reviewField(displayLang === "ja" ? "レビュー注記" : "Reviewer note", note));
    const readForm = () => {
        const after = deepClone(baseline);
        for (const key of ["doc_id", "title_ja", "title_en", "document_type", "layer", "status", "public_profile", "state", "scope", "role_ja", "role_en"]) {
            after[key] = controls[key].value.trim();
        }
        after.discovery ??= {};
        after.discovery.topics = commaValues(controls.topics.value);
        after.discovery.aliases = { ja: lines(controls.aliases_ja.value), en: lines(controls.aliases_en.value) };
        after.discovery.reader_questions = { ja: lines(controls.questions_ja.value), en: lines(controls.questions_en.value) };
        after.discovery.entry_level = controls.entry_level.value;
        return after;
    };
    const saveDecision = (kind) => {
        const after = readForm();
        const changed = JSON.stringify(after) !== JSON.stringify(baseline);
        const decision = kind === "approve" ? (changed ? "approve_with_edits" : "approve") : kind;
        registrationReviewState.decisions[String(candidate.path)] = {
            path: String(candidate.path), doc_id: String(after.doc_id ?? baseline.doc_id ?? ""), decision,
            reviewed_at: new Date().toISOString(), reviewer_note: note.value.trim(), before: baseline, after,
        };
        saveRegistrationReviewState();
        const next = nextUnreviewedReviewItem(`provisional:${String(candidate.path)}`);
        if (kind === "approve" && next)
            openReviewPoolItem(next);
        else
            render();
    };
    const decisionBar = el("div", "workbench-decision-bar");
    const approve = button(displayLang === "ja" ? "この内容で承認して次へ" : "Approve and next", "button primary");
    approve.addEventListener("click", () => saveDecision("approve"));
    const hold = button(displayLang === "ja" ? "保留" : "Hold", "button");
    hold.addEventListener("click", () => saveDecision("hold"));
    const reject = button(displayLang === "ja" ? "却下" : "Reject", "button danger-button");
    reject.addEventListener("click", () => saveDecision("reject"));
    const clear = button(displayLang === "ja" ? "この判断を未確認に戻す" : "Reset to unreviewed", "text-button");
    clear.addEventListener("click", () => { delete registrationReviewState.decisions[String(candidate.path)]; saveRegistrationReviewState(); render(); });
    decisionBar.append(approve, hold, reject, clear);
    form.append(decisionBar);
    page.append(form);
    const language = baseline.language_relation ?? {};
    if (Object.keys(language).length) {
        const languagePanel = el("section", "audit-panel candidate-review-panel");
        languagePanel.append(el("h2", "section-title small", displayLang === "ja" ? "言語関係（候補生成時）" : "Language relation (candidate baseline)"));
        for (const [label, value] of Object.entries(language)) {
            const row = el("div", "candidate-kv");
            row.append(el("span", "candidate-k", label), el("span", "candidate-v path", String(value ?? "")));
            languagePanel.append(row);
        }
        page.append(languagePanel);
    }
    const evidencePanel = el("section", "audit-panel candidate-review-panel");
    evidencePanel.append(el("h2", "section-title small", displayLang === "ja" ? "この候補の根拠" : "Evidence for this candidate"), el("p", "section-copy", displayLang === "ja"
        ? "候補生成時に参照した現在本文の箇所です。ここにない意味を補って登録案を強めてはいません。"
        : "These are locations in the current text used when generating the candidate. The proposal is not strengthened by meanings absent from this evidence."));
    const evidenceList = el("div", "candidate-evidence-list");
    for (const evidence of review.evidence ?? []) {
        const row = el("div", "candidate-evidence");
        const head = el("div", "candidate-evidence-head");
        head.append(badge(String(evidence.kind ?? "evidence")), el("span", "path", `${String(evidence.path ?? candidate.path ?? "")}:${String(evidence.line ?? "")}`));
        row.append(head, el("p", "candidate-evidence-text", String(evidence.text ?? "")));
        evidenceList.append(row);
    }
    evidencePanel.append(evidenceList);
    page.append(evidencePanel);
    return page;
}
function revisionBaselineForDoc(doc) {
    return {
        path: String(doc.path ?? ""),
        doc_id: String(doc.id ?? doc.doc_id ?? ""),
        document_type: String(doc.document_type ?? ""),
        title_ja: String(doc.title?.ja ?? ""),
        title_en: String(doc.title?.en ?? ""),
        layer: String(doc.layer ?? ""),
        status: String(doc.status ?? ""),
        state: String(doc.state ?? ""),
        scope: String(doc.scope ?? ""),
        role_ja: String(doc.role?.ja ?? ""),
        role_en: String(doc.role?.en ?? ""),
        discovery: deepClone(doc.discovery ?? {}),
    };
}
function renderRegisteredRevisionProposal(path) {
    const proposal = registeredReviewByPath(path);
    if (!proposal)
        return errorPage(`Unknown registered revision proposal: ${path}`);
    const doc = docByPath(path);
    if (!doc || isProvisionalDoc(doc))
        return errorPage(`Registered document not found for revision proposal: ${path}`);
    const page = el("main", "page");
    page.append(navBar("candidates"), dataBanner(), candidateStateBanner());
    const back = button(displayLang === "ja" ? "← レビュー一覧" : "← Review pool", "back-button");
    back.addEventListener("click", () => setRoute({ view: "candidates" }));
    page.append(back);
    const baseline = revisionBaselineForDoc(doc);
    const existing = revisionStateByPath(path);
    const working = existing?.after && Object.keys(existing.after).length ? deepClone(existing.after) : deepClone(baseline);
    working.discovery ??= {};
    working.discovery.reader_questions ??= { ja: [], en: [] };
    const proposedQuestions = proposal.proposed ?? {};
    if (!existing) {
        working.discovery.reader_questions = {
            ja: (proposedQuestions.ja ?? []).map((value) => String(value)),
            en: (proposedQuestions.en ?? []).map((value) => String(value)),
        };
    }
    const hero = el("section", "doc-header candidate-detail-header");
    const meta = el("div", "doc-meta-line");
    meta.append(badge(displayLang === "ja" ? "登録済み" : "Registered"), badge(displayLang === "ja" ? "改訂案" : "Revision proposal", "warn"), badge(reviewDecisionLabel(String(existing?.decision ?? "unreviewed")), decisionTone(String(existing?.decision ?? "unreviewed"))));
    hero.append(eyebrow(`REGISTERED REVISION · ${String(doc.id ?? "")}`), el("h1", "hero-title", titleForDoc(doc)), meta);
    const role = roleForDoc(doc);
    if (role)
        hero.append(el("p", "hero-copy", role));
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
    const panel = el("section", "audit-panel candidate-review-panel workbench-editor");
    panel.append(el("h2", "section-title small", displayLang === "ja" ? "reader questions 改訂案" : "Reader-question revision proposal"), el("p", "section-copy", displayLang === "ja"
        ? "現在のcanonical登録はそのまま維持します。この画面では登録済み文書の次回改訂案だけをレビューします。"
        : "The current canonical registration remains active. This screen reviews only a proposed future revision for the registered document."));
    const currentBox = el("div", "revision-question-columns");
    const currentPanel = el("div", "revision-question-panel");
    currentPanel.append(el("h3", "minor-title", displayLang === "ja" ? "現在値" : "Current"));
    for (const q of baseline.discovery?.reader_questions?.[displayLang] ?? [])
        currentPanel.append(el("div", "question-line", `Q. ${String(q)}`));
    if (!(baseline.discovery?.reader_questions?.[displayLang] ?? []).length)
        currentPanel.append(el("span", "muted", displayLang === "ja" ? "現在値なし" : "No current questions"));
    const proposalPanel = el("div", "revision-question-panel");
    proposalPanel.append(el("h3", "minor-title", displayLang === "ja" ? "提案値" : "Proposed"));
    for (const q of proposedQuestions[displayLang] ?? [])
        proposalPanel.append(el("div", "question-line", `Q. ${String(q)}`));
    currentBox.append(currentPanel, proposalPanel);
    panel.append(currentBox);
    const questionsJa = textArea((working.discovery.reader_questions?.ja ?? []).join("\n"), 6);
    const questionsEn = textArea((working.discovery.reader_questions?.en ?? []).join("\n"), 6);
    const note = textArea(String(existing?.reviewer_note ?? ""), 2);
    panel.append(reviewField("reader questions · ja", questionsJa, displayLang === "ja" ? "1行1件" : "One per line"), reviewField("reader questions · en", questionsEn, displayLang === "ja" ? "1行1件" : "One per line"), reviewField(displayLang === "ja" ? "レビュー注記" : "Reviewer note", note));
    const save = (decision) => {
        const after = deepClone(baseline);
        after.discovery ??= {};
        after.discovery.reader_questions = { ja: lines(questionsJa.value), en: lines(questionsEn.value) };
        const item = {
            doc_id: String(doc.id ?? ""),
            path,
            created_at: String(existing?.created_at ?? new Date().toISOString()),
            reviewed_at: new Date().toISOString(),
            reviewer_note: note.value.trim(),
            decision,
            source_kind: "registered_reader_question_seed",
            seed_source_sha256: String(registeredReviewPayload()?.source?.review_seed_sha256 ?? ""),
            before: baseline,
            after,
        };
        const others = (registrationReviewState.revision_candidates ?? []).filter((entry) => String(entry.path ?? "") !== path);
        registrationReviewState.revision_candidates = [...others, item];
        saveRegistrationReviewState();
        const next = nextUnreviewedReviewItem(`registered:${path}`);
        if (decision === "approve" && next)
            openReviewPoolItem(next);
        else
            render();
    };
    const bar = el("div", "workbench-decision-bar");
    const approve = button(displayLang === "ja" ? "この改訂案を承認して次へ" : "Approve revision and next", "button primary");
    approve.addEventListener("click", () => save("approve"));
    const hold = button(displayLang === "ja" ? "保留" : "Hold", "button");
    hold.addEventListener("click", () => save("hold"));
    const reject = button(displayLang === "ja" ? "却下" : "Reject", "button danger-button");
    reject.addEventListener("click", () => save("reject"));
    const clear = button(displayLang === "ja" ? "未確認に戻す" : "Reset to unreviewed", "text-button");
    clear.addEventListener("click", () => {
        registrationReviewState.revision_candidates = (registrationReviewState.revision_candidates ?? []).filter((entry) => String(entry.path ?? "") !== path);
        saveRegistrationReviewState();
        render();
    });
    bar.append(approve, hold, reject, clear);
    panel.append(bar);
    page.append(panel);
    return page;
}
function renderManualCandidate() {
    const page = el("main", "page");
    page.append(navBar("candidates"), dataBanner(), candidateStateBanner());
    const back = button(displayLang === "ja" ? "← 候補一覧" : "← Candidate list", "back-button");
    back.addEventListener("click", () => setRoute({ view: "candidates" }));
    page.append(back);
    const section = el("section", "audit-panel workbench-editor");
    section.append(eyebrow("MANUAL CANDIDATE"), el("h1", "section-title", displayLang === "ja" ? "候補を手動で追加" : "Create a manual candidate"));
    const fields = {
        path: textInput(), doc_id: textInput(), title_ja: textInput(), title_en: textInput(), layer: textInput(), document_type: textInput("assertion_document"),
        status: textInput(), public_profile: textInput(), scope: textArea("", 2), role_ja: textArea("", 3), role_en: textArea("", 3), topics: textInput(), questions_ja: textArea("", 3), questions_en: textArea("", 3), note: textArea("", 2),
    };
    const grid = el("div", "workbench-field-grid");
    for (const key of ["path", "doc_id", "title_ja", "title_en", "layer", "document_type", "status", "public_profile"])
        grid.append(reviewField(key, fields[key]));
    section.append(grid, reviewField("scope", fields.scope), reviewField("role_ja", fields.role_ja), reviewField("role_en", fields.role_en), reviewField("topics", fields.topics), reviewField("reader questions · ja", fields.questions_ja), reviewField("reader questions · en", fields.questions_en), reviewField(displayLang === "ja" ? "注記" : "Note", fields.note));
    const storeManual = (decision) => {
        const path = fields.path.value.trim();
        const docId = fields.doc_id.value.trim();
        if (!path || !docId) {
            alert(displayLang === "ja" ? "path と doc_id は必須です。" : "path and doc_id are required.");
            return;
        }
        const item = {
            id: `manual:${docId}:${Date.now()}`, created_at: new Date().toISOString(), reviewer_note: fields.note.value.trim(), decision,
            proposed: {
                path, doc_id: docId, title_ja: fields.title_ja.value.trim(), title_en: fields.title_en.value.trim(), layer: fields.layer.value.trim(), document_type: fields.document_type.value.trim(), status: fields.status.value.trim(), public_profile: fields.public_profile.value.trim(), state: "public-candidate", scope: fields.scope.value.trim(), role_ja: fields.role_ja.value.trim(), role_en: fields.role_en.value.trim(),
                discovery: { topics: commaValues(fields.topics.value), aliases: { ja: [], en: [] }, reader_questions: { ja: lines(fields.questions_ja.value), en: lines(fields.questions_en.value) }, entry_level: "intermediate" },
            },
        };
        registrationReviewState.manual_candidates.push(item);
        saveRegistrationReviewState();
        setRoute({ view: "candidates" });
    };
    const bar = el("div", "workbench-decision-bar");
    const approve = button(displayLang === "ja" ? "この手動候補を承認" : "Approve manual candidate", "button primary");
    approve.addEventListener("click", () => storeManual("approve"));
    const hold = button(displayLang === "ja" ? "候補として保留" : "Save on hold", "button");
    hold.addEventListener("click", () => storeManual("hold"));
    bar.append(approve, hold);
    section.append(bar);
    page.append(section);
    return page;
}
function addRevisionCandidate(doc) {
    const docId = String(doc.id ?? doc.doc_id ?? "");
    if ((registrationReviewState.revision_candidates ?? []).some((item) => String(item.doc_id) === docId)) {
        alert(displayLang === "ja" ? "この文書はすでに改訂候補へ入っています。" : "This document is already in the revision queue.");
        return;
    }
    const note = prompt(displayLang === "ja" ? "改訂候補にする理由・メモ（空でも可）" : "Reason/note for revision candidate (optional)") ?? "";
    const before = revisionBaselineForDoc(doc);
    registrationReviewState.revision_candidates.push({ doc_id: docId, path: String(doc.path ?? ""), created_at: new Date().toISOString(), reviewer_note: note.trim(), decision: "hold", before, after: {} });
    saveRegistrationReviewState();
    setRoute({ view: "revision-candidate", revision: docId });
}
function renderRevisionCandidate(docId) {
    const item = (registrationReviewState.revision_candidates ?? []).find((entry) => String(entry.doc_id ?? "") === docId);
    if (!item)
        return errorPage(`Unknown revision candidate: ${docId}`);
    const page = el("main", "page");
    page.append(navBar("candidates"), dataBanner(), candidateStateBanner());
    const back = button(displayLang === "ja" ? "← 候補一覧" : "← Candidate list", "back-button");
    back.addEventListener("click", () => setRoute({ view: "candidates" }));
    page.append(back);
    const baseline = deepClone(item.before ?? {});
    const working = Object.keys(item.after ?? {}).length ? deepClone(item.after) : deepClone(baseline);
    working.discovery ??= {};
    working.discovery.aliases ??= { ja: [], en: [] };
    working.discovery.reader_questions ??= { ja: [], en: [] };
    working.discovery.topics ??= [];
    const section = el("section", "audit-panel workbench-editor");
    section.append(eyebrow("REVISION CANDIDATE"), el("h1", "section-title", String(working.title_ja || working.title_en || docId)), el("p", "section-copy", displayLang === "ja" ? "現在の公開登録は維持したまま、次のmanifest改訂候補を編集します。" : "Edit a future manifest revision while the current public registration remains active."));
    const controls = {};
    for (const key of ["doc_id", "title_ja", "title_en", "document_type", "layer", "status", "public_profile", "state"])
        controls[key] = textInput(String(working[key] ?? ""));
    controls.scope = textArea(String(working.scope ?? ""), 2);
    controls.role_ja = textArea(String(working.role_ja ?? ""), 3);
    controls.role_en = textArea(String(working.role_en ?? ""), 3);
    controls.topics = textInput((working.discovery.topics ?? []).join(", "));
    controls.aliases_ja = textArea((working.discovery.aliases?.ja ?? []).join("\n"), 3);
    controls.aliases_en = textArea((working.discovery.aliases?.en ?? []).join("\n"), 3);
    controls.questions_ja = textArea((working.discovery.reader_questions?.ja ?? []).join("\n"), 4);
    controls.questions_en = textArea((working.discovery.reader_questions?.en ?? []).join("\n"), 4);
    const entry = el("select", "candidate-select");
    for (const value of ["foundation", "intermediate", "advanced"]) {
        const o = document.createElement("option");
        o.value = value;
        o.textContent = value;
        o.selected = String(working.discovery.entry_level ?? "") === value;
        entry.append(o);
    }
    controls.entry_level = entry;
    const grid = el("div", "workbench-field-grid");
    for (const key of ["doc_id", "title_ja", "title_en", "document_type", "layer", "status", "public_profile", "state"])
        grid.append(reviewField(key, controls[key]));
    section.append(grid, reviewField("scope", controls.scope), reviewField("role_ja", controls.role_ja), reviewField("role_en", controls.role_en), reviewField("topics", controls.topics), reviewField("aliases · ja", controls.aliases_ja), reviewField("aliases · en", controls.aliases_en), reviewField("reader questions · ja", controls.questions_ja), reviewField("reader questions · en", controls.questions_en), reviewField("entry_level", controls.entry_level));
    const note = textArea(String(item.reviewer_note ?? ""), 2);
    section.append(reviewField(displayLang === "ja" ? "レビュー注記" : "Reviewer note", note));
    const read = () => { const after = deepClone(baseline); for (const key of ["doc_id", "title_ja", "title_en", "document_type", "layer", "status", "public_profile", "state", "scope", "role_ja", "role_en"])
        after[key] = controls[key].value.trim(); after.discovery ??= {}; after.discovery.topics = commaValues(controls.topics.value); after.discovery.aliases = { ja: lines(controls.aliases_ja.value), en: lines(controls.aliases_en.value) }; after.discovery.reader_questions = { ja: lines(controls.questions_ja.value), en: lines(controls.questions_en.value) }; after.discovery.entry_level = controls.entry_level.value; return after; };
    const save = (decision) => { item.after = read(); item.decision = decision; item.reviewer_note = note.value.trim(); item.reviewed_at = new Date().toISOString(); saveRegistrationReviewState(); setRoute({ view: "candidates" }); };
    const bar = el("div", "workbench-decision-bar");
    const approve = button(displayLang === "ja" ? "改訂内容を承認" : "Approve revision", "button primary");
    approve.addEventListener("click", () => save("approve"));
    const hold = button(displayLang === "ja" ? "保留" : "Hold", "button");
    hold.addEventListener("click", () => save("hold"));
    const reject = button(displayLang === "ja" ? "却下" : "Reject", "button danger-button");
    reject.addEventListener("click", () => save("reject"));
    bar.append(approve, hold, reject);
    section.append(bar);
    page.append(section);
    return page;
}
function renderCandidates(candidatePath = "") {
    if (candidatePath) {
        const candidate = candidateByPath(candidatePath);
        return candidate ? candidateDetail(candidate) : errorPage(`Unknown registration candidate: ${candidatePath}`);
    }
    const page = el("main", "page");
    page.append(navBar("candidates"), dataBanner(), candidateStateBanner());
    const payload = candidatePayload();
    const section = el("section", "section candidate-page");
    section.append(eyebrow("REGISTRATION WORKBENCH"), el("h1", "hero-title", displayLang === "ja" ? "仮登録と改訂案を同じ土俵でレビューする" : "Review provisional and registered revisions in one pool"), el("p", "hero-copy", displayLang === "ja"
        ? "未登録文書の仮登録候補と、登録済み文書の改訂案を一つのレビュー面で扱います。Public側の仮登録表示はレビュー完了を待たず利用できます。"
        : "Provisionally registered documents and registered-document revision proposals share one review pool. Public discovery can operate while canonical metadata review remains open."));
    if (!payload) {
        section.append(el("p", "error", displayLang === "ja" ? "候補preview JSONを読み込めませんでした。" : "Candidate preview JSON could not be loaded."));
        page.append(section);
        return page;
    }
    const counts = combinedReviewCounts();
    const adHocRevisions = (registrationReviewState.revision_candidates ?? []).filter((item) => item.source_kind !== "registered_reader_question_seed");
    const stats = el("div", "audit-stats candidate-stats");
    stats.append(candidateMetric(displayLang === "ja" ? "未確認" : "Unreviewed", String(counts.unreviewed)), candidateMetric(displayLang === "ja" ? "承認" : "Approved", String((counts.approve ?? 0) + (counts.approve_with_edits ?? 0))), candidateMetric(displayLang === "ja" ? "保留" : "On hold", String(counts.hold ?? 0)), candidateMetric(displayLang === "ja" ? "却下" : "Rejected", String(counts.reject ?? 0)), candidateMetric(displayLang === "ja" ? "仮登録候補" : "Provisional", String(candidateList().length)), candidateMetric(displayLang === "ja" ? "登録済み改訂案" : "Registered revisions", String(registeredReviewList().length)));
    section.append(stats);
    const toolbar = el("div", "workbench-toolbar");
    const next = button(displayLang === "ja" ? "次の未確認へ" : "Next unreviewed", "button primary");
    next.addEventListener("click", () => { const item = nextUnreviewedReviewItem(); if (item)
        openReviewPoolItem(item); });
    const exportButton = button(displayLang === "ja" ? "レビュー結果を書き出す" : "Export review", "button");
    exportButton.addEventListener("click", downloadReviewExport);
    const importLabel = el("label", "button workbench-file-button", displayLang === "ja" ? "レビュー結果を読み込む" : "Import review");
    const importInput = document.createElement("input");
    importInput.type = "file";
    importInput.accept = "application/json,.json";
    importInput.hidden = true;
    importInput.addEventListener("change", async () => {
        const file = importInput.files?.[0];
        if (!file)
            return;
        try {
            await importReviewExport(file);
            render();
        }
        catch (error) {
            alert(String(error.message));
        }
        finally {
            importInput.value = "";
        }
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
    const makeSelect = (label, values) => {
        const wrap = el("label", "candidate-filter");
        wrap.append(el("span", "candidate-filter-label", label));
        const select = el("select", "candidate-select");
        const all = document.createElement("option");
        all.value = "";
        all.textContent = displayLang === "ja" ? "すべて" : "All";
        select.append(all);
        for (const value of values) {
            const option = document.createElement("option");
            option.value = value;
            option.textContent = value === "provisional"
                ? (displayLang === "ja" ? "仮登録候補" : "Provisional")
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
    const layerSelect = makeSelect(displayLang === "ja" ? "体系層" : "Layer", Array.from(new Set(allItems.map((item) => String(item.layer ?? "")).filter(Boolean))).sort());
    const confidenceSelect = makeSelect("confidence", Array.from(new Set(allItems.map((item) => String(item.confidence ?? "")).filter(Boolean))).sort());
    const reviewSelect = makeSelect(displayLang === "ja" ? "レビュー状態" : "Review state", ["unreviewed", "approve", "approve_with_edits", "hold", "reject"]);
    const visibilitySelect = makeSelect("visibility", Array.from(new Set(allItems.map((item) => String(item.visibility ?? "")).filter(Boolean))).sort());
    section.append(filters);
    const summaryLine = el("div", "candidate-result-summary");
    const grid = el("div", "candidate-grid");
    section.append(summaryLine, grid);
    const draw = () => {
        grid.replaceChildren();
        const query = queryInput.value.trim().normalize("NFKC").toLocaleLowerCase("ja-JP");
        const filtered = allItems.filter((item) => {
            if (kindSelect.value && item.kind !== kindSelect.value)
                return false;
            if (layerSelect.value && item.layer !== layerSelect.value)
                return false;
            if (confidenceSelect.value && item.confidence !== confidenceSelect.value)
                return false;
            if (visibilitySelect.value && item.visibility !== visibilitySelect.value)
                return false;
            if (reviewSelect.value && item.decision !== reviewSelect.value)
                return false;
            return !query || String(item.search_text ?? "").includes(query);
        });
        summaryLine.textContent = `${filtered.length} / ${allItems.length} ${displayLang === "ja" ? "レビュー項目を表示" : "review items shown"}`;
        for (const item of filtered) {
            const card = el("article", "candidate-card card");
            const meta = el("div", "doc-meta-line");
            meta.append(badge(reviewDecisionLabel(String(item.decision)), decisionTone(String(item.decision))));
            if (item.kind === "registered_revision")
                meta.append(badge(displayLang === "ja" ? "登録済み改訂案" : "Registered revision", "warn"));
            else
                meta.append(badge(displayLang === "ja" ? "仮登録候補" : "Provisional", "warn"));
            if (item.confidence)
                meta.append(badge(String(item.confidence)));
            if (item.visibility)
                meta.append(badge(String(item.visibility)));
            card.append(meta, el("h2", "card-title", String(item.title ?? "")));
            if (item.role)
                card.append(el("p", "card-copy", String(item.role)));
            if ((item.questions ?? []).length)
                card.append(el("div", "question-line", `Q. ${String(item.questions[0])}`));
            if (item.kind === "provisional") {
                const candidate = item.source ?? {};
                const needs = (candidate.review?.needs_human_judgment ?? []).map((value) => String(value));
                if (needs.length)
                    card.append(el("div", "candidate-review-hint", `${displayLang === "ja" ? "確認" : "Review"}: ${needs.join(" · ")}`));
            }
            else {
                const current = item.source?.current?.[displayLang] ?? [];
                const proposed = item.source?.proposed?.[displayLang] ?? [];
                card.append(el("div", "candidate-review-hint", displayLang === "ja"
                    ? `reader questions: 現在 ${current.length} → 提案 ${proposed.length}`
                    : `reader questions: current ${current.length} → proposed ${proposed.length}`));
            }
            card.append(el("div", "path", String(item.path ?? "")));
            const row = el("div", "card-actions");
            const inspect = button(displayLang === "ja" ? "レビューする" : "Review", "button compact-button");
            inspect.addEventListener("click", () => openReviewPoolItem(item));
            row.append(inspect);
            if (item.path && readerAllowedPaths().has(String(item.path)))
                row.append(readerButton(String(item.path)));
            card.append(row);
            grid.append(card);
        }
        if (!filtered.length)
            grid.append(el("p", "empty", displayLang === "ja" ? "条件に合うレビュー項目はありません。" : "No review item matches the filters."));
    };
    for (const control of [queryInput, kindSelect, layerSelect, confidenceSelect, reviewSelect, visibilitySelect]) {
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
                registrationReviewState.manual_candidates = registrationReviewState.manual_candidates.filter((entry) => entry.id !== item.id);
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
                registrationReviewState.revision_candidates = registrationReviewState.revision_candidates.filter((entry) => entry.doc_id !== item.doc_id);
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
function renderAudit() {
    const page = el("main", "page");
    page.append(navBar("audit"), dataBanner());
    const section = el("section", "section");
    section.append(eyebrow("DATA AUDIT"), el("h1", "hero-title", displayLang === "ja" ? "UIからデータへ戻る点検面" : "Audit the data from the UI surface"), el("p", "hero-copy", displayLang === "ja"
        ? "ここでは重要度を計算せず、現在UIに見えているものがどのデータ状態から来ているかを露出します。"
        : "This view exposes the data state behind the UI without calculating importance scores."));
    const nodeCounts = new Map();
    for (const node of docsGraph.nodes ?? [])
        nodeCounts.set(String(node.type), (nodeCounts.get(String(node.type)) ?? 0) + 1);
    const edgeCounts = new Map();
    for (const edge of docsGraph.edges ?? [])
        edgeCounts.set(String(edge.relation), (edgeCounts.get(String(edge.relation)) ?? 0) + 1);
    const stats = el("div", "audit-stats");
    const statRows = [
        [displayLang === "ja" ? "Public catalog 文書" : "Public catalog documents", String((docsIndex.documents ?? []).length)],
        [displayLang === "ja" ? "canonical 登録文書" : "Canonical registered documents", String(docsIndex.source?.registered_documents ?? nodeCounts.get("document") ?? 0)],
        [displayLang === "ja" ? "公開仮登録文書" : "Public provisional documents", String(docsIndex.source?.provisional_documents ?? 0)],
        [displayLang === "ja" ? "観測のみdocument nodes" : "Observed-only document nodes", String(nodeCounts.get("observed_document") ?? 0)],
        [displayLang === "ja" ? "登録候補台帳" : "Registration candidate ledger", String(candidatePayload()?.summary?.total_candidates ?? 0)],
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
        candidateAudit.append(el("h2", "section-title small", displayLang === "ja" ? "登録候補preview" : "Registration candidate preview"), el("p", "section-copy", displayLang === "ja"
            ? "候補台帳はcanonical manifestとは分離したままです。searchableな候補だけを開発情報を除いたPublic catalogへ投影し、検索・読解・関係探索の暫定入口として利用します。confidence、evidence、人間レビュー状態はDeveloper側だけに残ります。"
            : "The candidate ledger is retained as a review/audit source, while provisional entries now live in the canonical manifest. The Public catalog is generated from that single manifest-derived index. Confidence, evidence, and human-review state remain Developer-only."));
        const candidateOpen = button(displayLang === "ja" ? "候補レビューを開く" : "Open candidate review", "button secondary");
        candidateOpen.addEventListener("click", () => setRoute({ view: "candidates" }));
        candidateAudit.append(candidateOpen);
        section.append(candidateAudit);
    }
    const relationPanel = el("section", "audit-panel");
    relationPanel.append(el("h2", "section-title small", displayLang === "ja" ? "関係型の走査結果" : "Observed relation types"), el("p", "section-copy", displayLang === "ja"
        ? "これは重要度ではなく、現時点の走査件数です。各relationの具体的な辺は関係マップ側で確認します。"
        : "These are scan counts, not importance. Inspect the actual edges in the relation map."));
    const relationTable = el("div", "relation-count-table");
    for (const [relation, count] of Array.from(edgeCounts.entries()).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], "en"))) {
        const row = el("div", "relation-count-row");
        row.append(el("code", "", relation), el("span", "", String(count)));
        relationTable.append(row);
    }
    relationPanel.append(relationTable);
    section.append(relationPanel);
    const coverage = el("section", "audit-panel");
    coverage.append(el("h2", "section-title small", displayLang === "ja" ? "体系層ごとの登録 / 観測" : "Registered / observed by system layer"));
    const coverageList = el("div", "layer-list");
    for (const layer of layerSummaries(docsGraph).filter((row) => row.key !== "root")) {
        const row = el("button", "layer-row");
        row.type = "button";
        row.addEventListener("click", () => setRoute({ layer: String(layer.id) }));
        row.append(el("span", "layer-name", localized(layer.label, String(layer.key))), el("span", "layer-path", String(layer.path)), el("span", "layer-count", `${layer.registered.length} / ${layer.observed.length}`));
        coverageList.append(row);
    }
    coverage.append(coverageList);
    section.append(coverage);
    page.append(section);
    return page;
}
function errorPage(message) {
    const page = el("main", "page");
    page.append(navBar("home"), el("p", "error", message));
    return page;
}
function render() {
    if (!docsIndex || !docsGraph)
        return;
    const params = route();
    let content;
    try {
        if (params.get("topic"))
            content = renderTopic(String(params.get("topic")));
        else if (params.get("layer"))
            content = renderLayer(String(params.get("layer")));
        else if (params.get("read"))
            content = renderReader(String(params.get("read")));
        else if (params.get("doc"))
            content = renderDocument(String(params.get("doc")));
        else if (params.get("graph"))
            content = renderRelations(String(params.get("graph")));
        else if (params.get("view") === "search")
            content = renderSearch(params.get("q") ?? "");
        else if (params.get("view") === "relations")
            content = renderRelations();
        else if (isDeveloper() && params.get("view") === "candidates")
            content = renderCandidates(params.get("candidate") ?? "");
        else if (isDeveloper() && params.get("view") === "registered-review")
            content = renderRegisteredRevisionProposal(params.get("registered") ?? "");
        else if (isDeveloper() && params.get("view") === "manual-candidate")
            content = renderManualCandidate();
        else if (isDeveloper() && params.get("view") === "revision-candidate")
            content = renderRevisionCandidate(params.get("revision") ?? "");
        else if (isDeveloper() && params.get("view") === "audit")
            content = renderAudit();
        else
            content = renderExplore();
    }
    catch (error) {
        content = errorPage(String(error.message));
    }
    app.replaceChildren(content);
    window.scrollTo({ top: 0, behavior: "instant" });
}
async function load() {
    try {
        status.textContent = displayLang === "ja" ? "データを読み込み中…" : "Loading data…";
        const candidatePromise = isDeveloper()
            ? fetch(CANDIDATES_URL).catch(() => null)
            : Promise.resolve(null);
        const registeredReviewPromise = isDeveloper()
            ? fetch(REGISTERED_REVIEW_URL).catch(() => null)
            : Promise.resolve(null);
        const graphUrl = isDeveloper() ? DEVELOPER_GRAPH_URL : PUBLIC_GRAPH_URL;
        const [catalogResponse, graphResponse, publicContentResponse, candidateResponse, registeredReviewResponse] = await Promise.all([
            fetch(PUBLIC_CATALOG_URL),
            fetch(graphUrl),
            fetch(PUBLIC_CONTENT_URL),
            candidatePromise,
            registeredReviewPromise,
        ]);
        if (!catalogResponse.ok)
            throw new Error(`docs_public_catalog.json: HTTP ${catalogResponse.status}`);
        if (!graphResponse.ok)
            throw new Error(`${graphUrl}: HTTP ${graphResponse.status}`);
        if (!publicContentResponse.ok)
            throw new Error(`public-content.json: HTTP ${publicContentResponse.status}`);
        docsIndex = await catalogResponse.json();
        docsGraph = await graphResponse.json();
        publicContent = await publicContentResponse.json();
        if (isDeveloper() && candidateResponse?.ok)
            registrationCandidates = await candidateResponse.json();
        else
            registrationCandidates = null;
        if (isDeveloper() && registeredReviewResponse?.ok)
            registeredReviewProposals = await registeredReviewResponse.json();
        else
            registeredReviewProposals = null;
        if (isDeveloper() && registrationCandidates)
            loadRegistrationReviewState();
        status.textContent = "";
        updateHeaderControls();
        render();
    }
    catch (error) {
        status.textContent = String(error.message);
        status.className = "load-error";
    }
}
langButton.addEventListener("click", () => setLanguage(displayLang === "ja" ? "en" : "ja"));
headerMenuButton.addEventListener("click", () => setRoute({}));
headerBackButton.addEventListener("click", () => history.length > 1 ? history.back() : setRoute({}));
headerTopButton.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
headerBottomButton.addEventListener("click", () => window.scrollTo({ top: document.documentElement.scrollHeight, behavior: "smooth" }));
window.addEventListener("hashchange", render);
updateHeaderControls();
load();

import { type JsonObject } from "./search-core.js";
import { preferredDocumentForLanguage, presentationKeyForDocument } from "./language-core.js";

// Reader presentation only: neither canonical metadata nor assessment state.
const TEXT = {
  document: ["文書", "Document"],
  read: ["本文を読む", "Read"],
  toc: ["目次", "Contents"],
  readingTools: ["読書設定", "Reading settings"],
  textSize: ["文字", "Text size"],
  standard: ["標準", "Standard"],
  large: ["大", "Large"],
  larger: ["特大", "Larger"],
  theme: ["配色", "Theme"],
  themeSystem: ["端末に合わせる", "System"],
  themeLight: ["明るい", "Light"],
  themeDark: ["暗い", "Dark"],
  themePaper: ["紙", "Paper"],
  copyLink: ["リンクをコピー", "Copy link"],
  copied: ["リンクをコピーしました。", "Link copied."],
  copyFailed: ["コピーできませんでした。アドレス欄のURLをコピーしてください。", "Copy was unavailable. Copy the URL from the address bar instead."],
  settingsNotSaved: ["このブラウザでは設定を保存できません。今回の表示には適用しました。", "This browser could not save the setting. It has been applied for this visit."],
  selectedSearch: ["選択した語句を探す", "Search selected text"],
  selectedSearchShort: ["この語句を探す", "Search this text"],
  selectedDismiss: ["閉じる", "Close"],
  selectionHint: ["分からない語句は本文で選択すると、そのままNavigator内を検索できます。", "Select an unfamiliar phrase in the text to search the Navigator without retyping it."],
  unavailable: ["この文書は読書用カタログにありません。メニューから選び直してください。", "This document is not in the reading catalog. Choose a document from the menu."],
  loadFailed: ["本文を正しく読み込めませんでした。再読み込みしても続く場合は、原ファイルの確認が必要です。", "The document could not be read correctly. Reload the page; if the problem persists, the source file needs checking."],
  graphNotFound: ["関係の出発点を一つに特定できません。検索結果の「関係を見る」から開いてください。", "A unique starting point could not be found. Open Relations from a document in the search results."],
  chapterNotFound: ["指定された節が見つからないため、文書の先頭を表示しています。", "The requested section was not found. The document is shown from the beginning."],
  sectionAfterLanguage: ["言語版を切り替えました。見出しの対応を仮定せず、文書の先頭から表示します。", "Language edition changed. The document opens at the beginning because section correspondence is not assumed."],
  relatedIntro: ["本文リンクまたは明示された関係でつながる文書です。人気や重要度の順位ではありません。", "Documents connected by a source link or a declared relation. This is not a popularity or importance ranking."],
  brand: ["存在境界論", "Scientific Ontology"],
  subtitle: ["Scientific Ontology · 読書ナビゲーター", "Reading Navigator"],
  homeLabel: ["存在境界論の読書トップへ", "Scientific Ontology reading home"],
  footer: ["検索上の関連と概念の同一性、関係と真理、本文リンクと定義の所有は、それぞれ別です。", "Search association is not conceptual identity; a relation is not truth; a source link is not definition ownership."],
  startIntro: ["全体の見取り図と、読み進めるための入口を確認できます。", "An overview of the framework and the routes into it."],
  layerCount: ["この層の文書", "Documents in this layer"],
  fallbackJa: ["本文は日本語", "Text in Japanese"],
  fallbackEn: ["本文は英語", "Text in English"],
  editorialEditor: ["読書編集", "Reading editor"],
  editorialExport: ["選択をJSON出力", "Export selection JSON"],
  editorialImport: ["JSONを読み込む", "Import JSON"],
  editorialReset: ["現在の公開設定へ戻す", "Reset to published settings"],
  editorialAdd: ["追加", "Add"],
  editorialRemove: ["外す", "Remove"],
  editorialUp: ["上へ", "Up"],
  editorialDown: ["下へ", "Down"],
  editorialPreview: ["公開プレビュー", "Public preview"],
  editorialAllDocs: ["公開カタログの全文書", "All documents in the public catalog"],
  editorialSavedLocal: ["この選択はブラウザ内だけに保存されています。公開設定の変更にはJSONを出力し、repository-side applyを通します。", "This selection is saved only in this browser. Export JSON and use the repository-side apply step to change the public configuration."],
} as const;

export type ReadingTextKey = keyof typeof TEXT;
export type ReadingLanguage = "ja" | "en";

export function readerText(lang: ReadingLanguage, key: ReadingTextKey): string {
  return TEXT[key][lang === "ja" ? 0 : 1];
}

export function isTechnicalLabel(label: string, doc?: JsonObject): boolean {
  const clean = label.trim().replace(/^`|`$/g, "");
  if (!clean) return true;
  const path = String(doc?.path ?? "");
  if ([doc?.id, doc?.doc_id, path, path.split("/").at(-1)].filter(Boolean).includes(clean)) return true;
  return /^(?:doc|observed|path-family):/.test(clean) || /(?:^|[/\\])[^\s]+\.(?:md|markdown)(?:#.*)?$/i.test(clean);
}

export function publicDocumentTitle(doc: JsonObject, lang: ReadingLanguage): string {
  const title = doc.title;
  const candidates = typeof title === "string" ? [title] : [title?.[lang], title?.[lang === "ja" ? "en" : "ja"]];
  for (const value of candidates) {
    if (typeof value === "string" && value.trim() && !isTechnicalLabel(value, doc)) return value.trim();
  }
  return readerText(lang, "document");
}

export function publicLinkLabel(label: string, doc: JsonObject, lang: ReadingLanguage): string {
  // Preserve authored prose; replace mechanical filename/identity labels only.
  return isTechnicalLabel(label, doc) ? publicDocumentTitle(doc, lang) : label;
}

export function sectionSlug(text: string): string {
  return text.normalize("NFKC").toLowerCase()
    .replace(/[`*_~[\](){}<>]/g, "")
    .replace(/[^\p{Letter}\p{Number}]+/gu, "-")
    .replace(/^-+|-+$/g, "") || "section";
}

export function fragmentFromLink(href: string): string {
  const index = href.indexOf("#");
  if (index < 0) return "";
  const fragment = href.slice(index + 1);
  try { return decodeURIComponent(fragment); } catch { return fragment; }
}


export type InlineMathSegment =
  | { kind: "text"; value: string }
  | { kind: "math"; value: string; delimiter: "$" | "\\(" };

function isEscaped(text: string, index: number): boolean {
  let slashes = 0;
  for (let i = index - 1; i >= 0 && text[i] === "\\"; i -= 1) slashes += 1;
  return slashes % 2 === 1;
}

function findInlineDollarClose(text: string, start: number): number {
  for (let i = start + 1; i < text.length; i += 1) {
    if (text[i] === "\n") return -1;
    if (text[i] !== "$" || isEscaped(text, i)) continue;
    if (text[i - 1]?.trim() === "") continue;
    // Pandoc-style guard: avoid reading currency such as "$100-$200" as math.
    if (/\d/.test(text[i + 1] ?? "")) continue;
    return i;
  }
  return -1;
}

function findInlineParenClose(text: string, start: number): number {
  for (let i = start + 2; i + 1 < text.length; i += 1) {
    if (text[i] === "\n") return -1;
    if (text[i] === "\\" && text[i + 1] === ")" && !isEscaped(text, i)) return i;
  }
  return -1;
}

/** Split prose into raw text and TeX math without interpreting Markdown code spans. */
export function splitInlineMath(text: string): InlineMathSegment[] {
  const output: InlineMathSegment[] = [];
  let cursor = 0;
  let i = 0;
  const pushText = (end: number) => {
    if (end > cursor) output.push({ kind: "text", value: text.slice(cursor, end) });
  };

  while (i < text.length) {
    if (text[i] === "\\" && text[i + 1] === "(" && !isEscaped(text, i)) {
      const close = findInlineParenClose(text, i);
      if (close >= 0) {
        const value = text.slice(i + 2, close);
        if (value.trim()) {
          pushText(i);
          output.push({ kind: "math", value, delimiter: "\\(" });
          cursor = close + 2;
          i = cursor;
          continue;
        }
      }
    }

    if (text[i] === "$" && !isEscaped(text, i) && text[i - 1] !== "$" && text[i + 1] !== "$" && text[i + 1] && !/\s/.test(text[i + 1])) {
      const close = findInlineDollarClose(text, i);
      if (close >= 0) {
        const value = text.slice(i + 1, close);
        if (value.trim()) {
          pushText(i);
          output.push({ kind: "math", value, delimiter: "$" });
          cursor = close + 1;
          i = cursor;
          continue;
        }
      }
    }
    i += 1;
  }

  if (cursor < text.length) output.push({ kind: "text", value: text.slice(cursor) });
  if (!output.length) output.push({ kind: "text", value: text });
  return output;
}

export interface DisplayMathBlock {
  tex: string;
  nextIndex: number;
  delimiter: "$$" | "\\[";
}

/** Parse a display-math block beginning at lines[start]. Returns null for ordinary prose. */
export function displayMathBlockAt(lines: string[], start: number): DisplayMathBlock | null {
  const line = lines[start] ?? "";
  const trimmed = line.trim();

  if (trimmed.startsWith("$$")) {
    if (trimmed.length > 4 && trimmed.endsWith("$$")) {
      const tex = trimmed.slice(2, -2).trim();
      return tex ? { tex, nextIndex: start + 1, delimiter: "$$" } : null;
    }
    if (trimmed === "$$") {
      const body: string[] = [];
      let i = start + 1;
      while (i < lines.length && lines[i].trim() !== "$$") {
        body.push(lines[i]);
        i += 1;
      }
      if (i < lines.length && body.join("\n").trim()) {
        return { tex: body.join("\n").trim(), nextIndex: i + 1, delimiter: "$$" };
      }
    }
  }

  if (trimmed.startsWith("\\[")) {
    if (trimmed.length > 4 && trimmed.endsWith("\\]")) {
      const tex = trimmed.slice(2, -2).trim();
      return tex ? { tex, nextIndex: start + 1, delimiter: "\\[" } : null;
    }
    if (trimmed === "\\[") {
      const body: string[] = [];
      let i = start + 1;
      while (i < lines.length && lines[i].trim() !== "\\]") {
        body.push(lines[i]);
        i += 1;
      }
      if (i < lines.length && body.join("\n").trim()) {
        return { tex: body.join("\n").trim(), nextIndex: i + 1, delimiter: "\\[" };
      }
    }
  }

  return null;
}

export function isDisplayMathStart(line: string): boolean {
  const trimmed = line.trim();
  return trimmed === "$$" || /^\$\$.+\$\$$/.test(trimmed) || trimmed === "\\[" || /^\\\[.+\\\]$/.test(trimmed);
}

export function sourceHeaderLines(text: string): boolean {
  const lines = text.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
  const field = /^(?:Document ID|Doc ID|Status|State|Scope|Language|Claim strength|Layer|Authority|Public profile|Public handling|Primary question|Search terms|Document role|Publication layer|Maturity|Version|Last updated|Japanese authoritative source|Lifecycle|Maintenance|Canonical scope|Role|Domain|Non-claim boundary|Non-claim|Claim posture|Language relation|Claim boundary|Definition ownership|Related application|Legal status|English commensuration|Rule|Version-specific DOI|Formation provenance|Reading rule|Physical-near handling|Note|Source of release facts|Synchronizer|Target version|Commensuration note|Principle|Research program|Research context|Open philosophical questions|Period covered|Derivation)\s*:/i;
  return lines.length >= 2 && lines.every((line) => field.test(line));
}

export function documentKey(doc: JsonObject): string {
  return String(doc.id ?? doc.doc_id ?? doc.path ?? "");
}

export function documentForEditorialId(documents: JsonObject[], documentId: string): JsonObject | undefined {
  return documents.find((doc) => documentKey(doc) === documentId);
}

export function readingChannels(content: JsonObject): JsonObject[] {
  return [...(content.reading_channels ?? [])]
    .filter((channel: JsonObject) => channel && typeof channel === "object")
    .sort((a: JsonObject, b: JsonObject) => Number(a.order ?? 999) - Number(b.order ?? 999) || String(a.id ?? "").localeCompare(String(b.id ?? ""), "en"));
}

export interface ReadingChannelEntry {
  documentId: string;
  source: JsonObject;
  document: JsonObject;
}

export function readingChannelEntries(channel: JsonObject, documents: JsonObject[], lang: ReadingLanguage): ReadingChannelEntry[] {
  const seen = new Set<string>();
  const output: ReadingChannelEntry[] = [];
  for (const rawId of channel.documents ?? []) {
    const documentId = String(rawId ?? "");
    const source = documentForEditorialId(documents, documentId);
    if (!source) continue;
    const document = preferredDocumentForLanguage(source, documents, lang);
    const family = presentationKeyForDocument(document);
    if (seen.has(family)) continue;
    seen.add(family);
    output.push({ documentId, source, document });
  }
  return output;
}

export function sameEditorialSelection(a: unknown, b: unknown): boolean {
  return JSON.stringify(a ?? []) === JSON.stringify(b ?? []);
}

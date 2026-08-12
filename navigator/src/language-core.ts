import type { JsonObject } from "./search-core.js";

export type UiLanguage = "ja" | "en";
export type DocumentLanguage = UiLanguage | "bilingual" | "und";

function normalizedPath(value: unknown): string {
  return String(value ?? "").replace(/\\/g, "/");
}

function relationObject(doc: JsonObject): JsonObject | null {
  const value = doc.language_relation;
  return value && typeof value === "object" && !Array.isArray(value) ? value : null;
}

export function documentLanguage(doc: JsonObject): DocumentLanguage {
  const presentation = doc.presentation;
  const declared = String(presentation?.language ?? "").toLowerCase();
  if (declared === "ja" || declared === "en" || declared === "bilingual" || declared === "und") {
    return declared as DocumentLanguage;
  }

  const path = normalizedPath(doc.path);
  if (/\.ja\.md$/i.test(path)) return "ja";
  if (/\.en\.md$/i.test(path)) return "en";

  const relation = relationObject(doc);
  const relationLanguage = String(relation?.language ?? "").toLowerCase();
  if (relationLanguage === "ja") return "ja";
  if (relationLanguage === "en") return "en";
  if (["ja+en", "ja-en", "bilingual", "both"].includes(relationLanguage)) return "bilingual";

  const legacy = typeof doc.language_relation === "string" ? doc.language_relation.toLowerCase() : "";
  if (legacy.includes("japanese_authoritative")) return "ja";
  if (legacy.includes("english_commensuration")) return "en";

  return "und";
}

export function presentationKeyForDocument(doc: JsonObject): string {
  const presentationKey = String(doc.presentation?.family_key ?? "");
  if (presentationKey) return presentationKey;

  const path = normalizedPath(doc.path);
  if (/\.(ja|en)\.md$/i.test(path)) return `path-family:${path.replace(/\.(ja|en)\.md$/i, ".md")}`;

  const relation = relationObject(doc);
  const counterpart = normalizedPath(relation?.counterpart_path);
  if (path && counterpart) return `path-pair:${[path, counterpart].sort().join("|")}`;

  return `path:${path || String(doc.id ?? doc.doc_id ?? "")}`;
}

function counterpartPath(doc: JsonObject): string {
  const presentationCounterpart = normalizedPath(doc.presentation?.counterpart_path);
  if (presentationCounterpart) return presentationCounterpart;

  const relation = relationObject(doc);
  const declared = normalizedPath(relation?.counterpart_path);
  if (declared) return declared;

  const path = normalizedPath(doc.path);
  if (/\.ja\.md$/i.test(path)) return path.replace(/\.ja\.md$/i, ".en.md");
  if (/\.en\.md$/i.test(path)) return path.replace(/\.en\.md$/i, ".ja.md");
  return "";
}

function documentsByPath(allDocuments: JsonObject[]): Map<string, JsonObject> {
  return new Map(allDocuments.map((doc) => [normalizedPath(doc.path), doc]));
}

export function preferredDocumentForLanguage(
  doc: JsonObject,
  allDocuments: JsonObject[],
  lang: UiLanguage,
): JsonObject {
  const sourceLanguage = documentLanguage(doc);
  if (sourceLanguage === lang || sourceLanguage === "bilingual" || sourceLanguage === "und") return doc;

  const counterpart = counterpartPath(doc);
  if (!counterpart) return doc;
  const target = documentsByPath(allDocuments).get(counterpart);
  if (!target) return doc;
  const targetLanguage = documentLanguage(target);
  return targetLanguage === lang || targetLanguage === "bilingual" || targetLanguage === "und" ? target : doc;
}

export function preferredPathForLanguage(path: string, allDocuments: JsonObject[], lang: UiLanguage): string {
  const normalized = normalizedPath(path);
  const source = documentsByPath(allDocuments).get(normalized);
  if (!source) return normalized;
  return normalizedPath(preferredDocumentForLanguage(source, allDocuments, lang).path) || normalized;
}

export function collapseDocumentsForLanguage(
  documents: JsonObject[],
  allDocuments: JsonObject[],
  lang: UiLanguage,
): JsonObject[] {
  const output: JsonObject[] = [];
  const seen = new Set<string>();
  for (const source of documents) {
    const preferred = preferredDocumentForLanguage(source, allDocuments, lang);
    const key = presentationKeyForDocument(preferred);
    if (seen.has(key)) continue;
    seen.add(key);
    output.push(preferred);
  }
  return output;
}

export function collapseSearchResultsForLanguage(
  results: JsonObject[],
  allDocuments: JsonObject[],
  lang: UiLanguage,
  limit = results.length,
): JsonObject[] {
  const byKey = new Map<string, JsonObject>();
  const order: string[] = [];

  for (const source of results) {
    const preferred = preferredDocumentForLanguage(source, allDocuments, lang);
    const key = presentationKeyForDocument(preferred);
    const projected = {
      ...preferred,
      score: Number(source.score ?? 0),
      matches: source.matches ?? [],
    };
    const existing = byKey.get(key);
    if (!existing) {
      byKey.set(key, projected);
      order.push(key);
      continue;
    }
    if (Number(projected.score ?? 0) > Number(existing.score ?? 0)) byKey.set(key, projected);
  }

  return order.map((key) => byKey.get(key)!).slice(0, limit);
}

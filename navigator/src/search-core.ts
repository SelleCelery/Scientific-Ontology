export type JsonObject = Record<string, any>;

const METHOD_PRIORITY: Record<string, number> = {
  exact: 5,
  contains: 4,
  term_coverage: 3,
  query_expansion: 2,
  char_ngram: 1,
};

const ENTRY_LEVEL_ORDER: Record<string, number> = {
  foundation: 0,
  intermediate: 1,
  advanced: 2,
  "": 3,
};

function lexicalCompare(a: string, b: string): number {
  return a < b ? -1 : a > b ? 1 : 0;
}

function caseFold(value: string): string {
  // JavaScript has no full Unicode casefold primitive. This covers the corpus
  // used by the current repository and the most common casefold delta (ß -> ss).
  return value.toLocaleLowerCase("en-US").replace(/ß/g, "ss");
}

export function normalizeText(value: any): string {
  const text = caseFold(String(value ?? "").normalize("NFKC"));
  return text
    .replace(/[\p{P}\p{S}]/gu, " ")
    .trim()
    .split(/\s+/u)
    .filter(Boolean)
    .join(" ");
}

export function compactText(value: any): string {
  return normalizeText(value).replace(/ /g, "");
}

function ngrams(value: string, n: number): Set<string> {
  const result = new Set<string>();
  if (!value) return result;
  if (value.length < n) {
    result.add(value);
    return result;
  }
  for (let i = 0; i <= value.length - n; i += 1) result.add(value.slice(i, i + n));
  return result;
}

export function diceSimilarity(a: string, b: string): number {
  if (!a || !b) return 0;
  const n = Math.min(a.length, b.length) <= 5 ? 2 : 3;
  const left = ngrams(a, n);
  const right = ngrams(b, n);
  if (!left.size || !right.size) return 0;
  let intersection = 0;
  for (const value of left) if (right.has(value)) intersection += 1;
  return (2 * intersection) / (left.size + right.size);
}

function allowedLang(entryLang: string, selected: string): boolean {
  return selected === "both" || entryLang === "und" || entryLang === selected;
}

function knownTermValues(index: JsonObject, lang: string): Set<string> {
  const values = new Set<string>();
  for (const doc of index.documents ?? []) {
    for (const field of ["title", "aliases", "owned_concept", "topics"]) {
      for (const item of doc.search_fields?.[field] ?? []) {
        if (allowedLang(String(item.lang ?? "und"), lang)) {
          const norm = String(item.normalized ?? "");
          if (norm) values.add(norm);
        }
      }
    }
    values.add(normalizeText(doc.id ?? ""));
  }
  return values;
}

export function classifyQuery(query: string, index: JsonObject, mode = "auto", lang = "both"): string {
  if (mode === "term" || mode === "question") return mode;
  const normalized = normalizeText(query);
  const compact = normalized.replace(/ /g, "");
  if (knownTermValues(index, lang).has(normalized)) return "term";
  const markers = (index.search_profile?.question_markers_ja ?? []).map((value: any) => normalizeText(value));
  if (markers.some((marker: string) => marker && normalized.includes(marker))) return "question";
  if (compact.length >= 18 || normalized.split(" ").filter(Boolean).length >= 5) return "question";
  return "term";
}

function expansionPhrases(group: JsonObject, lang: string): Array<[string, string]> {
  const languages = lang === "both" ? ["ja", "en"] : [lang];
  const rows: Array<[string, string]> = [];
  for (const itemLang of languages) {
    for (const phrase of group[itemLang] ?? []) rows.push([itemLang, String(phrase)]);
  }
  return rows;
}

export function activeExpansionGroups(query: string, index: JsonObject, lang = "both"): string[] {
  const queryNorm = normalizeText(query);
  const queryCompact = queryNorm.replace(/ /g, "");
  const thresholds = index.search_profile?.thresholds ?? {};
  const minSim = Math.max(Number(thresholds.char_ngram_min_similarity ?? 0.28), 0.46);
  const active: string[] = [];
  for (const [groupId, group] of Object.entries(index.query_expansions ?? {})) {
    let contacted = false;
    for (const [, phrase] of expansionPhrases(group as JsonObject, lang)) {
      const norm = normalizeText(phrase);
      const compact = norm.replace(/ /g, "");
      if (!norm) continue;
      if (queryNorm === norm || queryNorm.includes(norm) || norm.includes(queryNorm)) {
        contacted = true;
        break;
      }
      if (Math.min(queryCompact.length, compact.length) >= 4 && diceSimilarity(queryCompact, compact) >= minSim) {
        contacted = true;
        break;
      }
    }
    if (contacted) active.push(String(groupId));
  }
  return active.sort(lexicalCompare);
}

function termCoverage(queryNorm: string, textNorm: string): number {
  const terms = queryNorm.split(" ").filter((term) => term.length >= 2);
  if (terms.length < 2) return 0;
  const matched = terms.filter((term) => textNorm.includes(term)).length;
  return matched / terms.length;
}

function matchEntry(
  query: string,
  entry: JsonObject,
  index: JsonObject,
  activeGroups: string[],
  lang: string,
): JsonObject | null {
  const entryLang = String(entry.lang ?? "und");
  if (!allowedLang(entryLang, lang)) return null;
  const queryNorm = normalizeText(query);
  const queryCompact = queryNorm.replace(/ /g, "");
  const textNorm = String(entry.normalized ?? "");
  const textCompact = String(entry.compact ?? "");
  const profile = index.search_profile ?? {};
  const strengths = profile.match_strength ?? {};
  const thresholds = profile.thresholds ?? {};
  const candidates: JsonObject[] = [];

  if (queryNorm && queryNorm === textNorm) {
    candidates.push({ method: "exact", strength: Number(strengths.exact ?? 1), expansion_group: null });
  }
  if (queryNorm && textNorm && (queryNorm.includes(textNorm) || textNorm.includes(queryNorm))) {
    candidates.push({ method: "contains", strength: Number(strengths.contains ?? 0.9), expansion_group: null });
  }

  const coverage = termCoverage(queryNorm, textNorm);
  if (coverage >= 0.5) {
    candidates.push({
      method: "term_coverage",
      strength: Number(strengths.term_coverage ?? 0.75) * coverage,
      expansion_group: null,
    });
  }

  const minChars = Number(thresholds.char_ngram_min_chars ?? 4);
  const minSim = Number(thresholds.char_ngram_min_similarity ?? 0.28);
  if (Math.min(queryCompact.length, textCompact.length) >= minChars) {
    const sim = diceSimilarity(queryCompact, textCompact);
    if (sim >= minSim) {
      candidates.push({
        method: "char_ngram",
        strength: Math.min(Number(strengths.char_ngram_cap ?? 0.45), sim),
        expansion_group: null,
        similarity: sim,
      });
    }
  }

  const expansionStrength = Number(strengths.query_expansion ?? 0.65);
  const expansions = index.query_expansions ?? {};
  const expansionAllowed = !["topics", "owned_concept"].includes(String(entry.field ?? ""));
  const groups = expansionAllowed ? activeGroups : [];
  for (const groupId of groups) {
    const group = expansions[groupId] ?? {};
    for (const [, phrase] of expansionPhrases(group, lang)) {
      const phraseNorm = normalizeText(phrase);
      const phraseCompact = phraseNorm.replace(/ /g, "");
      if (!phraseNorm) continue;
      if (phraseNorm === textNorm || phraseNorm.includes(textNorm) || textNorm.includes(phraseNorm)) {
        candidates.push({
          method: "query_expansion",
          strength: expansionStrength,
          expansion_group: groupId,
          expansion_phrase: phrase,
        });
      } else if (Math.min(phraseCompact.length, textCompact.length) >= minChars) {
        const sim = diceSimilarity(phraseCompact, textCompact);
        if (sim >= minSim) {
          candidates.push({
            method: "query_expansion",
            strength: expansionStrength * sim,
            expansion_group: groupId,
            expansion_phrase: phrase,
            similarity: sim,
          });
        }
      }
    }
  }

  if (!candidates.length) return null;
  candidates.sort((a, b) => {
    const strengthDelta = Number(b.strength) - Number(a.strength);
    if (strengthDelta !== 0) return strengthDelta;
    return (METHOD_PRIORITY[String(b.method)] ?? 0) - (METHOD_PRIORITY[String(a.method)] ?? 0);
  });
  return { ...candidates[0], text: String(entry.text ?? ""), lang: entryLang };
}

export function searchDocuments(
  query: string,
  index: JsonObject,
  mode = "auto",
  limit = 10,
  lang = "both",
): { mode: string; results: JsonObject[] } {
  const resolvedMode = classifyQuery(query, index, mode, lang);
  const activeGroups = activeExpansionGroups(query, index, lang);
  const weights = index.search_profile?.modes?.[resolvedMode]?.field_weights ?? {};
  const minimum = Number(index.search_profile?.thresholds?.minimum_result_score ?? 2.5);
  const results: JsonObject[] = [];

  for (const doc of index.documents ?? []) {
    let score = 0;
    const matches: JsonObject[] = [];
    let directCount = 0;
    const fields = doc.search_fields ?? {};
    for (const [field, weightValue] of Object.entries(weights)) {
      const weight = Number(weightValue);
      let best: JsonObject | null = null;
      for (const entry of fields[field] ?? []) {
        const candidate = matchEntry(query, { ...entry, field }, index, activeGroups, lang);
        if (!candidate) continue;
        if (
          !best ||
          Number(candidate.strength) > Number(best.strength) ||
          (Number(candidate.strength) === Number(best.strength) &&
            (METHOD_PRIORITY[String(candidate.method)] ?? 0) > (METHOD_PRIORITY[String(best.method)] ?? 0))
        ) {
          best = candidate;
        }
      }
      if (!best) continue;
      const contribution = weight * Number(best.strength);
      score += contribution;
      if (["exact", "contains", "term_coverage"].includes(String(best.method))) directCount += 1;
      matches.push({ ...best, field, weight, contribution });
    }
    if (score >= minimum) {
      matches.sort((a, b) => Number(b.contribution) - Number(a.contribution));
      results.push({
        doc_id: doc.id,
        score: Number(score.toFixed(6)),
        direct_match_count: directCount,
        path: doc.path,
        title: doc.title,
        role: doc.role,
        state: doc.state,
        registration_state: doc.registration_state ?? doc.publication?.registration_state ?? "registered",
        publication: { ...(doc.publication ?? {}) },
        entry_level: doc.discovery?.entry_level ?? "",
        matches,
        active_expansion_groups: activeGroups,
      });
    }
  }

  results.sort((a, b) => {
    const scoreDelta = Number(b.score) - Number(a.score);
    if (scoreDelta !== 0) return scoreDelta;
    const directDelta = Number(b.direct_match_count) - Number(a.direct_match_count);
    if (directDelta !== 0) return directDelta;
    return lexicalCompare(String(a.doc_id), String(b.doc_id));
  });
  return { mode: resolvedMode, results: results.slice(0, limit) };
}

export function localizedValue(value: any, lang: string, fallback = ""): string {
  if (value && typeof value === "object" && !Array.isArray(value)) {
    if (lang === "en") return String(value.en || value.ja || fallback);
    return String(value.ja || value.en || fallback);
  }
  return String(value || fallback);
}

export function topicDocuments(index: JsonObject, topicId: string): JsonObject[] {
  const docs = (index.documents ?? [])
    .filter((doc: JsonObject) => (doc.discovery?.topics ?? []).includes(topicId))
    .map((doc: JsonObject) => ({ ...doc }));
  docs.sort((a: JsonObject, b: JsonObject) => {
    const levelA = ENTRY_LEVEL_ORDER[String(a.discovery?.entry_level ?? "")] ?? 3;
    const levelB = ENTRY_LEVEL_ORDER[String(b.discovery?.entry_level ?? "")] ?? 3;
    if (levelA !== levelB) return levelA - levelB;
    const titleA = normalizeText(a.title?.ja || a.title?.en || a.id || "");
    const titleB = normalizeText(b.title?.ja || b.title?.en || b.id || "");
    const titleDelta = lexicalCompare(titleA, titleB);
    return titleDelta !== 0 ? titleDelta : lexicalCompare(String(a.id ?? ""), String(b.id ?? ""));
  });
  return docs;
}

export function topicCard(index: JsonObject, topicId: string): JsonObject {
  const config = index.topics?.[topicId] ?? {};
  const browse = config.browse ?? {};
  const docs = topicDocuments(index, topicId);
  const counts: Record<string, number> = { foundation: 0, intermediate: 0, advanced: 0, unspecified: 0 };
  for (const doc of docs) {
    const level = String(doc.discovery?.entry_level ?? "");
    counts[["foundation", "intermediate", "advanced"].includes(level) ? level : "unspecified"] += 1;
  }
  const label = browse.label ?? {};
  const description = browse.description ?? {};
  const questions = browse.starter_questions ?? {};
  return {
    topic_id: topicId,
    base_label: { ja: String(config.ja ?? ""), en: String(config.en ?? "") },
    featured: Boolean(browse.enabled ?? false),
    order: Number(browse.order ?? 9999),
    label: { ja: String(label.ja || config.ja || ""), en: String(label.en || config.en || "") },
    description: { ja: String(description.ja ?? ""), en: String(description.en ?? "") },
    starter_questions: {
      ja: (questions.ja ?? []).map((value: any) => String(value)),
      en: (questions.en ?? []).map((value: any) => String(value)),
    },
    document_count: docs.length,
    entry_level_counts: counts,
  };
}

export function browseTopics(index: JsonObject, includeEmpty = false): JsonObject[] {
  const cards: JsonObject[] = [];
  for (const topicId of Object.keys(index.topics ?? {})) {
    const card = topicCard(index, topicId);
    if (!card.featured) continue;
    if (!includeEmpty && Number(card.document_count) === 0) continue;
    cards.push(card);
  }
  cards.sort((a, b) => Number(a.order) - Number(b.order) || lexicalCompare(String(a.topic_id), String(b.topic_id)));
  return cards;
}

export function documentBrowseSummary(doc: JsonObject): JsonObject {
  return {
    doc_id: String(doc.id ?? ""),
    title: { ...(doc.title ?? {}) },
    path: String(doc.path ?? ""),
    role: { ...(doc.role ?? {}) },
    registration_state: String(doc.registration_state ?? doc.publication?.registration_state ?? "registered"),
    publication: { ...(doc.publication ?? {}) },
    entry_level: String(doc.discovery?.entry_level ?? ""),
    reader_questions: { ...(doc.discovery?.reader_questions ?? {}) },
  };
}

export function browsePayload(index: JsonObject, topicId?: string): JsonObject {
  if (!topicId) {
    return {
      visibility_profile: index.source?.visibility_profile ?? "",
      topics: browseTopics(index),
    };
  }
  if (!(topicId in (index.topics ?? {}))) throw new Error(`Unknown topic: ${topicId}`);
  return {
    visibility_profile: index.source?.visibility_profile ?? "",
    topic: topicCard(index, topicId),
    documents: topicDocuments(index, topicId).map(documentBrowseSummary),
  };
}

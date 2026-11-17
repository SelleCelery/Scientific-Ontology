/** Read-only term lookup for a shared v5.1.x/v6 dictionary schema. */
const isAsciiWord = (char) => Boolean(char && /^[A-Za-z0-9_]$/.test(char));
const nfc = (value) => String(value ?? '').normalize('NFC');

export function createTermLookup(runtime) {
  if (runtime?.kind !== 'so.term_dictionary_runtime_seed' || !Array.isArray(runtime.entries)) {
    throw new Error('Unsupported dictionary runtime data');
  }
  const byForm = new Map();
  const byId = new Map();
  for (const entry of runtime.entries) {
    if (!entry?.id || !Array.isArray(entry.forms)) throw new Error('Malformed dictionary entry');
    if (byId.has(entry.id)) throw new Error('Duplicate dictionary ID: ' + entry.id);
    byId.set(entry.id, entry);
    for (const raw of entry.forms) {
      const form = nfc(raw).trim();
      if (!form) continue;
      if (!byForm.has(form)) byForm.set(form, []);
      if (!byForm.get(form).includes(entry.id)) byForm.get(form).push(entry.id);
    }
  }
  const forms = [...byForm.keys()].sort((a,b) => b.length - a.length || a.localeCompare(b, 'ja'));
  function exactSelection(selection) {
    const form = nfc(selection).trim();
    return (byForm.get(form) || []).map((id) => byId.get(id));
  }
  function matchCaret(text, offset) {
    const value = nfc(text);
    const position = Math.min(Math.max(0, Number(offset) || 0), value.length);
    for (const form of forms) {
      if (form.length < 2) continue; // A single-character headword needs explicit selection.
      for (let start = Math.max(0, position - form.length); start <= position && start + form.length <= value.length; start++) {
        const end = start + form.length;
        if (position < start || position > end || value.slice(start, end) !== form) continue;
        if (isAsciiWord(form[0]) && isAsciiWord(value[start - 1])) continue;
        if (isAsciiWord(form[form.length - 1]) && isAsciiWord(value[end])) continue;
        return {surface: form, start, end, candidates: byForm.get(form).map((id) => byId.get(id)),
                match_kind: 'literal_caret_candidate_not_sense_resolved'};
      }
    }
    return null;
  }
  return {byId, forms, exactSelection, matchCaret};
}

export function linksForTerm(overlay, termId, limit = 20) {
  const id = 'dictterm:' + termId;
  const nodeMap = new Map((overlay?.nodes || []).map((node) => [node.id, node]));
  const documents = [], terms = [], sources = [];
  for (const edge of overlay?.edges || []) {
    if (edge.from !== id) continue;
    const target = nodeMap.get(edge.to);
    if (!target) continue;
    if (edge.relation === 'surface_attested_in') {
      const result = {id: target.id, label: target.label ?? target.path, path: target.path,
                      kind: target.type, occurrences: edge.provenance.length, line: edge.provenance[0]?.line};
      if (target.type === 'registered_document_reference') documents.push(result);
      else sources.push(result);
    } else if (edge.relation === 'definition_lexically_mentions') {
      terms.push({id: target.dictionary_id, label: target.label, kind: 'lexical_surface_only'});
    }
  }
  return {documents: documents.slice(0, limit), terms: terms.slice(0, limit),
          unregisteredSources: sources.slice(0, limit)};
}

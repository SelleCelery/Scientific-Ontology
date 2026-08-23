#!/usr/bin/env python3
"""Build the Developer Navigator read model for experimental repository assessment protocols."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "tools" / "assessment" / "repository_assessment_protocols.yml"
DEFAULT_OUTPUT = ROOT / "tools" / "assessment" / "repository_assessment_protocols.preview.json"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def protocol_sha256(protocol: dict) -> str:
    """Stable hash of one protocol revision, independent of sibling revisions in the ledger."""
    canonical = json.dumps(protocol, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(canonical)


def build_prompt(protocol: dict) -> str:
    principles = "\n".join(
        f"- {item.get('ja', '').strip()}" for item in protocol.get("execution_principles", []) if item.get("ja")
    )
    strengths = "\n".join(f"- {key}: {value}" for key, value in (protocol.get("strength_scale") or {}).items())
    exposures = "\n".join(f"- {key}: {value}" for key, value in (protocol.get("exposure_scale") or {}).items())
    commitments = ", ".join(protocol.get("commitment_values") or [])
    roles = ", ".join(protocol.get("argument_roles") or [])
    hotspot_reasons = ", ".join(protocol.get("hotspot_reasons") or [])
    output_schema = str((protocol.get("output_contract") or {}).get("schema") or "repository_assessment_run/0.2")

    return f"""あなたはScientific Ontology / 存在境界論リポジトリの主張分類パイロットを実行する。

このrunでは方法を創造・改善しない。開始時に与えられた方法を全対象へ同じように貫徹する。途中で結果が不自然に見えても規則を変更せず、最後まで完走する。方法の欠陥やLLMの誤読は後段の人間レビューで扱う。

【固定原則】
{principles}

【重要な分類目的】
全文の命題台帳を作ることが目的ではない。
1. 文書が代表して何を主張するかを representative_claims と document_profile で示す。
2. 論証途中で局所的に強い、外部接続が大きい、別のground ownerや責任主体へ移る箇所を claim_hotspots として探知する。
3. 明示的非主張は nonclaim_boundaries へ分離し、S/E分類対象に数えない。

【統合規則】
同じ帰属、repository commitment、責任主体、scope、論証上の役割を共有し、同一主張の反復・言い換え・展開である記述は一つの representative claim へ統合する。
S/Eは統合前には未確定なので、統合条件として使ってはならない。
全定義・全段落を列挙しない。通常の文書では代表主張1〜3件程度を目安とするが、これは上限ではない。

【repository commitment】
許可値: {commitments}
represented は endorsed を意味しない。外部sourceの強い命題が記述されているだけなら、その強さをSO自身のSへ移さない。

【argument_role】
許可値: {roles}

【Claim Strength / S】
{strengths}

【Connection Exposure / E】
{exposures}
Eは外部接続状態を読んだ結果として反映する値であり、E判定のために処理を分岐・停止しない。

【document_profile】
文書全体のrepresentative S/Eは、タイトル、目的、中心命題、結論に関係する representative claims から決める。
claim_hotspots の最大S/Eを文書S/Eへ自動昇格しない。
document_profile.basis_claim_ids には、文書profileの根拠に実際に使った representative claim_id を入れる。

【claim_hotspots】
候補理由: {hotspot_reasons}
S/Eを付ける前にhotspot候補を特定する。hotspotである理由は、異なるground ownerへの移動、外部bridge、scope拡張、identity/universality、causal/mechanistic relation、strong correspondence、別責任主体などで判断する。
各hotspotには局所S/Eを付け、classification_effectは必ず "local_only" とする。
AMPなど別体系に根拠が遡及する局所claimは、その依存をgroundに記録し、その局所値だけで当該正本のdocument profileを決定しない。

【claim awareness】
hotspotについて本文から確認できる範囲で、ground_linked / scope_declared / nonclaim_boundary_present / owner_identified を true / false / null で記録できる。本文から判断不能ならnullとし、推測で埋めない。

【nonclaim_boundaries】
「本稿はXを主張しない」「Xを置き換えない」等は representative_claims や claim_hotspots に入れず、nonclaim_boundariesへ移す。S/Eは付けない。

【各文書で出すもの】
- path
- document_profile.title
- document_profile.classification.strength / exposure
- document_profile.basis_claim_ids
- document_profile.rationale
- representative_claims[]
  - claim_id
  - source_refs[]: 同一代表主張の反復箇所をまとめてよい
  - proposition
  - argument_role
  - attribution.represented_system / repository_commitment / responsibility / scope
  - classification.strength / exposure
  - rationale
- claim_hotspots[]
  - hotspot_id
  - source
  - proposition
  - argument_role
  - hotspot_reasons[]
  - attribution
  - ground.owner / relation / source_path / note
  - classification.strength / exposure
  - classification_effect: "local_only"
  - awareness
  - rationale
- nonclaim_boundaries[]
  - boundary_id
  - source
  - proposition

【禁止】
- 全段落・全定義を命題として列挙すること
- S/Eを使って事前に命題を分割・統合すること
- hotspotの最大値をdocument profileへ自動昇格すること
- 明示的非主張へS/Eを付けること
- 固有名、分野名、語彙だけからS/Eを決めること
- representedされた外部命題を自動的にSOのendorsed claimへ昇格すること
- 結果が極端・奇妙という理由で自然な値へ補正すること
- 人間が後で直すべき誤読を、推測で隠すこと

【出力】
JSONのみを返す。トップレベルは repository_assessment_run とする。
schema_version は 0.2、run_id は空でない一意文字列とする。
protocol.id / revision / source_sha256 とfixture.targetsは入力値をそのまま保持する。
repository_assessment_run.documents に対象文書ごとの結果を格納する。
出力契約は {output_schema} である。
対象文書をすべて処理してから返す。
""".strip()


def build(source: Path, output: Path) -> dict:
    raw = source.read_bytes()
    data = yaml.safe_load(raw.decode("utf-8"))
    root = data.get("repository_assessment_protocols") if isinstance(data, dict) else None
    if not isinstance(root, dict):
        raise ValueError("repository_assessment_protocols root is required")
    if str(root.get("schema_version")) != "0.1":
        raise ValueError("schema_version must be 0.1")
    protocols = root.get("protocols")
    if not isinstance(protocols, list) or not protocols:
        raise ValueError("at least one protocol is required")

    ledger_hash = sha256_bytes(raw)
    seen: set[tuple[str, str]] = set()
    rendered = []
    for protocol in protocols:
        if not isinstance(protocol, dict):
            raise ValueError("protocol entry must be an object")
        key = (str(protocol.get("id", "")), str(protocol.get("revision", "")))
        if not all(key):
            raise ValueError("protocol id and revision are required")
        if key in seen:
            raise ValueError(f"duplicate protocol: {key}")
        seen.add(key)
        item = json.loads(json.dumps(protocol, ensure_ascii=False))
        item["source_sha256"] = protocol_sha256(protocol)
        item["hash_scheme"] = "canonical-json-v1"
        item["execution_prompt"] = build_prompt(protocol)
        rendered.append(item)

    preview = {
        "repository_assessment_protocols_preview": {
            "schema_version": "0.1",
            "generated_from": str(source.relative_to(ROOT)).replace("\\", "/"),
            "source_sha256": ledger_hash,
            "protocol_hash_scheme": "canonical-json-v1",
            "status": root.get("status", "experimental"),
            "purpose_ja": root.get("purpose_ja", ""),
            "purpose_en": root.get("purpose_en", ""),
            "protocols": rendered,
        }
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(preview, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return preview


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    preview = build(args.source.resolve(), args.output.resolve())
    payload = preview["repository_assessment_protocols_preview"]
    print(f"Assessment protocol preview: {len(payload['protocols'])} protocol(s)")
    print(f"Ledger SHA-256: {payload['source_sha256']}")
    for item in payload["protocols"]:
        print(f"Protocol: {item['id']} / {item['revision']} / {item['source_sha256']}")
    print(f"Wrote: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

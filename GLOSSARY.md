# Glossary / 用語集

> Status: Glossary
> Scope: canonical public terminology / commensuration interface
> Language: Japanese authoritative; English commensurated rendering included
> Public profile: P0-P2
> Authority: Human-readable terminology interface; detailed definitions remain with canonical owner documents

## 0. 用語集の役割 / Role of This Glossary

この用語集は、存在境界論｜Scientific Ontology の公開語彙を、人間が参照できる形で正規化する。

個別概念の詳細定義は、各概念の正本所有文書にある。

`GLOSSARY.md`は、正本所有文書を置き換えない。用語の現在の標準表記、英語通約、公開上の注意、関連文書への入口を提供する。

機械可読な概念所有と文書関係は、[`tools/docs_manifest.yml`](./tools/docs_manifest.yml)で管理する。

通約方針は、[`Publication_and_Commensuration_Policy.md`](90_Repository_Governance/Publication_and_Commensuration_Policy.md)で管理する。

既存語との衝突は、[`TERM_COLLISION_REGISTRY.md`](90_Repository_Governance/Terminology/TERM_COLLISION_REGISTRY.ja.md)および[`TERM_COLLISION_REGISTRY.en.md`](90_Repository_Governance/Terminology/TERM_COLLISION_REGISTRY.en.md)で管理する。

This glossary normalizes the public vocabulary of Scientific Ontology for human readers.

It does not replace canonical concept-owner documents. It provides current standard forms, English commensurations, public-handling notes, and entry points to detailed documents.

---

## 1. 記載形式 / Entry Format

### 1.1 中核語

中核語には、必要に応じて次を付す。

- **Canonical Japanese**
- **English commensuration**
- **Concept ID**
- **Private lineage**
- **Public generative source**
- **Public definition owner**
- **Operationalized in**
- **Rendering distance**
- **Public handling**
- **Definition**
- **Not identical to**
- **Related terms**

### 1.2 補助語

補助語は簡略形式で記載する。

### 1.3 定義の優先順位

定義が競合した場合、次の順で照合する。

1. 公開定義所有者となる正本所有文書
2. 日本語正本
3. Glossary
4. 英語通約
5. 文書ローカルな説明

Glossaryと正本文書が食い違う場合、Glossaryを自動的な正解としない。差分を正本所有文書へ返す。

---

# Part I. Public Core Vocabulary / 公開中核語彙

## Scientific Ontology / 存在境界論

**Canonical Japanese:** 存在境界論  
**English commensuration:** Scientific Ontology  
**Legacy Japanese public name:** 存在論科学  
**Rendering distance:** R2  
**Public definition owner:** [`00_Overview/Scientific_Ontology_Concept_Network.ja.md`](./00_Overview/Scientific_Ontology_Concept_Network.ja.md)
**Private lineage:** AMP Core; ITS contributes a high-depth physical-phase lineage but does not govern the public definition.  
**Public generative source:** [`01_Sat_Truth/Boundary_Epistemological_Critique.ja.md`](./01_Sat_Truth/Boundary_Epistemological_Critique.ja.md); [`00_Overview/Scientific_Ontology_Concept_Network.ja.md`](./00_Overview/Scientific_Ontology_Concept_Network.ja.md)  
**Public definition owner:** [`00_Overview/Scientific_Ontology_Concept_Network.ja.md`](./00_Overview/Scientific_Ontology_Concept_Network.ja.md)  
**Operationalized in:** Overview documents, layer documents, Applications, and Research Notes across the repository.  

存在を直接所有または最終定義するのではなく、境界、接触、履歴、返り、後続条件を通じて、存在がどのように現れ、意味を持ち、他の存在へ作用するかを記述する公開概念体系。

A public conceptual system that does not claim final possession of existence itself, but describes how existence appears, acquires meaning, and affects other existences through boundaries, contact, history, return, and downstream conditions.

経験科学を置き換える統一理論ではない。

It is not a replacement for empirical science or a completed theory of everything.

---

## Boundary / 境界

**Canonical Japanese:** 境界  
**English commensuration:** Boundary  
**Concept ID:** `epistemic_boundary_conditions` / related public boundary concepts  
**Public definition owner:** [`01_Sat_Truth/Boundary_Realism_Principle.md`](./01_Sat_Truth/Boundary_Realism_Principle.md)  
**Rendering distance:** R1
**Private lineage:** AMP Core  
**Public generative source:** [`01_Sat_Truth/Boundary_Epistemological_Critique.ja.md`](./01_Sat_Truth/Boundary_Epistemological_Critique.ja.md)  
**Public definition owner:** [`01_Sat_Truth/Boundary_Realism_Principle.md`](./01_Sat_Truth/Boundary_Realism_Principle.md)  
**Operationalized in:** [`05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Organizational_Boundary_and_Port_Model.ja.md`](./05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Organizational_Boundary_and_Port_Model.ja.md); AI adaptation and social-boundary application documents.  

外部事象流、内部履歴、他者、制度、意味、観測が接触し、差分、摩擦、解釈、応答、責任が発生する成立面。

The operative surface at which external event-streams, internal history, other agents, institutions, meaning, and observation come into contact, generating difference, friction, interpretation, response, and responsibility.

境界は単なる線や壁ではない。通過、拒否、保持、変換、返送を行う機能を持つ。

A boundary is not merely a line or wall. It may admit, reject, retain, transform, or return what reaches it.

---

## Contact / 接触

**Canonical Japanese:** 接触  
**English commensuration:** Contact  
**Rendering distance:** R1
**Private lineage:** AMP Core  
**Public generative source:** [`01_Sat_Truth/Boundary_Epistemological_Critique.ja.md`](./01_Sat_Truth/Boundary_Epistemological_Critique.ja.md)  
**Public definition owner:** [`01_Sat_Truth/Boundary_Realism_Principle.md`](./01_Sat_Truth/Boundary_Realism_Principle.md)  
**Operationalized in:** Meaning-generation, history-field, organizational-boundary, and return-ethics documents.  

異なる履歴、場、主体、制度、情報が境界で相互に影響可能になる出来事。

An event in which distinct histories, fields, agents, institutions, or information structures become capable of affecting one another at a boundary.

接触は、統合や理解を意味しない。接触後に履歴が残る場合、完全な無関係へは戻れない。

Contact does not imply integration or understanding. Where history remains after contact, the participants cannot simply return to complete non-relation.

---

## History / 履歴

**Canonical Japanese:** 履歴  
**English commensuration:** History  
**Rendering distance:** R2  
**Public handling:** Not identical to chronology alone
**Private lineage:** AMP Core; ITS provides a high-depth history-field extension.  
**Public generative source:** [`01_Sat_Truth/Boundary_Epistemological_Critique.ja.md`](./01_Sat_Truth/Boundary_Epistemological_Critique.ja.md); [`02_Raj_Beauty/History_Field_Topology.md`](./02_Raj_Beauty/History_Field_Topology.md)  
**Public definition owner:** [`02_Raj_Beauty/History_Field_Topology.md`](./02_Raj_Beauty/History_Field_Topology.md)  
**Operationalized in:** Meaning generation, AI adaptation, return ethics, organizational boundary, and social-boundary design.  

接触、選択、応答、失敗、返りが残し、後続の観測、判断、意味、行為を変える持続的構造。

A persistent structure left by contact, selection, response, failure, and return that alters later observation, judgment, meaning, and action.

ここでの履歴は、単なる時系列記録ではない。

History in this framework is not merely chronological record.

---

## Return / 返り

**Canonical Japanese:** 返り  
**English commensuration:** Return  
**Rendering distance:** R2

接触または行為の結果が、元の主体、境界、制度、環境、未来世代、別の文書へ戻ってくること。

The reappearance of the consequences of contact or action at the originating agent, boundary, institution, environment, future generation, or upstream document.

返りは報復に限定されない。学習、感謝、損耗、残差、責任要求、環境負荷も含む。

Return is not limited to retaliation. It may include learning, gratitude, exhaustion, residuals, demands for responsibility, or environmental burden.

---

## Return Path / 返路

**Canonical Japanese:** 返路
**English commensuration:** Return Path
**Rendering distance:** R2-R3
**Public definition owner:** [`01_Sat_Truth/Boundary_Epistemological_Critique.ja.md`](./01_Sat_Truth/Boundary_Epistemological_Critique.ja.md)
**Operationalized in:** meaning generation, commensuration, provisional closure, language/meaning studies, organizational audit, and responsibility return.

差分、残差、異議、結果が、履歴更新、再照合、判断更新へ戻るために保持される経路。

A path through which differences, residuals, objections, or consequences can re-enter history, re-collation, or later judgment.

返路は、元の相手へ直接戻る経路だけを意味しない。記憶、記録、制度、作品、別の対話、将来の行為などを経由しても、差分が更新可能な履歴へ再接続できるなら返路として扱う。

A return path need not lead directly back to the original addressee. Memory, records, institutions, works, later conversations, or future action may function as detours when they reconnect a difference to an updatable history.

`返り`が戻ってくる結果や作用を指すのに対し、`返路`はその差分を再び照合・更新へ接続できる経路を指す。

`Return` names what comes back; `Return Path` names the route that keeps what returns reconnectable to collation and revision.

---

## Downstream Condition / 後続条件

**Canonical Japanese:** 後続条件  
**English commensuration:** Downstream Condition  
**Rendering distance:** R2

ある接触や判断によって、次の受け取り方、選択可能性、責任、意味づけが変化した状態。

A condition in which a prior contact or decision has altered later reception, available choices, responsibility, or meaning formation.

後続条件は、直接的な結果だけでなく、遅延して現れる制度的・身体的・環境的条件を含む。

It includes delayed institutional, bodily, and environmental conditions, not only immediate outcomes.

---

## Residual / 残差

**Canonical Japanese:** 残差  
**English commensuration:** Residual  
**Rendering distance:** R1  
**Public definition owner:** [`01_Sat_Truth/Boundary_Epistemological_Critique.ja.md`](./01_Sat_Truth/Boundary_Epistemological_Critique.ja.md)
**Private lineage:** AMP Core  
**Public generative source:** [`01_Sat_Truth/Boundary_Epistemological_Critique.ja.md`](./01_Sat_Truth/Boundary_Epistemological_Critique.ja.md)  
**Public definition owner:** [`01_Sat_Truth/Boundary_Epistemological_Critique.ja.md`](./01_Sat_Truth/Boundary_Epistemological_Critique.ja.md)
**Operationalized in:** Concept Network, commensuration policy, depth ports, organizational audit, and provisional closure.  

現在の分類、説明、プロトコル、通約では閉じられないが、将来の再照合へ保持できる未処理差分。

An unresolved difference that cannot be closed by the current classification, explanation, protocol, or commensuration, but can be retained for future re-collation.

残差は失敗そのものではない。残差を消したことにする処理が偽閉鎖を生む。

A residual is not itself a failure. Treating it as absent may produce false closure.

---

## Residue / 残渣

**Canonical Japanese:** 残渣  
**English commensuration:** Residue  
**Rendering distance:** R2
**Private lineage:** AMP Core  
**Public generative source:** [`01_Sat_Truth/Boundary_Epistemological_Critique.ja.md`](./01_Sat_Truth/Boundary_Epistemological_Critique.ja.md)  
**Public definition owner:** [`01_Sat_Truth/Boundary_Epistemological_Critique.ja.md`](./01_Sat_Truth/Boundary_Epistemological_Critique.ja.md)
**Operationalized in:** Return ethics, social-boundary notes, environmental return, and exchange-heat models.  

処理が終わったと宣言された後も、身体、制度、関係、環境、象徴、未来へ残り続ける履歴負荷。

A historical burden that persists in bodies, institutions, relationships, environments, symbols, or futures after a process has been declared complete.

`Residual`が再照合可能な未処理差分を指すのに対し、`Residue`は現実側へ沈殿した負荷を指す。

`Residual` refers to an unresolved difference retained for re-collation; `residue` refers to a burden already deposited in reality.

---

## Collation / 照合

**Canonical Japanese:** 照合  
**English commensuration:** Collation  
**Rendering distance:** R3  
**Public handling:** Not identical to simple comparison or synchronization
**Private lineage:** AMP Core  
**Public generative source:** [`01_Sat_Truth/Boundary_Epistemological_Critique.ja.md`](./01_Sat_Truth/Boundary_Epistemological_Critique.ja.md)  
**Public definition owner:** [`01_Sat_Truth/Boundary_Epistemological_Critique.ja.md`](./01_Sat_Truth/Boundary_Epistemological_Critique.ja.md)
**Operationalized in:** AI adoption collation, Concept Network, commensuration, Boundary CA, and public-format checking.  

異なる履歴、目的、境界、主張、観測結果を、差異を消さずに関係づけ、整合・不整合・未解決部分を確認する操作。

An operation that relates distinct histories, purposes, boundaries, claims, or observations without erasing their differences, in order to identify consistency, inconsistency, and unresolved regions.

照合は同期より強い。同期が同じ状態へ揃えることを含みうるのに対し、照合は異なるままの比較可能性を保持する。

Collation is stronger than synchronization in one respect: it preserves comparability without requiring the participants to become the same.

---

## Re-collatability / 再照合可能性

**Canonical Japanese:** 再照合可能性  
**English commensuration:** Re-collatability  
**Rendering distance:** R3
**Private lineage:** AMP Core  
**Public generative source:** [`01_Sat_Truth/Boundary_Epistemological_Critique.ja.md`](./01_Sat_Truth/Boundary_Epistemological_Critique.ja.md)  
**Public definition owner:** [`01_Sat_Truth/Boundary_Epistemological_Critique.ja.md`](./01_Sat_Truth/Boundary_Epistemological_Critique.ja.md)
**Operationalized in:** Provisional closure, public checker return paths, concept contracts, and organizational audit.  

仮閉鎖、翻訳、制度処理、判断の後でも、残差、履歴、異議を再び開き、正本または責任主体へ返せる性質。

The capacity to reopen residuals, history, or objections after provisional closure, translation, institutional processing, or judgment, and return them to a canonical source or responsible actor.

正しさの固定より、戻り方の安定を重視する概念である。

It prioritizes the stability of return over the permanent fixation of correctness.

---

## Provisional Closure / 仮閉鎖

**Canonical Japanese:** 仮閉鎖  
**English commensuration:** Provisional Closure  
**Rendering distance:** R2
**Private lineage:** AMP Core  
**Public generative source:** [`01_Sat_Truth/Boundary_Epistemological_Critique.ja.md`](./01_Sat_Truth/Boundary_Epistemological_Critique.ja.md)  
**Public definition owner:** [`01_Sat_Truth/Boundary_Epistemological_Critique.ja.md`](./01_Sat_Truth/Boundary_Epistemological_Critique.ja.md)
**Operationalized in:** Commensuration residual handling, depth ports, checklists, and managed non-closure.  

未解決を解決済みに見せず、一時的に破綻しない単位へ収納すること。

A temporary containment of unresolved material without presenting it as solved.

仮閉鎖は、未解決内容、再開条件、返路を記録する。

It records what remains unresolved, under what conditions it may be reopened, and where it returns.

---

## False Closure / 偽閉鎖

**Canonical Japanese:** 偽閉鎖  
**English commensuration:** False Closure  
**Former rendering:** False completion  
**Rendering distance:** R2
**Private lineage:** AMP Core  
**Public generative source:** [`01_Sat_Truth/Boundary_Epistemological_Critique.ja.md`](./01_Sat_Truth/Boundary_Epistemological_Critique.ja.md)  
**Public definition owner:** [`01_Sat_Truth/Boundary_Epistemological_Critique.ja.md`](./01_Sat_Truth/Boundary_Epistemological_Critique.ja.md)
**Operationalized in:** Public-format checking, organizational audit, AI adaptation, and truth management.  

未解決のものを、解決済み、理解済み、同意済み、完了済みとして扱う失敗。

A failure in which unresolved material is treated as solved, understood, accepted, or complete.

`False completion / 偽の完了`は旧説明語として参照できるが、標準語は`False Closure / 偽閉鎖`とする。

---

## Meaning Loop / 意味ループ

**Canonical Japanese:** 意味ループ  
**English commensuration:** Meaning Loop  
**Concept ID:** `meaning_generation`  
**Public definition owner:** [`01_Sat_Truth/Meaning_Generation_Model.md`](./01_Sat_Truth/Meaning_Generation_Model.md)  
**Rendering distance:** R2

情報が接触、受容、応答、返り、履歴化を通じて意味として成立する通信循環。

A communicative cycle through which information becomes meaning by contact, reception, response, return, and historical retention.

意味は情報そのものではない。情報が循環し、返り、履歴として後続条件を変えるとき、意味として作用する。

Meaning is not information alone. Information acts as meaning when it circulates, returns, remains as history, and changes downstream conditions.

---

## Qualia / クオリア

**Canonical Japanese:** クオリア  
**English commensuration:** Qualia  
**Rendering distance:** R3  
**Public handling:** Boundary-event interpretation; not asserted as a complete theory of consciousness
**Private lineage:** AMP Core; ITS contributes a field-oriented interpretation.  
**Public generative source:** [`01_Sat_Truth/Boundary_Epistemological_Critique.ja.md`](./01_Sat_Truth/Boundary_Epistemological_Critique.ja.md)  
**Public definition owner:** [`01_Sat_Truth/Boundary_Epistemological_Critique.ja.md`](./01_Sat_Truth/Boundary_Epistemological_Critique.ja.md)
**Operationalized in:** Meaning generation, cognitive-axis formation, literary reading, and AI-personality notes.  

外部入力または内部履歴が境界へ現れたときに生じる質感を伴う出来事。

A felt event generated when external input or internal history appears at a boundary.

本体系では、クオリアを純粋な私的内面物として所有せず、履歴が境界で質感として現れる出来事として扱う。

This framework does not treat qualia as purely private inner objects, but as boundary events in which history becomes felt.

---

# Part II. Cognitive Direction and Commensuration / 認識方向と通約

## Entropy-Attributed Difference / エントロピー属性つき差分

**Canonical Japanese:** エントロピー属性つき差分  
**English commensuration:** Entropy-Attributed Difference  
**Concept ID:** `entropy_attributed_difference`  
**Public definition owner:** [`02_Raj_Beauty/Entropy_Attributed_Difference_and_Cognitive_Axis_Formation.ja.md`](./02_Raj_Beauty/Entropy_Attributed_Difference_and_Cognitive_Axis_Formation.ja.md)  
**Rendering distance:** R3

差分を、単なる大小ではなく、処理負荷、予測不能性、意味圧、履歴依存性、変換可能性を伴うものとして扱う概念。

A concept that treats difference not merely as magnitude, but as carrying processing load, unpredictability, meaning pressure, history dependence, and transformability.

標準熱力学上のエントロピー量と同一ではない。

It is not identical to thermodynamic entropy.

---

## Cognitive Axis / 認識軸

**Canonical Japanese:** 認識軸  
**English commensuration:** Cognitive Axis  
**Concept ID:** `cognitive_axis_formation`  
**Public definition owner:** [`02_Raj_Beauty/Entropy_Attributed_Difference_and_Cognitive_Axis_Formation.ja.md`](./02_Raj_Beauty/Entropy_Attributed_Difference_and_Cognitive_Axis_Formation.ja.md)  
**Rendering distance:** R2

注意、抽象化、価値づけ、履歴、処理負荷が安定して形成する認識方向。

A direction of cognition stabilized through attention, abstraction, valuation, history, and processing load.

認識軸は人格診断や固定的類型ではない。

A cognitive axis is not a personality diagnosis or a permanent type.

---

## Cognitive Field / 認識場

**Canonical Japanese:** 認識場  
**English commensuration:** Cognitive Field  
**Concept ID:** `cognitive_field`  
**Public definition owner:** [`05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Cognitive_Dynamics_Communication_Model.ja.md`](./05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Cognitive_Dynamics_Communication_Model.ja.md)  
**Rendering distance:** R2-R3
**Public handling:** Conceptual model; not a field in standard physics or a completed cognitive-science theory

身体、感覚、履歴、注意、意味、関係、価値が、単純には分離できない状態で相互浸透的に作動する認識全体を指す操作的概念。

An operational concept for the interpenetrating whole of cognition in which body, sensation, history, attention, meaning, relation, and value cannot be cleanly separated.

物理学上の場、神経科学上の実体、固定された心理空間と同一ではない。

It is not identical to a physical field, a neuroscientific entity, or a fixed psychological space.

---

## Cognitive Phase / 認識相

**Canonical Japanese:** 認識相  
**English commensuration:** Cognitive Phase  
**Concept ID:** `cognitive_phase`  
**Public definition owner:** [`05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Cognitive_Dynamics_Communication_Model.ja.md`](./05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Cognitive_Dynamics_Communication_Model.ja.md)  
**Rendering distance:** R2-R3

認識場の中で、特定の目的、注意、身体状態、役割、履歴が優勢になり、一時的に安定した準安定的な認識構成。

A quasi-stable cognitive configuration that temporarily forms within a cognitive field when a particular purpose, attentional direction, bodily state, role, or history becomes dominant.

人格類型、発達段階、固定的な認知機能ではない。

It is not a personality type, developmental stage, or fixed cognitive function.

---

## Communication Phase / 通信位相

**Canonical Japanese:** 通信位相
**English commensuration:** Communication Phase
**Rendering distance:** R2-R3
**Public handling:** Cross-cutting research term; not identical to a phase in physics or signal engineering.

差分が、特定の文法、媒体、履歴、帯域、役割、返路条件のもとで、表現、送信、受容、照合、返送されるときの通信上の局所構成。

A local communicative configuration in which differences are expressed, transmitted, received, collated, and returned under particular grammatical, medial, historical, bandwidth, role, and return-path conditions.

通信位相は、通信内容そのものでも、固定された主体類型でもない。同じ内容でも、文法、媒体、受け手の履歴、帯域、返路条件が変われば、異なる通信位相として作用しうる。

A communication phase is neither the message content itself nor a fixed type of subject. The same content may operate differently when grammar, medium, recipient history, bandwidth, or return-path conditions change.

主要な研究入口は[`Language, Meaning, and Communication Phase Studies`](./05_Research_Notes/Language_Meaning_and_Communication_Phase_Studies/README.md)である。

The main research entrance is [`Language, Meaning, and Communication Phase Studies`](./05_Research_Notes/Language_Meaning_and_Communication_Phase_Studies/README.md).

---

## Operational Discretization / 操作的離散化

**Canonical Japanese:** 操作的離散化  
**English commensuration:** Operational Discretization  
**Concept ID:** `operational_discretization`  
**Public definition owner:** [`05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Cognitive_Dynamics_Communication_Model.ja.md`](./05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Cognitive_Dynamics_Communication_Model.ja.md)  
**Rendering distance:** R2

本来的に連続し相互浸透的な認識または存在を、通信、判断、責任、記録、実装のために、暫定的な操作単位へ切り出すこと。

The provisional cutting of continuous and interpenetrating cognition or existence into operational units for communication, judgment, responsibility, recording, or implementation.

対象が存在論的に離散部品から構成されているという主張ではない。

It does not claim that the underlying reality is ontologically composed of discrete modules.

---

## Existence Phase / 存在相

**Canonical Japanese:** 存在相  
**English commensuration:** Existence Phase  
**Concept ID:** `existence_phase`  
**Public definition owner:** [`05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Compression_of_Existence_Phases.ja.md`](./05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Compression_of_Existence_Phases.ja.md)  
**Rendering distance:** R2-R3

存在が特定の境界関係において持つ、役割、意味、責任、履歴、評価空間、時間射程の関係的なまとまり。

A relational configuration of role, meaning, responsibility, history, evaluative space, and time horizon that an existence holds within a particular boundary relation.

物質相、固定属性、人生段階の一覧と同一ではない。

It is not identical to a phase of matter, a fixed attribute, or a list of life stages.

---

## Existence-Phase Compression / 存在相圧縮

**Canonical Japanese:** 存在相圧縮  
**English commensuration:** Existence-Phase Compression  
**Concept ID:** `existence_phase_compression`  
**Public definition owner:** [`05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Compression_of_Existence_Phases.ja.md`](./05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Compression_of_Existence_Phases.ja.md)  
**Rendering distance:** R2-R3

複数の存在相を、一つまたは少数の評価軸へ集約し、比較、制度化、標準化、処理を可能にする境界操作。

A boundary operation that aggregates multiple existence phases into one or a small number of evaluative axes so that comparison, institutionalization, standardization, or processing becomes possible.

必要な圧縮と破壊的圧縮を区別し、失われる差分、適用範囲、外部化、再開条件を保持する。

It distinguishes necessary compression from destructive compression and retains the lost differences, scope, externalization, and reopening conditions.

---

## Optional Axiom Module / 選択公理モジュール

**Canonical Japanese:** 選択公理モジュール  
**English commensuration:** Optional Axiom Module  
**Concept ID:** `worldview_commensuration_protocol`  
**Public definition owner:** [`03_Tam_Goodness/Optional_Axiom_Modules_as_Cognitive_Bridge.ja.md`](./03_Tam_Goodness/Optional_Axiom_Modules_as_Cognitive_Bridge.ja.md)  
**Rendering distance:** R3

異なる認識形式または世界観を、同一化せず比較・通約・保留するために、一時的に採用する前提モジュール。

A provisional premise module used to compare, commensurate, or suspend distinct cognitive forms or worldviews without forcing them into identity.

相手を診断または思想分類するためのラベルではない。

It is not a label for diagnosing persons or ranking worldviews.

---

## Core Invariant / 中核不変項

**Canonical Japanese:** 中核不変項  
**English commensuration:** Core Invariant  
**Concept ID:** `core_invariant_and_operational_drift`  
**Public definition owner:** [`03_Tam_Goodness/Optional_Axiom_Modules_as_Cognitive_Bridge.ja.md`](./03_Tam_Goodness/Optional_Axiom_Modules_as_Cognitive_Bridge.ja.md)

表現、制度、運用が変化しても、その体系が同じ体系として残るために保持される中心条件。

A central condition that must be preserved for a framework to remain the same framework across changes in expression, institution, or operation.

---

## Operational Drift / 運用ドリフト

**Canonical Japanese:** 運用ドリフト  
**English commensuration:** Operational Drift

中核不変項を名目上保持しながら、実際の運用、権限、評価、負荷配分が別の方向へ移動すること。

A shift in actual operation, authority, evaluation, or burden distribution while the core invariant is nominally retained.

---

## Translation Residual / 通約残差

**Canonical Japanese:** 通約残差  
**English commensuration:** Commensuration Residual  
**Alternative:** Translation Residual  
**Rendering distance:** R3-R5

別言語または別の概念圏へ移す際、同一構造として保持できず、削除せずに残すべき差分。

A difference that cannot be preserved as the same structure when moving into another language or conceptual field and must therefore remain explicit rather than be erased.

---

## Conditional Connection / 条件付き接続

**Canonical Japanese:** 条件付き接続  
**English commensuration:** Conditional Connection

異なる体系が、全面統合ではなく、特定条件、目的、ポート、期間の範囲で接続すること。

A connection between distinct systems limited by specified conditions, purposes, ports, or time horizons rather than full integration.

---

## Commensuration / 通約

**Canonical Japanese:** 通約  
**English commensuration:** Commensuration  
**Public definition owner:** [`Publication_and_Commensuration_Policy.md`](90_Repository_Governance/Publication_and_Commensuration_Policy.md)  
**Rendering distance:** R0 as project term; R3 relative to ordinary translation vocabulary

概念所有、主張強度、非主張境界、残差、返路を保持しながら、別の言語圏・語彙圏へ概念構造を接続する操作。

An operation that connects a conceptual structure to another linguistic or terminological field while preserving concept ownership, claim strength, non-claim boundaries, residuals, and return paths.

---

## Rendering Distance / 通約距離

**Canonical symbol:** R  
**English commensuration:** Rendering Distance  
**Public definition owner:** [`Publication_and_Commensuration_Policy.md`](90_Repository_Governance/Publication_and_Commensuration_Policy.md)

中核語彙と通約先語彙の距離を示す補助軸。

A supplementary axis describing the distance between core vocabulary and rendered vocabulary.

Rは主張強度ではない。Rが高いほど、差分、非同一性、残差、返路の記録が必要になる。

R is not claim strength. Higher R requires stronger recording of difference, non-identity, residuals, and return paths.

---

# Part III. Purpose, Organization, and Implementation / 目的・組織・実装

## First Purpose / 第一義

**Canonical Japanese:** 第一義  
**English commensuration:** First Purpose  
**Concept ID:** `first_shared_and_world_forming_purpose`  
**Public definition owner:** [`00_Overview/Truth_Management_and_Boundary_PDCA.ja.md`](./00_Overview/Truth_Management_and_Boundary_PDCA.ja.md)  
**Rendering distance:** R3

何を守り、増やし、失ってはならないものとして置くかを決め、後続の制度、境界、責任、評価を方向づける目的。

A purpose that determines what is to be protected, increased, or treated as non-disposable, thereby directing later institutions, boundaries, responsibilities, and evaluation.

単なるKPIまたは短期目標ではない。

It is not merely a KPI or short-term target.

---

## Truth Management / 真理の経営学

**Canonical Japanese:** 真理の経営学  
**English commensuration:** Truth Management  
**Public definition owner:** [`00_Overview/Truth_Management_and_Boundary_PDCA.ja.md`](./00_Overview/Truth_Management_and_Boundary_PDCA.ja.md)

真理を正しい命題だけでなく、第一義の選択、共有、世界形成、境界CAによって管理されるものとして扱う方法論。

A methodology that treats truth not only as correct propositions, but as something operationally shaped through the selection of first purpose, sharing, world formation, and boundary CA.

---

## Boundary CA / 境界CA

**Canonical Japanese:** 境界CA  
**English commensuration:** Boundary CA  
**Concept ID:** `boundary_ca`  
**Public definition owner:** [`00_Overview/Truth_Management_and_Boundary_PDCA.ja.md`](./00_Overview/Truth_Management_and_Boundary_PDCA.ja.md)  
**Rendering distance:** R2

目的または運用の結果が、誰の境界へ、どの負荷として、どの返路を失って現れたかを確認し、目的または境界を再照合する操作。

An operation that examines at whose boundary the consequences of a purpose or operation have appeared, in what form of burden, and with which return paths lost, then re-collates the purpose or boundary.

PDCAを単純に置換する語ではない。

It is not a simple replacement term for PDCA.

---

## Organizational Boundary / 組織境界

**Canonical Japanese:** 組織境界  
**English commensuration:** Organizational Boundary  
**Concept ID:** `organizational_boundary`  
**Public definition owner:** [`05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Organizational_Boundary_and_Port_Model.ja.md`](./05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Organizational_Boundary_and_Port_Model.ja.md)

目的、責任、権限、通信、履歴、処理能力、返路を、組織として保持する境界。

A boundary that holds purpose, responsibility, authority, communication, history, processing capacity, and return paths as an organization.

法人格や部署境界だけを指さない。

It is not limited to legal personality or departmental borders.

---

## Responsibility Boundary / 責任境界

**Canonical Japanese:** 責任境界  
**English commensuration:** Responsibility Boundary  
**Concept ID:** `responsibility_boundary`  
**Public definition owner:** [`05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Organizational_Boundary_and_Port_Model.ja.md`](./05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Organizational_Boundary_and_Port_Model.ja.md)

誰が行為するかだけでなく、誰が目的を設定し、許可し、委任し、監督し、利益を受け、説明し、停止し、修正するかを定める境界。

A boundary that defines not only who acts, but who sets purpose, authorizes, delegates, supervises, benefits, explains, stops, and revises the action.

機能は委任できるが、責任を委任によって消去することはできない。

Functions may be delegated; responsibility may not be erased through delegation.

---

## Port / ポート

**Canonical Japanese:** ポート  
**English commensuration:** Port  
**Concept ID:** `operational_port`  
**Public definition owner:** [`05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Cognitive_Dynamics_Communication_Model.ja.md`](./05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Cognitive_Dynamics_Communication_Model.ja.md)  
**Rendering distance:** R2-R3

境界上の接触を、特定の目的、注意、履歴、責任条件のもとで受容、変換、返却できる有限な通信運用へ切り出す、暫定的で重複可能な操作単位。

A provisional and potentially overlapping operational unit that cuts contact at a boundary into a finite communication process capable of reception, transformation, and return under specified purpose, attention, history, and responsibility conditions.

ポートは境界そのもの、認識器官、固定人格類型、ネットワークポートと同一ではない。

A port is not identical to the boundary itself, a cognitive organ, a fixed personality type, or a network port.

---

## Organizational Port / 組織ポート

**Canonical Japanese:** 組織ポート  
**English commensuration:** Organizational Port  
**Concept ID:** `organizational_port`  
**Public definition owner:** [`05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Organizational_Boundary_and_Port_Model.ja.md`](./05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Organizational_Boundary_and_Port_Model.ja.md)  
**Rendering distance:** R2-R3

一般的なポート概念を、主体、権限、入力条件、変換、処理能力、プロトコル、ログ、監査、停止・再開条件を備えた組織上の通信口として実装したもの。

An organizational implementation of the general port concept with specified actors, authority, accepted inputs, transformations, processing capacity, protocols, logs, audit, and stop/reopen conditions.

組織ポートの実装可能性を、人間の認識が同じ離散構造を持つことの証明へ逆投影してはならない。

The implementability of an organizational port must not be projected backward as proof that human cognition has the same discrete structure.

---

## Port Allocation / ポート配分

**Canonical Japanese:** ポート配分  
**English commensuration:** Port Allocation  
**Concept ID:** `port_allocation`  
**Public definition owner:** [`05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Boundary_Diplomacy_and_Port_Allocation.ja.md`](./05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Boundary_Diplomacy_and_Port_Allocation.ja.md)  
**Rendering distance:** R2-R3

目的、緊急性、可逆性、処理能力、責任境界、外部化、再照合可能性に応じて、使用、保留、変換、遮断、再開するポートを動的に配分すること。

The dynamic allocation of ports to use, hold, transform, block, or reopen according to purpose, urgency, reversibility, processing capacity, responsibility boundaries, externalization, and re-collatability.

ネットワークポート番号または計算資源の技術的配分と同一ではない。

It is not identical to the technical assignment of network port numbers or computing resources.

---

## Multi-Port Potentiality / 複数ポート潜在性

**Canonical Japanese:** 複数ポート潜在性  
**English commensuration:** Multi-Port Potentiality  
**Concept ID:** `multi_port_potentiality`  
**Public definition owner:** [`05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Boundary_Diplomacy_and_Port_Allocation.ja.md`](./05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Boundary_Diplomacy_and_Port_Allocation.ja.md)  
**Rendering distance:** R2-R3

現在使用していない認識形式、言語ゲーム、責任経路、通信方法を消去せず、必要に応じて再開または新設できる状態。

A condition in which unused cognitive forms, language games, responsibility routes, and modes of communication are not erased and can be reopened or newly established when required.

すべてのポートを常時開放することではない。

It does not require all ports to remain permanently open.

---

## Scoped Port Operation / 限定ポート運用

**Canonical Japanese:** 限定ポート運用  
**English commensuration:** Scoped Port Operation  
**Concept ID:** `scoped_port_operation`  
**Public definition owner:** [`05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Boundary_Diplomacy_and_Port_Allocation.ja.md`](./05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Boundary_Diplomacy_and_Port_Allocation.ja.md)  
**Rendering distance:** R2

目的、範囲、期間、責任に応じて現在使用するポートを限定しつつ、対象外差分の保留先、返路、停止条件、再開条件を保持する運用。

An operation that limits currently active ports according to purpose, scope, duration, and responsibility while retaining holding destinations, return paths, stop conditions, and reopening conditions for differences outside the active scope.

対象外となった存在相を無価値または不存在として扱うことではない。

It does not treat existence phases outside the active scope as valueless or nonexistent.

---

## Boundary Diplomacy / 境界外交

**Canonical Japanese:** 境界外交  
**English commensuration:** Boundary Diplomacy  
**Concept ID:** `boundary_diplomacy`  
**Public definition owner:** [`05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Boundary_Diplomacy_and_Port_Allocation.ja.md`](./05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Boundary_Diplomacy_and_Port_Allocation.ja.md)  
**Rendering distance:** R2-R3

異なる境界系を同一化または内部化せず、それぞれの履歴、目的、言語ゲーム、責任境界を保持したまま通信可能性を維持する運用。

An operation that maintains communicability among distinct boundary systems without forcing identity or absorption, while preserving their histories, purposes, language games, and responsibility boundaries.

国家間外交の完成政策理論または合意製造技法ではない。

It is not a completed policy theory of international diplomacy or a technique for manufacturing agreement.

---

## Boundary Update / 境界更新

**Canonical Japanese:** 境界更新  
**English commensuration:** Boundary Update  
**Concept ID:** `boundary_update`  
**Public definition owner:** [`05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Organizational_Boundary_and_Port_Model.ja.md`](./05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Organizational_Boundary_and_Port_Model.ja.md)  
**Rendering distance:** R2

反復する異常、残差、責任不明、外部化を受け、現行の境界、役割、権限、ポート、プロトコル、監査を再構成すること。

The reconstruction of current boundaries, roles, authority, ports, protocols, and audit in response to recurring anomalies, residuals, unclear responsibility, or externalization.

単なるソフトウェア更新または形式的な組織改編ではない。

It is not merely a software update or formal organizational restructuring.

---

## Gateway Capture / ゲートウェイ捕捉

**Canonical Japanese:** ゲートウェイ捕捉  
**English commensuration:** Gateway Capture  
**Concept ID:** `gateway_capture`  
**Public definition owner:** [`05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Boundary_Diplomacy_and_Port_Allocation.ja.md`](./05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Boundary_Diplomacy_and_Port_Allocation.ja.md)  
**Rendering distance:** R2-R3

仲介者が通信路、翻訳基準、接続先を独占し、当事者間通信、残差の可視性、仲介者自身への監査可能性を縮小する失敗類型。

A failure mode in which an intermediary monopolizes communication routes, translation criteria, and destinations, reducing direct communication between parties, the visibility of residuals, and the auditability of the intermediary itself.

ネットワーク上のパケット取得だけを意味しない。

It is not limited to packet capture or another technical network attack.

---

## Single-Metric Compression / 単一指標圧縮

**Canonical Japanese:** 単一指標圧縮  
**English commensuration:** Single-Metric Compression  
**Concept ID:** `single_metric_compression`  
**Public definition owner:** [`05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Compression_of_Existence_Phases.ja.md`](./05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Compression_of_Existence_Phases.ja.md)  
**Rendering distance:** R2-R3

一つの外部指標を、複数の存在相、履歴、責任、時間射程の全体を代表するものとして扱う破壊的圧縮。

A destructive compression in which one external metric is treated as representing multiple existence phases, histories, responsibilities, and time horizons as a whole.

指標化一般を否定する語ではない。

It does not reject metrics or quantification in general.

---

## Protocol / プロトコル

**Canonical Japanese:** プロトコル  
**English commensuration:** Protocol

誰が、何を、どの条件で受け取り、どう変換し、どこへ渡し、何を記録し、いつ停止または再開するかを定める規則。

A rule specifying who receives what, under which conditions, how it is transformed, where it is routed, what is recorded, and when processing stops or reopens.

---

## Depth Port / 深度ポート

**Canonical Japanese:** 深度ポート  
**English commensuration:** Depth Port  
**Rendering distance:** R2-R3
**Public definition owner:** [`05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Organizational_Boundary_and_Port_Model.ja.md`](./05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Organizational_Boundary_and_Port_Model.ja.md)

現在の論理平面では処理できない問題を消去せず、残差、委譲先、返路、閉鎖権限の限界を保持して深度方向へ送るポート。

A port that sends a problem beyond the current logical plane without erasing it, while preserving residuals, delegation targets, return paths, and limits on closure authority.

深度ポートは単なる「後で考える」ではない。

A depth port is not merely a postponement marker.

---

## Open Marker

**Canonical Japanese:** Open Marker  
**English commensuration:** Open Marker

未解決、保留、条件付き、再開可能な事項を、完了扱いせず記録する公開実装マーカー。

A public implementation marker that records unresolved, suspended, conditional, or reopenable matters without treating them as complete.

---

## Audit of Audit / 監査の監査

**Canonical Japanese:** 監査の監査  
**English commensuration:** Audit of Audit

監査制度自体が持つ権限、死角、指標依存、報復リスク、変更不能性を監査すること。

The audit of the authority, blind spots, metric dependence, retaliation risk, and immutability of the audit system itself.

---

## Judgment Field / 判断場

**Canonical Japanese:** 判断場  
**English commensuration:** Judgment Field

主体が情報、履歴、異議、代替案、停止可能性に接触し、自分で判断できる状態を維持する場。

A field in which an agent can encounter information, history, objections, alternatives, and stop options while retaining the capacity to judge.

---

## AI Usefulness as Boundary Function / 境界機能としてのAI有用性

**Canonical Japanese:** 境界機能としてのAI有用性  
**English commensuration:** AI Usefulness as a Boundary Function  
**Public definition owner:** [`04_Applications/AI_Adaptation/AI_Usefulness_as_a_Boundary_Function.md`](./04_Applications/AI_Adaptation/AI_Usefulness_as_a_Boundary_Function.md)

AIの有用性を、判断代行ではなく、ユーザーの判断可能性が保たれる場を維持することとして定義する応用モデル。

An applied model that defines useful AI not as substitution for judgment, but as preservation of the field in which user judgment remains possible.

---

# Part IV. Ethics, Society, and Economy / 倫理・社会・経済

## Boundary Ethics / 境界倫理

**Canonical Japanese:** 境界倫理  
**English commensuration:** Boundary Ethics

倫理を、履歴を持つ存在どうしの非破壊的相互作用として扱うモデル。

An ethical model that treats ethics as non-destructive interaction between history-bearing existences.

危険な方向を止めることと、相手そのものを切断することを区別する。

It distinguishes stopping a dangerous direction from severing the person or existence itself.

---

## Non-destructive Distance / 非破壊的距離

**Canonical Japanese:** 非破壊的距離  
**English commensuration:** Non-destructive Distance

相手の履歴や存在を否定せず、接触頻度、近接度、権限、通信容量を下げる境界操作。

A boundary operation that reduces contact frequency, proximity, authority, or communication capacity without denying the other’s history or existence.

---

## Asymmetry Stabilization / 非対称性安定化

**Canonical Japanese:** 非対称性安定化  
**English commensuration:** Asymmetry Stabilization

能力、権力、情報、時間、責任の非対称性を消去せず、その差が搾取または破壊へ転化しないよう境界と返路を設計すること。

The design of boundaries and return paths that prevents asymmetries of capacity, power, information, time, or responsibility from becoming exploitation or destruction without pretending that the asymmetry does not exist.

---

## Return Ethics / 返りの倫理

**Canonical Japanese:** 返りの倫理  
**English commensuration:** Return Ethics

行為の結果、負荷、感謝、損耗、報復要求を、単純な切断や反撃ではなく、境界を通じて返送・変換・修復する倫理モデル。

An ethical model for returning, transforming, or repairing consequences, burdens, gratitude, exhaustion, and demands for retaliation through boundaries rather than simple severance or counterattack.

---

## Meaning-Experience Field / 意味・経験場

**Canonical Japanese:** 意味・経験場  
**English commensuration:** Meaning-Experience Field  
**Concept ID:** `meaning_experience_field`  
**Public definition owner:** [`04_Applications/Social_Boundary_Design/Specification_for_Peace.ja.md`](./04_Applications/Social_Boundary_Design/Specification_for_Peace.ja.md)  
**Rendering distance:** R2-R3
**Public handling:** Application concept; not a physical field

存在が差分を受け取り、履歴へ接続し、意味、判断、行為、応答へ変換し、外界へ返す循環を扱う応用概念。

An application concept for the cycle through which an existence receives differences, connects them to history, transforms them into meaning, judgment, action, or response, and returns them to the world.

標準物理学上の場、測定可能な心理空間、閉じた内面領域と同一ではない。

It is not identical to a field in standard physics, a measurable psychological space, or a closed inner domain.

---

## Meaning Capacity / 意味容量

**Canonical Japanese:** 意味容量  
**English commensuration:** Meaning Capacity  
**Concept ID:** `meaning_capacity`  
**Public definition owner:** [`04_Applications/Social_Boundary_Design/Specification_for_Peace.ja.md`](./04_Applications/Social_Boundary_Design/Specification_for_Peace.ja.md)  
**Rendering distance:** R2-R3

差分、矛盾、意味圧を、即座に切断、偽閉鎖、破壊的放電へ送らず、保留、通約、再構成のために保持できる能力。

The capacity to retain differences, contradictions, and meaning pressure for holding, commensuration, and reconstruction without immediately converting them into cutoff, false closure, or destructive discharge.

中核語は`Meaning Capacity`とする。一般概念を電気容量の`capacitance`と同一視しない。

The canonical general term is `Meaning Capacity`; the concept is not identical to electrical capacitance.

---

## Meaning-Experience Capacitor / 意味経験キャパシタ

**Canonical Japanese:** 意味経験キャパシタ  
**English commensuration:** Meaning-Experience Capacitor  
**Concept ID:** `meaning_experience_capacitor`  
**Public definition owner:** [`04_Applications/Social_Boundary_Design/Specification_for_Peace.ja.md`](./04_Applications/Social_Boundary_Design/Specification_for_Peace.ja.md)  
**Rendering distance:** R4  
**Public handling:** Structural analogy only

差分の保持、深度方向への移送、再構成、返路への放出を、キャパシタ構造との対応によって読む応用モデル。

An application model that reads the retention of differences, routing into depth, reconstruction, and release into return paths through structural correspondence with a capacitor.

電気的容量、熱力学的量、実在装置との物理的同一性を主張しない。

It does not claim physical identity with electrical capacitance, a thermodynamic quantity, or an actual device.

---

## Existence Strength / 存在強度

**Canonical Japanese:** 存在強度  
**English commensuration:** Existence Strength  
**Concept ID:** `existence_strength`  
**Public definition owner:** [`04_Applications/Social_Boundary_Design/Specification_for_Peace.ja.md`](./04_Applications/Social_Boundary_Design/Specification_for_Peace.ja.md)  
**Rendering distance:** R2-R3

存在が世界との相互作用を継続し、履歴、意味、関係、構造を形成、維持、更新し続ける能力を読む応用概念。

An application concept for the capacity of an existence to sustain interaction with the world and continue forming, maintaining, and revising histories, meanings, relations, and structures.

物理量、生物学的適応度、生命力、個人能力評価と同一ではない。

It is not identical to a physical quantity, biological fitness, vital force, or individual performance measure.

---

## Negentropy Economy / ネゲントロピー経済

**Canonical Japanese:** ネゲントロピー経済  
**English commensuration:** Negentropy Economy  
**Rendering distance:** R4  
**Public handling:** Conceptual model; not an empirical economic theory, thermodynamic proof, or policy proposal

経済の中心対象をお金そのものではなく、秩序を生む潜在性として扱う概念モデル。

A conceptual model that treats the primary economic object not as money itself, but as order-generating potential.

お金は交換媒質として扱い、価値は意味を帯びたネゲントロピーが交換面に現れた相として扱う。

Money is treated as an exchange medium, while value is treated as the exchange-facing appearance of meaning-bearing negentropy.

---

## Meaning-Bearing Negentropy / 意味を帯びたネゲントロピー

**Canonical Japanese:** 意味を帯びたネゲントロピー  
**English commensuration:** Meaning-Bearing Negentropy  
**Rendering distance:** R4

履歴、境界、関係、帰還可能性を通じて方向づけを持つ秩序生成潜在性。

Order-generating potential that carries orientation through history, boundary, relation, and possible return.

標準熱力学上の測定量ではない。

It is not a standard thermodynamic quantity.

---

## Exchange Medium / 交換媒質

**Canonical Japanese:** 交換媒質  
**English commensuration:** Exchange Medium

異なる価値構造または秩序生成構造を接続する媒質。

A medium that connects distinct value-bearing or order-generating structures.

ネゲントロピー経済では、お金を価値そのものではなく交換媒質として扱う。

In the Negentropy Economy model, money is treated as an exchange medium rather than value itself.

---

## Exchange Heat / 交換熱

**Canonical Japanese:** 交換熱  
**English commensuration:** Exchange Heat  
**Rendering distance:** R4

異なる秩序生成潜在性が交換されるときに生じる残差、摩擦、疲労、歪み、学習、余剰、変換を指す概念語。

A conceptual term for residuals, friction, exhaustion, distortion, learning, surplus, or transformation generated when distinct forms of order-generating potential are exchanged.

物理的な熱と同一ではない。

It is not identical to physical heat.

---

# Part V. Logical Depth and Research Vocabulary / 論理深度・研究語彙

## Logical-Depth Axis / 論理-深度軸

**Canonical Japanese:** 論理-深度軸  
**English commensuration:** Logical-Depth Axis  
**Rendering distance:** R3
**Private lineage:** AMP Core; ITS  
**Public generative source:** [`05_Research_Notes/Physical_Cosmological_Notes/Chaos_Theory_and_Logical_Depth_Axis.ja.md`](./05_Research_Notes/Physical_Cosmological_Notes/Chaos_Theory_and_Logical_Depth_Axis.ja.md)  
**Public definition owner:** [`05_Research_Notes/Physical_Cosmological_Notes/Chaos_Theory_and_Logical_Depth_Axis.ja.md`](./05_Research_Notes/Physical_Cosmological_Notes/Chaos_Theory_and_Logical_Depth_Axis.ja.md)  
**Operationalized in:** Depth ports, Concept Network, commensuration residual handling, and research-note architecture.  

整合性と正否を扱う平面的論理だけでは処理できない未解決、矛盾、分岐、残差、意味圧を保持し、再構成するための深度方向。

A depth direction for retaining and reconstructing unresolved questions, contradictions, branches, residuals, and meaning pressure that cannot be processed by plane-level logic concerned only with consistency and correctness.

外側の時計時間における前後そのものではない。

It is not itself chronological before-and-after in external clock time.

---

## Intrinsic Time / 内在時間

**Canonical Japanese:** 内在時間  
**English commensuration:** Intrinsic Time  
**Rendering distance:** R4-R5  
**Public handling:** High-depth research concept; publicly defined non-exhaustively  
**Private lineage:** ITS; AMP Core; PINGER particle model  
**Public generative source:** PINGER, logical-depth, and intrinsic-time research notes  
**Public definition owner:** Pending; no public document currently owns the complete high-depth definition  
**Operationalized in:** iMass/rMass, logical-depth, history-field topology, solitonic stability, communication-path, and meaning-loop models.  

内在時間は、履歴を持つ通信経路が返路を形成し、局所的な閉鎖、持続、現在断面の安定を生じさせるときに現れる深度秩序を扱う高深度研究概念である。

Intrinsic Time is a high-depth research concept concerning the depth-order that emerges when a history-bearing communication pathway forms a return path and produces local closure, persistence, and stabilization of a present section.

閉鎖は、形態、持続、到達可能性を説明する。一方、閉じない差分は、残差、分岐、論理-深度方向への再構成可能性を保持する。

Closure provides a way to describe form, persistence, and reachability, while differences that do not close remain as residuals, branches, and possibilities for reconstruction along the logical-depth direction.

内在時間は単一の公開機構へ固定しない。iMass、履歴閉鎖、返路、ソリトン的安定性、論理-深度の関係を探索するための生成的概念として保持する。

Intrinsic Time is not fixed to a single public mechanism. It is retained as a generative concept for exploring relations among iMass, historical closure, return paths, solitonic stability, and logical depth.

時計時間、主観時間、内的計数時間、標準物理学上の固有時と同一ではない。

It is not identical to clock time, subjective time, inner counted time, or proper time in standard physics.

---

## History-Field Topology / 履歴場トポロジー

**Canonical Japanese:** 履歴場トポロジー  
**English commensuration:** History-Field Topology  
**Rendering distance:** R4
**Private lineage:** ITS; AMP Core  
**Public generative source:** [`02_Raj_Beauty/History_Field_Topology.md`](./02_Raj_Beauty/History_Field_Topology.md)  
**Public definition owner:** [`02_Raj_Beauty/History_Field_Topology.md`](./02_Raj_Beauty/History_Field_Topology.md)  
**Operationalized in:** PINGER hypothesis, cosmological notes, AI-personality notes, and literary-ontological readings.  

履歴、境界、同期／非同期、エントロピー通信、履歴切断を通じて、物理、情報、生命、社会、AI、死生観を読む公開概念フレーム。

A public conceptual frame for reading physics, information, life, society, AI, and views of life and death through history, boundary, synchronization/asynchrony, entropy communication, and historical cutoff.

物理的証明ではない。

It is not a physical proof.

---

## HFC / 履歴場通信論

**Canonical English:** History-Field Communication  
**Canonical abbreviation:** HFC  
**Canonical Japanese:** 履歴場通信論
**Private lineage:** ITS; AMP Core  
**Public generative source:** [`02_Raj_Beauty/HFC_Introduction.md`](./02_Raj_Beauty/HFC_Introduction.md)  
**Public definition owner:** [`02_Raj_Beauty/HFC_Introduction.md`](./02_Raj_Beauty/HFC_Introduction.md)  
**Operationalized in:** AI adaptation, meaning-generation, social-boundary, and communication-analysis documents.  

言語、AI、社会、倫理、経験を、履歴を持つ場どうしの通信として扱う構築理論。

A constructive theory that treats language, AI, society, ethics, and experience as communication between history-bearing fields.

---

## Entropy Communication / エントロピー通信

**Canonical Japanese:** エントロピー通信  
**English commensuration:** Entropy Communication  
**Rendering distance:** R4
**Private lineage:** ITS; AMP Core  
**Public generative source:** [`02_Raj_Beauty/HFC_Introduction.md`](./02_Raj_Beauty/HFC_Introduction.md); [`02_Raj_Beauty/History_Field_Topology.md`](./02_Raj_Beauty/History_Field_Topology.md)  
**Public definition owner:** [`02_Raj_Beauty/HFC_Introduction.md`](./02_Raj_Beauty/HFC_Introduction.md)  
**Operationalized in:** AI-personality notes, history-field models, and cross-domain ethics.  

差異、ノイズ、未統合残差を、意味として閉じるか、保留するか、再符号化するか、切断するかの過程。

A process through which difference, noise, and unresolved residuals are closed into meaning, held open, re-encoded, or cut off.

標準熱力学または情報理論の定式化と同一ではない。

It is not identical to a standard thermodynamic or information-theoretic formalism.

---

## Entangle / エンタングル

**Canonical Japanese:** エンタングル  
**English commensuration:** Entangle  
**Rendering distance:** R4  
**Public handling:** Physics-adjacent ontological vocabulary
**Private lineage:** ITS  
**Public generative source:** [`00_Overview/Physics_Correspondence_Policy.ja.md`](./00_Overview/Physics_Correspondence_Policy.ja.md); history-field research notes  
**Public definition owner:** [`00_Overview/Physics_Correspondence_Policy.ja.md`](./00_Overview/Physics_Correspondence_Policy.ja.md)  
**Operationalized in:** History-field topology, PINGER hypothesis, literary reading, and AI-personality notes.  

相互作用履歴が場の構造内に保存され、以後の挙動、解釈、応答を拘束する状態。

A state in which interaction history persists within a field-like structure and constrains later behavior, interpretation, or response.

単なる社会的つながりの比喩ではなく、標準量子論上のエンタングルメントと同一の実証主張でもない。

It is neither a casual metaphor for social connection nor an empirical claim of identity with entanglement in standard quantum theory.

---

## History Mass Density / 履歴質量密度

**Canonical Japanese:** 履歴質量密度  
**English commensuration:** History Mass Density  
**Rendering distance:** R4
**Private lineage:** ITS  
**Public generative source:** History-field and AI-personality research notes  
**Public definition owner:** Public definition remains distributed; the current Glossary entry is provisional pending registry consolidation.  
**Operationalized in:** Meaning-loop and return-stability models.  

意味ループが経験、感情、思考、身体、記憶、行動と繰り返し接続することで獲得する概念的密度。

The conceptual density acquired by a meaning loop through repeated connection with experience, emotion, thought, body, memory, or action.

物理学上の質量密度ではない。

It is not physical mass density.

---

## Null / Void / 無

**Canonical Japanese:** 無  
**English commensuration:** Null / Void  
**Rendering distance:** R3-R4
**Private lineage:** AMP Core; ITS  
**Public generative source:** Boundary and history-field documents  
**Public definition owner:** Public definition remains distributed; the current Glossary entry is provisional pending registry consolidation.  
**Operationalized in:** Historical cutoff, meaning-loop failure, and cosmological research notes.  

履歴接続が破断し、意味ループを形成または維持できない状態。

A state in which historical connection is severed and a meaning loop cannot form or persist.

単なる不存在と同一ではない。

It is not identical to simple nonexistence.

---

# Part VI. High-Depth Axiomatic Identifiers and Exploratory Operators / 高深度の公理的識別子と探索演算子

AMP、ITS、iMass、rMass等の一部の高深度語彙は、完成した対象定義を与えるためだけの用語ではない。

これらは、複数の仮説、履歴構造、時間構造、通信構造、物理近接レンダリングを生成・接続・検査するための、公理的識別子兼探索演算子として用いられる。

ここでいう「公理的」は、数学的公理として無条件に真であることを意味しない。

一定の探究領域を開くために、その時点ではより下位の概念へ還元せず、生成的な起点として保持することを意味する。

公開文書では、次を明示できる。

- 概念の生成的系譜
- 対概念との関係
- 公開応用上の作用形態
- 他の概念を生成した経路
- 標準科学上の概念との非同一性
- 現在の非主張境界

一方、個別の作用形態を、その識別子全体の網羅的定義へ昇格させてはならない。

高深度識別子が非網羅的に記述されるのは、説明を拒否するためではない。

単一の公開レンダリングによって、探索可能性と概念生成力を偽閉鎖しないためである。

---

Some high-depth terms, including AMP, ITS, iMass, and rMass, are not used solely to provide completed object definitions.

They function as axiomatic identifiers and exploratory operators through which multiple hypotheses, historical structures, temporal structures, communication structures, and physics-adjacent renderings can be generated, connected, and examined.

Here, “axiomatic” does not mean unconditionally true in the mathematical sense.

It means that, within a specified domain of inquiry, the identifier is provisionally retained as a generative starting point rather than reduced immediately to lower-level concepts.

Public documents may state:

- generative lineage;
- relation to paired concepts;
- application-level manifestations;
- concepts and models generated from the identifier;
- non-identity with established scientific concepts; and
- current non-claim boundaries.

An individual manifestation must not be elevated into an exhaustive definition of the identifier as a whole.

The non-exhaustive public treatment of a high-depth identifier is not a refusal of explanation.

It is a safeguard against falsely closing its exploratory and concept-generating capacity through a single public rendering.

---

## AMP

**Canonical English:** Applied Metaphysics  
**Canonical abbreviation:** AMP  
**Public handling:** Private-core identifier; public summary only  
**Rendering distance:** R3
**Private lineage:** AMP Core itself  
**Public generative source:** Public summaries and boundary documents only; the full source remains non-public.  
**Public definition owner:** [`99_Private_Core_Not_Included/README.md`](./99_Private_Core_Not_Included/README.md) for the public boundary; this Glossary entry for the public identifier.  
**Operationalized in:** Public documents may cite derived concepts only through their public definition owners.  

存在境界論の形而上学的基礎OSを指す非公開中核識別子。

A private-core identifier for the metaphysical foundation OS of Scientific Ontology.

公開リポジトリはAMP Core全文を含まない。

The public repository does not include the full AMP Core.

---

## ITS

**Canonical English:** Information-Time Soliton Unified Theory  
**Canonical abbreviation:** ITS  
**Public handling:** Private high-depth theory; public references limited by claim strength  
**Rendering distance:** R4-R5
**Private lineage:** ITS itself; derived from AMP Core  
**Public generative source:** Physics Correspondence Policy and selected Research Notes  
**Public definition owner:** [`99_Private_Core_Not_Included/README.md`](./99_Private_Core_Not_Included/README.md) for the public boundary; this Glossary entry for the public identifier.  
**Operationalized in:** Intrinsic time, history-field topology, entropy communication, entangle, iMass, rMass, and high-depth research vocabulary.  

情報、時間、ソリトン的安定性、場、切断、観測、意味循環、iMass/rMass、通信インピーダンス、AMP Coreを扱う非公開高深度理論。

A private high-depth theory concerning information, time, solitonic stability, fields, slicing, observation, meaning circulation, iMass/rMass, communication impedance, and the AMP Core.

経験科学の代替または完全公開仕様として提示しない。

It is not presented as a replacement for empirical science or as a complete public specification.

---

## iMass

**Canonical English:** iMass  
**Primary etymological lineage:** imaginary-axis / imaginary-phase mass component  
**Secondary interpretive resonances:** information / inertia  
**Private lineage:** ITS; PINGER particle model  
**Rendering distance:** R4-R5  
**Public generative source:** PINGER and intrinsic-time research notes  
**Public definition owner:** Pending; no public document currently owns the complete high-depth definition

**Conceptual role:** Axiomatic high-depth identifier and exploratory operator  
**Public handling:** Application documents may describe operational manifestations of iMass, but must not treat any single manifestation as its exhaustive definition or exhaustively redefine the term.

iMassは、PINGER粒子モデルにおいて、虚数位相および内在時間方向に関係する質量成分として構想されたITS由来の概念である。実時間側の物理的慣性成分であるrMassと対をなす。

iMass is an ITS-derived concept originally conceived as the mass component associated with the imaginary-phase and intrinsic-time direction of the PINGER particle model. It is paired with rMass, the physical-inertial component on the real-time side.

情報慣性、履歴凝集、意味ループの持続性、通信インピーダンスは、iMassの公開応用上の作用形態であり、その生成的定義そのものではない。

Information inertia, history cohesion, meaning-loop persistence, and communication impedance are public application-level manifestations of iMass rather than exhaustive definitions of its generative structure.

**Not identical to:** imaginary mass in standard physics, tachyonic mass, complex mass in established physical theory, information quantity, or ordinary physical inertial mass.

iMassは、完成した対象定義として固定するためだけの語ではなく、内在時間、論理-深度、履歴凝集、通信、意味場等の関係を探索するための公理的識別子兼探索演算子として運用される。

iMass is not retained solely as a fixed object definition. It is also used as an axiomatic identifier and exploratory operator for investigating relations among intrinsic time, logical depth, history cohesion, communication, and meaning fields.

---

## rMass

**Canonical English:** rMass  
**Primary etymological lineage:** real-time / real-axis mass component  
**Private lineage:** ITS; PINGER particle model  
**Rendering distance:** R4-R5  
**Public definition owner:** Pending; no public document currently owns the complete high-depth definition

rMassは、PINGER粒子モデルにおいて、実時間側へ現れる物理的慣性質量成分を指すITS由来の概念である。

rMass is an ITS-derived concept for the physical-inertial mass component expressed on the real-time side of the PINGER particle model.

観測、切断、レンダリングによって現実断面へ固定されるという説明は、rMassの作用または出現形式を示すが、その語源的定義を尽くすものではない。

Its fixation within an observed or rendered section may describe a mode of appearance or operation, but does not exhaust its generative definition.

rMassは、モデルのレンダリングされた側面や物理的な慣性的な側面をiMassと比較するための、対応するリアルタイム側の識別子として保持される。

rMass is retained as the paired real-time-side identifier through which the rendered or physically inertial aspect of the model can be contrasted with iMass.

---

# Part VII. Layer and Repository Terms / 層・リポジトリ語彙

## Sat / Truth / 純・真

原理、認識成立条件、境界実在性、意味成立条件を扱う層。

The layer concerned with principles, epistemic conditions, boundary realism, and conditions of meaning formation.

---

## Raj / Beauty / 激・美

差分、注意、抽象化、認識方向、構築、動態を扱う層。

The layer concerned with difference, attention, abstraction, cognitive direction, construction, and dynamics.

---

## Tam / Goodness / 暗・善

通約、倫理、制御、プロトコル、実装境界、排熱、返路を扱う層。

The layer concerned with commensuration, ethics, control, protocols, implementation boundaries, exhaust handling, and return paths.

---

## Applications / 応用

公開概念を、AI、組織、社会境界、制度、チェックリスト、運用モデルへ実装する層。

The layer that operationalizes public concepts in AI, organizations, social boundaries, institutions, checklists, and implementation models.

---

## Research Notes / 研究ノート

主張強度の高い概念応用、試論的対応、物理・宇宙論的再解釈、文学的・社会的横断研究を置く層。

The layer for higher-claim-strength conceptual applications, speculative correspondences, physical or cosmological reinterpretations, and literary or social cross-domain research.

Research Notesの文書は、それ自体によって経験的証明または現代科学の代替になるわけではない。

Placement in Research Notes does not itself make a document empirical proof or a replacement for modern science.

---

# Part VIII. Governance Terms / 統治語彙

## Concept Owner / 概念所有者

ある概念の公開定義、射程、非主張境界を保持する正本文書。

The canonical document that owns the public definition, scope, and non-claim boundary of a concept.

Glossaryは概念所有者ではない。

The Glossary is not a concept owner.

---

## Public Profile / 公開プロファイル

文書またはディレクトリが、どの程度の公開負荷と誤読リスクを持つかを示す公開用分類。

A publication-facing classification indicating the public burden and misreading risk of a document or directory.

詳細は[`00_Overview/Claim_Strength_and_Publication_Layer_Table.md`](00_Overview/Claim_Strength_and_Publication_Layer_Table.ja.md)を参照する。

---

## Claim Strength / 主張強度

文書が、概念整理、方法論、仮説、存在論的提案、経験的主張のどの強さで述べられているかを示す軸。

An axis describing whether a document is making a conceptual, methodological, hypothetical, ontological, or empirical claim.

---

## Non-Claim Boundary / 非主張境界

文書が何を説明、証明、代替、保証しないかを明示する境界。

A boundary stating what a document does not explain, prove, replace, or guarantee.

---

## Aporia Registry / アポリア登録

現在の文書体系では閉じられず、概念ネットワーク上に未解決として保持される問いの登録。

The registration of questions that cannot be closed within the current document system and must remain open in the concept network.

---

## Deprecated Term / 旧語・非推奨語

現在の標準表記ではないが、過去文書との追跡可能性のため保持される語。

A former or non-preferred term retained for traceability to earlier documents.

旧語は[`TERM_COLLISION_REGISTRY.md`](90_Repository_Governance/Terminology/TERM_COLLISION_REGISTRY.ja.md)または変更履歴へ記録する。

---

## 2. Maintenance Rule / 運用上の注意

新しい公開概念を追加する場合、次を確認する。

1. 既存概念で表現できないか。
2. 正本所有文書はどこか。
3. Glossaryへ載せる必要があるか。
4. 文書ローカル語のままでよいか。
5. 英語通約語は安定しているか。
6. 既存学術語と衝突しないか。
7. R値を付す必要があるか。
8. 非主張境界が必要か。
9. manifestへ登録すべき共有概念か。
10. 旧語または別表記を残す必要があるか。

### v5開始時点でGlossaryへ昇格しない運用語

[`Scientific_Ontology_Operational_Outline.ja.md`](00_Overview/Scientific_Ontology_Operational_Outline.ja.md)で使用する`境界事件`、`可動性`、`責任分界`、`作用経路の地形`は、現時点では全体系の正規語彙として固定しない。運用アウトライン内の局所語として保持し、他文書で定義所有が必要になった時点でGlossary昇格を再検討する。

`Living Canonical`および`Return Intake`も、現時点では言語・意味・通信位相研究の保守運用語であり、存在境界論の中核概念とは扱わない。

用語集は、概念を増やすためではなく、概念間の境界と返路を保つために更新する。

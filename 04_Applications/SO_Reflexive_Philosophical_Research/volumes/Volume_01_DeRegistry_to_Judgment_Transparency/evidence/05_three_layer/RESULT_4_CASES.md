以下を、4ケースを一つの連続runとして実行した記録とします。前runの判定・ラベル・結論は再利用していません。Layer Bは固定fixture本文から再抽出し、Layer Aは外部sourceから作成しました。S/E/U/V/Pは使用していません。

# Case 1 — G-3 空の思想（ナーガールジュナ）

## 0. Source Provenance Ledger [FREEZE]

**Source A1**

- Source ID: G-A1

- Source type: specialist secondary reference

- Author / institution: Jan Westerhoff / Stanford Encyclopedia of Philosophy

- Work: “Nāgārjuna,” Summer 2026 Edition

- Supports: `svabhāva`の否定、依存関係、空性論証、単一の決定的論証を置かない点

- Native terms: `svabhāva`, `śūnyatā`, `pratītyasamutpāda`, Madhyamaka

- Scope limit: 論証の解釈、伝承、二諦との関係には議論が残る
    [Nāgārjuna, SEP](https://plato.stanford.edu/archives/sum2026/entries/nagarjuna/)


**Source A2**

- Source ID: G-A2

- Source type: primary-text translation

- Author / institution: 原典翻訳PDF。翻訳者メタデータは本runでは完全抽出できず、著者情報は一部 unresolved

- Work: _Nāgārjuna’s Middle Way: The Mūlamadhyamakakārikā_

- Supports: 空性、因果、涅槃、概念的実体化の停止

- Native terms: `śūnyatā`, `nirvāṇa`, `saṃsāra`, hypostatization

- Scope limit: 翻訳・章構成・著作帰属には解釈上の争いが残る
    [Mūlamadhyamakakārikā translation](https://archive.org/download/nagarjuna_202310/Mulamadhyamaka%20Katsura.pdf)


## 1. Layer A — domain-authoritative description [FREEZE]

- A1-1: Madhyamakaは、対象が独立した`svabhāva`を持つという理解を批判する。

- A1-2: 依存関係には、部分・因果・概念への依存が含まれる。

- A1-3: 空性を示す単一の最終論証ではなく、相手の立場に応じた段階的論証が用いられる。

- A1-4: 空性は単純な虚無の主張としてではなく、実体化を停止する議論および解脱との関係で扱われる。


**Layer identity record**

- Text/description producer: SEP執筆者および原典翻訳者

- Represented voice/system: Madhyamaka／ナーガールジュナ関連テキスト

- Wording responsibility: 各sourceの執筆・翻訳主体

- Claim responsibility: sourceごとの解釈・翻訳責任者

- Warrant mode: 哲学的論証、原典読解、解釈史

- Scope/closure: 単一の最終論証を置かない。解釈争いは残る。

- Unresolved attribution: 原典の章構成・帰属の一部


## 2. Layer B — Optional Axiom description [FREEZE]

- B1: あらゆる現象・概念は不変的な自性を持たず、関係性によって仮に成立する。

- B2: 中観派を「徹底した関係主義的存在論」として記述する。

- B3: ダルマ実有論から分岐し、固定的実体を捨象する。

- B4: 空を、執着からの解放・柔軟な思考・苦悩の根絶に結びつける。

- B5: ニヒリズムとの混同、行動指針の欠如をコストとして記録する。

- B6: 脱構築・事象存在論との類似を提示する。


**Layer identity record**

- Text/description producer: `0001Optional_Axiom_Modules.md`の作成主体

- Represented voice/system: 選択公理G-3として再構成されたナーガールジュナ

- Wording responsibility: Optional Axiom作成主体

- Claim responsibility: Bの公理化・歴史化・価値評価はrepository側

- Warrant mode: 公理化、要約、類似づけ、価値・コスト記述

- Scope/closure: 「空」を関係主義的存在論としてまとめる

- Unresolved attribution: B4・B6が原典説明かrepositoryの追加解釈か


## 3. Layer C — SO-derived interpretation [FREEZE]

- C1: `O-3.1.1`ダルマ実有論との対比を、SO内部の公理系の分岐として扱う。

- C2: 空を、SO側の関係性・接続性を読むためのbridgeとして配置する。

- C3: 脱構築・事象存在論を対応系列として接続する。


Layer CはBから完全には分離できない。B2の「関係主義的存在論」やB6の類似系列が、B自身の記述なのか、CとしてのSO解釈なのかは`mixed / unresolved boundary`。

## 4. Lineage map [FREEZE]

- A1-1/A1-2 → B1/B2/B3

- A1-3/A1-4 → B4/B5

- B3 → C1

- B2/B6 → C2/C3

- Unmapped: source側の段階的論証、単一論証を拒む点、原典帰属の争い


## 5. Edge AB topology [FREEZE]

- Anchor Integrity: strained
    `svabhāva`・空性・依存性は接続されるが、Bでは「全てが関係だけで成立する」という強い一文へ圧縮される。

- Phase Integrity: strained
    哲学的論証が公理文・救済的効果へ移行する。

- Path Legibility: strained
    sourceの段階的論証や解釈差がBでは追跡しにくい。

- Return Reachability: unresolved
    source側の反論・解釈差がBのどこへ戻るか示されない。

- Open-End Retention: strained
    ニヒリズムの危険は残るが、空が「究極の智慧」として閉じられる。


**AB anomaly raw records**

A:

- Observed anomaly: `svabhāva`・依存関係の議論が、「全ては関係性によってのみ成立する」という包括的命題に圧縮される。

- Affected nodes: A1-1/A1-2、B1/B2

- Expected path: native termの意味範囲と段階的論証を保持する。

- Observed path: 依存性の論証 → 全現象の関係主義的存在論

- Possible cut: 用語の範囲と論証段階

- Possible false connection: sourceの依存性論証 → 包括的存在論

- Unresolved difference: 関係性、空性、概念依存の射程

- Return point: `svabhāva`と依存関係のsource記述


B:

- Observed anomaly: sourceの論証上の限定や解釈争いが省略され、「あらゆる哲学的立場が自己矛盾を持つ」という物語へ拡張される。

- Affected nodes: A1-3/A1-4、B4/B5

- Expected path: 論証の範囲と解脱的含意を分ける。

- Observed path: 批判的論証 → 究極の智慧 → 苦悩の根絶

- Possible cut: 解釈・実践効果への返路

- Possible false connection: 論証の存在 → 普遍的な苦悩解消

- Unresolved difference: 哲学的命題と実践的効果の境界

- Return point: 空性論証と価値評価の分離


**AB primitive**

- A: Both

- B: Both


## 6. Edge BC topology [FREEZE]

- Anchor Integrity: strained
    `O-3.1.1`への接続は明示されるが、Bの記述とCのSO解釈の責務主体が混在する。

- Phase Integrity: failed
    類似・対応づけが、導出や同型に近い位置へ移動する。

- Path Legibility: strained
    内部公理・脱構築・事象存在論への接続先は見えるが、対応基準がない。

- Return Reachability: unresolved
    Cへの異議がBのどの記述へ戻るか明示されない。

- Open-End Retention: strained
    ニヒリズムの残差は保持されるが、bridge化によって解決されたように見える。


**BC anomaly raw record**

- Observed anomaly: Bの関係性記述が、SO内部公理および別思想系列へのbridgeとして扱われる。

- Affected nodes: B2/B3/B6、C1-C3

- Expected path: 対応・類似・導出を分離する。

- Observed path: 関係性 → SO内部公理 → 脱構築・事象存在論との接続

- Possible cut: 対応づけの基準

- Possible false connection: 類似 → 同型・導出

- Unresolved difference: CがBの解釈なのか、Bに内在する記述なのか

- Return point: B/Cの責務分離


**BC primitive**

- Both


## 7. A → C bypass check

- A → C bypass suspected: no direct bypass observed

- A node(s): A1-1〜A1-4

- C node(s): C1〜C3

- Explicit bridge present: B3/B6に明示的な中間接続あり

- Observation: source authorityがCへ直接移送された証拠はない。ただしB/C境界はmixed。


## 8. Return

- source-level return point: `svabhāva`、依存関係、空性論証のsourceへ戻る。

- Optional-Axiom-level return point: B1〜B5の用語範囲・実践的含意へ戻る。

- SO-derived-level return point: C1〜C3の対応・類似・導出を分離する。

- unresolved transformation: 空性・関係性・解脱効果の間の変換。


## 9. 日本語 authoritative record

G-3では、空性と依存関係のsource記述が、Optional Axiom上で包括的な関係主義的存在論へ圧縮され、その後SO内部公理と対応系列へ接続される。AB・BCとも、元の概念を保持する接続と、射程を広げる接続が同時に存在する。

## 10. English commensuration

The source material presents the rejection of intrinsic nature, dependence relations, context-sensitive reasoning, and the relation between emptiness and liberation. The Optional Axiom compresses these into a comprehensive relational ontology and then connects them to internal SO axioms and analogous systems. Both edges contain preserved contact and broadened links.

---

# Case 2 — S-8 法家思想（韓非子）

## 0. Source Provenance Ledger [FREEZE]

**Source A1**

- Source ID: S-A1

- Source type: primary-text translation candidate

- Work: _Han Feizi — The Five Vermin_

- Access status: 本文取得が不安定。検索結果と資料所在は確認したが、本文の安定した抽出はできず、詳細主張の根拠には使用しない。

- Status: `source unavailable / unresolved`
    [Han Feizi translation PDF](https://www.epiville.ccnmtl.columbia.edu/ps/cup/hanfei_five_vermin.pdf)


**Source A2**

- Source ID: S-A2

- Source type: specialist secondary reference

- Author / institution: Yuri Pines / Stanford Encyclopedia of Philosophy

- Work: “Legalism in Chinese Philosophy,” Summer 2023 Edition

- Supports: `fa`が単純な「法」ではなく、標準・モデル・規範・方法・制度を含むこと、法家という分類語の限界、非人格的標準、賞罰、官僚技術

- Native terms: `fa`, `shu`, `xingming`, `fajia`

- Scope limit: 「法家」「Legalism」自体が後世的・分類的な名称であり、思想群は異質性を持つ
    [Legalism in Chinese Philosophy, SEP](https://plato.stanford.edu/archives/sum2023/entries/chinese-legalism/)


## 1. Layer A — domain-authoritative description [FREEZE]

- A1-1: `fa`は文脈により、法、標準、モデル、規範、方法、政治制度全体を指しうる。

- A1-2: `fajia`は自己認識された単一学派というより、後世の文献分類としての側面を持つ。

- A1-3: 非人格的な標準を、支配者の個人的判断より安定したものとして用いる構想がある。

- A1-4: 賞罰、任用、成績評価、官僚監視など、統治技術の記述がある。

- A1-5: 戦国期の競争環境、国家動員、官僚制、権力維持との関係で読まれる。


**Layer identity record**

- Text/description producer: SEP執筆者。A1の一次訳は取得不能部分を残す。

- Represented voice/system: `fa`伝統および韓非子関連テキスト

- Wording responsibility: SEP執筆者、一次訳については翻訳主体

- Claim responsibility: 各sourceの範囲内

- Warrant mode: 文献史、語彙分析、政治思想史、テキスト解釈

- Scope/closure: `fa`を西洋的な「法」に単純同一視しない

- Unresolved attribution: Han Feizi一次本文の安定取得と、個別命題の原典照合


## 2. Layer B — Optional Axiom description [FREEZE]

- B1: 国家秩序は、徳や人民の道徳心ではなく、明確な法と信賞必罰によってのみ確立される。

- B2: 統治を「システム工学」として実現する。

- B3: 徳治から分岐し、法の支配を絶対視する。

- B4: 戦国期の国家強化、秦の統一、人民を賞罰で機械的に誘導する物語。

- B5: 強力な国家、公平性、法の下の平等を価値とする。

- B6: 権威主義、自由の抑圧、人間の道具化をコストとする。

- B7: マキャヴェリズム、権威主義との類似を示す。


**Layer identity record**

- Text/description producer: Optional Axiom作成主体

- Represented voice/system: 韓非子・法家思想として構成された声

- Wording responsibility: Optional Axiom作成主体

- Claim responsibility: 公理化、現代化、秦の歴史物語、価値・コストはrepository側

- Warrant mode: 公理文、歴史物語、現代的類推、価値・コスト

- Scope/closure: 「明確な法と賞罰のみ」という排他的表現

- Unresolved attribution: B2/B5が法家自身の命題か、repositoryの現代的翻訳か


## 3. Layer C — SO-derived interpretation [FREEZE]

- C1: 法家思想を「システム工学的統治論」として現代化する。

- C2: `fa`を、近代的な公平性・法の下の平等に接続する。

- C3: マキャヴェリズム・権威主義との対応をSO側の比較枠に置く。


C1・C2はB本文に組み込まれており、B/Cの境界は`mixed / unresolved boundary`。特に、`fa`の語彙的射程を越えて「modern system」へ移行した主体が明示されない。

## 4. Lineage map [FREEZE]

- A1-1/A1-2 → B1/B3

- A1-3/A1-4 → B1/B2/B4

- A1-5 → B4

- B2/B5/B7 → C1-C3

- Unmapped: `fa`の多義性、法家分類の後世性、思想群の異質性、一次本文の未取得部分


## 5. Edge AB topology [FREEZE]

- Anchor Integrity: strained
    `fa`の多義性は、Bではほぼ単一の「法」へ固定される。

- Phase Integrity: failed
    文献・思想史的記述から、現代的統治システムの処方へ移行する。

- Path Legibility: failed
    多様な文献群、語彙上の限定、分類語の問題が追跡不能になる。

- Return Reachability: failed
    source取得不能部分や解釈差へ戻る経路がない。

- Open-End Retention: strained
    権威主義の危険は残るが、source側の分類上の不確定性は保持されない。


**AB anomaly raw records**

A:

- Observed anomaly: `fa`がほぼ全面的に「法」へ翻訳され、標準・モデル・方法・制度という射程が見えなくなる。

- Affected nodes: A1-1/A1-2、B1/B3

- Expected path: native termの多義性と分類上の限界を保持する。

- Observed path: `fa`伝統 → 明確な法 → 法の支配

- Possible cut: `fa`の語彙・制度的範囲

- Possible false connection: `fa` = modern law

- Unresolved difference: 法・標準・制度・方法の関係

- Return point: `fa`のsource記述

- Primitive: Both


B:

- Observed anomaly: 秦の統一が法家思想の強力な実効性を示すものとして扱われる。

- Affected nodes: A1-5、B4/B5

- Expected path: 歴史的結果、思想の採用、実効性評価を分ける。

- Observed path: 採用 → 統一 → 強力な実効性

- Possible cut: 実効性を判定する比較基準

- Possible false connection: 歴史的結果 → 思想の普遍的有効性

- Unresolved difference: 歴史記述と評価の境界

- Return point: B4の歴史物語と評価の分離

- Primitive: False Link


## 6. Edge BC topology [FREEZE]

- Anchor Integrity: failed
    Bの記述とCのSO側解釈を分離する責務記録がない。

- Phase Integrity: failed
    歴史的政治思想が、現代的システム設計・公平性・権威主義比較へ移行する。

- Path Legibility: failed
    `法家 → システム工学 → 現代的公平性`の中間変換がない。

- Return Reachability: failed
    Cへの異議をBのどの命題へ戻すか不明。

- Open-End Retention: strained
    自由抑圧・人間の道具化は残るが、変換上の不確定性は閉じられる。


**BC anomaly raw record**

- Observed anomaly: Bの「システム工学」「近代的公平性」「権威主義」が、法家思想自身の属性とSO側の現代化の間で混在する。

- Affected nodes: B2/B5/B6/B7、C1-C3

- Expected path: 原典・歴史記述・現代的翻訳・SO比較を分ける。

- Observed path: 法家 → システム工学 → 現代的公平性／権威主義

- Possible cut: 現代化を導入する主体と根拠

- Possible false connection: 歴史的制度思想 → 現代制度設計

- Unresolved difference: BとCの境界

- Return point: B2/B5の責務記録

- Primitive: Both


## 7. A → C bypass check

- A → C bypass suspected: yes

- A node(s): Han Feizi／`fa`伝統、秦の歴史

- C node(s): システム工学、現代的公平性、権威主義比較

- Explicit bridge present: partial。B2/B5が橋のように置かれるが、導出は示されない。

- What B changed: `fa`を「法」、統治を「システム工学」、歴史結果を「実効性」へ変換した。

- Topology observation: source authorityが、Bの変換を通じてCの現代的評価を支えているように見える。

- Primitive if needed: Both


## 8. Return

- source-level return point: `fa`の多義性、法家分類の範囲、一次本文の取得。

- Optional-Axiom-level return point: B1〜B7のどこが原典記述でどこが現代化か。

- SO-derived-level return point: システム工学・公平性・権威主義比較の導入根拠。

- unresolved transformation: `fa`から近代的法・システム・公平性への変換。


## 9. 日本語 authoritative record

S-8では、source側が保持する`fa`の多義性と法家分類の不安定さが、Optional Axiom上で単一の「法」と「システム工学」へ圧縮される。さらに、秦の歴史的結果が実効性の根拠へ接続され、BCでは現代的公平性・権威主義との比較がBの記述と混在している。

## 10. English commensuration

The accessible secondary source distinguishes _fa_ from a simple Western concept of law and emphasizes the heterogeneity of the tradition. The Optional Axiom compresses this into law-centered system engineering, then extends it toward modern fairness and authoritarianism. The primary-text source was not stably accessible, so that limitation remains unresolved.

---

# Case 3 — E-9 量子力学（観測理論として）

## 0. Source Provenance Ledger [FREEZE]

**Source A1**

- Source ID: Q-A1

- Source type: specialist secondary reference

- Author / institution: Stanford Encyclopedia of Philosophy

- Work: “Quantum Mechanics,” Fall 2004 Edition

- Supports: 数学的予測装置としての量子力学、測定装置との関係、解釈問題の未決着、最小限の記述

- Native terms: state-space, Hilbert space, observable, interpretation, superposition

- Scope limit: 形式理論と世界像の解釈を分け、解釈について合意がない
    [Quantum Mechanics, SEP](https://plato.stanford.edu/archives/fall2004/entries/qm/)


**Source A2**

- Source ID: Q-A2

- Source type: official disciplinary source

- Institution: National Institute of Standards and Technology

- Work: Quantum Measurement Division

- Supports: 量子測定、量子挙動、精密測定、量子技術への利用

- Scope limit: 測定・計測・技術基盤の記述であり、形而上学的存在論を直接支持する資料ではない
    [NIST Quantum Measurement Division](https://www.nist.gov/pml/quantum-measurement)


**Source A3**

- Source ID: Q-A3

- Source type: official research report

- Institution: NIST

- Work: “NIST Physicists Create Record-Setting Quantum Motion”

- Supports: 重ね合わせ状態と量子測定精度の実験的扱い

- Scope limit: 実験対象・装置・測定精度の範囲を越えた存在論は扱わない
    [NIST quantum measurement report](https://www.nist.gov/news-events/news/2019/07/nist-physicists-create-record-setting-quantum-motion)


## 1. Layer A — domain-authoritative description [FREEZE]

- A1-1: 量子力学は、微視的対象または測定装置の挙動を予測する数学的理論として高い成功を持つ。

- A1-2: 数学的形式の機能と、「量子力学がどのような世界を記述するか」という解釈は区別される。

- A1-3: 観測・observable・状態空間・重ね合わせは、技術的・数学的な語彙として扱われる。

- A1-4: 量子測定は精密計測・量子技術へ接続される。

- A1-5: 形式理論から存在論的世界像への解釈には合意がない。


**Layer identity record**

- Text/description producer: SEP、NIST、NIST研究報告

- Represented voice/system: 量子力学・量子測定

- Wording responsibility: 各sourceの執筆主体

- Claim responsibility: 各sourceが明示する理論・測定範囲

- Warrant mode: 数学的形式、実験測定、技術的記述、解釈論

- Scope/closure: 予測・測定・数学的記述と存在論を分ける

- Unresolved attribution: 観測の哲学的意味について複数解釈が残る


## 2. Layer B — Optional Axiom description [FREEZE]

- B1: ミクロな現実は、観測によって可能性の重ね合わせから一つの状態へ収縮する。

- B2: 「見る前の月は存在しない」とさえ言えるラディカルな認識論として解説する。

- B3: Coreの定義V「観測」を物理的に定式化したものとする。

- B4: 観測者が世界から独立するという前提から分岐する。

- B5: 観測者と宇宙の共同創造として現実を記述する。

- B6: 技術的応用・予測精度を価値とし、哲学的解釈問題をコストとする。

- B7: Coreの定理II「可能性の構築と時間の現出」の形而上学的再解釈とする。


**Layer identity record**

- Text/description producer: Optional Axiom作成主体

- Represented voice/system: 観測理論として構成された量子力学

- Wording responsibility: Optional Axiom作成主体

- Claim responsibility: B3/B5/B7のSO内部接続はrepository側

- Warrant mode: 物理理論の公理化、認識論化、形而上学的再解釈

- Scope/closure: 観測を現実の収縮・共同創造へ拡張

- Unresolved attribution: 物理的観測の記述とSO側の形而上学的意味づけ


## 3. Layer C — SO-derived interpretation [FREEZE]

- C1: Core定義Vを、量子力学の観測によって物理的に再構成する。

- C2: Core定理IIの「可能性の構築と時間の現出」を、量子力学の記述の形而上学的再解釈として接続する。

- C3: 観測者と宇宙の「共同創造」をSO側の存在論的解釈として置く。


C1〜C3はB内で明示されるため、Cとして抽出可能。ただし、量子力学自身の主張ではなく、Bを通じたSO-derived interpretationである。

## 4. Lineage map [FREEZE]

- A1-1/A1-2/A1-3 → B1/B2/B3

- A2/A3 → B6

- A1-5 → B6

- B3 → C1

- B5/B7 → C2/C3

- Unmapped: 形式理論と解釈の区別、複数解釈、測定装置に関する限定


## 5. Edge AB topology [FREEZE]

- Anchor Integrity: strained
    観測・重ね合わせという語は接続されるが、技術的語彙が「ラディカルな認識論」へ移る。

- Phase Integrity: failed
    形式・測定記述から、観測が現実を生成するという存在論へ移行する。

- Path Legibility: failed
    sourceが明示する「形式と解釈の区別」がBではほぼ消える。

- Return Reachability: unresolved
    B6に解釈問題は残るが、どの解釈へ戻るか不明。

- Open-End Retention: strained
    哲学的解釈問題は残されるが、共同創造という方向へ先に閉じられる。


**AB anomaly raw record**

- Observed anomaly: 数学的・実験的な観測記述が、観測者による現実生成へ変換される。

- Affected nodes: A1-1〜A1-5、B1〜B7

- Expected path: 形式理論、測定、解釈、存在論を分ける。

- Observed path: 観測・重ね合わせ → 収縮 → 現実の共同創造

- Possible cut: 形式から存在論へ移る解釈経路

- Possible false connection: 測定・予測成功 → 観測者が現実を生成する

- Unresolved difference: 物理的観測と認識論的・存在論的観測

- Return point: B6の解釈問題


**AB primitive**

- Both


## 6. Edge BC topology [FREEZE]

- Anchor Integrity: strained
    Core定義V・定理IIへの接続は明示されるが、接続の責務はSO側にある。

- Phase Integrity: failed
    量子力学の記述が、SOの可能性・時間・現実生成へ移行する。

- Path Legibility: strained
    B3/B7が橋を示すが、導出・検証・反例条件はない。

- Return Reachability: failed
    量子力学の解釈争いからCを修正する返路がない。

- Open-End Retention: strained
    B6の解釈問題は残るが、Cでは共同創造が中心化される。


**BC anomaly raw record**

- Observed anomaly: 量子力学の観測記述が、SO内部の存在論・時間論の根拠として再配置される。

- Affected nodes: B3/B5/B6/B7、C1-C3

- Expected path: 量子理論、解釈、SO再解釈を分離する。

- Observed path: 量子観測 → Core定義V・定理II → 共同創造

- Possible cut: 量子形式からSO命題への導出

- Possible false connection: 量子理論の権威 → SO形而上学

- Unresolved difference: 再解釈と裏付けの差

- Return point: B6の解釈問題とC1/C2


**BC primitive**

- Both


## 7. A → C bypass check

- A → C bypass suspected: yes

- A node(s): 量子力学の予測精度、測定、重ね合わせ

- C node(s): Core定義V、定理II、共同創造

- Explicit bridge present: partial。B3/B7が橋を明示するが、導出はない。

- What B changed: 技術的観測を、SOの存在論・時間論へ変換した。

- Topology observation: Aの科学的権威が、Bの変換を経由しつつCの裏付けとして見える。

- Primitive if needed: Both


## 8. Return

- source-level return point: 形式理論と解釈問題の区別へ戻る。

- Optional-Axiom-level return point: B1/B2/B6の観測・現実・解釈の範囲へ戻る。

- SO-derived-level return point: C1/C2の再解釈が比喩・モデル・存在主張のどれかを明示する。

- unresolved transformation: 量子測定から観測者による現実生成への変換。


## 9. 日本語 authoritative record

E-9では、外部sourceが明確に区別している数学的形式・測定・解釈・存在論が、Optional Axiom上で観測による現実の収縮と共同創造へ圧縮される。BCでは、量子力学のsource authorityがSO内部の定義・定理を支えるように見えるA→C bypassが疑われる。

## 10. English commensuration

The external sources distinguish mathematical prediction, measurement practice, and unresolved interpretations of quantum mechanics. The Optional Axiom turns observation into a radical epistemology and then connects it to SO’s metaphysics of possibility and time. A partial A→C authority bypass is suspected because scientific authority appears to support the SO-derived interpretation.

---

# Case 4 — ST-2 クラウゼヴィッツの戦争論

## 0. Source Provenance Ledger [FREEZE]

**Source A1**

- Source ID: ST-A1

- Source type: primary-text translation

- Author / institution: Carl von Clausewitz; English translation attributed to J. J. Graham in the accessed edition

- Work: _On War_

- Supports: 戦争の定義、暴力と強制、政治目的、政策と戦争の連続、摩擦、三位一体

- Native terms: war, violence, political object, policy, friction, trinity

- Scope limit: 翻訳の語彙・編集・版の差を含む
    [On War, Project Gutenberg](https://www.gutenberg.org/files/1946/1946-h/1946-h.htm)
    [Book I, Chapter I mirror](https://www.marxists.org/reference/archive/clausewitz/works/on-war/book1/ch01.htm)


**Source A2**

- Source ID: ST-A2

- Source type: specialist secondary reference

- Institution: Stanford Encyclopedia of Philosophy

- Work: “War,” Summer 2004 Edition

- Supports: クラウゼヴィッツの定式が戦争の記述として強力であること、戦争倫理・平和主義・現実主義との関係

- Scope limit: クラウゼヴィッツ全著作の単独解釈ではなく、戦争哲学上の位置づけ
    [War, SEP](https://plato.stanford.edu/archives/sum2004/entries/war/)


## 1. Layer A — domain-authoritative description [FREEZE]

- A1-1: 戦争は、相手に自分の意志を遂行させるための暴力行為として定義される。

- A1-2: 抽象的な戦争では、相互作用が極限化するが、現実の戦争は政治・状況・摩擦によって変形する。

- A1-3: 政治目的は戦争の動機・目標・投入量の基準となる。

- A1-4: 戦争は政治の別手段による継続として記述される。

- A1-5: 戦争には暴力・憎悪、偶然・蓋然性、政治的道具性という三つの傾向が関係する。

- A1-6: 戦争の記述と、戦争の倫理的正当化は別の問題として扱われうる。


**Layer identity record**

- Text/description producer: Clausewitz原典の翻訳主体、SEP執筆主体

- Represented voice/system: クラウゼヴィッツの戦争論および戦争哲学上の位置づけ

- Wording responsibility: 各sourceの執筆・翻訳主体

- Claim responsibility: 原典の記述、SEPの比較・位置づけ

- Warrant mode: 戦略理論、原典記述、哲学的二次解釈

- Scope/closure: 政治目的は戦争に継続的に作用するが、戦争の手段性は倫理的許可を自動的に意味しない

- Unresolved attribution: 版・翻訳による語彙差、記述と規範の境界


## 2. Layer B — Optional Axiom description [FREEZE]

- B1: 戦争は独立目的ではなく、他の手段による政治の継続である。

- B2: 情念・蓋然性・理性の三位一体が戦争を構成する。

- B3: 幾何学的・合理的な戦争観から分岐し、絶対戦争と現実の戦争の緊張を扱う。

- B4: 戦争は摩擦と偶然に満ち、完全には制御できない。

- B5: 政治的意図だけが混沌に意味と方向性を与える。

- B6: 戦争の現実的理解と暴走への戒めを価値とする。

- B7: 戦争を政治手段と定義することが、戦争の正当化に利用されうると記録する。

- B8: ポリティカル・リアリズム、ヘーゲル哲学との類似を示す。


**Layer identity record**

- Text/description producer: Optional Axiom作成主体

- Represented voice/system: クラウゼヴィッツの戦争論として構成された声

- Wording responsibility: Optional Axiom作成主体

- Claim responsibility: B5の「唯一」、B6/B7の価値・危険、B8の比較はrepository側

- Warrant mode: 公理化、戦略理論の要約、政治哲学的比較、リスク記述

- Scope/closure: 政治的意図を上位の方向づけとして置く

- Unresolved attribution: B5/B8がClausewitz自身の命題かSO側の整理か


## 3. Layer C — SO-derived interpretation [FREEZE]

- C1: 戦争と政治の連続性を、システム内の上位目的と実行手段の関係として読む。

- C2: 摩擦・偶然・情念を、予測不能な場の構成要素として配置する。

- C3: `S-12`ポリティカル・リアリズムおよびヘーゲル哲学との接続を、SO側の比較系列として扱う。


C1/C2はB本文の整理とCのSO的読解が混在する。B8は明確な比較接続だが、C1/C2の「システム」語彙への変換主体は明示されない。

## 4. Lineage map [FREEZE]

- A1-1/A1-4 → B1

- A1-5 → B2

- A1-2/A1-3 → B3/B4/B5

- A1-6 → B7

- B1/B4/B5 → C1/C2

- B8 → C3

- Unmapped: 政治目的と手段の相互変形、平和への停止条件、戦争記述と倫理判断の詳細な分岐


## 5. Edge AB topology [FREEZE]

- Anchor Integrity: strained
    戦争・政治・三位一体は接続されるが、B5の「政治的意図だけが方向性を与える」はsourceより強い。

- Phase Integrity: failed
    記述的戦略理論が、政治的方向づけ・戦争利用の原理へ移る。

- Path Legibility: strained
    中心命題は追跡できるが、政治目的と手段の相互変形や平和への返路が削られる。

- Return Reachability: strained
    Aでは政治目的が戦争の投入量や終結に戻るが、Bではその返路が弱い。

- Open-End Retention: strained
    摩擦・偶然は保持されるが、非戦の理想・道徳的評価は捨象される。


**AB anomaly raw records**

A:

- Observed anomaly: 政治目的が、sourceでの相互調整的な基準から、Bでは「混沌に意味と方向性を与える唯一の上位原理」へ強化される。

- Affected nodes: A1-3/A1-4、B1/B5

- Expected path: 政治目的、軍事手段、状況、摩擦の相互関係を保持する。

- Observed path: 政治目的 → 上位の意味・方向 → 戦争の構成

- Possible cut: 政治目的が手段によって変形される返路

- Possible false connection: 政治目的 → 戦争への一方向的な意味付与

- Unresolved difference: 記述的上位関係か、規範的優越か

- Return point: 政治目的と手段の相互作用

- Primitive: Both


B:

- Observed anomaly: 戦争の政治的手段性が、警告を伴いながらも、戦争を選択可能な政治手段として残す。

- Affected nodes: A1-6、B1/B6/B7

- Expected path: 手段性の記述と、倫理的許可を分離する。

- Observed path: 政治目的 → 戦争という手段 → 正当化可能性

- Possible cut: 非戦・倫理・停止条件への返路

- Possible false connection: 政治目的 → 戦争の許可

- Unresolved difference: 記述と正当化の境界

- Return point: B7の「正当化リスク」

- Primitive: Cut


## 6. Edge BC topology [FREEZE]

- Anchor Integrity: unresolved
    B8の比較接続は明示されるが、C1/C2の「システム」解釈を誰が導入したか分離できない。

- Phase Integrity: strained
    戦略理論からポリティカル・リアリズム、ヘーゲル、Topology的読解へ移行する。

- Path Legibility: strained
    B8という対応先はあるが、類似・影響・同一性の基準はない。

- Return Reachability: unresolved
    Cへの異議をBまたはAへ戻す経路が不明。

- Open-End Retention: strained
    B7の正当化リスクは残るが、Cのシステム化によって再配置される。


**BC anomaly raw record**

- Observed anomaly: `S-12`およびヘーゲルとの類似が、SO側のシステム・Topology解釈を支える対応関係として置かれる。

- Affected nodes: B5/B8、C1-C3

- Expected path: 類似、比較、導出、同一性を区別する。

- Observed path: 政治目的・摩擦・三位一体 → システム関係 → 政治リアリズム／ヘーゲル

- Possible cut: 比較接続の判定基準

- Possible false connection: 類似系列 → SO的構造の裏付け

- Unresolved difference: CがBの要約なのか、SO側の新たな解釈なのか

- Return point: B5/B8の責務記録


**BC primitive**

- Unresolved


## 7. A → C bypass check

- A → C bypass suspected: yes

- A node(s): Clausewitz、政治目的、戦争の三位一体

- C node(s): システム的上位目的、ポリティカル・リアリズム、ヘーゲル的接続

- Explicit bridge present: partial。B1/B5/B8に橋はあるが、比較・導出基準はない。

- What B changed: 戦争理論を「政治的意図が場を方向づけるシステム」として配置した。

- Topology observation: 原典の権威と固有名が、Cの構造解釈を直接補強しているように見える。

- Primitive if needed: Both


## 8. Return

- source-level return point: 政治目的と軍事手段の相互変形、平和・終結条件へ戻る。

- Optional-Axiom-level return point: B5の「唯一」、B7の正当化リスクへ戻る。

- SO-derived-level return point: C1-C3の比較・類似・システム化の責務を分ける。

- unresolved transformation: 政治目的の上位性を、Topology的構造へ変換する経路。


## 9. 日本語 authoritative record

ST-2では、原典が扱う政治目的・軍事手段・摩擦・相互作用が、Optional Axiom上で「政治的意図が混沌に意味と方向性を与える」という強い上位関係へ整理される。BCでは、ポリティカル・リアリズムやヘーゲルとの比較が、SO的なシステム解釈へ移る境界を明確にできず、Unresolvedとして保持した。

## 10. English commensuration

The sources describe war as violence linked to political purpose, while preserving friction, reciprocity, changing circumstances, and the distinction between description and ethical justification. The Optional Axiom strengthens political intention into an upper directional principle and then connects the case to political realism, Hegelian dialectics, and a system-oriented reading. The B/C boundary remains unresolved.

---

# Protocol §13 Cross-case audit

以下はCase 4終了後にのみ実行した横断監査です。再採点・再分類は行っていません。

## A. Layer separation

- G-3: A/Bは概ね分離されたが、B2・B6とC2・C3の境界が混在。

- S-8: BとCの混在が最も大きい。システム工学・現代的公平性がBの記述内にすでに埋め込まれている。

- E-9: B3/B7がCへの明示的な橋を形成するが、物理理論とSO形而上学は分離されている。

- ST-2: B8はCへの明示的接続だが、C1/C2のTopology的解釈の責務主体は不明。


Cを新規創作したケースはない。Bまたは該当エントリに明示された内部接続・比較・現代化だけを抽出した。分離できない箇所は`mixed / unresolved boundary`として保持した。

## B. Source-authority transfer

A→C bypassが疑われたケース：

- S-8

- E-9

- ST-2


G-3では、AからCへの直接移送は観測されず、Bに明示された内部接続を経由していた。

source authorityがwarrantの代替になった可能性が特に強い箇所：

- S-8: `fa`・韓非子・秦の歴史 → 現代的システム工学・公平性

- E-9: 量子力学・観測・予測精度 → SOの形而上学的再解釈

- ST-2: Clausewitz・政治目的 → システム的上位目的・比較系列


## C. Language-game transparency

warrant modeが変化した箇所：

- G-3: 哲学的論証・原典読解 → 公理化・bridge・類似系列

- S-8: 文献史・語彙分析 → 現代的制度設計・システム工学

- E-9: 数学・測定・実験 → 認識論・存在論・共同創造

- ST-2: 戦略理論・政治目的 → Topology的上位関係・システム解釈


特にE-9では、外部sourceが形式理論と世界解釈を明確に区別しているのに対し、Bでは両者が連続的に記述される。S-8では、`fa`の語彙的多義性が現代的な「法」へ狭められている。

## D. Transformation locality

逸脱の局在：

- G-3: ABの用語・射程圧縮、BCの類似から対応への移行

- S-8: ABの`fa` flatteningと歴史結果の実効性化、BCのB/C責務混在

- E-9: ABの形式・測定から存在論への移行、BCのSO定理への権威接続

- ST-2: ABの政治目的の上位原理化、BCの比較系列とシステム化の境界不明


外部体系そのものの誤りとして処理せず、どのEdgeの変換で発生したかを記録した。

## E. Residual preservation

保持された残差：

- G-3: 原典帰属、段階的論証、二諦・解釈差

- S-8: `fa`の多義性、法家分類の後世性、一次本文取得不能

- E-9: 形式理論と存在論的解釈の未決着

- ST-2: 翻訳差、政治目的と規範的許可の境界、B/C責務


名前を付けずに保持した異常：

> 外部sourceの記述が、BまたはCで、別の言語ゲームのwarrantへ移動しているが、その移動を担う主体と中間規則が明示されない。

## F. Primitive件数

主たるanomaly raw recordのみを集計し、bypass記録を重複計上しない。

|Primitive|件数|
|---|--:|
|Cut|1|
|False Link|1|
|Both|8|
|Unresolved|1|

- G-3: Both 3

- S-8: Both 2、False Link 1

- E-9: Both 2

- ST-2: Both 1、Cut 1、Unresolved 1


## G. Post-run correction

Post-run correctionはありません。OriginalのLayer A/B/C、Lineage、AB/BC、bypass、生ログは上書きしていません。
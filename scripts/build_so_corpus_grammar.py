#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corpus-wide Japanese grammar surface atlas, with reproducible source-linked evidence.

This is an evidence extractor, NOT a Japanese morphological parser or a semantic validator.
Every non-excluded repository Markdown document in the pinned inventory is visited.
All matched evidence is retained. Scope and unmatchable material are explicitly counted.
"""
import argparse
import collections
import hashlib
import json
import os
import re
try:
    import resource
except ImportError:
    resource = None
import sys
import time
import zipfile
from pathlib import Path

PREFIX='Scientific-Ontology/'
DICTIONARY_PREFIX='tools/assessment/term_dictionary/corpus_wide_draft/'
SOURCE_INV=DICTIONARY_PREFIX+'provenance/source_inventory.json'
CANDIDATE_FILE=DICTIONARY_PREFIX+'all_japanese_surface_candidates.jsonl'
DICT_FILE=DICTIONARY_PREFIX+'dictionary_reviewed.jsonl'
JP_CHARS=re.compile(r'[\u3041-\u30ff\u3400-\u9fff]')
URL=re.compile(r'(?:https?://|www\.)\S+')
INLINE_CODE=re.compile(r'`[^`]*`')
MDLINK=re.compile(r'\[([^\]]+)\]\([^)]+\)')
TAGS=re.compile(r'<[^>]*>')
TEX_COMMAND=re.compile(r'\\(?:[A-Za-z]+)')

# category, term/pattern, working interpretation, caution, matching mode
# Single-character grammatical particles are deliberately recorded as raw surface
# candidates only. A substring match is NOT a word segmentation decision.
DATA=[
 ('助詞・係り','は','主題提示・対比の候補','固有語やひらがなの一部との区別は未解析','weak'),
 ('助詞・係り','が','主格・焦点・逆接の候補','「ながら」等の部分文字列にも一致する','weak'),
 ('助詞・係り','を','対象・経路を示す格助詞候補','機械的には直前の体言を同定していない','weak'),
 ('助詞・係り','に','到達・場所・時点・対象など','語中の「に」も拾うため単独で品詞を確定できない','weak'),
 ('助詞・係り','で','手段・場所・原因または断定の連用形','語中一致と用法の多義性を含む','weak'),
 ('助詞・係り','と','引用・共同・並列・条件など','引用と接続を形態で区別できない','weak'),
 ('助詞・係り','の','連体・体言化・終助詞など','名詞化と所有関係を形態で区別できない','weak'),
 ('助詞・係り','も','添加・対比・譲歩など','文字列の一部も拾う','weak'),
 ('助詞・係り','へ','方向・到達先','単独ひらがなの一致は未確定','weak'),
 ('助詞・係り','や','並列・列挙','間投や引用内の部分一致にも注意','weak'),
 ('助詞・係り','か','疑問・選択・不定の候補','語中の「か」と区別していない','weak'),
 ('助詞・係り','から','起点・理由','理由と起点は文脈で異なる','surface'),
 ('助詞・係り','まで','限界・範囲','時間・場所・程度を分けていない','surface'),
 ('助詞・係り','より','比較・起点','活用語尾等との混同を確認する','surface'),
 ('助詞・係り','だけ','限定','必要条件と十分条件を保証しない','surface'),
 ('助詞・係り','しか','限定と否定の共起','否定との係り受けを照合していない','surface'),
 ('助詞・係り','こそ','強調・取り立て','強調対象は未解析','surface'),
 ('助詞・係り','さえ','極端例・最小条件の取り立て','量化の範囲は未解析','surface'),
 ('助詞・係り','ほど','比較・程度','文脈で閾値・強さが変わる','surface'),
 ('助詞・係り','ばかり','概数・限定・反復','文脈による読み分けが必要','surface'),
 ('助詞・係り','くらい','程度・限定','用例により「ぐらい」と交替','surface'),
 ('助詞・係り','ぐらい','程度・限定','「くらい」との語形差を保持','surface'),
 ('接続・談話','しかし','逆接・転換','反論の正当性を保証しない','surface'),
 ('接続・談話','ただし','条件付き限定・留保','何を限定するかは構造上別に特定する','surface'),
 ('接続・談話','したがって','帰結提示','形式的導出の成立を保証しない','surface'),
 ('接続・談話','ゆえに','理由から結論への導線','推論規則が成立した証明ではない','surface'),
 ('接続・談話','そこで','問題から対応へ移る','原因と対策の支持関係は未検証','surface'),
 ('接続・談話','一方で','対照・併存','二項の論理的排他性を含意しない','surface'),
 ('接続・談話','これに対して','対照する対象を提示','指示語「これ」の先行詞は未解析','surface'),
 ('接続・談話','これにより','前述作用の結果・手段','因果の証拠とは限らない','surface'),
 ('接続・談話','つまり','説明の要約・言い換え','厳密な同値を保証しない','surface'),
 ('接続・談話','すなわち','同格・言い換え','対象範囲と同値性は未検証','surface'),
 ('接続・談話','要するに','要約・圧縮','省略された限定に注意する','surface'),
 ('接続・談話','例えば','例示の導入','例から一般命題への導出を保証しない','surface'),
 ('接続・談話','たとえば','例示の導入（平仮名）','表記違いを示すが意味検査は別','surface'),
 ('接続・談話','なお','補記・注意','補記の作用範囲は未解析','surface'),
 ('接続・談話','むしろ','対比上の重心変更','元の比較軸を確認する','surface'),
 ('接続・談話','それでも','譲歩・逆接','前提撤回とは限らない','surface'),
 ('接続・談話','さらに','追加・拡張','追加が支持を増やすとは限らない','surface'),
 ('接続・談話','加えて','追加・併置','新条件が必要かは文脈で決まる','surface'),
 ('接続・談話','また','添加・並列','「または」と重なる部分を除いた出現のみ','surface'),
 ('接続・談話','および','連言・併記','形式論理のANDと同一視しない','surface'),
 ('接続・談話','または','選言・候補の提示','排他的選言かは文脈で決まる','surface'),
 ('接続・談話','あるいは','代替・言い換え','排他的選択と単なる別表現を区別する','surface'),
 ('接続・談話','かつ','連言・付加','量化範囲は未解析','surface'),
 ('接続・談話','反対に','対照・方向転換','論理的否定を意味するとは限らない','surface'),
 ('条件・仮定','であれば','条件節・仮定','現実条件と論理条件は別','surface'),
 ('条件・仮定','ならば','条件節・含意の表面形式','形式的な含意成立を保証しない','surface'),
 ('条件・仮定','だとすれば','仮定を受けた推論','仮定の受理と事実性を区別する','surface'),
 ('条件・仮定','とすれば','仮定・前提設定','前提の事実確認を含意しない','surface'),
 ('条件・仮定','としたら','仮定・仮想条件','反事実性は文脈で異なる','surface'),
 ('条件・仮定','とすると','仮定を置いた推移','論理的演繹を保証しない','surface'),
 ('条件・仮定','場合には','適用条件の明示','必要条件・十分条件を区別していない','surface'),
 ('条件・仮定','場合','事例・条件の範囲','常に条件構文とは限らない','surface'),
 ('条件・仮定','とき','時間・場合の条件','時点と条件とを混同しない','surface'),
 ('条件・仮定','際','特定場面・時点','場合との差は文脈を要する','surface'),
 ('条件・仮定','限り','必要条件・範囲の限定','「限りでは」と「限り」の差に注意','surface'),
 ('条件・仮定','ない限り','否定的な必要条件','スコープと対象を復元する必要','surface'),
 ('条件・仮定','たとえ','譲歩条件の導入','結末の条件節を検査する必要','surface'),
 ('条件・仮定','ても','譲歩・条件の表現','活用語尾の一部との混同可能性','surface'),
 ('条件・仮定','に応じて','条件依存の調整','因果か対応かは別に確認','surface'),
 ('条件・仮定','条件下で','条件と作用の場を限定','文脈で条件の識別が必要','surface'),
 ('条件・仮定','のもとで','前提・環境の指定','規範上の正当化とは独立','surface'),
 ('条件・仮定','を前提として','前提の宣言','前提が実証されたことを意味しない','surface'),
 ('否定・様相','ではない','述語否定・同定拒否','否定対象のスコープを機械的に確定しない','surface'),
 ('否定・様相','とは限らない','一般化の否定','反対命題の肯定とは異なる','surface'),
 ('否定・様相','というわけではない','解釈・含意の否定','先行発話への係り方は未検証','surface'),
 ('否定・様相','必ずしも','全称性の留保','通常は否定と共起するが自動判定しない','surface'),
 ('否定・様相','できない','不可能性・不許可・能力不足','導出不可能と探索未発見を区別する必要','surface'),
 ('否定・様相','ではなく','前項否定と後項提示','後続項が常に唯一の代替とは限らない','surface'),
 ('否定・様相','にすぎない','範囲の縮減・限定','語用論的評価を含み得る','surface'),
 ('否定・様相','に過ぎない','範囲の縮減・限定（漢字表記）','原文表記を保持','surface'),
 ('否定・様相','にとどまる','効果・範囲の限定','独立した検証が必要','surface'),
 ('否定・様相','べき','義務・推奨','規範的判断を事実命題と区別する','surface'),
 ('否定・様相','必要がある','必要性の提示','必要の主語・機能・根拠が必要','surface'),
 ('否定・様相','必要はない','必要性の否定','不要と不可能は異なる','surface'),
 ('否定・様相','可能性がある','可能性の提示','可能性と成立証明を混同しない','surface'),
 ('否定・様相','かもしれない','推量・可能性','強い根拠の表示とは限らない','surface'),
 ('否定・様相','あり得る','可能性・成立余地','構成可能性と現実実証は異なる','surface'),
 ('否定・様相','し得る','可能性・可能操作','技術的可否は別検証','surface'),
 ('否定・様相','してよい','許可・任意','権限主体が省略される場合がある','surface'),
 ('否定・様相','してはならない','禁止・制約','適用範囲と権限根拠を別照合','surface'),
 ('否定・様相','しなければならない','義務・必要条件','法的義務と設計条件を区別','surface'),
 ('否定・様相','とみなさない','分類・同定の拒否','否定と代替分類を区別','surface'),
 ('定義・引用','とは','主題・定義の導入','「とは」だけでは定義文と断定できない','surface'),
 ('定義・引用','と呼ぶ','命名・局所ラベルの宣言','一般正本定義とは限らない','surface'),
 ('定義・引用','と定義する','定義の明示','定義の所有範囲は別検証','surface'),
 ('定義・引用','として扱う','操作的な位置づけ','同一性や本質の主張とは限らない','surface'),
 ('定義・引用','とみなす','推定・分類規則の宣言','事実認定と擬制を区別','surface'),
 ('定義・引用','と読める','読み・解釈候補','外部理論の確認済み事実ではない','surface'),
 ('定義・引用','と考えられる','推論・考察の提示','著者断言や実証を示さない','surface'),
 ('定義・引用','と述べる','記述の帰属','実際の引用元を別に確認','surface'),
 ('定義・引用','と記す','文面記録の帰属','書かれたことと成立したことを区別','surface'),
 ('定義・引用','とされる','受動的帰属・通説化','誰によってかの確認を要する','surface'),
 ('定義・引用','という','命名・引用・説明の媒介','多義的なため意味型を自動確定しない','surface'),
 ('定義・引用','といえる','結論・言い換えの表示','推論経路の検証とは別','surface'),
 ('定義・引用','を指す','指示対象の限定','概念定義との対応は別検証','surface'),
 ('定義・引用','を意味する','語義・帰結の説明','同語反復か実質的主張か要確認','surface'),
 ('定義・引用','を示す','証拠・図示・表現の帰属','証明や実証の強さは別','surface'),
 ('定義・引用','を表す','記号・模型の対応','写像の正しさを別検証','surface'),
 ('定義・引用','という意味で','読みの適用条件','限定外への転用を防ぐ','surface'),
 ('定義・引用','である','叙述・定義の断定','定義なのか事実主張かは文脈依存','surface'),
 ('定義・引用','とする','採用・宣言・定義の候補','分析前提と事実を区別','surface'),
 ('範囲・量化','において','場・条件・領域の指定','何の対象範囲かを照合','surface'),
 ('範囲・量化','について','主題・対象の指定','関係の型まで決めない','surface'),
 ('範囲・量化','に関して','論点・関係先の指定','法的責任や支持関係を含意しない','surface'),
 ('範囲・量化','に対して','対象と作用方向','反対・比較・作用を分ける','surface'),
 ('範囲・量化','として','役割・立場・資格の指定','同一性を無条件に保証しない','surface'),
 ('範囲・量化','に限って','適用範囲の限定','必要条件・十分条件を分ける','surface'),
 ('範囲・量化','に限り','範囲・条件の限定','何が限定されるか未解析','surface'),
 ('範囲・量化','のみ','限定・排他','否定の範囲は別検証','surface'),
 ('範囲・量化','すべて','全称表現','領域母集団の指定が不可欠','surface'),
 ('範囲・量化','一部','部分集合・部分性','どの全体か未解析','surface'),
 ('範囲・量化','少なくとも','下限・必要十分の留保','数値の測定ではない','surface'),
 ('範囲・量化','それぞれ','分配・個別対応','1対1対応を保証しない','surface'),
 ('範囲・量化','ごとに','個別単位の指定','単位同定は未解析','surface'),
 ('範囲・量化','に照らして','基準・根拠の指定','その基準の採用権限は別','surface'),
 ('範囲・量化','によらず','独立・排除条件','否定対象を確認する','surface'),
 ('範囲・量化','の範囲','局所領域の限定','範囲境界の特定は必要','surface'),
 ('関係・因果','によって','手段・原因・受身動作主','因果関係の成立は別検証','surface'),
 ('関係・因果','により','原因・方法・基準','文脈により機能が異なる','surface'),
 ('関係・因果','を通じて','経路・媒介','接触したことと保存されたことは違う','surface'),
 ('関係・因果','に伴って','同時変動・付随','因果と共起を区別','surface'),
 ('関係・因果','につれて','変化への随伴','必然の数理関係とは限らない','surface'),
 ('関係・因果','その結果','帰結・結果提示','因果を確認する別資料が必要','surface'),
 ('関係・因果','結果として','結果・事後的配置','予測可能性とは別','surface'),
 ('関係・因果','ことによって','行為・作用を原因や手段へ接続','実際の作動の検証は別','surface'),
 ('関係・因果','とともに','付随・共変化','同一性や因果ではない','surface'),
 ('関係・因果','に向けて','目的・方向','結果の達成は保証しない','surface'),
 ('関係・因果','ために','目的・原因','「目的」と「原因」は異なる','surface'),
 ('関係・因果','ので','理由・説明','正当化や因果証明とは別','surface'),
 ('関係・因果','なぜなら','理由提示','前後の推論は未検証','surface'),
 ('関係・因果','による','修飾された原因・手段','対象の対応を別確認','surface'),
 ('比較・非含意','とは異なる','非同一性・比較','どの性質が異なるかを要確認','surface'),
 ('比較・非含意','同じではない','同一性否定','どの同一性を否定したか要確認','surface'),
 ('比較・非含意','同一ではない','概念・対象の非同一性','関連性の否定とは限らない','surface'),
 ('比較・非含意','別問題である','判断対象の分離','両者の無関係を意味しない','surface'),
 ('比較・非含意','別である','相違・独立の宣言','関係の切断とは限らない','surface'),
 ('比較・非含意','直ちに','推論・評価の即時性','否定語と共起するか別に調べる','surface'),
 ('比較・非含意','自動的に','規則的・無条件の移行','否定・留保との共起に注意','surface'),
 ('比較・非含意','というだけで','根拠不足・限定','後続否定の位置を確認する','surface'),
 ('比較・非含意','だけでは','十分条件の否定候補','必ずしも全称否定ではない','surface'),
 ('比較・非含意','といって','推論・評価の文脈提示','後続の肯否が重要','surface'),
 ('比較・非含意','であっても','譲歩・反例','結論の成立は別途照合','surface'),
 ('比較・非含意','にもかかわらず','期待と結果の不一致','論理矛盾の証拠とは限らない','surface'),
 ('比較・非含意','に比べて','比較対象・基準','比較尺度の同質性を要確認','surface'),
 ('比較・非含意','とは限らず','一般化の否定と継続','正反対を導くわけではない','surface'),
 ('比較・非含意','必ずしも.*?ではない','全称の限定否定を含む表面パターン','同じ文内の共起であり係り受けの保証はない','regex'),
 ('比較・非含意','だけ.*?とは限らない','十分条件否定らしい表面パターン','同じ文内の共起であり係り受けの保証はない','regex'),
 ('時間・相','している','進行・結果状態','時制・主語は未解析','surface'),
 ('時間・相','していた','過去の進行・結果状態','文体や対象時間で異なる','surface'),
 ('時間・相','てきた','過去から現在への連続','すべてが同一の対象持続とは限らない','surface'),
 ('時間・相','ていく','後続への進展','規範的方向づけも含み得る','surface'),
 ('時間・相','し続ける','反復・持続','終了条件は未解析','surface'),
 ('時間・相','することがある','場合による生起','全称命題ではない','surface'),
 ('時間・相','以前','過去の参照点','実時刻と論理順序を区別','surface'),
 ('時間・相','以後','基準点より後','更新順序と時計時刻は別','surface'),
 ('時間・相','後から','事後の判断・形成','後付けの正当化と区別を要する','surface'),
 ('時間・相','現在','現時点への限定','成立範囲の条件も必要','surface'),
 ('時間・相','将来','未来への参照','予測と願望を分ける','surface'),
 ('時間・相','まだ','未成立・未到達','永続的不可能と混同しない','surface'),
 ('時間・相','すでに','成立済み・先行','現在の権限確認は別','surface'),
 ('論証・引用形式','⇒','記号的帰結・指示','自然言語の含意・導出と同一視しない','symbol'),
 ('論証・引用形式','→','推移・関係・遷移記号','関係の型の検証を要する','symbol'),
 ('論証・引用形式','≠','非同一性の記号','対象・単位の一致を要する','symbol'),
 ('論証・引用形式','∧','連言・合成記号','文脈の論理体系を特定する','symbol'),
 ('論証・引用形式','∨','選言記号','排他的選言の可否を区別','symbol'),
 ('論証・引用形式','¬','否定記号','対象体系の否定規則を要確認','symbol'),
 ('論証・引用形式','⊢','導出関係の記号','証明体系を別に明示する必要','symbol'),
 ('論証・引用形式','⊬','導出非成立を表す記号','探索未発見と証明された非導出を区別','symbol'),
]

SYNTHESIS = '## 第一部\u3000文法として何を読み取るか\n\n### 1．文法の単位は、文字列でも命題でもない\n\n本文に「は」「が」「を」が現れることと、その文字が助詞として機能していることは同じではない。例えば「は」は、ある主題を提示したり、対比を導入したりする。しかし「は」という一字が見つかっただけでは、主題がどこからどこまでか、何と比較されているかは分からない。語彙を分割する前に文字を助詞として数えてしまえば、見かけ上の精度が上がっても構文の再構成にはならない。\n\n逆に、一つの文が複数の異なる判断を含むことがある。条件を述べ、想定する反例を加え、最後に適用範囲を限定する一文では、条件、反例、限定を別々に取り出す必要がある。表面一致の単位と、文法的作用の単位と、監査に使える命題の単位は、それぞれ別に成立する。本稿の照合記録は最初の単位を提供するが、後二者を完成したとはしない。\n\n### 2．「は」と「が」――主題と判断の中心\n\n「XはYである」には、Xを主題とした判断を読む余地がある。しかしXが文脈上の既知主題であるか、Xと他候補の対比であるかは、文の外へ遡らなければ決まらない。「XがYである」も、ある性質の主体、識別の焦点、逆接の節など複数の用法を持つ。したがって、一字助詞を辞書の独立定義として大量に追加する代わりに、文法の項で構造と用例を扱う。\n\n本試行では「は」「が」をそれぞれ表面文字列として全件抽出したが、形態素・格関係の確定をしていない。後に辞書の登録対象から切り分けるときも、同じ文字列が専門語や見出し名に含まれている場合を、文法の判定済みとして自動除外してはならない。\n\n### 3．条件を述べることと、条件から導くこと\n\n「であれば」「ならば」「場合には」「とすれば」は、条件を提示する。条件節の存在は、前提が現実に成立することを意味せず、また後件が形式的に証明されたことを意味しない。\n\n原文には次の一文がある。『この変換が曖昧であれば、目的は現場へ届かない。』（`05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Organizational_Boundary_and_Port_Model.ja.md:73`）。ここで文法上確認できるのは、変換の曖昧さを条件節に置いて後件を述べていることである。変換の曖昧さをどの指標で測るか、後件がどの条件下で必然となるかは、文法より先の論証と検証の仕事になる。\n\nまた『ただし、非線形であれば必ずカオスになるわけではない。』（`05_Research_Notes/Physical_Cosmological_Notes/Chaos_Theory_and_Logical_Depth_Axis.ja.md:46`）では、条件形と全称的な帰結の否定が重なる。「非線形である」と「必ずカオスである」を単純な含意として受理しないことが要点であり、文法層では否定が及ぶ範囲を後段へ引き渡す。\n\n### 4．否定は一種類ではない\n\n「ではない」は述語を否定する。「とは限らない」は一般化を拒む。「できない」は能力・条件・禁止・不可能性を含み得る。「まだない」は現在の不在を示し得るが、将来の成立不能を示さない。「というわけではない」は先行する解釈や含意を退ける場合がある。\n\nたとえば『人に症状が出たからといって、その人だけに原因があるとは限らない。』（`05_Research_Notes/Metaphysical_Approach/Engineering Research on Correctness/存在境界論における監査理論.ja.md:2832`）では、症状が出た事実自体を否定していない。否定されるのは、原因をその人だけへ帰属させる一般化である。これを単純な「偽」というラベルに縮約すると、否定していない部分まで失う。\n\nよって文法層では、否定語の位置、範囲、程度、先行する主張との接続を候補として記録する。その結果から論理式を構成する工程では、同じ否定語から直ちに同じ演算子を割り当てない。\n\n### 5．「というだけでは」と十分条件の不成立\n\n『講和したというだけでは、平和にならない。』（`07_Creative_Offshoots/Literary_Essays/Questions_Boundaries_and_Peace.ja.md:1012`）という文は、「講和した」ことを取り消していない。「講和した」という一条件だけでは、「平和になった」という後件に届かないことを主張している。\n\n「だけでは」「というだけで」「とは限らない」は、前件の事実性を保持したまま、その十分性を否定できる。これは論理学的な非含意を記す言い方に近いが、個別の文がどの程度形式的な非含意を主張しているかは別に調べる。文法書は、否定対象のずれを見失わないための入口である。\n\n### 6．定義、命名、解釈を混同しない\n\n「XとはYである」「XをYと呼ぶ」「Xとして扱う」「Xとみなす」「Xと読める」は、似た形を持つが働きが違う。定義の宣言、局所的命名、操作上の取扱い、擬制、解釈可能性は、同じ身分を持たない。特に「と読める」は、対象の唯一の本質や外部分野の公式定義を宣言するとは限らない。\n\nこの文法上の相違を、辞書の定義所有へそのまま写してはならない。定義文の表面型を見つけることは、辞書の採録候補を見つける方法にはなるが、採録許可でも正本昇格でもない。\n\n原文には『保留したことを無責任とみなさない。』（`05_Research_Notes/Cognitive_Dynamics_Communication_Studies/Cognitive_Dynamics_Communication_Model.ja.md:627`）という文がある。ここで退けているのは、ある行為と評価語を結び付ける分類である。行為の存在や責任の所在をすべて否定したと読んではならない。\n\n### 7．接続表現は論理的な支持線ではない\n\n「しかし」「一方で」「それでも」は対比・逆接の導線を作る。「したがって」「ゆえに」は結論を導く説明に用いられる。「つまり」「すなわち」は要約や言い換えを表す。「例えば」は事例へ進む。「または」「および」は選言・並列に接続する。しかしこれらの語があるだけでは、前後の命題の正しい論理関係は決まらない。\n\n特に「したがって」を機械的に `support` 関係へ変換してしまえば、無効な論証や比喩も監査用の支持線に変わってしまう。一方で、論理接続が明記されていなくても、原文には実際の支持関係が存在し得る。「接続語があること」と「導出可能であること」の両方向に、早すぎる断定を避ける必要がある。\n\n### 8．範囲・量化・主張強度を読む\n\n「すべて」「一部」「少なくとも」「のみ」「それぞれ」は、対象集合と量化を調整する。「において」「のもとで」「に限って」「条件下で」は、どこまでを主張しているかを限定する。これらを失うと、一つの局所結論が対象一般の主張に変わる。\n\n『AI安全において、拒否は必要である。』（`03_Tam_Goodness/Boundary_Ethics_Model.md:120`）は、AI安全という問題範囲で必要性を述べる。文法上の「において」が消えると、「拒否はあらゆる場面で必要」という別の主張へ膨らみかねない。専門分野・適用範囲・判断主体は、辞書だけでなく文法の側でも保持しなければならない。\n\n### 9．原因、手段、媒体、目的は別の関係\n\n「によって」「により」「を通じて」は、原因、手段、媒介、受動の動作主などを担う。「ために」は目的にも原因にもなる。「に伴って」「につれて」は共変化を示し得るが、必ずしも原因と結果を証明しない。\n\nある文で「AによってBとなる」と書かれていても、AがBの唯一の原因か、Aが必要な媒介か、AとBに共通の条件があるかは、文法だけでは決められない。逆に、その区別を保持しないまま「関係あり」として一つの線に変換すると、後の分析がどの関係を検証しているか分からなくなる。\n\n### 10．叙述の時間と生成上の順序\n\n「していた」「てきた」「ていく」「以前」「以後」「後から」「現在」は、経験や記録を時間的に配置する手掛かりである。しかし、SOの研究原稿では「生成上先にある」という依存の順序と、時計による時間、文書の成立順序を区別する必要がある。文法上の時制・相の形式だけでは、どの時間軸についての主張かを固定できない。\n\n特に、後から説明できるようになったことを、最初からその理解が存在していたという史実へ読み替えることはできない。時間表現は、履歴の同一性・作用・再記述の境界を指定したうえで解釈する。\n\n### 11．接続の機能を残し、文章を定義書へ変換しない\n\n文学的な反復、比喩、問い、強調、間、引用の重層性は、文法・談話の機能を持つ。繰り返し現れた語を「同じ辞書見出しだから不要」と削れば、文章が何をどう読ませるかという働きを損なう。\n\n逆に文法書は、本文からそれらの表現を消し去るためのものではない。読者がある表現に出会った際、それが何を制約し、何を開き、どこから先が別の意味判断なのかを確認するための補助である。\n\n### 12．文法書が後の分析機構へ渡せるもの\n\n今回の表面照合から、次に機構研究で扱える候補は、①候補句の抽出、②条件や否定の出現検出、③定義・引用・解釈の文面型検出、④出典への追跡、⑤文書や表記間の比較可能性である。ここには決定的な規則として再実行できるものがある。\n\n一方、助詞の係り受け、語義と品詞の多義解消、否定の正確な作用域、比喩と命題の区別、前提の妥当性、文書間の同一主張判定は、この表面照合だけでは確立しない。これらは原文文脈を伴うLLMの総合的な読解を要する候補であり、その判断が正しいかどうかは独立に試す必要がある。\n\n今回確立したのは「文法を完全に分析する機械」ではなく、**一度Repository全域に対して具体的な文法の読解枠を適用し、その出力・入力・弱点・計算費用を再検査できる基礎資料**である。結果が十分かどうかはHumanの内容判断を残す。仕分け規則の改善は次の実験にできるが、初稿全域の処理をそこで保留する必要はない。\n'

GROUP_DESC={
 '助詞・係り':'基本助詞の候補表記を観測する。ただし、日本語の形態素解析器を使用しないため、特に1文字助詞の件数は文法使用回数ではない。',
 '接続・談話':'談話接続、説明の段落運動、理由提示、対照、例示の表面形式。接続語から論理的支持を導くことはしない。',
 '条件・仮定':'条件、仮定、適用範囲の導入。必要条件か十分条件かは原文の命題関係として別判定する。',
 '否定・様相':'否定、可能性、規範、制約、義務の語法。不存在・未判定・不可能性の区別は用語・命題層でも検査する。',
 '定義・引用':'定義候補、命名、解釈、引用、帰属の表現。これらの出現をもって正本定義の存在や導出の成立を宣言しない。',
 '範囲・量化':'対象範囲、集合、量化、各主体の配置。数えられている母集団や条件が未確定なら未判定とする。',
 '関係・因果':'原因、手段、目的、媒介の表面形式。自然言語の連結と検証された因果関係は区別する。',
 '比較・非含意':'同一性否定、比較、結論への不当な飛躍を抑える表現。反論・限定・非含意の区別は原文の係り受け次第。',
 '時間・相':'時制・相と、時間・順序を示す表現。歴史的時間と論理的な形成順を混同しない。',
 '論証・引用形式':'表記としての記号。原文での数式・コードブロックは本走査では除外するので件数は不完全。',
}

def sha(data): return hashlib.sha256(data).hexdigest()
def load_jsonl(raw):
    return [json.loads(s) for s in raw.decode('utf-8-sig').splitlines() if s.strip()]
def textfile(p,obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(obj,(list,dict)):
        data=json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    else:data=obj
    # Repository handoff text contract: UTF-8, LF, and a final LF for text files.
    # Keep this normalization at the output boundary, including generated HTML.
    if data and not data.endswith('\n'):
        data += '\n'
    p.write_bytes(data.encode('utf-8'))

def mask_line(raw):
    # Preserve most narrative prose, including blockquotes and markdown tables.
    # This cleaning deliberately avoids sentence segmentation and dependency parsing.
    s=raw.rstrip('\r\n')
    s=INLINE_CODE.sub(' ',s)
    s=MDLINK.sub(lambda m:m.group(1),s)
    s=URL.sub(' ',s)
    s=TAGS.sub(' ',s)
    s=TEX_COMMAND.sub(' ',s)
    return s

def compile_patterns():
    patterns=[]; ids=collections.Counter()
    for group,literal,explain,caution,mode in DATA:
        ids[group]+=1
        rid='G'+str(list(GROUP_DESC).index(group)+1).zfill(2)+'-'+str(ids[group]).zfill(3)
        if mode=='regex':
            raw=literal.replace('.*?','[^。！？\n]{0,65}?')
        else:raw=re.escape(literal)
        pat=re.compile(raw)
        patterns.append({'id':rid,'group':group,'label':literal,'explanation':explain,'risk':caution,'mode':mode,'pattern':raw,'re':pat})
    return patterns

def render_viewer(index, counts):
    """Self-contained offline HTML reader, no external scripts or API requests."""
    raw=json.dumps({'index':index,'coverage':counts},ensure_ascii=False,sort_keys=True)
    # Safe JSON string in script element even if source excerpt contains tags.
    raw=raw.replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    html=r'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>SO Repository 日本語文法書｜全域照合稿</title>
<style>
:root{color-scheme:light;--ink:#27313c;--navy:#213b51;--paper:#f6f6f2;--accent:#0d786b;--line:#d5dddf;--muted:#67737b}
*{box-sizing:border-box}body{margin:0;background:var(--paper);font-family:system-ui,'Yu Gothic','Hiragino Kaku Gothic ProN',sans-serif;color:var(--ink)}
header{background:#203c50;color:#fff;padding:35px max(22px,calc((100vw - 1120px)/2)) 27px}
h1{font-size:clamp(22px,3vw,33px);letter-spacing:.04em;margin:0 0 8px}header p{max-width:900px;line-height:1.7;color:#dde8e8;font-size:14px}
main{max-width:1160px;margin:24px auto;padding:0 22px 80px}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(185px,1fr));gap:12px;margin-bottom:20px}
.stat{background:#fff;border:1px solid var(--line);border-radius:10px;padding:16px;min-height:108px}.stat strong{font-variant-numeric:tabular-nums;display:block;font-size:27px;color:var(--navy);margin:6px 0}.stat small{color:var(--muted)}
.toolbar{display:flex;flex-wrap:wrap;gap:12px;background:white;border:1px solid var(--line);border-radius:10px;padding:16px;margin:18px 0;align-items:center;position:sticky;top:0;z-index:2;box-shadow:0 8px 20px #1c33420d}
input,select{background:#fff;color:var(--ink);border:1px solid #adbcc4;padding:11px 13px;border-radius:7px;min-width:150px;font-size:14px}input{flex:2;min-width:220px}select{flex:1}#count{font-size:13px;color:var(--muted)}
section.note{background:#e8f1ee;border-left:5px solid var(--accent);padding:17px 19px;margin:18px 0;line-height:1.8;font-size:14px}
article{background:white;border:1px solid var(--line);border-radius:10px;margin:12px 0;padding:20px 23px}article h2{font-size:20px;margin:0 0 12px}article h2 span{font-size:13px;color:var(--muted);margin-right:8px}
.badge{display:inline-block;font-size:12px;padding:4px 8px;background:#edf5f1;color:#246055;border-radius:4px;margin-right:5px}.weak{background:#fff0e4;color:#984d13}
.meta{font-size:13px;color:var(--muted);margin:10px 0}.explain{line-height:1.75}.risk{color:#684621;line-height:1.7}.examples{border-top:1px solid var(--line);padding-top:12px;margin-top:12px}
.example{border-left:2px solid #dce5e4;padding:8px 10px 8px 13px;margin:7px 0;font-size:13px;line-height:1.6;word-break:break-all}
.example a{color:#0c645e;text-decoration:none}.example a:hover{text-decoration:underline}.example p{margin:5px 0 0}
footer{margin-top:40px;font-size:13px;color:var(--muted);line-height:1.8}
@media(max-width:700px){header{padding:24px 22px}main{padding:0 12px 50px}.toolbar{position:static}article{padding:15px}}
</style></head><body><header><h1>日本語文法書｜SO Repository全域照合稿</h1>
<p>単語の定義ではなく、助詞・接続・条件・否定・引用・範囲・因果などの表現の働きを調べます。全域走査の結果を読める形にした研究用第一稿です。正本ではありません。</p></header>
<main><div class="cards" id="stats"></div>
<section class="note"><b>読み方：</b>全原文を走査しましたが、各出現の構文・語義をLLMが全件検証したわけではありません。特に一文字助詞（薄橙）は単なる部分文字列の出現数です。表面一致から論理的導出、事実、定義権限を判定しないでください。原文と位置はZIP内の <code>grammar_surface_concordance.jsonl</code> に全件収録しています。</section>
<div class="toolbar"><input id="query" placeholder="表記・働き・注意点で検索（例：否定、条件、とは）" aria-label="検索"><select id="group" aria-label="章で絞る"><option value="">全章</option></select><select id="quality" aria-label="出現種別で絞る"><option value="">全文字形式</option><option value="weak">要注意：一文字候補</option><option value="surface">複合表現・文字列</option><option value="regex">複合条件パターン</option><option value="symbol">記号表記</option></select><span id="count"></span></div>
<div id="results"></div><footer>元資料の日本語正本86、ほか150文書を含む236文書を走査。未一致行、出典台帳、27,901候補との交差台帳、実行資源記録は同梱ファイルを参照してください。Windows/Macでオフライン表示可能。外部CDN・APIを使用していません。</footer></main>
<script>const DATA=__DATA__;
const n=v=>Number(v).toLocaleString('ja-JP');
function node(tag,cls,text){const e=document.createElement(tag);if(cls)e.className=cls;if(text!==undefined)e.textContent=text;return e;}
const stats=document.getElementById('stats');
for(const [k,v] of [['走査文書',DATA.coverage.scanned_documents],['文法事項',DATA.coverage.grammar_patterns],['表面一致（延べ）',DATA.coverage.all_surface_hits_including_overlaps],['一文字の曖昧一致',DATA.coverage.weak_single_character_substring_hits],['相対的に強い表現一致',DATA.coverage.nonweak_surface_hits],['未一致の日本語行',DATA.coverage.unmatched_japanese_lines]]){
 const e=node('div','stat');e.append(node('small','',k));e.append(node('strong','',n(v)));stats.append(e);}
const groups=[...new Set(DATA.index.map(x=>x.group))];for(const g of groups){const o=node('option','',g);o.value=g;document.getElementById('group').append(o);}
const root=document.getElementById('results'),q=document.getElementById('query'),gr=document.getElementById('group'),quality=document.getElementById('quality');
function render(){const query=q.value.trim().toLowerCase(),g=gr.value,z=quality.value;root.replaceChildren();
 const subset=DATA.index.filter(x=>(!g||x.group===g)&&(!z||x.matching_mode===z)&&(!query||[x.surface,x.group,x.explanation,x.risk,x.id].some(s=>s.toLowerCase().includes(query))));
 document.getElementById('count').textContent=n(subset.length)+' / '+n(DATA.index.length)+'事項';
 for(const x of subset){const a=node('article');const h=node('h2');h.append(node('span','',x.id+' / '+x.group));h.append(node('span','', ' '));h.append(node('span','',x.surface));a.append(h);
 const p=node('div','meta');p.append(node('span',x.matching_mode==='weak'?'badge weak':'badge',x.matching_mode));p.append(node('span','',`延べ ${n(x.surface_hits)}件／文書 ${x.documents_with_hits}件`));a.append(p);
 a.append(node('p','explain',x.explanation));a.append(node('p','risk','注意：'+x.risk));
 const details=node('details','examples');const sum=node('summary','',`原文の例 ${x.examples.length}件（例は全件ではありません）`);details.append(sum);
 for(const e of x.examples){const block=node('div','example');const link=node('a','',`${e.file}:${e.line}`);link.href='../../../../'+e.file.split('/').map(encodeURIComponent).join('/');link.target='_blank';block.append(link);block.append(node('p','',e.excerpt));details.append(block);}
 a.append(details);root.append(a);}}
[q,gr,quality].forEach(e=>e.addEventListener('input',render));render();
</script></body></html>'''
    return html.replace('__DATA__',raw)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source-zip',required=True)
    ap.add_argument('--dictionary-zip',required=True)
    ap.add_argument('--out',required=True)
    args=ap.parse_args()
    t0=time.perf_counter(); p0=time.process_time(); times={}
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    srcbytes=Path(args.source_zip).read_bytes();dicbytes=Path(args.dictionary_zip).read_bytes()
    sha_src=sha(srcbytes);sha_dict=sha(dicbytes)
    with zipfile.ZipFile(args.dictionary_zip) as dz,zipfile.ZipFile(args.source_zip) as sz:
        inv=json.loads(dz.read(SOURCE_INV));
        if sha_src!=inv['source_archive_sha256']:
            raise ValueError('Source archive SHA differs from pinned inventory')
        candidates=load_jsonl(dz.read(CANDIDATE_FILE)); defs=load_jsonl(dz.read(DICT_FILE));
        if len(candidates)!=27901 or len(defs)!=1365: raise ValueError('Unexpected candidate/draft totals')
        t1=time.perf_counter();times['input_load_seconds']=round(t1-t0,5)
        grammar=compile_patterns();gram_by_id={g['id']:g for g in grammar}
        termset={r['term'] for r in candidates}
        dset={r['term'] for r in defs}
        errors=[];documents=[];rows=[];unmatched=[]
        global_counts=collections.Counter(); file_counts=collections.defaultdict(collections.Counter)
        layer_by_path={f['path']:f['reading_layer'] for f in inv['files']}
        # All 238 source inventory documents are accounted for, but quarantine remains excluded.
        for f in inv['files']:
            rel=f['path'];lay=f['reading_layer'];included=f['read_for_creation']
            record={'path':rel,'layer':lay,'read_for_creation':included,'source_sha256':f['sha256']}
            if not included:
                record.update(status='excluded_by_source_inventory',lines=0,prose_lines_with_japanese=0,matched_lines=0,unmatched_japanese_lines=0,grammar_surface_hits=0)
                documents.append(record);continue
            raw=sz.read(PREFIX+rel)
            if sha(raw)!=f['sha256']:
                raise ValueError('Input markdown SHA does not match pinned inventory: '+rel)
            content=raw.decode('utf-8-sig')
            in_fence=False;fence_marker='';in_math=False
            prose_jp=0;matched_lines=0;unmatched_jp=0;hit_total=0;raw_lines=content.splitlines()
            for line_no,rawline in enumerate(raw_lines,1):
                stripped=rawline.strip()
                # Fence may use backticks or tildes, and include math; no code within analysis.
                fs=re.match(r'^(`{3,}|~{3,})',stripped)
                if fs:
                    typ=fs.group(1)[0]
                    if not in_fence:in_fence=True;fence_marker=typ
                    elif typ==fence_marker:in_fence=False
                    continue
                if in_fence:continue
                if stripped.startswith('$$') or stripped.startswith('\\['):
                    if stripped.count('$$')==2 and stripped!='$$': continue
                    in_math=not in_math;continue
                if in_math:continue
                # Lines made entirely of display math, links, tables dividers are skipped.
                if re.fullmatch(r'[-|: \t]+',stripped) or re.match(r'^\\(?:begin|end|text|boxed)\b',stripped):continue
                s=mask_line(rawline)
                if not JP_CHARS.search(s):continue
                prose_jp+=1
                hits_this_line=0
                for g in grammar:
                    for m in g['re'].finditer(s):
                        # A specific exception prevents the 'また' record from double counting 'または'.
                        if g['label']=='また' and s[m.end():].startswith('は'): continue
                        label=g['label']
                        # A context window is a locator, not a full original quote.
                        context=s[max(0,m.start()-58):min(len(s),m.end()+76)].strip()
                        row={'id':g['id'],'category':g['group'],'form':label,'file':rel,'line':line_no,
                             'char_start':m.start(),'char_end':m.end(),'matching_mode':g['mode'],
                             'review_state':'surface_evidence_not_grammatical_parse',
                             'excerpt':context}
                        rows.append(row)
                        global_counts[g['id']]+=1;file_counts[rel][g['id']]+=1
                        hit_total+=1;hits_this_line+=1
                if hits_this_line:matched_lines+=1
                else:
                    unmatched_jp+=1
                    unmatched.append({'file':rel,'line':line_no,'reason':'no_pattern_match',
                                      'preview':s[:160]})
            record.update(status='scanned',lines=len(raw_lines),prose_lines_with_japanese=prose_jp,
                          matched_lines=matched_lines,unmatched_japanese_lines=unmatched_jp,
                          grammar_surface_hits=hit_total)
            documents.append(record)
        t2=time.perf_counter();times['source_scan_seconds']=round(t2-t1,5)
        rows.sort(key=lambda x:(x['file'],x['line'],x['char_start'],x['id']))
        unmatched.sort(key=lambda x:(x['file'],x['line']))
        gindex=[]
        for g in grammar:
            ex=[r for r in rows if r['id']==g['id']]
            docs_count=len(set(r['file'] for r in ex))
            # E.g. pick deterministic examples spread across documents, not one top-level source.
            chosen=[];seen=set()
            # Prefer original Japanese prose in genuine sentences, not metadata or headings.
            example_ranked=sorted(ex,key=lambda r:(layer_by_path.get(r['file'])!='japanese_original_prose',
                bool(re.match(r'^\s*(?:[#|>]\s*|[-*]\s+|\d+[.)]\s+)',r['excerpt'])),
                r['file'],r['line']))
            for row in example_ranked:
                if row['file'] not in seen and len(chosen)<3:
                    chosen.append({'file':row['file'],'line':row['line'],'excerpt':row['excerpt']});seen.add(row['file'])
            gindex.append({'id':g['id'],'group':g['group'],'surface':g['label'],'explanation':g['explanation'],
                           'risk':g['risk'],'matching_mode':g['mode'],'regex':g['pattern'],
                           'surface_hits':len(ex),'documents_with_hits':docs_count,
                           'present_in_27901_candidate_registry':g['label'] in termset,
                           'present_in_1365_editorial_drafts':g['label'] in dset,
                           'examples':chosen})
        by_layer=collections.defaultdict(lambda:collections.Counter())
        for f in documents:
            c=by_layer[f['layer']]
            c['documents']+=1;c['scanned']+=int(f['status']=='scanned')
            for field in ['lines','prose_lines_with_japanese','matched_lines','unmatched_japanese_lines','grammar_surface_hits']:
                c[field]+=f[field]
        counts={'source_archive_sha256':sha_src,'dictionary_archive_sha256':sha_dict,
                'inventory_documents':len(documents),'scanned_documents':sum(f['status']=='scanned' for f in documents),
                'excluded_documents':sum(f['status']!='scanned' for f in documents),
                'japanese_primary_documents':sum(f['layer']=='japanese_original_prose' and f['status']=='scanned' for f in documents),
                'supplemental_documents':sum(f['layer']!='japanese_original_prose' and f['status']=='scanned' for f in documents),
                'prose_lines_with_japanese':sum(f['prose_lines_with_japanese'] for f in documents),
                'lines_with_grammar_surface_hits':sum(f['matched_lines'] for f in documents),
                'unmatched_japanese_lines':sum(f['unmatched_japanese_lines'] for f in documents),
                'all_surface_hits_including_overlaps':len(rows),
                'grammar_patterns':len(grammar),
                'weak_single_character_substring_hits':sum(global_counts[g['id']] for g in grammar if g['mode']=='weak'),
                'nonweak_surface_hits':sum(global_counts[g['id']] for g in grammar if g['mode']!='weak'),
                'patterns_present_in_candidate_registry':sum(g['present_in_27901_candidate_registry'] for g in gindex),
                'patterns_present_in_editorial_drafts':sum(g['present_in_1365_editorial_drafts'] for g in gindex),
                'total_term_candidates':len(candidates),'total_existing_editorial_drafts':len(defs),
                'by_layer':dict(by_layer),
                'limitations':['All surface hits, not morphological parse or word sense disambiguation.',
                   'Single-character particles count substring appearances and are not confirmed grammar tokens.',
                   'Grammatical examples are not semantic validations or logical entailment evidence.',
                   'English, code, mathematical displays, and text with no Japanese characters are out of Japanese-grammar analysis.',
                   'Pattern overlaps count independently; counts do not sum to unique grammatical constructions.',
                   'Other than the excluded 2 files, every inventory file is scanned, even if 0 Japanese prose lines.',
                   'A full Japanese grammar of all texts is not proven by a pattern atlas.'],
                'canonical':False,'human_adopted':False,'repository_applied':False}
        # Render grammar: human-authored descriptions + whole-repository recurrence and traceable usage.
        def esc(s):return s.replace('|','\\|').replace('`','\\`')
        b=[]
        b.append('# SO Repository日本語文法書――全域照合稿（第一稿）')
        b.append('')
        b.append('> 研究資料／Repository未採用・非canonical。辞書ではなく、日本語の構文・助詞・接続・限定・引用・様相を扱う文法書の第一稿。')
        b.append('> 分析器は日本語の形態素・係り受けを判定しない。原文に対する**表面形式の全域照合**と、LLMが設計した用法解説の二段階である。')
        b.append('> 件数は文法的用法の正確な出現数ではない。とくに一字助詞、重なり、引用、式やコードの除外は下記の限界を読むこと。')
        b.append('')
        b.append('## はじめに――文法と辞書を分ける')
        b.append('')
        b.append('辞書は語や概念の意味・使用条件を扱う。文法は、主張が何を主題にし、何を否定し、どの条件へ限定し、どこまでを仮定し、どの言葉を引用や帰属として扱うかという結合の形式を扱う。')
        b.append('')
        b.append('「したがって」と書かれていても実際に結論が導かれるとは限らない。「と定義する」と書かれていてもその定義がRepository正本とは限らない。文法形式、主張の身分、推論の妥当性は別の層にある。')
        b.append('')
        b.append('本稿では、入力の全文書を走査したうえで、日本語文法に関わる表記候補を記録する。下記の出現例は説明の補助であり、当該行の構文解析済み証拠ではない。')
        b.append('')
        b.append('## 対象と確認できた規模')
        b.append('')
        b.append(f"- 原文アーカイブ固定SHA-256：`{sha_src}`")
        b.append(f"- 対象 inventory {counts['inventory_documents']} Markdownのうち、検査対象 {counts['scanned_documents']}、原判定で除外した {counts['excluded_documents']}。")
        b.append(f"- 日本語本文層 {counts['japanese_primary_documents']} 文書、その他 {counts['supplemental_documents']} 文書（英語主体・形成史・索引等も含む）を走査した。")
        b.append(f"- 日本語を含む非コード行 {counts['prose_lines_with_japanese']:,}、うち選定表面形式に一致した行 {counts['lines_with_grammar_surface_hits']:,}、未一致 {counts['unmatched_japanese_lines']:,}。")
        b.append(f"- 用法の観測対象 {len(grammar)} 項目、延べ表面一致 {len(rows):,} 件（重複算入）。うち一文字などの弱い表記一致 {counts['weak_single_character_substring_hits']:,} 件、相対的に検査しやすい表現一致 {counts['nonweak_surface_hits']:,} 件。")
        b.append(f"- 27,901件の表記候補と照合すると、文法書の表記のうち {counts['patterns_present_in_candidate_registry']} 項目が一致。既存1,365件の暫定定義と一致した表記は {counts['patterns_present_in_editorial_drafts']} 項目。意味が自動統合されたわけではない。")
        b.append('')
        b.append('## 読み方と失敗モード')
        b.append('')
        b.append('1. 文章の「は」と別の語に埋まった「は」を機械的に区別していない。**一字助詞の出現数を助詞の正確な頻度と読まない**。')
        b.append('2. 正規表現に一致しない用法も存在し得る。逆に、一致した文字列が別の機能を持つ場合がある。')
        b.append('3. 一つの行に複数の文法項目が現れることがある。各項目の件数は重複算入であり、単純に足して文数を出さない。')
        b.append('4. 原文の所在は独立した `grammar_surface_concordance.jsonl` に記録する。文法書本文は原文正本を変更しない。')
        b.append('5. 項目の解説は機能の候補であり、個々の出現がその機能に当たることを確認したものではない。')
        b.append('')
        b.append(SYNTHESIS)
        b.append('## 第二部　各章の用法とRepository中の例')
        b.append('')
        for group,desc in GROUP_DESC.items():
            b.append('### '+group)
            b.append('');b.append(desc);b.append('')
            for g in gindex:
                if g['group']!=group:continue
                b.append(f"#### {g['id']}　{g['surface']}")
                b.append('')
                b.append('**働き：** '+g['explanation']+'。')
                b.append('');b.append('**混同・限界：** '+g['risk']+'。')
                b.append('')
                b.append(f"照合：延べ表面一致 **{g['surface_hits']:,} 件**／出現文書 **{g['documents_with_hits']} 件**。出現型 `{g['matching_mode']}`。27,901候補に同表記：{'あり' if g['present_in_27901_candidate_registry'] else 'なし'}。")
                b.append('')
                if g['examples']:
                    b.append('**原文上の例（照合位置）：**')
                    b.append('')
                    for ex in g['examples']:
                        b.append(f"- `{ex['file']}:{ex['line']}`：{ex['excerpt']}")
                else:
                    b.append('**原文上の例：**今回の対象範囲では表面一致なし。説明は文法上の検査項目として保持。')
                b.append('')
        b.append('## 辞書との境界')
        b.append('')
        b.append('本稿は助詞・接続・条件・否定・引用等の**働き**を扱う。例えば「は」の表面一致を辞書の一語へ登録したという主張ではない。「正しさ」「境界」「Return」など概念の定義と用法差は、辞書側で扱う。')
        b.append('')
        b.append('概念を示す語が文法上の働きも持つ場合、辞書と文法の両方からその位置を参照できる。ただしその両者を同一の定義へ統合する必要はない。')
        b.append('')
        b.append('## 未達成の検証')
        b.append('')
        b.append('文法表面の全域照合は終えたが、日本語全文の形態素解析・依存構造解析・語義の曖昧性解消を全件実施したわけではない。厳密な文法分類の正答率も未測定。')
        b.append('辞書に何件収録されるかの正確な推定は、今回の文法書だけからは得られない。')
        b.append('また、補助層に含まれる英文の英文法は本稿の対象外。英語通約と日本語正本を混同しない。')
        b.append('')
        b.append('## 27,901表記候補との交差台帳')
        b.append('')
        b.append('`candidate_boundary_27901.jsonl` は全候補について、文法書の選定表記との**完全一致**を示す。非一致は辞書採録済みや辞書適格を意味しない。文法側の表記一致も形態素の検査を要する。')
        b.append('')
        b.append('## 再実行と機構解析')
        b.append('')
        b.append('生成スクリプトは、入力ZIPと辞書ZIPのSHAを固定し、すべての対象Markdownの内容SHAを照合してから走査する。')
        b.append('原文を隠して「分類済み」と宣言するのではなく、全一致を行・文字位置付きで記録し、未一致行も記録する。')
        b.append('解析器が使った表現規則、対象範囲、除外規則は `grammar_patterns.json` と `coverage.json` にある。')
        b.append('再計算時の実行時間・CPU・メモリは可変なので、決定的成果物と分けて `runtime_metrics.json` に書く。ChatGPT内部のトークン数と推論処理量は取得できないため、不明として記録する。')
        b.append('')
        textfile(out/'SO_repository_grammar_all_surface_ja.md','\n'.join(b)+'\n')
        rule_export=[{k:v for k,v in g.items() if k!='re'} for g in grammar]
        textfile(out/'grammar_patterns.json',rule_export)
        textfile(out/'grammar_index.json',gindex)
        textfile(out/'grammar_viewer.html',render_viewer(gindex,counts))
        textfile(out/'coverage.json',counts)
        # Every one of the 27,901 surface candidates gets a visible handoff state.
        exact_lookup=collections.defaultdict(list)
        for g in grammar:exact_lookup[g['label']].append(g['id'])
        boundary=[]
        for candidate in candidates:
            ids=exact_lookup.get(candidate['term'],[])
            boundary.append({'term':candidate['term'],
                'literal_observations':candidate.get('literal_observations'),
                'input_review_status':candidate.get('review_status'),
                'input_surface_kinds':candidate.get('surface_kinds',[]),
                'exact_grammar_form_matches':ids,
                'state': 'grammar_form_overlap_context_required' if ids else 'not_in_selected_grammar_forms_dictionary_eligibility_undecided',
                'not_a_semantic_or_lexical_validation':True})
        textfile(out/'candidate_boundary_27901.jsonl',''.join(json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n' for x in boundary))
        textfile(out/'source_document_coverage.jsonl',''.join(json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n' for x in documents))
        textfile(out/'grammar_surface_concordance.jsonl',''.join(json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n' for x in rows))
        textfile(out/'japanese_lines_without_selected_patterns.jsonl',''.join(json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n' for x in unmatched))
        t3=time.perf_counter();times['output_render_seconds']=round(t3-t2,5)
        mem=resource.getrusage(resource.RUSAGE_SELF) if resource is not None else None
        metrics={'wall_clock_seconds':round(time.perf_counter()-t0,4),'cpu_time_seconds':round(time.process_time()-p0,4),
                 'peak_rss_platform_units':mem.ru_maxrss if mem is not None else None,'peak_rss_units_note':'KiB on Linux; bytes on macOS; unavailable on Windows',
                 'source_zip_size_bytes':len(srcbytes),'dictionary_zip_size_bytes':len(dicbytes),
                 'source_markdown_bytes_scanned':sum(f['bytes'] for f in inv['files'] if f['read_for_creation']),
                 'input_japanese_surface_candidates':len(candidates),'input_assistant_editorial_drafts':len(defs),
                 'selected_grammar_patterns':len(grammar),'candidate_surface_hits':len(rows),
                 'jsonl_evidence_rows':len(rows)+len(unmatched)+len(documents)+len(candidates),
                 'script_calls_to_external_llm_api':0,
                 'chatgpt_model_inference_cost':'not observable in this environment',
                 'source_sha256':sha_src,'dictionary_sha256':sha_dict,
                 'phase_time_seconds':times}
        textfile(out/'runtime_metrics.json',metrics)
        print(json.dumps({'summary':{k:counts[k] for k in ['inventory_documents','scanned_documents','prose_lines_with_japanese','lines_with_grammar_surface_hits','unmatched_japanese_lines','grammar_patterns','all_surface_hits_including_overlaps']},'resources':metrics},ensure_ascii=False,indent=2))

if __name__=='__main__':main()

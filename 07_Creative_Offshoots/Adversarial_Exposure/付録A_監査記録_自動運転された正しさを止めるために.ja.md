# 付録A　監査記録――三論点統合論考との相互照合と残差集積

> Role: cross-application structural audit / residual accumulation
> Current definition owner: [『正しさ・個性・無・切断――論理と通信トポロジーから組み立てる「正しい」の工学的定義』](../../01_Sat_Truth/正しさ・個性・無・切断_論理通信トポロジー.ja.md)
> Related application: [『自動運転された正しさを止めるために――Business、自然災害認定、心の継承をめぐる構造と判断の責任』  ](自動運転された正しさを止めるために.ja.md)
> Status: Appendix / audit record / non-canonical extension candidate
> Scope: correctness / action closure / authority / return / actuation / individuality / provenance / proxy return / irreversible residual
> Reading rule: 本付録は、正本の定義を書き換えるものではない。正本を三つの応用論点へ接触させた結果として露出した残差を記録し、どの残差が正本の内部で処理でき、どの残差が次層の理論を要求するかを区別するための監査記録である。A.1はこの監査に必要な操作的投影であり、現行正本の完全な再掲ではない。定義上の差異がある場合はcurrent definition ownerを優先する。
> Layer: 07_Creative_Offshoots / Adversarial_Exposure
> Language: Japanese authoritative; English commensuration in a separate file
> English commensuration: [English audit record](Appendix_A_Audit_Record_Cross_Collation_and_Residual_Accumulation.en.md)
> Authority: この接触と残差の記録を保持する。正本の定義を追加・置換する権限は持たない。

---

## A.0　監査の目的

本付録の目的は、三つの論点――Businessの最適化、人間関係における「自然災害認定」、身体の死後にも残り得る心的作用とprovenance――を、『正しさ・個性・無・切断』の工学的定義へ接触させ、その対応関係と未処理残差を記録することである。

この監査では、三論点を「正本の具体例」として一方向に説明するだけでは足りない。応用先へ正本を降ろしたとき、正本側に不足していた区別が露出する可能性があるからである。したがって、監査方向は双方向とする。

$$
\text{Foundational Model}
\;\longrightarrow\;
\text{Application}
$$

だけでなく、

$$
\text{Application}
\;\longrightarrow\;
\text{Residual}
\;\longrightarrow\;
\text{Foundational Re-audit}
$$

を含める。

本付録で扱う三論点は同じ現象ではない。市場・組織、対人関係、履歴継承を一つの法則へ還元することもしない。共通して問うのは、有限な系が複雑な対象を扱うために圧縮・抽象化・仮閉鎖を行ったあと、その圧縮から漏れた差分をどのように保持し、どこまで現在の判断へ返せるか、という構造である。

---

## A.1　監査に必要な正本の最小理解

本節は、正本を事前に読んでいない監査者が、本付録だけを用いて最低限の監査を再現できるようにするための要約である。以下は正本の完全な代替ではないが、本付録で使用する記号と条件を定義する。

ここで再現するのは、この監査を再現するために必要な最小投影である。現行正本の完全な再掲や版固定コピーではない。監査記録としてのQ1–Q14と、現行正本における概念の採否は分けて読む。現行定義の確認には上記current definition ownerを用いる。

### A.1.1　現在の論理空間

時点 $t$ において、系が区別・探索・比較・再照合できる論理空間を

$$
\Omega_t
$$

とする。

少なくとも、

$$
\Omega_t
=
\{E_t,A_t,\Pi_t,H_t,Q_t,B_t\}
$$

を含む。

ここで、

- $E_t$：観測・入力された事実候補
- $A_t$：現在受理している命題・関係
- $\Pi_t$：推論・変換・探索規則
- $H_t$：形成履歴
- $Q_t$：未処理差分・open end・residual
- $B_t$：利用可能な探索資源

である。

最も重要な境界条件は、

$$
\Omega_t \neq \text{World}
$$

である。系が現在扱える範囲と、世界そのものを同一視してはならない。

### A.1.2　内部成立性

状態 $S_t$ が「正しい」と扱われる前に、少なくとも内部成立性

$$
I(S_t)
$$

を要求する。

内部成立性とは、既知の矛盾を未処理のまま隠していないこと、根拠のないjoinを置いていないこと、支持経路や形成条件へ戻る経路を必要な範囲で保持していること、未処理差分を解決済みとして偽装していないこと、適用範囲外へ結論を延長していないことを含む。

要するに、

> 残っているものを、残っていないことにしない。

という条件である。

### A.1.3　frontier、探索履歴、defeater

現在の資源 $B_t$ と探索器 $\Pi_t$ のもとで、何を探索対象として構成できるかを

$$
\mathcal{F}_{B_t}(S_t,\Pi_t)
$$

とする。

実際に行われた探索履歴を

$$
\tau_t
$$

とする。

そして、その探索の中で、現在の妥当性を変更・保留・局所化させるものをdefeaterと呼ぶ。反例だけでなく、支持経路の失効、未検討の代替説明、見落としていた分岐、履歴整合性の破壊なども含む。

実際に発見されたdefeater集合を、

$$
D_{B_t}(S_t,\Pi_t;\tau_t)
$$

とする。

### A.1.4　探索飽和と $D=\varnothing$ / $D=\bot$

単に「反論が見つからなかった」だけでは正しさを認定しない。

実際の探索履歴 $\tau_t$ があり、かつ、

$$
\operatorname{Sat}(\tau_t\mid S_t,\Pi_t,B_t)=1
$$

すなわち、現在の探索規則と資源条件のもとで、実行すべき探索を実際に試み、そのうえで妥当な探索飽和として停止した場合にのみ、defeater集合を評価する。

その条件を満たしたうえでdefeaterが見つからなければ、

$$
D_{B_t}(S_t,\Pi_t)=\varnothing
$$

である。

一方、探索していない、資源切れで止まった、探索器が壊れた、portを閉じた、return pathが切れた、同じ場所を循環した、といった場合は、

$$
D_{B_t}(S_t,\Pi_t)=\bot
$$

すなわち未判定である。

この区別は本付録全体で最重要となる。

### A.1.5　Return / Reopening

正本では、

$$
R(S_t)
=
\operatorname{Ingress}(S_t)
\land
\operatorname{Traceback}(S_t)
\land
\operatorname{Reopen}(S_t)
$$

と置く。

Ingressは、現在の妥当性を変更し得る差分が監査構造へ入ってこられることを意味する。

Tracebackは、現在の判断からsupport、変換、形成履歴、入力資料・観測条件、適用範囲へ必要な範囲で戻れることを意味する。ここで戻るのは、判断を成立させた追跡可能な支持構造であり、最終的な形而上学的根拠を所有することではない。

Reopenは、新しい差分やsupport失効が来たとき、現在の仮閉鎖を解除して再検査へ戻せることを意味する。

### A.1.6　工学的な「正しい」

以上から、正本の最小形は、

$$
\boxed{
C_{B_t}^{(k)}(S_t)
=
I(S_t)
\land
\bigl(D_{B_t}(S_t,\Pi_t^{(k)})=\varnothing\bigr)
\land
R(S_t)
}
$$

である。

これは哲学一般のtruthを所有したという意味ではない。

意味するのは、

> 現在の資源・探索器・形成履歴のもとで内部成立性を保ち、実際に壊しに行き、探索飽和後にもdefeaterを発見できず、なお新しい差分が来たとき支持経路・形成条件へ戻って再び開ける。

という工学的状態である。

### A.1.7　個性

個性は性格ラベルではなく、探索構造として、

$$
K=(s_0,\Pi,H,\rho)
$$

と置かれる。

$s_0$ は探索開始状態、$\Pi$ は探索作用素群、$H$ は形成履歴、$\rho$ は有限資源をどこへ配るかという優先規則である。

したがって、異なる個性は、

$$
\operatorname{Reach}_B(K_A)\neq \operatorname{Reach}_B(K_B)
$$

となり得る。

ここから、個性は真偽を自由に決めるものではなく、何がその「正しさ」を破り得るかへの到達可能性を変えるfrontier generatorとして扱われる。

### A.1.8　無・切断・残差・圧

正本では「無」を一種類にまとめず、Pure Unknown、Expected Missing、Cut、Resource Boundary、Deliberate Sealなどに分ける。

重要なのは、

$$
r(v)=\operatorname{Expected}(v)-\operatorname{Observed}(v)
$$

という抽象的な残差である。

期待された接続と観測された状態の差が残差を作る。

下流の残差を逆向きに集約した探索優先度の候補を、

$$
P(v)
=
\sum_{u\in Desc(v)}w(u,v)|r(u)|
$$

のように置く。

ただし、

$$
P(v)\not\Rightarrow \operatorname{Truth}(v)
$$

である。

圧は「ここに真理がある」という信号ではなく、「現在構造と入力世界の関係がうまくいっていないので再検査せよ」という信号である。

### A.1.9　通信トポロジー

系を、

$$
G=(V,E,P,H)
$$

と見る。

$V$ は状態・概念・観測・判断のnode、$E$ はsupport・変換・依存・returnなどのedge、$P$ は外部port、$H$ は形成・変更履歴である。

基本的な故障形は二つある。

一つは、本来つながるべき経路が通らないCutである。

もう一つは、根拠のない因果・不当な一般化・別履歴の同一視など、つながってはいけないものをつなぐUnsupported Joinである。

---

## A.2　三論点を共通形式へ写像する

三論点には、有限な目的のために対象を圧縮して扱うという共通操作がある。

一般形を、

$$
X_i
\xrightarrow{\Phi_i}
M_i
\xrightarrow{\Pi_i}
Y_i
$$

と置く。

ここで、

- $X_i$：本来の対象
- $\Phi_i$：圧縮・抽象化・モデル化
- $M_i$：運用上のモデル
- $\Pi_i$：そのモデル上での推論・最適化・判断
- $Y_i$：出力・結果

である。

Businessでは、

$$
X_B=
\text{人間・時間・土地・技能・関係}
$$

を、

$$
\Phi_B
$$

によって価格、工数、利益、稼働率、単価などの運用変数へ圧縮する。

自然災害認定では、

$$
X_N=
\text{相手という人間全体}
$$

を、

$$
\Phi_N
$$

によって「現在の関係で観測できる反応パターン」へ圧縮する。

心的履歴の継承では、

$$
X_H=
\text{生きた経験・判断・形成履歴}
$$

を、

$$
\Phi_H
$$

によって文章、教訓、制度、記録へ圧縮する。

この操作自体は不正ではない。有限系が対象全体を保持できない以上、圧縮は必要である。

危険なのは、

$$
M_i \equiv X_i
$$

と扱い始めたときである。

すなわち、扱うために作ったモデルが対象全体への定義権限を取得する。

本付録では、この状態を監査用の暫定記号として、

$$
\operatorname{FC}(S)
=
\operatorname{TreatAsClosed}(S)
\land
\Bigl[
D(S)=\bot
\;\lor\;
\neg R(S)
\;\lor\;
\operatorname{ScopeOverflow}(S)
\Bigr]
$$

と置く。

$\operatorname{FC}$ はFalse Closureの監査記号であり、正本の正規記号ではない。

意味するのは、

> 本来は正しさを閉じる条件を満たしていない、あるいは適用範囲を越えているのに、運用上は「すでに正しい・すでに十分・もう検査不要」として扱われている状態

である。

Businessでは「黒字だから構造全体としてよい」。

自然災害認定では「何度言っても変わらなかったから、この人は変われない」。

履歴継承では「昔から残っている教訓だから、今も正しい」。

いずれも、局所的な成立を対象全体へ拡張する可能性を持つ。

---

## A.3　監査対象1――Businessと社会的return

### A.3.1　正本との直接対応

Business論で最も直接的に対応するのはCutとReturnである。

たとえば、無理な納期が達成されたとする。意思決定者には「納品成功」が返るが、その達成によって生じた疲労、離職、学習機会の喪失が意思決定面へ戻らない場合、

$$
Y_{\mathrm{success}}
\rightarrow
\operatorname{Decision}
$$

は成立する一方、

$$
Q_{\mathrm{cost}}
\nrightarrow
\operatorname{Decision}
$$

となる。

これは通信トポロジー上のCutとして読める。

ここで重要なのは、苦情窓口やアンケートの存在だけではreturnを保証しないことである。

情報が入ってきても、判断条件や資源配分を変更できなければ、Ingressは存在しても実効的なreturnにはなっていない可能性がある。

### A.3.2　残差：Actuate

正本の

$$
R
=
\operatorname{Ingress}
\land
\operatorname{Traceback}
\land
\operatorname{Reopen}
$$

は認識・監査系として強い。

しかし社会制度へ降ろすと、新しい残差が出る。

異議が入る。

原因へ戻れる。

再検査もできる。

それでも、決定を変える権限、予算、人員、実装経路がなければ、社会的には「返った」と言えるのか。

そこで本付録では監査用候補として、

$$
R_{\mathrm{social}}^{*}
=
\operatorname{Ingress}
\land
\operatorname{Traceback}
\land
\operatorname{Reopen}
\land
\operatorname{Actuate}
$$

を置く。

ここで $\operatorname{Actuate}$ は、

> 再照合によって変更された判断を、実際の決定・資源配分・手続・実装へ戻せる作用経路

を指す。

これは正本への追加定義ではない。

むしろ、

$$
R \stackrel{?}{\Longrightarrow} \text{social correction}
$$

が必ずしも成立しないという応用上の残差である。

### A.3.3　外部化とreturnの非対称性

Businessでは、決定した主体と費用を受け取る主体が異なることがある。

したがって、

$$
\operatorname{DecisionActor} \neq \operatorname{CostBearer}
$$

が成立し得る。

このとき、失敗が発生しても、

$$
Q_{\mathrm{cost}}
$$

が決定者へ戻らず、第三者の負担として吸収される可能性がある。

この残差は、単に「経営者が悪い」と読むべきではない。

見るべきなのは、

$$
\text{Who decides?}
$$

$$
\text{Who receives the effect?}
$$

$$
\text{Who can reopen the decision?}
$$

の三点が一致しているか、または有効に接続されているかである。

---

## A.4　監査対象2――自然災害認定とAction Closure

### A.4.1　最重要分離

自然災害認定を正本へ接触させたとき、最も大きい残差は、

$$
\operatorname{EpistemicClosure}
\neq
\operatorname{ActionClosure}
$$

である。

相手が将来変化し得るかという命題について、十分な探索飽和に達していない場合、

$$
D_{B_t}(P_{\mathrm{other\ updateable}})=\bot
$$

である。

これは「相手は変われない」とは言えない状態である。

しかし、自分の身体・時間・安全・生活条件を守るため、

$$
\operatorname{Close}_{\mathrm{action}}=1
$$

とすることは可能である。

したがって、

$$
\operatorname{Close}_{\mathrm{action}}=1
$$

と、

$$
\operatorname{Close}_{\mathrm{claim}}=0
$$

は両立する。

意味するのは、

> 私は、あなたが永久に変われないとは確定しない。しかし、その確認のために、これ以上自分の身体と時間を使うことはしない。

という状態である。

### A.4.2　Resource Boundary / Deliberate Sealとの関係

自然災害認定後の退避は、正本の分類ではResource BoundaryまたはDeliberate Sealと接触する。

つまり、

$$
B_t \leq B_{\min}
$$

となった、または安全・回復上の理由から、

$$
\operatorname{DeliberateSeal}=1
$$

とする。

このとき静けさが生じても、それを探索飽和と混同してはならない。

$$
\operatorname{Silence}
\not\Rightarrow
D=\varnothing
$$

である。

### A.4.3　個性による観測軸の違い

正本では個性を、

$$
K=(s_0,\Pi,H,\rho)
$$

と置く。

すると、こちらの観測軸 $\rho_A$ では更新が見えなくても、

$$
\operatorname{Observed}_{\rho_A}(\operatorname{Update}_B)=0
$$

から、

$$
\operatorname{Update}(B)=0
$$

とは導けない。

相手が別の条件・別の関係・別の軸で更新している可能性は残る。

この残差は自然災害認定を弱体化するものではない。

むしろ、

$$
\operatorname{Close}_{\mathrm{action}}=1,
\qquad
\operatorname{Close}_{\mathrm{claim}}=0
$$

という分離を必要とする理由になる。

### A.4.4　私的退避と公的断定の証拠負担

相手について広い否定的主張を公表することと、自分が接触を減らすことでは、必要な根拠強度が異なる。

したがって、

$$
\operatorname{EvidenceThreshold}_{\mathrm{public\ claim}}
>
\operatorname{EvidenceThreshold}_{\mathrm{private\ retreat}}
$$

となり得る。

これは「私的判断なら何でもよい」という意味ではない。

私的退避の主眼が自分の資源配分であるのに対し、公的断定は相手の評判・権利・機会へ作用するためである。

### A.4.5　鏡像性と権力非対称

相手もこちらを固定的な反応系として扱っている可能性はある。

しかし、

$$
\operatorname{MutualModeling}
$$

があることと、

$$
\operatorname{MutualPower}
$$

が等しいことは別である。

接触を強制できる側と離脱しにくい側では、同じ「拒否」「固定化」「切断」でも作用が異なる。

したがって、鏡像性を発見しても、

$$
\operatorname{Responsibility}_A=\operatorname{Responsibility}_B
$$

とは自動的に置かない。

---

## A.5　監査対象3――身体・心・provenanceとProxy Return

### A.5.1　作用継続と主体継続の分離

人の身体が停止した後も、文章、制度、教訓、判断基準が作用し続けることはある。

しかし、

$$
\operatorname{Effect}_{t>\mathrm{death}}\neq 0
$$

から、

$$
\operatorname{Subject}_{t>\mathrm{death}}\neq 0
$$

は導けない。

作用の継続と本人の主観的継続を分ける。

### A.5.2　元主体へのreturnが不可能になる場合

本人が死亡した場合、あるいは組織が消滅した場合、

$$
\operatorname{Ingress}_{\mathrm{source}}=0
$$

となり得る。

元の主体へ返せない残差が残る。

そこで、

$$
S_0
\rightarrow
\operatorname{Artifact}
\rightarrow
S_1
$$

という後続構造を考える。

$S_0$ は元主体、Artifactは文章・記録・制度・データ、$S_1$ は後続の読者・組織・監査主体である。

ここで、

$$
R_{\mathrm{successor}}
=
\operatorname{Ingress}(S_1)
\land
\operatorname{Traceback}_{\mathrm{archive}}
\land
\operatorname{Reopen}(S_1)
$$

というProxy / Successor Returnの候補が現れる。

意味するのは、

> 残差を必ず発生源へ戻すのではなく、残差を再判断可能な後続主体へ接続する。

ということである。

これは正本のreturn概念の置換ではない。

元主体が消滅したとき、returnをどこまで拡張して読めるかという未解決点である。

### A.5.3　provenanceは妥当性を保証しない

履歴へ戻れることは重要だが、

$$
\operatorname{Provenance}(x)
\not\Rightarrow
\operatorname{Validity}(x)
$$

である。

誤った判断にも履歴はある。

偏見にも形成理由はある。

したがってprovenanceは、

> 正しいことの証明

ではなく、

> 再検査を可能にする入口

として扱う。

### A.5.4　不可逆残差

すべての残差を回収できるとは限らない。

元の記録がなく、当事者も死亡し、関係者の記憶も失われた場合、

$$
\operatorname{Traceback}=0
$$

となることがある。

ここで「返路を作れば解決する」と考えること自体が偽閉鎖になり得る。

したがって、

$$
\operatorname{IrrecoverableResidual}
$$

を理論上認める必要がある。

不可逆残差が存在することは、returnを不要にするのではない。

むしろ、失われる前に何を残すべきかという事前設計の重要性を上げる。

---

## A.6　統合論考そのものへのCorrectness Audit

監査対象論考を $T$ とする。

ここでは、その論考自体を正本の工学的正しさへ入れて監査する。

### A.6.1　内部成立性

$$
I(T)
$$

は比較的強い。

理由は、元三論点にあった危うい飛躍をかなり自覚的に縮小しているためである。

たとえば、

$$
\operatorname{Resources}\uparrow
\Rightarrow
\operatorname{Judgment}\downarrow
$$

を一般則として置かず、

$$
\operatorname{Resources}\uparrow
\Rightarrow
\text{ability to continue after error may increase}
$$

へ限定している。

また、

$$
\operatorname{ObservedUpdate}=0
\Rightarrow
\operatorname{UpdateImpossible}
$$

を退け、

$$
\operatorname{ObservedUpdate}=0
\land
B_t\text{ exhausted}
\Rightarrow
\text{action may close while claim remains open}
$$

という方向へ修正している。

さらに、

$$
\operatorname{EffectContinuation}
\neq
\operatorname{SubjectContinuation}
$$

を明示している。

### A.6.2　Ingress / Traceback / Reopen

論考は、自分自身への反論可能性を明示しており、Ingressは比較的強い。

元の三論点への由来と修正理由も追えるため、Tracebackも比較的強い。

「この論をどこから殺せるか」「おまえこそ自然災害ではないか」を置いているため、Reopenも意識的に設計されている。

### A.6.3　defeater状態

ただし、

$$
D_T=\varnothing
$$

とは評価できない。

監査で実施したのは、内部整合監査、概念的反例生成、適用範囲縮小、自己適用、provenance監査、三領域間の構造比較である。

Business、組織論、意思決定論、権力論、心理学、記憶研究、倫理学など、異なる探索器による十分な外部探索はまだ行っていない。

したがって、

$$
D_T=\bot
$$

が妥当である。

これは否定評価ではない。

現時点の適切な状態記述は、

> Strong provisional research state / not correctness-certified

である。

### A.6.4　暫定Correctness Certificate

```text
Correctness Certificate — Audit Target T

State:
  Business / 退避 / 履歴継承に共通する
  「圧縮 → 局所成立 → 偽閉鎖 → 残差切断」構造仮説

Internal consistency:
  comparatively strong
  normative bridge remains unresolved

Search operators executed:
  - internal consistency audit
  - counterexample generation
  - scope restriction
  - self-application
  - provenance audit
  - cross-domain structural comparison

Saturation:
  NO

Termination reason:
  current writing / audit stopping point
  not search saturation

Defeater status:
  ⊥  UNDETERMINED

Ingress:
  explicitly designed

Traceback:
  comparatively strong

Reopen:
  explicitly designed

Known unopened regions:
  - action authorization
  - power asymmetry
  - institutional actuation
  - individuality-dependent observation
  - irreversible residual
  - proxy / successor return
  - empirical validation
  - evaluator-side boundary pressure

Overall:
  not correctness-certified
  strong provisional research state
```

---

## A.7　残差集積

残差を一つの数値へ合算しない。

Business、対人関係、履歴継承、論考自身では、残差の意味と影響範囲が異なるからである。

したがって、

$$
\mathbf Q
=
(Q_1,Q_2,\ldots,Q_n)
$$

という残差ベクトルとして保持する。

### Q1　Epistemic Correctness と Action Authorization は別である

$$
C_{\mathrm{epistemic}}
\neq
Permit_{\mathrm{action}}
$$

正しいと判断できることと、世界へ介入してよいことは同じではない。

これは本監査で露出した最重要残差である。

### Q2　Action Closure と Claim Closure は別である

$$
\operatorname{Close}_{\mathrm{action}}=1
$$

であっても、

$$
\operatorname{Close}_{\mathrm{claim}}=0
$$

であり得る。

人は、相手の本質を確定しなくても、接触を止めてよい場合がある。

### Q3　社会的ReturnにはActuateが必要か

$$
R_{\mathrm{social}}^{*}
\stackrel{?}{=}
R\land \operatorname{Actuate}
$$

異議が入り、根拠へ戻り、再検査できても、決定変更の権限経路がなければ社会的returnと呼べるか。

未解決である。

### Q4　Expectedのprovenance

残差は、

$$
r(v)=\operatorname{Expected}(v)-\operatorname{Observed}(v)
$$

で定義される。

しかしExpected自体が誤っていれば、残差圧は偽誘導を起こす。

したがって、

$$
\operatorname{Provenance}(\operatorname{Expected})
$$

とExpectedの失効条件が必要になる。

### Q5　個性依存の観測差

$$
\operatorname{Observed}_{\rho_A}(\operatorname{Update}_B)=0
\not\Rightarrow
\operatorname{Update}(B)=0
$$

別個性・別探索幾何による更新を、自分の観測軸だけでゼロ判定しないための条件が必要である。

### Q6　Proxy / Successor Return

元主体が消滅した場合、

$$
\text{Return to Source}
$$

が不可能になる。

そのとき、

$$
\text{Return to Re-auditable Successor}
$$

をreturn概念へ含めるかは未解決である。

### Q7　私的退避が第三者へ残差を移す問題

個人が正当に退避しても、その負担が別の個人へ移る場合がある。

$$
\operatorname{PrivateClosure}
\rightarrow
\operatorname{ExternalResidual}
$$

が発生し得る。

したがって、個人の退避を否定せず、制度側で残差の再配分を監査する必要がある。

### Q8　provenanceと妥当性の非同一性

$$
\operatorname{Provenance}
\neq
\operatorname{Validity}
$$

由来へ戻れることは、由来が正しいことを保証しない。

### Q9　Businessの系境界

「Business」という語の中に、企業、契約、市場、所有、法制度、労働関係、消費者選択を同時に入れると、

$$
G_B
$$

の境界が曖昧になる。

どのnodeがどのedgeを変更できるかを分けないと、責任主体が混ざる。

### Q10　監査対象論考は未飽和である

$$
D_T=\bot
$$

である。

内部成立性が高いことと、外部探索が飽和したことは区別する。

### Q11　同じ圧縮操作でも権力効果は同じではない

Businessが他者を運用するために圧縮する場合と、個人が自分の接触を減らすために圧縮する場合は、

$$
\Phi_B
$$

と

$$
\Phi_N
$$

に形式的類似があっても、他者への作用範囲が異なる。

したがって、

$$
\operatorname{SameOperation}
\not\Rightarrow
\operatorname{SameResponsibility}
$$

である。

### Q12　Irrecoverable Residual

すべての残差に返路を作れるとは限らない。

$$
Q_{\mathrm{irrecoverable}}\neq\varnothing
$$

を理論上認める必要がある。

### Q13　停止条件と無限自己監査

監査を監査し続ければ無限後退する。

したがって、

$$
\operatorname{AuditClosure}
$$

そのものに正当な停止条件が必要である。

ただし、その停止を

$$
\operatorname{Correctness}
$$

と同一視してはならない。

### Q14　スケール横断による偽同型

個人、企業、社会、死後の履歴継承へ同じ記号を使うと、構造的類似を存在論的同一性へ読み替える危険がある。

したがって、

$$
\operatorname{StructuralSimilarity}
\neq
\operatorname{OntologicalIdentity}
$$

を明示する必要がある。

---

## A.8　最重要残差――「正しさ」から「介入」への橋

本監査で最も大きい残差は、正本が扱うCorrectnessと、現実のAction Authorizationの間にある。

正本は、

$$
C_{B_t}^{(k)}(S_t)
$$

をかなり厳密に定める。

しかし、

$$
C_{B_t}^{(k)}(S_t)=1
$$

であっても、

$$
\operatorname{MayDo}(a)=1
$$

とは限らない。

つまり、

$$
\operatorname{Know}(P)
\not\Rightarrow
\operatorname{MayDo}(A)
$$

である。

この間には、少なくとも次のような別条件が存在する可能性がある。

$$
\operatorname{Authority}
$$

$$
\operatorname{Consent}
$$

$$
\operatorname{BoundaryRespect}
$$

$$
\operatorname{BurdenDistribution}
$$

$$
\operatorname{Safety}
$$

$$
\operatorname{Reversibility}
$$

$$
\operatorname{ThirdPartyImpact}
$$

ただし、本付録ではこれらをCanonicalなAction Authorization式として確定しない。

監査用の候補として、

$$
\operatorname{Auth}_t(a)
\stackrel{?}{=}
C_{B_t}^{(k)}(S_t)
\land
\operatorname{Jurisdiction}_t(a)
\land
\operatorname{Boundary}_t(a)
\land
\operatorname{Burden}_t(a)
\land
\operatorname{Safety}_t(a)
$$

程度の形を置けるが、各項の定義は未確定である。

重要なのは式そのものではない。

> 世界について正しく知ることと、世界をこちらの判断で変更する権利を持つことは別である。

という残差を保持することである。

本監査では、これは小修正ではなく、次層の理論候補と判定する。

---

## A.9　監査者向け再現手順

この付録を用いて別の論考・制度・人間関係・AI出力を監査する場合、次の順序を推奨する。

第一に、監査対象 $S$ と系境界を明示する。対象が個人なのか、組織なのか、制度なのか、文書なのかを混ぜない。

第二に、対象が何を圧縮して扱っているかを記述する。

$$
X
\xrightarrow{\Phi}
M
$$

を置き、$M$ が $X$ 全体だと誤認されていないかを見る。

第三に、内部成立性 $I(S)$ を監査する。既知矛盾、Unsupported Join、適用範囲超過、未処理差分の偽装を確認する。

第四に、探索条件を分ける。

$$
(B,\Pi,\tau,\mathcal F_B)
$$

を記録し、探索したのか、資源切れなのか、port閉鎖なのかを区別する。

第五に、

$$
D=\varnothing
$$

と

$$
D=\bot
$$

を絶対に混同しない。

第六に、

$$
R=\operatorname{Ingress}\land \operatorname{Traceback}\land \operatorname{Reopen}
$$

を確認する。社会制度の場合は、必要に応じてActuate残差を別記する。

第七に、個性差を確認する。自分の探索軸で見えないことを、対象に存在しないことへ変換していないかを見る。

第八に、CutとUnsupported Joinを監査する。つながるべきものが切れていないか、つながってはいけないものをつないでいないかを見る。

第九に、Epistemic ClosureとAction Closureを分ける。命題を確定できないことと、行為を止められないことを同一視しない。

第十に、行為へ移る場合は、Correctnessとは別にAuthority、Boundary、Burden、Safety等の条件が必要かを確認する。

第十一に、返路が元主体へ戻れない場合、Proxy / Successor Returnの必要性を検討する。

第十二に、残差を単一スコアへ圧縮せず、

$$
\mathbf Q=(Q_1,Q_2,\ldots,Q_n)
$$

として保持する。

第十三に、停止理由を記録する。監査終了は探索飽和とは限らない。

第十四に、再開条件を置く。どの新しい事実・反例・被害・異議が来たら監査を再開するかを明示する。

---

## A.10　本監査の最終判定

三論点統合論考は、『正しさ・個性・無・切断』と強い構造的連続性を持つ。

特に、圧縮モデルと対象の非同一性、Cut、Return、Traceback、Reopen、provenance、個性によるfrontier差、偽閉鎖の危険という点で、統合論考は正本の応用面として読める。

一方で、本監査は、三論点へ正本を適用した結果として、少なくとも四つの大きな未処理領域を残差として記録した。

第一に、

$$
\operatorname{Correctness}
\neq
ActionAuthorization
$$

である。

第二に、

$$
\operatorname{ActionClosure}
\neq
ClaimClosure
$$

である。

第三に、

$$
\operatorname{Return}
$$

が社会実装ではActuateを必要とする可能性がある。

第四に、元主体が消滅した場合のProxy / Successor Returnである。

本付録では、これらを正本へ統合せず、残差として保持する。現行正本における採否は、current definition owner側の明示的記述に従う。

いずれも定義変更の影響範囲が大きく、正本の「正しい」の工学的定義を越えて、判断・介入・制度・継承の理論へ進むためである。

したがって、本付録では以下の状態で保持する。

$$
\operatorname{Status}(Q_1,Q_2,Q_3,Q_6)
=
\text{Open / high-priority residual}
$$

統合論考そのものについては、

$$
I(T)\approx \text{strong}
$$

$$
R(T)\approx \text{strong}
$$

である一方、

$$
D_T=\bot
$$

であり、探索飽和には達していない。

最終判定は、

> **強い暫定研究状態。正しさ認定ではない。**

である。

この判定は、論考を弱めるものではない。

むしろ、その論考が自分を壊し得る経路をまだ保持していることを確認する。

---

## A.11　監査記録の最終圧縮

本監査で得られた構造を最小形へ圧縮する。

### 圧縮1

$$
\operatorname{Model} \neq \text{World}
$$

扱うためのモデルは、対象そのものではない。

### 圧縮2

$$
D=\bot \neq D=\varnothing
$$

未判定と、探索後にdefeaterが見つからなかった状態を混同しない。

### 圧縮3

$$
\operatorname{Close}_{\mathrm{action}}=1
\not\Rightarrow
\operatorname{Close}_{\mathrm{claim}}=1
$$

行為を止めても、命題まで閉じる必要はない。

### 圧縮4

$$
\operatorname{Correctness}
\not\Rightarrow
\operatorname{Authorization}
$$

正しく知っていても、介入権限が生じるとは限らない。

### 圧縮5

$$
\operatorname{Ingress}+\operatorname{Traceback}+\operatorname{Reopen}
\stackrel{\mathrm{social}}{\not\Rightarrow}
\operatorname{Change}
$$

社会実装では、判断変更を作用へ戻す権限経路が別に必要かもしれない。

### 圧縮6

$$
\operatorname{Provenance}
\neq
\operatorname{Validity}
$$

履歴は正しさの証明ではなく、再検査面である。

### 圧縮7

$$
\operatorname{Return}
\not\equiv
\text{Return to Origin}
$$

元主体が消滅した場合、再判断可能な後続主体への接続が必要になる場合がある。

### 圧縮8

$$
\operatorname{StructuralSimilarity}
\neq
\operatorname{OntologicalIdentity}
$$

異なる領域で同じ記号が使えることは、同じ存在論を持つことの証明ではない。

### 最終残差

正本は、「有限な系が、現在どこまで正しいとして閉じてよいか」を扱う。

三論点は、その次の境界を露出した。

> **正しさを得た主体が、どこまで世界へ介入してよいのか。**

この問いは、正本の外部ではあるが、正本から自然に発生した。

したがって、本監査では、この残差を削除せず、次層へ送る。

$$
\boxed{
\operatorname{Correctness}
\;\longrightarrow\;
\operatorname{ActionBoundary}
\;\longrightarrow\;
\operatorname{Unresolved}
}
$$

ここが、現時点の返路である。


---

[ディレクトリの案内](README.md)・[監査対象の論考](自動運転された正しさを止めるために.ja.md)・[英語通約](Appendix_A_Audit_Record_Cross_Collation_and_Residual_Accumulation.en.md)

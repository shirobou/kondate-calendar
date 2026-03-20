"""
労働基準法の構造化HTML修正スクリプト
- 不完全・低品質なエントリを修正
- law-article ラッパー除去
- <ul>/<li> による箇条書き化
- <span class="logic"> による論理演算子の独立
"""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('structured_労働基準法.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 修正が必要なエントリの新しいstructuredを定義
fixes = {}

# ── 法9条：労働者の定義 ──
fixes["法9条"] = '''<div class="law-body"><div class="principle-section"><div class="subject-line">労働基準法で「<span class="subject">労働者</span>」とは、</div><ul class="condition-list"><li>職業の種類を問わず、</li><li>事業<span class="logic">又は</span>事務所（以下「事業」という。）に使用される者で、</li></ul><div class="predicate-line"><span class="predicate">賃金を支払われる者をいう。</span></div></div></div>'''

# ── 法17条：前借金相殺の禁止 ──
fixes["法17条"] = '''<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">使用者</span>は、</div><ul class="condition-list"><li>前借金その他労働することを条件とする前貸の債権と</li><li>賃金を</li></ul><div class="predicate-line"><span class="predicate">相殺してはならない。</span></div></div></div>'''

# ── 法13条：労働基準法違反の労働契約 ──
fixes["法13条"] = '''<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">労働基準法で定める基準に達しない労働条件を定める労働契約</span>は、</div><div class="predicate-line">その部分については<span class="predicate">無効とする。</span></div></div><div class="principle-section"><div class="subject-line">この場合において、<span class="subject">無効となった部分</span>は、</div><div class="predicate-line"><span class="predicate">労働基準法で定める基準による。</span></div></div></div>'''

# ── 法15条 2項3項：労働条件の明示と即時解除 ──
fixes["法15条"] = '''<div class="law-body"><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line">明示された労働条件が<span class="condition">事実と相違する場合</span>においては、</div><ul class="condition-list"><li><span class="subject">労働者</span>は、</li></ul><div class="predicate-line">即時に労働契約を<span class="predicate">解除することができる。</span></div></div><div class="principle-section"><span class="item-number">第3項</span><div class="subject-line">就業のために住居を変更した<span class="subject">労働者</span>が、</div><ul class="condition-list"><li>契約解除の日から<span class="period">14日以内</span>に帰郷する<span class="condition">場合</span>においては、</li></ul><div class="predicate-line"><span class="subject">使用者</span>は、必要な旅費を<span class="predicate">負担しなければならない。</span></div></div></div>'''

# ── 法20条：解雇予告 ──
fixes["法20条"] = '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">使用者</span>は、</div><ul class="condition-list"><li><span class="subject">労働者</span>を解雇しようとする<span class="condition">場合</span>においては、</li></ul><div class="predicate-line">少なくとも<span class="period">30日前</span>にその予告を<span class="predicate">しなければならない。</span></div></div><div class="principle-section"><div class="subject-line"><span class="period">30日前</span>に予告をしない<span class="subject">使用者</span>は、</div><div class="predicate-line"><span class="period">30日分以上</span>の<span class="period">平均賃金</span>を<span class="predicate">支払わなければならない。</span></div></div></div>'''

# ── 法22条：退職時の証明・解雇理由証明書 ──
fixes["法22条"] = '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">労働者</span>が、退職の場合において、</div><ul class="condition-list"><li>使用期間、</li><li>業務の種類、</li><li>その事業における地位、</li><li>賃金<span class="logic">又は</span>退職の事由<br>（退職の事由が解雇の場合にあっては、その理由を含む。）</li></ul><div class="subject-line">について証明書を請求した<span class="condition">場合</span>においては、</div><div class="predicate-line"><span class="subject">使用者</span>は、<span class="predicate">遅滞なくこれを交付しなければならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">労働者</span>が、<span class="period">解雇の予告がされた日</span>から退職の日までの間において、</div><ul class="condition-list"><li>当該解雇の理由について証明書を請求した<span class="condition">場合</span>においては、</li></ul><div class="predicate-line"><span class="subject">使用者</span>は、<span class="predicate">遅滞なくこれを交付しなければならない。</span></div></div><div class="exception-section"><div class="exception-keyword"><span class="exception">ただし、</span></div><ul class="condition-list"><li>解雇の予告がされた日以後に<span class="subject">労働者</span>が当該解雇以外の事由により退職した<span class="condition">場合</span>においては、</li></ul><div class="predicate-line"><span class="subject">使用者</span>は、当該退職の日以後、これを<span class="exception">交付することを要しない。</span></div></div><div class="principle-section"><span class="item-number">第3項</span><div class="subject-line">前2項の<span class="subject">証明書</span>には、</div><div class="predicate-line"><span class="subject">労働者</span>の請求しない事項を<span class="predicate">記入してはならない。</span></div></div></div>'''

# ── 法24条：賃金支払の5原則 ──
fixes["法24条"] = '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">賃金</span>は、</div><ul class="condition-list"><li><span class="period">通貨</span>で、</li><li><span class="period">直接</span>労働者に、</li><li>その<span class="period">全額</span>を</li></ul><div class="predicate-line"><span class="predicate">支払わなければならない。</span></div></div></div>'''

# ── 令：賃金支払の原則（法24条の続き） ──
fixes["令"] = '''<div class="law-body"><div class="exception-section"><div class="exception-keyword"><span class="exception">ただし、</span></div><ul class="condition-list"><li><span class="logic">若しくは</span><span class="period">労働協約</span>に別段の定めがある場合</li><li class="logic-item"><span class="logic">又は</span></li><li>厚生労働省令で定める賃金について確実な支払の方法で厚生労働省令で定めるものによる場合</li></ul><div class="predicate-line">→ <span class="period">通貨以外のもの</span>で<span class="exception">支払うことができる。</span></div></div><div class="exception-section"><ul class="condition-list"><li><span class="period">法令</span>に別段の定めがある場合</li><li class="logic-item"><span class="logic">又は</span></li><li><span class="period">労使協定</span>がある場合</li></ul><div class="predicate-line">→ 賃金の<span class="period">一部を控除</span>して<span class="exception">支払うことができる。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">賃金</span>は、</div><ul class="condition-list"><li><span class="period">毎月1回以上</span>、</li><li><span class="period">一定の期日</span>を定めて</li></ul><div class="predicate-line"><span class="predicate">支払わなければならない。</span></div></div><div class="exception-section"><div class="exception-keyword"><span class="exception">ただし、</span></div><ul class="condition-list"><li>臨時に支払われる賃金、</li><li><span class="period">賞与</span>その他これに準ずるもので厚生労働省令で定める賃金</li></ul><div class="predicate-line">については、<span class="exception">この限りでない。</span></div></div></div>'''

# ── 法25条：非常時払 ──
fixes["法25条"] = '''<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">使用者</span>は、</div><ul class="condition-list"><li><span class="subject">労働者</span>が出産、疾病、災害その他厚生労働省令で定める非常の場合の費用に充てるために<span class="condition">請求する場合</span>においては、</li><li><span class="period">支払期日前</span>であっても、</li></ul><div class="predicate-line">既往の労働に対する賃金を<span class="predicate">支払わなければならない。</span></div></div></div>'''

# ── 法26条：休業手当 ──
fixes["法26条"] = '''<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="condition">使用者の責に帰すべき事由による休業の場合</span>においては、</div><ul class="condition-list"><li><span class="subject">使用者</span>は、</li><li>休業期間中当該<span class="subject">労働者</span>に、</li></ul><div class="predicate-line">その<span class="period">平均賃金の100分の60以上</span>の手当を<span class="predicate">支払わなければならない。</span></div></div></div>'''

# ── 法27条：出来高払制の保障給 ──
fixes["法27条"] = '''<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">出来高払制その他の請負制</span>で使用する<span class="subject">労働者</span>については、</div><ul class="condition-list"><li><span class="subject">使用者</span>は、</li></ul><div class="predicate-line"><span class="period">労働時間</span>に応じ一定額の賃金の保障を<span class="predicate">しなければならない。</span></div></div></div>'''

# ── 法32条：法定労働時間 ──
fixes["法32条"] = '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">使用者</span>は、</div><ul class="condition-list"><li><span class="subject">労働者</span>に、</li><li>休憩時間を除き<span class="period">1週間について40時間</span>を超えて、</li></ul><div class="predicate-line"><span class="predicate">労働させてはならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">使用者</span>は、</div><ul class="condition-list"><li><span class="period">1週間の各日</span>については、<span class="subject">労働者</span>に、</li><li>休憩時間を除き<span class="period">1日について8時間</span>を超えて、</li></ul><div class="predicate-line"><span class="predicate">労働させてはならない。</span></div></div></div>'''

# ── 法12条1項：平均賃金の最低保障 ──
fixes["法12条1項"] = '''<div class="law-body"><div class="exception-section"><div class="exception-keyword"><span class="exception">ただし、</span><span class="subject">平均賃金の金額</span>は、次の各号によって計算した金額を下ってはならない。</div><ul class="condition-list"><li>ア. 賃金が、労働した日<span class="logic">若しくは</span>時間によって算定され、<span class="logic">又は</span>出来高払制その他の請負制によって定められた<span class="condition">場合</span><br>→ <span class="period">賃金の総額</span>をその期間中に<span class="period">労働した日数</span>で除した金額の<span class="period">100分の60</span></li><li>イ. 賃金の一部が、月、週その他一定の期間によって定められた<span class="condition">場合</span><br>→ その部分の総額をその期間の<span class="period">総日数</span>で除した金額と<br>　 ア.の金額の<span class="period">合算額</span></li></ul></div></div>'''

# ── 法66条：妊産婦の変形労働時間制の適用制限 ──
fixes["法66条"] = '''<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">使用者</span>は、</div><ul class="condition-list"><li><span class="subject">妊産婦</span>が<span class="condition">請求した場合</span>においては、</li><li>1箇月単位の変形労働時間制、</li><li>1年単位の変形労働時間制<span class="logic">及び</span></li><li>1週間単位の非定型的変形労働時間制</li></ul><div class="predicate-line">の規定にかかわらず、<span class="period">1週間</span>について法定労働時間、<span class="period">1日</span>について<span class="period">8時間</span>を超えて労働<span class="predicate">させてはならない。</span></div></div></div>'''

# ── 法83条：補償を受ける権利 ──
fixes["法83条"] = '''<div class="law-body"><div class="principle-section"><div class="subject-line">補償を受ける<span class="subject">権利</span>は、</div><div class="predicate-line"><span class="subject">労働者</span>の退職によって変更<span class="predicate">されることはない。</span></div></div></div>'''

# ── 法112条：国・公共団体への適用 ──
fixes["法112条"] = '''<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">労働基準法<span class="logic">及び</span>労働基準法に基づいて発する命令</span>は、</div><ul class="condition-list"><li>国、</li><li>都道府県、</li><li>市町村その他これに準ずべきものについても</li></ul><div class="predicate-line"><span class="predicate">適用あるものとする。</span></div></div></div>'''

# ── 則25条の2：法定労働時間の特例 ──
fixes["則25条の2"] = '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">使用者</span>は、</div><ul class="condition-list"><li>法別表第1第8号（<span class="period">商業</span>）、</li><li>第10号（<span class="period">映画・演劇業</span>（映画の製作の事業を除く。））、</li><li>第13号（<span class="period">保健衛生業</span>）<span class="logic">及び</span></li><li>第14号（<span class="period">接客娯楽業</span>）</li></ul><div class="subject-line">に掲げる事業のうち<span class="period">常時10人未満</span>の労働者を使用するものについては、</div><div class="predicate-line">法第32条の規定にかかわらず、<span class="period">1週間について44時間</span>、<span class="period">1日について8時間</span>まで<span class="predicate">労働させることができる。</span></div></div></div>'''

# ── 法41条の2：高度プロフェッショナル制度 ──
fixes["法41条の2"] = '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">労使委員会</span>が設置された事業場において、</div><ul class="condition-list"><li>当該委員会がその委員の<span class="period">5分の4以上</span>の多数による議決により所定事項に関する決議をし、</li><li class="logic-item"><span class="logic">かつ</span></li><li><span class="subject">使用者</span>が当該決議を<span class="subject">行政官庁</span>（所轄労働基準監督署長）に届け出た<span class="condition">場合</span>において、</li><li><span class="subject">対象労働者</span>であって書面によりその同意を得たものを<br>当該事業場における対象業務に就かせたときは、</li></ul><div class="predicate-line">労働時間、休憩、休日<span class="logic">及び</span>深夜の割増賃金に関する規定は、<span class="predicate">適用しない。</span></div></div></div>'''

# ── 法37条：割増賃金 ──
fixes["法37条"] = '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項 本文</span><div class="subject-line"><span class="subject">使用者</span>が、</div><ul class="condition-list"><li>第33条<span class="logic">又は</span>第36条第1項の規定により労働時間を延長し、<span class="logic">又は</span>休日に労働させた<span class="condition">場合</span>においては、</li></ul><div class="predicate-line">通常の労働時間<span class="logic">又は</span>労働日の賃金の計算額の<br><span class="period">2割5分以上5割以下</span>の率で計算した<span class="period">割増賃金</span>を<span class="predicate">支払わなければならない。</span></div></div><div class="exception-section"><div class="exception-keyword"><span class="exception">ただし、</span></div><ul class="condition-list"><li>延長して労働させた時間が<span class="period">1箇月について60時間を超えた場合</span>においては、</li></ul><div class="predicate-line">その超えた時間の労働については、<br><span class="period">5割以上</span>の率で計算した割増賃金を<span class="predicate">支払わなければならない。</span></div></div><div class="principle-section"><span class="item-number">第4項</span><div class="subject-line"><span class="subject">使用者</span>が、</div><ul class="condition-list"><li><span class="period">午後10時</span>から<span class="period">午前5時</span>までの間において労働させた<span class="condition">場合</span>においては、</li></ul><div class="predicate-line"><span class="period">2割5分以上</span>の率で計算した割増賃金を<span class="predicate">支払わなければならない。</span></div></div></div>'''

# ── 法106条：法令等の周知 ──
fixes["法106条"] = '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">使用者</span>は、</div><ul class="condition-list"><li>労働基準法<span class="logic">及び</span>労働基準法に基づく命令の要旨、</li><li>就業規則、</li><li>労使協定、</li><li>労使委員会の決議</li></ul><div class="predicate-line">を、常時各作業場の見やすい場所へ掲示し、<span class="logic">又は</span>備え付けること、<br>書面を交付することその他の方法によって、<br><span class="subject">労働者</span>に<span class="predicate">周知させなければならない。</span></div></div></div>'''

# ── 法107条：労働者名簿 ──
fixes["法107条"] = '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">使用者</span>は、</div><ul class="condition-list"><li>各事業場ごとに<span class="period">労働者名簿</span>を、</li><li>各<span class="subject">労働者</span>（日日雇い入れられる者を除く。）について調製し、</li><li>氏名、生年月日、履歴その他厚生労働省令で定める事項を</li></ul><div class="predicate-line"><span class="predicate">記入しなければならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="condition">記入すべき事項に変更があった場合</span>においては、</div><div class="predicate-line"><span class="predicate">遅滞なく訂正しなければならない。</span></div></div></div>'''

# ── 法108条：賃金台帳 ──
fixes["法108条"] = '''<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">使用者</span>は、</div><ul class="condition-list"><li>各事業場ごとに<span class="period">賃金台帳</span>を調製し、</li><li>賃金計算の基礎となる事項<span class="logic">及び</span>賃金の額その他厚生労働省令で定める事項を</li></ul><div class="predicate-line">賃金支払の都度遅滞なく<span class="predicate">記入しなければならない。</span></div></div></div>'''

# ── 法109条：記録の保存 ──
fixes["法109条"] = '''<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">使用者</span>は、</div><ul class="condition-list"><li>労働者名簿、</li><li>賃金台帳<span class="logic">及び</span></li><li>雇入れ、解雇、災害補償、賃金その他労働関係に関する重要な書類を</li></ul><div class="predicate-line"><span class="period">5年間</span>（当分の間、<span class="period">3年間</span>）<span class="predicate">保存しなければならない。</span></div></div></div>'''

# ── 法101条：労働基準監督官の権限 ──
fixes["法101条"] = '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">労働基準監督官</span>は、</div><ul class="condition-list"><li>事業場、寄宿舎その他の附属建設物に<span class="predicate">臨検</span>し、</li><li>帳簿<span class="logic">及び</span>書類の提出を求め、</li><li class="logic-item"><span class="logic">又は</span></li><li><span class="subject">使用者</span><span class="logic">若しくは</span><span class="subject">労働者</span>に対して<span class="predicate">尋問を行うことができる。</span></li></ul></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">労働基準監督官</span>は、</div><div class="predicate-line">その身分を証明する証票を<span class="predicate">携帯しなければならない。</span></div></div></div>'''

# ── 法96条の2：寄宿舎の届出 ──
fixes["法96条の2"] = '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">使用者</span>は、</div><ul class="condition-list"><li><span class="period">常時10人以上</span>の労働者を就業させる事業、</li><li>厚生労働省令で定める危険な事業<span class="logic">又は</span>衛生上有害な事業</li></ul><div class="subject-line">の附属寄宿舎を設置し、移転し、<span class="logic">又は</span>変更しようとする<span class="condition">場合</span>においては、</div><div class="predicate-line">厚生労働省令で定める危害防止等に関する基準に従い定めた計画を、<br>工事着手<span class="period">14日前</span>までに、<span class="subject">行政官庁</span>に<span class="predicate">届け出なければならない。</span></div></div></div>'''

# ── 法84条：他の法律との関係 ──
fixes["法84条"] = '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><ul class="condition-list"><li>労働基準法に規定する災害補償の事由について、</li><li>労災保険法<span class="logic">又は</span>厚生労働省令で指定する法令に基づいて</li><li>労働基準法の災害補償に相当する給付が行われるべきものである<span class="condition">場合</span>においては、</li></ul><div class="predicate-line"><span class="subject">使用者</span>は、補償の責を<span class="predicate">免れる。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><ul class="condition-list"><li><span class="subject">使用者</span>が労働基準法による補償を行った<span class="condition">場合</span>においては、</li></ul><div class="predicate-line">同一の事由については、その価額の限度において<br>民法による損害賠償の責を<span class="predicate">免れる。</span></div></div></div>'''

# ── 法114条：付加金 ──
fixes["法114条"] = '''<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">裁判所</span>は、</div><ul class="condition-list"><li>第20条（解雇予告手当）、</li><li>第26条（休業手当）<span class="logic">若しくは</span></li><li>第37条（割増賃金）の規定に違反した<span class="subject">使用者</span></li><li class="logic-item"><span class="logic">又は</span></li><li>第39条第9項（年次有給休暇中の賃金）の規定による賃金を支払わなかった<span class="subject">使用者</span>に対して、</li></ul><div class="predicate-line"><span class="subject">労働者</span>の請求により、<br>未払金のほか、これと同一額の<span class="period">付加金</span>の支払を<span class="predicate">命ずることができる。</span></div></div></div>'''

# 適用
fixed_count = 0
for item in data:
    ref = item['reference']
    if ref in fixes:
        item['structured'] = fixes[ref]
        fixed_count += 1
        print(f"  ✔ {ref} を修正しました")

print(f"\n合計 {fixed_count}/{len(fixes)} 件を修正")

# 未適用の修正を確認
refs_in_data = {item['reference'] for item in data}
for ref in fixes:
    if ref not in refs_in_data:
        print(f"  ⚠ {ref} はデータに存在しません")

# 保存
with open('structured_労働基準法.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\nstructured_労働基準法.json を上書き保存しました")

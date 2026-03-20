"""
労働安全衛生法 構造化 Batch 3 (articles 60-89)
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('structured_労働安全衛生法.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

ref_map = {item['reference']: i for i, item in enumerate(data)}

def update(ref, html):
    if ref in ref_map:
        data[ref_map[ref]]['structured'] = html
        print(f"  Updated: {ref}")
    else:
        print(f"  WARNING: {ref} not found!")

# 60. 法57条の3 - リスクアセスメント
update("法57条の3", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><div class="predicate-line">表示対象物<span class="logic">及び</span>通知対象物による危険性<span class="logic">又は</span>有害性等を<span class="predicate">調査しなければならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><div class="predicate-line">前項の調査の結果に基づいて、労働安全衛生法<span class="logic">又は</span>これに基づく命令の規定による措置を講ずるほか、<br>労働者の危険<span class="logic">又は</span>健康障害を防止するため必要な措置を講ずるように<span class="predicate">努めなければならない。</span></div></div><div class="principle-section"><span class="item-number">第3項</span><div class="subject-line"><span class="subject">厚生労働大臣</span>は、</div><div class="predicate-line">前2項の措置に関して、その適切<span class="logic">かつ</span>有効な実施を図るため必要な指針を<span class="predicate">公表するものとする。</span></div></div><div class="principle-section"><span class="item-number">第4項</span><div class="subject-line"><span class="subject">厚生労働大臣</span>は、</div><div class="predicate-line">前項の指針に従い、事業者<span class="logic">又は</span>その団体に対し、必要な指導、援助等を<span class="predicate">行うことができる。</span></div></div></div>')

# 61. 法57条の4 - 新規化学物質の届出
update("法57条の4", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">新規化学物質を製造し、<span class="logic">又は</span>輸入しようとする事業者</span>は、</div><ul class="condition-list"><li>あらかじめ、厚生労働大臣の定める基準に従って有害性の調査を行い、</li><li>当該新規化学物質の名称、有害性の調査の結果その他の事項を</li></ul><div class="predicate-line"><span class="subject">厚生労働大臣</span>に<span class="predicate">届け出なければならない。</span></div></div><div class="principle-section"><span class="item-number">第3項</span><div class="subject-line"><span class="subject">厚生労働大臣</span>は、</div><ul class="condition-list"><li><span class="condition">第1項の規定による届出があった場合</span>には、</li></ul><div class="predicate-line">当該新規化学物質の名称を<span class="predicate">公表するものとする。</span></div></div><div class="principle-section"><span class="item-number">第4項</span><div class="subject-line"><span class="subject">厚生労働大臣</span>は、</div><ul class="condition-list"><li><span class="condition">第1項の規定による届出があった場合</span>には、</li><li>有害性の調査の結果について学識経験者の意見を聴き、</li><li>当該届出に係る化学物質による労働者の健康障害を防止するため必要があると<span class="condition">認めるとき</span>は、</li></ul><div class="predicate-line">届出をした事業者に対し、施設<span class="logic">又は</span>設備の設置<span class="logic">又は</span>整備、保護具の備付けその他の措置を講ずべきことを<span class="predicate">勧告することができる。</span></div></div></div>')

# 62. 法57条の4第1項 - (empty, skip or minimal)
update("法57条の4第1項", '<div class="law-body"><div class="principle-section"><div class="predicate-line">（法57条の4第1項の詳細規定 — 上位条文を参照）</div></div></div>')

# 63. 法57条の5 - 有害性の調査指示
update("法57条の5", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">厚生労働大臣</span>は、</div><ul class="condition-list"><li>化学物質で、がんその他の重度の健康障害を労働者に生ずるおそれのあるものについて、</li><li>当該化学物質による労働者の健康障害を防止するため必要があると<span class="condition">認めるとき</span>は、</li></ul><div class="predicate-line">当該化学物質を製造し、輸入し、<span class="logic">又は</span>使用している事業者その他厚生労働省令で定める事業者に対し、<br>政令で定める有害性の調査を行い、その結果を報告すべきことを<span class="predicate">指示することができる。</span></div></div><div class="principle-section"><span class="item-number">第3項</span><div class="subject-line"><span class="subject">厚生労働大臣</span>は、</div><ul class="condition-list"><li><span class="condition">第1項の規定による指示を行おうとするとき</span>は、</li></ul><div class="predicate-line">あらかじめ、学識経験者の意見を<span class="predicate">聴かなければならない。</span></div></div><div class="principle-section"><span class="item-number">第4項</span><div class="subject-line"><span class="subject">第1項の規定による有害性の調査を行った事業者</span>は、</div><div class="predicate-line">その結果に基づいて、当該化学物質による労働者の健康障害を防止するため<br>必要な措置を速やかに<span class="predicate">講じなければならない。</span></div></div></div>')

# 64. 法61条 - 就業制限
update("法61条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>クレーンの運転その他の業務で、政令で定めるものについては、</li><li>都道府県労働局長の当該業務に係る免許を受けた者<span class="logic">又は</span>登録教習機関が行う当該業務に係る技能講習を修了した者<br>その他厚生労働省令で定める資格を有する者でなければ、</li></ul><div class="predicate-line">当該業務に<span class="predicate">就かせてはならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="predicate-line">前項の規定により当該業務につくことができる者以外の者は、当該業務を<span class="predicate">行なってはならない。</span></div></div><div class="principle-section"><span class="item-number">第3項</span><div class="subject-line">第1項の規定により当該業務につくことができる者は、</div><ul class="condition-list"><li><span class="condition">当該業務に従事するとき</span>は、</li></ul><div class="predicate-line">これに係る免許証その他その資格を証する書面を<span class="predicate">携帯していなければならない。</span></div></div></div>')

# 65. 法75条 - 免許試験
update("法75条", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">免許試験</span>は、</div><div class="predicate-line">厚生労働省令で定める区分ごとに、<span class="subject">都道府県労働局長</span>が<span class="predicate">行う。</span></div></div></div>')

# 66. 法72条 - 免許
update("法72条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line">第12条第1項（衛生管理者）、第14条（作業主任者）<span class="logic">又は</span>第61条第1項（就業制限業務）の免許は、</div><div class="predicate-line">第75条第1項の免許試験に合格した者その他厚生労働省令で定める資格を有する者に対し、<br>免許証を交付して<span class="predicate">行う。</span></div></div></div>')

# 67. 法76条 - 技能講習
update("法76条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">技能講習</span>は、</div><div class="predicate-line">別表第18に掲げる区分ごとに、学科講習<span class="logic">又は</span>実技講習によって<span class="predicate">行う。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line">技能講習を行なった者（<span class="subject">登録教習機関</span>）は、</div><div class="predicate-line">当該技能講習を修了した者に対し、技能講習修了証を<span class="predicate">交付しなければならない。</span></div></div></div>')

# 68. 法62条 - 中高年齢者等の適正配置
update("法62条", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>中高年齢者その他労働災害の防止上その就業に当たって特に配慮を必要とする者については、</li></ul><div class="predicate-line">これらの者の心身の条件に応じて適正な配置を行うように<span class="predicate">努めなければならない。</span></div></div></div>')

# 69. 法62条の2 - 高年齢者の労災防止
update("法62条の2", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>高年齢者の労働災害の防止を図るため、</li><li>高年齢者の特性に配慮した作業環境の改善、作業の管理その他の必要な措置を講ずるように</li></ul><div class="predicate-line"><span class="predicate">努めなければならない。</span></div></div></div>')

# 70. 法59条 - 安全衛生教育（雇入れ時等）
update("法59条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li><span class="condition">労働者を雇い入れたとき</span>は、</li></ul><div class="predicate-line">当該労働者に対し、その従事する業務に関する安全<span class="logic">又は</span>衛生のための教育を<span class="predicate">行なわなければならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="predicate-line">前項の規定は、<span class="condition">労働者の作業内容を変更したとき</span>について<span class="predicate">準用する。</span></div></div></div>')

# 71. 法60条 - 職長教育
update("法60条", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>その事業場の業種が政令で定めるものに<span class="condition">該当するとき</span>は、</li><li>新たに職務につくこととなった職長その他の作業中の労働者を直接指導<span class="logic">又は</span>監督する者<br>（<span class="exception">作業主任者を除く。</span>）に対し、</li></ul><div class="predicate-line">次の事項について、安全<span class="logic">又は</span>衛生のための教育を<span class="predicate">行なわなければならない。</span></div><ul class="condition-list"><li>1. 作業方法の決定<span class="logic">及び</span>労働者の配置に関すること。</li><li>2. 労働者に対する指導<span class="logic">又は</span>監督の方法に関すること。</li><li>3. 1.<span class="logic">及び</span>2.に掲げるもののほか、労働災害を防止するため必要な事項で、厚生労働省令で定めるもの</li></ul></div></div>')

# 72. 法60条の2 - 危険有害業務従事者の教育
update("法60条の2", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>第59条<span class="logic">及び</span>第60条に定めるもののほか、</li><li>その事業場における安全衛生の水準の向上を図るため、</li><li>危険<span class="logic">又は</span>有害な業務に現に就いている者に対し、</li></ul><div class="predicate-line">その従事する業務に関する安全<span class="logic">又は</span>衛生のための教育を行うように<span class="predicate">努めなければならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">厚生労働大臣</span>は、</div><div class="predicate-line">前項の教育の適切<span class="logic">かつ</span>有効な実施を図るため必要な指針を<span class="predicate">公表するものとする。</span></div></div><div class="principle-section"><span class="item-number">第3項</span><div class="subject-line"><span class="subject">厚生労働大臣</span>は、</div><div class="predicate-line">前項の指針に従い、事業者<span class="logic">又は</span>その団体に対し、必要な指導等を<span class="predicate">行うことができる。</span></div></div></div>')

# 73. 法65条 - 作業環境測定
update("法65条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><div class="predicate-line">有害な業務を行う屋内作業場その他の作業場で、政令で定めるものについて、<br>必要な作業環境測定を行い、<span class="logic">及び</span>その結果を記録して<span class="predicate">おかなければならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="predicate-line">前項の規定による作業環境測定は、<span class="subject">厚生労働大臣</span>の定める作業環境測定基準に従って<span class="predicate">行わなければならない。</span></div></div><div class="principle-section"><span class="item-number">第3項</span><div class="subject-line"><span class="subject">厚生労働大臣</span>は、</div><div class="predicate-line">第1項の規定による作業環境測定の適切<span class="logic">かつ</span>有効な実施を図るため<br>必要な作業環境測定指針を<span class="predicate">公表するものとする。</span></div></div><div class="principle-section"><span class="item-number">第5項</span><div class="subject-line"><span class="subject">都道府県労働局長</span>は、</div><ul class="condition-list"><li>作業環境の改善により労働者の健康を保持する必要があると<span class="condition">認めるとき</span>は、</li></ul><div class="predicate-line">労働衛生指導医の意見に基づき、事業者に対し、<br>作業環境測定の実施その他必要な事項を<span class="predicate">指示することができる。</span></div></div></div>')

# 74. 法65条の2 - 作業環境測定の評価
update("法65条の2", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>作業環境測定の結果の評価に基づいて、</li><li>労働者の健康を保持するため必要があると<span class="condition">認められるとき</span>は、</li></ul><div class="predicate-line">施設<span class="logic">又は</span>設備の設置<span class="logic">又は</span>整備、健康診断の実施その他の適切な措置を<span class="predicate">講じなければならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><div class="predicate-line">前項の評価を行うに当たっては、<span class="subject">厚生労働大臣</span>の定める作業環境評価基準に従って<span class="predicate">行わなければならない。</span></div></div><div class="principle-section"><span class="item-number">第3項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>前項の規定による作業環境測定の結果の評価を<span class="condition">行ったとき</span>は、</li></ul><div class="predicate-line">その結果を記録して<span class="predicate">おかなければならない。</span></div></div></div>')

# 75. 法66条 - 健康診断
update("法66条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><div class="predicate-line">労働者に対し、医師による健康診断を<span class="predicate">行わなければならない。</span></div></div></div>')

# 76. 則43条 - 雇入時の健康診断
update("則43条", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li><span class="condition">常時使用する労働者を雇い入れるとき</span>は、</li></ul><div class="predicate-line">当該労働者に対し、所定の項目について医師による健康診断を<span class="predicate">行わなければならない。</span></div></div><div class="exception-section"><div class="exception-keyword"><span class="exception">ただし、</span></div><ul class="condition-list"><li>医師による健康診断を受けた後、<span class="period">3月</span>を経過しない者を雇い入れる場合において、</li><li>その者が当該健康診断の結果を証明する書面を提出したときは、</li></ul><div class="predicate-line">当該健康診断の項目に相当する項目については、<span class="exception">この限りでない。</span></div></div></div>')

# 77. 則44条 - 定期健康診断
update("則44条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>常時使用する労働者（<span class="exception">特定業務従事者を除く。</span>）に対し、</li><li><span class="period">1年以内ごとに1回</span>、定期に、</li></ul><div class="predicate-line">所定の項目について医師による健康診断を<span class="predicate">行わなければならない。</span></div></div></div>')

# 78. 則45条 - 特定業務従事者の健康診断
update("則45条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>特定業務に常時従事する労働者に対し、</li><li>当該業務への配置替えの際<span class="logic">及び</span><span class="period">6月以内ごとに1回</span>、定期に、</li></ul><div class="predicate-line">定期健康診断の検査項目について医師による健康診断を<span class="predicate">行わなければならない。</span></div><div class="predicate-line">この場合において、胸部エックス線検査<span class="logic">及び</span>喀痰検査については、<br><span class="period">1年以内ごとに1回</span>、定期に、行えば<span class="predicate">足りるものとする。</span></div></div></div>')

# 79. 則45条の2 - 海外派遣労働者の健康診断
update("則45条の2", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>労働者を本邦外の地域に<span class="period">6月以上</span>派遣しようとするときは、</li></ul><div class="predicate-line">あらかじめ、当該労働者に対し、定期健康診断の検査項目<span class="logic">及び</span>厚生労働大臣が定める項目のうち<br>医師が必要であると認める項目について、医師による健康診断を<span class="predicate">行わなければならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>本邦外の地域に<span class="period">6月以上</span>派遣した労働者を本邦の地域内における業務に就かせるとき<br>（一時的に就かせるときを除く。）は、</li></ul><div class="predicate-line">当該労働者に対し、所定の項目について、医師による健康診断を<span class="predicate">行わなければならない。</span></div></div></div>')

# 80. 則47条 - 給食従事者の検便
update("則47条", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>事業に附属する食堂<span class="logic">又は</span>炊事場における給食の業務に従事する労働者に対し、</li><li>その雇入れの際<span class="logic">又は</span>当該業務への配置替えの際、</li></ul><div class="predicate-line">検便による健康診断を<span class="predicate">行なわなければならない。</span></div></div></div>')

# 81. 法66条の2 - 自発的健康診断
update("法66条の2", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">深夜業に従事する労働者であって、その深夜業の回数その他の事項が厚生労働省令で定める要件に該当するもの</span>は、</div><div class="predicate-line">自ら受けた健康診断の結果を証明する書面を事業者に<span class="predicate">提出することができる。</span></div></div></div>')

# 82. 則51条 - 健康診断個人票の保存
update("則51条", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">事業者</span>は、</div><div class="predicate-line">安全衛生法の規定による健康診断の結果に基づき、<br>健康診断個人票を作成して、これを<span class="period">5年間</span><span class="predicate">保存しなければならない。</span></div></div></div>')

# 83. 則52条 - 健康診断結果の報告
update("則52条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="period">常時50人以上</span>の労働者を使用する<span class="subject">事業者</span>は、</div><ul class="condition-list"><li>健康診断（定期健康診断<span class="logic">又は</span>特定業務従事者の健康診断であって定期のものに限る。）を行ったときは、</li></ul><div class="predicate-line">遅滞なく、所定の事項を所轄労働基準監督署長に<span class="predicate">報告しなければならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>歯科医師による健康診断（定期のものに限る。）を行ったときは、</li></ul><div class="predicate-line">遅滞なく、所定の事項を所轄労働基準監督署長に<span class="predicate">報告しなければならない。</span></div></div></div>')

# 84. 法66条の4 - 医師等の意見聴取
update("法66条の4", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>労働安全衛生法の規定による健康診断の結果<br>（当該健康診断の項目に異常の所見があると診断された労働者に係るものに限る。）に基づき、</li></ul><div class="predicate-line">当該労働者の健康を保持するために必要な措置について、<br>医師<span class="logic">又は</span>歯科医師の意見を<span class="predicate">聴かなければならない。</span></div></div></div>')

# 85. 法66条の5 - 健康診断実施後の措置
update("法66条の5", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>前条の規定による医師<span class="logic">又は</span>歯科医師の意見を勘案し、</li><li><span class="condition">その必要があると認めるとき</span>は、</li></ul><div class="predicate-line">当該労働者の実情を考慮して、就業場所の変更、作業の転換、労働時間の短縮、深夜業の回数の減少等の措置を講ずるほか、<br>作業環境測定の実施、施設<span class="logic">又は</span>設備の設置<span class="logic">又は</span>整備、<br>当該医師<span class="logic">又は</span>歯科医師の意見の衛生委員会<span class="logic">若しくは</span>安全衛生委員会<span class="logic">又は</span>労働時間等設定改善委員会への報告<br>その他の適切な措置を<span class="predicate">講じなければならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">厚生労働大臣</span>は、</div><div class="predicate-line">前項の規定により事業者が講ずべき措置の適切<span class="logic">かつ</span>有効な実施を図るため<br>必要な指針を<span class="predicate">公表するものとする。</span></div></div></div>')

# 86. 法66条の6 - 健康診断結果の通知
update("法66条の6", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>一般健康診断、特殊健康診断、歯科医師による健康診断<span class="logic">及び</span>臨時健康診断を受けた労働者に対し、</li></ul><div class="predicate-line">遅滞なく、当該健康診断の結果を<span class="predicate">通知しなければならない。</span></div></div></div>')

# 87. 法66条の7 - 保健指導
update("法66条の7", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>一般健康診断<span class="logic">若しくは</span>当該健康診断に係る労働者指定医師による健康診断<span class="logic">又は</span>自発的健康診断の結果、</li><li>特に健康の保持に努める必要があると認める労働者に対し、</li></ul><div class="predicate-line">医師<span class="logic">又は</span>保健師による保健指導を行うように<span class="predicate">努めなければならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">労働者</span>は、</div><div class="predicate-line">前条の規定により通知された健康診断の結果<span class="logic">及び</span>前項の規定による保健指導を利用して、<br>その健康の保持に<span class="predicate">努めるものとする。</span></div></div></div>')

# 88. 法66条の8 - 面接指導
update("法66条の8", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>その労働時間の状況その他の事項が労働者の健康の保持を考慮して<br>厚生労働省令で定める要件に該当する労働者に対し、</li></ul><div class="predicate-line">医師による<span class="subject">面接指導</span>（問診その他の方法により心身の状況を把握し、<br>これに応じて面接により必要な指導を行うことをいう。）を<span class="predicate">行わなければならない。</span></div></div></div>')

# 89. 法66条の8の2 - 研究開発業務従事者の面接指導
update("法66条の8の2", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>その労働時間が労働者の健康の保持を考慮して厚生労働省令で定める時間を超える労働者</li><li>（労働基準法第36条第11項に規定する業務（新たな技術、商品<span class="logic">又は</span>役務の研究開発に係る業務）に従事する者に<span class="period">限る。</span>）に対し、</li></ul><div class="predicate-line">医師による面接指導を<span class="predicate">行わなければならない。</span></div></div></div>')

print(f"\nBatch 3 done. Total items: {len(data)}")

with open('structured_労働安全衛生法.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Saved.")

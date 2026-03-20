"""
労働安全衛生法 構造化 Batch 4 (articles 90-128)
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

# 90. 則52条の7の2 - 面接指導の時間要件
update("則52条の7の2", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line">法66条の8の2第1項の厚生労働省令で定める時間は、</div><div class="predicate-line">休憩時間を除き1週間当たり<span class="period">40時間</span>を超えて労働させた場合におけるその超えた時間について、<br>1月当たり<span class="period">100時間</span>とする。</div></div></div>')

# 91. 法66条の8の4 - 高プロ対象者の面接指導
update("法66条の8の4", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>労働基準法第41条の2第1項（高度プロフェッショナル制度）の規定により労働する労働者であって、</li><li>その健康管理時間が当該労働者の健康の保持を考慮して厚生労働省令で定める時間を超えるものに対し、</li></ul><div class="predicate-line">医師による面接指導を<span class="predicate">行わなければならない。</span></div></div></div>')

# 92. 法66条の10 - ストレスチェック
update("法66条の10", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><div class="predicate-line">労働者に対し、医師、保健師その他の厚生労働省令で定める者（以下「<span class="subject">医師等</span>」という。）による<br>心理的な負担の程度を把握するための検査を<span class="predicate">行わなければならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><div class="predicate-line">前項の規定により行う検査を受けた労働者に対し、<br>当該検査を行った医師等から当該検査の結果が通知されるように<span class="predicate">しなければならない。</span></div><div class="predicate-line">この場合において、当該<span class="subject">医師等</span>は、<br>あらかじめ当該検査を受けた労働者の同意を得ないで、<br>当該労働者の検査の結果を事業者に<span class="predicate">提供してはならない。</span></div></div></div>')

# 93. 法67条 - 健康管理手帳
update("法67条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">都道府県労働局長</span>は、</div><ul class="condition-list"><li>がんその他の重度の健康障害を生ずるおそれのある業務で、政令で定めるものに従事していた者のうち、</li><li>厚生労働省令で定める要件に該当する者に対し、</li></ul><div class="predicate-line">離職の際に<span class="logic">又は</span>離職の後に、当該業務に係る<span class="subject">健康管理手帳</span>を<span class="predicate">交付するものとする。</span></div></div><div class="exception-section"><div class="exception-keyword"><span class="exception">ただし、</span></div><ul class="condition-list"><li>現に当該業務に係る健康管理手帳を所持している者については、</li></ul><div class="predicate-line"><span class="exception">この限りでない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">政府</span>は、</div><div class="predicate-line">健康管理手帳を所持している者に対する健康診断に関し、必要な措置を<span class="predicate">行う。</span></div></div><div class="principle-section"><span class="item-number">第3項</span><div class="predicate-line">健康管理手帳の交付を受けた者は、当該健康管理手帳を他人に譲渡し、<span class="logic">又は</span>貸与<span class="predicate">してはならない。</span></div></div></div>')

# 94. 法68条 - 病者の就業禁止
update("法68条", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>伝染性の疾病その他の疾病で、厚生労働省令で定めるものにかかった労働者については、</li></ul><div class="predicate-line">その就業を<span class="predicate">禁止しなければならない。</span></div></div></div>')

# 95. 法68条の2 - 受動喫煙防止
update("法68条の2", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">事業者</span>は、</div><div class="predicate-line">労働者の受動喫煙を防止するため、<br>当該事業者<span class="logic">及び</span>事業場の実情に応じ適切な措置を講ずるよう<span class="predicate">努めるものとする。</span></div></div></div>')

# 96. 法71条 - 国の援助（健康保持増進）
update("法71条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">国</span>は、</div><ul class="condition-list"><li>労働者の健康の保持増進に関する措置の適切<span class="logic">かつ</span>有効な実施を図るため、</li></ul><div class="predicate-line">必要な資料の提供、作業環境測定<span class="logic">及び</span>健康診断の実施の促進、<br>受動喫煙の防止のための設備の設置の促進、<br>事業場における健康教育等に関する指導員の確保<span class="logic">及び</span>資質の向上の促進<br>その他の必要な援助に<span class="predicate">努めるものとする。</span></div></div></div>')

# 97. 法65条の4 - 作業時間の制限
update("法65条の4", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>潜水業務その他の健康障害を生ずるおそれのある業務で、厚生労働省令で定めるものに従事させる労働者については、</li></ul><div class="predicate-line">厚生労働省令で定める作業時間についての基準に違反して、<br>当該業務に<span class="predicate">従事させてはならない。</span></div></div></div>')

# 98. 法65条の3 - 作業の管理
update("法65条の3", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">事業者</span>は、</div><div class="predicate-line">労働者の健康に配慮して、労働者の従事する作業を適切に管理するように<span class="predicate">努めなければならない。</span></div></div></div>')

# 99. 法69条 - 健康教育等
update("法69条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><div class="predicate-line">労働者に対する健康教育<span class="logic">及び</span>健康相談その他労働者の健康の保持増進を図るため<br>必要な措置を継続的<span class="logic">かつ</span>計画的に講ずるように<span class="predicate">努めなければならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">労働者</span>は、</div><div class="predicate-line">前項の事業者が講ずる措置を利用して、その健康の保持増進に<span class="predicate">努めるものとする。</span></div></div></div>')

# 100. 法71条の2 - 快適な職場環境
update("法71条の2", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>事業場における安全衛生の水準の向上を図るため、</li><li>次の措置を継続的<span class="logic">かつ</span>計画的に講ずることにより、</li></ul><div class="predicate-line">快適な職場環境を形成するように<span class="predicate">努めなければならない。</span></div><ul class="condition-list"><li>1. 作業環境を快適な状態に維持管理するための措置</li><li>2. 労働者の従事する作業について、その方法を改善するための措置</li><li>3. 作業に従事することによる労働者の疲労を回復するための施設<span class="logic">又は</span>設備の設置<span class="logic">又は</span>整備</li><li>4. 前3号に掲げるもののほか、快適な職場環境を形成するため必要な措置</li></ul></div></div>')

# 101. 法78条 - 特別安全衛生改善計画
update("法78条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">厚生労働大臣</span>は、</div><ul class="condition-list"><li>重大な労働災害が<span class="condition">発生した場合</span>において、</li><li>重大な労働災害の再発を防止するため必要がある場合として厚生労働省令で定める場合に該当すると<span class="condition">認めるとき</span>は、</li></ul><div class="predicate-line"><span class="subject">事業者</span>に対し、その事業場の安全<span class="logic">又は</span>衛生に関する改善計画<br>（以下「<span class="subject">特別安全衛生改善計画</span>」という。）を作成し、<br>これを厚生労働大臣に提出すべきことを<span class="predicate">指示することができる。</span></div></div><div class="principle-section"><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li><span class="condition">特別安全衛生改善計画を作成しようとする場合</span>には、</li></ul><div class="predicate-line">当該事業場の過半数労働組合<span class="logic">又は</span>過半数代表者の意見を<span class="predicate">聴かなければならない。</span></div></div></div>')

# 102. 法79条 - 安全衛生改善計画
update("法79条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">都道府県労働局長</span>は、</div><ul class="condition-list"><li>事業場の施設その他の事項について、労働災害の防止を図るため総合的な改善措置を講ずる必要があると<span class="condition">認めるとき</span>は、</li></ul><div class="predicate-line">事業者に対し、当該事業場の安全<span class="logic">又は</span>衛生に関する改善計画<br>（以下「<span class="subject">安全衛生改善計画</span>」という。）を作成すべきことを<span class="predicate">指示することができる。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li><span class="condition">安全衛生改善計画を作成しようとする場合</span>には、</li></ul><div class="predicate-line">当該事業場の過半数労働組合<span class="logic">又は</span>過半数代表者の意見を<span class="predicate">聴かなければならない。</span></div><div class="predicate-line">また、第1項の事業者<span class="logic">及び</span>その労働者は、安全衛生改善計画を<span class="predicate">守らなければならない。</span></div></div></div>')

# 103. 法80条 - コンサルタント診断の勧奨
update("法80条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">厚生労働大臣</span>は、</div><ul class="condition-list"><li>第78条第1項又は第4項の規定による特別安全衛生改善計画の作成<span class="logic">又は</span>変更の指示をした<span class="condition">場合</span>において、</li><li>専門的な助言を必要とすると認めるときは、</li></ul><div class="predicate-line">当該事業者に対し、<span class="subject">労働安全コンサルタント<span class="logic">又は</span>労働衛生コンサルタント</span>による安全<span class="logic">又は</span>衛生に係る診断を受け、<br><span class="logic">かつ</span>、特別安全衛生改善計画の作成<span class="logic">又は</span>変更について、これらの者の意見を聴くべきことを<span class="predicate">勧奨することができる。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">都道府県労働局長</span>は、</div><ul class="condition-list"><li>第79条第1項の規定による安全衛生改善計画の作成の指示をした<span class="condition">場合</span>において、</li><li>専門的な助言を必要とすると認めるときは、</li></ul><div class="predicate-line">当該事業者に対し、労働安全コンサルタント<span class="logic">又は</span>労働衛生コンサルタントによる安全<span class="logic">又は</span>衛生に係る診断を受け、<br><span class="logic">かつ</span>、安全衛生改善計画の作成について、これらの者の意見を聴くべきことを<span class="predicate">勧奨することができる。</span></div></div></div>')

# 104. 法81条 - コンサルタントの業務
update("法81条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">労働安全コンサルタント</span>は、</div><div class="predicate-line">労働安全コンサルタントの名称を用いて、他人の求めに応じ報酬を得て、<br>労働者の安全の水準の向上を図るため、事業場の安全についての診断<span class="logic">及び</span>これに基づく指導を行うことを<span class="predicate">業とする。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">労働衛生コンサルタント</span>は、</div><div class="predicate-line">労働衛生コンサルタントの名称を用いて、他人の求めに応じ報酬を得て、<br>労働者の衛生の水準の向上を図るため、事業場の衛生についての診断<span class="logic">及び</span>これに基づく指導を行うことを<span class="predicate">業とする。</span></div></div></div>')

# 105. 法86条 - コンサルタントの義務
update("法86条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">コンサルタント</span>は、</div><div class="predicate-line">コンサルタントの信用を傷つけ、<span class="logic">又は</span>コンサルタント全体の不名誉となるような行為を<span class="predicate">してはならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">コンサルタント</span>は、</div><div class="predicate-line">その業務に関して知り得た秘密を漏らし、<span class="logic">又は</span>盗用<span class="predicate">してはならない。</span></div><div class="predicate-line">コンサルタントでなくなった後においても、同様とする。</div></div></div>')

# 106. 法88条 - 計画の届出
update("法88条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>機械等で、厚生労働省令で定めるものを設置し、<span class="logic">若しくは</span>移転し、<span class="logic">又は</span>これらの主要構造部分を変更しようとするときは、</li></ul><div class="predicate-line">その計画を当該工事の開始の日の<span class="period">30日前</span>までに、<br><span class="subject">労働基準監督署長</span>に<span class="predicate">届け出なければならない。</span></div></div></div>')

# 107. 法88条1項 - (empty)
update("法88条1項", '<div class="law-body"><div class="principle-section"><div class="predicate-line">（法88条第1項の詳細規定 — 上位条文を参照）</div></div></div>')

# 108. 法89条 - 計画の審査
update("法89条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">厚生労働大臣</span>は、</div><div class="predicate-line">第88条第1項から第3項までの規定による届出があった計画のうち、<br>高度の技術的検討を要するものについて審査を<span class="predicate">することができる。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">厚生労働大臣</span>は、</div><div class="predicate-line">前項の審査を行うに当たっては、学識経験者の意見を<span class="predicate">きかなければならない。</span></div></div><div class="principle-section"><span class="item-number">第3項</span><div class="subject-line"><span class="subject">厚生労働大臣</span>は、</div><ul class="condition-list"><li><span class="condition">第1項の審査の結果必要があると認めるとき</span>は、</li></ul><div class="predicate-line">届出をした事業者に対し、労働災害の防止に関する事項について<br>必要な勧告<span class="logic">又は</span>要請を<span class="predicate">することができる。</span></div></div></div>')

# 109. 法89条の2 - 審査の準用
update("法89条の2", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">都道府県労働局長</span>は、</div><div class="predicate-line">第88条第1項<span class="logic">又は</span>第3項の規定による届出があった計画のうち、<br>高度の技術的検討を要するものに準ずるものとして厚生労働省令で定めるものについて<br>審査を<span class="predicate">することができる。</span></div></div></div>')

# 110. 法90条 - 労働基準監督署長等の職権
update("法90条", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">労働基準監督署長<span class="logic">及び</span>労働基準監督官</span>は、</div><div class="predicate-line">労働安全衛生法の施行に関する事務を<span class="predicate">つかさどる。</span></div></div></div>')

# 111. 法91条 - 労働基準監督官の権限
update("法91条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">労働基準監督官</span>は、</div><ul class="condition-list"><li>労働安全衛生法を施行するため必要があると<span class="condition">認めるとき</span>は、</li></ul><div class="predicate-line">事業場に立ち入り、関係者に質問し、帳簿、書類その他の物件を検査し、<br><span class="logic">若しくは</span>作業環境測定を行い、<span class="logic">又は</span>検査に必要な限度において<br>無償で製品、原材料<span class="logic">若しくは</span>器具を<span class="predicate">収去することができる。</span></div></div></div>')

# 112. 法93条 - 産業安全専門官等
update("法93条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="predicate-line">厚生労働省、都道府県労働局<span class="logic">及び</span>労働基準監督署に、<br><span class="subject">産業安全専門官<span class="logic">及び</span>労働衛生専門官</span>を<span class="predicate">置く。</span></div></div></div>')

# 113. 法95条 - 労働衛生指導医
update("法95条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="predicate-line">都道府県労働局に、<span class="subject">労働衛生指導医</span>を<span class="predicate">置く。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">労働衛生指導医</span>は、</div><div class="predicate-line">第65条第5項（作業環境測定の実施等）<span class="logic">又は</span>第66条第4項（臨時の健康診断等）の規定による指示に関する事務<br>その他労働者の衛生に関する事務に<span class="predicate">参画する。</span></div></div><div class="principle-section"><span class="item-number">第3項</span><div class="subject-line"><span class="subject">労働衛生指導医</span>は、</div><div class="predicate-line">労働衛生に関し学識経験を有する医師のうちから、<span class="subject">厚生労働大臣</span>が<span class="predicate">任命する。</span></div></div></div>')

# 114. 法96条 - 労働衛生指導医の立入検査
update("法96条", '<div class="law-body"><div class="principle-section"><span class="item-number">第4項</span><div class="subject-line"><span class="subject">都道府県労働局長</span>は、</div><ul class="condition-list"><li>労働衛生指導医を第95条第2項の規定による事務に参画させるため必要があると<span class="condition">認めるとき</span>は、</li></ul><div class="predicate-line">当該労働衛生指導医をして事業場に立ち入り、関係者に質問させ、<br><span class="logic">又は</span>作業環境測定<span class="logic">若しくは</span>健康診断の結果の記録その他の物件を<span class="predicate">検査させることができる。</span></div></div></div>')

# 115. 法97条 - 申告
update("法97条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">作業従事者</span>は、</div><ul class="condition-list"><li>事業場に労働安全衛生法<span class="logic">又は</span>これに基づく命令の規定に違反する事実があるときは、</li></ul><div class="predicate-line">その事実を都道府県労働局長、労働基準監督署長<span class="logic">又は</span>労働基準監督官に申告して<br>是正のため適当な措置をとるように<span class="predicate">求めることができる。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><div class="predicate-line">前項の申告をしたことを理由として、労働者に対し、<br>解雇その他不利益な取扱いを<span class="predicate">してはならない。</span></div></div></div>')

# 116. 法98条 - 使用停止命令等
update("法98条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">都道府県労働局長<span class="logic">又は</span>労働基準監督署長</span>は、</div><ul class="condition-list"><li>第20条から第25条まで等の規定に違反する事実が<span class="condition">あるとき</span>は、</li></ul><div class="predicate-line">その違反した事業者、注文者、機械等貸与者<span class="logic">又は</span>建築物貸与者に対し、<br>作業の全部<span class="logic">又は</span>一部の停止、建設物等の全部<span class="logic">又は</span>一部の使用の停止<span class="logic">又は</span>変更<br>その他労働災害を防止するため必要な事項を<span class="predicate">命ずることができる。</span></div></div></div>')

# 117. 法99条 - 応急措置命令
update("法99条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">都道府県労働局長<span class="logic">又は</span>労働基準監督署長</span>は、</div><ul class="condition-list"><li>法98条第1項の場合以外の場合において、</li><li>労働災害発生の急迫した危険があり、<span class="logic">かつ</span>、緊急の必要があるときは、</li></ul><div class="predicate-line">必要な限度において、事業を行う者に対し、<br>作業の全部<span class="logic">又は</span>一部の一時停止、建設物等の全部<span class="logic">又は</span>一部の使用の一時停止<br>その他当該労働災害を防止するため必要な応急の措置を講ずることを<span class="predicate">命ずることができる。</span></div></div></div>')

# 118. 法99条の2 - 講習の受講指示
update("法99条の2", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">都道府県労働局長</span>は、</div><ul class="condition-list"><li>労働災害が<span class="condition">発生した場合</span>において、</li><li>その再発を防止するため必要があると認めるときは、</li></ul><div class="predicate-line">当該労働災害に係る事業者に対し、期間を定めて、<br>当該労働災害が発生した事業場の総括安全衛生管理者、安全管理者、衛生管理者、統括安全衛生責任者<br>その他労働災害の防止のための業務に従事する者に<br>都道府県労働局長の指定する者が行う講習を受けさせるよう<span class="predicate">指示することができる。</span></div></div></div>')

# 119. 法100条 - 報告等
update("法100条", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">厚生労働大臣</span>、<span class="subject">都道府県労働局長</span><span class="logic">又は</span><span class="subject">労働基準監督署長</span>は、</div><ul class="condition-list"><li>労働安全衛生法を施行するため必要があると認めるときは、</li><li>事業者、労働者、機械等貸与者、建築物貸与者、通知対象物譲渡者等<span class="logic">又は</span>コンサルタントに対し、</li></ul><div class="predicate-line">必要な事項を報告させ、<span class="logic">又は</span>出頭を<span class="predicate">命ずることができる。</span></div></div></div>')

# 120. 則97条 - 労働者死傷病報告
update("則97条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>労働者が労働災害等により死亡し、<span class="logic">又は</span>休業したときは、</li></ul><div class="predicate-line">遅滞なく、所定事項を所轄労働基準監督署長に<span class="predicate">報告しなければならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line">前項の場合において、休業の日数が<span class="period">4日に満たないとき</span>は、</div><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li><span class="period">1月から3月</span>まで、<span class="period">4月から6月</span>まで、<span class="period">7月から9月</span>まで<span class="logic">及び</span><span class="period">10月から12月</span>までの期間における当該事実について、</li></ul><div class="predicate-line">それぞれの期間における最後の月の翌月末日までに、<br>所定の事項<span class="logic">及び</span>休業日数を所轄労働基準監督署長に<span class="predicate">報告しなければならない。</span></div></div></div>')

# 121. 則96条 - 事故報告
update("則96条", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>所定の場合は、</li></ul><div class="predicate-line">遅滞なく、報告書を所轄労働基準監督署長に<span class="predicate">提出しなければならない。</span></div></div></div>')

# 122. 法101条 - 法令の周知
update("法101条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><div class="predicate-line">労働安全衛生法<span class="logic">及び</span>これに基づく命令の要旨を常時各作業場の見やすい場所に掲示し、<br><span class="logic">又は</span>備え付けることその他の厚生労働省令で定める方法により、労働者に<span class="predicate">周知させなければならない。</span></div></div><div class="principle-section"><span class="item-number">第4項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><div class="predicate-line">第57条の2第1項<span class="logic">又は</span>第2項の規定により通知された事項を、<br>化学物質等を取り扱う各作業場の見やすい場所に常時掲示し、<span class="logic">又は</span>備え付けることその他の厚生労働省令で定める方法により、<br>当該物を取り扱う労働者に<span class="predicate">周知させなければならない。</span></div></div></div>')

# 123. 法102条 - 工作物の教示
update("法102条", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">ガス工作物その他政令で定める工作物を設けている者</span>は、</div><ul class="condition-list"><li>当該工作物の所在する場所<span class="logic">又は</span>その附近で工事その他の仕事を行う事業者から、</li><li>当該工作物による労働災害の発生を防止するためにとるべき措置についての教示を求められたときは、</li></ul><div class="predicate-line">これを<span class="predicate">教示しなければならない。</span></div></div></div>')

# 124. 法104条 - 心身の状態に関する情報の取扱い
update("法104条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>労働安全衛生法<span class="logic">又は</span>同法に基づく命令の規定による措置の実施に関し、</li><li>労働者の心身の状態に関する情報を収集し、保管し、<span class="logic">又は</span>使用するに当たっては、</li></ul><div class="predicate-line">労働者の健康の確保に必要な範囲内で労働者の心身の状態に関する情報を収集し、<br><span class="logic">並びに</span>当該収集の目的の範囲内でこれを保管し、<span class="logic">及び</span>使用<span class="predicate">しなければならない。</span></div></div><div class="exception-section"><div class="exception-keyword"><span class="exception">ただし、</span></div><ul class="condition-list"><li>本人の同意がある場合その他正当な事由がある場合は、</li></ul><div class="predicate-line"><span class="exception">この限りでない。</span></div></div></div>')

# 125. 法106条 - 国の援助
update("法106条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">国</span>は、</div><ul class="condition-list"><li>労働災害の防止に資するため、</li><li>事業者が行う安全衛生施設の整備、特別安全衛生改善計画<span class="logic">又は</span>安全衛生改善計画の実施その他の活動について、</li></ul><div class="predicate-line">金融上の措置、技術上の助言その他必要な援助を行うように<span class="predicate">努めるものとする。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">国</span>は、</div><div class="predicate-line">前項の援助を行うに当たっては、中小企業者に対し、特別の<span class="predicate">配慮をするものとする。</span></div></div></div>')

# 126. 法111条 - 審査請求の制限
update("法111条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="predicate-line">製造時等検査、性能検査、個別検定<span class="logic">又は</span>型式検定の結果についての処分については、<br>審査請求を<span class="predicate">することができない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="predicate-line">指定試験機関が行う試験事務に係る処分<span class="logic">若しくは</span>その不作為、<br>指定コンサルタント試験機関が行うコンサルタント試験事務に係る処分<span class="logic">若しくは</span>その不作為<span class="logic">又は</span><br>指定登録機関が行う登録事務に係る処分<span class="logic">若しくは</span>その不作為については、<br><span class="subject">厚生労働大臣</span>に対し、審査請求を<span class="predicate">することができる。</span></div></div></div>')

# 127. 法116条 - 罰則
update("法116条", '<div class="law-body"><div class="principle-section"><div class="predicate-line">第55条（製造等禁止物質の製造等の禁止）の規定に違反した者は、<br><span class="period">3年</span>以下の拘禁刑<span class="logic">又は</span><span class="period">300万円</span>以下の罰金に<span class="predicate">処する。</span></div></div></div>')

# 128. 法122条 - 両罰規定
update("法122条", '<div class="law-body"><div class="principle-section"><div class="predicate-line">法人の代表者又は法人<span class="logic">若しくは</span>人の代理人、使用人その他の従業者が、<br>その法人又は人の業務に関して、<br>第116条、第117条、第119条<span class="logic">又は</span>第120条の違反行為をしたときは、<br>行為者を罰するほか、その法人<span class="logic">又は</span>人に対しても、各本条の罰金刑を<span class="predicate">科する。</span></div></div></div>')

print(f"\nBatch 4 done. Total items: {len(data)}")

with open('structured_労働安全衛生法.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Saved.")

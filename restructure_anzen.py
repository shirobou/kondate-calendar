"""
労働安全衛生法の構造化HTMLを労働基準法と同品質に作り直すスクリプト
"""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('structured_労働安全衛生法.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Build a map: reference -> index
ref_map = {item['reference']: i for i, item in enumerate(data)}

def update(ref, html):
    """Update the structured HTML for a given reference."""
    if ref in ref_map:
        data[ref_map[ref]]['structured'] = html
        print(f"  Updated: {ref}")
    else:
        print(f"  WARNING: {ref} not found!")

# ============================================================
# Articles 0-29
# ============================================================

# 0. 法1条 - 目的 (already decent, but improve)
update("法1条", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">労働安全衛生法</span>は、</div><ul class="condition-list"><li>労働基準法と相まって、</li><li>労働災害の防止のための危害防止基準の確立、</li><li>責任体制の明確化<span class="logic">及び</span></li><li>自主的活動の促進の措置を講ずる等</li><li>その防止に関する総合的計画的な対策を推進することにより</li></ul><div class="predicate-line">職場における労働者の安全と健康を確保するとともに、<br>快適な職場環境の形成を促進することを<span class="predicate">目的とする。</span></div></div></div>')

# 1. 法2条 - 定義
update("法2条", '<div class="law-body"><div class="principle-section"><div class="subject-line">労働安全衛生法において、次の各号に掲げる用語の意義は、それぞれ当該各号に定めるところによる。</div><ul class="condition-list"><li><span class="item-number">1号</span> <span class="subject">労働災害</span>…労働者の就業に係る建設物、設備、原材料、ガス、蒸気、粉じん等により、<span class="logic">又は</span>作業行動その他業務に起因して、<br>労働者が負傷し、疾病にかかり、<span class="logic">又は</span>死亡することをいう。</li><li><span class="item-number">2号</span> <span class="subject">労働者</span>…労働基準法第9条に規定する労働者<br>（<span class="exception">同居の親族のみを使用する事業<span class="logic">又は</span>事務所に使用される者<span class="logic">及び</span>家事使用人を除く。</span>）をいう。</li><li><span class="item-number">3号</span> <span class="subject">事業者</span>…事業を行う者で、労働者を使用するものをいう。</li><li><span class="item-number">3号の2</span> <span class="subject">化学物質</span>…元素<span class="logic">及び</span>化合物をいう。</li><li><span class="item-number">4号</span> <span class="subject">作業環境測定</span>…作業環境の実態をは握するため空気環境その他の作業環境について行う<br>デザイン、サンプリング<span class="logic">及び</span>分析（解析を含む。）をいう。</li></ul></div></div>')

# 2. 法115条 - 適用除外
update("法115条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">労働安全衛生法</span>（<span class="exception">労働災害防止計画に関する規定を除く。</span>）は、</div><ul class="condition-list"><li>鉱山保安法第2条第2項<span class="logic">及び</span>第4項の規定による鉱山における保安については、</li></ul><div class="predicate-line"><span class="predicate">適用しない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">労働安全衛生法</span>は、</div><ul class="condition-list"><li>船員法の適用を受ける船員については、</li></ul><div class="predicate-line"><span class="predicate">適用しない。</span></div></div></div>')

# 3. 法3条 - 事業者等の責務
update("法3条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>単に労働安全衛生法で定める労働災害の防止のための最低基準を守るだけでなく、</li><li>快適な職場環境の実現と労働条件の改善を通じて</li><li>職場における労働者の安全と健康を確保するように</li></ul><div class="predicate-line"><span class="predicate">しなければならない。</span></div><div class="subject-line">また、<span class="subject">事業者</span>は、</div><div class="predicate-line">国が実施する労働災害の防止に関する施策に協力するように<span class="predicate">しなければならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">機械、器具その他の設備を設計し、製造し、<span class="logic">若しくは</span>輸入する者、<br>原材料を製造し、<span class="logic">若しくは</span>輸入する者<span class="logic">又は</span><br>建設物を建設し、<span class="logic">若しくは</span>設計する者</span>は、</div><div class="predicate-line">これらの物の設計、製造、輸入<span class="logic">又は</span>建設に際して、<br>これらの物が使用されることによる労働災害の発生の防止に資するように<span class="predicate">努めなければならない。</span></div></div><div class="principle-section"><span class="item-number">第3項</span><div class="subject-line"><span class="subject">建設工事の注文者その他の仕事を他人に請け負わせる者</span>は、</div><div class="predicate-line">施工方法、作業方法、工期、納期等について、<br>安全で衛生的な作業の遂行を損なうおそれのある条件を付さないように<span class="predicate">配慮しなければならない。</span></div></div></div>')

# 4. 法4条 - 労働者の協力義務
update("法4条", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">労働者<span class="logic">及び</span>労働者以外の者で労働者と同一の場所において仕事の作業に従事するもの</span>は、</div><ul class="condition-list"><li>労働災害を防止するため必要な事項を守るほか、</li><li>事業者その他の関係者が実施する労働災害の防止に関する措置に協力するように</li></ul><div class="predicate-line"><span class="predicate">努めなければならない。</span></div></div></div>')

# 5. 法5条 - 事業者の届出等
update("法5条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line">2以上の建設業に属する事業の事業者が、一の場所において行われる当該事業の仕事を<span class="condition">共同連帯して請け負った場合</span>においては、</div><ul class="condition-list"><li>そのうちの1人を代表者として定め、</li><li>これを当該仕事の開始の日の<span class="period">14日前</span>までに、</li><li>当該仕事が行われる場所を管轄する労働基準監督署長を経由して、</li><li>当該仕事が行われる場所を管轄する都道府県労働局長に</li></ul><div class="predicate-line"><span class="predicate">届け出なければならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="condition">前項の規定による届出がないとき</span>は、</div><div class="predicate-line"><span class="subject">都道府県労働局長</span>が代表者を<span class="predicate">指名する。</span></div></div><div class="principle-section"><span class="item-number">第4項</span><div class="subject-line"><span class="condition">第1項に規定する場合</span>においては、</div><ul class="condition-list"><li>当該事業を同項<span class="logic">又は</span>第2項の代表者のみの事業と、</li><li>当該代表者のみを当該事業の事業者と、</li><li>当該事業の仕事に従事する労働者を当該代表者のみが使用する労働者と</li></ul><div class="predicate-line">それぞれみなして、労働安全衛生法を<span class="predicate">適用する。</span></div></div></div>')

# 6. 法6条 - 労働災害防止計画の策定
update("法6条", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">厚生労働大臣</span>は、</div><ul class="condition-list"><li>労働政策審議会の意見をきいて、</li><li>労働災害の防止のための主要な対策に関する事項その他労働災害の防止に関し重要な事項を定めた計画<br>（以下「労働災害防止計画」という。）を</li></ul><div class="predicate-line"><span class="predicate">策定しなければならない。</span></div></div></div>')

# 7. 法7条 - 労働災害防止計画の変更
update("法7条", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">厚生労働大臣</span>は、</div><ul class="condition-list"><li>労働災害の発生状況、労働災害の防止に関する対策の効果等を考慮して</li><li>必要があると<span class="condition">認めるとき</span>は、</li><li>労働政策審議会の意見をきいて、</li></ul><div class="predicate-line">労働災害防止計画を<span class="predicate">変更しなければならない。</span></div></div></div>')

# 8. 法8条 - 労働災害防止計画の公表
update("法8条", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">厚生労働大臣</span>は、</div><ul class="condition-list"><li><span class="condition">労働災害防止計画を策定したとき</span>は、</li></ul><div class="predicate-line">遅滞なく、これを<span class="predicate">公表しなければならない。</span></div><div class="predicate-line">これを変更したときも、同様とする。</div></div></div>')

# 9. 法9条 - 勧告等
update("法9条", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">厚生労働大臣</span>は、</div><ul class="condition-list"><li>労働災害防止計画の的確かつ円滑な実施のため</li><li>必要があると<span class="condition">認めるとき</span>は、</li></ul><div class="predicate-line">事業を行う者、その団体その他の関係者に対し、<br>労働災害の防止に関する事項について必要な勧告<span class="logic">又は</span>要請を<span class="predicate">することができる。</span></div></div></div>')

# 10. 法10条 - 総括安全衛生管理者
update("法10条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>政令で定める規模の事業場ごとに、</li><li><span class="subject">総括安全衛生管理者</span>を選任し、</li><li>その者に安全管理者、衛生管理者<span class="logic">又は</span>救護技術管理者の指揮をさせるとともに、</li></ul><div class="predicate-line">安全衛生に関する業務を統括管理<span class="predicate">させなければならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">総括安全衛生管理者</span>は、</div><div class="predicate-line">当該事業場においてその事業の実施を統括管理する者をもって<span class="predicate">充てなければならない。</span></div></div><div class="principle-section"><span class="item-number">第3項</span><div class="subject-line"><span class="subject">都道府県労働局長</span>は、</div><ul class="condition-list"><li>労働災害を防止するため必要があると<span class="condition">認めるとき</span>は、</li></ul><div class="predicate-line">総括安全衛生管理者の業務の執行について事業者に<span class="predicate">勧告することができる。</span></div></div></div>')

# 11. 法11条 - 安全管理者
update("法11条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>政令で定める業種<span class="logic">及び</span>規模の事業場ごとに、</li><li>厚生労働省令で定める資格を有する者のうちから、</li><li><span class="subject">安全管理者</span>を選任し、</li></ul><div class="predicate-line">その者に第10条第1項各号の業務のうち安全に係る技術的事項を<span class="predicate">管理させなければならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">労働基準監督署長</span>は、</div><ul class="condition-list"><li>労働災害を防止するため必要があると<span class="condition">認めるとき</span>は、</li></ul><div class="predicate-line">事業者に対し、安全管理者の増員<span class="logic">又は</span>解任を<span class="predicate">命ずることができる。</span></div></div></div>')

# 12. 法12条 - 衛生管理者
update("法12条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>政令で定める規模の事業場ごとに、</li><li>都道府県労働局長の免許を受けた者その他厚生労働省令で定める資格を有する者のうちから、</li><li>当該事業場の業務の区分に応じて、</li><li><span class="subject">衛生管理者</span>を選任し、</li></ul><div class="predicate-line">その者に第10条第1項各号の業務のうち衛生に係る技術的事項を<span class="predicate">管理させなければならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">労働基準監督署長</span>は、</div><ul class="condition-list"><li>労働災害を防止するため必要があると<span class="condition">認めるとき</span>は、</li></ul><div class="predicate-line">事業者に対し、衛生管理者の増員<span class="logic">又は</span>解任を<span class="predicate">命ずることができる。</span></div></div></div>')

# 13. 法13条 - 産業医
update("法13条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>政令で定める規模の事業場ごとに、</li><li>医師のうちから<span class="subject">産業医</span>を選任し、</li></ul><div class="predicate-line">その者に労働者の健康管理その他の厚生労働省令で定める事項（以下「労働者の健康管理等」という。）を<span class="predicate">行わせなければならない。</span></div></div><div class="principle-section"><span class="item-number">第3項</span><div class="subject-line"><span class="subject">産業医</span>は、</div><div class="predicate-line">労働者の健康管理等を行うのに必要な医学に関する知識に基づいて、<br>誠実にその職務を<span class="predicate">行わなければならない。</span></div></div><div class="principle-section"><span class="item-number">第4項</span><div class="subject-line">産業医を選任した<span class="subject">事業者</span>は、</div><div class="predicate-line"><span class="subject">産業医</span>に対し、労働者の労働時間に関する情報その他の<br>産業医が労働者の健康管理等を適切に行うために必要な情報として厚生労働省令で定めるものを<span class="predicate">提供しなければならない。</span></div></div></div>')

# 14. 法13条の2 - 産業医等
update("法13条の2", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>第13条第1項の事業場以外の事業場については、</li><li>労働者の健康管理等を行うのに必要な医学に関する知識を有する医師その他厚生労働省令で定める者に</li></ul><div class="predicate-line">労働者の健康管理等の全部<span class="logic">又は</span>一部を行わせるように<span class="predicate">努めなければならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">前項に規定する者に労働者の健康管理等の全部<span class="logic">又は</span>一部を行わせる事業者</span>は、</div><div class="predicate-line">同項に規定する者に対し、労働者の労働時間に関する情報その他の<br>労働者の健康管理等を適切に行うために必要な情報として厚生労働省令で定めるものを提供するように<span class="predicate">努めなければならない。</span></div></div></div>')

# 15. 法13条の3 - 産業医等の体制整備
update("法13条の3", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>産業医<span class="logic">又は</span>第13条の2第1項に規定する者による労働者の健康管理等の適切な実施を図るため、</li><li>産業医<span class="logic">又は</span>同項に規定する者が労働者からの健康相談に応じ、適切に対応するために必要な体制の整備</li><li>その他の必要な措置を講ずるように</li></ul><div class="predicate-line"><span class="predicate">努めなければならない。</span></div></div></div>')

# 16. 法12条の2 - 安全衛生推進者等
update("法12条の2", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>安全管理者の選任を要する事業場<span class="logic">及び</span>衛生管理者の選任を要する事業場以外の事業場で、</li><li>使用する労働者の数が<span class="period">常時10人以上50人未満</span>の事業場ごとに、</li><li><span class="subject">安全衛生推進者</span>（安全管理者の選任を要する業種以外の業種の事業場にあっては、<span class="subject">衛生推進者</span>）を選任し、</li></ul><div class="predicate-line">その者に総括安全衛生管理者が統括管理する業務を<span class="predicate">担当させなければならない。</span></div></div></div>')

# 17. 法14条 - 作業主任者
update("法14条", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>高圧室内作業その他の労働災害を防止するための管理を必要とする作業で、政令で定めるものについては、</li><li><span class="subject">都道府県労働局長の免許を受けた者</span><span class="logic">又は</span><span class="subject">登録教習機関が行う技能講習を修了した者</span>のうちから、</li><li>当該作業の区分に応じて、</li></ul><div class="predicate-line"><span class="subject">作業主任者</span>を選任し、その者に当該作業に従事する労働者の指揮その他の厚生労働省令で定める事項を<span class="predicate">行わせなければならない。</span></div></div></div>')

# 18. 法17条 - 安全委員会
update("法17条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>政令で定める業種<span class="logic">及び</span>規模の事業場ごとに、</li><li>次の事項を調査審議させ、事業者に対し意見を述べさせるため、</li></ul><div class="predicate-line"><span class="subject">安全委員会</span>を<span class="predicate">設けなければならない。</span></div><ul class="condition-list"><li>1. 労働者の危険を防止するための基本となるべき対策に関すること。</li><li>2. 労働災害の原因<span class="logic">及び</span>再発防止対策で、安全に係るものに関すること。</li><li>3. 1.<span class="logic">及び</span>2.に掲げるもののほか、労働者の危険の防止に関する重要事項</li></ul></div></div>')

# 19. 法18条 - 衛生委員会
update("法18条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>政令で定める規模の事業場ごとに、</li><li>次の事項を調査審議させ、事業者に対し意見を述べさせるため、</li></ul><div class="predicate-line"><span class="subject">衛生委員会</span>を<span class="predicate">設けなければならない。</span></div><ul class="condition-list"><li>1. 労働者の健康障害を防止するための基本となるべき対策に関すること。</li><li>2. 労働者の健康の保持増進を図るための基本となるべき対策に関すること。</li><li>3. 労働災害の原因<span class="logic">及び</span>再発防止対策で、衛生に係るものに関すること。</li><li>4. 1.〜3.に掲げるもののほか、労働者の健康障害の防止<span class="logic">及び</span>健康の保持増進に関する重要事項</li></ul></div></div>')

# 20. 法19条 - 安全衛生委員会
update("法19条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>第17条<span class="logic">及び</span>前条の規定により安全委員会<span class="logic">及び</span>衛生委員会を設けなければならないときは、</li><li>それぞれの委員会の設置に代えて、</li></ul><div class="predicate-line"><span class="subject">安全衛生委員会</span>を<span class="predicate">設置することができる。</span></div></div></div>')

# 21. 則23条 - 委員会の運営
update("則23条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><div class="predicate-line">安全委員会、衛生委員会<span class="logic">又は</span>安全衛生委員会（以下「委員会」という。）を<br><span class="period">毎月1回以上</span>開催するように<span class="predicate">しなければならない。</span></div></div><div class="principle-section"><span class="item-number">第3項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><div class="predicate-line">委員会の開催の都度、遅滞なく、<br>委員会における議事の概要を所定の方法によって労働者に<span class="predicate">周知させなければならない。</span></div></div><div class="principle-section"><span class="item-number">第4項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><div class="predicate-line">委員会の開催の都度、所定の事項を記録し、これを<span class="period">3年間</span><span class="predicate">保存しなければならない。</span></div></div><div class="principle-section"><span class="item-number">第5項</span><div class="subject-line"><span class="subject">産業医</span>は、</div><div class="predicate-line">衛生委員会<span class="logic">又は</span>安全衛生委員会に対して<br>労働者の健康を確保する観点から必要な調査審議を<span class="predicate">求めることができる。</span></div></div></div>')

# 22. 法15条 - 統括安全衛生責任者
update("法15条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">特定元方事業者</span>は、</div><ul class="condition-list"><li>当該一の場所において、その労働者<span class="logic">及び</span>関係請負人に係る作業従事者が作業を行うときは、</li><li>これらの作業従事者の作業が同一の場所において行われることによって生ずる労働災害を防止するため、</li><li><span class="subject">統括安全衛生責任者</span>を選任し、</li><li>その者に元方安全衛生管理者の指揮をさせるとともに、</li></ul><div class="predicate-line">第30条第1項各号の事項を統括管理<span class="predicate">させなければならない。</span></div></div><div class="exception-section"><div class="exception-keyword"><span class="exception">ただし、</span></div><ul class="condition-list"><li>これらの作業従事者の数が政令で定める数未満であるときは、</li></ul><div class="predicate-line"><span class="exception">この限りでない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">統括安全衛生責任者</span>は、</div><div class="predicate-line">当該場所においてその事業の実施を統括管理する者をもって<span class="predicate">充てなければならない。</span></div></div><div class="principle-section"><span class="item-number">第5項</span><div class="subject-line"><span class="subject">都道府県労働局長</span>は、</div><ul class="condition-list"><li>労働災害を防止するため必要があると<span class="condition">認めるとき</span>は、</li></ul><div class="predicate-line">統括安全衛生責任者の業務の執行について当該統括安全衛生責任者を選任した事業者に<span class="predicate">勧告することができる。</span></div></div></div>')

# 23. 法15条の2 - 元方安全衛生管理者
update("法15条の2", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">統括安全衛生責任者を選任した事業者で、建設業その他政令で定める業種に属する事業を行うもの</span>は、</div><ul class="condition-list"><li>厚生労働省令で定める資格を有する者のうちから、</li><li><span class="subject">元方安全衛生管理者</span>を選任し、</li></ul><div class="predicate-line">その者に統括安全衛生責任者が統括管理する事項のうち技術的事項を<span class="predicate">管理させなければならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">労働基準監督署長</span>は、</div><ul class="condition-list"><li>労働災害を防止するため必要があると<span class="condition">認めるとき</span>は、</li></ul><div class="predicate-line">当該元方安全衛生管理者を選任した事業者に対し、<br>元方安全衛生管理者の増員<span class="logic">又は</span>解任を<span class="predicate">命ずることができる。</span></div></div></div>')

# 24. 法16条 - 安全衛生責任者
update("法16条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="condition">統括安全衛生責任者を選任すべき場合</span>において、</div><ul class="condition-list"><li>統括安全衛生責任者を選任すべき事業者以外の請負人で、当該仕事を自ら行うものは、</li></ul><div class="predicate-line"><span class="subject">安全衛生責任者</span>を選任し、<br>その者に統括安全衛生責任者との連絡その他の厚生労働省令で定める事項を<span class="predicate">行わせなければならない。</span></div></div></div>')

# 25. 法15条の3 - 店社安全衛生管理者
update("法15条の3", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">建設業に属する事業の元方事業者</span>は、</div><ul class="condition-list"><li>その労働者<span class="logic">及び</span>関係請負人に係る作業従事者が一の場所において作業を行うときは、</li><li>当該場所において行われる仕事に係る請負契約を締結している事業場ごとに、</li><li>これらの作業従事者の作業が同一の場所で行われることによって生ずる労働災害を防止するため、</li><li>厚生労働省令で定める資格を有する者のうちから、</li></ul><div class="predicate-line"><span class="subject">店社安全衛生管理者</span>を選任し、その者に所定の事項を<span class="predicate">行わせなければならない。</span></div></div></div>')

# 26. 法19条の2 - 能力向上教育
update("法19条の2", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>事業場における安全衛生の水準の向上を図るため、</li><li>安全管理者、衛生管理者、安全衛生推進者、衛生推進者その他労働災害の防止のための業務に従事する者に対し、</li></ul><div class="predicate-line">これらの者が従事する業務に関する能力の向上を図るための教育、講習等を行い、<br><span class="logic">又は</span>これらを受ける機会を与えるように<span class="predicate">努めなければならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">厚生労働大臣</span>は、</div><div class="predicate-line">前項の教育、講習等の適切<span class="logic">かつ</span>有効な実施を図るため必要な指針を<span class="predicate">公表するものとする。</span></div></div><div class="principle-section"><span class="item-number">第3項</span><div class="subject-line"><span class="subject">厚生労働大臣</span>は、</div><div class="predicate-line">前項の指針に従い、事業者<span class="logic">又は</span>その団体に対し、必要な指導等を<span class="predicate">行うことができる。</span></div></div></div>')

# 27. 法19条の3 - 国の援助
update("法19条の3", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">国</span>は、</div><ul class="condition-list"><li>産業医の選任が義務づけられていない事業場の労働者の健康の確保に資するため、</li></ul><div class="predicate-line">労働者の健康管理等に関する相談、情報の提供その他の必要な援助を行うように<span class="predicate">努めるものとする。</span></div></div></div>')

# 28. 法20条 - 事業者の講ずべき措置等（危険防止）
update("法20条", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">事業者</span>は、</div><div class="predicate-line">次の危険を防止するため必要な措置を<span class="predicate">講じなければならない。</span></div><ul class="condition-list"><li>1. 機械、器具その他の設備（以下「機械等」という。）による危険</li><li>2. 爆発性の物、発火性の物、引火性の物等による危険</li><li>3. 電気、熱その他のエネルギーによる危険</li></ul></div></div>')

# 29. 法21条 - 事業者の講ずべき措置等（作業方法・場所）
update("法21条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><div class="predicate-line">掘削、採石、荷役、伐木等の業務における作業方法から生ずる危険を防止するため<br>必要な措置を<span class="predicate">講じなければならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><div class="predicate-line">労働者が墜落するおそれのある場所、土砂等が崩壊するおそれのある場所等に係る危険を防止するため<br>必要な措置を<span class="predicate">講じなければならない。</span></div></div></div>')

print(f"\nBatch 1 done. Total items: {len(data)}")

# Save
with open('structured_労働安全衛生法.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Saved.")

"""
労働安全衛生法 構造化 Batch 2 (articles 30-59)
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

# 30. 法22条 - 健康障害防止措置
update("法22条", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">事業者</span>は、</div><div class="predicate-line">次の健康障害を防止するため必要な措置を<span class="predicate">講じなければならない。</span></div><ul class="condition-list"><li>1. 原材料、ガス、蒸気、粉じん、酸素欠乏空気、病原体等による健康障害</li><li>2. 放射線、高温、低温、超音波、騒音、振動、異常気圧等による健康障害</li><li>3. 計器監視、精密工作等の作業による健康障害</li><li>4. 排気、排液<span class="logic">又は</span>残さい物による健康障害</li></ul></div></div>')

# 31. 法23条 - 作業場の措置
update("法23条", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>労働者を就業させる建設物その他の作業場について、</li><li>通路、床面、階段等の保全<span class="logic">並びに</span></li><li>換気、採光、照明、保温、防湿、休養、避難<span class="logic">及び</span>清潔に必要な措置</li><li>その他労働者の健康、風紀<span class="logic">及び</span>生命の保持のため必要な措置を</li></ul><div class="predicate-line"><span class="predicate">講じなければならない。</span></div></div></div>')

# 32. 法24条 - 作業行動による労災防止
update("法24条", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">事業者</span>は、</div><div class="predicate-line">労働者の作業行動から生ずる労働災害を防止するため必要な措置を<span class="predicate">講じなければならない。</span></div></div></div>')

# 33. 法26条 - 労働者の遵守義務
update("法26条", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">労働者<span class="logic">及び</span>労働者と同一の場所において仕事の作業に従事する労働者以外の作業従事者</span>は、</div><div class="predicate-line">事業者が第20条から第25条まで<span class="logic">及び</span>前条第1項の規定に基づき講ずる措置に応じて、<br>必要な事項を<span class="predicate">守らなければならない。</span></div></div></div>')

# 34. 法28条 - 技術上の指針
update("法28条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">厚生労働大臣</span>は、</div><ul class="condition-list"><li>第20条から第25条まで<span class="logic">及び</span>第25条の2第1項の規定により事業者が講ずべき措置の適切<span class="logic">かつ</span>有効な実施を図るため</li><li>必要な業種<span class="logic">又は</span>作業ごとの技術上の指針を</li></ul><div class="predicate-line"><span class="predicate">公表するものとする。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">厚生労働大臣</span>は、</div><div class="predicate-line">前項の技術上の指針を定めるに当たっては、<br>中高年齢者に関して、特に<span class="predicate">配慮するものとする。</span></div></div></div>')

# 35. 法25条 - 緊急時の措置
update("法25条", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li><span class="condition">労働災害発生の急迫した危険があるとき</span>は、</li></ul><div class="predicate-line">直ちに作業を中止し、労働者を作業場から退避させる等必要な措置を<span class="predicate">講じなければならない。</span></div></div></div>')

# 36. 法25条の2 - 救護措置
update("法25条の2", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">建設業その他政令で定める業種に属する事業の仕事で、政令で定めるものを行う事業者</span>は、</div><ul class="condition-list"><li>爆発、火災等が生じたことに伴い作業従事者の救護に関する措置がとられる場合における<br>労働災害の発生を防止するため、次の措置を</li></ul><div class="predicate-line"><span class="predicate">講じなければならない。</span></div><ul class="condition-list"><li>1. 作業従事者の救護に関し必要な機械等の備付け<span class="logic">及び</span>管理を行うこと。</li><li>2. 作業従事者の救護に関し必要な事項についての訓練を行うこと。</li><li>3. 1.<span class="logic">及び</span>2.に掲げるもののほか、爆発、火災等に備えて、作業従事者の救護に関し必要な事項を行うこと。</li></ul></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">前項に規定する事業者</span>は、</div><div class="predicate-line">厚生労働省令で定める資格を有する者のうちから、<br>同項各号の措置のうち技術的事項を管理する者を選任し、<br>その者に当該技術的事項を<span class="predicate">管理させなければならない。</span></div></div></div>')

# 37. 法29条 - 元方事業者の指導義務
update("法29条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">元方事業者</span>は、</div><div class="predicate-line">関係請負人<span class="logic">及び</span>関係請負人に係る作業従事者が、当該仕事に関し、<br>労働安全衛生法<span class="logic">又は</span>これに基づく命令の規定に違反しないよう<br>必要な指導を<span class="predicate">行わなければならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">元方事業者</span>は、</div><ul class="condition-list"><li>関係請負人又は関係請負人に係る作業従事者が、当該仕事に関し、</li><li>労働安全衛生法<span class="logic">又は</span>これに基づく命令の規定に違反していると<span class="condition">認めるとき</span>は、</li></ul><div class="predicate-line">是正のため必要な指示を<span class="predicate">行わなければならない。</span></div></div></div>')

# 38. 法29条の2 - 建設業の元方事業者の措置
update("法29条の2", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">建設業に属する事業の元方事業者</span>は、</div><ul class="condition-list"><li>土砂等が崩壊するおそれのある場所、機械等が転倒するおそれのある場所その他の厚生労働省令で定める場所において</li><li>関係請負人に係る作業従事者が当該事業の仕事の作業を<span class="condition">行うとき</span>は、</li></ul><div class="predicate-line">当該関係請負人が講ずべき当該場所に係る危険を防止するための措置が適正に講ぜられるように、<br>技術上の指導その他の必要な措置を<span class="predicate">講じなければならない。</span></div></div></div>')

# 39. 法30条 - 特定元方事業者の措置
update("法30条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">特定元方事業者</span>は、</div><ul class="condition-list"><li>その労働者<span class="logic">及び</span>関係請負人に係る作業従事者の作業が同一の場所において行われることによって生ずる労働災害を防止するため、</li><li>次の事項に関する必要な措置を</li></ul><div class="predicate-line"><span class="predicate">講じなければならない。</span></div><ul class="condition-list"><li>1. 協議組織の設置<span class="logic">及び</span>運営を行うこと。</li><li>2. 作業間の連絡<span class="logic">及び</span>調整を行うこと。</li><li>3. 作業場所を巡視すること。</li><li>4. 関係請負人が行う労働者の安全<span class="logic">又は</span>衛生のための教育に対する指導<span class="logic">及び</span>援助を行うこと。</li><li>5. 建設業の特定元方事業者にあっては、仕事の工程に関する計画<span class="logic">及び</span>作業場所における機械、設備等の配置に関する計画を作成すること。</li><li>6. 1.〜5.に掲げるもののほか、当該労働災害を防止するため必要な事項</li></ul></div></div>')

# 40. 法30条の2 - 製造業等の元方事業者の措置
update("法30条の2", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">製造業その他政令で定める業種に属する事業（特定事業を除く。）の元方事業者</span>は、</div><ul class="condition-list"><li>その労働者<span class="logic">及び</span>関係請負人に係る作業従事者の作業が同一の場所において行われることによって生ずる労働災害を防止するため、</li></ul><div class="predicate-line">作業間の連絡<span class="logic">及び</span>調整を行うことに関する措置その他必要な措置を<span class="predicate">講じなければならない。</span></div></div></div>')

# 41. 法31条 - 注文者の措置
update("法31条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">特定事業の仕事を自ら行う注文者</span>は、</div><ul class="condition-list"><li>建設物、設備<span class="logic">又は</span>原材料（以下「建設物等」という。）を、</li><li>当該仕事を行う場所においてその請負人に係る作業従事者に使用させるときは、</li></ul><div class="predicate-line">当該建設物等について、労働災害を防止するため必要な措置を<span class="predicate">講じなければならない。</span></div></div></div>')

# 42. 法33条 - 機械等貸与者の措置
update("法33条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">機械等貸与者</span>は、</div><div class="predicate-line">当該機械等の貸与を受けた事業を行う者の事業場における<br>当該機械等による労働災害を防止するため必要な措置を<span class="predicate">講じなければならない。</span></div><ul class="condition-list"><li>1. 当該機械等をあらかじめ点検し、異常を認めたときは、補修その他必要な整備を行うこと。</li><li>2. 当該機械等の貸与を受ける事業者に対し、所定事項を記載した書面を交付すること。</li></ul></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">機械等貸与者から機械等の貸与を受けた者</span>は、</div><ul class="condition-list"><li>当該機械等を操作する者がその使用する労働者で<span class="condition">ないとき</span>は、</li></ul><div class="predicate-line">当該機械等の操作による労働災害を防止するため必要な措置を<span class="predicate">講じなければならない。</span></div></div></div>')

# 43. 法34条 - 建築物貸与者の措置
update("法34条", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">建築物貸与者</span>は、</div><div class="predicate-line">当該建築物の貸与を受けた者の事業に係る当該建築物による<br>労働災害を防止するため必要な措置を<span class="predicate">講じなければならない。</span></div></div><div class="exception-section"><div class="exception-keyword"><span class="exception">ただし、</span></div><ul class="condition-list"><li>当該建築物の全部を一の事業者<span class="logic">若しくは</span>個人事業者に貸与するとき、</li><li class="logic-item"><span class="logic">又は</span></li><li>2以上の個人事業者のみに貸与するときは、</li></ul><div class="predicate-line"><span class="exception">この限りでない。</span></div></div></div>')

# 44. 法35条 - 重量表示
update("法35条", '<div class="law-body"><div class="principle-section"><div class="subject-line">一の貨物で、重量が<span class="period">1トン</span>以上のものを発送しようとする者は、</div><div class="predicate-line">見やすく、<span class="logic">かつ</span>、容易に消滅しない方法で、<br>当該貨物にその重量を<span class="predicate">表示しなければならない。</span></div></div><div class="exception-section"><div class="exception-keyword"><span class="exception">ただし、</span></div><ul class="condition-list"><li>包装されていない貨物で、その重量が一見して明らかであるものを発送しようとするときは、</li></ul><div class="predicate-line"><span class="exception">この限りでない。</span></div></div></div>')

# 45. 法37条 - 特定機械等の定義
update("法37条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="predicate-line">特に危険な作業を必要とする機械等として別表第1に掲げるもので、<br>政令で定めるものを「<span class="subject">特定機械等</span>」という。</div></div></div>')

# 46. 法38条 - 製造時等検査
update("法38条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line">次の者は、</div><ul class="condition-list"><li>特定機械等を製造し、<span class="logic">若しくは</span>輸入した者、</li><li>特定機械等で厚生労働省令で定める期間設置されなかったものを設置しようとする者<span class="logic">又は</span></li><li>特定機械等で使用を廃止したものを再び設置し、<span class="logic">若しくは</span>使用しようとする者</li></ul><div class="predicate-line">当該特定機械等<span class="logic">及び</span>これに係る厚生労働省令で定める事項について、<br><span class="subject">登録設計審査等機関</span>の検査を<span class="predicate">受けなければならない。</span></div></div><div class="exception-section"><div class="exception-keyword"><span class="exception">ただし、</span></div><ul class="condition-list"><li>輸入された特定機械等について当該特定機械等を外国において製造した者が同項の規定による検査を受けた場合は、</li></ul><div class="predicate-line"><span class="exception">この限りでない。</span></div></div></div>')

# 47. 法39条 - 検査証の交付
update("法39条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">登録設計審査等機関</span>は、</div><ul class="condition-list"><li>第38条第1項<span class="logic">又は</span>第2項の検査（以下「製造時等検査」という。）に合格した移動式の特定機械等について、</li></ul><div class="predicate-line">検査証を<span class="predicate">交付する。</span></div></div></div>')

# 48. 法40条 - 検査証なしの使用禁止
update("法40条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="predicate-line">検査証を受けていない特定機械等は、<span class="predicate">使用してはならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="predicate-line">検査証を受けた特定機械等は、検査証とともにするのでなければ、<br>譲渡し、<span class="logic">又は</span>貸与<span class="predicate">してはならない。</span></div></div></div>')

# 49. 法41条 - 検査証の有効期間
update("法41条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">検査証の有効期間</span>は、</div><div class="predicate-line">特定機械等の種類に応じて、厚生労働省令で定める期間とする。</div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line">検査証の有効期間の更新を受けようとする者は、</div><div class="predicate-line">当該特定機械等<span class="logic">及び</span>これに係る厚生労働省令で定める事項について、<br><span class="subject">登録性能検査機関</span>が行う性能検査を<span class="predicate">受けなければならない。</span></div></div></div>')

# 50. 法42条 - 譲渡等の制限
update("法42条", '<div class="law-body"><div class="principle-section"><div class="subject-line">特定機械等以外の機械等で、</div><ul class="condition-list"><li>別表第2に掲げるものその他危険<span class="logic">若しくは</span>有害な作業を必要とするもの、</li><li>危険な場所において使用するもの<span class="logic">又は</span></li><li>危険<span class="logic">若しくは</span>健康障害を防止するため使用するもの</li></ul><div class="predicate-line">のうち、政令で定めるものは、<br>厚生労働大臣が定める規格<span class="logic">又は</span>安全装置を具備しなければ、<br>譲渡し、貸与し、<span class="logic">又は</span>設置<span class="predicate">してはならない。</span></div></div></div>')

# 51. 法43条 - 防護措置のない機械の譲渡制限
update("法43条", '<div class="law-body"><div class="principle-section"><div class="subject-line">動力により駆動される機械等で、</div><ul class="condition-list"><li>作動部分上の突起物<span class="logic">又は</span>動力伝導部分<span class="logic">若しくは</span>調速部分に</li><li>厚生労働省令で定める防護のための措置が施されていないものは、</li></ul><div class="predicate-line">譲渡し、貸与し、<span class="logic">又は</span>譲渡<span class="logic">若しくは</span>貸与の目的で<span class="predicate">展示してはならない。</span></div></div></div>')

# 52. 法44条 - 個別検定
update("法44条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line">第42条の機械等のうち、別表第3に掲げる機械等で政令で定めるものを製造し、<span class="logic">又は</span>輸入した者は、</div><div class="predicate-line"><span class="subject">登録個別検定機関</span>が個々に行う当該機械等についての検定（以下「個別検定」という。）を<span class="predicate">受けなければならない。</span></div></div><div class="principle-section"><span class="item-number">第4項</span><div class="subject-line">個別検定を受けた者は、</div><div class="predicate-line">当該個別検定に合格した機械等に、当該個別検定に合格した旨の表示を<span class="predicate">付さなければならない。</span></div></div></div>')

# 53. 法44条の2 - 型式検定
update("法44条の2", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line">第42条の機械等のうち、別表第4に掲げる機械等で政令で定めるものを製造し、<span class="logic">又は</span>輸入した者は、</div><div class="predicate-line"><span class="subject">登録型式検定機関</span>が行う当該機械等の型式についての検定（以下「型式検定」という。）を<span class="predicate">受けなければならない。</span></div></div><div class="principle-section"><span class="item-number">第4項</span><div class="subject-line"><span class="subject">登録型式検定機関</span>は、</div><div class="predicate-line">型式検定に合格した型式について、型式検定合格証を申請者に<span class="predicate">交付する。</span></div></div><div class="principle-section"><span class="item-number">第5項</span><div class="subject-line">型式検定を受けた者は、</div><div class="predicate-line">当該型式検定に合格した型式の機械等を本邦において製造し、<span class="logic">又は</span>本邦に輸入したときは、<br>当該機械等に、型式検定に合格した型式の機械等である旨の表示を<span class="predicate">付さなければならない。</span></div></div></div>')

# 54. 法43条の2 - 回収・改善命令
update("法43条の2", '<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">厚生労働大臣<span class="logic">又は</span>都道府県労働局長</span>は、</div><ul class="condition-list"><li>特定機械等以外の機械等を製造し、又は輸入した者が、</li><li>当該機械等で、所定の各号のいずれかに該当するものを譲渡し、<span class="logic">又は</span>貸与した<span class="condition">場合</span>には、</li></ul><div class="predicate-line">その者に対し、当該機械等の回収<span class="logic">又は</span>改善を図ること、<br>当該機械等を使用している者へ厚生労働省令で定める事項を通知すること<br>その他当該機械等が使用されることによる労働災害を防止するため必要な措置を講ずることを<span class="predicate">命ずることができる。</span></div></div></div>')

# 55. 法45条 - 定期自主検査
update("法45条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><div class="predicate-line">ボイラーその他の機械等で、政令で定めるものについて、<br>定期に自主検査を行い、<span class="logic">及び</span>その結果を記録して<span class="predicate">おかなければならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">事業者</span>は、</div><ul class="condition-list"><li>前項の機械等で政令で定めるものについて同項の規定による自主検査のうち</li><li>厚生労働省令で定める自主検査（以下「<span class="subject">特定自主検査</span>」という。）を行うときは、</li></ul><div class="predicate-line">その事業者で厚生労働省令で定める資格を有するものが自ら実施し、<br><span class="logic">又は</span>その使用する労働者で当該資格を有するもの<span class="logic">若しくは</span>検査業者に<span class="predicate">実施させなければならない。</span></div></div></div>')

# 56. 法55条 - 製造等の禁止
update("法55条", '<div class="law-body"><div class="principle-section"><div class="subject-line">黄りんマツチ、ベンジジン、ベンジジンを含有する製剤その他の<br>労働者に重度の健康障害を生ずる物で、政令で定めるものは、</div><div class="predicate-line">製造し、輸入し、譲渡し、提供し、<span class="logic">又は</span>使用<span class="predicate">してはならない。</span></div></div><div class="exception-section"><div class="exception-keyword"><span class="exception">ただし、</span></div><ul class="condition-list"><li>試験研究のため製造し、輸入し、<span class="logic">又は</span>使用する場合で、</li><li>政令で定める要件に該当するときは、</li></ul><div class="predicate-line"><span class="exception">この限りでない。</span></div></div></div>')

# 57. 法56条 - 製造の許可
update("法56条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line">ジクロルベンジジン、ジクロルベンジジンを含有する製剤その他の<br>労働者に重度の健康障害を生ずるおそれのある物で、政令で定めるものを製造しようとする者は、</div><div class="predicate-line">あらかじめ、<span class="subject">厚生労働大臣</span>の許可を<span class="predicate">受けなければならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">厚生労働大臣</span>は、</div><ul class="condition-list"><li><span class="condition">前項の許可の申請があった場合</span>には、</li><li>その申請を審査し、</li><li>製造設備、作業方法等が厚生労働大臣の定める基準に適合していると<span class="condition">認めるとき</span>でなければ、</li></ul><div class="predicate-line">同項の許可を<span class="predicate">してはならない。</span></div></div></div>')

# 58. 法57条 - 表示義務
update("法57条", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line">爆発性の物、発火性の物、引火性の物その他の労働者に危険を生ずるおそれのある物<br><span class="logic">若しくは</span>労働者に健康障害を生ずるおそれのある物で政令で定めるもの<br><span class="logic">又は</span>製造許可物質を容器に入れ、<span class="logic">又は</span>包装して、譲渡し、<span class="logic">又は</span>提供する者は、</div><div class="predicate-line">その容器<span class="logic">又は</span>包装に所定の事項を<span class="predicate">表示しなければならない。</span></div></div><div class="exception-section"><div class="exception-keyword"><span class="exception">ただし、</span></div><ul class="condition-list"><li>その容器<span class="logic">又は</span>包装のうち、主として一般消費者の生活の用に供するためのものについては、</li></ul><div class="predicate-line"><span class="exception">この限りでない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line">前項の政令で定める物<span class="logic">又は</span>製造許可物質を前項に規定する方法以外の方法により譲渡し、<span class="logic">又は</span>提供する者は、</div><div class="predicate-line">同項に定める所定の事項を記載した文書を、<br>譲渡し、<span class="logic">又は</span>提供する相手方に<span class="predicate">交付しなければならない。</span></div></div></div>')

# 59. 法57条の2 - SDS通知義務
update("法57条の2", '<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">通知対象物を譲渡し、<span class="logic">又は</span>提供する者（通知対象物譲渡者等）</span>は、</div><div class="predicate-line">文書の交付その他厚生労働省令で定める方法により通知対象物に関する所定の事項を、<br>譲渡し、<span class="logic">又は</span>提供する相手方に<span class="predicate">通知しなければならない。</span></div></div><div class="exception-section"><div class="exception-keyword"><span class="exception">ただし、</span></div><ul class="condition-list"><li>主として一般消費者の生活の用に供される製品として通知対象物を譲渡し、<span class="logic">又は</span>提供する場合については、</li></ul><div class="predicate-line"><span class="exception">この限りでない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">通知対象物譲渡者等</span>は、</div><ul class="condition-list"><li>前項の規定により通知した事項に変更を行う必要が<span class="condition">生じたとき</span>は、</li></ul><div class="predicate-line">文書の交付その他厚生労働省令で定める方法により、<br>変更後の事項を、速やかに、譲渡し、<span class="logic">又は</span>提供した相手方に通知するよう<span class="predicate">努めなければならない。</span></div></div></div>')

print(f"\nBatch 2 done. Total items: {len(data)}")

with open('structured_労働安全衛生法.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Saved.")

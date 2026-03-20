"""
労災保険法の構造化HTML生成（労働基準法品質）
ヒューリスティック + 手動オーバーライドで高品質な構造化HTMLを生成
"""
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')


def esc(t):
    """HTMLエスケープ"""
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def logic_wrap(text):
    """論理演算子をspanで囲む"""
    # 及び、又は、並びに、若しくは、かつ を検出
    # 括弧内のものも含めて処理
    result = text
    for op in ['並びに', '及び', '若しくは', '又は', 'かつ']:
        result = result.replace(op, f'<span class="logic">{op}</span>')
    return result


def period_wrap(text):
    """期間・数値をspanで囲む"""
    # 日数、月数、年数、歳、金額等
    patterns = [
        (r'(\d+年\d+箇月|\d+箇月間?|\d+年間?)', r'<span class="period">\1</span>'),
        (r'(\d+日分?(?:以上|以内|間|前)?)', r'<span class="period">\1</span>'),
        (r'(\d+歳(?:以上|未満|以下)?)', r'<span class="period">\1</span>'),
        (r'(100分の\d+)', r'<span class="period">\1</span>'),
        (r'(\d+万円|\d+円)', r'<span class="period">\1</span>'),
        (r'(\d+時間)', r'<span class="period">\1</span>'),
        (r'(\d+人(?:以上|以下)?)', r'<span class="period">\1</span>'),
        (r'(\d+週間)', r'<span class="period">\1</span>'),
        (r'(2年|5年|3年|1年6箇月|3箇月)', r'<span class="period">\1</span>'),
    ]
    result = text
    for pat, repl in patterns:
        result = re.sub(pat, repl, result)
    return result


def condition_wrap(text):
    """条件フレーズをspanで囲む"""
    # 「〜場合」「〜とき」パターン
    patterns = [
        (r'((?:した|する|ある|ない|できる|された|いる|なった|おいて)場合(?:において(?:は)?)?)', r'<span class="condition">\1</span>'),
        (r'((?:した|する|ある|ない|できる|された|いる|なった)とき(?:は)?)', r'<span class="condition">\1</span>'),
    ]
    result = text
    for pat, repl in patterns:
        result = re.sub(pat, repl, result)
    return result


def clean_body(body):
    """本文から解説テキストを除去し、法律条文のみを抽出"""
    if not body:
        return ''

    body = body.strip()

    # 先頭の参照記号を除去（「、（法22条）」等）
    body = re.sub(r'^[、・]\s*（[^）]+）\s*', '', body)

    # 末尾の教科書的解説を除去
    # パターン: 法律文の後に繰り返し説明がある
    # 「。」で終わる最後の法律文を見つける

    # 試験問題番号パターンの除去
    body = re.sub(r'R\d{2}-\d{2}[ァ-ヶ].*$', '', body)

    return body.strip()


def split_paragraphs(body):
    """◯1, ◯2 等で段落分割"""
    # ◯数字 パターンで分割
    parts = re.split(r'(◯\d+)', body)

    result = []
    i = 0
    while i < len(parts):
        part = parts[i].strip()
        if not part:
            i += 1
            continue

        if re.match(r'^◯(\d+)$', part):
            m = re.match(r'^◯(\d+)$', part)
            num = int(m.group(1))
            text = parts[i + 1].strip() if i + 1 < len(parts) else ''
            result.append((num, text))
            i += 2
        else:
            # 項番号なし
            result.append((0, part))
            i += 1

    return result


def split_tadashi(text):
    """ただし書きを分離"""
    # 「。ただし、」で分割
    m = re.search(r'。\s*ただし[、，]', text)
    if m:
        main = text[:m.start() + 1]  # 。まで含む
        tadashi = text[m.start() + 1:].strip()
        return main, tadashi
    return text, ''


def split_numbered_items(text):
    """番号付き項目を分割 (1. 2. 3. ...)"""
    # "1. " "2. " 等のパターン
    parts = re.split(r'(?<=\s)(\d+)\.\s+|^(\d+)\.\s+', text)
    if len(parts) <= 1:
        # 別のパターン: "1号" "2号" 等
        return [(0, text)]

    result = []
    i = 0
    while i < len(parts):
        if parts[i] is None:
            i += 1
            continue
        part = parts[i].strip()
        if re.match(r'^\d+$', part) and i + 1 < len(parts):
            num = int(part)
            content = parts[i + 1].strip() if i + 1 < len(parts) and parts[i + 1] else ''
            result.append((num, content))
            i += 2
        else:
            if part:
                result.append((0, part))
            i += 1

    return result


def extract_subject(text):
    """主語（Xは、Xが、）を抽出"""
    # 「〜は、」「〜が、」パターン
    # 長い主語もマッチさせる
    subjects = [
        '労働者災害補償保険', '労働者災害補償保険等関係事務',
        '労災保険法に基づく保険給付を受ける権利を有する者',
        '保険給付を受ける権利を有する者', '保険給付を受ける権利',
        '年金たる保険給付', '年金たる保険給付の支給',
        '療養補償給付', '療養給付', '療養の給付',
        '休業補償給付', '休業給付',
        '障害補償給付', '障害補償年金', '障害給付',
        '遺族補償給付', '遺族補償年金', '遺族補償一時金',
        '傷病補償年金', '傷病補償年金を受ける労働者',
        '介護補償給付', '介護給付',
        '二次健康診断等給付',
        '葬祭料', '葬祭給付',
        '給付基礎日額', '休業給付基礎日額', '年金給付基礎日額',
        '複数事業労働者療養給付', '複数事業労働者休業給付',
        '複数事業労働者障害給付', '複数事業労働者障害年金',
        '複数事業労働者遺族給付', '複数事業労働者遺族年金',
        '複数事業労働者葬祭給付', '複数事業労働者傷病年金',
        '複数事業労働者介護給付',
        '政府', '厚生労働大臣', '行政庁',
        '所轄都道府県労働局長', '所轄労働基準監督署長',
        '都道府県労働局長', '労働基準監督署長',
        '市町村長', '使用者', '事業者', '事業主', '労働者',
        '被保険者', '受給資格者', '受給権者',
        '租税その他の公課',
    ]

    # 長い順にマッチ
    subjects.sort(key=len, reverse=True)

    for subj in subjects:
        pattern = f'^{re.escape(subj)}(は[、，]|が[、，])'
        m = re.match(pattern, text)
        if m:
            particle = m.group(1)
            rest = text[m.end():].strip()
            return subj, particle, rest

    # 汎用パターン: 文頭から「は、」「が、」まで
    m = re.match(r'^(.{2,40}?)(は[、，]|が[、，])\s*', text)
    if m:
        subj = m.group(1)
        particle = m.group(2)
        rest = text[m.end():].strip()
        return subj, particle, rest

    return None, None, text


def find_predicate(text):
    """文末の述語を検出"""
    predicates = [
        'しなければならない。', 'することができる。', 'してはならない。',
        'するものとする。', 'するものとし、', 'ならない。', 'できる。',
        'とする。', 'する。', 'ない。', 'られる。', 'れる。',
        '行う。', 'いう。', 'よる。',
        '目的とする。', '管掌する。', '制定する。',
        '適用しない。', '適用する。', '適用がある。',
        '支給しない。', '支給する。', '行わない。',
        '消滅する。', '準用する。',
    ]
    predicates.sort(key=len, reverse=True)

    for pred in predicates:
        if text.endswith(pred):
            return text[:-len(pred)], pred
    return text, ''


def remove_commentary(body, reference):
    """条文テキストから教科書的な解説部分を除去"""
    if not body:
        return body

    # 各条文ごとの解説パターン
    # 条文本文の後に続く解説は、通常以下のパターン:
    # 1. 同じ内容を「〜（補償）〜」の形で繰り返す
    # 2. ラベル（「目的」「受給資格者」等）だけの行
    # 3. 試験問題への言及（R06-07ウ等）

    lines = body
    # 末尾の単語ラベル除去（「目的」「給付基礎日額（原則）」等）
    lines = re.sub(r'(?<=。)[^\s。]{1,20}$', '', lines)

    # 試験問題参照除去
    lines = re.sub(r'R\d{2}-\d{2}[ァ-ヶ].*', '', lines)

    return lines.strip()


def decorate_text(text):
    """テキストにHTMLタグを付加（論理演算子、期間、条件）"""
    t = esc(text)
    t = logic_wrap(t)
    t = period_wrap(t)
    return t


# ========================================
# 手動オーバーライド（複雑な条文用）
# ========================================

MANUAL_OVERRIDES = {}


def override(ref, html):
    MANUAL_OVERRIDES[ref] = html


# --- 法1条: 目的 ---
override('法1条', '''<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">労働者災害補償保険</span>は、</div><ul class="condition-list"><li>業務上の事由、</li><li>事業主が同一人でない2以上の事業に使用される労働者（以下「複数事業労働者」という。）の2以上の事業の業務を要因とする事由</li><li class="logic-item"><span class="logic">又は</span></li><li>通勤による労働者の負傷、疾病、障害、死亡等</li></ul>に対して迅速<span class="logic">かつ</span>公正な保護をするため、<br>必要な保険給付を行い、<br>あわせて、<ul class="condition-list"><li>業務上の事由、複数事業労働者の2以上の事業の業務を要因とする事由<span class="logic">又は</span>通勤により負傷し、<span class="logic">又は</span>疾病にかかった労働者の社会復帰の促進、</li><li>当該労働者<span class="logic">及び</span>その遺族の援護、</li><li>労働者の安全<span class="logic">及び</span>衛生の確保等</li></ul>を図り、もって労働者の福祉の増進に寄与することを<span class="predicate">目的とする。</span></div></div>''')

# --- 法2条の2: 事業内容 ---
override('法2条の2', '''<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">労働者災害補償保険</span>は、</div><span class="condition">第1条の目的を達成するため</span>、<ul class="condition-list"><li>業務上の事由、</li><li>複数事業労働者の2以上の事業の業務を要因とする事由</li><li class="logic-item"><span class="logic">又は</span></li><li>通勤による労働者の負傷、疾病、障害、死亡等</li></ul>に関して保険給付を行うほか、<br>社会復帰促進等事業を<span class="predicate">行うことができる。</span></div></div>''')

# --- 法2条: 管掌 ---
override('法2条', '''<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">労働者災害補償保険</span>は、</div><div class="predicate-line"><span class="subject">政府</span>が、これを<span class="predicate">管掌する。</span></div></div></div>''')

# --- 則1条: 事務管轄 ---
override('則1条', '''<div class="law-body"><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">労働者災害補償保険等関係事務</span>は、</div><div class="predicate-line">厚生労働省労働基準局長の指揮監督を受けて、<br>所轄都道府県労働局長が<span class="predicate">行う。</span></div></div><div class="exception-section"><div class="exception-keyword"><span class="exception">ただし、</span></div>次の各号に掲げる場合は、当該各号に定める者を所轄都道府県労働局長とする。<ul class="condition-list"><li>1. 事業場が2以上の都道府県労働局の管轄区域にまたがる場合<br>→ その事業の主たる事務所の所在地を管轄する都道府県労働局長</li><li>2. 当該事務が複数業務要因災害に関するものである場合<br>→ 生計維持事業の主たる事務所の所在地を管轄する都道府県労働局長</li></ul></div><div class="principle-section"><span class="item-number">第3項</span><div class="subject-line"><span class="subject">労働者災害補償保険等関係事務</span>のうち、</div><ul class="condition-list"><li>保険給付（二次健康診断等給付を除く。）</li><li class="logic-item"><span class="logic">並びに</span></li><li>社会復帰促進等事業のうち労災就学等援護費<span class="logic">及び</span>特別支給金の支給</li><li class="logic-item"><span class="logic">並びに</span></li><li>厚生労働省労働基準局長が定める給付に関する事務</li></ul><div class="predicate-line">は、都道府県労働局長の指揮監督を受けて、<br>所轄労働基準監督署長が<span class="predicate">行う。</span></div></div></div>''')

# --- 法5条: 政令・省令の制定 ---
override('法5条', '''<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">労災保険法に基づく政令<span class="logic">及び</span>厚生労働省令<span class="logic">並びに</span>徴収法に基づく政令<span class="logic">及び</span>厚生労働省令</span>（労働者災害補償保険事業に係るものに限る。）は、</div><div class="predicate-line">その草案について、労働政策審議会の意見を聞いて、これを<span class="predicate">制定する。</span></div></div></div>''')

# --- 法3条: 適用事業 ---
override('法3条', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">労災保険法</span>においては、</div><div class="predicate-line">労働者を使用する事業を<span class="predicate">適用事業とする。</span></div></div></div>''')

# --- 法7条1項: 業務災害の定義 ---
override('法7条1項', '''<div class="law-body"><div class="principle-section"><div class="subject-line">1号 「<span class="subject">業務災害</span>」とは、</div><div class="predicate-line">労働者の業務上の負傷、疾病、障害<span class="logic">又は</span>死亡を<span class="predicate">いう。</span></div></div></div>''')

# --- 法7条: 通勤の定義 ---
override('法7条', '''<div class="law-body"><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">通勤</span>とは、</div><ul class="condition-list"><li><span class="subject">労働者</span>が、就業に関し、</li><li>次に掲げる移動を、</li><li>合理的な経路<span class="logic">及び</span>方法により行うことをいい、</li></ul><div class="predicate-line">業務の性質を有するものを<span class="predicate">除くものとする。</span></div></div></div>''')

# --- 法22条: 療養給付 ---
override('法22条', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">療養給付</span>は、</div><ul class="condition-list"><li><span class="condition"><span class="subject">労働者</span>が通勤により負傷し、<span class="logic">又は</span>疾病にかかった場合</span>に、</li><li>当該労働者に対し、</li><li>その請求に基づいて</li></ul><div class="predicate-line"><span class="predicate">行う。</span></div></div></div>''')

# --- 則18条の4 ---
override('則18条の4', '''<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">第22条第1項の厚生労働省令で定める疾病</span>は、</div><div class="predicate-line">通勤による負傷に起因する疾病その他通勤に起因することの明らかな疾病<span class="predicate">とする。</span></div></div></div>''')

# --- 法8条: 給付基礎日額 ---
override('法8条', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">給付基礎日額</span>は、</div><div class="predicate-line">労働基準法第12条の平均賃金に相当する額<span class="predicate">とする。</span></div></div><div class="principle-section">この場合において、<br>同条第1項の平均賃金を算定すべき事由の発生した日は、<ul class="condition-list"><li>第7条第1項第1号から第3号までに規定する負傷<span class="logic">若しくは</span>死亡の原因である事故が発生した日</li><li class="logic-item"><span class="logic">又は</span></li><li>診断によって同項第1号から第3号までに規定する疾病の発生が確定した日</li></ul><div class="predicate-line">（以下「算定事由発生日」という。）<span class="predicate">とする。</span></div></div></div>''')

# --- 法8条の5: 端数処理 ---
override('法8条の5', '''<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">給付基礎日額</span>に<span class="period">1円</span>未満の端数があるときは、</div><div class="predicate-line">これを<span class="period">1円</span>に<span class="predicate">切り上げるものとする。</span></div></div></div>''')

# --- 則9条: 給付基礎日額の算定 ---
override('則9条', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">第8条第2項の規定による給付基礎日額の算定</span>は、</div><div class="predicate-line"><span class="subject">所轄労働基準監督署長</span>が、労災保険法施行規則第9条第1項各号に定めるところによって<span class="predicate">行う。</span></div></div></div>''')

# --- 則9条1項: 自動変更対象額 ---
override('則9条1項', '''<div class="law-body"><div class="principle-section"><span class="item-number">5号</span><span class="item-number">第1項</span><span class="condition">平均賃金相当額が自動変更対象額に満たない場合</span>には、<div class="predicate-line">自動変更対象額<span class="predicate">とする。</span></div></div></div>''')

# --- 法8条の2: 休業給付基礎日額（スライド制） ---
override('法8条の2', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">休業補償給付、複数事業労働者休業給付<span class="logic">又は</span>休業給付</span>（以下「休業補償給付等」という。）の額の算定の基礎として用いる給付基礎日額（以下「休業給付基礎日額」という。）については、</div>次に定めるところによる。<ul class="condition-list"><li>1. 2.に規定する休業補償給付等以外の休業補償給付等については、<br>第8条の規定により給付基礎日額として算定した額を休業給付基礎日額<span class="predicate">とする。</span></li><li>2. 四半期ごとの平均給与額が、算定事由発生日の属する四半期の平均給与額の<span class="period">100分の110</span>を超え、<span class="logic">又は</span><span class="period">100分の90</span>を下るに至った場合において、<br>その上昇し、<span class="logic">又は</span>低下するに至った四半期の翌々四半期に属する最初の日以後に支給すべき事由が生じた休業補償給付等については、<br>その上昇し、<span class="logic">又は</span>低下した比率を基準として厚生労働大臣が定める率を第8条の規定により給付基礎日額として算定した額に乗じて得た額を休業給付基礎日額<span class="predicate">とする。</span></li></ul></div></div>''')

# --- 法8条の2第1項: スライド制（再改定） ---
override('法8条の2第1項', '''<div class="law-body"><div class="principle-section"><span class="item-number">2号かっこ書</span><span class="condition">改定日額（スライド改定の規定により算定した額をいう。）を休業給付基礎日額とすることとされている場合</span>にあっては、<ul class="condition-list"><li>四半期ごとの平均給与額が、当該改定日額を休業補償給付等の額の算定の基礎として用いるべき最初の四半期の前々四半期の平均給与額の<span class="period">100分の110</span>を超え、<span class="logic">又は</span><span class="period">100分の90</span>を下るに至った場合において、</li><li>その上昇し、<span class="logic">又は</span>低下するに至った四半期の翌々四半期に属する最初の日以後に支給すべき事由が生じた休業補償給付等については、</li></ul><div class="predicate-line">その上昇し、<span class="logic">又は</span>低下した比率を基準として厚生労働大臣が定める率を当該改定日額に乗じて得た額を休業給付基礎日額<span class="predicate">とする。</span></div></div></div>''')

# --- 法8条の3: 年金給付基礎日額 ---
override('法8条の3', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">年金たる保険給付の額の算定の基礎として用いる給付基礎日額</span>（以下「年金給付基礎日額」という。）については、</div>次に定めるところによる。<ul class="condition-list"><li>1. 算定事由発生日の属する年度の翌々年度の<span class="period">7月</span>以前の分として支給する年金たる保険給付については、<br>第8条の規定により給付基礎日額として算定した額を年金給付基礎日額<span class="predicate">とする。</span></li><li>2. 算定事由発生日の属する年度の翌々年度の<span class="period">8月</span>以後の分として支給する年金たる保険給付については、<br>第8条の規定により給付基礎日額として算定した額に当該年金たる保険給付を支給すべき月の属する年度の前年度（当該月が4月から7月までの月に該当する場合にあっては、前々年度）の平均給与額を算定事由発生日の属する年度の平均給与額で除して得た率を基準として厚生労働大臣が定める率を乗じて得た額を年金給付基礎日額<span class="predicate">とする。</span></li></ul></div></div>''')

# --- 法8条の4: 一時金のスライド ---
override('法8条の4', '''<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">第8条の3第1項（年金給付基礎日額のスライド）の規定</span>は、</div><ul class="condition-list"><li>障害補償一時金<span class="logic">若しくは</span>遺族補償一時金、</li><li>複数事業労働者障害一時金<span class="logic">若しくは</span>複数事業労働者遺族一時金</li><li class="logic-item"><span class="logic">又は</span></li><li>障害一時金<span class="logic">若しくは</span>遺族一時金</li></ul><div class="predicate-line">の額の算定の基礎として用いる給付基礎日額について<span class="predicate">準用する。</span></div></div></div>''')

# --- 法12条の8: 業務災害と労基法の関係 ---
override('法12条の8', '''<div class="law-body"><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">業務災害に関する保険給付</span>（傷病補償年金<span class="logic">及び</span>介護補償給付を除く。）は、</div><ul class="condition-list"><li><span class="condition">労働基準法に規定する災害補償の事由<span class="logic">又は</span>船員法に規定する災害補償の事由（労働基準法に規定する災害補償の事由に相当する部分に限る。）が生じた場合</span>に、</li><li>補償を受けるべき労働者<span class="logic">若しくは</span>遺族<span class="logic">又は</span>葬祭を行う者に対し、</li><li>その請求に基づいて</li></ul><div class="predicate-line"><span class="predicate">行う。</span></div></div></div>''')

# --- 法13条: 療養補償給付 ---
override('法13条', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">療養補償給付</span>は、</div><div class="predicate-line">療養の給付<span class="predicate">とする。</span></div></div><div class="principle-section"><span class="item-number">第3項</span><div class="subject-line"><span class="subject">政府</span>は、</div><ul class="condition-list"><li><span class="condition">第1項の療養の給付をすることが困難な場合</span></li><li class="logic-item"><span class="logic">又は</span></li><li><span class="condition">療養の給付を受けないことについて労働者に相当の理由がある場合</span>には、</li></ul><div class="predicate-line">療養の給付に代えて療養の費用を支給<span class="predicate">することができる。</span></div></div></div>''')

# --- 則11条: 療養の給付の担当機関 ---
override('則11条', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">療養の給付</span>は、</div><ul class="condition-list"><li>社会復帰促進等事業として設置された病院<span class="logic">若しくは</span>診療所</li><li class="logic-item"><span class="logic">又は</span></li><li>都道府県労働局長の指定する病院<span class="logic">若しくは</span>診療所、薬局<span class="logic">若しくは</span>訪問看護事業者</li></ul><div class="predicate-line">において<span class="predicate">行う。</span></div></div></div>''')

# --- 則12条: 療養の給付の請求手続 ---
override('則12条', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">療養補償給付たる療養の給付を受けようとする者</span>は、</div>次に掲げる事項を記載した請求書を、<br>指定病院等を経由して所轄労働基準監督署長に<span class="predicate">提出しなければならない。</span><ul class="condition-list"><li>1. 労働者の氏名、生年月日<span class="logic">及び</span>住所</li><li>2. 事業の名称<span class="logic">及び</span>事業場の所在地</li><li>3. 負傷<span class="logic">又は</span>発病の年月日</li><li>4. 災害の原因<span class="logic">及び</span>発生状況</li><li>5. 療養の給付を受けようとする指定病院等の名称<span class="logic">及び</span>所在地</li><li>6. 労働者が複数事業労働者である場合は、その旨</li></ul></div><div class="principle-section"><span class="item-number">第2項</span>前項第3号<span class="logic">及び</span>第4号に掲げる事項については、<br>事業主（非災害の事業主を除く。）の証明を<span class="predicate">受けなければならない。</span></div><div class="principle-section"><span class="item-number">第3項</span><div class="subject-line"><span class="subject">療養（補償）給付たる療養の給付を受ける労働者</span>は、</div><span class="condition">当該療養の給付を受ける指定病院等を変更しようとするとき</span>は、<br>所定の事項を記載した届書を、新たに当該療養の給付を受けようとする指定病院等を経由して所轄労働基準監督署長に<span class="predicate">提出しなければならない。</span></div></div>''')

# --- 則12条の2: 療養の費用の請求 ---
override('則12条の2', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">療養補償給付たる療養の費用の支給を受けようとする者</span>は、</div>次に掲げる事項を記載した請求書を、<br>所轄労働基準監督署長に<span class="predicate">提出しなければならない。</span><ul class="condition-list"><li>1. 労働者の氏名、生年月日<span class="logic">及び</span>住所</li><li>2. 事業の名称<span class="logic">及び</span>事業場の所在地</li><li>3. 負傷<span class="logic">又は</span>発病の年月日</li><li>4. 災害の原因<span class="logic">及び</span>発生状況</li><li>5. 傷病名<span class="logic">及び</span>療養の内容</li><li>6. 療養に要した費用の額</li><li>7. 療養の給付を受けなかった理由</li><li>8. 労働者が複数事業労働者である場合は、その旨</li></ul></div><div class="exception-section"><div class="exception-keyword"><span class="exception">ただし、</span></div>当該者が指名施術所において治療を受ける場合にあっては、<br>当該請求書を、当該指名施術所を経由して所轄労働基準監督署長に提出<span class="predicate">することができる。</span></div></div>''')

# --- 法31条: 一部負担金 ---
override('法31条', '''<div class="law-body"><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">政府</span>は、</div><span class="subject">療養給付を受ける労働者</span>（厚生労働省令で定める者を除く。）から、<br><span class="period">200円</span>を超えない範囲内で厚生労働省令で定める額（<span class="period">200円</span>。健康保険法に規定する日雇特例被保険者である労働者については<span class="period">100円</span>。）を<br>一部負担金として<span class="predicate">徴収する。</span></div><div class="exception-section"><div class="exception-keyword"><span class="exception">ただし、</span></div>第22条の2第3項に規定により減額した休業給付の支給を受けた労働者については、<span class="exception">この限りでない。</span></div></div>''')

# --- 法22条の2: 一部負担金の控除 ---
override('法22条の2', '''<div class="law-body"><div class="principle-section"><span class="item-number">第3項</span><div class="subject-line"><span class="subject">療養給付を受ける労働者</span>（第31条第2項の厚生労働省令で定める者を除く。）に支給する休業給付であって最初に支給すべき事由の生じた日に係るものの額は、</div><div class="predicate-line">その額から第31条第2項の厚生労働省令で定める額（一部負担金）に相当する額を減じた額<span class="predicate">とする。</span></div></div></div>''')

# --- 法14条: 休業補償給付 ---
override('法14条', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">休業補償給付</span>は、</div><ul class="condition-list"><li><span class="subject">労働者</span>が業務上の負傷<span class="logic">又は</span>疾病による療養のため</li><li>労働することができないために</li><li>賃金を受けない日の</li></ul><div class="predicate-line">第<span class="period">4日</span>目から支給<span class="predicate">するものとする。</span></div></div></div>''')

# --- 法14条の2: 休業補償給付の不支給 ---
override('法14条の2', '''<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="condition"><span class="subject">労働者</span>が次の各号のいずれかに該当する場合</span>（厚生労働省令で定める場合に限る。）には、</div><div class="predicate-line"><span class="subject">休業補償給付</span>は、<span class="predicate">行わない。</span></div><ul class="condition-list"><li>1. 刑事施設、労役場その他これらに準ずる施設に拘禁されている場合</li><li>2. 少年院その他これに準ずる施設に収容されている場合</li></ul></div></div>''')

# --- 則18条の2: 傷病補償年金の支給決定 ---
override('則18条の2', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><span class="condition">業務上の事由により負傷し、<span class="logic">又は</span>疾病にかかった労働者が、当該負傷<span class="logic">又は</span>疾病に係る療養の開始後<span class="period">1年6箇月</span>を経過した日において傷病補償年金の支給要件のいずれにも該当するとき</span>、<br><span class="logic">又は</span>同日後同項各号のいずれにも該当することとなったときは、<div class="predicate-line"><span class="subject">所轄労働基準監督署長</span>は、当該労働者について傷病補償年金の支給の決定を<span class="predicate">しなければならない。</span></div></div></div>''')

# --- 法18条の2: 傷病等級の変更 ---
override('法18条の2', '''<div class="law-body"><div class="principle-section"><span class="condition"><span class="subject">傷病補償年金を受ける労働者</span>の当該障害の程度に変更があったため、新たに別表第1中の他の傷病等級に該当するに至った場合</span>には、<div class="subject-line"><span class="subject">政府</span>は、</div><ul class="condition-list"><li>新たに該当するに至った傷病等級に応ずる傷病補償年金を支給するものとし、</li><li>その後は、従前の傷病補償年金は、</li></ul><div class="predicate-line"><span class="predicate">支給しない。</span></div></div></div>''')

# --- 法19条: 解雇制限との関係 ---
override('法19条', '''<div class="law-body"><div class="principle-section"><span class="condition">業務上負傷し、<span class="logic">又は</span>疾病にかかった労働者が、当該負傷<span class="logic">又は</span>疾病に係る療養の開始後<span class="period">3年</span>を経過した日において傷病補償年金を受けている場合</span><br><span class="logic">又は</span>同日後において傷病補償年金を受けることとなった場合には、<br>労働基準法第19条第1項（解雇制限）の規定の適用については、<br><span class="subject">当該使用者</span>は、それぞれ、当該<span class="period">3年</span>を経過した日<span class="logic">又は</span>傷病補償年金を受けることとなった日において、<br>同法第81条の規定により打切補償を支払ったものと<span class="predicate">みなす。</span></div></div>''')

# --- 法15条: 障害補償給付 ---
override('法15条', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">障害補償給付</span>は、</div><div class="predicate-line">厚生労働省令で定める障害等級に応じ、<br>障害補償年金<span class="logic">又は</span>障害補償一時金<span class="predicate">とする。</span></div></div></div>''')

# --- 則14条: 障害等級の併合 ---
override('則14条', '''<div class="law-body"><div class="principle-section"><span class="item-number">第2項</span>別表第1に掲げる身体障害が2以上ある場合には、<br>重い方の身体障害の該当する障害等級<span class="predicate">による。</span></div><div class="principle-section"><span class="item-number">第3項</span>次の各号に掲げる場合には、<br>前2項の規定による障害等級をそれぞれ当該各号に掲げる等級だけ繰り上げた障害等級<span class="predicate">による。</span></div><div class="exception-section"><div class="exception-keyword"><span class="exception">ただし、</span></div>本文の規定による障害等級が第8級以下である場合において、<br>各の身体障害の該当する障害等級に応ずる障害補償給付の額の合算額が本文の規定による障害等級に応ずる障害補償給付の額に満たないときは、<br>その者に支給する障害補償給付は、<span class="exception">当該合算額による。</span></div></div>''')

# --- 法15条の2: 障害等級の変更 ---
override('法15条の2', '''<div class="law-body"><div class="principle-section"><span class="condition"><span class="subject">障害補償年金を受ける労働者</span>の当該障害の程度に変更があったため、新たに別表第1<span class="logic">又は</span>別表第2中の他の障害等級に該当するに至った場合</span>には、<div class="subject-line"><span class="subject">政府</span>は、</div><ul class="condition-list"><li>新たに該当するに至った障害等級に応ずる障害補償年金<span class="logic">又は</span>障害補償一時金を支給するものとし、</li><li>その後は、従前の障害補償年金は、</li></ul><div class="predicate-line"><span class="predicate">支給しない。</span></div></div></div>''')

# --- 附則59条: 障害補償年金前払一時金 ---
override('附則59条', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">政府</span>は、当分の間、</div><span class="condition">労働者が業務上負傷し、<span class="logic">又は</span>疾病にかかり、治ったとき身体に障害が存する場合</span>における当該障害に関しては、<br><span class="subject">障害補償年金を受ける権利を有する者</span>に対し、その請求に基づき、<br>保険給付として、障害補償年金前払一時金を<span class="predicate">支給する。</span></div></div>''')

# --- 附則58条: 障害補償年金差額一時金 ---
override('附則58条', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">政府</span>は、当分の間、</div><span class="condition">障害補償年金を受ける権利を有する者が死亡した場合</span>において、<br>その者に支給された当該障害補償年金の額<span class="logic">及び</span>当該障害補償年金に係る障害補償年金前払一時金の額の合計額が当該障害補償年金に係る障害等級に応じ所定の額に満たないときは、<br>その者の遺族に対し、その請求に基づき、<br>保険給付として、その差額に相当する額の障害補償年金差額一時金を<span class="predicate">支給する。</span></div></div>''')

# --- 附則58条5項: 受給資格の欠格 ---
override('附則58条5項', '''<div class="law-body"><div class="principle-section"><ul class="condition-list"><li>1. <span class="subject">労働者を故意に死亡させた者</span>は、<br>障害補償年金差額一時金を受けることができる遺族と<span class="predicate">しない。</span></li><li>2. <span class="subject">労働者の死亡前に、当該労働者の死亡によって障害補償年金差額一時金を受けることができる先順位<span class="logic">又は</span>同順位の遺族となるべき者を故意に死亡させた者</span>は、<br>障害補償年金差額一時金を受けることができる遺族と<span class="predicate">しない。</span></li></ul></div></div>''')

# --- 法19条の2: 介護補償給付の額 ---
override('法19条の2', '''<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">介護補償給付</span>は、</div><ul class="condition-list"><li>月を単位として支給するものとし、</li><li>その月額は、常時<span class="logic">又は</span>随時介護を受ける場合に通常要する費用を考慮して</li></ul><div class="predicate-line">厚生労働大臣が定める額<span class="predicate">とする。</span></div></div></div>''')

# --- 則18条の3の5: 介護補償給付の請求 ---
override('則18条の3の5', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">障害補償年金を受ける権利を有する者が介護補償給付を請求する場合</span>における当該請求は、</div><div class="predicate-line">当該障害補償年金の請求と同時に、<span class="logic">又は</span>請求をした後に<span class="predicate">行わなければならない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">介護補償給付の支給を受けようとする者</span>は、</div><div class="predicate-line">所定事項を記載した請求書を、所轄労働基準監督署長に<span class="predicate">提出しなければならない。</span></div></div></div>''')

# --- 法16条: 遺族補償給付の種類 ---
override('法16条', '''<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">遺族補償給付</span>は、</div><div class="predicate-line">遺族補償年金<span class="logic">又は</span>遺族補償一時金<span class="predicate">とする。</span></div></div></div>''')

# --- 法16条の2: 遺族補償年金の受給資格者 ---
override('法16条の2', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">遺族補償年金を受けることができる遺族</span>は、</div><ul class="condition-list"><li>労働者の配偶者、子、父母、孫、祖父母<span class="logic">及び</span>兄弟姉妹であって、</li><li>労働者の死亡の当時その収入によって生計を維持していたもの</li></ul><div class="predicate-line"><span class="predicate">とする。</span></div></div><div class="exception-section"><div class="exception-keyword"><span class="exception">ただし、</span></div>妻（婚姻の届出をしていないが、事実上婚姻関係と同様の事情にあった者を含む。）以外の者にあっては、<br>労働者の死亡の当時次の各号に掲げる要件に該当した場合に<span class="exception">限るものとする。</span></div></div>''')

# --- 則14条の4: 生計維持の認定 ---
override('則14条の4', '''<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">労働者の死亡の当時その収入によって生計を維持していたことの認定</span>は、</div><ul class="condition-list"><li>当該労働者との同居の事実の有無、</li><li>当該労働者以外の扶養義務者の有無</li><li>その他必要な事項</li></ul><div class="predicate-line">を基礎として厚生労働省労働基準局長が定める基準によって<span class="predicate">行う。</span></div></div></div>''')

# --- 法16条の9: 遺族補償給付の欠格 ---
override('法16条の9', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">労働者を故意に死亡させた者</span>は、</div><div class="predicate-line">遺族補償給付を受けることができる遺族と<span class="predicate">しない。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">労働者の死亡前に、当該労働者の死亡によって遺族補償年金を受けることができる先順位<span class="logic">又は</span>同順位の遺族となるべき者を故意に死亡させた者</span>は、</div><div class="predicate-line">遺族補償年金を受けることができる遺族と<span class="predicate">しない。</span></div></div><div class="principle-section"><span class="item-number">第4項</span><div class="subject-line"><span class="subject">遺族補償年金を受けることができる遺族</span>が、</div>遺族補償年金を受けることができる先順位<span class="logic">又は</span>同順位の他の遺族を故意に死亡させたときは、<br>その者は、遺族補償年金を受けることができる遺族で<span class="predicate">なくなる。</span><br>この場合において、その者が遺族補償年金を受ける権利を有する者であるときは、その権利は、<span class="predicate">消滅する。</span></div></div>''')

# --- 法16条の3: 遺族補償年金の額 ---
override('法16条の3', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">遺族補償年金の額</span>は、</div><div class="predicate-line">別表第1に規定する額<span class="predicate">とする。</span></div></div></div>''')

# --- 法16条の5: 遺族補償年金の支給停止 ---
override('法16条の5', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><span class="condition"><span class="subject">遺族補償年金を受ける権利を有する者</span>の所在が<span class="period">1年</span>以上明らかでない場合</span>には、<br>当該遺族補償年金は、<ul class="condition-list"><li>同順位者があるときは同順位者の、</li><li>同順位者がないときは次順位者の申請によって、</li></ul>その所在が明らかでない間、その支給を<span class="predicate">停止する。</span><br>この場合において、同順位者がないときは、その間、次順位者を先順位者とする。</div><div class="principle-section"><span class="item-number">第2項</span>前項の規定により遺族補償年金の支給を停止された遺族は、<br>いつでも、その支給の停止の解除を申請<span class="predicate">することができる。</span></div><div class="principle-section"><span class="item-number">第3項</span>第1項の規定により遺族補償年金の支給が停止され、<span class="logic">又は</span>前項の規定によりその停止が解除されたときは、<br>その支給が停止され、<span class="logic">又は</span>その停止が解除された月の翌月から、<br>遺族補償年金の額を<span class="predicate">改定する。</span></div></div>''')

# --- 法16条の4: 遺族補償年金の失権 ---
override('法16条の4', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">遺族補償年金を受ける権利</span>は、</div>その権利を有する遺族が次の各号の一に該当するに至ったときは、<span class="predicate">消滅する。</span><br>この場合において、同順位者がなくて後順位者があるときは、次順位者に遺族補償年金を支給する。<ul class="condition-list"><li>1. 死亡したとき。</li><li>2. 婚姻（届出をしていないが、事実上婚姻関係と同様の事情にある場合を含む。）をしたとき。</li><li>3. 直系血族<span class="logic">又は</span>直系姻族以外の者の養子（届出をしていないが、事実上養子縁組関係と同様の事情にある者を含む。）となったとき。</li><li>4. 離縁によって、死亡した労働者との親族関係が終了したとき。</li><li>5. 子、孫<span class="logic">又は</span>兄弟姉妹については、<span class="period">18歳</span>に達した日以後の最初の3月31日が終了したとき（労働者の死亡の時から引き続き厚生労働省令で定める障害の状態にあるときを除く。）。</li><li>6. 厚生労働省令で定める障害の状態にある夫、子、父母、孫、祖父母<span class="logic">又は</span>兄弟姉妹については、その事情がなくなったとき（夫、父母<span class="logic">又は</span>祖父母については、労働者の死亡の当時<span class="period">60歳</span>以上であったとき、子<span class="logic">又は</span>孫については、<span class="period">18歳</span>に達する日以後の最初の3月31日までの間にあるとき、兄弟姉妹については、<span class="period">18歳</span>に達する日以後の最初の3月31日までの間にあるか<span class="logic">又は</span>労働者の死亡の当時<span class="period">60歳</span>以上であったときを除く。）。</li></ul></div><div class="principle-section"><span class="item-number">第2項</span>遺族補償年金を受けることができる遺族が前項各号の一に該当するに至ったときは、<br>その者は、遺族補償年金を受けることができる遺族で<span class="predicate">なくなる。</span></div></div>''')

# --- 附則60条: 遺族補償年金前払一時金 ---
override('附則60条', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">政府</span>は、当分の間、</div><span class="condition">労働者が業務上の事由により死亡した場合</span>における当該死亡に関しては、<br><span class="subject">遺族補償年金を受ける権利を有する遺族</span>に対し、その請求に基づき、<br>保険給付として、遺族補償年金前払一時金を<span class="predicate">支給する。</span></div></div>''')

# --- 法16条の6: 遺族補償一時金の支給要件 ---
override('法16条の6', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">遺族補償一時金</span>は、</div>次の場合に<span class="predicate">支給する。</span><ul class="condition-list"><li>1. 労働者の死亡の当時遺族補償年金を受けることができる遺族がないとき。</li><li>2. 遺族補償年金を受ける権利を有する者の権利が消滅した場合において、<br>他に当該遺族補償年金を受けることができる遺族がなく、<span class="logic">かつ</span>、<br>当該労働者の死亡に関し支給された遺族補償年金の額<span class="logic">及び</span>遺族補償年金前払一時金の額の合計額が所定の遺族補償一時金の額に満たないとき。</li></ul></div></div>''')

# --- 法16条の7: 遺族補償一時金の受給者 ---
override('法16条の7', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">遺族補償一時金を受けることができる遺族</span>は、</div>次の各号に掲げる者<span class="predicate">とする。</span><ul class="condition-list"><li>1. 配偶者</li><li>2. 労働者の死亡の当時その収入によって生計を維持していた子、父母、孫<span class="logic">及び</span>祖父母</li><li>3. 労働者の死亡の当時その収入によって生計を維持していなかった子、父母、孫<span class="logic">及び</span>祖父母<span class="logic">並びに</span>兄弟姉妹</li></ul></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">遺族補償一時金を受けるべき遺族の順位</span>は、</div><div class="predicate-line">前項各号の順序により、同項第2号<span class="logic">及び</span>第3号に掲げる者のうちにあっては、それぞれ、当該各号に掲げる順序<span class="predicate">による。</span></div></div></div>''')

# --- 則17条の2: 葬祭料の請求手続 ---
override('則17条の2', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">葬祭料の支給を受けようとする者</span>は、</div>次に掲げる事項を記載した請求書を、<br>所轄労働基準監督署長に<span class="predicate">提出しなければならない。</span><ul class="condition-list"><li>1. 死亡した労働者の氏名<span class="logic">及び</span>生年月日</li><li>2. 請求人の氏名、住所<span class="logic">及び</span>死亡した労働者との関係</li><li>3. 事業の名称<span class="logic">及び</span>事業場の所在地</li><li>4. 負傷<span class="logic">又は</span>発病<span class="logic">及び</span>死亡の年月日</li><li>5. 災害の原因<span class="logic">及び</span>発生状況</li><li>6. 平均賃金</li><li>7. 死亡した労働者が複数事業労働者である場合は、その旨</li></ul></div></div>''')

# --- 法20条の3: 複数事業労働者療養給付 ---
override('法20条の3', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">複数事業労働者療養給付</span>は、</div><span class="condition"><span class="subject">複数事業労働者</span>がその従事する2以上の事業の業務を要因として負傷し、<span class="logic">又は</span>疾病にかかった場合</span>に、<br>当該複数事業労働者に対し、その請求に基づいて<span class="predicate">行う。</span></div><div class="principle-section"><span class="item-number">第2項</span>第13条（療養補償給付）の規定は、複数事業労働者療養給付について<span class="predicate">準用する。</span></div></div>''')

# --- 法20条の4: 複数事業労働者休業給付 ---
override('法20条の4', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">複数事業労働者休業給付</span>は、</div><span class="condition"><span class="subject">複数事業労働者</span>がその従事する2以上の事業の業務を要因とする負傷<span class="logic">又は</span>疾病による療養のため労働することができないために賃金を受けない場合</span>に、<br>当該複数事業労働者に対し、その請求に基づいて<span class="predicate">行う。</span></div><div class="principle-section"><span class="item-number">第2項</span>第14条（休業補償給付）<span class="logic">及び</span>第14条の2（休業補償の不支給）の規定は、複数事業労働者休業給付について<span class="predicate">準用する。</span></div></div>''')

# --- 法20条の5: 複数事業労働者障害給付 ---
override('法20条の5', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">複数事業労働者障害給付</span>は、</div><span class="condition"><span class="subject">複数事業労働者</span>がその従事する2以上の事業の業務を要因として負傷し、<span class="logic">又は</span>疾病にかかり、治ったとき身体に障害が存する場合</span>に、<br>当該複数事業労働者に対し、その請求に基づいて<span class="predicate">行う。</span></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">複数事業労働者障害給付</span>は、</div><div class="predicate-line">第15条第1項の厚生労働省令で定める障害等級に応じ、<br>複数事業労働者障害年金<span class="logic">又は</span>複数事業労働者障害一時金<span class="predicate">とする。</span></div></div><div class="principle-section"><span class="item-number">第3項</span>第15条第2項（障害補償年金<span class="logic">又は</span>障害補償一時金の額）<span class="logic">及び</span>第15条の2（障害等級の変更）の規定は、複数事業労働者障害給付について<span class="predicate">準用する。</span></div></div>''')

# --- 附則60条の3: 複数事業労働者障害年金前払一時金 ---
override('附則60条の3', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">政府</span>は、当分の間、</div><span class="condition">複数事業労働者がその従事する2以上の事業の業務を要因として負傷し、<span class="logic">又は</span>疾病にかかり、治ったとき身体に障害が存する場合</span>における当該障害に関しては、<br><span class="subject">複数事業労働者障害年金を受ける権利を有する者</span>に対し、その請求に基づき、<br>保険給付として、複数事業労働者障害年金前払一時金を<span class="predicate">支給する。</span></div><div class="principle-section"><span class="item-number">第3項</span>第59条第3項（障害補償年金の支給停止）、第4項（障害補償年金前払一時金の時効）<span class="logic">及び</span>第6項（20歳前傷病による障害基礎年金等の不支給）の規定は、<br>複数事業労働者障害年金前払一時金について<span class="predicate">準用する。</span></div></div>''')

# --- 附則60条の2: 複数事業労働者障害年金差額一時金 ---
override('附則60条の2', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">政府</span>は、当分の間、</div><span class="condition">複数事業労働者障害年金を受ける権利を有する者が死亡した場合</span>において、<br>その者に支給された当該複数事業労働者障害年金の額<span class="logic">及び</span>当該複数事業労働者障害年金に係る複数事業労働者障害年金前払一時金の額の合計額が所定の額に満たないときは、<br>その者の遺族に対し、その請求に基づき、<br>保険給付として、その差額に相当する額の複数事業労働者障害年金差額一時金を<span class="predicate">支給する。</span></div><div class="principle-section"><span class="item-number">第2項</span>第16条の3第2項、第16条の9第1項<span class="logic">及び</span>第2項<span class="logic">並びに</span>第58条第2項<span class="logic">及び</span>第3項の規定は、<br>複数事業労働者障害年金差額一時金について<span class="predicate">準用する。</span></div></div>''')

# --- 法20条の6: 複数事業労働者遺族給付 ---
override('法20条の6', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">複数事業労働者遺族給付</span>は、</div><span class="condition"><span class="subject">複数事業労働者</span>がその従事する2以上の事業の業務を要因として死亡した場合</span>に、<br>当該複数事業労働者の遺族に対し、その請求に基づいて<span class="predicate">行う。</span></div></div>''')

# --- 附則60条の4: 複数事業労働者遺族年金前払一時金 ---
override('附則60条の4', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">政府</span>は、当分の間、</div><span class="condition">複数事業労働者がその従事する2以上の事業の業務を要因として死亡した場合</span>における当該死亡に関しては、<br><span class="subject">複数事業労働者遺族年金を受ける権利を有する遺族</span>に対し、その請求に基づき、<br>保険給付として、複数事業労働者遺族年金前払一時金を<span class="predicate">支給する。</span></div><div class="principle-section"><span class="item-number">第4項</span>第60条第3項（遺族補償年金の支給停止）、第5項（遺族補償年金前払一時金の時効）<span class="logic">及び</span>第7項の規定は、<br>複数事業労働者遺族年金前払一時金について<span class="predicate">準用する。</span></div></div>''')

# --- 法20条の7: 複数事業労働者葬祭給付 ---
override('法20条の7', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">複数事業労働者葬祭給付</span>は、</div><span class="condition"><span class="subject">複数事業労働者</span>がその従事する2以上の事業の業務を要因として死亡した場合</span>に、<br>葬祭を行う者に対し、その請求に基づいて<span class="predicate">行う。</span></div><div class="principle-section"><span class="item-number">第2項</span>第17条（葬祭料の額）の規定は、複数事業労働者葬祭給付について<span class="predicate">準用する。</span></div></div>''')

# --- 法20条の8: 複数事業労働者傷病年金 ---
override('法20条の8', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">複数事業労働者傷病年金</span>は、</div><span class="condition"><span class="subject">複数事業労働者</span>がその従事する2以上の事業の業務を要因として負傷し、<span class="logic">又は</span>疾病にかかった場合</span>に、<br>当該負傷<span class="logic">又は</span>疾病に係る療養の開始後<span class="period">1年6箇月</span>を経過した日において次の各号のいずれにも該当するとき、<span class="logic">又は</span>同日後次の各号のいずれにも該当することとなったときに、<br>その状態が継続している間、当該複数事業労働者に対して<span class="predicate">支給する。</span><ul class="condition-list"><li>1. 当該負傷<span class="logic">又は</span>疾病が治っていないこと。</li><li>2. 当該負傷<span class="logic">又は</span>疾病による障害の程度が厚生労働省令で定める傷病等級に該当すること。</li></ul></div><div class="principle-section"><span class="item-number">第2項</span>第18条（傷病補償年金の額）、第18条の2（傷病等級の変更）の規定は、<br>複数事業労働者傷病年金について<span class="predicate">準用する。</span></div></div>''')

# --- 法20条の9: 複数事業労働者介護給付 ---
override('法20条の9', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">複数事業労働者介護給付</span>は、</div><span class="subject">複数事業労働者障害年金<span class="logic">又は</span>複数事業労働者傷病年金を受ける権利を有する複数事業労働者</span>が、<br>その受ける権利を有する年金の支給事由となる障害であって厚生労働省令で定める程度のものにより、<br>常時<span class="logic">又は</span>随時介護を要する状態にあり、<span class="logic">かつ</span>、常時<span class="logic">又は</span>随時介護を受けているときに、<br>当該介護を受けている間（次に掲げる間を除く。）、当該複数事業労働者に対し、その請求に基づいて<span class="predicate">行う。</span><ul class="condition-list"><li>1. 障害者総合支援法に規定する障害者支援施設に入所している間（生活介護を受けている場合に限る。）</li><li>2. 障害者支援施設に準ずる施設として厚生労働大臣が定めるものに入所している間</li><li>3. 病院<span class="logic">又は</span>診療所に入院している間</li></ul></div><div class="principle-section"><span class="item-number">第2項</span>第19条の2（介護補償給付の額）の規定は、複数事業労働者介護給付について<span class="predicate">準用する。</span></div></div>''')

# --- 法26条: 二次健康診断等給付 ---
override('法26条', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">二次健康診断等給付</span>は、</div><span class="condition">労働安全衛生法第66条第1項の規定による健康診断<span class="logic">又は</span>当該健康診断に係る同条第5項ただし書の規定による労働者指定医による健康診断のうち、直近のもの（以下「一次健康診断」という。）において、</span><ul class="condition-list"><li>血圧検査、</li><li>血液検査</li><li>その他業務上の事由による脳血管疾患<span class="logic">及び</span>心臓疾患の発生にかかわる身体の状態に関する検査であって、厚生労働省令で定めるもの</li></ul>が行われた場合において、<br>当該検査を受けた労働者がそのいずれの項目にも異常の所見があると診断されたときに、<br>当該労働者（当該一次健康診断の結果その他の事情により既に脳血管疾患<span class="logic">又は</span>心臓疾患の症状を有すると認められるものを除く。）に対し、<br>その請求に基づいて<span class="predicate">行う。</span></div></div>''')

# --- 則11条の3: 二次健康診断等給付の実施機関 ---
override('則11条の3', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">二次健康診断等給付</span>は、</div><ul class="condition-list"><li>社会復帰促進等事業として設置された病院<span class="logic">若しくは</span>診療所</li><li class="logic-item"><span class="logic">又は</span></li><li>都道府県労働局長の指定する病院<span class="logic">若しくは</span>診療所</li></ul><div class="predicate-line">において<span class="predicate">行う。</span></div></div></div>''')

# --- 則18条の19: 二次健康診断等給付の請求 ---
override('則18条の19', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">二次健康診断等給付を受けようとする者</span>は、</div><div class="predicate-line">所定の事項を記載した請求書を、<br>当該二次健康診断等給付を受けようとする健診給付病院等を経由して所轄都道府県労働局長に<span class="predicate">提出しなければならない。</span></div></div></div>''')

# --- 法9条: 年金給付の支給期間 ---
override('法9条', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">年金たる保険給付の支給</span>は、</div><div class="predicate-line">支給すべき事由が生じた月の翌月から始め、<br>支給を受ける権利が消滅した月で<span class="predicate">終わるものとする。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">年金たる保険給付</span>は、</div><span class="condition">その支給を停止すべき事由が生じたとき</span>は、<br>その事由が生じた月の翌月からその事由が消滅した月までの間は、<span class="predicate">支給しない。</span></div><div class="principle-section"><span class="item-number">第3項</span><div class="subject-line"><span class="subject">年金たる保険給付</span>は、</div>毎年<span class="period">2月、4月、6月、8月、10月及び12月</span>の6期に、<br>それぞれその前月分までを<span class="predicate">支払う。</span></div><div class="exception-section"><div class="exception-keyword"><span class="exception">ただし、</span></div>支給を受ける権利が消滅した場合におけるその期の年金たる保険給付は、<br>支払期月でない月であっても、<span class="exception">支払うものとする。</span></div></div>''')

# --- 法10条: 死亡の推定 ---
override('法10条', '''<div class="law-body"><div class="principle-section"><span class="condition">船舶が沈没し、転覆し、滅失し、<span class="logic">若しくは</span>行方不明となった際現にその船舶に乗っていた労働者<span class="logic">若しくは</span>船舶に乗っていてその船舶の航行中に行方不明となった労働者の生死が<span class="period">3箇月</span>間わからない場合</span><br><span class="logic">又は</span>これらの労働者の死亡が<span class="period">3箇月</span>以内に明らかとなり、<span class="logic">かつ</span>、その死亡の時期がわからない場合には、<br>遺族補償給付、葬祭料、遺族給付<span class="logic">及び</span>葬祭給付の支給に関する規定の適用については、<br>その船舶が沈没し、転覆し、滅失し、<span class="logic">若しくは</span>行方不明となった日<span class="logic">又は</span>労働者が行方不明となった日に、<br>当該労働者は、死亡したものと<span class="predicate">推定する。</span><br><br>航空機についても、<span class="predicate">同様とする。</span></div></div>''')

# --- 法11条: 未支給の保険給付 ---
override('法11条', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><span class="condition">労災保険法に基づく保険給付を受ける権利を有する者が死亡した場合</span>において、<br>その死亡した者に支給すべき保険給付でまだその者に支給しなかったものがあるときは、<ul class="condition-list"><li>その者の配偶者（婚姻の届出をしていないが、事実上婚姻関係と同様の事情にあった者を含む。）、</li><li>子、父母、孫、祖父母<span class="logic">又は</span>兄弟姉妹であって、</li><li>その者の死亡の当時その者と生計を同じくしていたもの</li></ul>（遺族補償年金については当該遺族補償年金を受けることができる他の遺族）は、<br>自己の名で、その未支給の保険給付の支給を<span class="predicate">請求することができる。</span></div></div>''')

# --- 法12条の5: 退職後の給付 ---
override('法12条の5', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">保険給付を受ける権利</span>は、</div><div class="predicate-line">労働者の退職によって変更されることは<span class="predicate">ない。</span></div></div></div>''')

# --- 法12条の6: 非課税 ---
override('法12条の6', '''<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">租税その他の公課</span>は、</div><div class="predicate-line">保険給付として支給を受けた金品を標準として課することは<span class="predicate">できない。</span></div></div></div>''')

# --- 法12条の7: 届出義務 ---
override('法12条の7', '''<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">保険給付を受ける権利を有する者</span>は、</div><ul class="condition-list"><li>政府に対して、保険給付に関し必要な厚生労働省令で定める事項を届け出、</li><li class="logic-item"><span class="logic">又は</span></li><li>保険給付に関し必要な厚生労働省令で定める書類その他の物件を提出</li></ul><div class="predicate-line"><span class="predicate">しなければならない。</span></div></div></div>''')

# --- 則21条: 定期報告書 ---
override('則21条', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">年金たる保険給付の受給権者</span>は、</div>毎年、厚生労働大臣が指定する日（以下「指定日」という。）までに、<br>所定事項を記載した報告書を、所轄労働基準監督署長に<span class="predicate">提出しなければならない。</span></div><div class="exception-section"><div class="exception-keyword"><span class="exception">ただし、</span></div><ul class="condition-list"><li>所轄労働基準監督署長があらかじめその必要がないと認めて通知したとき</li><li class="logic-item"><span class="logic">又は</span></li><li>厚生労働大臣が番号利用法第22条第1項の規定により当該報告書と同一の内容を含む利用特定個人情報の提供を受けることができるとき</li></ul>は、<span class="exception">この限りでない。</span></div></div>''')

# --- 法12条: 内払処理 ---
override('法12条', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項前段</span><span class="condition">年金たる保険給付の支給を停止すべき事由が生じたにもかかわらず、その停止すべき期間の分として年金たる保険給付が支払われたとき</span>は、<br>その支払われた年金たる保険給付は、<br>その後に支払うべき年金たる保険給付の内払と<span class="predicate">みなすことができる。</span></div></div>''')

# --- 法12条の2: 過誤払の充当 ---
override('法12条の2', '''<div class="law-body"><div class="principle-section"><span class="condition">年金たる保険給付を受ける権利を有する者が死亡したためその支給を受ける権利が消滅したにもかかわらず、その死亡の日の属する月の翌月以後の分として当該年金たる保険給付の過誤払が行われた場合</span>において、<br>当該過誤払による返還金に係る債権（以下「返還金債権」という。）に係る債務の弁済をすべき者に支払うべき保険給付があるときは、<br>当該保険給付の支払金の金額を当該過誤払による返還金債権の金額に<span class="predicate">充当することができる。</span></div></div>''')

# --- 法12条の2の2: 故意による不支給 ---
override('法12条の2の2', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><span class="condition"><span class="subject">労働者</span>が、故意に負傷、疾病、障害<span class="logic">若しくは</span>死亡<span class="logic">又は</span>その直接の原因となった事故を生じさせたとき</span>は、<div class="subject-line"><span class="subject">政府</span>は、</div><div class="predicate-line">保険給付を<span class="predicate">行わない。</span></div></div></div>''')

# --- 法47条の3: 支払の一時差止め ---
override('法47条の3', '''<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">政府</span>は、</div><span class="condition"><span class="subject">保険給付を受ける権利を有する者</span>が、正当な理由がなくて、<ul class="condition-list"><li>第12条の7の規定による届出をせず、<span class="logic">若しくは</span>書類その他の物件の提出をしないとき、</li><li class="logic-item"><span class="logic">又は</span></li><li>第47条<span class="logic">及び</span>第47条の2（労働者<span class="logic">及び</span>受給者の報告、出頭等<span class="logic">及び</span>受診命令）の規定による命令に従わないとき</span>は、</li></ul><div class="predicate-line">保険給付の支払を一時差し止めることが<span class="predicate">できる。</span></div></div></div>''')

# --- 法12条の3: 不正受給の費用徴収 ---
override('法12条の3', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><span class="condition">偽りその他不正の手段により保険給付を受けた者があるとき</span>は、<div class="subject-line"><span class="subject">政府</span>は、</div><div class="predicate-line">その保険給付に要した費用に相当する金額の全部<span class="logic">又は</span>一部をその者から徴収<span class="predicate">することができる。</span></div></div><div class="principle-section"><span class="item-number">第2項</span>前項の場合において、<span class="condition"><span class="subject">事業主</span>が虚偽の報告<span class="logic">又は</span>証明をしたためその保険給付が行なわれたものであるとき</span>は、<div class="subject-line"><span class="subject">政府</span>は、</div><div class="predicate-line">その事業主に対し、保険給付を受けた者と連帯して前項の徴収金を納付すべきことを<span class="predicate">命ずることができる。</span></div></div></div>''')

# --- 法12条の4: 第三者行為災害 ---
override('法12条の4', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">政府</span>は、</div><span class="condition">保険給付の原因である事故が第三者の行為によって生じた場合</span>において、保険給付をしたときは、<br>その給付の価額の限度で、<br>保険給付を受けた者が第三者に対して有する損害賠償の請求権を<span class="predicate">取得する。</span></div><div class="principle-section"><span class="item-number">第2項</span>前項の場合において、<span class="condition">保険給付を受けるべき者が当該第三者から同一の事由について損害賠償を受けたとき</span>は、<div class="subject-line"><span class="subject">政府</span>は、</div><div class="predicate-line">その価額の限度で保険給付をしないことが<span class="predicate">できる。</span></div></div></div>''')

# --- 附則64条: 事業主の損害賠償との調整 ---
override('附則64条', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><span class="condition"><span class="subject">労働者<span class="logic">又は</span>その遺族</span>が年金給付を受けるべき場合</span>（前払一時金を請求することができる場合に限る。）であって、<br>同一の事由について、当該労働者を使用している事業主<span class="logic">又は</span>使用していた事業主から民法その他の法律による損害賠償を受けることができるときは、<br>当該損害賠償については、当分の間、次に定めるところによるものとする。<ul class="condition-list"><li>1. <span class="subject">事業主</span>は、当該労働者<span class="logic">又は</span>その遺族の年金給付を受ける権利が消滅するまでの間、<br>前払一時金給付の最高限度額に相当する額となるべき額の限度で、<br>その損害賠償の履行をしないことが<span class="predicate">できる。</span></li><li>2. 前号の規定により損害賠償の履行が猶予されている場合において、年金給付<span class="logic">又は</span>前払一時金給付の支給が行われたときは、<br><span class="subject">事業主</span>は、当該年金給付<span class="logic">又は</span>前払一時金給付の額となるべき額の限度で、<br>その損害賠償の責めを<span class="predicate">免れる。</span></li></ul></div></div>''')

# --- 法29条: 社会復帰促進等事業 ---
override('法29条', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">政府</span>は、</div>労働者災害補償保険の適用事業に係る労働者<span class="logic">及び</span>その遺族について、<br>社会復帰促進等事業として、次の事業を行うことが<span class="predicate">できる。</span><ul class="condition-list"><li>1. 療養に関する施設<span class="logic">及び</span>リハビリテーションに関する施設の設置<span class="logic">及び</span>運営その他被災労働者の円滑な社会復帰を促進するために必要な事業</li><li>2. 被災労働者の療養生活の援護、被災労働者の受ける介護の援護、その遺族の就学の援護、被災労働者<span class="logic">及び</span>その遺族が必要とする資金の貸付けによる援護その他被災労働者<span class="logic">及び</span>その遺族の援護を図るために必要な事業</li><li>3. 業務災害の防止に関する活動に対する援助、健康診断に関する施設の設置<span class="logic">及び</span>運営その他労働者の安全<span class="logic">及び</span>衛生の確保、保険給付の適切な実施の確保<span class="logic">並びに</span>賃金の支払の確保を図るために必要な事業</li></ul></div></div>''')

# --- 則4条: 特別支給金の額（テーブル） ---
override('則4条', '''<div class="law-body"><div class="principle-section">障害特別支給金の額は、障害等級に応じ次の通りである。<ul class="condition-list"><li>第1級: <span class="period">342万円</span>　/　第8級: <span class="period">65万円</span></li><li>第2級: <span class="period">320万円</span>　/　第9級: <span class="period">50万円</span></li><li>第3級: <span class="period">300万円</span>　/　第10級: <span class="period">39万円</span></li><li>第4級: <span class="period">264万円</span>　/　第11級: <span class="period">29万円</span></li><li>第5級: <span class="period">225万円</span>　/　第12級: <span class="period">20万円</span></li><li>第6級: <span class="period">192万円</span>　/　第13級: <span class="period">14万円</span></li><li>第7級: <span class="period">159万円</span>　/　第14級: <span class="period">8万円</span></li></ul></div></div>''')

# --- 法33条: 特別加入 ---
override('法33条', '''<div class="law-body"><div class="principle-section">次の各号に掲げる者の業務災害、複数業務要因災害<span class="logic">及び</span>通勤災害に関しては、この章に定めるところによる。<ul class="condition-list"><li>1. 常時<span class="period">300人</span>（金融業<span class="logic">若しくは</span>保険業、不動産業<span class="logic">又は</span>小売業を主たる事業とする事業主については<span class="period">50人</span>、卸売業<span class="logic">又は</span>サービス業を主たる事業とする事業主については<span class="period">100人</span>）以下の労働者を使用する事業（以下「特定事業」という。）の事業主で<br>労働保険事務組合に労働保険事務の処理を委託するものである者（事業主が法人その他の団体であるときは、代表者）</li><li>2. 前号の事業主が行う事業に従事する者（労働者である者を除く。）</li></ul></div></div>''')

# --- 法38条: 審査請求 ---
override('法38条', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">保険給付に関する決定に不服のある者</span>は、</div><ul class="condition-list"><li>労働者災害補償保険審査官に対して審査請求をし、</li><li>その決定に不服のある者は、労働保険審査会に対して再審査請求をすることが</li></ul><div class="predicate-line"><span class="predicate">できる。</span></div></div><div class="principle-section"><span class="item-number">第2項</span>前項の審査請求をしている者は、<br><span class="condition">審査請求をした日から<span class="period">3箇月</span>を経過しても審査請求についての決定がないとき</span>は、<br>労働者災害補償保険審査官が審査請求を棄却したものと<span class="predicate">みなすことができる。</span></div><div class="principle-section"><span class="item-number">第3項</span>第1項の審査請求<span class="logic">及び</span>再審査請求は、<br>時効の完成猶予<span class="logic">及び</span>更新に関しては、これを裁判上の請求と<span class="predicate">みなす。</span></div></div>''')

# --- 法40条: 訴訟との関係 ---
override('法40条', '''<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">第38条第1項に規定する処分の取消しの訴え</span>は、</div><div class="predicate-line">当該処分についての審査請求に対する労働者災害補償保険審査官の決定を経た後でなければ、<span class="predicate">提起することができない。</span></div></div></div>''')

# --- 法30条: 費用の徴収 ---
override('法30条', '''<div class="law-body"><div class="principle-section">労働者災害補償保険事業に要する費用にあてるため<span class="subject">政府</span>が徴収する保険料については、<br>徴収法の定めるところ<span class="predicate">による。</span></div></div>''')

# --- 法42条: 時効 ---
override('法42条', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><ul class="condition-list"><li><span class="subject">療養補償給付、休業補償給付、葬祭料、介護補償給付、<br>複数事業労働者療養給付、複数事業労働者休業給付、複数事業労働者葬祭給付、複数事業労働者介護給付、<br>療養給付、休業給付、葬祭給付、介護給付<span class="logic">及び</span>二次健康診断等給付</span>を受ける権利は、<br>これらを行使することができる時から<span class="period">2年</span>を経過したとき、</li><li><span class="subject">障害補償給付、遺族補償給付、<br>複数事業労働者障害給付、複数事業労働者遺族給付、<br>障害給付<span class="logic">及び</span>遺族給付</span>を受ける権利は、<br>これらを行使することができる時から<span class="period">5年</span>を経過したときは、</li></ul><div class="predicate-line">時効によって<span class="predicate">消滅する。</span></div></div></div>''')

# --- 法45条: 戸籍事項の無料証明 ---
override('法45条', '''<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">市町村長</span>（特別区の区長を含むものとし、指定都市においては、区長<span class="logic">又は</span>総合区長とする。）は、</div><ul class="condition-list"><li>行政庁</li><li class="logic-item"><span class="logic">又は</span></li><li>保険給付を受けようとする者</li></ul>に対して、当該市町村の条例で定めるところにより、<br>保険給付を受けようとする者<span class="logic">又は</span>遺族の戸籍に関し、無料で証明を<span class="predicate">行うことができる。</span></div></div>''')

# --- 則51条: 書類の保存 ---
override('則51条', '''<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">労災保険に係る保険関係が成立し、<span class="logic">若しくは</span>成立していた事業の事業主<span class="logic">又は</span>労働保険事務組合<span class="logic">若しくは</span>労働保険事務組合であった団体</span>は、</div><div class="predicate-line">労災保険に関する書類（徴収法<span class="logic">又は</span>徴収法施行規則による書類を除く。）を、<br>その完結の日から<span class="period">3年間</span>保存<span class="predicate">しなければならない。</span></div></div></div>''')

# --- 法46条: 使用者への報告命令 ---
override('法46条', '''<div class="law-body"><div class="principle-section"><div class="subject-line"><span class="subject">所轄都道府県労働局長<span class="logic">又は</span>所轄労働基準監督署長</span>は、</div><ul class="condition-list"><li>労働者を使用する者、</li><li>労働保険事務組合、</li><li>一人親方等の団体、</li><li>派遣先の事業主</li><li class="logic-item"><span class="logic">又は</span></li><li>船員派遣の役務の提供を受ける者</li></ul>に対して、労災保険法の施行に関し必要な報告、文書の提出<span class="logic">又は</span>出頭を<span class="predicate">命ずることができる。</span></div></div>''')

# --- 法48条: 立入検査 ---
override('法48条', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">行政庁</span>（所轄都道府県労働局長<span class="logic">又は</span>所轄労働基準監督署長）は、</div>労災保険法の施行に必要な限度において、<br>当該職員に、<ul class="condition-list"><li>適用事業の事業場、</li><li>労働保険事務組合<span class="logic">若しくは</span>一人親方等の団体の事務所、</li><li>派遣先の事業の事業場</li><li class="logic-item"><span class="logic">又は</span></li><li>船員派遣の役務の提供を受ける者の事業場</li></ul>に立ち入り、関係者に質問させ、<span class="logic">又は</span>帳簿書類その他の物件を検査させることが<span class="predicate">できる。</span></div><div class="principle-section"><span class="item-number">第2項</span>前項の規定により立入検査をする職員は、<br>その身分を示す証明書を携帯し、関係者に提示<span class="predicate">しなければならない。</span></div></div>''')

# --- 法49条の3: 資料提供の協力 ---
override('法49条の3', '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">厚生労働大臣</span>は、</div>労災保険法の施行に関し、<br>関係行政機関<span class="logic">又は</span>公私の団体に対し、<br>資料の提供その他必要な協力を<span class="predicate">求めることができる。</span></div><div class="principle-section"><span class="item-number">第2項</span>前項の規定による協力を求められた関係行政機関<span class="logic">又は</span>公私の団体は、<br>できるだけその求めに応じ<span class="predicate">なければならない。</span></div></div>''')


# ========================================
# メイン処理
# ========================================

def main():
    # 既存の structured データを読み込み
    with open('structured_労災保険法.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"労災保険法: {len(data)}件の条文を処理")

    updated = 0
    for item in data:
        ref = item['reference']
        if ref in MANUAL_OVERRIDES:
            item['structured'] = MANUAL_OVERRIDES[ref]
            updated += 1
            print(f"  ✓ {ref}: 手動オーバーライド適用")
        else:
            print(f"  - {ref}: オーバーライドなし（既存を維持）")

    print(f"\n更新: {updated}/{len(data)}件")

    # 保存
    with open('structured_労災保険法.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("structured_労災保険法.json を保存しました")


if __name__ == '__main__':
    main()

"""
健康保険法の全201条文を v3フォーマットの構造化HTMLに変換するスクリプト。

6要素のクラス分類:
1. subject (主語): 誰が、何が
2. condition (要件・条件): 〜の場合、〜を除き
3. logic (論理演算子): かつ、又は、若しくは、並びに、及び
4. period (数字・期限): 3年、満60歳以上、30日間
5. predicate (述語・効果): 〜しなければならない、〜してはならない、〜できる
6. exception (例外・ただし書き): ただし〜、〜この限りでない
"""
import json
import re

# =============================================
# 法文テキスト抽出（解説テキスト除去）
# =============================================

with open('struct_input_健康保険法.json', 'r', encoding='utf-8') as f:
    input_data = json.load(f)

def extract_law_text(body, reference):
    """bodyから法文テキスト部分のみを抽出し、段落リストを返す"""
    text = body.strip()

    # 先頭のゴミ除去（前の条文の参照テキストなど）
    if text and text[0] in '、1':
        m = re.search(r'◯\d', text)
        if m and m.start() < 80:
            text = text[m.start():]
        elif text.startswith('1号') or text.startswith('1.'):
            m = re.search(r'◯\d', text)
            if m:
                text = text[m.start():]
        elif text.startswith('、'):
            # 「、」で始まるゴミを除去
            # ◯マーカーがあればそこから
            m = re.search(r'◯\d', text)
            if m:
                text = text[m.start():]
            else:
                # ◯マーカーなしの場合は最初の法的主語を探す
                # 例: "、附則3条6項 ◯1..."
                text = re.sub(r'^、[^◯]*?(?=◯)', '', text)
                if text.startswith('、'):
                    # それでもダメなら ◯ なしのテキストとして処理
                    text = text.lstrip('、').strip()

    # 段落分割
    paragraphs = []
    if '◯' in text:
        parts = re.split(r'(◯\d+)', text)
        i = 0
        while i < len(parts):
            if re.match(r'◯\d+$', parts[i]):
                marker = parts[i]
                if i + 1 < len(parts):
                    content = parts[i + 1]
                    paragraphs.append((marker, content))
                    i += 2
                else:
                    i += 1
            else:
                if parts[i].strip():
                    paragraphs.append(('', parts[i]))
                i += 1
    else:
        paragraphs.append(('', text))

    # 各段落から解説テキストを除去
    cleaned = []
    for marker, content in paragraphs:
        clean = remove_explanation(content)
        if clean.strip():
            cleaned.append((marker, clean.strip()))

    return cleaned

def remove_explanation(text):
    """テキストから解説部分を除去する"""
    sentences = []
    current = ''
    paren_depth = 0

    for ch in text:
        if ch == '（':
            paren_depth += 1
        elif ch == '）':
            paren_depth -= 1
            if paren_depth < 0:
                paren_depth = 0
        current += ch
        if ch == '。' and paren_depth <= 0:
            sentences.append(current)
            current = ''
    if current.strip():
        sentences.append(current)

    if not sentences:
        return text

    # 最初の文は必ず法文テキスト（解説ではない）
    law_text = sentences[0]
    for i in range(1, len(sentences)):
        s = sentences[i].strip()
        if is_explanation(s):
            break
        law_text += sentences[i]

    return law_text.strip()

EXPLANATION_HEADINGS = [
    '目的', '基本的理念', '保険者の種類', '管掌の区分', '全国健康保険協会',
    '日本年金機構', '財務大臣', '地方厚生局長', '基金など', '組合の構成',
    '組合の任意設立', '強制設立', '組合の成立', '組合員', '役員',
    '組合会', '会計年度', '予算', '組合債', '合併', '分割', '解散',
    '健全化計画', '報告の徴収', '監督', '健康保険組合連合会',
    '強制適用事業所', '任意適用事業所', '擬制', '一括適用',
    '新規適用届', '事業主の氏名', '適用事業所に該当',
    '適用除外', '共済組合', '事業主の届出', '強制被保険者',
    '被保険者資格', '任意継続被保険者', '特例退職被保険者',
    '資格の確認', '届出', '業績評価', '事業計画', '借入金',
    '余裕金', '重要な財産', '役員の報酬', '準備金',
    '被保険者証', '氏名変更', '住所変更', '通知',
    '2以上の事業所', '2024改正', '2026改正', '2021改正', '2023改正',
    '標準報酬月額', '標準賞与額', '定時決定', '随時改定',
    '報酬月額', '賞与額', '賞与支払届', '保険料', '保険料率',
    '一般保険料率', '特定保険料率', '基本保険料率',
    '介護保険料率', '調整保険料', '国庫負担', '国庫補助',
    '保険給付', '療養の給付', '保険医療機関', '保険薬局',
    '一部負担金', '入院時食事療養費', '入院時生活療養費',
    '保険外併用療養費', '療養費', '訪問看護療養費',
    '高額療養費', '高額介護合算療養費', '移送費',
    '傷病手当金', '出産育児一時金', '出産手当金',
    '埋葬料', '家族療養費', '家族訪問看護療養費',
    '家族移送費', '家族埋葬料', '家族出産育児一時金',
    '資格喪失後', '給付制限', '損害賠償', '不正利得',
    '受給権', '租税', '日雇特例被保険者', '特別療養費',
    '保健事業', '福祉事業', '時効', '届出義務', '届出等',
    '不服申立て', '審査請求', '再審査請求', '主要給付費',
    '記載事項', '資格確認書', '被扶養者', '現物給与',
    '要件', '育児休業等終了時改定', '産前産後休業終了時改定',
    '確認の請求', '資格取得届', '資格取得届との関係',
    '平成', '昭和', '令和',
    '作成し', '厚生労働大臣の',
    '任意適用', '法定',
]

def is_explanation(sent):
    """文が解説テキストかどうかを判定"""
    if re.search(r'R\d{2}-\d{2}', sent):
        return True
    if re.search(r'(です|ます|ません|ください|しょう)。$', sent):
        return True
    if re.search(r'（法\d+条[^）]*）$', sent):
        return True
    if re.search(r'（令\d+条[^）]*）$', sent):
        return True
    if re.search(r'（則\d+条[^）]*）$', sent):
        return True
    if re.search(r'（附則[^）]*）$', sent):
        return True
    for heading in EXPLANATION_HEADINGS:
        if sent.startswith(heading):
            return True
    if len(sent) <= 15 and '。' not in sent and not re.match(r'◯\d', sent):
        if not sent.endswith(('する', 'ない', 'できる', 'とする', 'ものとする')):
            return True
    return False

# =============================================
# 構造化HTML生成
# =============================================

def escape_html(text):
    """HTMLエスケープ"""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def wrap_logic(text):
    """テキスト中の論理演算子をspanで囲む"""
    # 順序重要: 長い方を先にマッチ
    operators = ['若しくは', '並びに', '又は', '及び', 'かつ']
    for op in operators:
        text = text.replace(op, f'<span class="logic">{op}</span>')
    return text

def wrap_period(text):
    """テキスト中の数字・期限をspanで囲む"""
    patterns = [
        # X人, X人以上, X人以内, X人未満
        (r'(\d[\d,]*人(?:以上|以内|未満)?)', r'<span class="period">\1</span>'),
        # X日以内, X日間
        (r'(\d+日(?:以内|間)?)', r'<span class="period">\1</span>'),
        # X月以内, X月を超え, Xか月, X月間
        (r'(\d+(?:か)?月(?:以内|を超え(?:て)?|間)?)', r'<span class="period">\1</span>'),
        # X年以内, X年間, X年を経過
        (r'(\d+年(?:以内|間|を経過)?)', r'<span class="period">\1</span>'),
        # X分のX以上
        (r'(\d+分の\d+(?:以上)?)', r'<span class="period">\1</span>'),
        # X歳, 満X歳
        (r'((?:満)?\d+歳(?:以上|未満|に達し)?)', r'<span class="period">\1</span>'),
        # X万円
        (r'(\d[\d,]*万円)', r'<span class="period">\1</span>'),
        # X,000分のX
        (r'([\d,]+分の[\d,]+)', r'<span class="period">\1</span>'),
        # XX%
        (r'(\d+(?:\.\d+)?(?:%|％|パーセント))', r'<span class="period">\1</span>'),
    ]
    for pattern, repl in patterns:
        text = re.sub(pattern, repl, text)
    # ネストしたperiodを修正
    text = re.sub(r'<span class="period">([^<]*)<span class="period">([^<]*)</span>([^<]*)</span>',
                  r'<span class="period">\1\2\3</span>', text)
    return text

def split_multi_sentences(text):
    """段落内の複数文を分割する（ただし書き以外の文区切り）"""
    # 括弧内の句点は無視
    sentences = []
    current = ''
    paren_depth = 0

    for ch in text:
        if ch == '（':
            paren_depth += 1
        elif ch == '）':
            paren_depth -= 1
            if paren_depth < 0:
                paren_depth = 0
        current += ch
        if ch == '。' and paren_depth == 0:
            sentences.append(current)
            current = ''

    if current.strip():
        sentences.append(current)

    return sentences

def structure_paragraph(text, para_num=None):
    """1つの段落（法文テキスト）を構造化HTMLに変換する"""
    text = text.strip()
    if not text:
        return ''

    # まず、段落内の複数文を検出
    # 「〜ならない。これを変更しようとするときも、同様とする。」のようなパターン
    sentences = split_multi_sentences(text)

    # ただし書きを含む文を結合
    merged = []
    for sent in sentences:
        if sent.strip().startswith('ただし、') and merged:
            merged[-1] = merged[-1] + sent
        else:
            merged.append(sent)

    # 各文をただし書きで分割して構造化
    html_parts = []
    for j, sent_text in enumerate(merged):
        parts = split_tadashi(sent_text)
        for i, (part_text, is_exception) in enumerate(parts):
            pn = para_num if (j == 0 and i == 0) else None
            if is_exception:
                html_parts.append(structure_exception(part_text, pn))
            else:
                html_parts.append(structure_principle(part_text, pn))

    return '\n'.join(html_parts)

def split_tadashi(text):
    """テキストを「ただし書き」で分割する"""
    # 括弧内の「ただし」は無視
    parts = []
    current = ''
    paren_depth = 0
    i = 0

    while i < len(text):
        ch = text[i]
        if ch == '（':
            paren_depth += 1
            current += ch
            i += 1
        elif ch == '）':
            paren_depth -= 1
            if paren_depth < 0:
                paren_depth = 0
            current += ch
            i += 1
        elif paren_depth == 0 and text[i:].startswith('ただし、'):
            if current.strip():
                parts.append((current.strip(), False))
            current = 'ただし、'
            i += 4
        elif paren_depth == 0 and text[i:].startswith('ただし書の') or (paren_depth == 0 and text[i:].startswith('ただし書')):
            # 「前項ただし書の」はただし書きの分割ではない
            current += ch
            i += 1
        else:
            current += ch
            i += 1

    if current.strip():
        is_exc = current.strip().startswith('ただし、') or current.strip().startswith('ただし，')
        parts.append((current.strip(), is_exc))

    if not parts:
        parts.append((text, False))

    return parts

def structure_principle(text, para_num=None):
    """原則部分の構造化"""
    html = '  <div class="principle-section">\n'

    if para_num:
        num_label = para_num.replace('◯', '第') + '項'
        html += f'    <span class="item-number">{num_label}</span>\n'

    # 主語と述語を分離
    subject, rest = extract_subject(text)

    if subject:
        subject_html = wrap_period(wrap_logic(subject))
        html += f'    <div class="subject-line"><span class="subject">{subject_html}は、</span></div>\n'

    if rest:
        # 条件リストと述語を分離
        conditions, predicate = extract_conditions_and_predicate(rest)

        if conditions:
            html += '    <ul class="condition-list">\n'
            for cond in conditions:
                if cond.get('is_logic'):
                    logic_html = f'<span class="logic">{cond["text"]}</span>'
                    html += f'      <li class="logic-item">{logic_html}</li>\n'
                else:
                    cond_html = wrap_period(wrap_logic(cond['text']))
                    html += f'      <li><span class="condition">{cond_html}</span></li>\n'
            html += '    </ul>\n'

        if predicate:
            pred_html = wrap_period(wrap_logic(predicate))
            html += f'    <div class="predicate-line"><span class="predicate">{pred_html}</span></div>\n'
    elif not subject:
        # 主語も述語もない場合（全体を述語として扱う）
        pred_html = wrap_period(wrap_logic(text))
        html += f'    <div class="predicate-line"><span class="predicate">{pred_html}</span></div>\n'

    html += '  </div>'
    return html

def structure_exception(text, para_num=None):
    """ただし書き部分の構造化"""
    html = '  <div class="exception-section">\n'

    if para_num:
        num_label = para_num.replace('◯', '第') + '項'
        html += f'    <span class="item-number">{num_label}</span>\n'

    # "ただし、" を除去
    rest = text
    if rest.startswith('ただし、'):
        rest = rest[4:]
    elif rest.startswith('ただし，'):
        rest = rest[4:]

    html += '    <div class="exception-keyword"><span class="exception">ただし、</span></div>\n'

    # 条件と結論を分離
    conditions, conclusion = extract_exception_parts(rest)

    if conditions:
        html += '    <ul class="condition-list">\n'
        for cond in conditions:
            if cond.get('is_logic'):
                logic_html = f'<span class="logic">{cond["text"]}</span>'
                html += f'      <li class="logic-item">{logic_html}</li>\n'
            else:
                cond_html = wrap_period(wrap_logic(cond['text']))
                html += f'      <li><span class="condition">{cond_html}</span></li>\n'
        html += '    </ul>\n'

    if conclusion:
        conc_html = wrap_period(wrap_logic(conclusion))
        html += f'    <div class="predicate-line"><span class="exception">{conc_html}</span></div>\n'

    html += '  </div>'
    return html

def extract_subject(text):
    """テキストから主語を抽出する"""
    # パターン: 「Xは、」で主語を区切る
    # ただし、括弧内の「は、」は無視

    paren_depth = 0
    for i, ch in enumerate(text):
        if ch == '（':
            paren_depth += 1
        elif ch == '）':
            paren_depth -= 1
            if paren_depth < 0:
                paren_depth = 0

        if paren_depth == 0 and i > 0 and text[i-1:i+1] == 'は、':
            # "は、" が見つかった
            subject = text[:i-1]
            rest = text[i+1:]

            # 主語が長すぎる場合は分割しない
            if len(subject) > 200:
                return None, text

            # 「は、」の前が条件的でないことを確認
            # 例: "〜場合においては、" → これは条件
            if subject.endswith(('場合において', '場合に', 'ときに', 'ときにおいて')):
                return None, text

            return subject, rest

    # 「は、」がない場合
    return None, text

def extract_conditions_and_predicate(text):
    """テキストから条件リストと述語を分離する"""
    text = text.strip()
    if not text:
        return [], ''

    # 述語パターン（文末）
    predicate_patterns = [
        'しなければならない。',
        'してはならない。',
        'することができる。',
        'することができない。',
        'するものとする。',
        'とする。',
        'ものとする。',
        'ものとみなす。',
        'みなす。',
        'この限りでない。',
        '妨げない。',
        '命ずることができる。',
        '積み立てなければならない。',
        '償還しなければならない。',
        '提出しなければならない。',
        '届け出なければならない。',
        '届出しなければならない。',
        '申請しなければならない。',
        '通知しなければならない。',
        '報告しなければならない。',
        '行うものとする。',
        '公表しなければならない。',
        '徴収する。',
        '交付する。',
        '補助する。',
        '負担する。',
        '管掌する。',
        '決定する。',
        '改定する。',
        '行わない。',
        '行う。',
        '設ける。',
        '組織する。',
        '選挙する。',
        '互選する。',
        '任命する。',
        '同様とする。',
    ]

    # 文末の述語を見つける
    predicate = ''
    remaining = text

    # 最後の句点位置を見つける（括弧内を無視）
    last_period = find_last_period(text)

    if last_period >= 0:
        # 述語部分を特定（最後の文の述語的な部分）
        sentence_end = text[:last_period + 1]

        # 条件と述語を分離
        # 読点で区切られた最後の部分が述語
        conditions, predicate = split_conditions_predicate(text)
        return conditions, predicate

    return [], text

def find_last_period(text):
    """括弧内を無視して最後の句点位置を見つける"""
    paren_depth = 0
    last = -1
    for i, ch in enumerate(text):
        if ch == '（':
            paren_depth += 1
        elif ch == '）':
            paren_depth -= 1
            if paren_depth < 0:
                paren_depth = 0
        elif ch == '。' and paren_depth == 0:
            last = i
    return last

def split_conditions_predicate(text):
    """テキストを条件リストと述語に分離する"""
    # 読点で分割（括弧内は無視）
    parts = split_by_comma(text)

    if len(parts) <= 1:
        return [], text

    # 最後のパートが述語
    predicate = parts[-1].strip()
    if predicate.endswith('。'):
        pass  # OK

    # 前のパートが条件
    conditions = []
    for part in parts[:-1]:
        part = part.strip()
        if part:
            conditions.append({'text': part, 'is_logic': False})

    return conditions, predicate

def split_by_comma(text):
    """括弧内を無視して読点で分割"""
    parts = []
    current = ''
    paren_depth = 0

    for ch in text:
        if ch == '（':
            paren_depth += 1
            current += ch
        elif ch == '）':
            paren_depth -= 1
            if paren_depth < 0:
                paren_depth = 0
            current += ch
        elif ch == '、' and paren_depth == 0:
            parts.append(current)
            current = ''
        else:
            current += ch

    if current:
        parts.append(current)

    return parts

def extract_exception_parts(text):
    """ただし書きの条件と結論を分離"""
    text = text.strip()

    # 「この限りでない。」で終わるか確認
    if text.endswith('この限りでない。'):
        condition_text = text[:-8]  # 「この限りでない。」を除去
        conditions = []
        parts = split_by_comma(condition_text)
        for part in parts:
            part = part.strip()
            if part:
                conditions.append({'text': part, 'is_logic': False})
        return conditions, 'この限りでない。'

    # 「受理することができる。」等で終わる場合
    conditions, predicate = split_conditions_predicate(text)
    return conditions, predicate

def generate_structured_html(reference, paragraphs):
    """全段落を統合した構造化HTMLを生成"""
    if not paragraphs:
        return ''

    html = '<div class="law-body">\n'

    for marker, text in paragraphs:
        para_num = marker if marker else None
        para_html = structure_paragraph(text, para_num)
        if para_html:
            html += para_html + '\n'

    html += '</div>'
    return html

# =============================================
# メイン処理
# =============================================

# 特殊な条文のハードコード（抽出が難しいもの）
SPECIAL_ARTICLES = {
    '法123条': [('◯1', '日雇特例被保険者の保険の保険者は、協会とする。')],
    '法5条': [('◯1', '全国健康保険協会は、健康保険組合の組合員でない被保険者（日雇特例被保険者を除く。）の保険を管掌する。')],
    '法18条': [
        ('◯1', '健康保険組合に、組合会を置く。'),
        ('◯2', '組合会は、組合会議員をもって組織する。'),
        ('◯3', '組合会議員の定数は、偶数とし、その半数は、設立事業所の事業主において設立事業所の事業主（その代理人を含む。）及び設立事業所に使用される者のうちから選定し、他の半数は、被保険者である組合員において互選する。'),
    ],
    '法33条': [
        ('◯1', '任意適用事業所の事業主は、厚生労働大臣の認可を受けて、当該事業所を適用事業所でなくすることができる。'),
        ('◯2', '前項の認可を受けようとするときは、当該事業所の事業主は、当該事業所に使用される者（被保険者である者に限る。）の4分の3以上の同意を得て、厚生労働大臣に申請しなければならない。'),
    ],
    '法38条': [
        ('', '任意継続被保険者は、次の各号のいずれかに該当するに至った日の翌日（第4号から第6号までのいずれかに該当するに至ったときは、その日）から、その資格を喪失する。1. 任意継続被保険者となった日から起算して2年を経過したとき。2. 死亡したとき。3. 保険料（初めて納付すべき保険料を除く。）を納付期日までに納付しなかったとき（納付の遅延について正当な理由があると保険者が認めたときを除く。）。4. 強制被保険者となったとき。5. 船員保険の被保険者となったとき。6. 後期高齢者医療の被保険者等となったとき。7. 任意継続被保険者でなくなることを希望する旨を、保険者に申し出た場合において、その申出が受理された日の属する月の末日が到来したとき。'),
    ],
    '法40条': [
        ('◯1', '被保険者の報酬月額は、次の各号に掲げる場合の区分に応じ、当該各号に定めるところにより算定する。1. 第41条第1項の規定により算定する場合 報酬月額は、被保険者が毎年7月1日現に使用される事業所において同日前3月間に受けた報酬の総額をその期間の月数で除して得た額とする。2. 第42条第1項の規定により算定する場合 報酬月額は、被保険者の資格を取得した月の報酬月額とする。3. 第43条第1項の規定により算定する場合 報酬月額は、被保険者が現に使用される事業所において継続した3月間に受けた報酬の総額を3で除して得た額とする。'),
    ],
    '法152条の2': [
        ('◯1', '国庫は、予算の範囲内において、協会が管掌する健康保険の被保険者に係る後期高齢者支援金及び後期高齢者関係事務費拠出金並びに介護納付金の納付に要する費用の一部を補助する。'),
    ],
    '附則3条': [
        ('', '特定健康保険組合の任意継続被保険者に対して支給する保険給付については、当該特定健康保険組合の規約で定めるところにより、法第99条の傷病手当金及び法第102条の出産手当金を支給しないことができる。'),
    ],
    '法3条': [
        ('◯3', '「適用事業所」とは、次の各号のいずれかに該当する事業所をいう。1. 適用業種である事業の事業所であって、常時5人以上の従業員を使用するもの 2. 前号に掲げるもののほか、国、地方公共団体又は法人の事業所であって、常時従業員を使用するもの'),
    ],
    '法165条': [
        ('◯1', '任意継続被保険者及び特例退職被保険者は、自己の負担する保険料を前納することができる。'),
    ],
    '法172条': [
        ('', '保険者は、次に掲げる場合においては、期限前であっても、すべて徴収することができる。1. 納付義務者が、次のいずれかに該当する場合 ア.国税、地方税その他の公課の滞納について、滞納処分を受けるとき。ウ.強制執行を受けるとき。オ.破産手続開始の決定を受けたとき。キ.企業担保権の実行手続の開始があったとき。ケ.競売の開始があったとき。2. 法人である納付義務者が、解散をした場合 3. 被保険者の使用される事業所が、廃止された場合'),
    ],
    '法182条': [
        ('', '保険給付の消滅時効は、国税及び地方税に次ぐものとする。'),
    ],
    '法183条': [
        ('', '保険料等は、健康保険法に別段の規定があるものを除き、国税徴収の例により徴収する。'),
    ],
    '法63条': [
        ('◯3', '療養の給付を受けようとする者は、次に掲げる病院若しくは診療所又は薬局のうち、自己の選定するものから、電子資格確認により被保険者であることの確認を受け、療養の給付を受けるものとする。1. 厚生労働大臣の指定を受けた病院若しくは診療所（以下「保険医療機関」という。）又は薬局（以下「保険薬局」という。）2. 特定の保険者が管掌する被保険者に対して診療又は調剤を行う病院若しくは診療所又は薬局であって、当該保険者が指定したもの 3. 健康保険組合である保険者が開設する病院若しくは診療所又は薬局'),
    ],
    '法70条': [
        ('◯1', '保険医療機関又は保険薬局は、当該保険医療機関において診療に従事する保険医又は当該保険薬局において調剤に従事する保険薬剤師に、診療又は調剤に当たらせるほか、療養の給付を担当しなければならない。'),
    ],
    '法65条': [
        ('◯1', '保険医療機関又は保険薬局の指定は、病院若しくは診療所又は薬局の開設者の申請により行う。'),
    ],
    '法68条': [
        ('◯1', '保険医療機関又は保険薬局の指定は、指定の日から起算して6年を経過したときは、その効力を失う。'),
    ],
    '法79条': [
        ('◯1', '保険医療機関又は保険薬局は、1月以上の予告期間を設けて、その指定を辞退することができる。'),
    ],
    '法64条': [
        ('', '保険医療機関において健康保険の診療に従事する医師若しくは歯科医師又は保険薬局において健康保険の調剤に従事する薬剤師は、厚生労働大臣の登録を受けた医師若しくは歯科医師（以下「保険医」と総称する。）又は薬剤師（以下「保険薬剤師」という。）でなければならない。'),
    ],
    '法72条': [
        ('◯1', '保険医療機関において診療に従事する保険医又は保険薬局において調剤に従事する保険薬剤師は、保険医療機関及び保険医療養担当規則に定める保険医の診療方針又は保険薬局及び保険薬剤師療養担当規則に定める調剤の一般的方針に従って、健康保険の診療又は調剤に当たらなければならない。'),
    ],
    '法73条': [
        ('◯1', '保険医療機関及び保険薬局は療養の給付に関し、保険医及び保険薬剤師は健康保険の診療又は調剤に関し、厚生労働大臣の指導を受けなければならない。'),
    ],
    '法74条': [
        ('◯1', '保険医療機関又は保険薬局から療養の給付を受ける者は、その給付を受ける際、その各号に掲げる場合の区分に応じ、当該給付につき第76条第2項又は第3項の規定により算定した額に当該各号に定める割合を乗じて得た額を、一部負担金として、当該保険医療機関又は保険薬局に支払わなければならない。1. 70歳に達する日の属する月の翌月以前である場合…100分の30 2. 70歳に達する日の属する月の翌月以後である場合（次号に掲げる場合を除く。）…100分の20 3. 70歳に達する日の属する月の翌月以後である場合であって、政令で定めるところにより算定した収入の額が政令で定める額（28万円）以上であるとき…100分の30'),
    ],
    '則62条': [
        ('', '保険医療機関等は、交付しなければならない領収証には、正当な理由がない限り、入院時食事療養費に係る療養について被保険者から支払を受けた費用の額のうち食事療養標準負担額とその他の費用の額とを区分して記載しなければならない。'),
    ],
    '則62条の5': [
        ('', '保険医療機関等は、交付しなければならない領収証には、正当な理由がない限り、入院時生活療養費に係る療養について被保険者から支払を受けた費用の額のうち生活療養標準負担額とその他の費用の額とを区分して記載しなければならない。'),
    ],
    '則64条': [
        ('', '保険医療機関等は、交付しなければならない領収証には、保険外併用療養費に係る療養について被保険者から支払を受けた費用の額のうち保険外併用療養費に係る一部負担相当額とその他の費用の額とを区分（当該費用の額に食事療養に係る食事療養標準負担額又は生活療養に係る生活療養標準負担額が含まれるときは、当該額についても区分）して記載しなければならない。'),
    ],
    '法115条': [
        ('◯1', '療養の給付について支払われた一部負担金の額又は療養（食事療養及び生活療養を除く。以下において同じ。）に要した費用の額からその療養に要した費用につき保険外併用療養費、療養費、高額療養費、家族療養費若しくは家族高額療養費として支給された額に相当する額を控除した額（以下「一部負担金等の額」という。）が著しい額であるときは、その療養の給付又はその保険外併用療養費、療養費、高額療養費、家族療養費若しくは家族高額療養費の支給を受けた者に対し、高額療養費を支給する。'),
        ('◯2', '高額療養費の支給要件、支給額その他高額療養費の支給に関して必要な事項は、療養に必要な費用の負担の家計に与える影響及び療養に要した費用の額を考慮して、政令で定める。'),
    ],
    '法115条の2': [
        ('◯1', '一部負担金等の額（高額療養費が支給される場合においては、当該支給額に相当する額を控除した額）並びに介護保険法に規定するサービス利用者負担額（同法の高額サービスが支給される場合においては、当該支給額を控除した額）及び同法に規定する予防サービス利用者負担額（同法の高額予防サービスが支給される場合においては、当該支給額を控除した額）の合計額が著しい額であるときは、当該一部負担金等の額に係る療養の給付又は保険外併用療養費、療養費、高額療養費、家族療養費若しくは家族高額療養費の支給を受けた者に対し、高額介護合算療養費を支給する。'),
    ],
    '則80条': [
        ('', '移送費の金額は、最も経済的な通常の経路及び方法により移送された場合の費用により算定した額とする。ただし、現に移送に要した費用の金額を超えることができない。'),
    ],
    '法103条': [
        ('◯1', '出産手当金が支給される場合（第108条第3項又は第4項（傷病手当金又は障害手当金との調整）に該当するときを除く。）においては、その期間、傷病手当金は、支給しない。ただし、その受けることができる出産手当金の額（第2項の規定の適用（出産手当金との差額支給）の場合においては、同項の規定に規定する額と同項の規定により算定される出産手当金の額との合算額）が、傷病手当金の額より少ないときは、その差額を支給する。'),
        ('◯2', '出産手当金を支給すべき場合において傷病手当金が支給されたときは、その支給された傷病手当金（前項ただし書の規定により支給されたものを除く。）は、出産手当金の内払とみなす。'),
    ],
    '則84条の3': [
        ('', '傷病手当金は、同一の傷病について支給を始めた日の累計が法第99条第4項に規定する支給期間の日数に達するまで支給する。'),
    ],
    '則84条': [
        ('◯1', '傷病手当金の支給を受けようとする者は、所定の事項を記載した申請書を保険者に提出しなければならない。'),
    ],
    '法61条': [
        ('', '保険給付を受ける権利は、譲り渡し、担保に供し、又は差し押さえることができない。'),
    ],
    '法62条': [
        ('', '租税その他の公課は、保険給付として支給を受けた金品を標準として、課することができない。'),
    ],
    '法203条': [
        ('◯1', '日雇特例被保険者の保険の保険者の事務のうち厚生労働大臣が行うものの一部は、市町村長（特別区の区長を含むものとし、指定都市においては、区長又は総合区長とする。）が行うこととすることができる。'),
        ('◯2', '全国健康保険協会は、市町村長（特別区を含む。）に対し、日雇特例被保険者の保険の保険者の事務のうち全国健康保険協会が行うものの一部を委託することができる。'),
    ],
    '法190条': [
        ('', '保険給付の処分若しくは徴収の処分又は滞納処分及び滞納処分に不服がある者は、社会保険審査官に対して審査請求をすることができる。'),
    ],
    '法193条': [
        ('◯1', '保険料等を徴収し、又はその還付を受ける権利及び保険給付を受ける権利は、これらを行使することができる時から2年を経過したときは、時効により消滅する。'),
        ('◯2', '保険料等の納入の告知又は督促は、時効更新の効力を有する。'),
    ],
}

results = []
for item in input_data:
    ref = item['reference']
    body = item['body']

    if ref in SPECIAL_ARTICLES:
        paragraphs = SPECIAL_ARTICLES[ref]
    else:
        paragraphs = extract_law_text(body, ref)

    html = generate_structured_html(ref, paragraphs)
    results.append({
        'reference': ref,
        'structured': html
    })

# 保存
with open('structured_健康保険法.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# 検証用出力
with open('_health_structured_preview.txt', 'w', encoding='utf-8') as out:
    for r in results:
        out.write(f'=== {r["reference"]} ===\n')
        out.write(r['structured'])
        out.write('\n\n')

print(f'Generated structured HTML for {len(results)} articles')
# 空の記事を報告
empty = [r['reference'] for r in results if not r['structured'].strip()]
if empty:
    print(f'Empty articles: {empty}')

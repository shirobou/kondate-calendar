"""
健康保険法の各条文bodyから、法文テキストのみを抽出するスクリプト。
解説・補足テキストを除去し、純粋な条文テキストだけを残す。
"""
import json
import re

with open('struct_input_健康保険法.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def extract_law_text(body, reference):
    """bodyから法文テキスト部分のみを抽出する"""
    text = body.strip()

    # 先頭のゴミ（前の条文の参照など）を除去
    # 例: "、厚生年金保険法100条の6第3項 ◯1機構は..."
    # 例: "1号～8号 ◯1次の各号..."
    if text and not text[0] in '◯健適被保任指厚連日事第前国組法令協理監予当届初2次使産報業介出高傷医受資':
        # ◯マーカーの前にゴミがある場合
        m = re.search(r'◯\d', text)
        if m:
            text = text[m.start():]
        else:
            # 条文テキストの開始を探す
            # "1号～8号" のようなプレフィックスをスキップ
            m = re.match(r'^[^。]+?\s+', text)
            if m and len(m.group()) < 30:
                text = text[m.end():]

    # 段落分割: ◯1, ◯2, ◯3... で分ける
    paragraphs = []
    # ◯マーカーがある場合
    if '◯' in text:
        parts = re.split(r'(◯\d+)', text)
        i = 0
        while i < len(parts):
            if re.match(r'◯\d+', parts[i]):
                marker = parts[i]
                if i + 1 < len(parts):
                    content = parts[i + 1]
                    paragraphs.append((marker, content))
                    i += 2
                else:
                    i += 1
            else:
                # ◯なしの先頭テキスト
                if parts[i].strip():
                    paragraphs.append(('', parts[i]))
                i += 1
    else:
        paragraphs.append(('', text))

    # 各段落から解説テキストを除去
    cleaned = []
    for marker, content in paragraphs:
        clean = remove_explanation(content, reference)
        if clean.strip():
            cleaned.append((marker, clean.strip()))

    return cleaned

def remove_explanation(text, reference):
    """テキストから解説部分を除去する"""
    # 法文は通常、句点(。)で終わる文で構成される
    # 解説テキストは法文の後に続く

    # まず文を句点で分割
    sentences = []
    current = ''
    paren_depth = 0

    for ch in text:
        if ch == '（':
            paren_depth += 1
        elif ch == '）':
            paren_depth -= 1
        current += ch
        if ch == '。' and paren_depth <= 0:
            sentences.append(current)
            current = ''
    if current.strip():
        sentences.append(current)

    if not sentences:
        return text

    # 解説テキストの開始を検出
    # パターン:
    # 1. 見出し語（漢字のみの短いフレーズ）で始まる文
    # 2. R0X-XXX のような試験問題番号
    # 3. 「〜です。」「〜ます。」で終わる平易な文
    # 4. （法XX条）のような条文参照で終わる文
    # 5. 箇条書きの解説

    law_text = ''
    for i, sent in enumerate(sentences):
        sent_stripped = sent.strip()

        # 解説の開始パターンを検出
        if is_explanation(sent_stripped, i, sentences):
            break

        law_text += sent

    # 末尾の残りテキスト（句点なし）が解説の場合は除去
    # 例: "目的" のような見出し語
    law_text = law_text.strip()

    return law_text

def is_explanation(sent, idx, all_sentences):
    """文が解説テキストかどうかを判定"""

    # 試験問題番号
    if re.search(r'R\d{2}-\d{2}', sent):
        return True

    # 「〜です。」「〜ます。」で終わる
    if re.search(r'(です|ます|ません|ください|しょう)。$', sent):
        return True

    # 条文参照で終わる（解説での引用）
    if re.search(r'（法\d+条[^）]*）$', sent):
        return True
    if re.search(r'（令\d+条[^）]*）$', sent):
        return True
    if re.search(r'（則\d+条[^）]*）$', sent):
        return True

    # 見出し語で始まる（法文は通常、主語+は、で始まる）
    # 例: "目的", "基本的理念", "保険者の種類"
    explanation_headings = [
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
        '被保険者証', '氏名変更', '住所変更',
        '2以上の事業所', '2024改正', '2026改正',
        '標準報酬月額', '標準賞与額', '定時決定', '随時改定',
        '報酬月額', '賞与額', '保険料', '保険料率',
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
        '不服申立て', '審査請求', '再審査請求',
        '記載事項', '資格確認書', '被扶養者',
    ]

    for heading in explanation_headings:
        if sent.startswith(heading):
            return True

    # 短い見出し語（10文字以下で句点なし）
    if len(sent) <= 15 and '。' not in sent and not re.match(r'◯\d', sent):
        # ただし条文の一部（"同様とする" 等）でないことを確認
        if not sent.endswith('する') and not sent.endswith('ない') and not sent.endswith('できる'):
            return True

    return False

# 全条文を処理
results = []
for item in data:
    ref = item['reference']
    body = item['body']
    paragraphs = extract_law_text(body, ref)
    results.append({
        'reference': ref,
        'paragraphs': paragraphs
    })

# 結果を出力
with open('_health_law_clean.txt', 'w', encoding='utf-8') as out:
    for r in results:
        out.write(f'=== {r["reference"]} ===\n')
        for marker, text in r['paragraphs']:
            if marker:
                out.write(f'  {marker}{text}\n')
            else:
                out.write(f'  {text}\n')
        out.write('\n')

# JSON形式でも保存
with open('_health_law_clean.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f'Processed {len(results)} articles')
for r in results[:5]:
    print(f'\n--- {r["reference"]} ---')
    for marker, text in r['paragraphs']:
        print(f'  {marker}{text[:100]}...' if len(text) > 100 else f'  {marker}{text}')

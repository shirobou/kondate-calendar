"""
社労士テキストPDFから条文を再抽出（PyMuPDF版）
- 赤枠テキスト → <mark> タグ（赤シート対象）
- 太字テキスト → <b> タグ（重要キーワード）
- 不自然な空白を除去
"""
import fitz
import os
import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

PDF_BASE = r"C:\Users\kokor\Desktop\社労士テキストPDF"
OUTPUT_FILE = r"C:\Users\kokor\Desktop\Claude-Personal\extracted_final.json"

SUBJECT_NAMES = {
    "01_労働基準法": "労働基準法",
    "02_労働安全衛生法": "労働安全衛生法",
    "03_労災保険法": "労災保険法",
    "04_雇用保険法": "雇用保険法",
    "05_労働保険徴収法": "労働保険徴収法",
    "06_労働一般常識": "労働一般常識",
    "07_健康保険法": "健康保険法",
    "08_国民年金法": "国民年金法",
    "09_厚生年金保険法": "厚生年金保険法",
    "10_社会保険一般常識": "社会保険一般常識",
}

CJK_MAP = str.maketrans({
    '⽂':'文','⽬':'目','⽤':'用','⽣':'生','⽇':'日','⽉':'月',
    '⼈':'人','⼀':'一','⼆':'二','⼤':'大','⼩':'小','⼦':'子',
    '⾏':'行','⾃':'自','⾄':'至','⾦':'金','⾝':'身','⾮':'非',
    '⼒':'力','⼝':'口','⼟':'土','⼥':'女','⼯':'工','⼿':'手',
    '⽅':'方','⽔':'水','⽕':'火','⽊':'木','⽴':'立','⽩':'白',
    '⽯':'石','⽰':'示','⽶':'米','⾐':'衣','⾷':'食','⾞':'車',
    '⾔':'言','⾜':'足','⾒':'見','⻑':'長','⻘':'青','⾼':'高',
    '⽥':'田','⽸':'缶','⼊':'入','⼋':'八','⼗':'十',
    '⽀':'支','⽐':'比','⽑':'毛','⽚':'片','⽗':'父','⽝':'犬',
    '⽞':'玄','⽟':'玉','⽡':'瓦','⽢':'甘','⽮':'矢',
    '⽲':'禾','⽳':'穴','⽵':'竹','⽷':'糸','⽿':'耳',
    '⾁':'肉','⾂':'臣','⾆':'舌','⾈':'舟',
    '⾊':'色','⾍':'虫','⾎':'血','⻄':'西','⻆':'角',
    '⾨':'門','⾬':'雨','⾳':'音','⾸':'首','⾺':'馬','⾻':'骨',
    '⿂':'魚','⿃':'鳥','⿅':'鹿','⿆':'麦','⿇':'麻','⿊':'黒',
    '⿏':'鼠','⿐':'鼻','⿑':'斉','⿓':'龍','⿔':'亀',
    '⺟':'母','⺠':'民','⻩':'黄','⻫':'斉','⻭':'歯',
    '⼜':'又','⼠':'士','⼭':'山','⼰':'己','⼲':'干','⼼':'心',
    '⼾':'戸','⽋':'欠','⽌':'止','⽒':'氏','⽫':'皿','⽼':'老',
    '⾅':'臼','⾚':'赤','⾯':'面','⾰':'革','⾵':'風','⾶':'飛','⾹':'香',
})


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def get_red_rects(page):
    """ページ内の赤い囲み枠の矩形リストを返す"""
    rects = []
    for d in page.get_drawings():
        c = d.get('color')
        if c and len(c) == 3 and c[0] > 0.7 and c[1] < 0.15 and c[2] < 0.15:
            r = d.get('rect')
            if r and r.width > 12 and 6 < r.height < 40:
                rects.append(r)
    return rects


def is_in_rect(bbox, rects, margin=5):
    """スパンの中心が矩形リスト内にあるか"""
    sx, sy, sx2, sy2 = bbox
    cx = (sx + sx2) / 2
    cy = (sy + sy2) / 2
    for rr in rects:
        if (rr.x0 - margin <= cx <= rr.x1 + margin and
            rr.y0 - margin <= cy <= rr.y1 + margin):
            return True
    return False


def extract_page_lines(page):
    """1ページから (html_line, plain_line, page_num) のリストを返す"""
    red_rects = get_red_rects(page)
    lines = []
    blocks = page.get_text('dict')['blocks']

    for block in blocks:
        if 'lines' not in block:
            continue
        for line in block['lines']:
            html_parts = []
            plain_parts = []
            for span in line['spans']:
                text = span['text'].translate(CJK_MAP)
                if not text:
                    continue
                is_bold = bool(span['flags'] & 16)
                in_red = is_in_rect(span['bbox'], red_rects)
                escaped = esc(text)

                if in_red:
                    html_parts.append(f'<mark>{escaped}</mark>')
                elif is_bold:
                    html_parts.append(f'<b>{escaped}</b>')
                else:
                    html_parts.append(escaped)
                plain_parts.append(text)

            if html_parts:
                lines.append((''.join(html_parts), ''.join(plain_parts)))

    return lines


def clean_html(html_text):
    """条文HTMLの整形: 空白除去 + タグ統合"""
    # 連続する同種タグを統合
    html_text = re.sub(r'</b><b>', '', html_text)
    html_text = re.sub(r'</mark><mark>', '', html_text)
    # 空タグ除去
    html_text = re.sub(r'<b>\s*</b>', '', html_text)
    html_text = re.sub(r'<mark>\s*</mark>', '', html_text)

    # タグを一時退避して空白処理
    tags = []
    def save_tag(m):
        tags.append(m.group(0))
        return chr(0xE000 + len(tags) - 1)
    temp = re.sub(r'</?(?:b|mark)>', save_tag, html_text)

    # 不要な空白を除去
    cleaned = []
    for i, c in enumerate(temp):
        if c == ' ' or c == '\u3000':  # 半角・全角スペース
            prev_c = temp[i-1] if i > 0 else ' '
            next_c = temp[i+1] if i < len(temp)-1 else ' '
            # プライベート領域(タグ)や日本語文字の間のスペースは除去
            p_ja = ord(prev_c) >= 0x3000 or 0xE000 <= ord(prev_c) <= 0xF8FF
            n_ja = ord(next_c) >= 0x3000 or 0xE000 <= ord(next_c) <= 0xF8FF
            p_punc = prev_c in 'はがをにでとのもへやかっ、。）」・'
            n_punc = next_c in 'はがをにでとのもへやかっ、。（「・'
            if p_ja and n_ja:
                continue
            if p_punc or n_punc:
                continue
            if p_ja and n_punc:
                continue
            if p_punc and n_ja:
                continue
        if c == '\u3000':
            continue
        cleaned.append(c)
    temp = ''.join(cleaned)

    # タグ復元
    for i, tag in enumerate(tags):
        temp = temp.replace(chr(0xE000 + i), tag)

    # 再度タグ統合
    temp = re.sub(r'</b><b>', '', temp)
    temp = re.sub(r'</mark><mark>', '', temp)
    temp = re.sub(r'<b>\s*</b>', '', temp)
    temp = re.sub(r'<mark>\s*</mark>', '', temp)

    return temp.strip()


def extract_articles(pdf_path, source_file):
    """PDFから条文を抽出（赤枠+太字付き）"""
    doc = fitz.open(pdf_path)
    all_lines = []
    for page_idx in range(len(doc)):
        page = doc[page_idx]
        page_lines = extract_page_lines(page)
        for html_line, plain_line in page_lines:
            all_lines.append((html_line, plain_line, page_idx + 1))
    doc.close()

    articles = []
    ref_pattern = re.compile(
        r'^(?:<b>)?((?:法|令|則|附則|規則|措置法|整備法|暫定措置法)'
        r'(?:第?\d+条(?:の\d+)?(?:の\d+)?)?'
        r'(?:第?\d+項)?)(?:</b>)?$'
    )
    end_markers = ['重要度', '補足', '選択注意', '学習のポイント', '比較',
                   '過去問', '過去労', '過去社', '過去災', '過去雇',
                   'Copyright', '参考図書']

    i = 0
    in_article = False
    cur_ref = None
    cur_parts = []
    cur_page = 0
    last_importance = ''  # 直近の重要度
    importance_next = False  # 次の行が★マーク

    def save():
        nonlocal cur_ref, cur_parts, cur_page, last_importance
        if cur_ref and cur_parts:
            html = ' '.join(cur_parts)
            html = clean_html(html)
            plain = re.sub(r'</?(?:b|mark)>', '', html)
            if len(plain) >= 10:
                articles.append({
                    "reference": cur_ref,
                    "body_html": html,
                    "body": plain,
                    "source": source_file,
                    "page": cur_page,
                    "importance": last_importance,
                })

    while i < len(all_lines):
        html_l, plain_l, pg = all_lines[i]
        ps = plain_l.strip()

        # 重要度の追跡（条文の前に出現する）
        if importance_next:
            importance_next = False
            star_m = re.match(r'^[特★●―\s]+$', ps)
            if star_m:
                last_importance = ps.replace(' ', '')
                i += 1
                continue
        if ps == '重要度':
            importance_next = True
            # 条文セクション内なら終了マーカーとして扱う
            if in_article:
                save()
                cur_ref = None
                cur_parts = []
                in_article = False
            i += 1
            continue

        if ps == '条文':
            in_article = True
            save()
            cur_ref = None
            cur_parts = []
            i += 1
            continue

        if in_article:
            is_end = any(ps.startswith(m) for m in end_markers)
            if re.match(r'^\d+-\d+', ps) and not re.match(r'^\d+条', ps):
                is_end = True
            if is_end:
                save()
                cur_ref = None
                cur_parts = []
                in_article = False
                i += 1
                continue

            ref_m = ref_pattern.match(html_l.strip())
            if ref_m:
                save()
                cur_ref = ref_m.group(1)
                cur_parts = []
                cur_page = pg
                i += 1
                continue

            if cur_ref is not None:
                cur_parts.append(html_l)
            elif in_article and cur_ref is None:
                # インライン参照
                inline_m = re.match(
                    r'(?:<b>)?((?:法|令|則|附則|規則)(?:第?\d+条(?:の\d+)?(?:の\d+)?)'
                    r'(?:第?\d+項)?)(?:</b>)?\s*(.*)',
                    html_l.strip()
                )
                if inline_m:
                    save()
                    cur_ref = inline_m.group(1)
                    cur_parts = [inline_m.group(2)] if inline_m.group(2) else []
                    cur_page = pg
                else:
                    cur_parts.append(html_l)
        i += 1

    save()
    return articles


def main():
    all_data = {}
    total = 0
    total_marks = 0

    for folder_name in sorted(os.listdir(PDF_BASE)):
        folder_path = os.path.join(PDF_BASE, folder_name)
        if not os.path.isdir(folder_path):
            continue

        subj = SUBJECT_NAMES.get(folder_name, folder_name)
        subj_articles = []

        for pdf_file in sorted(os.listdir(folder_path)):
            if not pdf_file.endswith('.pdf') or pdf_file.startswith('00_') or 'まとめ' in pdf_file:
                continue
            try:
                arts = extract_articles(os.path.join(folder_path, pdf_file), pdf_file)
                subj_articles.extend(arts)
            except Exception as ex:
                print(f"  ERROR {pdf_file}: {ex}")

        # 重複除去
        seen = set()
        unique = []
        for a in subj_articles:
            if a['reference'] not in seen:
                seen.add(a['reference'])
                unique.append(a)

        # 赤シートの数を数える
        marks = sum(a['body_html'].count('<mark>') for a in unique)
        total_marks += marks

        all_data[subj] = unique
        total += len(unique)
        print(f"{subj}: {len(unique)}条文, 赤シート{marks}箇所")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False)

    print(f"\n合計: {total}条文, 赤シート{total_marks}箇所")
    sz = os.path.getsize(OUTPUT_FILE)
    print(f"ファイル: {OUTPUT_FILE} ({sz/1024:.0f}KB)")


if __name__ == '__main__':
    main()

"""
社労士テキストPDFから条文を太字情報付きで再抽出するスクリプト

PyMuPDF(fitz)を使って、太字部分を<b>タグで囲んだHTMLを生成する。
"""
import fitz
import os
import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

PDF_BASE = r"C:\Users\kokor\Desktop\社労士テキストPDF"
OUTPUT_FILE = r"C:\Users\kokor\Desktop\Claude-Personal\extracted_articles_styled.json"

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

# CJK互換文字の正規化テーブル
CJK_MAP = str.maketrans({
    '⽂': '文', '⽬': '目', '⽤': '用', '⽣': '生', '⽇': '日', '⽉': '月',
    '⼈': '人', '⼀': '一', '⼆': '二', '⼤': '大', '⼩': '小', '⼦': '子',
    '⾏': '行', '⾃': '自', '⾄': '至', '⾦': '金', '⾝': '身', '⾮': '非',
    '⼒': '力', '⼝': '口', '⼟': '土', '⼥': '女', '⼯': '工', '⼿': '手',
    '⽅': '方', '⽔': '水', '⽕': '火', '⽊': '木', '⽴': '立', '⽩': '白',
    '⽯': '石', '⽰': '示', '⽶': '米', '⾐': '衣', '⾷': '食', '⾞': '車',
    '⾔': '言', '⾜': '足', '⾒': '見', '⻑': '長', '⻘': '青', '⾼': '高',
    '⽥': '田', '⽸': '缶', '⼊': '入', '⼋': '八', '⼗': '十',
    '⽀': '支', '⽐': '比', '⽑': '毛', '⽚': '片', '⽗': '父', '⽝': '犬',
    '⽞': '玄', '⽟': '玉', '⽡': '瓦', '⽢': '甘', '⽮': '矢',
    '⽲': '禾', '⽳': '穴', '⽵': '竹', '⽷': '糸', '⽿': '耳',
    '⾁': '肉', '⾂': '臣', '⾆': '舌', '⾈': '舟',
    '⾊': '色', '⾍': '虫', '⾎': '血', '⻄': '西', '⻆': '角',
    '⾨': '門', '⾬': '雨', '⾳': '音', '⾸': '首', '⾺': '馬', '⾻': '骨',
    '⿂': '魚', '⿃': '鳥', '⿅': '鹿', '⿆': '麦', '⿇': '麻', '⿊': '黒',
    '⿏': '鼠', '⿐': '鼻', '⿑': '斉', '⿓': '龍', '⿔': '亀',
    '⺟': '母', '⺠': '民', '⻩': '黄', '⻫': '斉', '⻭': '歯',
    '⼜': '又', '⼠': '士', '⼭': '山', '⼰': '己', '⼲': '干', '⼼': '心',
    '⼾': '戸', '⽋': '欠', '⽌': '止', '⽒': '氏', '⽫': '皿', '⽼': '老',
    '⾅': '臼', '⾚': '赤', '⾯': '面', '⾰': '革', '⾵': '風', '⾶': '飛',
    '⾹': '香',
})

def normalize(text):
    return text.translate(CJK_MAP)


def html_escape(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def extract_styled_lines(pdf_path):
    """PDFからスタイル付きテキストをページごとに抽出する。
    各ページ: [(text, is_bold, page_num), ...]
    ただし行単位ではなくスパン単位で返す。
    """
    doc = fitz.open(pdf_path)
    all_lines = []  # [(styled_html_line, plain_text_line, page_num), ...]

    for page_idx, page in enumerate(doc):
        blocks = page.get_text('dict')['blocks']
        for block in blocks:
            if 'lines' not in block:
                continue
            for line in block['lines']:
                html_parts = []
                plain_parts = []
                for span in line['spans']:
                    text = span['text']
                    if not text:
                        continue
                    text = normalize(text)
                    is_bold = bool(span['flags'] & 16)
                    escaped = html_escape(text)

                    if is_bold:
                        html_parts.append(f'<b>{escaped}</b>')
                    else:
                        html_parts.append(escaped)
                    plain_parts.append(text)

                if html_parts:
                    html_line = ''.join(html_parts)
                    plain_line = ''.join(plain_parts)
                    all_lines.append((html_line, plain_line, page_idx + 1))

    doc.close()
    return all_lines


def clean_styled_body(html_text):
    """条文本文のHTML整形: 不要な空白を除去しつつ<b>タグを保持"""
    # <b>タグの前後の空白を除去
    html_text = re.sub(r'\s*(</?b>)\s*', r'\1', html_text)
    # 日本語文字間の空白を除去（ただし<b>タグ内を壊さないよう注意）
    # タグを一時的に置換
    tags = []
    def save_tag(m):
        tags.append(m.group(0))
        return f'\x00TAG{len(tags)-1}\x00'
    temp = re.sub(r'</?b>', save_tag, html_text)
    # 日本語文字間の不要な空白を除去
    temp = re.sub(r'(?<=[\u3000-\u9FFF\uF900-\uFAFF]) (?=[\u3000-\u9FFF\uF900-\uFAFF\u3040-\u309F\u30A0-\u30FF])', '', temp)
    temp = re.sub(r'(?<=[\u3040-\u309F\u30A0-\u30FF]) (?=[\u3000-\u9FFF\uF900-\uFAFF\u3040-\u309F\u30A0-\u30FF])', '', temp)
    # 助詞・記号の前後の空白を除去
    temp = re.sub(r' (?=[はがをにでとのもへやか、。）」])', '', temp)
    temp = re.sub(r'(?<=[（「]) ', '', temp)
    # 残りの余分な空白
    temp = re.sub(r'　', '', temp)  # 全角スペース除去
    temp = re.sub(r' +', ' ', temp)  # 連続半角スペースを1つに
    # タグを復元
    def restore_tag(m):
        idx = int(m.group(0).replace('\x00TAG', '').replace('\x00', ''))
        return tags[idx]
    result = re.sub(r'\x00TAG\d+\x00', restore_tag, temp)
    # 連続する<b></b>を統合
    result = re.sub(r'</b><b>', '', result)
    # 空の<b></b>を除去
    result = re.sub(r'<b></b>', '', result)
    return result.strip()


def extract_articles_styled(pdf_path, source_file):
    """PDFからスタイル付き条文を抽出"""
    lines = extract_styled_lines(pdf_path)
    articles = []

    # 条文参照パターン
    ref_pattern = re.compile(
        r'^<b>((?:法|令|則|附則|規則|措置法|整備法|暫定措置法)'
        r'(?:第?\d+条(?:の\d+)?(?:の\d+)?)?'
        r'(?:第?\d+項)?)</b>$'
    )

    end_markers = [
        '重要度', '補足', '選択注意', '学習のポイント', '比較',
        '過去問', '過去労', '過去社', '過去災', '過去雇',
        'Copyright', '参考図書',
    ]

    i = 0
    in_article_section = False
    current_ref = None
    current_body_parts = []
    current_page = 0

    def save_current():
        nonlocal current_ref, current_body_parts, current_page
        if current_ref and current_body_parts:
            body_html = ' '.join(current_body_parts)
            body_html = clean_styled_body(body_html)
            # プレーンテキスト版も作成（検索用）
            plain = re.sub(r'</?b>', '', body_html)
            if len(plain) >= 10:
                articles.append({
                    "reference": current_ref,
                    "body_html": body_html,
                    "body": plain,
                    "source": source_file,
                    "page": current_page,
                })

    while i < len(lines):
        html_line, plain_line, page_num = lines[i]
        plain_stripped = plain_line.strip()

        # 「条文」ヘッダーを検出（太字の「条文」）
        if plain_stripped == '条文' and '<b>' in html_line:
            in_article_section = True
            save_current()
            current_ref = None
            current_body_parts = []
            i += 1
            continue

        if in_article_section:
            # 終了マーカーチェック
            is_end = False
            for marker in end_markers:
                if plain_stripped.startswith(marker):
                    is_end = True
                    break
            if re.match(r'^\d+-\d+', plain_stripped) and not re.match(r'^\d+条', plain_stripped):
                is_end = True

            if is_end:
                save_current()
                current_ref = None
                current_body_parts = []
                in_article_section = False
                i += 1
                continue

            # 新しい条文参照を検出
            ref_match = ref_pattern.match(html_line.strip())
            if ref_match:
                save_current()
                current_ref = ref_match.group(1)
                current_body_parts = []
                current_page = page_num
                i += 1
                continue

            # 条文本文
            if current_ref is not None:
                current_body_parts.append(html_line)
            elif in_article_section and current_ref is None:
                # インライン参照チェック
                inline_match = re.match(
                    r'<b>((?:法|令|則|附則|規則)(?:第?\d+条(?:の\d+)?(?:の\d+)?)'
                    r'(?:第?\d+項)?)</b>\s*(.*)',
                    html_line.strip()
                )
                if inline_match:
                    save_current()
                    current_ref = inline_match.group(1)
                    current_body_parts = [inline_match.group(2)] if inline_match.group(2) else []
                    current_page = page_num
                else:
                    current_body_parts.append(html_line)

        i += 1

    save_current()
    return articles


def main():
    all_articles = {}
    total_count = 0

    for folder_name in sorted(os.listdir(PDF_BASE)):
        folder_path = os.path.join(PDF_BASE, folder_name)
        if not os.path.isdir(folder_path):
            continue

        subject_name = SUBJECT_NAMES.get(folder_name, folder_name)
        subject_articles = []

        pdf_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.pdf')])
        for pdf_file in pdf_files:
            if pdf_file.startswith('00_') or 'まとめ' in pdf_file:
                continue
            pdf_path = os.path.join(folder_path, pdf_file)
            try:
                articles = extract_articles_styled(pdf_path, pdf_file)
                subject_articles.extend(articles)
            except Exception as ex:
                print(f"  ERROR: {pdf_file}: {ex}")

        # 重複除去
        seen = set()
        unique = []
        for art in subject_articles:
            if art["reference"] not in seen:
                seen.add(art["reference"])
                unique.append(art)

        all_articles[subject_name] = unique
        count = len(unique)
        total_count += count
        print(f"{subject_name}: {count} 条文抽出")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)

    print(f"\n合計: {total_count} 条文")
    print(f"保存先: {OUTPUT_FILE}")


if __name__ == '__main__':
    main()

"""
社労士テキストPDFから条文を抽出するスクリプト

PDFテキストから「条⽂」ヘッダーを検出し、法○条の条文本文を抽出する。
科目ごとにJSON形式で出力する。
"""
import PyPDF2
import os
import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

PDF_BASE = r"C:\Users\kokor\Desktop\社労士テキストPDF"
OUTPUT_FILE = r"C:\Users\kokor\Desktop\Claude-Personal\extracted_articles.json"

# 科目名の正規化マッピング
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


def extract_text_from_pdf(pdf_path):
    """PDFからテキストを全ページ分抽出"""
    text = ""
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def extract_text_with_pages(pdf_path):
    """PDFからテキストをページ番号付きで抽出。各行に(line_text, page_number)を返す"""
    lines_with_pages = []
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page_idx, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                for line in page_text.split('\n'):
                    lines_with_pages.append((line, page_idx + 1))  # 1-indexed
    return lines_with_pages


def normalize_text(text):
    """全角・半角の揺れを正規化"""
    # 丸数字の統一 (◯1 → ① など)
    # CJK互換文字の正規化
    text = text.replace('⽂', '文').replace('⽬', '目').replace('⽤', '用')
    text = text.replace('⽣', '生').replace('⽇', '日').replace('⽉', '月')
    text = text.replace('⼈', '人').replace('⼀', '一').replace('⼆', '二')
    text = text.replace('⼤', '大').replace('⼩', '小').replace('⼦', '子')
    text = text.replace('⾏', '行').replace('⾃', '自').replace('⾄', '至')
    text = text.replace('⾦', '金').replace('⾝', '身').replace('⾮', '非')
    text = text.replace('⼒', '力').replace('⼝', '口').replace('⼟', '土')
    text = text.replace('⼥', '女').replace('⼯', '工').replace('⼿', '手')
    text = text.replace('⽅', '方').replace('⽔', '水').replace('⽕', '火')
    text = text.replace('⽊', '木').replace('⽴', '立').replace('⽩', '白')
    text = text.replace('⽯', '石').replace('⽰', '示').replace('⽶', '米')
    text = text.replace('⾐', '衣').replace('⾷', '食').replace('⾞', '車')
    text = text.replace('⾔', '言').replace('⾜', '足').replace('⾒', '見')
    text = text.replace('⻑', '長').replace('⻘', '青').replace('⾼', '高')
    text = text.replace('⽥', '田').replace('⽬', '目').replace('⽸', '缶')
    text = text.replace('⼊', '入').replace('⼋', '八').replace('⼗', '十')
    text = text.replace('⼆', '二').replace('⼯', '工').replace('⼿', '手')
    text = text.replace('⽀', '支').replace('⽂', '文').replace('⽅', '方')
    text = text.replace('⽊', '木').replace('⽐', '比').replace('⽑', '毛')
    text = text.replace('⽚', '片').replace('⽗', '父').replace('⽝', '犬')
    text = text.replace('⽞', '玄').replace('⽟', '玉').replace('⽡', '瓦')
    text = text.replace('⽢', '甘').replace('⽣', '生').replace('⽤', '用')
    text = text.replace('⽬', '目').replace('⽮', '矢').replace('⽯', '石')
    text = text.replace('⽰', '示').replace('⽲', '禾').replace('⽳', '穴')
    text = text.replace('⽵', '竹').replace('⽷', '糸').replace('⽿', '耳')
    text = text.replace('⾁', '肉').replace('⾂', '臣').replace('⾃', '自')
    text = text.replace('⾄', '至').replace('⾆', '舌').replace('⾈', '舟')
    text = text.replace('⾊', '色').replace('⾍', '虫').replace('⾎', '血')
    text = text.replace('⻄', '西').replace('⻆', '角').replace('⻑', '長')
    text = text.replace('⾨', '門').replace('⾬', '雨').replace('⾳', '音')
    text = text.replace('⾸', '首').replace('⾺', '馬').replace('⾻', '骨')
    text = text.replace('⿂', '魚').replace('⿃', '鳥').replace('⿅', '鹿')
    text = text.replace('⿆', '麦').replace('⿇', '麻').replace('⿊', '黒')
    text = text.replace('⿏', '鼠').replace('⿐', '鼻').replace('⿑', '斉')
    text = text.replace('⿓', '龍').replace('⿔', '亀')
    # 追加: 残りのCJK互換文字
    text = text.replace('⺟', '母').replace('⺠', '民').replace('⻩', '黄')
    text = text.replace('⻫', '斉').replace('⻭', '歯')
    text = text.replace('⼜', '又').replace('⼠', '士').replace('⼭', '山')
    text = text.replace('⼰', '己').replace('⼲', '干').replace('⼼', '心')
    text = text.replace('⼾', '戸').replace('⽋', '欠').replace('⽌', '止')
    text = text.replace('⽒', '氏').replace('⽫', '皿').replace('⽼', '老')
    text = text.replace('⾅', '臼').replace('⾚', '赤').replace('⾯', '面')
    text = text.replace('⾰', '革').replace('⾵', '風').replace('⾶', '飛')
    text = text.replace('⾹', '香')
    return text


def extract_articles_from_text(text, source_file):
    """テキストから条文ブロックを抽出する"""
    articles = []
    text = normalize_text(text)

    # 「条文」ヘッダーを探して、その後の条文ブロックを抽出
    # パターン: "条文" の後に "法○条" が続く
    # 条文ブロックの終了: 次のセクションヘッダー等

    # 条文セクションを分割して探す
    parts = re.split(r'\n\s*条文\s*\n', text)

    for i in range(1, len(parts)):
        block = parts[i]

        # このブロックから個別の条文を抽出
        # 「法○条」「令○条」「則○条」「附則○条」などで始まる条文を探す
        # 条文の終わりは、次の非条文コンテンツ（重要度、補足、選択注意、学習のポイント、比較、過去問等）
        article_pattern = re.compile(
            r'((?:法|令|則|附則|規則|措置法|整備法)(?:第?\d+条(?:の\d+)?(?:第?\d+項)?)?)\s*\n(.*?)(?=\n(?:重要度|補足|選択注意|学習のポイント|比較|過去問|過去労|過去社|過去災|過去雇|Copyright|\d+-\d+(?:-\d+)?\s|条文|法別表|参考図書|$))',
            re.DOTALL
        )

        matches = article_pattern.finditer(block)
        for m in matches:
            article_ref = m.group(1).strip()
            article_body = m.group(2).strip()

            if not article_body or len(article_body) < 10:
                continue

            # 条文本文を整形（余分な空白を除去）
            article_body = re.sub(r'\s+', ' ', article_body).strip()

            articles.append({
                "reference": article_ref,
                "body": article_body,
                "source": source_file,
            })

    return articles


def extract_articles_v2(text, source_file):
    """旧版（互換性のため残す）"""
    lines_with_pages = [(line, 0) for line in text.split('\n')]
    return extract_articles_v3(lines_with_pages, source_file)


def extract_articles_v3(lines_with_pages, source_file):
    """
    ページ番号付き条文抽出（v3）
    lines_with_pages: [(line_text, page_number), ...]
    """
    articles = []

    # テキスト正規化（ページ情報を保持）
    normalized = []
    for line, page in lines_with_pages:
        normalized.append((normalize_text(line), page))

    i = 0
    in_article_section = False
    current_ref = None
    current_body_lines = []
    current_page = 0

    # 条文終了を示すキーワード
    end_markers = [
        '重要度', '補足', '選択注意', '学習のポイント', '比較',
        '過去問', '過去労', '過去社', '過去災', '過去雇',
        'Copyright', '参考図書',
    ]

    # 条文参照パターン（法○条、令○条、則○条など）
    ref_pattern = re.compile(
        r'^((?:法|令|則|附則|規則|措置法|整備法|暫定措置法)'
        r'(?:第?\d+条(?:の\d+)?(?:の\d+)?)?'
        r'(?:第?\d+項)?)\s*$'
    )

    def save_current():
        nonlocal current_ref, current_body_lines, current_page
        if current_ref and current_body_lines:
            body = ' '.join(current_body_lines).strip()
            body = re.sub(r'\s+', ' ', body)
            if len(body) >= 10:
                articles.append({
                    "reference": current_ref,
                    "body": body,
                    "source": source_file,
                    "page": current_page,
                })

    while i < len(normalized):
        line, page = normalized[i]
        line = line.strip()

        # 「条文」ヘッダーを検出
        if line == '条文':
            in_article_section = True
            save_current()
            current_ref = None
            current_body_lines = []
            i += 1
            continue

        if in_article_section:
            # 終了マーカーチェック
            is_end = False
            for marker in end_markers:
                if line.startswith(marker):
                    is_end = True
                    break
            # セクション番号パターン (例: 2-1-1, 1-2 など)
            if re.match(r'^\d+-\d+', line) and not re.match(r'^\d+条', line):
                is_end = True

            if is_end:
                save_current()
                current_ref = None
                current_body_lines = []
                in_article_section = False
                i += 1
                continue

            # 新しい条文参照を検出
            ref_match = ref_pattern.match(line)
            if ref_match:
                save_current()
                current_ref = ref_match.group(1)
                current_body_lines = []
                current_page = page  # 条文が始まったページを記録
                i += 1
                continue

            # 条文本文の一部
            if line and current_ref is not None:
                current_body_lines.append(line)
            elif line and in_article_section and current_ref is None:
                inline_ref = re.match(
                    r'((?:法|令|則|附則|規則)(?:第?\d+条(?:の\d+)?(?:の\d+)?)'
                    r'(?:第?\d+項)?)\s+(.*)',
                    line
                )
                if inline_ref:
                    save_current()
                    current_ref = inline_ref.group(1)
                    current_body_lines = [inline_ref.group(2)]
                    current_page = page
                else:
                    current_body_lines.append(line)

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
            # 合格戦略講座とまとめはスキップ
            if pdf_file.startswith('00_') or 'まとめ' in pdf_file:
                continue

            pdf_path = os.path.join(folder_path, pdf_file)
            try:
                lines_with_pages = extract_text_with_pages(pdf_path)
                articles = extract_articles_v3(lines_with_pages, pdf_file)
                subject_articles.extend(articles)
            except Exception as e:
                print(f"  ERROR: {pdf_file}: {e}")

        # 重複を除去（同じreferenceの条文は最初の出現のみ保持）
        seen = set()
        unique_articles = []
        for art in subject_articles:
            key = art["reference"]
            if key not in seen:
                seen.add(key)
                unique_articles.append(art)

        all_articles[subject_name] = unique_articles
        count = len(unique_articles)
        total_count += count
        print(f"{subject_name}: {count} 条文抽出")

    # 保存
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)

    print(f"\n合計: {total_count} 条文")
    print(f"保存先: {OUTPUT_FILE}")


if __name__ == '__main__':
    main()

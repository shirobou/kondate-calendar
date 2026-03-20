#!/usr/bin/env python3
"""
社労士試験条文の構造化HTMLへの変換スクリプト
入力: struct_input_*.json (reference, body)
出力: structured_*.json (reference, structured)

実行: python process_structured.py
"""
import json
import re
import os
import html


def extract_law_text(body):
    """bodyから条文本文のみを抽出（解説・参照を除去）"""
    if not body or len(body.strip()) < 5:
        return ""

    text = body.strip()

    # 先頭の関連条文参照を除去（例: "、附則3条、厚年附則4条の3第1項 ◯1..."）
    # ◯数字 の前にある短い参照テキストを除去
    m = re.search(r'◯\d', text)
    if m and m.start() > 0 and m.start() < 150:
        prefix = text[:m.start()].strip()
        # 条文参照っぽいパターン（条・項・号、法名など）
        if re.match(r'^[、\s]', prefix) or re.match(r'^[\w・]+条', prefix):
            text = text[m.start():]

    # 先頭の "1号～8号" のような表記を除去
    text = re.sub(r'^[\d号～・\s]+\s*(?=◯|\w)', '', text)

    # 条文本文と解説を分離
    # ◯N で始まる段落に分割
    paragraphs = re.split(r'(◯\d+)', text)

    law_parts = []
    i = 0
    while i < len(paragraphs):
        part = paragraphs[i].strip()
        if re.match(r'^◯\d+$', part):
            if i + 1 < len(paragraphs):
                para_text = part + paragraphs[i + 1]
                i += 2
            else:
                i += 1
                continue
        else:
            para_text = part
            i += 1

        if not para_text.strip():
            continue

        # 条文の文を抽出（解説を除去）
        sentences = []
        current = ""
        paren_depth = 0

        for ch in para_text:
            current += ch
            if ch == '（':
                paren_depth += 1
            elif ch == '）':
                paren_depth = max(0, paren_depth - 1)
            elif ch == '。' and paren_depth == 0:
                sentences.append(current.strip())
                current = ""

        # 残りのテキスト処理
        remaining = current.strip()
        if remaining:
            # 短いタイトル的テキスト（「目的」「管掌」等）は除去
            if len(remaining) <= 30 and not remaining.endswith('。'):
                pass  # 除去
            elif len(remaining) > 30:
                # 長い残りテキストでも解説っぽければ除去
                pass
            # else: 短すぎるタイトルなので除去

        # 条文の文だけを選択（解説文を除去）
        law_sentences = []
        for sent in sentences:
            if not sent:
                continue
            # 解説パターンの検出
            if re.match(r'^R\d{2}-\d{2}', sent):
                break
            if re.match(r'^\d{4}改正', sent):
                break
            if re.match(r'^20\d{2}改正', sent):
                break
            # 口語体は解説
            if re.search(r'(です。|ません。|ください。|ありません。|なります。|いいます。|されています。|できません。|含まれます。)', sent):
                break
            # 過去問参照
            if re.search(r'（\d+-\d+-\d+参照）$', sent):
                break
            # 「◯◯法HP）」で終わる
            if re.search(r'HP）$', sent):
                break
            law_sentences.append(sent)

        if law_sentences:
            law_parts.append(''.join(law_sentences))

    result = ''.join(law_parts)

    # 末尾の短いタイトルテキストを除去（「。」で終わらないもの）
    result = re.sub(r'([。）])([^。）]{1,25})$',
                     lambda m: m.group(1) if not m.group(2).endswith('。') and not m.group(2).endswith('）') else m.group(0),
                     result)

    return result.strip()


def escape_html(text):
    """HTMLエスケープ（既存のspanタグは保持）"""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text


def wrap_logic(text):
    """論理演算子をspanで囲む"""
    for kw in ['並びに', '又は', '若しくは', '及び']:
        text = text.replace(kw, f'<span class="logic">{kw}</span>')
    return text


def wrap_periods(text):
    """数字・期限をspanで囲む"""
    # 既にspanタグ内にある数字はスキップするため、タグ外のみ対象
    patterns = [
        (r'(?<!class=")(\d+歳)', r'<span class="period">\1</span>'),
        (r'(?<!class=")(\d+年)', r'<span class="period">\1</span>'),
        (r'(?<!class=")(\d+月を超え)', r'<span class="period">\1</span>'),
        (r'(?<!class=")(\d+月以内)', r'<span class="period">\1</span>'),
        (r'(?<!class=")(\d+月間)', r'<span class="period">\1</span>'),
        (r'(?<!class=")(\d+日以内)', r'<span class="period">\1</span>'),
        (r'(?<!class=")(\d+日以上)', r'<span class="period">\1</span>'),
        (r'(?<!class=")(\d+人以上)', r'<span class="period">\1</span>'),
        (r'(?<!class=")(\d+人以内)', r'<span class="period">\1</span>'),
        (r'(?<!class=")(\d+,?\d*万円)', r'<span class="period">\1</span>'),
        (r'(?<!class=")(\d+,?\d*円)', r'<span class="period">\1</span>'),
        (r'(?<!class=")(\d+分の\d+)', r'<span class="period">\1</span>'),
        (r'(?<![>\d])(翌月末日)', r'<span class="period">\1</span>'),
        (r'(?<![>\d])(翌日)', r'<span class="period">\1</span>'),
        (r'(?<![>\d])(その日)', r'<span class="period">\1</span>'),
        (r'(\d+年6月)', r'<span class="period">\1</span>'),
        (r'(\d+箇月)', r'<span class="period">\1</span>'),
    ]
    for pat, rep in patterns:
        # spanタグ内にネストしないよう注意
        if '<span class="period">' not in re.sub(pat, rep, text):
            text = re.sub(pat, rep, text)
        else:
            # 安全にやる
            text = re.sub(pat, rep, text)
    return text


def structure_paragraph(para_num, para_text):
    """1つの項を構造化HTMLに変換"""
    html_parts = []

    # ただし書きの分離
    # ◯ の中のただしは除く
    tadashi_pos = -1
    paren_depth = 0
    for idx in range(len(para_text) - 3):
        ch = para_text[idx]
        if ch == '（':
            paren_depth += 1
        elif ch == '）':
            paren_depth = max(0, paren_depth - 1)
        elif paren_depth == 0 and para_text[idx:idx+4] == 'ただし、':
            tadashi_pos = idx
            break

    if tadashi_pos >= 0:
        main_text = para_text[:tadashi_pos].strip()
        exception_text = para_text[tadashi_pos:].strip()
    else:
        main_text = para_text.strip()
        exception_text = ""

    # 号の列挙を検出（1. 2. 3. パターン）
    numbered_items = re.split(r'(?:^|\s)(\d+)\.\s*', main_text)

    # 本文部分（号の前の部分）
    main_body = numbered_items[0].strip() if numbered_items else main_text
    items = []
    j = 1
    while j < len(numbered_items) - 1:
        item_num = numbered_items[j]
        item_text = numbered_items[j + 1].strip()
        items.append((item_num, item_text))
        j += 2

    # --- 本則セクション ---
    html_parts.append('  <div class="principle-section">')

    if para_num:
        html_parts.append(f'    <span class="item-number">第{para_num}項</span>')

    # 主語の抽出
    subject_match = re.match(r'^(.+?)(は、|が、)', main_body)

    if subject_match:
        subject = subject_match.group(1)
        particle = subject_match.group(2)[0]
        remaining = main_body[subject_match.end():]

        subject_html = wrap_logic(subject)
        subject_html = wrap_periods(subject_html)
        html_parts.append(f'    <div class="subject-line"><span class="subject">{subject_html}</span>{particle}、</div>')

        # 条件と述語を分離
        predicate_match = re.search(r'([^、。（）]+。)$', remaining)

        if predicate_match and len(remaining) > len(predicate_match.group(1)):
            conditions_text = remaining[:predicate_match.start()]
            predicate = predicate_match.group(1)

            if conditions_text.strip():
                # 括弧の外の読点で分割
                conditions = split_by_comma(conditions_text)
                if conditions:
                    html_parts.append('    <ul class="condition-list">')
                    for cond in conditions:
                        cond_html = wrap_logic(cond)
                        cond_html = wrap_periods(cond_html)
                        html_parts.append(f'      <li><span class="condition">{cond_html}</span></li>')
                    html_parts.append('    </ul>')

            predicate_html = wrap_logic(predicate)
            predicate_html = wrap_periods(predicate_html)
            html_parts.append(f'    <div class="predicate-line"><span class="predicate">{predicate_html}</span></div>')
        else:
            remaining_html = wrap_logic(remaining)
            remaining_html = wrap_periods(remaining_html)
            html_parts.append(f'    <div class="predicate-line"><span class="predicate">{remaining_html}</span></div>')
    else:
        main_html = wrap_logic(main_body)
        main_html = wrap_periods(main_html)
        html_parts.append(f'    <div class="predicate-line"><span class="predicate">{main_html}</span></div>')

    # 号の列挙
    if items:
        html_parts.append('    <ul class="condition-list">')
        for item_num, item_text in items:
            item_html = wrap_logic(item_text)
            item_html = wrap_periods(item_html)
            html_parts.append(f'      <li><span class="condition">{item_num}. {item_html}</span></li>')
        html_parts.append('    </ul>')

    html_parts.append('  </div>')

    # --- ただし書きセクション ---
    if exception_text:
        html_parts.append('  <div class="exception-section">')
        html_parts.append('    <div class="exception-keyword"><span class="exception">ただし、</span></div>')

        exc_body = exception_text[4:]  # 「ただし、」を除去

        exc_predicate_match = re.search(r'([^、。（）]+。)$', exc_body)

        if exc_predicate_match and len(exc_body) > len(exc_predicate_match.group(1)):
            exc_conditions_text = exc_body[:exc_predicate_match.start()]
            exc_predicate = exc_predicate_match.group(1)

            if exc_conditions_text.strip():
                exc_conditions = split_by_comma(exc_conditions_text)
                if exc_conditions:
                    html_parts.append('    <ul class="condition-list">')
                    for cond in exc_conditions:
                        cond_html = wrap_logic(cond)
                        cond_html = wrap_periods(cond_html)
                        html_parts.append(f'      <li><span class="condition">{cond_html}</span></li>')
                    html_parts.append('    </ul>')

            exc_pred_html = wrap_logic(exc_predicate)
            exc_pred_html = wrap_periods(exc_pred_html)
            html_parts.append(f'    <div class="predicate-line"><span class="exception">{exc_pred_html}</span></div>')
        else:
            exc_html = wrap_logic(exc_body)
            exc_html = wrap_periods(exc_html)
            html_parts.append(f'    <div class="predicate-line"><span class="exception">{exc_html}</span></div>')

        html_parts.append('  </div>')

    return html_parts


def split_by_comma(text):
    """括弧の外にある読点で分割"""
    parts = []
    current = ""
    paren_depth = 0

    for ch in text:
        if ch == '（':
            paren_depth += 1
            current += ch
        elif ch == '）':
            paren_depth = max(0, paren_depth - 1)
            current += ch
        elif ch == '、' and paren_depth == 0:
            if current.strip():
                parts.append(current.strip())
            current = ""
        else:
            current += ch

    if current.strip():
        parts.append(current.strip())

    return parts


def structure_article(body):
    """条文テキストを構造化HTMLに変換"""
    law_text = extract_law_text(body)
    if not law_text or len(law_text) < 5:
        return ""

    # 項の分割
    parts = re.split(r'◯(\d+)', law_text)

    paragraphs = []
    if parts[0].strip():
        paragraphs.append(('', parts[0].strip()))

    i = 1
    while i < len(parts) - 1:
        num = parts[i]
        text = parts[i + 1].strip()
        paragraphs.append((num, text))
        i += 2

    if not paragraphs:
        return ""

    html_parts = ['<div class="law-body">']

    for para_num, para_text in paragraphs:
        para_html = structure_paragraph(para_num, para_text)
        html_parts.extend(para_html)

    html_parts.append('</div>')

    return '\n'.join(html_parts)


def process_file(input_path, output_path):
    """ファイルを処理"""
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    results = []
    for item in data:
        ref = item.get('reference', '')
        body = item.get('body', '')

        structured = structure_article(body)
        results.append({
            'reference': ref,
            'structured': structured
        })

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    total = len(results)
    non_empty = sum(1 for r in results if r['structured'])
    print(f"  Total: {total}, Structured: {non_empty}, Empty: {total - non_empty}")


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    files = [
        ('struct_input_健康保険法.json', 'structured_健康保険法.json'),
        ('struct_input_国民年金法.json', 'structured_国民年金法.json'),
        ('struct_input_厚生年金保険法.json', 'structured_厚生年金保険法.json'),
    ]

    for input_name, output_name in files:
        input_path = os.path.join(base_dir, input_name)
        output_path = os.path.join(base_dir, output_name)
        print(f"Processing {input_name}...")
        process_file(input_path, output_path)
        print(f"  -> {output_name}")

    print("Done! All files processed.")


if __name__ == '__main__':
    main()

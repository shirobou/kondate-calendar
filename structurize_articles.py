#!/usr/bin/env python3
"""
条文プレーンテキストを構造化HTMLに変換するスクリプト。
各条文のbodyを解析し、主語・述語・条件・数字・例外などをHTMLタグでマークアップする。
"""
import json
import re
import sys

def structurize_article(body: str) -> str:
    """条文のbodyテキストを構造化HTMLに変換する"""
    if not body or not body.strip():
        return ""

    # まず条文本文と解説部分を分離する
    # 解説部分は通常、条文の後に続く説明テキスト
    text = body.strip()

    # 項(◯1, ◯2, ◯3...)で分割
    paragraphs = split_paragraphs(text)

    if len(paragraphs) == 0:
        return ""

    result_parts = []
    for para_num, para_text in paragraphs:
        html = process_paragraph(para_num, para_text)
        result_parts.append(html)

    return "\n".join(result_parts)


def split_paragraphs(text: str) -> list:
    """テキストを項番号で分割する。返り値は [(項番号or None, テキスト), ...]"""
    # ◯1, ◯2, etc. で分割
    # まず◯+数字のパターンを探す
    pattern = r'◯(\d+)'

    parts = re.split(pattern, text)

    result = []
    if len(parts) == 1:
        # 項番号なし - 全体を1つとして処理
        result.append((None, text.strip()))
    else:
        # parts[0]が空でなければ、項番号なしの前置テキスト
        if parts[0].strip():
            # 号番号(1号, 2号等)で始まる場合や、かっこ書で始まる場合
            result.append((None, parts[0].strip()))

        # parts[1], parts[2], ... は番号とテキストの交互
        for i in range(1, len(parts), 2):
            num = parts[i]
            txt = parts[i+1].strip() if i+1 < len(parts) else ""
            if txt:
                result.append((num, txt))

    return result


def process_paragraph(para_num, text: str) -> str:
    """1つの項を処理してHTMLにする"""
    # 解説部分を除去（条文の後の解説テキスト）
    text = remove_commentary(text)

    if not text.strip():
        if para_num:
            return f'<span class="para"><span class="koko">◯{para_num}</span></span>'
        return ""

    # 文を構造化
    html = build_structured_html(text)

    if para_num:
        return f'<span class="para"><span class="koko">◯{para_num}</span>\n{html}</span>'
    else:
        return html


def remove_commentary(text: str) -> str:
    """条文本文から解説・補足テキストを除去する"""
    # よくある解説パターンを検出して除去
    # パターン: 条文の後に「○○とは」「○○の場合」などの解説が続く

    # 「。」で文を分割し、条文部分だけを残す
    # 解説は通常、以下のようなパターンで始まる:
    # - 「R0X-0XA」(過去問番号)
    # - 「（法XX条）」で終わる繰り返し
    # - 見出し的なテキスト（短い、述語がない）

    # まず条文の終わりを見つける
    # 条文は通常「〜する。」「〜とする。」「〜ならない。」等で終わる

    sentences = split_sentences(text)

    if not sentences:
        return text

    # 条文本文の終わりを判定
    main_text_end = find_main_text_end(sentences)

    return "。".join(sentences[:main_text_end+1]) + "。" if main_text_end < len(sentences) else text


def split_sentences(text: str) -> list:
    """句点「。」で文を分割（かっこ内の句点は無視）"""
    sentences = []
    current = ""
    paren_depth = 0

    for char in text:
        if char == '（':
            paren_depth += 1
            current += char
        elif char == '）':
            paren_depth -= 1
            current += char
        elif char == '。' and paren_depth <= 0:
            current += char
            sentences.append(current.strip())
            current = ""
        else:
            current += char

    if current.strip():
        sentences.append(current.strip())

    # 末尾の「。」を除去して返す
    return [s.rstrip('。') for s in sentences if s.strip()]


def find_main_text_end(sentences: list) -> int:
    """条文本文の最後の文のインデックスを返す"""
    if not sentences:
        return 0

    last_main = 0
    for i, sent in enumerate(sentences):
        # 解説パターンの検出
        if is_commentary(sent):
            break
        last_main = i

    return last_main


def is_commentary(sent: str) -> bool:
    """その文が解説・補足テキストかどうかを判定"""
    # 過去問番号パターン
    if re.search(r'R\d{2}-\d{2}[A-Z]', sent):
        return True

    # 「（法XX条）」「（法XX条X項）」で終わる繰り返し説明
    if re.search(r'（法\d+条.*?）$', sent):
        return True
    if re.search(r'（則\d+条.*?）$', sent):
        return True

    # 「〜参照」で終わる
    if sent.endswith('参照）'):
        return True

    # 「〜です」「〜ます」「〜ません」 - 解説的な口語体
    if re.search(r'(です|ます|ません|でした|ました|しょう)$', sent):
        return True
    if re.search(r'(です|ます|ません|でした|ました|しょう)。?$', sent):
        return True

    # 改正年
    if re.search(r'^\d{4}改正', sent):
        return True
    if re.search(r'^20\d{2}改正', sent):
        return True

    # 見出し的（非常に短い、述語がない）
    if len(sent) < 15 and not re.search(r'(する|ない|できる|とする|れる|られる)$', sent):
        # ただし号の列挙は除外
        if not re.match(r'\d+\.', sent):
            return True

    # 行政手引
    if '行政手引' in sent:
        return True

    # Q&A
    if 'Q＆A' in sent or 'Q&A' in sent:
        return True

    return False


def build_structured_html(text: str) -> str:
    """テキストを構造化HTMLに変換する"""

    # 号の列挙を処理 (1. 2. 3. や ア イ ウ)
    has_items = bool(re.search(r'(?:^|\s)(\d+)\.\s', text))

    # ただし書きを分離
    main_part, tadashi_parts = split_tadashi(text)

    # メインの条文を構造化
    html = structurize_main(main_part, has_items)

    # ただし書きを追加
    for tp in tadashi_parts:
        tadashi_html = structurize_main(tp, False)
        html += f'\n<div class="indent"><span class="ex">{tadashi_html}</span></div>'

    return html


def split_tadashi(text: str) -> tuple:
    """ただし書きを分離する"""
    # 「ただし、」で分割
    parts = re.split(r'ただし、', text)
    main = parts[0].strip()
    tadashi = [p.strip() for p in parts[1:] if p.strip()]
    return main, tadashi


def structurize_main(text: str, has_items: bool) -> str:
    """メインテキストを構造化する"""

    # 号の列挙を分離して処理
    if has_items:
        return process_with_items(text)

    # 条件節でネスト
    html = process_conditions(text)

    return html


def process_with_items(text: str) -> str:
    """号の列挙がある条文を処理"""
    # 柱書と号を分離
    # パターン: "次の各号" や "次に掲げる" の後に 1. 2. 3. が来る

    # 1. で始まる号を分割
    item_pattern = r'(\d+)\.\s*'
    parts = re.split(item_pattern, text)

    if len(parts) <= 1:
        return process_conditions(text)

    # parts[0] = 柱書, parts[1]=番号, parts[2]=内容, ...
    pillar = parts[0].strip()

    # 柱書を処理
    html = process_conditions(pillar)

    # 各号を処理
    items_html = ""
    for i in range(1, len(parts), 2):
        num = parts[i]
        content = parts[i+1].strip() if i+1 < len(parts) else ""
        if content:
            item_html = apply_markups(content)
            items_html += f'<br>{num}. {item_html} '

    if items_html:
        html += f'\n<div class="indent">{items_html.strip()}</div>'

    return html


def process_conditions(text: str) -> str:
    """条件節を検出してインデント構造にする"""

    # 条件パターン: 「〜場合」「〜とき」「〜において」
    condition_patterns = [
        (r'(.+?)(場合においては|場合において|場合には|場合に|場合は)', 'cd'),
        (r'(.+?)(ときは|ときに)', 'cd'),
    ]

    # まず主語を検出
    result = apply_markups(text)

    # 条件節がある場合はindentで囲む
    # 「〜場合においては、」のパターンを検出
    if re.search(r'場合においては|場合において|場合には|場合に|場合は|ときは|ときに', text):
        result = apply_condition_indent(text)
    else:
        result = apply_markups(text)

    return result


def apply_condition_indent(text: str) -> str:
    """条件節をindentで囲む"""
    # 条件部分と結論部分を分離
    # パターン: 〜場合においては、〜する

    patterns = [
        r'(.*?(?:場合|とき)(?:においては|において|には|に|は))([、,])(.*)',
    ]

    for pattern in patterns:
        m = re.match(pattern, text, re.DOTALL)
        if m:
            condition = m.group(1).strip()
            rest = m.group(3).strip()

            condition_html = apply_markups(condition)
            rest_html = apply_markups(rest)

            # 条件部分にcdクラスを適用
            condition_html = f'<span class="cd">{condition_html}</span>'

            return f'{condition_html}<br>\n<div class="indent">{rest_html}</div>'

    return apply_markups(text)


def apply_markups(text: str) -> str:
    """テキストに各種マークアップを適用する"""
    if not text:
        return ""

    html = text

    # 数字・期限・金額をマークアップ (nクラス)
    # 日数、年数、月数、金額、割合
    number_patterns = [
        (r'(\d+日)', r'<span class="n">\1</span>'),
        (r'(\d+年)', r'<span class="n">\1</span>'),
        (r'(\d+月)', r'<span class="n">\1</span>'),
        (r'(\d+箇月)', r'<span class="n">\1</span>'),
        (r'(\d+円)', r'<span class="n">\1</span>'),
        (r'(\d+歳)', r'<span class="n">\1</span>'),
        (r'(100分の\d+)', r'<span class="n">\1</span>'),
        (r'(1000分の\d+)', r'<span class="n">\1</span>'),
        (r'(\d+分の\d+)', r'<span class="n">\1</span>'),
        (r'(\d+週間)', r'<span class="n">\1</span>'),
        (r'(\d+時間)', r'<span class="n">\1</span>'),
        (r'(\d+人)', r'<span class="n">\1</span>'),
        (r'(\d+万円)', r'<span class="n">\1</span>'),
    ]

    for pattern, replacement in number_patterns:
        html = re.sub(pattern, replacement, html)

    # 述語・結論をマークアップ (vクラス)
    verb_patterns = [
        r'(しなければならない)',
        r'(してはならない)',
        r'(することができる)',
        r'(することができない)',
        r'(するものとする)',
        r'(支給する)',
        r'(支払わなければならない)',
        r'(適用しない)',
        r'(適用する)',
        r'(行うものとする)',
        r'(準用する)',
        r'(を行う)',
        r'(とする(?!。))',  # 文末の「とする」
        r'(免れる)',
        r'(認められる)',
    ]

    for pattern in verb_patterns:
        html = re.sub(pattern, r'<span class="v">\1</span>', html)

    return html


def process_file(input_path: str, output_path: str):
    """1ファイルを処理する"""
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Processing {input_path}: {len(data)} articles")

    result = []
    for i, item in enumerate(data):
        ref = item['reference']
        body = item.get('body', '')

        structured = structurize_article(body)

        result.append({
            'reference': ref,
            'structured': structured
        })

        if (i + 1) % 10 == 0:
            print(f"  Processed {i+1}/{len(data)}")

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Output written to {output_path}: {len(result)} articles")


if __name__ == '__main__':
    base = r'c:\Users\kokor\Desktop\Claude-Personal'

    process_file(
        f'{base}/struct_input_労災保険法.json',
        f'{base}/structured_労災保険法.json'
    )

    process_file(
        f'{base}/struct_input_雇用保険法.json',
        f'{base}/structured_雇用保険法.json'
    )

    print("Done!")

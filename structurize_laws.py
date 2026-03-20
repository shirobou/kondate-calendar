#!/usr/bin/env python3
"""
社労士試験条文を構造化HTMLに変換するスクリプト。
条文本文のみを対象とし、解説部分を除外する。
6要素クラス: subject, condition, logic, period, predicate, exception
"""

import json
import re


def extract_law_text(body):
    """bodyから条文本文のみを抽出し、解説部分を除外する。"""
    if not body or len(body.strip()) < 5:
        return ""

    text = body.strip()

    # 先頭の参照情報（「、附則X条」「、厚年附則X条」など）を除去
    text = re.sub(r'^[、\s]*(?:附則\d+条[^◯]*?|厚年附則[^◯]*?|平成\d+年附則[^◯]*?|令和\d+年附則[^◯]*?)(?=◯|\d|[^\d])', '', text).strip()
    if text.startswith('、'):
        text = text.lstrip('、').strip()

    # 項番号(◯1, ◯2, etc.)で始まる部分を特定
    has_items = bool(re.search(r'◯\d+', text))

    if has_items:
        law_parts = []
        item_pattern = re.compile(r'(◯\d+.*?)(?=◯\d+|$)', re.DOTALL)
        items = item_pattern.findall(text)

        for item in items:
            clean = clean_item_text(item)
            if clean:
                law_parts.append(clean)

        return '\n'.join(law_parts)
    else:
        return clean_item_text(text)


def clean_item_text(text):
    """条文本文から解説部分を除去する。"""
    if not text:
        return ""

    text = text.strip()

    sentences = split_into_sentences(text)
    law_sentences = []

    # 条文の終了を検出するための状態管理
    found_terminal = False  # 述語終止形を見つけたか

    for i, sent in enumerate(sentences):
        if is_commentary(sent, i):
            break

        s = sent.strip()

        # 号リスト（1. 2. 等）やただし書きは条文の続き
        is_continuation = (
            re.match(r'^(?:\d+\.\s|[イロハニホヘトチリヌ][\.\s])', s) or
            s.startswith('ただし') or
            re.match(r'^◯\d+', s) or
            re.match(r'^前項', s)
        )

        # 既に条文の述語終止形を見つけていて、かつ続きでない場合は解説
        if found_terminal and not is_continuation:
            # 次の文が条文の続きかどうかを判定
            # 条文の号リスト等でなければ解説と判断
            break

        law_sentences.append(sent)

        # 述語終止形の検出
        if s.endswith('。') and re.search(
            r'(?:ものとする|こととする|とする|しなければならない|ことができる|'
            r'みなす|適用する|行わせるものとする|妨げない|委任することができる|'
            r'管掌する|設ける|行うものとする|目的とする|寄与する|'
            r'喪失する|取得する|算入する|この限りでない|同様とする)。$', s):
            found_terminal = True

    result = ''.join(law_sentences).strip()
    return result


def remove_trailing_commentary_in_sentence(sent):
    """文末の解説的な付録テキストを除去する。
    例: 'を管掌する。管掌の区分...' → 'を管掌する。'
    ただし条文の号リスト等は保持する。"""
    # 最初の「。」の後に条文らしくないテキストが続く場合
    # → 「。」で切り、残りが解説見出しなら除去
    # これは split_into_sentences で既に分割されているはずだが、
    # 最後の文に「。」がない尾部が含まれることがある
    if '。' not in sent:
        return sent

    # 最後の「。」の後のテキストを確認（カッコ外）
    last_period = find_last_period_outside_parens(sent)
    if last_period < 0 or last_period >= len(sent) - 1:
        return sent

    after = sent[last_period + 1:].strip()
    if not after:
        return sent

    # 残りのテキストが短い見出し的なものか判定
    if len(after) < 30 and not re.match(r'^(?:◯\d+|\d+\.|[イロハニホヘトチリヌ]\.)', after):
        return sent[:last_period + 1]

    return sent


def find_last_period_outside_parens(text):
    """カッコ外の最後の「。」の位置を返す。"""
    paren_depth = 0
    last_pos = -1
    for i, ch in enumerate(text):
        if ch in '（(':
            paren_depth += 1
        elif ch in '）)':
            paren_depth = max(0, paren_depth - 1)
        elif ch == '。' and paren_depth == 0:
            last_pos = i
    return last_pos


def split_into_sentences(text):
    """テキストを文単位で分割する（カッコの入れ子を考慮）。"""
    sentences = []
    current = []
    paren_depth = 0

    for ch in text:
        current.append(ch)
        if ch in '（(':
            paren_depth += 1
        elif ch in '）)':
            paren_depth = max(0, paren_depth - 1)
        elif ch == '。' and paren_depth == 0:
            sentences.append(''.join(current))
            current = []

    if current:
        remaining = ''.join(current).strip()
        if remaining:
            sentences.append(remaining)

    return sentences


def is_commentary(sent, index):
    """文が解説かどうかを判定する。"""
    s = sent.strip()
    if not s:
        return True

    # 最初の文は条文
    if index == 0:
        return False

    # 項番号で始まる文は条文
    if re.match(r'^◯\d+', s):
        return False

    # 号番号で始まる文は条文
    if re.match(r'^(?:\d+\.\s|[イロハニホヘトチリヌ][\.\s])', s):
        return False

    # ただし書きは条文
    if s.startswith('ただし'):
        return False

    # 明らかな解説パターン
    commentary_indicators = [
        r'[A-Z]\d{2}-\d+',       # R07-08B 過去問番号
        r'\d{4}改正',              # 2022改正
        r'(?:例えば|なお、|ちなみに|具体的に|すなわち|つまり)',
        r'(?:ません|ます[。]|です[。]|しょう[。]|ください|できます|なります|あります)',
        r'(?:参照\）|参照）|\d+-\d+-\d+参照)',
        r'ことになります',
        r'注意が必要',
        r'暗記',
        r'出題されて',
        r'ひっかけ',
        r'重要な論点',
        r'捨て問',
        r'HP\）',
        r'称することもあります',
        r'といいます',
        r'いう(?:こと)?になります',
        r'ではありません',
        r'とされて(?:い|おり)',
        r'と考えられ',
        r'に限ります',
        r'のではなく',
        r'が異なります',
        r'が設立されて',
        r'と大別される',
        r'に注意',
        r'この場合',
        r'創設され',
        r'されました',
    ]

    for pattern in commentary_indicators:
        if re.search(pattern, s):
            return True

    # 短い見出しテキスト（「。」がない、20文字以下）
    if len(s) < 25 and '。' not in s and not re.match(r'^[◯\d]', s):
        # 号リストのアイテムは除外
        if not re.match(r'^\d+\.', s):
            return True

    # （法XX条Y項）で終わる参照文
    if re.search(r'（法\d+条[^）]*）\s*$', s) and not re.match(r'^◯\d+', s):
        return True

    return False


def structurize_article(body):
    """条文テキストを構造化HTMLに変換する。"""
    law_text = extract_law_text(body)

    if not law_text or len(law_text.strip()) < 3:
        return ""

    items = split_into_items(law_text)
    if not items:
        return ""

    parts = []
    for item_num, item_text in items:
        part = structurize_item(item_num, item_text)
        if part:
            parts.append(part)

    if not parts:
        return ""

    inner = '\n'.join(parts)
    return f'<div class="law-body">\n{inner}\n</div>'


def split_into_items(text):
    """テキストを項ごとに分割する。
    ◯N は項番号。ただし ◯12以上 のように ◯1+テキスト のケースに注意。
    """
    items = []

    # まず ◯ の位置を全て見つけ、項番号を決定
    markers = list(re.finditer(r'◯(\d+)', text))

    if not markers:
        items.append((None, text.strip()))
        return items

    # 項番号の妥当性チェック: 連番であること
    # 例: ◯1, ◯2, ◯3 → OK
    # ◯1, ◯12 → ◯12 は ◯1 + "2..." の可能性が高い
    parsed_markers = []
    expected_num = 1
    for m in markers:
        raw_num = int(m.group(1))
        start = m.start()
        end = m.end()

        if raw_num == expected_num:
            parsed_markers.append((start, end, raw_num))
            expected_num += 1
        elif raw_num > expected_num and raw_num < expected_num + 5:
            # 飛び番（◯1 → ◯3 等）もあり得る
            parsed_markers.append((start, end, raw_num))
            expected_num = raw_num + 1
        else:
            # ◯12 → ◯1 として解釈し、残りはテキストの一部
            # ◯ + expected_num の桁数分だけ取る
            actual_num_str = str(expected_num)
            raw_str = m.group(1)
            if raw_str.startswith(actual_num_str):
                actual_end = start + 1 + len(actual_num_str)  # ◯ + digits
                parsed_markers.append((start, actual_end, expected_num))
                expected_num += 1
            else:
                # それでもダメなら最初の1桁を項番号とする
                parsed_markers.append((start, start + 2, int(raw_str[0])))
                expected_num = int(raw_str[0]) + 1

    # マーカー間のテキストを項として抽出
    for idx, (start, end, num) in enumerate(parsed_markers):
        if idx + 1 < len(parsed_markers):
            next_start = parsed_markers[idx + 1][0]
            body_text = text[end:next_start].strip()
        else:
            body_text = text[end:].strip()

        if body_text:
            items.append((num, body_text))

    return items


def structurize_item(item_num, text):
    """1つの項を構造化HTMLに変換する。"""
    if not text or len(text.strip()) < 2:
        return ""

    text = text.strip()
    main_text, exception_text = split_proviso(text)

    sections = []

    main_html = structurize_main(main_text)
    if main_html:
        item_marker = f'    <span class="item-number">第{item_num}項</span>\n' if item_num else ''
        sections.append(f'  <div class="principle-section">\n{item_marker}{main_html}\n  </div>')

    if exception_text:
        exc_html = structurize_exception(exception_text)
        if exc_html:
            sections.append(f'  <div class="exception-section">\n{exc_html}\n  </div>')

    return '\n'.join(sections)


def split_proviso(text):
    """本文とただし書きを分割する（カッコ内の「ただし」は無視）。"""
    paren_depth = 0
    for i in range(len(text)):
        ch = text[i]
        if ch in '（(':
            paren_depth += 1
        elif ch in '）)':
            paren_depth = max(0, paren_depth - 1)
        elif paren_depth == 0 and text[i:i+3] == 'ただし':
            return text[:i].strip(), text[i:].strip()

    return text, ""


def structurize_main(text):
    """主文を構造化する。"""
    if not text:
        return ""

    subject, rest = extract_subject(text)

    lines = []

    if subject:
        subj_html = markup_all(esc(subject))
        lines.append(f'    <div class="subject-line"><span class="subject">{subj_html}</span>は、</div>')
        text_to_parse = rest
    else:
        text_to_parse = text

    if not text_to_parse:
        return '\n'.join(lines)

    # 号リスト(1. 2. 3.)を検出
    has_numbered = bool(re.search(r'(?:^|\s)1\.\s', text_to_parse))

    if has_numbered:
        conditions, predicate = extract_with_numbered_list(text_to_parse)
    else:
        conditions, predicate = extract_conditions_and_predicate(text_to_parse)

    if conditions:
        lines.append('    <ul class="condition-list">')
        for cond in conditions:
            marked = markup_all(esc(cond))
            lines.append(f'      <li><span class="condition">{marked}</span></li>')
        lines.append('    </ul>')

    if predicate:
        marked = markup_all(esc(predicate))
        lines.append(f'    <div class="predicate-line"><span class="predicate">{marked}</span></div>')

    return '\n'.join(lines)


def structurize_exception(text):
    """ただし書きを構造化する。"""
    if not text:
        return ""

    inner = text
    if inner.startswith('ただし、'):
        inner = inner[4:]
    elif inner.startswith('ただし'):
        inner = inner[3:]

    lines = []
    lines.append(f'    <span class="exception">ただし、</span>')

    conditions, predicate = extract_conditions_and_predicate(inner)

    if conditions:
        lines.append('    <ul class="condition-list">')
        for cond in conditions:
            marked = markup_all(esc(cond))
            lines.append(f'      <li><span class="condition">{marked}</span></li>')
        lines.append('    </ul>')

    if predicate:
        marked = markup_all(esc(predicate))
        lines.append(f'    <div class="predicate-line"><span class="exception">{marked}</span></div>')

    return '\n'.join(lines)


def extract_subject(text):
    """主語を「は、」で分離する（カッコ外のみ）。"""
    paren_depth = 0
    for i in range(len(text)):
        ch = text[i]
        if ch in '（(':
            paren_depth += 1
        elif ch in '）)':
            paren_depth = max(0, paren_depth - 1)
        elif paren_depth == 0 and text[i:i+2] == 'は、':
            subject = text[:i]
            rest = text[i+2:]
            if len(subject) > 200:
                return "", text
            return subject, rest

    return "", text


def extract_conditions_and_predicate(text):
    """テキストから条件群と述語を抽出する。"""
    if not text:
        return [], ""

    clauses = split_by_commas(text)

    if len(clauses) <= 1:
        return [], text

    predicate = clauses[-1]
    conditions = clauses[:-1]

    # 条件が1つで短い場合はまとめる
    if len(conditions) == 1 and len(conditions[0]) < 8:
        return [], text

    return conditions, predicate


def extract_with_numbered_list(text):
    """号番号付きリストを含むテキストを分解する。"""
    first_num = re.search(r'(?:^|\s)1\.\s', text)

    conditions = []
    predicate = ""

    if first_num:
        prefix = text[:first_num.start()].strip()
        list_text = text[first_num.start():].strip()

        if prefix:
            conditions.append(prefix)

        # 号を個別に抽出
        items = re.split(r'(?=\d+\.\s)', list_text)
        for item in items:
            item = item.strip()
            if item:
                conditions.append(item)

    else:
        return extract_conditions_and_predicate(text)

    return conditions, predicate


def split_by_commas(text):
    """テキストをカッコ外の読点「、」で分割する。"""
    parts = []
    current = []
    paren_depth = 0

    for ch in text:
        if ch in '（(':
            paren_depth += 1
            current.append(ch)
        elif ch in '）)':
            paren_depth = max(0, paren_depth - 1)
            current.append(ch)
        elif ch == '、' and paren_depth == 0:
            parts.append(''.join(current).strip())
            current = []
        else:
            current.append(ch)

    if current:
        remaining = ''.join(current).strip()
        if remaining:
            parts.append(remaining)

    # 短すぎる要素は前の要素と結合
    merged = []
    for p in parts:
        if merged and len(p) < 4:
            merged[-1] = merged[-1] + '、' + p
        else:
            merged.append(p)

    return merged


def esc(text):
    """HTMLエスケープ。"""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def markup_all(text):
    """論理演算子と期間をマークアップする。"""
    text = markup_logic(text)
    text = markup_period(text)
    return text


def markup_logic(text):
    """論理演算子を独立タグでマークアップする。"""
    # 既にspan内の場合はスキップするため、置換は慎重に
    logic_words = ['並びに', '及び', '又は', '若しくは', 'かつ']

    for word in logic_words:
        # spanタグ内でない場所のみ置換
        result = []
        i = 0
        in_tag = False
        while i < len(text):
            if text[i] == '<':
                in_tag = True
                result.append(text[i])
                i += 1
            elif text[i] == '>':
                in_tag = False
                result.append(text[i])
                i += 1
            elif not in_tag and text[i:i+len(word)] == word:
                # この位置がspanタグの内部属性でないか確認
                result.append(f'<span class="logic">{word}</span>')
                i += len(word)
            else:
                result.append(text[i])
                i += 1
        text = ''.join(result)

    return text


def markup_period(text):
    """数字・期限をマークアップする。"""
    patterns = [
        (r'(\d+日以内)', r'<span class="period">\1</span>'),
        (r'(\d+月を超え)', r'<span class="period">\1</span>'),
        (r'(\d+箇月)', r'<span class="period">\1</span>'),
        (r'(\d+歳以上\d+歳未満)', r'<span class="period">\1</span>'),
        (r'(\d+歳(?:以上|未満|以下))', r'<span class="period">\1</span>'),
        (r'(\d+歳)', r'<span class="period">\1</span>'),
        (r'(\d+人以内)', r'<span class="period">\1</span>'),
        (r'(\d+人以上)', r'<span class="period">\1</span>'),
        (r'(\d+分の\d+以上)', r'<span class="period">\1</span>'),
        (r'(事業年度開始前)', r'<span class="period">\1</span>'),
    ]

    for pattern, replacement in patterns:
        # 既にperiodタグがなければ安全に置換
        if 'class="period"' not in text:
            text = re.sub(pattern, replacement, text)
        else:
            # 既にperiodタグがある場合、素の正規表現で位置を確認しながら置換
            new_text = text
            for m in reversed(list(re.finditer(pattern, text))):
                start = m.start()
                preceding = text[max(0, start - 30):start]
                if 'class="period">' not in preceding:
                    new_text = new_text[:start] + f'<span class="period">{m.group(1)}</span>' + new_text[m.end():]
            text = new_text

    return text


def process_file(input_path, output_path):
    """1ファイルを処理する。"""
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    results = []
    for item in data:
        ref = item.get('reference', '')
        body = item.get('body', '')

        if not body or len(body.strip()) < 5:
            results.append({"reference": ref, "structured": ""})
            continue

        try:
            structured = structurize_article(body)
            results.append({"reference": ref, "structured": structured})
        except Exception as e:
            print(f"  ERROR on {ref}: {e}")
            results.append({"reference": ref, "structured": ""})

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    non_empty = sum(1 for r in results if r['structured'])
    empty = sum(1 for r in results if not r['structured'])
    print(f"  Total: {len(results)}, Structured: {non_empty}, Empty: {empty}")


def main():
    base = r'c:\Users\kokor\Desktop\Claude-Personal'

    files = [
        ('struct_input_健康保険法.json', 'structured_健康保険法.json'),
        ('struct_input_国民年金法.json', 'structured_国民年金法.json'),
        ('struct_input_厚生年金保険法.json', 'structured_厚生年金保険法.json'),
    ]

    for input_name, output_name in files:
        input_path = f'{base}\\{input_name}'
        output_path = f'{base}\\{output_name}'
        print(f"Processing: {input_name}")
        process_file(input_path, output_path)
        print()


if __name__ == '__main__':
    main()

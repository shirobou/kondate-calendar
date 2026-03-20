#!/usr/bin/env python3
"""
労災保険法の条文を構造化HTMLに変換するスクリプト。
労働基準法_newと同等品質を目指す。

6要素クラス: subject, condition, logic, period, predicate, exception
構造クラス: law-body, principle-section, exception-section, subject-line,
           condition-list, predicate-line, item-number, logic-item
"""

import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')


# ============================================================
# テキスト抽出: bodyから条文本文のみを取得し解説を除去
# ============================================================

def extract_law_text(body):
    """bodyから条文本文のみを抽出し、解説部分を除外する。"""
    if not body or len(body.strip()) < 5:
        return ""

    text = body.strip()

    # 先頭の参照情報を除去（「、附則X条」「、（法22条）」など）
    text = re.sub(r'^[、\s]*(?:(?:附則|厚年附則|平成\d+年附則|令和\d+年附則)\d+[^◯]*?)(?=◯|\d|[^\d])', '', text).strip()
    # 先頭の「、（法XX条）」パターン
    text = re.sub(r'^[、\s]*（[^）]*）\s*', '', text).strip()
    # 先頭の「、則XX条」パターン
    text = re.sub(r'^[、\s]*則\d+[^◯]*?(?=◯)', '', text).strip()
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
        # 号番号で始まる場合（1号、2号 等）
        m = re.match(r'^(\d+号)\s*(?:◯)?\s*', text)
        if m:
            text = text[m.end():].strip()
        return clean_item_text(text)


def clean_item_text(text):
    """条文本文から解説部分を除去する。"""
    if not text:
        return ""

    text = text.strip()

    sentences = split_into_sentences(text)
    law_sentences = []

    found_terminal = False
    terminal_count = 0

    for i, sent in enumerate(sentences):
        if is_commentary(sent, i):
            break

        s = sent.strip()

        # 重複テキスト検出（解説が条文を繰り返すパターン）
        if i > 0 and len(s) > 20:
            existing = ''.join(law_sentences)
            # 文の一部が既出テキストと重複するか
            for check_len in [20, 15]:
                if len(s) >= check_len:
                    check = s[:check_len]
                    if check in existing:
                        found_terminal = True  # 強制終了
                        break
            if found_terminal and not any(s.startswith(p) for p in ['ただし', 'この場合', '前項', '前2項']):
                break

        is_continuation = (
            re.match(r'^(?:\d+\.\s|[イロハニホヘトチリヌ][\.\s])', s) or
            s.startswith('ただし') or
            re.match(r'^◯\d+', s) or
            re.match(r'^前項', s) or
            re.match(r'^この場合において', s) or
            re.match(r'^前2項', s)
        )

        if found_terminal and not is_continuation:
            break

        law_sentences.append(sent)

        # 述語終止形の検出（広めにマッチ）
        if s.endswith('。') and re.search(
            r'(?:ものとする|こととする|とする|しなければならない|ことができる|'
            r'みなす|適用する|行わせるものとする|妨げない|委任することができる|'
            r'管掌する|設ける|行うものとする|目的とする|寄与する|'
            r'喪失する|取得する|算入する|この限りでない|同様とする|'
            r'行う|支給する|準用する|免れる|とみなす|支払う|'
            r'徴収する|行わない|適用しない|消滅する|制定する|'
            r'支給しない|としない|でなくなる|なくなる|でない|'
            r'減じた額とする|いう|よる|ある)。$', s):
            found_terminal = True
            terminal_count += 1

    result = ''.join(law_sentences).strip()
    return result


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

    if index == 0:
        return False

    if re.match(r'^◯\d+', s):
        return False

    if re.match(r'^(?:\d+\.\s|[イロハニホヘトチリヌ][\.\s])', s):
        return False

    if s.startswith('ただし'):
        return False

    if s.startswith('この場合において'):
        return False

    commentary_indicators = [
        r'[A-Z]\d{2}-\d+',
        r'\d{4}(?:改正|年)',
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
        r'創設され',
        r'されました',
        r'わけではありません',
        r'コンメンタール',
        r'昭和\d+年',
        r'令和\d+年',
        r'平成\d+年',
        r'基発\d+',
        r'基収\d+',
        # 労災特有: 見出し的テキスト
        r'^[^\s。]{2,10}$',  # 短い見出し（句点なし）
    ]

    for pattern in commentary_indicators:
        if re.search(pattern, s):
            return True

    # 短い見出しテキスト（「。」がない、20文字以下）
    if len(s) < 25 and '。' not in s and not re.match(r'^[◯\d]', s):
        if not re.match(r'^\d+\.', s):
            return True

    # （法XX条Y項）で終わる参照文
    if re.search(r'（[^）]*[法則条項].*）\s*$', s) and not re.match(r'^◯\d+', s):
        # ただし条文内の括弧注記は除外
        if len(s) < 40:
            return True

    return False


# ============================================================
# 構造化: 条文テキストをHTMLに変換
# ============================================================

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

    inner = ''.join(parts)
    return f'<div class="law-body">{inner}</div>'


def split_into_items(text):
    """テキストを項ごとに分割する。"""
    items = []

    markers = list(re.finditer(r'◯(\d+)', text))

    if not markers:
        items.append((None, text.strip()))
        return items

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
            parsed_markers.append((start, end, raw_num))
            expected_num = raw_num + 1
        else:
            actual_num_str = str(expected_num)
            raw_str = m.group(1)
            if raw_str.startswith(actual_num_str):
                actual_end = start + 1 + len(actual_num_str)
                parsed_markers.append((start, actual_end, expected_num))
                expected_num += 1
            else:
                parsed_markers.append((start, start + 2, int(raw_str[0])))
                expected_num = int(raw_str[0]) + 1

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

    # メイン文の構造化
    main_sections = structurize_main(main_text, item_num)
    sections.extend(main_sections)

    # ただし書き
    if exception_text:
        exc_html = structurize_exception(exception_text)
        if exc_html:
            sections.append(f'<div class="exception-section">{exc_html}</div>')

    return ''.join(sections)


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


def structurize_main(text, item_num=None):
    """主文を構造化する。複数のprinciple-sectionを返すことがある。"""
    if not text:
        return []

    sections = []

    # 「この場合において」で文を分割
    kono_parts = split_by_konobai(text)

    for part_idx, part_text in enumerate(kono_parts):
        section_html = structurize_single_section(
            part_text,
            item_num if part_idx == 0 else None
        )
        if section_html:
            sections.append(f'<div class="principle-section">{section_html}</div>')

    return sections


def split_by_konobai(text):
    """「この場合において、」で文を分割する（カッコ外のみ）。"""
    parts = []
    paren_depth = 0
    pattern = 'この場合において、'
    last_split = 0

    for i in range(len(text)):
        ch = text[i]
        if ch in '（(':
            paren_depth += 1
        elif ch in '）)':
            paren_depth = max(0, paren_depth - 1)
        elif paren_depth == 0 and text[i:i+len(pattern)] == pattern:
            prev = text[last_split:i].strip()
            if prev:
                parts.append(prev)
            last_split = i

    remaining = text[last_split:].strip()
    if remaining:
        parts.append(remaining)

    return parts if parts else [text]


def structurize_single_section(text, item_num=None):
    """1つのsectionを構造化する。"""
    if not text:
        return ""

    lines = []

    if item_num is not None:
        lines.append(f'<span class="item-number">第{item_num}項</span>')

    # 号リスト(1. 2. 3.)を検出
    has_numbered = bool(re.search(r'(?:^|\s)1\.\s', text))

    # 主語の抽出
    subject, rest = extract_subject(text)

    if subject:
        subj_html = markup_all(esc(subject))
        # subject内のsubjectキーワードを検出
        subj_html = mark_subject_keywords(subj_html)
        lines.append(f'<div class="subject-line">{subj_html}は、</div>')
        text_to_parse = rest
    else:
        # 主語なし：条件で始まるか、定義文か
        cond_start, cond_rest = extract_leading_condition(text)
        if cond_start:
            start_html = markup_all(esc(cond_start))
            start_html = mark_subject_keywords(start_html)
            lines.append(f'<div class="subject-line">{start_html}</div>')
            text_to_parse = cond_rest
        else:
            text_to_parse = text

    if not text_to_parse:
        return ''.join(lines)

    if has_numbered:
        conds, pred = extract_with_numbered_list(text_to_parse)
        if conds:
            lines.append('<ul class="condition-list">')
            for c in conds:
                marked = markup_all(esc(c))
                marked = mark_subject_keywords(marked)
                lines.append(f'<li>{marked}</li>')
            lines.append('</ul>')
        if pred:
            marked = markup_all(esc(pred))
            marked = mark_subject_keywords(marked)
            lines.append(f'<div class="predicate-line">{marked}</div>')
    else:
        conds, pred = extract_conditions_and_predicate(text_to_parse)
        if conds:
            lines.append('<ul class="condition-list">')
            for c in conds:
                marked = markup_all(esc(c))
                marked = mark_subject_keywords(marked)
                # 条件タグを付与するか判定
                if is_true_condition(c):
                    marked = f'<span class="condition">{marked}</span>'
                lines.append(f'<li>{marked}</li>')
            lines.append('</ul>')
        if pred:
            marked = markup_all(esc(pred))
            marked = mark_subject_keywords(marked)
            marked = mark_predicate(marked)
            lines.append(f'<div class="predicate-line">{marked}</div>')
        elif not conds:
            # 条件も述語もない → 全体をsubject-lineに
            if not subject and not lines:
                marked = markup_all(esc(text_to_parse))
                marked = mark_subject_keywords(marked)
                marked = mark_predicate(marked)
                lines.append(f'<div class="subject-line">{marked}</div>')
            elif not any('<div class="predicate-line">' in l for l in lines):
                marked = markup_all(esc(text_to_parse))
                marked = mark_subject_keywords(marked)
                marked = mark_predicate(marked)
                lines.append(f'<div class="predicate-line">{marked}</div>')

    return ''.join(lines)


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
    lines.append('<div class="exception-keyword"><span class="exception">ただし、</span></div>')

    conds, pred = extract_conditions_and_predicate(inner)

    if conds:
        lines.append('<ul class="condition-list">')
        for c in conds:
            marked = markup_all(esc(c))
            marked = mark_subject_keywords(marked)
            if is_true_condition(c):
                marked = f'<span class="condition">{marked}</span>'
            lines.append(f'<li>{marked}</li>')
        lines.append('</ul>')

    if pred:
        marked = markup_all(esc(pred))
        marked = mark_subject_keywords(marked)
        lines.append(f'<div class="predicate-line"><span class="exception">→ {marked}</span></div>')
    elif not conds:
        marked = markup_all(esc(inner))
        marked = mark_subject_keywords(marked)
        lines.append(f'<div class="predicate-line"><span class="exception">{marked}</span></div>')

    return ''.join(lines)


# ============================================================
# 抽出ヘルパー
# ============================================================

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


def extract_leading_condition(text):
    """文頭の条件節（「〜場合においては、」等）を抽出する。"""
    patterns = [
        r'^(.+?場合)においては[、，]\s*',
        r'^(.+?とき)は[、，]\s*',
        r'^(.+?場合)には[、，]\s*',
        r'^(.+?ときは)[、，]\s*',
    ]

    for pat in patterns:
        m = re.match(pat, text)
        if m and len(m.group(1)) < 150:
            return text[:m.end()].rstrip('、，').rstrip() + '、', text[m.end():]

    return "", ""


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
            # prefixに述語が含まれる場合
            prefix_parts = split_by_commas(prefix)
            if len(prefix_parts) > 1:
                predicate_candidate = prefix_parts[-1]
                if has_predicate_ending(predicate_candidate):
                    predicate = predicate_candidate
                    prefix = '、'.join(prefix_parts[:-1])

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


# ============================================================
# 条件判定: conditionタグを付与すべきか
# ============================================================

def is_true_condition(text):
    """テキストが真の条件節かどうかを判定する。
    労働基準法_newのパターン: 「〜場合」「〜とき」「〜限り」等で終わる節のみ。
    """
    t = text.strip().rstrip('、，。')

    # 条件パターン
    condition_endings = [
        r'場合$',
        r'ときは?$',
        r'において$',
        r'においては$',
        r'に際し$',
        r'限り$',
        r'にあっては$',
        r'(?:を|の)理由として$',
        r'によって$',
        r'に基づいて$',
        r'(?:を|が)超え$',
        r'(?:を|が)下る$',
        r'に至った$',
    ]

    for pat in condition_endings:
        if re.search(pat, t):
            return True

    # 「〜した場合」「〜する場合」等の内部パターン
    if re.search(r'場合(?:には|においては|において)', t):
        return True

    return False


def has_predicate_ending(text):
    """述語の終止形を含むかどうか。"""
    t = text.strip()
    return bool(re.search(
        r'(?:する|しない|できる|ならない|とする|いう|行う|支給する|'
        r'準用する|免れる|みなす|ある|よる|適用しない|適用する|'
        r'徴収する|行わない|管掌する)[。]?$', t))


# ============================================================
# マークアップ
# ============================================================

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
    logic_words = ['並びに', '及び', '又は', '若しくは', 'かつ']

    for word in logic_words:
        esc_word = esc(word)
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
            elif not in_tag and text[i:i+len(esc_word)] == esc_word:
                result.append(f'<span class="logic">{esc_word}</span>')
                i += len(esc_word)
            else:
                result.append(text[i])
                i += 1
        text = ''.join(result)

    return text


def markup_period(text):
    """数字・期限をマークアップする。"""
    patterns = [
        (r'(\d+年\d+箇月)', r'<span class="period">\1</span>'),
        (r'(\d+日以内)', r'<span class="period">\1</span>'),
        (r'(\d+日分)', r'<span class="period">\1</span>'),
        (r'(\d+日目)', r'<span class="period">\1</span>'),
        (r'(\d+日間)', r'<span class="period">\1</span>'),
        (r'(\d+日前)', r'<span class="period">\1</span>'),
        (r'(\d+月を超え)', r'<span class="period">\1</span>'),
        (r'(\d+箇月)', r'<span class="period">\1</span>'),
        (r'(\d+年を経過した日)', r'<span class="period">\1</span>'),
        (r'(\d+年間)', r'<span class="period">\1</span>'),
        (r'(\d+年)', r'<span class="period">\1</span>'),
        (r'(\d+歳以上\d+歳未満)', r'<span class="period">\1</span>'),
        (r'(\d+歳(?:以上|未満|以下))', r'<span class="period">\1</span>'),
        (r'(\d+歳)', r'<span class="period">\1</span>'),
        (r'(\d+人以内)', r'<span class="period">\1</span>'),
        (r'(\d+人以上)', r'<span class="period">\1</span>'),
        (r'(100分の\d+(?:以上)?)', r'<span class="period">\1</span>'),
        (r'(10分の\d+)', r'<span class="period">\1</span>'),
        (r'(\d+分の\d+以上)', r'<span class="period">\1</span>'),
        (r'(\d+円)', r'<span class="period">\1</span>'),
    ]

    for pattern, replacement in patterns:
        if 'class="period"' not in text:
            text = re.sub(pattern, replacement, text)
        else:
            new_text = text
            for m in reversed(list(re.finditer(pattern, text))):
                start = m.start()
                preceding = text[max(0, start - 30):start]
                if 'class="period">' not in preceding:
                    new_text = new_text[:start] + f'<span class="period">{m.group(1)}</span>' + new_text[m.end():]
            text = new_text

    return text


# 主語キーワード
SUBJECT_KEYWORDS = [
    '使用者', '事業者', '事業主', '労働者', '被保険者', '受給資格者',
    '政府', '厚生労働大臣', '都道府県労働局長', '都道府県知事',
    '労働基準監督署長', '労働基準監督官', '公共職業安定所長',
    '行政官庁', '市町村長', '国',
    '労働委員会', '所轄労働基準監督署長',
    '労働者災害補償保険', '遺族', '配偶者',
]


def mark_subject_keywords(html):
    """テキスト中の主語キーワードに<span class="subject">を付与する。
    ただし既にタグ内のものはスキップ。"""
    for kw in sorted(SUBJECT_KEYWORDS, key=len, reverse=True):
        esc_kw = esc(kw)
        result = []
        i = 0
        in_tag = False
        in_span = 0  # spanの深さ

        while i < len(html):
            if html[i] == '<':
                in_tag = True
                # subject spanの開始/終了を追跡
                if html[i:].startswith('<span class="subject">'):
                    in_span += 1
                elif html[i:].startswith('</span>') and in_span > 0:
                    in_span -= 1
                result.append(html[i])
                i += 1
            elif html[i] == '>':
                in_tag = False
                result.append(html[i])
                i += 1
            elif not in_tag and in_span == 0 and html[i:i+len(esc_kw)] == esc_kw:
                # 前後のコンテキストを確認（既にsubjectタグ内でないか）
                pre = ''.join(result[-30:]) if len(result) > 30 else ''.join(result)
                if 'class="subject">' not in pre or '</span>' in pre[pre.rfind('class="subject">'):]:
                    result.append(f'<span class="subject">{esc_kw}</span>')
                else:
                    result.append(esc_kw)
                i += len(esc_kw)
            else:
                result.append(html[i])
                i += 1
        html = ''.join(result)

    return html


def mark_predicate(html):
    """述語部分に<span class="predicate">を付与する。"""
    # 末尾の述語パターンを検出
    predicate_patterns = [
        r'(しなければならない。)$',
        r'(してはならない。)$',
        r'(することができる。)$',
        r'(ものとする。)$',
        r'(こととする。)$',
        r'(とする。)$',
        r'(みなす。)$',
        r'(とみなす。)$',
        r'(いう。)$',
        r'(行う。)$',
        r'(支給する。)$',
        r'(準用する。)$',
        r'(管掌する。)$',
        r'(適用しない。)$',
        r'(適用する。)$',
        r'(適用されない。)$',
        r'(免れる。)$',
        r'(徴収する。)$',
        r'(行わない。)$',
        r'(でなければならない。)$',
        r'(支払わなければならない。)$',
        r'(提出しなければならない。)$',
        r'(届け出なければならない。)$',
        r'(受けなければならない。)$',
        r'(支給しない。)$',
        r'(ある。)$',
        r'(よる。)$',
        r'(できる。)$',
        r'(による。)$',
        r'(同様とする。)$',
        r'(この限りでない。)$',
    ]

    for pat in predicate_patterns:
        m = re.search(pat, html)
        if m:
            # タグ内でないか確認
            start = m.start()
            pre = html[max(0, start-20):start]
            if 'class="predicate">' not in pre:
                html = html[:m.start()] + f'<span class="predicate">{m.group(1)}</span>' + html[m.end():]
            break

    return html


# ============================================================
# メイン処理
# ============================================================

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
            # 品質チェック
            check_quality(ref, structured, body)
        except Exception as e:
            print(f"  ERROR on {ref}: {e}")
            import traceback
            traceback.print_exc()
            results.append({"reference": ref, "structured": ""})

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    non_empty = sum(1 for r in results if r['structured'])
    empty = sum(1 for r in results if not r['structured'])
    has_ul = sum(1 for r in results if '<ul' in r.get('structured', ''))
    has_subj = sum(1 for r in results if 'subject' in r.get('structured', ''))
    has_pred = sum(1 for r in results if 'predicate' in r.get('structured', ''))

    print(f"\n=== Summary ===")
    print(f"  Total: {len(results)}")
    print(f"  Structured: {non_empty}, Empty: {empty}")
    print(f"  With <ul>: {has_ul} ({has_ul/max(non_empty,1)*100:.0f}%)")
    print(f"  With subject: {has_subj} ({has_subj/max(non_empty,1)*100:.0f}%)")
    print(f"  With predicate: {has_pred} ({has_pred/max(non_empty,1)*100:.0f}%)")

    # condition比率チェック
    total_text = 0
    cond_text = 0
    for r in results:
        st = r.get('structured', '')
        plain = re.sub(r'<[^>]+>', '', st)
        total_text += len(plain)
        for m in re.finditer(r'<span class="condition">(.*?)</span>', st, re.DOTALL):
            cond_text += len(re.sub(r'<[^>]+>', '', m.group(1)))
    if total_text > 0:
        print(f"  Condition ratio: {cond_text/total_text*100:.1f}%")


def check_quality(ref, html, body):
    """品質チェック: 問題があれば警告を出す。"""
    if not html:
        if len(body.strip()) > 30:
            print(f"  WARNING [{ref}]: Empty structured for non-trivial body ({len(body)} chars)")
        return

    plain = re.sub(r'<[^>]+>', '', html)

    # condition比率チェック
    cond_len = 0
    for m in re.finditer(r'<span class="condition">(.*?)</span>', html, re.DOTALL):
        cond_len += len(re.sub(r'<[^>]+>', '', m.group(1)))
    if len(plain) > 0 and cond_len / len(plain) > 0.5:
        print(f"  WARNING [{ref}]: High condition ratio ({cond_len/len(plain)*100:.0f}%)")

    # 構造の基本チェック
    if '<div class="law-body">' not in html:
        print(f"  WARNING [{ref}]: Missing law-body wrapper")


def main():
    base = r'c:\Users\kokor\Desktop\Claude-Personal'

    input_path = f'{base}\\struct_input_労災保険法.json'
    output_path = f'{base}\\structured_労災保険法_new.json'

    print(f"Processing: 労災保険法")
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print()
    process_file(input_path, output_path)


if __name__ == '__main__':
    main()

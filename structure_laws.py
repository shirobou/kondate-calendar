#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
社労士試験の条文を構造化HTMLに変換するスクリプト
"""

import json
import re
import html


def clean_body(body: str) -> str:
    """条文本文から解説部分・過去問番号等を除去し、純粋な条文テキストを返す"""
    if not body or len(body.strip()) < 5:
        return ""

    # 先頭の「、」や参照条文番号を除去
    body = re.sub(r'^[、）]\s*', '', body)
    body = re.sub(r'^(則附則\d+条の?\d*\s*)', '', body)

    # 過去問番号パターン (R07-災08A 等) を除去
    body = re.sub(r'[RHST]\d{2}-[災雇一般社共厚労安衛健国]\d{2}[A-E]\s*', '', body)

    return body.strip()


def extract_law_text(body: str) -> str:
    """bodyから条文部分のみを抽出する（解説・補足は除外）"""
    if not body:
        return ""

    text = clean_body(body)
    if not text:
        return ""

    return text


def detect_items(text: str):
    """項番号（◯1, ◯2 等）で分割"""
    # ◯数字 パターン
    parts = re.split(r'(◯\d+)', text)
    items = []

    if len(parts) <= 1:
        # 項番号なし → 全体を1項として扱う
        return [(0, text)]

    i = 0
    while i < len(parts):
        if re.match(r'◯\d+', parts[i]):
            num = int(re.search(r'\d+', parts[i]).group())
            if i + 1 < len(parts):
                items.append((num, parts[i + 1].strip()))
                i += 2
            else:
                i += 1
        else:
            if parts[i].strip():
                items.append((0, parts[i].strip()))
            i += 1

    return items if items else [(0, text)]


def split_proviso(text: str):
    """ただし書きで分割"""
    # 「ただし、」で分割
    match = re.search(r'(ただし、|但し、)', text)
    if match:
        main = text[:match.start()].strip()
        proviso = text[match.start():].strip()
        return main, proviso
    return text, None


def find_subject(text: str):
    """主語を検出（「は、」で終わる部分）"""
    # 最初の「は、」を探す
    match = re.search(r'^(.+?)(は、)', text)
    if match:
        subject = match.group(1)
        rest = text[match.end():]
        return subject, rest
    return None, text


def find_predicate(text: str):
    """述語を検出（文末の動詞句）"""
    # 文末のパターン
    patterns = [
        r'(ものとする。?)$',
        r'(しなければならない。?)$',
        r'(することができる。?)$',
        r'(することができない。?)$',
        r'(を徴収する。?)$',
        r'(に処する。?)$',
        r'(を科する。?)$',
        r'(消滅する。?)$',
        r'(成立する。?)$',
        r'(定めるものとする。?)$',
        r'(とする。?)$',
        r'(総称する。?)$',
        r'(をいう。?)$',
        r'(という。?\)。?)$',
        r'(とみなす。?)$',
        r'(適用する。?)$',
        r'(を生ずる。?)$',
        r'(に限る。?\)。?)$',
        r'(を除く。?\)。?)$',
        r'(納付しなければならない。?)$',
        r'(提出しなければならない。?)$',
        r'(届け出なければならない。?)$',
        r'(行わなければならない。?)$',
        r'(命ずることができる。?)$',
        r'(させることができる。?)$',
        r'(行なわせることができる。?)$',
        r'(知らせなければならない。?)$',
        r'(保存しなければならない。?)$',
        r'(備えておかなければならない。?)$',
        r'(交付することができる。?)$',
        r'(承認することができる。?)$',
        r'(延納させることができる。?)$',
        r'(延納することができる。?)$',
        r'(処理することができる。?)$',
        r'(徴収しない。?)$',
        r'(通知しなければならない。?)$',
        r'(報告しなければならない。?)$',
        r'(に消滅する。?)$',
        r'(納付することができる。?)$',
        r'(を徴収する。?)$',
        r'(に任ずるものとする。?)$',
    ]

    for pat in patterns:
        match = re.search(pat, text)
        if match:
            before = text[:match.start()].strip()
            pred = match.group(1)
            return before, pred

    # マッチしない場合、最後の句点で区切る
    last_period = text.rfind('。')
    if last_period > 0:
        # 最後の動詞句を探す
        return text, ""

    return text, ""


def mark_logic(text: str) -> str:
    """論理演算子をマーク"""
    # 「又は」「並びに」「及び」「若しくは」「かつ」をspan.logicで囲む
    for word in ['並びに', '又は', '若しくは', '及び', 'かつ']:
        text = text.replace(word, f'<span class="logic">{word}</span>')
    return text


def mark_periods(text: str) -> str:
    """数字・期限をマーク"""
    # 数字+単位のパターン
    patterns = [
        r'(\d+年間)',
        r'(\d+年)',
        r'(\d+月以内)',
        r'(\d+日以内)',
        r'(\d+日以上)',
        r'(\d+日)',
        r'(\d+万円以上)',
        r'(\d+万円未満)',
        r'(\d+万円以下)',
        r'(\d+万円)',
        r'(\d+円以上)',
        r'(\d+円未満)',
        r'(\d+円)',
        r'(\d+人未満)',
        r'(\d+人以上)',
        r'(\d+人)',
        r'(\d+分の\d+以上)',
        r'(\d+分の\d+)',
        r'(100分の\d+)',
        r'(\d+パーセント)',
        r'(\d+トン未満)',
        r'(\d+トン)',
        r'(翌日)',
        r'(翌月末日)',
        r'(6月1日)',
    ]
    for pat in patterns:
        text = re.sub(pat, r'<span class="period">\1</span>', text)

    # 重複マークを修正
    text = re.sub(r'<span class="period">(<span class="period">.*?</span>.*?)</span>', r'\1', text)

    return text


def escape_html(text: str) -> str:
    """HTMLエスケープ（既存タグは保持）"""
    # &, <, > をエスケープするが、自分で付けたspanタグは除く
    text = text.replace('&', '&amp;')
    # <span と </span> 以外の < > をエスケープ
    # まず一時的にspanタグを保護
    text = text.replace('<span ', '\x00SPAN ')
    text = text.replace('</span>', '\x00/SPAN\x00')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('\x00SPAN ', '<span ')
    text = text.replace('\x00/SPAN\x00', '</span>')
    return text


def get_first_sentence(text: str) -> str:
    """条文の最初の文（最初の。まで）を取得。解説部分は除外"""
    # 条文番号パターンで始まる部分を除去
    text = re.sub(r'^[、）]\s*', '', text)
    text = re.sub(r'^(則?\d+条\d*項?\s*)', '', text)
    text = re.sub(r'^(\d+号\s*)', '', text)

    return text


def extract_pure_law(body: str, reference: str) -> str:
    """解説・過去問・コメンタール等を除去し、純粋な条文のみを抽出"""
    if not body or len(body.strip()) < 5:
        return ""

    text = body.strip()

    # 先頭の参照条文除去
    text = re.sub(r'^[、）]\s*', '', text)
    text = re.sub(r'^(則附則\d+条の?\d*\s*)', '', text)
    text = re.sub(r'^(、[^◯]*?\s+)', '', text)

    # 過去問番号や解説の開始を検出して、そこまでを条文とする
    # 典型的な解説開始パターン
    cut_patterns = [
        r'[RHST]\d{2}-[災雇一般社共厚労安衛健国]\d{2}[A-E]',  # 過去問番号
        r'（コンメンタール',  # コンメンタール参照
        r'趣旨[RHST]\d{2}',  # 趣旨+過去問
        r'[^（）。]+の要件[RHST]',  # 要件+過去問
        r'(?<=[。）])[^◯]*(?:ただし|なお|ちなみに|つまり|したがって|すなわち)',  # 解説的な接続
    ]

    # まず、条文の終わりを探す
    # 条文は通常「。」で終わり、その後に解説や過去問番号が続く
    # 見出し語（太字）の後に解説が始まるパターン

    # 簡易的に: 最初の条文参照（法XX条）の後の解説を除去
    # ◯1 ◯2 等の項がある場合は、全項を含む

    lines = []
    # ◯N で始まる項を検出
    item_pattern = re.compile(r'◯(\d+)')
    items = list(item_pattern.finditer(text))

    if items:
        # 項がある場合、各項の条文を抽出
        for idx, m in enumerate(items):
            start = m.end()
            if idx + 1 < len(items):
                end = items[idx + 1].start()
            else:
                end = len(text)
            item_text = text[start:end].strip()

            # 条文部分のみ（解説開始前まで）
            for cp in cut_patterns:
                cut_match = re.search(cp, item_text)
                if cut_match:
                    item_text = item_text[:cut_match.start()].strip()
                    break

            # 見出し語パターン（解説タイトル）で切る
            title_match = re.search(r'(?<=[。）])\s*[^\s◯]{2,15}(?=[RHST]\d{2}|$)', item_text)
            if title_match and title_match.start() > 10:
                possible_cut = item_text[:title_match.start()].strip()
                if possible_cut.endswith('。') or possible_cut.endswith('）'):
                    item_text = possible_cut

            if item_text:
                lines.append(f'◯{m.group(1)}{item_text}')
    else:
        # 項番号なし
        item_text = text
        for cp in cut_patterns:
            cut_match = re.search(cp, item_text)
            if cut_match:
                item_text = item_text[:cut_match.start()].strip()
                break

        # 見出し語パターンで切る
        title_match = re.search(r'(?<=[。）])\s*[^\s◯（]{2,15}(?=[RHST]\d{2}|[「])', item_text)
        if title_match and title_match.start() > 10:
            possible_cut = item_text[:title_match.start()].strip()
            if possible_cut.endswith('。') or possible_cut.endswith('）'):
                item_text = possible_cut

        lines.append(item_text)

    result = '\n'.join(lines)

    # 最終クリーンアップ
    result = re.sub(r'[RHST]\d{2}-[災雇一般社共厚労安衛健国]\d{2}[A-E]\s*', '', result)
    result = re.sub(r'（コンメンタール[^）]*）', '', result)
    result = re.sub(r'\s+', ' ', result).strip()

    return result


def structurize_item(text: str, item_num: int = 0) -> str:
    """1つの項を構造化HTMLに変換"""
    if not text or len(text.strip()) < 3:
        return ""

    text = text.strip()

    # 項番号除去
    text = re.sub(r'^◯\d+\s*', '', text)

    # ただし書き分離
    main_text, proviso = split_proviso(text)

    html_parts = []

    # 項番号
    if item_num > 0:
        html_parts.append(f'<span class="item-number">第{item_num}項</span>')

    # 主語検出
    subject, rest = find_subject(main_text)

    if subject:
        subject_marked = mark_logic(subject)
        subject_marked = mark_periods(subject_marked)
        html_parts.append(f'<div class="subject-line"><span class="subject">{subject_marked}</span>は、</div>')
    else:
        rest = main_text

    # 述語検出
    middle, predicate = find_predicate(rest)

    # 中間部分（条件）
    if middle.strip():
        middle_marked = mark_logic(middle.strip())
        middle_marked = mark_periods(middle_marked)
        # 列挙がある場合はリスト化
        numbered = re.split(r'(\d+\.\s)', middle_marked)
        if len(numbered) > 2:
            html_parts.append('<ul class="condition-list">')
            i = 0
            while i < len(numbered):
                if re.match(r'\d+\.\s', numbered[i]):
                    if i + 1 < len(numbered):
                        html_parts.append(f'<li><span class="condition">{numbered[i]}{numbered[i+1].strip()}</span></li>')
                        i += 2
                    else:
                        i += 1
                else:
                    if numbered[i].strip():
                        html_parts.append(f'<li><span class="condition">{numbered[i].strip()}</span></li>')
                    i += 1
            html_parts.append('</ul>')
        else:
            html_parts.append(f'<ul class="condition-list"><li><span class="condition">{middle_marked}</span></li></ul>')

    # 述語
    if predicate:
        predicate_marked = mark_periods(predicate)
        html_parts.append(f'<div class="predicate-line"><span class="predicate">{predicate_marked}</span></div>')

    result = '\n'.join(html_parts)

    # ただし書き
    if proviso:
        proviso_marked = mark_logic(proviso)
        proviso_marked = mark_periods(proviso_marked)

        # ただし書きの述語を探す
        proviso_body = re.sub(r'^(ただし、|但し、)', '', proviso).strip()
        prov_middle, prov_pred = find_predicate(proviso_body)

        exception_parts = []
        exception_parts.append('<div class="exception-keyword"><span class="exception">ただし、</span></div>')

        if prov_middle.strip():
            prov_middle_marked = mark_logic(prov_middle.strip())
            prov_middle_marked = mark_periods(prov_middle_marked)
            exception_parts.append(f'<ul class="condition-list"><li><span class="condition">{prov_middle_marked}</span></li></ul>')

        if prov_pred:
            prov_pred_marked = mark_periods(prov_pred)
            exception_parts.append(f'<div class="predicate-line"><span class="exception">{prov_pred_marked}</span></div>')

        result += '\n<div class="exception-section">\n' + '\n'.join(exception_parts) + '\n</div>'

    return result


def structurize(body: str, reference: str) -> str:
    """条文全体を構造化HTMLに変換"""
    if not body or len(body.strip()) < 5:
        return ""

    # 純粋な条文テキストを抽出
    law_text = extract_pure_law(body, reference)
    if not law_text or len(law_text.strip()) < 5:
        return ""

    # 項分割
    items = detect_items(law_text)

    sections = []
    for item_num, item_text in items:
        section_html = structurize_item(item_text, item_num)
        if section_html:
            sections.append(f'<div class="principle-section">\n{section_html}\n</div>')

    if not sections:
        return ""

    return '<div class="law-body">\n' + '\n'.join(sections) + '\n</div>'


def process_file(input_path: str, output_path: str):
    """1ファイルを処理"""
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    results = []
    for item in data:
        ref = item.get('reference', '')
        body = item.get('body', '')

        structured = structurize(body, ref)
        results.append({
            'reference': ref,
            'structured': structured
        })

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Processed {len(results)} items -> {output_path}")
    empty_count = sum(1 for r in results if not r['structured'])
    print(f"  Empty: {empty_count}, Structured: {len(results) - empty_count}")


def main():
    base = r'c:\Users\kokor\Desktop\Claude-Personal'

    files = [
        ('struct_input_労働保険徴収法.json', 'structured_労働保険徴収法.json'),
        ('struct_input_労働一般常識.json', 'structured_労働一般常識.json'),
        ('struct_input_社会保険一般常識.json', 'structured_社会保険一般常識.json'),
    ]

    for inp, out in files:
        input_path = f'{base}\\{inp}'
        output_path = f'{base}\\{out}'
        print(f"Processing: {inp}")
        process_file(input_path, output_path)
        print()


if __name__ == '__main__':
    main()

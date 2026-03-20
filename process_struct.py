#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
条文構造化HTML変換スクリプト
入力: struct_input_労働一般常識.json, struct_input_社会保険一般常識.json
出力: structured_労働一般常識.json, structured_社会保険一般常識.json
"""

import json
import re
import os

def extract_law_text(body):
    """条文本文のみを抽出（解説・コメント部分を除外）"""
    if not body or len(body.strip()) < 10:
        return ""

    # Remove leading markers like "、則XX条" etc at the very start
    text = body.strip()

    # Try to find where commentary begins
    # Common patterns for commentary start:
    commentary_markers = [
        # Title-like markers (Japanese keywords that indicate explanatory text)
        r'(?:^|(?<=。))(?:目的|定義|趣旨|概要|労働組合|民事免責|団体交渉|労働協約|'
        r'有効期間|一般的拘束力|不当労働行為|労働委員会|救済命令等|再審査|'
        r'争議行為の届出義務|公益事業|安全保持施設|労働契約の内容|'
        r'労働者の安全|就業規則|適用除外|基本的理念|紛争の解決|'
        r'退職手当|男女雇用機会均等|職場における|国、事業主|'
        r'募集及び採用|中途採用|治療と就業|外国人雇用|'
        r'報告の徴収|指導、助言|手数料|学校等|特別の法人|'
        r'情報提供|労働者供給事業|派遣先事業所|個人単位|'
        r'離職後|グループ企業|派遣先責任者|'
        r'使命|社会保険労務士の職責|補佐人制度|資格|欠格事由|'
        r'不正行為|審査事項|業務を行い得ない|報告及び検査|懲戒の種類|'
        r'設立の手続|業務の範囲|社員の競業|解散|設立|'
        r'国民健康保険団体連合会|特別療養費|都道府県国民健康保険|'
        r'出産育児交付金|保険料の徴収|支払の一時差止め|時効|'
        r'前期高齢者交付金|医療費適正化|特定健康診査|'
        r'後期高齢者医療広域連合|被保険者|不服申立て|'
        r'要介護状態等|資格の取得|資格の喪失|届出|認定申請|'
        r'介護給付|予防給付)'
        r'(?![をにはがのでもと])'  # Not followed by particles
    ]

    # Find the first occurrence of repeated content or explanatory text
    # Strategy: Look for the pattern where text after the law article repeats
    # with slight modifications (indicating commentary)

    # Split by common law reference patterns like （法XX条）
    # These often mark the boundary between law text and commentary

    return text


def separate_law_and_commentary(body):
    """条文本文と解説を分離する"""
    if not body or len(body.strip()) < 10:
        return "", ""

    text = body.strip()

    # Remove leading rule references like "、則XX条" at start
    text = re.sub(r'^[、・](?:則|法)\d+条(?:の\d+)?(?:第?\d+項)?(?:・\d+項)*\s*', '', text)
    text = re.sub(r'^ただし書', '', text)

    # Pattern: ◯N indicates article items
    # Find the law text portion (ends at a clear boundary)

    # Strategy 1: Find where a "title keyword" appears after a 。
    # These keywords signal explanatory text
    title_keywords = [
        '目的', '定義', '趣旨', '概要', '労働組合', '民事免責', '団体交渉',
        '労働協約', '有効期間', '一般的拘束力', '不当労働行為', '労働委員会',
        '救済命令等', '再審査', '争議行為の届出義務', '公益事業', '安全保持施設',
        '労働契約の内容の理解の促進', '労働者の安全への配慮',
        '就業規則による労働契約の内容の変更', '適用除外', '基本的理念',
        '紛争の解決の援助', '退職手当の保全措置',
        '職場における妊娠', '職場における優越的',
        '男女雇用機会均等推進者', '国、事業主及び労働者の責務',
        '募集及び採用における', '中途採用に関する', '治療と就業の両立',
        '外国人雇用状況', '報告の徴収', '指導、助言及び勧告',
        '手数料', '学校等の行う', '特別の法人の行う', '情報提供',
        '労働者供給事業の禁止', '派遣先事業所単位', '個人単位',
        '離職後1年以内', 'グループ企業への派遣', '派遣先責任者',
        '使命', '社会保険労務士の職責', '補佐人制度', '資格',
        '欠格事由', '不正行為の指示', '審査事項等',
        '業務を行い得ない事件', '報告及び検査', '懲戒の種類',
        '設立の手続', '業務の範囲', '社員の競業の禁止', '解散',
        '設立', '会則を守る義務',
        '国民健康保険団体連合会', '特別療養費', '都道府県国民健康保険運営方針',
        '出産育児交付金', '国民健康保険給付費等交付金', '保険料の徴収',
        '支払の一時差止め', '時効',
        '前期高齢者交付金', '前期高齢者納付金等',
        '医療費適正化基本方針', '特定健康診査等基本指針', '特定健康診査等実施計画',
        '後期高齢者医療', '後期高齢者医療広域連合', '後期高齢者支援金等',
        '不服申立て', '被保険者', '要介護状態等の定義',
        '資格の取得の時期', '資格の喪失の時期', '届出', '認定申請に対する処分',
        '介護給付', '予防給付',
        '育児休業', '出生時育児休業', '介護休業', '子の看護等休暇', '介護休暇',
        '所定外労働の制限', '法定時間外労働の制限', '深夜業の制限',
        '育児のための所定労働時間の短縮', '介護のための所定労働時間の短縮',
        '柔軟な働き方', '育児休業に関する定めの周知',
        '育児休業の取得の状況の公表', '労働者の配置に関する配慮',
        '苦情の自主的解決', '紛争の解決の援助', '調停の委任',
        '報告の徴収並びに助言', '一般事業主行動計画',
        '労働条件の明示', '求人等に関する情報', '個人情報の取扱い',
        '求人の申込み', '求職の申込み', '公共職業安定所による情報提供',
        '特定地方公共団体の責務', '有料職業紹介',
        '特定募集情報等提供事業', '報酬の受領の禁止', '報酬供与の禁止',
        '派遣元における労使協定', '派遣労働者であることの明示',
        '労働者派遣に関する料金', '派遣先への各種通知',
        '日雇労働者', '労働者派遣契約の解除',
        '事業所単位の派遣可能期間', '派遣元事業主',
    ]

    # Find the end of law text
    # Look for a title keyword that appears after a period
    law_end = len(text)

    for keyword in title_keywords:
        # Find keyword that appears after。or at a clear boundary
        idx = text.find(keyword)
        if idx > 0:
            # Check if this is after a 。or at a reasonable boundary
            preceding = text[:idx]
            # Check if the preceding character suggests end of law text
            if preceding and preceding[-1] in '。るいすきなもの':
                law_end = min(law_end, idx)
            # Also check for R0X-0XY (exam reference) patterns before keyword
            if re.search(r'R\d{2}-\d{2}[A-Z]?\s*$', preceding):
                match = re.search(r'R\d{2}-\d{2}[A-Z]?\s*$', preceding)
                law_end = min(law_end, match.start())

    # Also look for patterns like "（法XX条）" followed by explanatory text
    ref_pattern = re.finditer(r'（法\d+条(?:の\d+)?(?:第?\d+項)?）', text)
    for match in ref_pattern:
        end_pos = match.end()
        if end_pos < len(text):
            # Check if what follows looks like commentary
            remaining = text[end_pos:end_pos+20]
            if not remaining.startswith('◯') and not remaining.startswith('第'):
                law_end = min(law_end, match.start())

    # Also detect R0X-0XY exam reference patterns
    exam_ref = re.search(r'R\d{2}-\d{2}', text)
    if exam_ref:
        law_end = min(law_end, exam_ref.start())

    # Also detect year reform markers like "2021改正", "2020改正"
    reform_match = re.search(r'\d{4}改正', text)
    if reform_match:
        law_end = min(law_end, reform_match.start())

    law_text = text[:law_end].strip()

    return law_text, text[law_end:].strip()


def structure_law_text(body, reference):
    """条文本文を構造化HTMLに変換"""
    if not body or len(body.strip()) < 10:
        return ""

    law_text, _ = separate_law_and_commentary(body)

    if not law_text or len(law_text.strip()) < 5:
        return ""

    # Build structured HTML
    html_parts = []
    html_parts.append('<div class="law-body">')

    # Split into items (◯1, ◯2, etc.)
    items = re.split(r'(◯\d+)', law_text)

    sections = []
    if items[0].strip():
        sections.append(('', items[0].strip()))

    i = 1
    while i < len(items):
        marker = items[i] if i < len(items) else ''
        content = items[i+1].strip() if i+1 < len(items) else ''
        sections.append((marker, content))
        i += 2

    for idx, (marker, content) in enumerate(sections):
        if not content:
            continue

        item_num = ''
        if marker:
            num = re.search(r'(\d+)', marker)
            if num:
                item_num = f'第{num.group(1)}項'

        # Process the section content
        section_html = process_section(content, item_num)
        html_parts.append(section_html)

    html_parts.append('</div>')
    return '\n'.join(html_parts)


def process_section(content, item_num=''):
    """1つの項を構造化"""
    parts = []

    # Check for ただし書き
    tadashi_split = re.split(r'(ただし[、,]|但し[、,])', content, maxsplit=1)

    main_text = tadashi_split[0].strip()
    exception_text = ''
    if len(tadashi_split) > 2:
        exception_text = tadashi_split[1] + tadashi_split[2]

    # Process main text
    parts.append('<div class="principle-section">')
    if item_num:
        parts.append(f'<span class="item-number">{item_num}</span>')

    # Try to identify subject and predicate
    main_html = analyze_sentence(main_text)
    parts.append(main_html)
    parts.append('</div>')

    # Process exception (ただし書き)
    if exception_text:
        parts.append('<div class="exception-section">')
        exc_html = analyze_exception(exception_text)
        parts.append(exc_html)
        parts.append('</div>')

    return '\n'.join(parts)


def wrap_logic(text):
    """論理演算子を独立タグで囲む"""
    # Order matters - longer patterns first
    logic_words = [
        ('並びに', '並びに'),
        ('若しくは', '若しくは'),
        ('又は', '又は'),
        ('及び', '及び'),
        ('かつ', 'かつ'),
        ('または', 'または'),
        ('もしくは', 'もしくは'),
    ]

    for word, display in logic_words:
        text = text.replace(word, f'<span class="logic">{display}</span>')

    return text


def wrap_periods(text):
    """数字・期限をperiodタグで囲む"""
    # Match various period/number patterns
    patterns = [
        # X年、X月、X日、X週間 etc
        (r'(\d+(?:\.\d+)?)\s*(年|月|日|週間|箇月|か月|年間)', r'<span class="period">\1\2</span>'),
        # X分のY
        (r'(\d+分の\d+)', r'<span class="period">\1</span>'),
        # X歳
        (r'(\d+歳)', r'<span class="period">\1</span>'),
        # X人
        (r'(\d+人)', r'<span class="period">\1</span>'),
        # X万円
        (r'(\d+万円)', r'<span class="period">\1</span>'),
        # X円
        (r'(\d+円)', r'<span class="period">\1</span>'),
        # 100分のXX
        (r'(100分の\d+)', r'<span class="period">\1</span>'),
        # X時間
        (r'(\d+時間)', r'<span class="period">\1</span>'),
        # X労働日
        (r'(\d+労働日)', r'<span class="period">\1</span>'),
        # X日以内
        (r'(\d+日以内)', r'<span class="period">\1日以内</span>'),
    ]

    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text)

    # Avoid double-wrapping
    text = re.sub(r'<span class="period"><span class="period">([^<]+)</span></span>',
                  r'<span class="period">\1</span>', text)

    return text


def analyze_sentence(text):
    """文を分析して主語・条件・述語に分解"""
    parts = []

    # Find subject: text before first は、
    # Common pattern: "Xは、Y" where X is subject
    subject_match = re.match(r'^(.+?)は[、,]\s*', text)

    if subject_match:
        subject = subject_match.group(1).strip()
        rest = text[subject_match.end():].strip()

        subject = wrap_logic(subject)
        subject = wrap_periods(subject)

        parts.append(f'<div class="subject-line"><span class="subject">{subject}</span>は、</div>')

        # Find predicate: last verb phrase
        predicate = ''
        condition = rest

        # Try to find the predicate (ending pattern)
        pred_patterns = [
            r'(しなければならない。)$',
            r'(することができる。)$',
            r'(することができない。)$',
            r'(してはならない。)$',
            r'(するものとする。)$',
            r'(とする。)$',
            r'(とみなす。)$',
            r'(を生ずる。)$',
            r'(をいう。)$',
            r'(を有する。)$',
            r'(に限る。)$',
            r'(を免れない。)$',
            r'(させることができる。)$',
            r'(させなければならない。)$',
            r'(適用しない。)$',
            r'(適用されない。)$',
            r'(講じなければならない。)$',
            r'(行わなければならない。)$',
            r'(行うことができる。)$',
            r'(定めるものとする。)$',
            r'(努めなければならない。)$',
            r'(講ずるものとする。)$',
            r'(支給する。)$',
            r'(交付する。)$',
            r'(徴収する。)$',
            r'(消滅する。)$',
            r'(設けるものとする。)$',
            r'(受けてはならない。)$',
            r'(行ってはならない。)$',
            r'(与えてはならない。)$',
            r'(取得することができる。)$',
            r'(明示しなければならない。)$',
            r'(届け出なければならない。)$',
            r'(選任しなければならない。)$',
            r'(受理しなければならない。)$',
            r'(紹介してはならない。)$',
            r'(公表しなければならない。)$',
            r'(配慮しなければならない。)$',
            r'(周知しなければならない。)$',
            r'(通知しなければならない。)$',
            r'(報告しなければならない。)$',
            r'(指示することができる。)$',
        ]

        for pat in pred_patterns:
            m = re.search(pat, condition)
            if m:
                predicate = m.group(1)
                condition = condition[:m.start()].strip()
                break

        # Process condition
        condition = wrap_logic(condition)
        condition = wrap_periods(condition)

        # Check if there are numbered items (1. 2. 3. etc)
        numbered_items = re.split(r'(?:^|\s)(\d+)\.\s', condition)

        if len(numbered_items) > 2:
            # Has numbered items
            parts.append('<ul class="condition-list">')
            if numbered_items[0].strip():
                cond_text = numbered_items[0].strip()
                parts.append(f'<li><span class="condition">{cond_text}</span></li>')

            i = 1
            while i < len(numbered_items):
                num = numbered_items[i]
                item_text = numbered_items[i+1].strip() if i+1 < len(numbered_items) else ''
                item_text = item_text.rstrip('。').strip()
                parts.append(f'<li><span class="condition">{num}. {item_text}</span></li>')
                i += 2
            parts.append('</ul>')
        else:
            parts.append('<ul class="condition-list">')
            parts.append(f'<li><span class="condition">{condition}</span></li>')
            parts.append('</ul>')

        if predicate:
            parts.append(f'<div class="predicate-line"><span class="predicate">{predicate}</span></div>')

    else:
        # No clear subject-は pattern
        processed = wrap_logic(text)
        processed = wrap_periods(processed)

        # Try to find predicate
        predicate = ''
        condition = processed

        pred_patterns = [
            r'(しなければならない。)$',
            r'(することができる。)$',
            r'(することができない。)$',
            r'(してはならない。)$',
            r'(するものとする。)$',
            r'(とする。)$',
            r'(をいう。)$',
            r'(を有する。)$',
        ]

        for pat in pred_patterns:
            m = re.search(pat, condition)
            if m:
                predicate = m.group(1)
                condition = condition[:m.start()].strip()
                break

        parts.append('<ul class="condition-list">')
        parts.append(f'<li><span class="condition">{condition}</span></li>')
        parts.append('</ul>')

        if predicate:
            parts.append(f'<div class="predicate-line"><span class="predicate">{predicate}</span></div>')

    return '\n'.join(parts)


def analyze_exception(text):
    """ただし書きを分析"""
    parts = []

    text = wrap_logic(text)
    text = wrap_periods(text)

    parts.append(f'<span class="exception">{text}</span>')

    return '\n'.join(parts)


def process_file(input_path, output_path):
    """ファイルを処理"""
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    results = []
    for item in data:
        ref = item['reference']
        body = item.get('body', '')

        structured = structure_law_text(body, ref)

        results.append({
            'reference': ref,
            'structured': structured
        })

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Processed {len(results)} items -> {output_path}")


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Process 労働一般常識
    process_file(
        os.path.join(base_dir, 'struct_input_労働一般常識.json'),
        os.path.join(base_dir, 'structured_労働一般常識.json')
    )

    # Process 社会保険一般常識
    process_file(
        os.path.join(base_dir, 'struct_input_社会保険一般常識.json'),
        os.path.join(base_dir, 'structured_社会保険一般常識.json')
    )


if __name__ == '__main__':
    main()

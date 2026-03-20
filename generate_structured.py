#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
雇用保険法・労働保険徴収法の条文を構造化HTMLに変換するスクリプト
6要素クラス:
  subject (主語), condition (条件), logic (論理演算子),
  period (数字・期限), predicate (述語), exception (例外)
"""

import json
import re
import html as html_mod


def remove_commentary(text):
    """条文テキストから解説・補足部分を除去し、条文本文のみを残す"""
    if not text or not text.strip():
        return ""

    text = text.strip()

    # 先頭の条文参照を除去
    text = re.sub(r'^[、）・]+\s*', '', text)
    text = re.sub(r'^(?:(?:法|則|令|附則|整備法|整備政令|平成\d+年厚労告\d+号)\d*条(?:の\d+)?(?:\d+項)?[、\s・]*)+\s*', '', text)
    text = re.sub(r'^(?:\d+号(?:かっこ書)?[、\s]*)+', '', text)
    text = re.sub(r'^(?:かっこ書[、\s]*)+', '', text)

    # 解説マーカーで切断
    cut_markers = [
        'R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7',
        '2020改正', '2021改正', '2022改正', '2023改正', '2024改正', '2025改正', '2026改正',
        '（行政手引', '（コンメンタール', '（適用手引', '（厚生労働省',
        '（昭和44年', '（昭和56年',
        '常にどこを学習',
        '育児休業給付金支給申請書については、電子申請',
        '「年少者雇用特例被保険者」',
        '「林業」については、労災保険では',
        '例えば、建築工事',
        '「定年年齢に達したことにより',
    ]

    for marker in cut_markers:
        idx = text.find(marker)
        if idx > 0:
            text = text[:idx].rstrip()

    # 末尾の見出しワードを除去
    tail_patterns = [
        r'(?:趣旨|目的|管掌|定義|概要|離職の定義|強制適用事業|暫定任意適用事業|'
        r'適用除外者[①②③]*(?:（[^）]*）)?|高年齢被保険者の特例|高年齢被保険者|'
        r'短期雇用特例被保険者|日雇労働者|日雇労働被保険者|'
        r'一般被保険者などへの切替、日雇労働被保険者の資格継続|'
        r'確認の通知|被保険者証の交付|資格取得届|資格喪失届|離職票の交付|転勤届|個人番号変更届|'
        r'日雇労働被保険者手帳の交付|'
        r'適用事業所設置（廃止）届|事業主事業所各種変更届|代理人選任・解任届|'
        r'休業等開始時賃金証明書(?:（[^）]*）)?|休業等を行っていた者が離職した場合の賃金の届出|'
        r'教育訓練休暇開始時賃金月額証明書|'
        r'失業等給付の種類|就職への努力|受給資格要件(?:（すべて）)?|'
        r'被保険者期間などの定義|賃金日額（原則）|賃金|'
        r'基本手当の減額|認定手続|基本手当の支給|'
        r'自動変更対象額とは|受給期間|妊娠、出産、育児などの特例|事業開始の特例|待期|'
        r'所定給付日数とは|特定受給資格者|特定理由離職者[①②]*(?:（[^）]*）)?|'
        r'就職困難な受給資格者|'
        r'待期中の訓練延長給付|個別延長給付の対象者|広域延長給付の対象者|'
        r'全国延長給付の対象者|地域延長給付の対象者|延長給付の優先順位|'
        r'失業の認定（公共職業訓練等を受ける受給資格者の場合）|'
        r'傷病手当|高年齢求職者給付金|受給手続|特例一時金|'
        r'公共職業訓練等を受ける場合の特例|'
        r'普通給付|受給日数|受給要件|特例給付|'
        r'日雇労働求職者給付金と基本手当などとの関係|'
        r'支給要件|支給額|支給の効果|支給申請手続(?:（初回）)?|'
        r'移転費|移転費の返還|求職活動支援費の種類|広域求職活動費|短期訓練受講費|'
        r'求職活動関係役務利用費|'
        r'教育訓練給付金支給対象者|受給資格確認|'
        r'教育訓練休暇給付金|教育訓練支援給付金|'
        r'育児休業等給付|支給対象者|支給要件|'
        r'譲渡などの禁止|公課の禁止|未支給の失業等給付|'
        r'未支給の基本手当の請求手続|不正利得の返還命令など|'
        r'基本手当などの給付制限|日雇労働求職者給付金の給付制限|'
        r'就職促進給付の給付制限|教育訓練給付の給付制限|'
        r'高年齢雇用継続給付の給付制限|介護休業給付の給付制限|'
        r'育児休業給付の給付制限|'
        r'就職拒否または受講拒否があった場合の給付制限|離職理由による給付制限|'
        r'延長給付を受けている受給資格者の場合|'
        r'報告などの命令|不利益取扱いの禁止|'
        r'審査請求及び再審査請求|不服理由の制限|時効|'
        r'雇用安定事業|能力開発事業(?:の内容)?|事業などの利用|'
        r'職業訓練受講給付金|給付費に対する国庫負担|国庫負担の特例|'
        # 徴収法
        r'保険関係成立の時期|任意加入の申請|名称、所在地等変更届|'
        r'代理人選任・解任届|保険関係の消滅(?:（任意脱退）)?|'
        r'継続事業|一元適用事業|一括有期事業報告書|一括の要件|'
        r'労働保険料の種類|一般保険料の額|賃金総額の特例|一般保険料率|'
        r'第[123]種特別加入保険料|印紙保険料の額|'
        r'概算保険料の納期限(?:（原則）)?|概算保険料の申告先|概算保険料の延納|'
        r'延納の要件|増加概算保険料[①②]*(?:（[^）]*）)?|概算保険料の追加徴収|'
        r'確定保険料の申告(?:（原則）)?|追徴金の徴収|口座振替による納付|'
        r'印紙保険料の納付|雇用保険印紙購入通帳|雇用保険印紙の購入|'
        r'帳簿の調製及び報告|印紙保険料の認定決定|特例納付保険料制度|'
        r'督促|先取特権の順位|延滞金|'
        r'労働保険事務組合|徴収金の納付責任|帳簿の備付け|報奨金|'
        r'労働保険料の納付義務|賃金からの控除|'
        r'書類の保管|報告・出頭など|立入検査|'
        r'事業主に対する罰則|両罰規定|'
        r'暫定任意適用事業（労災保険法）|労働保険)$'
    ]

    for pat in tail_patterns:
        m = re.search(pat, text)
        if m and m.start() > 5:
            text = text[:m.start()].rstrip()
            break

    return text.strip()


def split_paragraphs(text):
    """◯1, ◯2 で項を分割"""
    parts = re.split(r'(◯\d+)', text)

    paragraphs = []
    i = 0

    # 先頭テキスト（◯なし）
    if parts[0].strip():
        if len(parts) > 2:
            paragraphs.append(parts[0].strip() + parts[1] + parts[2])
            i = 3
        else:
            paragraphs.append(parts[0].strip())
            i = 1
    else:
        i = 1

    while i < len(parts):
        if re.match(r'◯\d+', parts[i]):
            para = parts[i]
            if i + 1 < len(parts):
                para += parts[i + 1]
                i += 2
            else:
                i += 1
            paragraphs.append(para)
        else:
            if paragraphs:
                paragraphs[-1] += parts[i]
            else:
                paragraphs.append(parts[i])
            i += 1

    return paragraphs if paragraphs else [text]


def wrap_logic(text):
    """論理演算子を独立spanタグで囲む"""
    # 長い演算子から先に処理
    operators = ['並びに', '若しくは', '又は', 'かつ', '及び']
    for op in operators:
        text = text.replace(op, f'<span class="logic">{op}</span>')
    return text


def wrap_period(text):
    """数字・期限をperiodタグで囲む"""
    # 複合パターン（長い方を先に）
    patterns = [
        (r'(\d+分の\d+)', r'<span class="period">\1</span>'),
        (r'(100分の\d+)', r'<span class="period">\1</span>'),
        (r'(1,000分の\d+)', r'<span class="period">\1</span>'),
        (r'(\d+箇月以上)', r'<span class="period">\1</span>'),
        (r'(\d+箇月以内)', r'<span class="period">\1</span>'),
        (r'(\d+箇月間)', r'<span class="period">\1</span>'),
        (r'(\d+箇月)', r'<span class="period">\1</span>'),
        (r'(\d+年間)', r'<span class="period">\1</span>'),
        (r'(\d+年以上)', r'<span class="period">\1</span>'),
        (r'(\d+年以内)', r'<span class="period">\1</span>'),
        (r'(\d+年)', r'<span class="period">\1</span>'),
        (r'(\d+月間)', r'<span class="period">\1</span>'),
        (r'(\d+日以上)', r'<span class="period">\1</span>'),
        (r'(\d+日以内)', r'<span class="period">\1</span>'),
        (r'(\d+日間)', r'<span class="period">\1</span>'),
        (r'(\d+日分)', r'<span class="period">\1</span>'),
        (r'(\d+日)', r'<span class="period">\1</span>'),
        (r'(\d+週間)', r'<span class="period">\1</span>'),
        (r'(\d+歳以上)', r'<span class="period">\1</span>'),
        (r'(\d+歳未満)', r'<span class="period">\1</span>'),
        (r'(\d+歳)', r'<span class="period">\1</span>'),
        (r'(\d+(?:万)?円以上)', r'<span class="period">\1</span>'),
        (r'(\d+(?:万)?円以下)', r'<span class="period">\1</span>'),
        (r'(\d+(?:万)?円未満)', r'<span class="period">\1</span>'),
        (r'(\d+(?:万)?円)', r'<span class="period">\1</span>'),
        (r'(\d+,\d{3}円)', r'<span class="period">\1</span>'),
        (r'(\d+パーセント)', r'<span class="period">\1</span>'),
        (r'(\d+人)', r'<span class="period">\1</span>'),
        (r'(翌日)', r'<span class="period">\1</span>'),
        (r'(翌月末日)', r'<span class="period">\1</span>'),
    ]

    for pat, rep in patterns:
        text = re.sub(pat, rep, text)

    # ネストしたspan.periodを修正
    text = re.sub(r'<span class="period">([^<]*)<span class="period">([^<]*)</span>',
                  r'<span class="period">\1\2', text)

    return text


def find_ha_split(text):
    """「は、」で主語と残りを分割（括弧のネストを考慮）"""
    paren_depth = 0
    for i, ch in enumerate(text):
        if ch in '（(':
            paren_depth += 1
        elif ch in '）)':
            paren_depth = max(0, paren_depth - 1)

        if paren_depth == 0 and i < len(text) - 1:
            if text[i:i+2] == 'は、':
                return text[:i], text[i+2:]

    return None, text


def extract_predicate(text):
    """末尾の述語を抽出"""
    pred_endings = [
        'することができる。',
        'しなければならない。',
        'するものとする。',
        'ものとする。',
        'とする。',
        'させることができる。',
        'に消滅する。',
        'が成立する。',
        'が消滅する。',
        'を徴収する。',
        'を支給する。',
        'について支給する。',
        'を支給しない。',
        'に算入しない。',
        'として計算する。',
        'を総称する。',
        'を定めるものとする。',
        'を行うものとする。',
        'とみなす。',
        'に適用する。',
        'を適用する。',
        '適用する。',
        'を命ずることができる。',
        'を返還しなければならない。',
        'に提出しなければならない。',
        'を提出しなければならない。',
        'を納付しなければならない。',
        '納付しなければならない。',
        'を届け出なければならない。',
        '行わなければならない。',
        'を交付しなければならない。',
        'を報告しなければならない。',
        'を徴収しない。',
        'とみなす。',
        'をいう。',
        'に支給する。',
        'に、支給する。',
    ]

    for ending in pred_endings:
        if text.endswith(ending):
            return text[:-len(ending)].rstrip(), ending
        # 。なしバージョンも試す
        ending_no_period = ending.rstrip('。')
        if text.endswith(ending_no_period):
            return text[:-len(ending_no_period)].rstrip(), ending_no_period

    return text, None


def split_numbered_items(text):
    """1. 2. 3. のような列挙を分割"""
    items = re.split(r'(?=\d+\.\s)', text)
    items = [it.strip() for it in items if it.strip()]
    return items


def structure_paragraph(text):
    """単一の項を構造化HTMLに変換"""
    text = text.strip()
    if not text:
        return ""

    # 項番号抽出
    item_num = None
    m = re.match(r'◯(\d+)', text)
    if m:
        item_num = int(m.group(1))
        text = text[m.end():].strip()

    if not text:
        return ""

    html_parts = []
    html_parts.append('<div class="principle-section">')

    if item_num:
        html_parts.append(f'<span class="item-number">第{item_num}項</span>')

    # ただし書き分離
    tadashi = None
    # 括弧のネストを考慮してただし書きを探す
    paren_depth = 0
    tadashi_idx = -1
    for i, ch in enumerate(text):
        if ch in '（(':
            paren_depth += 1
        elif ch in '）)':
            paren_depth = max(0, paren_depth - 1)
        if paren_depth == 0 and text[i:].startswith('ただし、'):
            tadashi_idx = i
            break

    if tadashi_idx > 0:
        tadashi = text[tadashi_idx:]
        text = text[:tadashi_idx].rstrip()

    # 主語分割
    subject, rest = find_ha_split(text)

    if subject:
        subj_html = wrap_logic(subject)
        subj_html = wrap_period(subj_html)
        html_parts.append(f'<div class="subject-line"><span class="subject">{subj_html}</span>は、</div>')

        # 残りから述語を抽出
        condition_text, predicate = extract_predicate(rest)

        # 条件部分を処理
        if condition_text:
            numbered = split_numbered_items(condition_text)
            if len(numbered) > 1:
                html_parts.append('<ul class="condition-list">')
                for ni in numbered:
                    ni_html = wrap_logic(ni)
                    ni_html = wrap_period(ni_html)
                    html_parts.append(f'<li><span class="condition">{ni_html}</span></li>')
                html_parts.append('</ul>')
            else:
                cond_html = wrap_logic(condition_text)
                cond_html = wrap_period(cond_html)
                html_parts.append(f'<ul class="condition-list"><li><span class="condition">{cond_html}</span></li></ul>')

        if predicate:
            pred_html = wrap_period(predicate)
            html_parts.append(f'<div class="predicate-line"><span class="predicate">{pred_html}</span></div>')
    else:
        # 主語なし: 全体を条件として扱う
        condition_text, predicate = extract_predicate(text)
        numbered = split_numbered_items(condition_text)
        if len(numbered) > 1:
            html_parts.append('<ul class="condition-list">')
            for ni in numbered:
                ni_html = wrap_logic(ni)
                ni_html = wrap_period(ni_html)
                html_parts.append(f'<li><span class="condition">{ni_html}</span></li>')
            html_parts.append('</ul>')
        else:
            cond_html = wrap_logic(condition_text)
            cond_html = wrap_period(cond_html)
            html_parts.append(f'<ul class="condition-list"><li><span class="condition">{cond_html}</span></li></ul>')

        if predicate:
            pred_html = wrap_period(predicate)
            html_parts.append(f'<div class="predicate-line"><span class="predicate">{pred_html}</span></div>')

    # ただし書き
    if tadashi:
        tad_html = wrap_logic(tadashi)
        tad_html = wrap_period(tad_html)
        html_parts.append(f'<div class="exception-section"><span class="exception">{tad_html}</span></div>')

    html_parts.append('</div>')
    return '\n'.join(html_parts)


def structure_article(body):
    """条文body全体を構造化HTMLに変換"""
    if not body or len(body.strip()) < 10:
        return ""

    text = remove_commentary(body)
    if not text or len(text) < 10:
        return ""

    paragraphs = split_paragraphs(text)

    parts = ['<div class="law-body">']
    for para in paragraphs:
        para = para.strip()
        if para:
            parts.append(structure_paragraph(para))
    parts.append('</div>')

    return '\n'.join(parts)


def process_file(input_path, output_path):
    """入力JSONを処理して出力"""
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    results = []
    for item in data:
        ref = item['reference']
        body = item.get('body', '')

        structured = structure_article(body)
        results.append({"reference": ref, "structured": structured})

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    empty = sum(1 for r in results if r['structured'] == '')
    print(f"処理完了: {len(results)}件 (空: {empty}件) -> {output_path}")


if __name__ == '__main__':
    base = r'c:\Users\kokor\Desktop\Claude-Personal'

    process_file(
        f'{base}\\struct_input_雇用保険法.json',
        f'{base}\\structured_雇用保険法.json'
    )

    process_file(
        f'{base}\\struct_input_労働保険徴収法.json',
        f'{base}\\structured_労働保険徴収法.json'
    )

#!/usr/bin/env python3
"""
条文をstructured HTMLに変換するスクリプト。
bodyテキストから条文本文部分を抽出し、構造化HTMLを生成する。
"""
import json
import re
import sys


def extract_legal_text(body: str) -> str:
    """bodyから条文本文部分を抽出する（解説・通達部分を除く）"""
    if not body or not body.strip():
        return ""

    # 過去問番号パターン（R07-雇01C等）の前で切る
    # まず項番号(◯1等)で始まる条文をまとめて取得
    # 解説部分の開始を検出するパターン
    commentary_patterns = [
        r'趣旨[A-Z]',
        r'[A-Z]\d{2}-[災雇]\d{2}[A-Z]',  # R06-雇08A等の過去問番号
        r'(?:労働保険|保険関係|継続事業|一括の要件|一元適用|二元適用|暫定任意|保険関係の消滅|任意加入|任意脱退|名称、所在地|代理人選任|変更届|労働保険料の種類|一般保険料の額|賃金総額の特例|一般保険料率|労災保険率|雇用保険率|メリット制|概算保険料|確定保険料|印紙保険料|特別加入|特例納付|追徴金|延滞金|滞納処分|不当労働行為|民事免責|団体交渉|労働組合|労働協約|一般的拘束力|労働者|有効期間|規範的効力|欠格事由|使命|資格|補佐人|不正行為|懲戒|報告及び検査|審査事項|業務を行い得ない)(?![をにはがのでと])',
    ]

    text = body
    return text


def structure_article(body: str, reference: str) -> str:
    """条文テキストを構造化HTMLに変換する"""
    if not body or not body.strip():
        return ""

    text = body.strip()

    # 前処理: 先頭の「）」や「、」で始まるゴミを除去
    text = re.sub(r'^[）、]\s*', '', text)
    # 先頭の条文参照番号を除去 (例: "2号、法9条", "、整備法7条", "、則5条2項" 等)
    text = re.sub(r'^[、]?\s*(?:則附則|整備法|法|則)\d+条(?:の\d+)?(?:\d+項)?(?:\d+号)?[、\s]*', '', text)
    text = re.sub(r'^\d+号[、]?\s*', '', text)
    text = re.sub(r'^、法\d+条、則\d+条\d+号\s*', '', text)
    text = re.sub(r'^、法45条、則76条2号\s*', '', text)
    text = re.sub(r'^、則7条\s*', '', text)

    # 解説部分を除去: 過去問番号パターンの前で切る
    # パターン: 見出し語 + R0X-... or 直接的な解説文
    lines = []

    # まず項(◯1, ◯2等)で分割して条文部分を抽出
    # 条文と解説の境界を見つける

    # 典型的な解説開始パターン
    cut_patterns = [
        # 見出し語（条文の末尾に付く短いタイトル）+ 過去問番号
        r'(?:趣旨|労働保険|保険関係成立|保険関係の消滅|継続事業|有期事業|一元適用事業|二元適用事業|暫定任意適用事業|任意加入|任意脱退|名称.所在地等変更届|代理人選任.解任届|一括の要件|請負事業の一括|労働保険料の種類|一般保険料の額|賃金総額の特例|一般保険料率|労災保険率|雇用保険率|メリット制|概算保険料|確定保険料|印紙保険料|特別加入|特例納付|追徴金|延滞金|滞納処分|認定決定|労働保険事務組合|不当労働行為|民事免責|団体交渉|労働組合|労働協約|一般的拘束力|労働者|有効期間|規範的効力|欠格事由|使命|資格|補佐人制度|不正行為|懲戒|報告及び検査|審査事項|業務を行い得ない|目的|定義|適用事業|被保険者|届出|受給権|時効|費用の負担|国庫負担|罰則|改正|総則|保険給付|通則|老齢|障害|遺族|一時金|年金|手当金|育児休業|介護休業|教育訓練|高年齢|求職者|就職促進|職業紹介|職業訓練|職業安定|労働契約|就業規則|賃金|労働時間|休憩|休日|年次有給休暇|解雇|退職|安全衛生|労災保険|雇用保険|健康保険|厚生年金|国民年金|国民健康保険|介護保険|児童手当|児童扶養手当|特別児童扶養手当|障害者雇用|男女雇用機会均等|育児介護休業|最低賃金|労働者派遣|パートタイム|高齢者雇用|社会保険労務士|確定拠出年金|確定給付企業年金|社会保障協定|船員保険|労働施策|女性活躍|次世代育成|個別労働紛争|労働審判|特定受給資格者|離職証明書|基本手当|所定給付日数|給付制限|傷病手当金|出産手当金|出産育児一時金|報酬|標準報酬|保険料率|積立金|短期給付|長期給付|日雇|任意継続|脱退一時金|合算対象期間|振替加算|加給年金|繰上げ|繰下げ|在職老齢|離婚時|遺族基礎年金|遺族厚生年金|寡婦年金|死亡一時金|障害基礎年金|障害厚生年金|障害手当金|特例老齢)(?:R\d{2}|「|[\s\n])',
    ]

    # シンプルなアプローチ: 条文本文（◯で始まる項を含む）を抽出
    # 解説は通常、見出し語で始まる

    # 条文テキストを構造化
    result = process_text(text, reference)
    return result


def process_text(text: str, reference: str) -> str:
    """テキストを解析して構造化HTMLを生成する"""
    if not text.strip():
        return ""

    # 解説部分を切り離す
    main_text = separate_main_text(text)
    if not main_text.strip():
        return ""

    html_parts = []

    # 項(◯1, ◯2等)で分割
    paragraphs = split_paragraphs(main_text)

    for i, para in enumerate(paragraphs):
        koko_num = para.get('num', '')
        content = para.get('text', '').strip()
        if not content:
            continue

        if i > 0:
            html_parts.append('<span class="para"></span>')

        if koko_num:
            html_parts.append(f'<span class="koko">{koko_num}</span>')

        # 条文テキストを構造化
        structured = structure_content(content)
        html_parts.append(structured)

    return '\n'.join(html_parts)


def separate_main_text(text: str) -> str:
    """条文本文と解説を分離し、条文本文のみ返す"""
    # 過去問番号パターン: R07-雇01C, R06-災08A等
    # これらは解説部分の目印

    # まず全体をスキャンして解説開始位置を見つける

    # パターン1: 短い見出し語の後に解説が続く
    # 例: "...を総称する。労働保険「労働保険」とは..."
    # パターン2: 過去問番号で始まる解説
    # 例: "...成立する。保険関係成立の時期R06-雇08A..."
    # パターン3: 条文参照で終わる解説
    # 例: "...（法1条）"

    # 条文末尾の句点「。」の後に来る見出し語を検出
    # 見出し語は通常漢字のみで構成され短い

    # 簡易的な方法: 最初の完全な条文（項を含む）を抽出
    # ◯N で始まる項があればそれらをすべて含める

    # 条文終了の目印を探す
    result = text

    # パターン: 条文の後に続く解説部分を除去
    # 過去問番号 R0X-YYY が出現したらその直前の見出し語ごと切る
    past_exam = re.search(r'R\d{2}-[災雇]\d{2}[A-Z]', result)
    if past_exam:
        pos = past_exam.start()
        # 過去問番号の前にある見出し語も除去
        # 見出し語は通常、句点の後にある
        before = result[:pos]
        # 最後の句点を探す
        last_period = before.rfind('。')
        if last_period >= 0:
            # 句点の後の文字列が見出し語かチェック
            after_period = before[last_period+1:].strip()
            # 見出し語は通常短い（20文字以内の漢字・カタカナ）
            if len(after_period) <= 30 and re.match(r'^[一-龥ァ-ヶー・（）\s]+$', after_period):
                result = result[:last_period+1]
            else:
                result = before
        else:
            result = before

    # 2回目以降の出現もチェック（解説内の繰り返し）
    # 一般的に、条文が繰り返される部分は解説
    # 「（法XX条）」で終わる参照は解説の一部

    # 条文末の見出し語を除去（句点の後の漢字のみの短い文字列）
    result = re.sub(r'。([一-龥ァ-ヶー・（）]{1,20})$', '。', result)

    return result.strip()


def split_paragraphs(text: str) -> list:
    """テキストを項(◯1, ◯2等)で分割する"""
    paragraphs = []

    # ◯N パターンで分割
    parts = re.split(r'(◯\d+)', text)

    if not parts:
        return [{'num': '', 'text': text}]

    # 最初の部分（◯で始まらない）
    if parts[0].strip():
        paragraphs.append({'num': '', 'text': parts[0].strip()})

    # ◯N + テキスト のペア
    i = 1
    while i < len(parts):
        num = parts[i] if i < len(parts) else ''
        txt = parts[i+1] if i+1 < len(parts) else ''
        if num or txt.strip():
            paragraphs.append({'num': num, 'text': txt.strip()})
        i += 2

    if not paragraphs:
        paragraphs.append({'num': '', 'text': text})

    return paragraphs


def structure_content(text: str) -> str:
    """条文テキストに構造化HTMLタグを適用する"""
    if not text.strip():
        return ""

    # 文を分解して構造化
    result = text

    # 1. 数字・期限・金額をマーク (nクラス)
    # 日数、年数、金額、分数、人数等
    result = mark_numbers(result)

    # 2. ただし書きをマーク (exクラス)
    result = mark_exceptions(result)

    # 3. 条件節をマーク (cdクラス)
    result = mark_conditions(result)

    # 4. 主語をマーク (sクラス)
    result = mark_subjects(result)

    # 5. 述語・結論をマーク (vクラス)
    result = mark_predicates(result)

    # 6. インデント構造を適用
    result = apply_indentation(result)

    return result


def mark_numbers(text: str) -> str:
    """数字・期限・金額を<span class="n">でマークする"""
    # 数字を含む表現をマーク
    patterns = [
        # 分数: X分のY
        (r'(\d+分の\d+)', r'<span class="n">\1</span>'),
        # 年月日期限: X日以内、X年、X月、X箇月
        (r'(\d+日以内)', r'<span class="n">\1</span>'),
        (r'(\d+日前)', r'<span class="n">\1</span>'),
        (r'(\d+日間)', r'<span class="n">\1</span>'),
        (r'(\d+年以内)', r'<span class="n">\1</span>'),
        (r'(\d+年間)', r'<span class="n">\1</span>'),
        (r'(\d+年)', r'<span class="n">\1</span>'),
        (r'(\d+箇月)', r'<span class="n">\1</span>'),
        (r'(\d+月\d+日)', r'<span class="n">\1</span>'),
        # 人数
        (r'(\d+人以上)', r'<span class="n">\1</span>'),
        (r'(\d+人未満)', r'<span class="n">\1</span>'),
        (r'(\d+人以下)', r'<span class="n">\1</span>'),
        # 金額
        (r'(\d+万円)', r'<span class="n">\1</span>'),
        (r'(\d+円)', r'<span class="n">\1</span>'),
        # トン数
        (r'(\d+トン)', r'<span class="n">\1</span>'),
        # パーセント
        (r'(\d+パーセント)', r'<span class="n">\1</span>'),
        (r'(\d+％)', r'<span class="n">\1</span>'),
        # 倍
        (r'(\d+倍)', r'<span class="n">\1</span>'),
        # 単純な数字+助数詞
        (r'(\d+種)', r'<span class="n">\1</span>'),
        (r'(\d+号)', r'<span class="n">\1</span>'),
        # 「3年を経過しない」等
        (r'(\d+年を経過しない)', r'<span class="n">\1</span>'),
        (r'(\d+年をこえる)', r'<span class="n">\1</span>'),
        (r'(\d+年を超える)', r'<span class="n">\1</span>'),
    ]

    result = text
    for pattern, replacement in patterns:
        # 既にタグ内にある場合はスキップ
        result = re.sub(r'(?<!">)' + pattern, replacement, result)

    return result


def mark_exceptions(text: str) -> str:
    """ただし書きを<span class="ex">でマークする"""
    # 「ただし、...この限りでない。」等
    # 「但し、...」
    result = text

    # ただし書きをindent+exで囲む
    tadashi_pattern = r'((?:ただし|但し)、[^。]+。)'

    def replace_tadashi(m):
        return f'<div class="indent"><span class="ex">{m.group(1)}</span></div>'

    result = re.sub(tadashi_pattern, replace_tadashi, result)

    return result


def mark_conditions(text: str) -> str:
    """条件節を<span class="cd">でマークする"""
    result = text

    # 「〜場合には」「〜ときは」「〜場合において」等の条件節
    patterns = [
        (r'([^。、<>]+?(?:場合には|場合においては|場合において|場合は))', r'<span class="cd">\1</span>'),
        (r'([^。、<>]+?(?:ときは|とき(?=[、。])))', r'<span class="cd">\1</span>'),
        (r'([^。、<>]+?(?:に限る|に限り))', r'<span class="cd">\1</span>'),
    ]

    for pattern, replacement in patterns:
        # 既にタグ内にない場合のみ
        if '<span class="cd">' not in result:
            result = re.sub(pattern, replacement, result, count=1)

    return result


def mark_subjects(text: str) -> str:
    """主語を<span class="s">でマークする"""
    result = text

    # 文頭の主語パターン: 「XXは、」「XXが」
    # 最初の「は、」の前が主語
    subject_match = re.match(r'^(<span class="koko">[^<]+</span>)?([^、。<>]+?)(は、)', result)
    if subject_match:
        prefix = subject_match.group(1) or ''
        subject = subject_match.group(2)
        particle = subject_match.group(3)
        if len(subject) > 1 and len(subject) < 80:
            result = f'{prefix}<span class="s">{subject}</span>{particle}{result[subject_match.end():]}'

    return result


def mark_predicates(text: str) -> str:
    """述語・結論を<span class="v">でマークする"""
    result = text

    # 文末の述語パターン
    predicate_patterns = [
        r'(定めるものとする)。',
        r'(総称する)。',
        r'(とする)。$',
        r'(とみなす)。',
        r'(を徴収する)。',
        r'(適用する)。',
        r'(成立する)。',
        r'(消滅する)。',
        r'(行ってはならない)。',
        r'(しなければならない)。',
        r'(することができる)。',
        r'(することができない)。',
        r'(有しない)。',
        r'(有する)。',
        r'(効力を生ずる)。',
        r'(を目的とする)。',
        r'(資格を有する)。',
        r'(資格を有しない)。',
    ]

    for pattern in predicate_patterns:
        if re.search(pattern, result):
            result = re.sub(pattern, r'<span class="v">\1</span>。', result, count=1)
            break

    return result


def apply_indentation(text: str) -> str:
    """条件節等にインデントを適用する"""
    result = text

    # 号(1. 2. 3. 等)の並列をインデント
    # 「1. 」「2. 」等のパターン
    if re.search(r'(?:1\.\s|1\.\s)', result):
        # 号リストをdiv.indentで囲む
        parts = re.split(r'(\d+\.\s)', result)
        if len(parts) >= 3:
            new_parts = [parts[0]]
            new_parts.append('<div class="indent">')
            for j in range(1, len(parts)):
                new_parts.append(parts[j])
            new_parts.append('</div>')
            result = ''.join(new_parts)

    return result


def process_file(input_path: str, output_path: str):
    """入力ファイルを処理して出力ファイルに書き込む"""
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    output = []
    for item in data:
        ref = item.get('reference', '')
        body = item.get('body', '')

        if not body or not body.strip():
            structured = ""
        else:
            structured = structure_article(body, ref)

        output.append({
            'reference': ref,
            'structured': structured
        })

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Processed {len(output)} items: {input_path} -> {output_path}")


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
        process_file(input_path, output_path)

    print("All done!")


if __name__ == '__main__':
    main()

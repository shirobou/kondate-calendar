"""
条文テキストを自動で構造化HTMLに変換するスクリプト
ヒューリスティックルールで主語・述語・条件・数字・例外を検出し、
インデント＋色分けHTMLを生成する。
"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

SUBJECTS = [
    '労働基準法', '労働安全衛生法', '労災保険法', '雇用保険法',
    '労働保険徴収法', '労働一般常識', '健康保険法', '国民年金法',
    '厚生年金保険法', '社会保険一般常識'
]


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def structurize(body):
    """条文テキストを構造化HTMLに変換"""
    if not body or len(body) < 10:
        return ''

    body = body.strip()

    # 項分割（◯1, ◯2, ◯3 ... で分割）
    paras = re.split(r'(◯\d+)', body)

    result_parts = []

    i = 0
    while i < len(paras):
        part = paras[i].strip()
        if not part:
            i += 1
            continue

        # 項番号
        if re.match(r'^◯\d+$', part):
            para_num = part
            para_body = paras[i + 1].strip() if i + 1 < len(paras) else ''
            i += 2
            html = f'<span class="para"><span class="koko">{esc(para_num)}</span>\n'
            html += structurize_sentence(para_body)
            html += '</span>'
            result_parts.append(html)
        else:
            # 項番号なしの本文
            html = structurize_sentence(part)
            result_parts.append(html)
            i += 1

    return '\n'.join(result_parts)


def structurize_sentence(text):
    """1つの項の内容を構造化"""
    if not text:
        return ''

    # ただし書きを分離
    main_text, tadashi = split_tadashi(text)

    # メイン文を構造化
    html = process_main(main_text)

    # ただし書き
    if tadashi:
        html += f'\n<div class="indent"><span class="ex">{esc(tadashi)}</span></div>'

    return html


def split_tadashi(text):
    """ただし書きを分離"""
    # 「ただし、」「ただし」で分割
    m = re.search(r'(?:。\s*)?ただし[、，]', text)
    if m:
        main = text[:m.start()] + '。'
        tadashi = text[m.start():].lstrip('。').strip()
        return main, tadashi
    return text, ''


def process_main(text):
    """メインの文を構造化"""
    if not text:
        return ''

    lines = []

    # 文を句点で分割（ただし括弧内の句点は除く）
    sentences = split_sentences(text)

    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue
        lines.append(process_single_sentence(sent))

    return '\n'.join(lines)


def split_sentences(text):
    """文を句点で分割（括弧内は除く）"""
    result = []
    depth = 0
    current = []
    for ch in text:
        if ch in '（(':
            depth += 1
        elif ch in '）)':
            depth -= 1
        current.append(ch)
        if ch == '。' and depth <= 0:
            result.append(''.join(current))
            current = []
    if current:
        result.append(''.join(current))
    return result


def process_single_sentence(sent):
    """1文を構造化"""
    result = ''

    # 主語の検出（文頭の「Xは、」パターン）
    subj_match = re.match(
        r'^((?:使用者|事業者|事業主|労働者|被保険者|受給資格者|政府|厚生労働大臣|'
        r'都道府県労働局長|都道府県知事|労働基準監督署長|労働基準監督官|'
        r'公共職業安定所長|行政官庁|市町村長|国|'
        r'保険給付を受ける権利を有する者|保険給付を受ける権利|'
        r'労働委員会|コンサルタント|'
        r'[^\s、。]{2,20}?)(?:は|が)[、，])\s*',
        sent
    )

    if subj_match:
        subj_text = subj_match.group(1)
        rest = sent[subj_match.end():]
        # 主語部分を色付け
        subj_colored = colorize_subject(subj_text)
        result += subj_colored + '\n'
        # 残りをインデント内で処理
        result += '<div class="indent">' + colorize_body(rest) + '</div>'
    else:
        result += colorize_body(sent)

    return result


def colorize_subject(text):
    """主語部分の色付け"""
    # 「Xは」「Xが」のパターン
    m = re.match(r'^(.+?)(は|が)$', text)
    if m:
        return f'<span class="s">{esc(m.group(1))}</span>{esc(m.group(2))}、'
    return f'<span class="s">{esc(text)}</span>'


def colorize_body(text):
    """本文の色付け（述語、条件、数字）"""
    if not text:
        return ''

    # 一旦エスケープ
    t = esc(text)

    # 数字・期限の色付け（緑）
    num_patterns = [
        r'(\d+日分?以上|\d+日間?|\d+日前|\d+箇月間?|\d+箇月以?内?|\d+年間?)',
        r'(\d+歳[以上未満]*)',
        r'(100分の\d+以?上?|10分の\d+)',
        r'(\d+週間|\d+時間|\d+万円|\d+円)',
        r'(\d+労働日|\d+人以上|\d+回)',
        r'(平均賃金)',
    ]
    for pat in num_patterns:
        t = re.sub(pat, r'<span class="n">\1</span>', t)

    # 条件の色付け（オレンジ）
    cond_patterns = [
        r'((?:した|する|しようとする|された|できない|あった|受けた|該当する|認める)場合(?:においては?|には?|であって)?)',
        r'((?:した|する|しようとする)とき(?:は)?)',
        r'((?:業務上|通勤により|政令で定める))',
    ]
    for pat in cond_patterns:
        t = re.sub(pat, r'<span class="cd">\1</span>', t)

    # 述語の色付け（赤）
    pred_patterns = [
        r'((?:しなければならない|なければならない|してはならない|することができる|'
        r'することができない|適用しない|適用される|支払わなければならない|'
        r'行わなければならない|与えなければならない|'
        r'講じなければならない|選任しなければならない|'
        r'届け出なければならない|提出しなければならない|'
        r'報告しなければならない|通知しなければならない|'
        r'交付しなければならない|設けなければならない|'
        r'記録しておかなければならない|保存しなければならない|'
        r'行うことができる|命ずることができる|'
        r'認めることができる|求めることができる|'
        r'徴収することができる|'
        r'努めなければならない|努めるものとする|'
        r'解雇してはならない|使用してはならない|'
        r'就かせてはならない|労働させてはならない|'
        r'差別的取扱をしてはならない|差別的取扱いをしてはならない|'
        r'課することはできない|譲り渡し.*できない|'
        r'変更されることはない|'
        r'免れる|科する|処する|'
        r'支給する|行う|定める))[。]?',
    ]
    for pat in pred_patterns:
        t = re.sub(pat, r'<span class="v">\1</span>', t)

    # 並列の改行（「並びに」「又は」の前で改行）
    t = re.sub(r'(並びに)', r'<br><br>\1', t)
    t = re.sub(r'(?<=[。、）])\s*(又は)', r'<br>\1', t)

    # 号の改行（1. 2. 3. やア. イ. ウ.）
    t = re.sub(r'\s*(\d+\.)\s*', r'<br>\1 ', t)
    t = re.sub(r'\s*([アイウエオカキクケコ]\.)\s*', r'<br>\1 ', t)

    return t


def main():
    with open('extracted_final.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    total = 0
    for subj in SUBJECTS:
        arts = data.get(subj, [])
        structured = []
        for art in arts:
            body = art.get('body', '')
            st = structurize(body)
            structured.append({
                'reference': art['reference'],
                'structured': st,
            })

        out_file = f'structured_{subj}.json'
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(structured, f, ensure_ascii=False)

        has_st = sum(1 for s in structured if s['structured'])
        total += has_st
        print(f'{subj}: {len(structured)}件 (構造化: {has_st}件)')

    print(f'\n合計: {total}件')


if __name__ == '__main__':
    main()

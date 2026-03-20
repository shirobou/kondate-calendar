"""
徹底的な条文データクレンジング
教材解説・自己引用・重複リスト・見出しテキストを除去
"""
import json, re, sys, os

sys.stdout.reconfigure(encoding='utf-8')
base = 'c:/Users/kokor/Desktop/Claude-Personal'

with open(f'{base}/extracted_final.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def plain_to_html_offset(html_str, plain_offset):
    plain_pos = 0
    in_tag = False
    for i, ch in enumerate(html_str):
        if ch == '<':
            in_tag = True
            continue
        if ch == '>':
            in_tag = False
            continue
        if not in_tag:
            if plain_pos >= plain_offset:
                return i
            plain_pos += 1
    return len(html_str)

def cut_at(a, cut_pos):
    """Cut body and body_html at the given plain-text position"""
    body = a['body']
    body_html = a['body_html']
    a['body'] = body[:cut_pos].rstrip()
    html_cut = plain_to_html_offset(body_html, cut_pos)
    a['body_html'] = body_html[:html_cut].rstrip()
    a['body_html'] = re.sub(r'<[^>]*$', '', a['body_html'])

def normalize_ref(ref):
    """Normalize reference for matching: 法25条の22 -> 25条の22"""
    return re.sub(r'^[法則令附則規則]+', '', ref).replace(' ', '')

def find_best_cut(body, ref):
    """Find the best position to cut contaminated content.
    Returns cut position or None."""
    ref_norm = normalize_ref(ref)
    
    cut_candidates = []
    
    # Strategy 1: Self-citation pattern （法XX条YY項）
    # This is the article citing itself - a sure sign of explanation text
    for m in re.finditer(r'（[法則附則規則令]*' + re.escape(ref_norm) + r'[第\d項号]*）', body):
        # Backtrack to the 。 before the citation
        before = body[:m.start()]
        last_p = before.rfind('。')
        if last_p > 10:
            cut_candidates.append(last_p + 1)
    
    # Strategy 2: Generic self-citation patterns（法XX条）（法XX条第Y項）
    for m in re.finditer(r'（[法則附則規則令]+\d+条[のの]?\d*(?:第\d+[項号])?(?:第\d+[項号])?）', body):
        pos = m.start()
        # Check if this citation is at/near end of a sentence
        after = body[m.end():m.end()+30].strip()
        # If followed by non-article text (explanation), cut before the citation
        if not after or not after[0] in '◯①②③④⑤⑥⑦⑧⑨':
            before = body[:pos]
            last_p = before.rfind('。')
            if last_p > 10 and last_p > len(body) * 0.3:  # Don't cut too early
                cut_candidates.append(last_p + 1)
    
    # Strategy 3: Explanation headers after article text
    # Pattern: 。TITLE_TEXT + explanation
    headers = [
        r'用語の定義', r'の定義$', r'の届出', r'の特例(?![\u3000-\u9FFF])',
        r'をまとめると', r'の内容$', r'とは[、\s]', r'について$',
    ]
    for h in headers:
        for m in re.finditer(h, body):
            before = body[:m.start()]
            last_p = before.rfind('。')
            if last_p > 10:
                cut_candidates.append(last_p + 1)
    
    # Strategy 4: Past exam references that might still be present
    for m in re.finditer(r'R\d{2}-\d{2}[A-Za-zｱ-ﾝ]|平\d+[A-Za-z]', body):
        before = body[:m.start()]
        last_p = before.rfind('。')
        if last_p > 10:
            cut_candidates.append(last_p + 1)
    
    # Strategy 5: Explanation text markers
    for m in re.finditer(r'本条に罰則|本条は|なお、|ちなみに|注意|ポイント|改正|2026改正|2022改正', body):
        before = body[:m.start()]
        last_p = before.rfind('。')
        if last_p > 10 and last_p > len(body) * 0.3:
            cut_candidates.append(last_p + 1)
    
    # Strategy 6: Repeated numbered lists (duplicated items)
    # Find first set of numbered items and check if they repeat
    num_items = list(re.finditer(r'(\d+)\.\s', body))
    if len(num_items) >= 4:
        # Check for "1." appearing twice
        ones = [m for m in num_items if m.group(1) == '1']
        if len(ones) >= 2:
            # The second "1." starts the duplicate list
            second_one = ones[1]
            before = body[:second_one.start()]
            last_p = before.rfind('。')
            if last_p > 10:
                cut_candidates.append(last_p + 1)
    
    if not cut_candidates:
        return None
    
    # Use the earliest cut that still preserves at least 30% of the body
    min_cut = len(body) * 0.3
    valid = [c for c in cut_candidates if c >= min_cut]
    if valid:
        return min(valid)
    return None

fixed = 0
for subj, articles in data.items():
    for a in articles:
        body = a.get('body', '')
        if not body or len(body) < 30:
            continue
        
        cut_pos = find_best_cut(body, a['reference'])
        if cut_pos and cut_pos < len(body) - 5:
            old_len = len(body)
            cut_at(a, cut_pos)
            new_len = len(a['body'])
            if new_len < old_len:
                fixed += 1

print(f'修正件数: {fixed}')

with open(f'{base}/extracted_final.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('保存完了')

# Verify the specific article
for a in data.get('社会保険一般常識', []):
    if a['reference'] == '法25条の22':
        print(f'\n法25条の22: {len(a["body"])}字')
        print(a['body'][:300])
        break

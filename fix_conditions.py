"""
構造化HTMLのconditionタグ過剰問題を修正するスクリプト
- conditionキーワードなし → タグ除去（プレーンテキスト化）
- conditionキーワードあり＆長い → 局所化（キーワード周辺のみタグ付け）
"""
import json, re, os, sys

sys.stdout.reconfigure(encoding='utf-8')

base = 'c:/Users/kokor/Desktop/Claude-Personal'
SUBJECTS = [
    '労働基準法', '労働安全衛生法', '労災保険法', '雇用保険法',
    '労働保険徴収法', '労働一般常識', '健康保険法', '国民年金法',
    '厚生年金保険法', '社会保険一般常識'
]

# Condition keywords (longer first for matching priority)
COND_KEYWORDS = [
    'する場合', 'した場合', 'である場合', 'ない場合', 'ある場合',
    'れる場合', 'れた場合', 'きた場合', 'なる場合', 'える場合',
    'するとき', 'したとき', 'であるとき', 'ないとき', 'あるとき',
    'れるとき', 'れたとき', 'きたとき', 'なるとき', 'えるとき',
    '場合において', '場合には',
    'を除き', 'のほか', 'に限り', 'を超え', 'に満たない',
    '該当する', 'に掲げる', '場合', 'とき',
]

# Particles that are natural break points
BREAK_CHARS = set('はがをにでと、，のへも')

def find_condition_keyword(text):
    """Find the last condition keyword in text, return (keyword, position)"""
    for kw in COND_KEYWORDS:
        idx = text.rfind(kw)
        if idx >= 0:
            return kw, idx
    return None, -1

def narrow_condition_text(text):
    """Narrow a long condition span to just the keyword phrase.
    Returns (before_plain, condition_part, after_plain)"""
    kw, idx = find_condition_keyword(text)
    if kw is None:
        return text, '', ''
    
    # Find break point before keyword (go back up to 15 chars)
    search_start = max(0, idx - 15)
    best_break = idx  # Default: keyword only
    
    for j in range(idx - 1, search_start - 1, -1):
        if text[j] in BREAK_CHARS:
            best_break = j + 1
            break
    
    before = text[:best_break]
    cond = text[best_break:idx + len(kw)]
    after = text[idx + len(kw):]
    return before, cond, after

def has_nested_tags(html_content):
    """Check if the content has nested HTML tags"""
    return bool(re.search(r'<span\s+class=', html_content))

def fix_structured_html(st):
    """Fix over-tagged condition spans in structured HTML"""
    if not st:
        return st
    
    def replace_condition(match):
        full = match.group(0)
        inner = match.group(1)
        
        # Get plain text (removing nested tags)
        plain = re.sub(r'<[^>]+>', '', inner)
        
        # Short spans are fine
        if len(plain) <= 20:
            return full
        
        # Check if has nested important tags (subject, period, logic)
        if has_nested_tags(inner):
            # Has nested tags - more complex handling
            kw, _ = find_condition_keyword(plain)
            if kw is None:
                # No condition keyword + nested tags → unwrap condition, keep inner tags
                return inner
            # Has keyword + nested tags → keep as is (too complex to narrow safely)
            return full
        
        # Plain text only (no nested tags)
        kw, _ = find_condition_keyword(plain)
        if kw is None:
            # No condition keyword → remove condition tag entirely
            return inner
        
        # Has keyword → narrow to just the keyword phrase
        before, cond, after = narrow_condition_text(plain)
        if cond:
            return before + '<span class="condition">' + cond + '</span>' + after
        return inner
    
    # Match condition spans (non-greedy, handle one level of nesting)
    # This regex matches <span class="condition">...</span> including nested spans
    pattern = r'<span class="condition">((?:(?!<span class="condition">).)*?)</span>'
    
    result = re.sub(pattern, replace_condition, st)
    return result

# Process all structured JSON files
total_fixed = 0
for subj in SUBJECTS:
    struct_file = f'{base}/structured_{subj}.json'
    if not os.path.exists(struct_file):
        continue
    
    with open(struct_file, 'r', encoding='utf-8') as f:
        struct_list = json.load(f)
    
    fixed_count = 0
    for item in struct_list:
        st = item.get('structured', '')
        if not st:
            continue
        new_st = fix_structured_html(st)
        if new_st != st:
            item['structured'] = new_st
            fixed_count += 1
    
    if fixed_count:
        with open(struct_file, 'w', encoding='utf-8') as f:
            json.dump(struct_list, f, ensure_ascii=False, indent=2)
        print(f'{subj}: {fixed_count}件修正')
        total_fixed += fixed_count

print(f'\n合計修正: {total_fixed}件')

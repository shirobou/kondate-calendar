"""
法24条と令の構造化HTMLを統合修正
"""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('structured_労働基準法.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 法24条: 5原則すべてを1つの構造化HTMLに統合
fix_24 = '''<div class="law-body"><div class="principle-section"><span class="item-number">第1項</span><div class="subject-line"><span class="subject">賃金</span>は、</div><ul class="condition-list"><li><span class="period">通貨</span>で、</li><li><span class="period">直接</span>労働者に、</li><li>その<span class="period">全額</span>を</li></ul><div class="predicate-line"><span class="predicate">支払わなければならない。</span></div></div><div class="exception-section"><div class="exception-keyword"><span class="exception">ただし、</span>通貨払いの例外：</div><ul class="condition-list"><li><span class="period">労働協約</span>に別段の定めがある場合</li><li class="logic-item"><span class="logic">又は</span></li><li>厚生労働省令で定める確実な支払方法による場合</li></ul><div class="predicate-line">→ <span class="period">通貨以外のもの</span>で<span class="exception">支払うことができる。</span></div></div><div class="exception-section"><div class="exception-keyword">全額払いの例外：</div><ul class="condition-list"><li><span class="period">法令</span>に別段の定めがある場合</li><li class="logic-item"><span class="logic">又は</span></li><li><span class="period">労使協定</span>がある場合</li></ul><div class="predicate-line">→ 賃金の<span class="period">一部を控除</span>して<span class="exception">支払うことができる。</span></div></div><div class="principle-section"><span class="item-number">第2項</span><div class="subject-line"><span class="subject">賃金</span>は、</div><ul class="condition-list"><li><span class="period">毎月1回以上</span>、</li><li><span class="period">一定の期日</span>を定めて</li></ul><div class="predicate-line"><span class="predicate">支払わなければならない。</span></div></div><div class="exception-section"><div class="exception-keyword"><span class="exception">ただし、</span></div><ul class="condition-list"><li>臨時に支払われる賃金、</li><li><span class="period">賞与</span>その他これに準ずるもので厚生労働省令で定める賃金</li></ul><div class="predicate-line">については、<span class="exception">この限りでない。</span></div></div></div>'''

# 令: 法24条に統合したので、令の方にも同じ内容を入れる（どちらを開いても全体が見える）
fix_rei = fix_24

for item in data:
    if item['reference'] == '法24条':
        item['structured'] = fix_24
        print("  ✔ 法24条 を統合版に修正")
    elif item['reference'] == '令':
        item['structured'] = fix_rei
        print("  ✔ 令 も統合版に修正")

with open('structured_労働基準法.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n保存完了")

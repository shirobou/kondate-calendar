"""
社労士条文かみ砕きツール 最終ビルダー
赤シート機能 + かみ砕き解説 + ブックマーク + 学習進捗
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

# 再抽出データ（赤枠+太字+空白除去済み）
with open('extracted_final.json', 'r', encoding='utf-8') as f:
    styled_data = json.load(f)

# 統合データ構築
combined = {}
total_articles = 0
total_marks = 0

for subj in SUBJECTS:
    # 解説ファイル
    exp_file = f'explanations_{subj}.json'
    with open(exp_file, 'r', encoding='utf-8') as f:
        explanations = json.load(f)
    exp_map = {e['reference']: e for e in explanations}

    # 構造化データ
    struct_file = f'structured_{subj}.json'
    struct_map = {}
    if os.path.exists(struct_file):
        with open(struct_file, 'r', encoding='utf-8') as f:
            struct_list = json.load(f)
        struct_map = {s['reference']: s.get('structured', '') for s in struct_list}

    # 再抽出データ
    styled = styled_data.get(subj, [])
    styled_map = {a['reference']: a for a in styled}

    merged = []
    # 再抽出データをベースにする（赤枠情報があるため）
    refs_done = set()
    for art in styled:
        ref = art['reference']
        exp = exp_map.get(ref, {})
        merged.append({
            'r': ref,
            't': exp.get('title', ''),
            'h': art.get('body_html', ''),  # HTMLタグ付き原文
            'b': art.get('body', ''),       # プレーン原文
            's': exp.get('simple', ''),
            'e': exp.get('example', ''),
            'p': exp.get('point', ''),
            'f': art.get('source', '').replace('.pdf', ''),
            'pg': art.get('page', 0),
            'im': art.get('importance', ''),  # 重要度
            'st': struct_map.get(ref, ''),  # 構造化HTML
        })
        refs_done.add(ref)

    # 解説にあるが再抽出にない条文も追加（原文なし）
    for exp in explanations:
        if exp['reference'] not in refs_done:
            merged.append({
                'r': exp['reference'],
                't': exp.get('title', ''),
                'h': '',
                'b': '',
                's': exp.get('simple', ''),
                'e': exp.get('example', ''),
                'p': exp.get('point', ''),
                'f': '',
                'pg': 0,
            })

    # テキスト（PDFファイル）順にソート
    # source順 → PDFファイル名の先頭番号順（元のテキスト順序を維持）
    def sort_key(a):
        f = a.get('f', '')
        # ファイル名先頭の番号を抽出 (例: "01_労働基準法1-..." → 1)
        m = re.match(r'^(\d+)', f)
        file_num = int(m.group(1)) if m else 9999
        # ファイル内でのページ順
        pg = a.get('pg', 0) or 9999
        return (file_num, pg)

    merged.sort(key=sort_key)

    marks = sum(1 for a in merged if '<mark>' in a.get('h', ''))
    combined[subj] = merged
    total_articles += len(merged)
    total_marks += marks
    print(f"{subj}: {len(merged)}件 (赤シート付き: {marks}件)")

data_json = json.dumps(combined, ensure_ascii=False, separators=(',', ':'))
print(f"\n合計: {total_articles}件, データ: {len(data_json)/1024:.0f}KB")

# HTMLテンプレート
HTML = r'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<title>社労士 条文かみ砕きツール</title>
<style>
:root{--p:#1a73e8;--pl:#e8f0fe;--bg:#f8f9fa;--c:#fff;--t:#202124;--ts:#5f6368;--bd:#dadce0;--as:#1a73e8;--ae:#0d652d;--ap:#c5221f;--ao:#7627bb;--bm:#f9ab00;--done:#34a853;--red:#c5221f}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans JP',sans-serif;background:var(--bg);color:var(--t);line-height:1.6}
.hd{background:var(--p);color:#fff;padding:14px 20px;position:sticky;top:0;z-index:100;box-shadow:0 2px 4px rgba(0,0,0,.2)}
.hd h1{font-size:17px;font-weight:600}.hd .sub{font-size:11px;opacity:.8;margin-top:2px}
.hd-nav{display:flex;gap:8px;margin-top:8px;flex-wrap:wrap}
.hd-nav button{background:rgba(255,255,255,.2);border:none;color:#fff;padding:4px 12px;border-radius:12px;font-size:12px;cursor:pointer}
.hd-nav button:hover{background:rgba(255,255,255,.35)}
.hd-nav button.hn-act{background:#fff;color:var(--p);font-weight:600}
.ct{max-width:800px;margin:0 auto;padding:16px}
.sg{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;margin:16px 0}
.sb{padding:12px 10px;border:2px solid var(--bd);border-radius:12px;background:var(--c);cursor:pointer;text-align:center;font-size:13px;font-weight:500;transition:all .2s;position:relative}
.sb:hover{border-color:var(--p);background:var(--pl)}
.sb .cnt{display:block;font-size:11px;color:var(--ts);margin-top:3px}
.sb .prog{display:block;margin-top:5px;height:4px;background:#e0e0e0;border-radius:2px;overflow:hidden}
.sb .prog-bar{height:100%;background:var(--done);border-radius:2px;transition:width .3s}
.sb .prog-txt{font-size:10px;color:var(--ts);margin-top:2px}
.sx{position:relative;margin:14px 0}
.sx input{width:100%;padding:11px 16px 11px 40px;border:2px solid var(--bd);border-radius:24px;font-size:14px;outline:none;background:var(--c)}
.sx input:focus{border-color:var(--p);box-shadow:0 0 0 3px rgba(26,115,232,.15)}
.sx::before{content:'\1F50D';position:absolute;left:14px;top:50%;transform:translateY(-50%);font-size:15px}
.st{text-align:center;color:var(--ts);font-size:13px;margin:6px 0 14px}
.al{list-style:none}
.ai{background:var(--c);border-radius:12px;margin-bottom:10px;box-shadow:0 1px 2px rgba(0,0,0,.06);overflow:hidden;border:1px solid var(--bd)}
.ai.learned{border-left:4px solid var(--done)}
.ai.bookmarked{border-left:4px solid var(--bm)}
.ai.learned.bookmarked{border-left:4px solid var(--bm)}
.ah{padding:12px 14px;cursor:pointer;display:flex;align-items:center;gap:8px}
.ah:hover{background:var(--pl)}
.ar{background:var(--p);color:#fff;padding:2px 8px;border-radius:5px;font-size:12px;font-weight:600;white-space:nowrap}
.ar-sub{background:#0d652d;font-size:11px}
.a-im{font-size:11px;color:#f9ab00;letter-spacing:-1px;white-space:nowrap;flex-shrink:0}
.a-im-high{color:#c5221f}
.ai-sub{margin-left:20px}
.ai-sub .ah{padding-left:10px}
.at{font-size:13px;font-weight:500;flex:1}
.a-icons{display:flex;gap:2px;align-items:center}
.a-bm,.a-ck{font-size:15px;padding:3px;cursor:pointer;opacity:.3;transition:opacity .15s;user-select:none}
.a-bm:hover,.a-ck:hover{opacity:.7}
.a-bm.on{opacity:1;color:var(--bm)}.a-ck.on{opacity:1;color:var(--done)}
.ag{font-size:16px;color:var(--ts);transition:transform .2s}
.ai.op .ag{transform:rotate(180deg)}
.ab{display:none;padding:0 14px 14px}
.ai.op .ab{display:block}
/* 赤シート機能 */
.rs-ctrl{margin-bottom:10px;display:flex;gap:8px;align-items:center}
.rs-btn{padding:5px 14px;border:2px solid var(--red);border-radius:16px;background:var(--red);color:#fff;font-size:12px;font-weight:600;cursor:pointer}
.rs-btn.off{background:var(--c);color:var(--red)}
.rs-hint{font-size:11px;color:var(--ts)}
.body-html{font-size:14px;line-height:2;margin-bottom:12px;padding:12px;background:#fafafa;border-radius:8px;border:1px solid var(--bd)}
.body-tabs{display:flex;gap:4px;margin-bottom:8px}
.body-tab{padding:4px 12px;border:1px solid var(--bd);border-radius:14px;background:var(--c);cursor:pointer;font-size:11px;color:var(--ts)}
.body-tab.bt-act{background:var(--p);color:#fff;border-color:var(--p)}
.body-struct{display:none;font-size:14px;line-height:2.1;padding:0;margin-bottom:10px}
.body-struct.show{display:block}
.body-html.hide{display:none}
.body-struct .law-body{padding:16px;background:#fafafa;border-radius:8px;border:1px solid #e0e0e0}
.body-struct .subject{color:#1a73e8;font-weight:700}
.body-struct .subject-line{margin-bottom:4px}
.body-struct .condition-list{list-style:none;padding-left:1.5em;border-left:3px solid #e8eaf6;margin:6px 0 6px 8px}
.body-struct .condition-list li{padding:3px 0;color:var(--t)}
.body-struct .condition{color:#e65100}
.body-struct .logic{display:inline-block;background:#fff3e0;color:#e65100;font-weight:700;font-size:12px;padding:2px 10px;border-radius:4px;border:1px solid #ffe0b2;margin:2px 2px}
.body-struct .logic-item{list-style:none}
.body-struct .period{color:#0d652d;font-weight:700;background:#e8f5e9;padding:1px 5px;border-radius:3px}
.body-struct .predicate{color:#c5221f;font-weight:700}
.body-struct .predicate-line{margin-top:6px;padding-top:4px}
.body-struct .exception-section{margin-top:12px;padding:12px 16px;background:#faf5ff;border-radius:8px;border:1px dashed #ce93d8}
.body-struct .exception-keyword{margin-bottom:4px}
.body-struct .exception{color:#7627bb;font-weight:600}
.body-struct .exception-section .condition-list{border-left-color:#e1bee7}
.body-struct .principle-section{margin-bottom:16px;padding-bottom:16px;border-bottom:1px solid #f0f0f0}
.body-struct .principle-section:last-of-type{border-bottom:none;margin-bottom:0;padding-bottom:0}
.body-struct .item-number{display:inline-block;background:#e8eaf6;color:#3f51b5;font-weight:700;font-size:12px;padding:2px 10px;border-radius:4px;margin-bottom:6px}
.body-html mark{background:var(--red);color:var(--red);border-radius:3px;padding:1px 3px;cursor:pointer;transition:all .15s;user-select:none;font-style:normal;font-weight:normal}
.body-html mark.rv,.body-html.rs-off mark{background:transparent;color:var(--red);font-weight:700;text-decoration:underline;text-decoration-color:rgba(197,34,31,.25);text-underline-offset:3px}
.body-html b{font-weight:700}
.sc{margin-bottom:10px;padding:10px 12px;border-radius:8px;border-left:4px solid}
.sc-s{background:#e8f0fe;border-color:var(--as)}.sc-e{background:#e6f4ea;border-color:var(--ae)}.sc-p{background:#fce8e6;border-color:var(--ap)}
.sl{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px}
.sc-s .sl{color:var(--as)}.sc-e .sl{color:var(--ae)}.sc-p .sl{color:var(--ap)}
.st2{font-size:13px;line-height:1.7;font-weight:400;font-family:'Meiryo','Noto Sans JP',sans-serif;-webkit-font-smoothing:antialiased}
.si{font-size:11px;color:var(--ts);margin-top:6px;padding:5px 8px;background:var(--bg);border-radius:5px}
.bb{display:inline-flex;align-items:center;gap:5px;padding:7px 14px;border:none;background:var(--pl);color:var(--p);border-radius:18px;cursor:pointer;font-size:13px;font-weight:500;margin-bottom:10px}
.bb:hover{background:#d2e3fc}
.vt,.vs,.vb,.vp{display:none}
.app[data-view="top"] .vt{display:block}
.app[data-view="subject"] .vs{display:block}
.app[data-view="bookmarks"] .vb{display:block}
.app[data-view="progress"] .vp{display:block}
.eb{padding:5px 12px;border:1px solid var(--bd);border-radius:14px;background:var(--c);cursor:pointer;font-size:11px;color:var(--ts)}
.eb:hover{background:var(--bg)}
.tb{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;flex-wrap:wrap;gap:6px}
.filter-btns{display:flex;gap:4px;flex-wrap:wrap}
.filter-btn{padding:3px 9px;border:1px solid var(--bd);border-radius:10px;background:var(--c);cursor:pointer;font-size:11px;color:var(--ts)}
.filter-btn:hover{background:var(--bg)}.filter-btn.fa{background:var(--p);color:#fff;border-color:var(--p)}
.prog-summary{background:var(--c);border-radius:12px;padding:18px;margin-bottom:14px;border:1px solid var(--bd)}
.prog-summary h3{font-size:15px;margin-bottom:10px}
.prog-ov{height:10px;background:#e0e0e0;border-radius:5px;overflow:hidden;margin-bottom:6px}
.prog-ov-bar{height:100%;background:var(--done);border-radius:5px}
.prog-pct{font-size:22px;font-weight:700;color:var(--done);text-align:center;margin:10px 0}
.prog-det{font-size:13px;color:var(--ts);text-align:center}
.sp-row{display:flex;align-items:center;gap:8px;padding:7px 10px;background:var(--c);border-radius:7px;border:1px solid var(--bd);margin-bottom:6px}
.sp-name{font-size:12px;font-weight:500;width:110px;flex-shrink:0}
.sp-bar{flex:1;height:7px;background:#e0e0e0;border-radius:4px;overflow:hidden}
.sp-bar-fill{height:100%;background:var(--done);border-radius:4px}
.sp-txt{font-size:11px;color:var(--ts);width:55px;text-align:right;flex-shrink:0}
.sec-hd{padding:10px 14px;margin:16px 0 6px;background:linear-gradient(135deg,#e8eaf6,#f3e5f5);border-radius:10px;font-size:13px;font-weight:600;color:#37474f;border-left:4px solid #5c6bc0;cursor:pointer;user-select:none;display:flex;align-items:center;gap:8px}
.sec-hd:first-child{margin-top:0}
.sec-hd::before{content:'📖';font-size:14px}
.sec-hd .sec-cnt{font-size:11px;font-weight:400;color:var(--ts);margin-left:auto}
@media(max-width:600px){.sg{grid-template-columns:repeat(2,1fr)}.ct{padding:10px}.sp-name{width:70px;font-size:10px}.sec-hd{font-size:11px;padding:8px 10px}}
</style>
</head>
<body>
<div class="hd">
<h1>社労士 条文かみ砕きツール</h1>
<div class="sub">10科目の条文を「赤シート」「やさしい日本語」「具体例」「試験ポイント」で理解</div>
<div class="hd-nav">
<button class="hn-act" onclick="navTo('top')">科目一覧</button>
<button onclick="navTo('bookmarks')">ブックマーク</button>
<button onclick="navTo('progress')">学習進捗</button>
</div>
</div>
<div class="ct">
<div class="app" data-view="top">
<div class="vt">
<div class="sx"><input type="text" id="gs" placeholder="条文を検索（例：解雇予告、有給休暇、標準報酬…）"></div>
<div id="sr"></div>
<div id="sgrid" class="sg"></div>
</div>
<div class="vs">
<button class="bb" onclick="navTo('top')">← 科目一覧</button>
<h2 id="stitle" style="font-size:17px;margin-bottom:4px;"></h2>
<div class="tb">
<div class="st" id="sstats"></div>
<div class="filter-btns">
<button class="filter-btn fa" onclick="setF('all',this)">すべて</button>
<button class="filter-btn" onclick="setF('unlearned',this)">未学習</button>
<button class="filter-btn" onclick="setF('learned',this)">学習済</button>
<button class="filter-btn" onclick="setF('bookmarked',this)">★</button>
</div>
<button class="rs-btn" id="rsGlobal" onclick="tRSAll()">赤シート ON</button>
<button class="eb" onclick="toggleAll()">すべて開く</button>
</div>
<div class="sx"><input type="text" id="ss" placeholder="この科目内を検索…"></div>
<ul class="al" id="alist"></ul>
</div>
<div class="vb">
<button class="bb" onclick="navTo('top')">← 科目一覧</button>
<h2 style="font-size:17px;margin-bottom:10px;">ブックマーク</h2>
<div id="bmE" class="st">ブックマークはまだありません。★をタップして追加。</div>
<ul class="al" id="bmL"></ul>
</div>
<div class="vp">
<button class="bb" onclick="navTo('top')">← 科目一覧</button>
<h2 style="font-size:17px;margin-bottom:10px;">学習進捗</h2>
<div class="prog-summary">
<h3>全体の進捗</h3>
<div class="prog-ov"><div class="prog-ov-bar" id="pB"></div></div>
<div class="prog-pct" id="pP">0%</div>
<div class="prog-det" id="pD"></div>
</div>
<div id="sP"></div>
<div style="text-align:center;margin-top:16px;">
<button class="eb" onclick="if(confirm('学習進捗をリセットしますか？'))resetP()">進捗リセット</button>
</div>
</div>
</div>
</div>
<script>
const D=__DATA__;
const S=["労働基準法","労働安全衛生法","労災保険法","雇用保険法","労働保険徴収法","労働一般常識","健康保険法","国民年金法","厚生年金保険法","社会保険一般常識"];
let cur=null,allE=false,cF='all',rsOff=false;
function gS(){try{return JSON.parse(localStorage.getItem('shr')||'{}');}catch(e){return{};}}
function sS(d){localStorage.setItem('shr',JSON.stringify(d));}
function ky(s,r){return s+'::'+r;}
function isBm(s,r){const d=gS();return!!(d[ky(s,r)]&&d[ky(s,r)].b);}
function isLn(s,r){const d=gS();return!!(d[ky(s,r)]&&d[ky(s,r)].l);}
function tBm(s,r,el){const d=gS(),k=ky(s,r);if(!d[k])d[k]={};d[k].b=!d[k].b;sS(d);el.classList.toggle('on',d[k].b);el.closest('.ai').classList.toggle('bookmarked',d[k].b);}
function tLn(s,r,el){const d=gS(),k=ky(s,r);if(!d[k])d[k]={};d[k].l=!d[k].l;sS(d);el.classList.toggle('on',d[k].l);el.closest('.ai').classList.toggle('learned',d[k].l);bG();}
function cLn(s){const d=gS();let c=0;(D[s]||[]).forEach(a=>{if(d[ky(s,a.r)]&&d[ky(s,a.r)].l)c++;});return c;}
function resetP(){sS({});navTo('progress');}
function init(){bG();document.getElementById('gs').addEventListener('input',onGS);document.getElementById('ss').addEventListener('input',()=>aF());}
function bG(){const g=document.getElementById('sgrid');g.innerHTML='';S.forEach(s=>{const c=(D[s]||[]).length,ln=cLn(s),pct=c?Math.round(ln/c*100):0;const b=document.createElement('div');b.className='sb';b.innerHTML=s+'<span class="cnt">'+c+'条文</span><div class="prog"><div class="prog-bar" style="width:'+pct+'%"></div></div><span class="prog-txt">'+ln+'/'+c+'</span>';b.onclick=()=>showS(s);g.appendChild(b);});}
function navTo(v){document.querySelector('.app').dataset.view=v;cur=null;document.querySelectorAll('.hd-nav button').forEach(b=>b.classList.remove('hn-act'));const i={top:0,bookmarks:1,progress:2}[v];if(i!==undefined)document.querySelectorAll('.hd-nav button')[i].classList.add('hn-act');if(v==='bookmarks')rBm();if(v==='progress')rPr();if(v==='top')bG();}
function showS(n){cur=n;cF='all';rsOff=false;document.querySelector('.app').dataset.view='subject';document.getElementById('stitle').textContent=n;document.getElementById('ss').value='';allE=false;document.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('fa'));document.querySelector('.filter-btn').classList.add('fa');const rb=document.getElementById('rsGlobal');rb.textContent='赤シート ON';rb.classList.remove('off');ren(D[n]||[]);}
function setF(f,el){cF=f;document.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('fa'));el.classList.add('fa');aF();}
function aF(){if(!cur)return;let a=D[cur]||[];const q=document.getElementById('ss').value.trim().toLowerCase();if(q.length>=2)a=a.filter(x=>(x.r+x.t+x.s+x.e+x.p+(x.b||'')).toLowerCase().includes(q));if(cF==='bookmarked')a=a.filter(x=>isBm(cur,x.r));else if(cF==='learned')a=a.filter(x=>isLn(cur,x.r));else if(cF==='unlearned')a=a.filter(x=>!isLn(cur,x.r));ren(a);}
function isSub(r){return/^(則|令|附則|規則|措置法|整備法|暫定措置法)/.test(r);}
function ren(arts){const l=document.getElementById('alist');const sj=cur;document.getElementById('sstats').textContent=arts.length+'件';l.innerHTML='';let lastSrc='';arts.forEach(a=>{
// ソースファイルが変わったらセクションヘッダーを挿入
if(a.f&&a.f!==lastSrc){lastSrc=a.f;const cnt=arts.filter(x=>x.f===a.f).length;const hd=document.createElement('div');hd.className='sec-hd';hd.innerHTML=esc(a.f)+'<span class="sec-cnt">'+cnt+'件</span>';l.appendChild(hd);}
const li=document.createElement('li');const bm=isBm(sj,a.r),ln=isLn(sj,a.r),sub=isSub(a.r);li.className='ai'+(bm?' bookmarked':'')+(ln?' learned':'')+(sub?' ai-sub':'');
const arCls='ar'+(sub?' ar-sub':'');
const hasMarks=a.h&&a.h.includes('<mark>');
const rsBtn=hasMarks?'<button class="rs-btn" onclick="event.stopPropagation();tRSi(this)" style="font-size:10px;padding:3px 8px;margin-left:auto;">赤シート</button>':'';
let bodyHtml='';
if(a.h&&a.st){bodyHtml='<div class="body-tabs"><span class="body-tab bt-act" onclick="swTab(this,\'struct\')">構造化</span><span class="body-tab" onclick="swTab(this,\'raw\')">原文</span></div><div class="body-struct show">'+a.st+'</div><div class="body-html hide">'+a.h+'</div>';}
else if(a.h){bodyHtml='<div class="body-html">'+a.h+'</div>';}
else if(a.st){bodyHtml='<div class="body-struct show">'+a.st+'</div>';}
const imHtml=a.im?'<span class="a-im'+(a.im.includes('特')?' a-im-high':'')+'">'+esc(a.im)+'</span>':'';
li.innerHTML='<div class="ah" onclick="tog(this)"><span class="'+arCls+'">'+esc(a.r)+'</span><span class="at">'+esc(a.t)+'</span>'+imHtml+rsBtn+'<span class="a-icons"><span class="a-bm'+(bm?' on':'')+'" onclick="event.stopPropagation();tBm(\''+esc(sj)+'\',\''+esc(a.r)+'\',this)">★</span><span class="a-ck'+(ln?' on':'')+'" onclick="event.stopPropagation();tLn(\''+esc(sj)+'\',\''+esc(a.r)+'\',this)">✓</span></span><span class="ag">▼</span></div><div class="ab">'+bodyHtml+sec('やさしい日本語','s',a.s)+sec('身近な具体例','e',a.e)+sec('試験ポイント','p',a.p)+(a.f?'<div class="si">📖 '+esc(a.f)+(a.pg?' p.'+a.pg:'')+'</div>':'')+'</div>';l.appendChild(li);});
l.querySelectorAll('.body-html mark').forEach(el=>{el.addEventListener('click',function(ev){ev.stopPropagation();this.classList.toggle('rv');});});}
function rBm(){const d=gS();let h=[];S.forEach(s=>(D[s]||[]).forEach(a=>{if(d[ky(s,a.r)]&&d[ky(s,a.r)].b)h.push({...a,sj:s});}));const el=document.getElementById('bmL'),em=document.getElementById('bmE');if(!h.length){el.innerHTML='';em.style.display='block';return;}em.style.display='none';el.innerHTML='';h.forEach(a=>{const li=document.createElement('li');const ln=isLn(a.sj,a.r);li.className='ai bookmarked'+(ln?' learned':'');li.innerHTML='<div class="ah" onclick="tog(this)"><span class="ar">'+esc(a.r)+'</span><span class="at">'+esc(a.sj+' — '+a.t)+'</span><span class="a-icons"><span class="a-bm on" onclick="event.stopPropagation();tBm(\''+esc(a.sj)+'\',\''+esc(a.r)+'\',this)">★</span><span class="a-ck'+(ln?' on':'')+'" onclick="event.stopPropagation();tLn(\''+esc(a.sj)+'\',\''+esc(a.r)+'\',this)">✓</span></span><span class="ag">▼</span></div><div class="ab">'+(a.h?'<div class="body-html">'+a.h+'</div>':'')+sec('やさしい日本語','s',a.s)+sec('身近な具体例','e',a.e)+sec('試験ポイント','p',a.p)+'</div>';el.appendChild(li);});el.querySelectorAll('.body-html mark').forEach(el=>{el.addEventListener('click',function(ev){ev.stopPropagation();this.classList.toggle('rv');});});}
function rPr(){let tA=0,lA=0;const sp=document.getElementById('sP');sp.innerHTML='';S.forEach(s=>{const t=(D[s]||[]).length,ln=cLn(s);tA+=t;lA+=ln;const p=t?Math.round(ln/t*100):0;sp.innerHTML+='<div class="sp-row"><span class="sp-name">'+s+'</span><div class="sp-bar"><div class="sp-bar-fill" style="width:'+p+'%"></div></div><span class="sp-txt">'+ln+'/'+t+'</span></div>';});const pA=tA?Math.round(lA/tA*100):0;document.getElementById('pB').style.width=pA+'%';document.getElementById('pP').textContent=pA+'%';document.getElementById('pD').textContent=lA+' / '+tA+' 条文';}
function sec(l,c,t){if(!t)return'';return'<div class="sc sc-'+c+'"><div class="sl">'+l+'</div><div class="st2">'+esc(t)+'</div></div>';}
function esc(s){if(!s)return'';const d=document.createElement('div');d.textContent=s;return d.innerHTML;}
function tog(h){h.parentElement.classList.toggle('op');}
function toggleAll(){allE=!allE;document.querySelectorAll('.ai').forEach(i=>i.classList.toggle('op',allE));document.querySelector('.eb').textContent=allE?'すべて閉じる':'すべて開く';}
function swTab(el,mode){const p=el.closest('.ab');const tabs=p.querySelectorAll('.body-tab');tabs.forEach(t=>t.classList.remove('bt-act'));el.classList.add('bt-act');const st=p.querySelector('.body-struct');const rw=p.querySelector('.body-html');if(mode==='struct'){if(st)st.classList.add('show');if(rw)rw.classList.add('hide');}else{if(st)st.classList.remove('show');if(rw)rw.classList.remove('hide');}}
function tRSAll(){const marks=document.querySelectorAll('.body-html mark');const anyRevealed=Array.from(marks).some(m=>m.classList.contains('rv'));if(anyRevealed){marks.forEach(m=>m.classList.remove('rv'));document.getElementById('rsGlobal').textContent='赤シート ON';document.getElementById('rsGlobal').classList.remove('off');}else{marks.forEach(m=>m.classList.add('rv'));document.getElementById('rsGlobal').textContent='赤シート OFF';document.getElementById('rsGlobal').classList.add('off');}}
function tRSi(btn){const ai=btn.closest('.ai');const marks=ai.querySelectorAll('.body-html mark');const any=Array.from(marks).some(m=>m.classList.contains('rv'));marks.forEach(m=>m.classList.toggle('rv',!any));}
function onGS(ev){const q=ev.target.value.trim().toLowerCase();const r=document.getElementById('sr');if(q.length<2){r.innerHTML='';return;}let h=[];S.forEach(s=>(D[s]||[]).forEach(a=>{if((a.r+a.t+a.s+a.e+a.p+(a.b||'')).toLowerCase().includes(q))h.push({...a,sj:s});}));if(!h.length){r.innerHTML='<p class="st">\u8A72\u5F53\u306A\u3057</p>';return;}let htm='<p class="st">'+h.length+'\u4EF6\u30D2\u30C3\u30C8</p><ul class="al">';h.slice(0,50).forEach(a=>{htm+='<li class="ai"><div class="ah" onclick="tog(this)"><span class="ar">'+esc(a.r)+'</span><span class="at">'+esc(a.sj+' \u2014 '+a.t)+'</span><span class="ag">\u25BC</span></div><div class="ab">'+(a.h?'<div class="body-html rs-off">'+a.h+'</div>':'')+sec('\u3084\u3055\u3057\u3044\u65E5\u672C\u8A9E','s',a.s)+sec('\u5177\u4F53\u4F8B','e',a.e)+sec('\u8A66\u9A13\u30DD\u30A4\u30F3\u30C8','p',a.p)+'</div></li>';});if(h.length>50)htm+='<p class="st">\u4ED6'+(h.length-50)+'\u4EF6</p>';htm+='</ul>';r.innerHTML=htm;r.querySelectorAll('.body-html mark').forEach(el=>{el.addEventListener('click',function(ev){ev.stopPropagation();this.classList.toggle('rv');});});}
init();
</script>
</body>
</html>'''

html = HTML.replace('__DATA__', data_json)

with open('sharoushi.html', 'w', encoding='utf-8') as f:
    f.write(html)

sz = os.path.getsize('sharoushi.html')
print(f"\nHTML生成: sharoushi.html ({sz/1024:.0f}KB)")

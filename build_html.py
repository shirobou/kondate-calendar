"""
社労士条文かみ砕きツール HTMLビルダー
全科目の解説データを1つのHTMLファイルに埋め込む
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

SUBJECTS = [
    '労働基準法', '労働安全衛生法', '労災保険法', '雇用保険法',
    '労働保険徴収法', '労働一般常識', '健康保険法', '国民年金法',
    '厚生年金保険法', '社会保険一般常識'
]

# 原文データ読み込み
with open('extracted_articles.json', 'r', encoding='utf-8') as f:
    originals = json.load(f)

# 統合
combined = {}
for subj in SUBJECTS:
    exp_file = f'explanations_{subj}.json'
    with open(exp_file, 'r', encoding='utf-8') as f:
        explanations = json.load(f)

    orig_map = {a['reference']: a for a in originals.get(subj, [])}

    merged = []
    for exp in explanations:
        ref = exp['reference']
        orig = orig_map.get(ref, {})
        merged.append({
            'r': ref,
            't': exp.get('title', ''),
            'b': orig.get('body', ''),
            's': exp.get('simple', ''),
            'e': exp.get('example', ''),
            'p': exp.get('point', ''),
            'f': orig.get('source', '').replace('.pdf', ''),
            'pg': orig.get('page', 0),
        })

    combined[subj] = merged
    print(f'{subj}: {len(merged)}件')

data_json = json.dumps(combined, ensure_ascii=False, separators=(',', ':'))
print(f'\nデータサイズ: {len(data_json)/1024:.0f}KB')

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>社労士 条文かみ砕きツール</title>
<style>
:root{--p:#1a73e8;--pl:#e8f0fe;--bg:#f8f9fa;--c:#fff;--t:#202124;--ts:#5f6368;--bd:#dadce0;--as:#1a73e8;--ae:#0d652d;--ap:#c5221f;--ao:#7627bb;--bm:#f9ab00;--done:#34a853}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans JP',sans-serif;background:var(--bg);color:var(--t);line-height:1.6}
.hd{background:var(--p);color:#fff;padding:16px 20px;position:sticky;top:0;z-index:100;box-shadow:0 2px 4px rgba(0,0,0,.2)}
.hd h1{font-size:18px;font-weight:600}.hd .sub{font-size:12px;opacity:.8;margin-top:2px}
.hd-nav{display:flex;gap:12px;margin-top:8px}
.hd-nav button{background:rgba(255,255,255,.2);border:none;color:#fff;padding:4px 12px;border-radius:12px;font-size:12px;cursor:pointer}
.hd-nav button:hover{background:rgba(255,255,255,.35)}
.hd-nav button.hn-act{background:#fff;color:var(--p);font-weight:600}
.ct{max-width:800px;margin:0 auto;padding:16px}
.sg{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px;margin:16px 0}
.sb{padding:14px 12px;border:2px solid var(--bd);border-radius:12px;background:var(--c);cursor:pointer;text-align:center;font-size:13px;font-weight:500;transition:all .2s;position:relative}
.sb:hover{border-color:var(--p);background:var(--pl)}
.sb.act{border-color:var(--p);background:var(--p);color:#fff}
.sb .cnt{display:block;font-size:11px;color:var(--ts);margin-top:4px}
.sb.act .cnt{color:rgba(255,255,255,.8)}
.sb .prog{display:block;margin-top:6px;height:4px;background:#e0e0e0;border-radius:2px;overflow:hidden}
.sb .prog-bar{height:100%;background:var(--done);border-radius:2px;transition:width .3s}
.sb .prog-txt{font-size:10px;color:var(--ts);margin-top:2px}
.sx{position:relative;margin:16px 0}
.sx input{width:100%;padding:12px 16px 12px 44px;border:2px solid var(--bd);border-radius:24px;font-size:15px;outline:none;background:var(--c)}
.sx input:focus{border-color:var(--p);box-shadow:0 0 0 3px rgba(26,115,232,.15)}
.sx::before{content:'\1F50D';position:absolute;left:16px;top:50%;transform:translateY(-50%);font-size:16px}
.st{text-align:center;color:var(--ts);font-size:13px;margin:8px 0 16px}
.al{list-style:none}
.ai{background:var(--c);border-radius:12px;margin-bottom:12px;box-shadow:0 1px 3px rgba(0,0,0,.08);overflow:hidden;border:1px solid var(--bd)}
.ai.learned{border-left:4px solid var(--done)}
.ai.bookmarked{border-left:4px solid var(--bm)}
.ai.learned.bookmarked{border-left:4px solid var(--bm)}
.ah{padding:14px 16px;cursor:pointer;display:flex;align-items:center;gap:10px}
.ah:hover{background:var(--pl)}
.ar{background:var(--p);color:#fff;padding:3px 10px;border-radius:6px;font-size:13px;font-weight:600;white-space:nowrap}
.at{font-size:14px;font-weight:500;flex:1}
.a-icons{display:flex;gap:2px;align-items:center}
.a-bm,.a-ck{font-size:16px;padding:4px;cursor:pointer;opacity:.3;transition:opacity .2s;user-select:none}
.a-bm:hover,.a-ck:hover{opacity:.7}
.a-bm.on{opacity:1;color:var(--bm)}.a-ck.on{opacity:1;color:var(--done)}
.ag{font-size:18px;color:var(--ts);transition:transform .2s}
.ai.op .ag{transform:rotate(180deg)}
.ab{display:none;padding:0 16px 16px}
.ai.op .ab{display:block}
.sc{margin-bottom:14px;padding:12px 14px;border-radius:8px;border-left:4px solid}
.sc-s{background:#e8f0fe;border-color:var(--as)}
.sc-e{background:#e6f4ea;border-color:var(--ae)}
.sc-p{background:#fce8e6;border-color:var(--ap)}
.sc-o{background:#f3e8fd;border-color:var(--ao)}
.sl{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px}
.sc-s .sl{color:var(--as)}.sc-e .sl{color:var(--ae)}.sc-p .sl{color:var(--ap)}.sc-o .sl{color:var(--ao)}
.st2{font-size:14px;line-height:1.7}
.si{font-size:11px;color:var(--ts);margin-top:8px;padding:6px 10px;background:var(--bg);border-radius:6px}
.bb{display:inline-flex;align-items:center;gap:6px;padding:8px 16px;border:none;background:var(--pl);color:var(--p);border-radius:20px;cursor:pointer;font-size:13px;font-weight:500;margin-bottom:12px}
.bb:hover{background:#d2e3fc}
.vt{display:none}.vs{display:none}.vb{display:none}.vp{display:none}
.app[data-view="top"] .vt{display:block}
.app[data-view="subject"] .vs{display:block}
.app[data-view="bookmarks"] .vb{display:block}
.app[data-view="progress"] .vp{display:block}
.eb{padding:6px 14px;border:1px solid var(--bd);border-radius:16px;background:var(--c);cursor:pointer;font-size:12px;color:var(--ts)}
.eb:hover{background:var(--bg)}
.tb{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;flex-wrap:wrap;gap:8px}
.filter-btns{display:flex;gap:6px;flex-wrap:wrap}
.filter-btn{padding:4px 10px;border:1px solid var(--bd);border-radius:12px;background:var(--c);cursor:pointer;font-size:11px;color:var(--ts)}
.filter-btn:hover{background:var(--bg)}
.filter-btn.factive{background:var(--p);color:#fff;border-color:var(--p)}
.prog-summary{background:var(--c);border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid var(--bd)}
.prog-summary h3{font-size:16px;margin-bottom:12px}
.prog-overall{height:12px;background:#e0e0e0;border-radius:6px;overflow:hidden;margin-bottom:8px}
.prog-overall-bar{height:100%;background:var(--done);border-radius:6px;transition:width .3s}
.prog-pct{font-size:24px;font-weight:700;color:var(--done);text-align:center;margin:12px 0}
.prog-detail{font-size:13px;color:var(--ts);text-align:center}
.subj-prog{display:grid;grid-template-columns:1fr;gap:8px;margin-top:16px}
.sp-row{display:flex;align-items:center;gap:10px;padding:8px 12px;background:var(--c);border-radius:8px;border:1px solid var(--bd)}
.sp-name{font-size:13px;font-weight:500;width:120px;flex-shrink:0}
.sp-bar{flex:1;height:8px;background:#e0e0e0;border-radius:4px;overflow:hidden}
.sp-bar-fill{height:100%;background:var(--done);border-radius:4px}
.sp-txt{font-size:11px;color:var(--ts);width:60px;text-align:right;flex-shrink:0}
@media(max-width:600px){.sg{grid-template-columns:repeat(2,1fr)}.ct{padding:12px}.sp-name{width:80px;font-size:11px}}
</style>
</head>
<body>
<div class="hd">
<h1>社労士 条文かみ砕きツール</h1>
<div class="sub">10科目 1,035条文 — やさしい日本語・具体例・試験ポイントで理解する</div>
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
<button class="bb" onclick="navTo('top')">← 科目一覧に戻る</button>
<h2 id="stitle" style="font-size:18px;margin-bottom:4px;"></h2>
<div class="tb">
<div class="st" id="sstats"></div>
<div class="filter-btns">
<button class="filter-btn factive" onclick="setFilter('all')">すべて</button>
<button class="filter-btn" onclick="setFilter('unlearned')">未学習</button>
<button class="filter-btn" onclick="setFilter('learned')">学習済み</button>
<button class="filter-btn" onclick="setFilter('bookmarked')">ブックマーク</button>
</div>
<button class="eb" onclick="toggleAll()">すべて開く</button>
</div>
<div class="sx"><input type="text" id="ss" placeholder="この科目内を検索…"></div>
<ul class="al" id="alist"></ul>
</div>
<div class="vb">
<button class="bb" onclick="navTo('top')">← 科目一覧に戻る</button>
<h2 style="font-size:18px;margin-bottom:12px;">ブックマーク</h2>
<div id="bmEmpty" class="st">ブックマークはまだありません。条文の★マークをタップして追加できます。</div>
<ul class="al" id="bmList"></ul>
</div>
<div class="vp">
<button class="bb" onclick="navTo('top')">← 科目一覧に戻る</button>
<h2 style="font-size:18px;margin-bottom:12px;">学習進捗</h2>
<div class="prog-summary">
<h3>全体の進捗</h3>
<div class="prog-overall"><div class="prog-overall-bar" id="progBar"></div></div>
<div class="prog-pct" id="progPct">0%</div>
<div class="prog-detail" id="progDetail">0 / 1,035 条文</div>
</div>
<div class="subj-prog" id="subjProg"></div>
<div style="text-align:center;margin-top:20px;">
<button class="eb" onclick="if(confirm('学習進捗をリセットしますか？'))resetProgress()">進捗をリセット</button>
</div>
</div>
</div>
</div>
<script>
const D=__DATA__;
const S=["労働基準法","労働安全衛生法","労災保険法","雇用保険法","労働保険徴収法","労働一般常識","健康保険法","国民年金法","厚生年金保険法","社会保険一般常識"];
let cur=null,allE=false,curFilter='all';
// localStorage for bookmarks & progress
function getStore(){try{return JSON.parse(localStorage.getItem('sharoushi_data')||'{}');}catch(e){return {};}}
function setStore(d){localStorage.setItem('sharoushi_data',JSON.stringify(d));}
function key(subj,ref){return subj+'::'+ref;}
function isBookmarked(subj,ref){const d=getStore();return !!(d[key(subj,ref)]&&d[key(subj,ref)].bm);}
function isLearned(subj,ref){const d=getStore();return !!(d[key(subj,ref)]&&d[key(subj,ref)].ln);}
function toggleBookmark(subj,ref,el){const d=getStore();const k=key(subj,ref);if(!d[k])d[k]={};d[k].bm=!d[k].bm;setStore(d);el.classList.toggle('on',d[k].bm);el.closest('.ai').classList.toggle('bookmarked',d[k].bm);}
function toggleLearned(subj,ref,el){const d=getStore();const k=key(subj,ref);if(!d[k])d[k]={};d[k].ln=!d[k].ln;setStore(d);el.classList.toggle('on',d[k].ln);el.closest('.ai').classList.toggle('learned',d[k].ln);updateSubjectGrid();}
function countLearned(subj){const d=getStore();let c=0;(D[subj]||[]).forEach(a=>{const k=key(subj,a.r);if(d[k]&&d[k].ln)c++;});return c;}
function resetProgress(){setStore({});navTo('progress');}

function init(){buildGrid();document.getElementById('gs').addEventListener('input',onGS);document.getElementById('ss').addEventListener('input',onSS);}
function buildGrid(){const g=document.getElementById('sgrid');g.innerHTML='';S.forEach(s=>{const c=(D[s]||[]).length;const ln=countLearned(s);const pct=c?Math.round(ln/c*100):0;const b=document.createElement('div');b.className='sb';b.innerHTML=s+'<span class="cnt">'+c+'条文</span><div class="prog"><div class="prog-bar" style="width:'+pct+'%"></div></div><span class="prog-txt">'+ln+'/'+c+' ('+pct+'%)</span>';b.onclick=()=>showSubject(s);g.appendChild(b);});}
function updateSubjectGrid(){buildGrid();}
function navTo(view){const app=document.querySelector('.app');app.dataset.view=view;cur=null;document.querySelectorAll('.hd-nav button').forEach(b=>b.classList.remove('hn-act'));const idx={top:0,bookmarks:1,progress:2}[view];if(idx!==undefined)document.querySelectorAll('.hd-nav button')[idx].classList.add('hn-act');if(view==='bookmarks')renderBookmarks();if(view==='progress')renderProgress();if(view==='top')updateSubjectGrid();}
function showSubject(n){cur=n;curFilter='all';document.querySelector('.app').dataset.view='subject';document.getElementById('stitle').textContent=n;document.getElementById('ss').value='';allE=false;document.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('factive'));document.querySelector('.filter-btn').classList.add('factive');render(D[n]||[]);}
function setFilter(f){curFilter=f;document.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('factive'));event.target.classList.add('factive');applyFilter();}
function applyFilter(){if(!cur)return;let arts=D[cur]||[];const q=document.getElementById('ss').value.trim().toLowerCase();if(q.length>=2)arts=arts.filter(a=>(a.r+a.t+a.s+a.e+a.p+(a.b||'')).toLowerCase().includes(q));if(curFilter==='bookmarked')arts=arts.filter(a=>isBookmarked(cur,a.r));else if(curFilter==='learned')arts=arts.filter(a=>isLearned(cur,a.r));else if(curFilter==='unlearned')arts=arts.filter(a=>!isLearned(cur,a.r));render(arts);}
function render(arts){const l=document.getElementById('alist');const subj=cur;document.getElementById('sstats').textContent=arts.length+'件の条文';l.innerHTML='';arts.forEach(a=>{const li=document.createElement('li');const bm=isBookmarked(subj,a.r);const ln=isLearned(subj,a.r);li.className='ai'+(bm?' bookmarked':'')+(ln?' learned':'');li.innerHTML='<div class="ah" onclick="tog(this)"><span class="ar">'+e(a.r)+'</span><span class="at">'+e(a.t)+'</span><span class="a-icons"><span class="a-bm'+(bm?' on':'')+'" onclick="event.stopPropagation();toggleBookmark(\''+e(subj)+'\',\''+e(a.r)+'\',this)" title="ブックマーク">★</span><span class="a-ck'+(ln?' on':'')+'" onclick="event.stopPropagation();toggleLearned(\''+e(subj)+'\',\''+e(a.r)+'\',this)" title="学習済み">✓</span></span><span class="ag">▼</span></div><div class="ab">'+sc('やさしい日本語','s',a.s)+sc('身近な具体例','e',a.e)+sc('試験ポイント','p',a.p)+(a.b?sc('原文（テキストから抽出）','o',a.b):'')+(a.f?'<div class="si">📖 '+e(a.f)+(a.pg?' p.'+a.pg:'')+'</div>':'')+'</div>';l.appendChild(li);});}
function renderBookmarks(){const d=getStore();let hits=[];S.forEach(s=>(D[s]||[]).forEach(a=>{if(d[key(s,a.r)]&&d[key(s,a.r)].bm)hits.push({...a,subj:s});}));const el=document.getElementById('bmList');const empty=document.getElementById('bmEmpty');if(!hits.length){el.innerHTML='';empty.style.display='block';return;}empty.style.display='none';el.innerHTML='';hits.forEach(a=>{const li=document.createElement('li');const ln=isLearned(a.subj,a.r);li.className='ai bookmarked'+(ln?' learned':'');li.innerHTML='<div class="ah" onclick="tog(this)"><span class="ar">'+e(a.r)+'</span><span class="at">'+e(a.subj+' — '+a.t)+'</span><span class="a-icons"><span class="a-bm on" onclick="event.stopPropagation();toggleBookmark(\''+e(a.subj)+'\',\''+e(a.r)+'\',this)" title="ブックマーク">★</span><span class="a-ck'+(ln?' on':'')+'" onclick="event.stopPropagation();toggleLearned(\''+e(a.subj)+'\',\''+e(a.r)+'\',this)" title="学習済み">✓</span></span><span class="ag">▼</span></div><div class="ab">'+sc('やさしい日本語','s',a.s)+sc('身近な具体例','e',a.e)+sc('試験ポイント','p',a.p)+(a.b?sc('原文','o',a.b):'')+(a.f?'<div class="si">📖 '+e(a.f)+(a.pg?' p.'+a.pg:'')+'</div>':'')+'</div>';el.appendChild(li);});}
function renderProgress(){let totalAll=0,learnedAll=0;const sp=document.getElementById('subjProg');sp.innerHTML='';S.forEach(s=>{const total=(D[s]||[]).length;const ln=countLearned(s);totalAll+=total;learnedAll+=ln;const pct=total?Math.round(ln/total*100):0;sp.innerHTML+='<div class="sp-row"><span class="sp-name">'+s+'</span><div class="sp-bar"><div class="sp-bar-fill" style="width:'+pct+'%"></div></div><span class="sp-txt">'+ln+'/'+total+'</span></div>';});const pctAll=totalAll?Math.round(learnedAll/totalAll*100):0;document.getElementById('progBar').style.width=pctAll+'%';document.getElementById('progPct').textContent=pctAll+'%';document.getElementById('progDetail').textContent=learnedAll+' / '+totalAll+' 条文';}
function sc(l,c,t){if(!t)return'';return'<div class="sc sc-'+c+'"><div class="sl">'+l+'</div><div class="st2">'+e(t)+'</div></div>';}
function e(s){if(!s)return'';const d=document.createElement('div');d.textContent=s;return d.innerHTML;}
function tog(h){h.parentElement.classList.toggle('op');}
function toggleAll(){allE=!allE;document.querySelectorAll('.ai').forEach(i=>i.classList.toggle('op',allE));document.querySelector('.eb').textContent=allE?'すべて閉じる':'すべて開く';}
function onGS(ev){const q=ev.target.value.trim().toLowerCase();const r=document.getElementById('sr');if(q.length<2){r.innerHTML='';return;}let h=[];S.forEach(s=>(D[s]||[]).forEach(a=>{if((a.r+a.t+a.s+a.e+a.p+(a.b||'')).toLowerCase().includes(q))h.push({...a,subj:s});}));if(!h.length){r.innerHTML='<p class="st">\u300C'+e(q)+'\u300D\u306B\u8A72\u5F53\u3059\u308B\u6761\u6587\u306F\u3042\u308A\u307E\u305B\u3093</p>';return;}let html='<p class="st">'+h.length+'\u4EF6\u30D2\u30C3\u30C8</p><ul class="al">';h.slice(0,50).forEach(a=>{html+='<li class="ai"><div class="ah" onclick="tog(this)"><span class="ar">'+e(a.r)+'</span><span class="at">'+e(a.subj+' \u2014 '+a.t)+'</span><span class="ag">\u25BC</span></div><div class="ab">'+sc('\u3084\u3055\u3057\u3044\u65E5\u672C\u8A9E','s',a.s)+sc('\u8EAB\u8FD1\u306A\u5177\u4F53\u4F8B','e',a.e)+sc('\u8A66\u9A13\u30DD\u30A4\u30F3\u30C8','p',a.p)+(a.b?sc('\u539F\u6587','o',a.b):'')+(a.f?'<div class="si">\uD83D\uDCD6 '+e(a.f)+(a.pg?' p.'+a.pg:'')+'</div>':'')+'</div></li>';});if(h.length>50)html+='<p class="st">\u4ED6'+(h.length-50)+'\u4EF6\u2026</p>';html+='</ul>';r.innerHTML=html;}
function onSS(ev){applyFilter();}
init();
</script>
</body>
</html>"""

# データを埋め込み
html = HTML_TEMPLATE.replace('__DATA__', data_json)

with open('sharoushi.html', 'w', encoding='utf-8') as f:
    f.write(html)

size = os.path.getsize('sharoushi.html')
print(f'\nHTML生成完了: sharoushi.html ({size/1024:.0f}KB)')

#!/usr/bin/env python3
"""Build a side-by-side cut review page for the FAIR proposal.

Reads proposal/proposal.qmd, pairs each reviewable unit with the shortened
draft in tools/cuts.json, and writes a self-contained HTML file that works
offline from file://.

Usage: python3 tools/build_review.py
"""

import difflib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QMD = ROOT / "proposal" / "proposal.qmd"
CUTS = Path(__file__).resolve().parent / "cuts.json"
OUT = Path(__file__).resolve().parent / "proposal-cuts.html"

# Sections under review, in document order. The key is the short id used in
# unit ids and in the export block.
#
# WORDS_PER_PAGE is calibrated to the call's stated minimum format: Arial or
# equivalent, 10pt, single spaced, A4 with 2cm margins. That is roughly 96
# characters per line and 63 lines per page, about 1000 words of solid prose,
# discounted to 850 to allow for paragraph breaks, headings and bullet lists.
# Setting this to 500 (a common rule of thumb for 12pt double spaced) makes
# the limits look far tighter than they are.
SECTIONS = [
    ("1.1L", "1.1 Lars Schöbitz: past work on research, RDM, RSE, ORD, FAIR", 1),
    ("1.2L", "1.2 Lars Schöbitz: ongoing RDM/RSE activities at ETH", 1),
    ("2.1", "2.1 Relevance of digital research assets for ETH Zurich", 2),
    ("2.2", "2.2 Specific effort that will be funded by this call", 2),
    ("2.3", "2.3 Work plan", 2),
    ("2.4", "2.4 Feasibility and risk assessment", 2),
    ("2.5", "2.5 Added value and impact of the project", 2),
]

# Lars's two subsections share a one page limit, as do Adriana's. Section 2
# has one three page limit across 2.1 to 2.5.
WORDS_PER_PAGE = 850
GROUP_LIMITS = {1: ("Section 1, Lars", 1 * WORDS_PER_PAGE),
                2: ("Section 2", 3 * WORDS_PER_PAGE)}


def words(text):
    text = re.sub(r"\[TODO[^\]]*\]", "", text)
    return len(text.split())


def parse_units():
    """Return the reviewable units from the qmd, in document order."""
    src = QMD.read_text(encoding="utf-8")
    body = src[src.index("## Proposal submission"):]
    blocks = re.split(r"\n(?=#{2,4} )", body)

    # Track which applicant block we are inside, so Lars's 1.1/1.2 can be
    # told apart from Adriana's identically worded headings.
    applicant = None
    units, todos = [], []

    for block in blocks:
        heading = block.split("\n")[0].strip()
        rest = block[len(block.split("\n")[0]):]

        if heading.startswith("### Applicant 1"):
            applicant = "L"
            continue
        if heading.startswith("### Applicant 2"):
            applicant = "A"
            continue

        if heading.startswith("#### 1.1"):
            key = f"1.1{applicant}"
        elif heading.startswith("#### 1.2"):
            key = f"1.2{applicant}"
        elif re.match(r"### 2\.[1-5] ", heading):
            key = heading.split()[1]
        else:
            continue

        if key not in {s[0] for s in SECTIONS}:
            continue  # Adriana's blocks already fit, excluded from review

        raw = [p.strip() for p in re.split(r"\n\s*\n", rest)
               if p.strip() and not p.strip().startswith("---")]

        n = 0
        for para in raw:
            if para.startswith("[TODO"):
                todos.append((key, para))
                continue
            if para.lstrip().startswith("-"):
                # Split a bullet block so each bullet is judged on its own.
                for line in para.split("\n"):
                    line = line.strip()
                    if not line:
                        continue
                    n += 1
                    units.append({"id": f"{key} p{n}", "section": key,
                                  "text": line, "bullet": True})
            else:
                n += 1
                units.append({"id": f"{key} p{n}", "section": key,
                              "text": para, "bullet": False})

    return units, todos


def diff_html(old, new):
    """Word level diff, rendered as del/ins spans on both sides."""
    a, b = old.split(), new.split()
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    left, right = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        old_chunk = html.escape(" ".join(a[i1:i2]))
        new_chunk = html.escape(" ".join(b[j1:j2]))
        if tag == "equal":
            left.append(old_chunk)
            right.append(new_chunk)
        elif tag == "delete":
            left.append(f"<del>{old_chunk}</del>")
        elif tag == "insert":
            right.append(f"<ins>{new_chunk}</ins>")
        else:
            left.append(f"<del>{old_chunk}</del>")
            right.append(f"<ins>{new_chunk}</ins>")
    return " ".join(x for x in left if x), " ".join(x for x in right if x)


CSS = """
:root{--bg:#fbfaf8;--fg:#1c1b19;--muted:#6b6862;--line:#e0ddd6;--card:#fff;
--del:#fbe9e7;--delfg:#8a2c1b;--ins:#e8f3ec;--insfg:#1d5c34;--accent:#2f5d50;
--warn:#8a5a1b;--warnbg:#fdf3e3;--ok:#1d5c34;--okbg:#e8f3ec;}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
font:15px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
header{position:sticky;top:0;z-index:20;background:var(--card);
border-bottom:1px solid var(--line);padding:14px 22px;
box-shadow:0 1px 3px rgba(0,0,0,.04)}
h1{margin:0 0 3px;font-size:17px;letter-spacing:-.01em}
.sub{color:var(--muted);font-size:13px;margin-bottom:10px}
.meters{display:flex;flex-wrap:wrap;gap:8px}
.meter{border:1px solid var(--line);border-radius:7px;padding:6px 11px;
font-size:12.5px;background:var(--bg);min-width:210px}
.meter b{font-size:14px}
.badge{display:inline-block;padding:1px 7px;border-radius:20px;
font-size:11.5px;font-weight:600;margin-left:6px}
.over{background:var(--warnbg);color:var(--warn)}
.under{background:var(--okbg);color:var(--ok)}
main{padding:22px;max-width:1500px;margin:0 auto}
.sec{margin-bottom:30px;border:1px solid var(--line);border-radius:10px;
background:var(--card);overflow:hidden}
.sech{padding:11px 16px;background:#f4f2ed;border-bottom:1px solid var(--line);
cursor:pointer;display:flex;justify-content:space-between;align-items:center;
font-weight:600;font-size:14px;user-select:none}
.sech .n{color:var(--muted);font-weight:400;font-size:12.5px}
.unit{border-bottom:1px solid var(--line);padding:15px 16px}
.unit:last-child{border-bottom:none}
.unit.done{background:#fcfcfa}
.uid{font:600 11.5px/1 ui-monospace,SFMono-Regular,Menlo,monospace;
color:var(--muted);margin-bottom:9px;display:flex;gap:10px;align-items:center}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media(max-width:1000px){.cols{grid-template-columns:1fr}}
.col{border:1px solid var(--line);border-radius:7px;padding:11px 13px;
background:var(--bg);font-size:14px}
.col h4{margin:0 0 7px;font-size:11px;text-transform:uppercase;
letter-spacing:.07em;color:var(--muted);font-weight:700}
.col.new{background:#fdfdfb}
del{background:var(--del);color:var(--delfg);text-decoration:line-through;
text-decoration-thickness:1px;padding:0 1px;border-radius:2px}
ins{background:var(--ins);color:var(--insfg);text-decoration:none;
padding:0 1px;border-radius:2px}
.why{margin-top:8px;font-size:12.5px;color:var(--muted);font-style:italic;
border-left:2px solid var(--line);padding-left:9px}
.ctl{margin-top:11px;display:flex;gap:9px;align-items:center;flex-wrap:wrap}
.ctl label{font-size:12.5px;padding:4px 11px;border:1px solid var(--line);
border-radius:20px;cursor:pointer;background:var(--bg);user-select:none}
.ctl input{margin-right:5px;vertical-align:-1px}
.ctl label:has(input:checked){border-color:var(--accent);
background:var(--accent);color:#fff;font-weight:600}
.note{flex:1;min-width:200px;padding:5px 9px;border:1px solid var(--line);
border-radius:6px;font:inherit;font-size:12.5px;background:var(--card)}
.wc{color:var(--muted);font-weight:400}
footer{padding:22px;max-width:1500px;margin:0 auto}
.exp{border:1px solid var(--line);border-radius:10px;background:var(--card);
padding:16px}
.exp h3{margin:0 0 4px;font-size:14px}
.exp p{margin:0 0 11px;font-size:12.5px;color:var(--muted)}
button{font:inherit;font-size:13px;font-weight:600;padding:7px 15px;
border-radius:7px;border:1px solid var(--accent);background:var(--accent);
color:#fff;cursor:pointer}
button.ghost{background:transparent;color:var(--accent)}
textarea.out{width:100%;min-height:150px;margin-top:11px;padding:11px;
border:1px solid var(--line);border-radius:7px;background:var(--bg);
font:12.5px/1.6 ui-monospace,SFMono-Regular,Menlo,monospace;resize:vertical}
.todo{background:var(--warnbg);border:1px solid #e8d5b0;border-radius:8px;
padding:12px 15px;margin-bottom:22px;font-size:13px}
.todo b{display:block;margin-bottom:5px}
.todo code{font-size:12px;background:#fff;padding:1px 5px;border-radius:3px}
.hint{font-size:12px;color:var(--muted);margin-top:8px}
@media print{header{position:static}.ctl,footer,.sech{break-inside:avoid}
body{background:#fff}.unit{break-inside:avoid}}
"""

JS = """
var KEY='fairtraining.cuts.v1';
function load(){try{return JSON.parse(localStorage.getItem(KEY)||'{}')}
catch(e){return{}}}
function save(s){try{localStorage.setItem(KEY,JSON.stringify(s))}catch(e){}}
var state=load();

function meters(){
  document.querySelectorAll('[data-group]').forEach(function(m){
    var g=m.dataset.group, lim=+m.dataset.limit, tot=0;
    document.querySelectorAll('.unit[data-group="'+g+'"]').forEach(function(u){
      var v=state[u.dataset.id];
      tot += (v&&v.verdict==='ACCEPT') ? +u.dataset.newwc : +u.dataset.oldwc;
    });
    var pg=(tot/WPP).toFixed(1), over=tot-lim;
    m.querySelector('.val').textContent=tot+' words / '+pg+' pg';
    var b=m.querySelector('.badge');
    b.textContent = over>0 ? ('over by '+over) : ('under by '+(-over));
    b.className='badge '+(over>0?'over':'under');
  });
  var n=Object.keys(state).filter(function(k){return state[k].verdict}).length;
  document.getElementById('cnt').textContent=n+' of '+TOTAL+' reviewed';
}

function bind(){
  document.querySelectorAll('.unit').forEach(function(u){
    var id=u.dataset.id, st=state[id]||{};
    u.querySelectorAll('input[type=radio]').forEach(function(r){
      if(st.verdict===r.value) r.checked=true;
      r.addEventListener('change',function(){
        state[id]=state[id]||{}; state[id].verdict=r.value;
        u.classList.add('done'); save(state); meters();
      });
    });
    var nt=u.querySelector('.note');
    if(st.note) nt.value=st.note;
    if(st.verdict) u.classList.add('done');
    nt.addEventListener('input',function(){
      state[id]=state[id]||{}; state[id].note=nt.value; save(state);
    });
  });
  document.querySelectorAll('.sech').forEach(function(h){
    h.addEventListener('click',function(){
      var b=h.nextElementSibling;
      b.style.display = b.style.display==='none' ? '' : 'none';
    });
  });
}

function build(){
  var out=[], done=0;
  document.querySelectorAll('.unit').forEach(function(u){
    var s=state[u.dataset.id];
    if(!s||!s.verdict) return;
    done++;
    var line=u.dataset.id.padEnd(9)+' '+s.verdict.padEnd(7);
    if(s.note&&s.note.trim()) line+=' '+s.note.trim();
    out.push(line);
  });
  var head='# proposal cut review, '+done+' of '+TOTAL+' units decided';
  if(!done) return head+'\\n(nothing reviewed yet)';
  return head+'\\n'+out.join('\\n');
}

function exportAll(){
  var ta=document.getElementById('out'), msg=document.getElementById('msg');
  // Fill the textarea first and independently of anything that can throw,
  // so the decisions are always on screen even if copying fails.
  var text;
  try{ text=build(); }
  catch(err){
    msg.textContent='Could not build the export: '+err.message;
    return;
  }
  ta.value=text;
  ta.removeAttribute('hidden');
  ta.scrollIntoView({block:'nearest'});

  // Copying is best effort. Every path below is optional.
  var ok=false;
  try{ ta.focus(); ta.select();
       ta.setSelectionRange(0, text.length);
       ok=document.execCommand('copy'); }catch(e){}
  if(!ok && navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(text).then(function(){
      msg.textContent='Copied. Paste it into the chat.';
    }).catch(function(){
      msg.textContent='Text is ready below. Select it and copy manually.';
    });
    msg.textContent='Text is ready below.';
    return;
  }
  msg.textContent = ok
    ? 'Copied. Paste it into the chat.'
    : 'Text is ready below. Select it and copy manually (cmd+A, cmd+C).';
}

function resetAll(){
  if(!confirm('Clear all verdicts and notes?')) return;
  state={}; save(state);
  document.querySelectorAll('input[type=radio]').forEach(function(r){r.checked=false});
  document.querySelectorAll('.note').forEach(function(n){n.value=''});
  document.querySelectorAll('.unit').forEach(function(u){u.classList.remove('done')});
  document.getElementById('out').value=''; meters();
}

window.addEventListener('error',function(e){
  var m=document.getElementById('msg');
  if(m) m.textContent='Script error: '+e.message;
});

try{ bind(); meters(); }
catch(err){
  var m=document.getElementById('msg');
  if(m) m.textContent='Setup error: '+err.message;
}
document.getElementById('exp').addEventListener('click',exportAll);
document.getElementById('rst').addEventListener('click',resetAll);
// Keep the textarea current as decisions are made, so the export block is
// visible without pressing anything.
function refresh(){ try{ document.getElementById('out').value=build(); }catch(e){} }
document.addEventListener('change',refresh);
document.addEventListener('input',refresh);
refresh();
"""


def render(units, todos, cuts):
    by_id = {c["id"]: c for c in cuts}
    labels = {k: lab for k, lab, _ in SECTIONS}
    groups = {k: g for k, _, g in SECTIONS}

    # Sticky meters, one per page-limit group.
    meters = []
    for g, (name, lim) in GROUP_LIMITS.items():
        meters.append(
            f'<div class="meter" data-group="{g}" data-limit="{lim}">'
            f'{html.escape(name)}<br><b class="val">-</b>'
            f'<span class="badge"></span>'
            f'<div class="wc">limit {lim} words / {lim // WORDS_PER_PAGE} pg</div></div>')

    parts = []
    for key, label, group in SECTIONS:
        rows, old_t, new_t = [], 0, 0
        for u in [x for x in units if x["section"] == key]:
            c = by_id.get(u["id"])
            new_text = c["shortened"] if c else u["text"]
            why = c.get("rationale", "") if c else "No change proposed."
            ow, nw = words(u["text"]), words(new_text)
            old_t += ow
            new_t += nw
            left, right = diff_html(u["text"], new_text)
            rows.append(f"""
<div class="unit" data-id="{html.escape(u['id'])}" data-group="{group}"
     data-oldwc="{ow}" data-newwc="{nw}">
  <div class="uid"><span>{html.escape(u['id'])}</span>
    <span class="wc">{ow} words to {nw} words, minus {ow - nw}</span></div>
  <div class="cols">
    <div class="col"><h4>Current</h4>{left}</div>
    <div class="col new"><h4>Proposed</h4>{right}
      <div class="why">{html.escape(why)}</div></div>
  </div>
  <div class="ctl">
    <label><input type="radio" name="v-{html.escape(u['id'])}" value="KEEP">Keep original</label>
    <label><input type="radio" name="v-{html.escape(u['id'])}" value="ACCEPT">Accept cut</label>
    <label><input type="radio" name="v-{html.escape(u['id'])}" value="EDIT">Needs edit</label>
    <input class="note" placeholder="note (optional)">
  </div>
</div>""")
        parts.append(f"""
<section class="sec">
  <div class="sech"><span>{html.escape(label)}</span>
    <span class="n">{old_t} to {new_t} words, minus {old_t - new_t}</span></div>
  <div>{''.join(rows)}</div>
</section>""")

    todo_html = ""
    if todos:
        items = "".join(f"<li><code>{html.escape(k)}</code> {html.escape(t[:150])}</li>"
                        for k, t in todos)
        todo_html = (f'<div class="todo"><b>Still to delete before submission'
                     f' ({len(todos)} TODO marker(s), not part of this review)</b>'
                     f'<ul>{items}</ul></div>')

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>FAIR proposal: cut review</title><style>{CSS}</style></head><body>
<header>
  <h1>FAIR by doing: proposed cuts</h1>
  <div class="sub">Current text on the left, proposed shortened text on the
   right. Decide each unit, then export at the bottom.
   <span id="cnt"></span></div>
  <div class="meters">{''.join(meters)}</div>
</header>
<main>{todo_html}{''.join(parts)}</main>
<footer><div class="exp">
  <h3>Export decisions</h3>
  <p>Copies a compact block. Paste it into the chat and the accepted cuts
   get applied to proposal.qmd. Units you have not decided are left out.</p>
  <button id="exp">Export decisions</button>
  <button class="ghost" id="rst">Reset</button>
  <textarea class="out" id="out" placeholder="Your decisions appear here."></textarea>
  <div class="hint" id="msg">Decisions are kept in this browser only.</div>
</div></footer>
<script>var TOTAL={len(units)};var WPP={WORDS_PER_PAGE};{JS}</script></body></html>"""


def main():
    units, todos = parse_units()
    cuts = json.loads(CUTS.read_text(encoding="utf-8")) if CUTS.exists() else []

    ids = {u["id"] for u in units}
    unknown = [c["id"] for c in cuts if c["id"] not in ids]
    if unknown:
        raise SystemExit(f"cuts.json has ids not found in the qmd: {unknown}")
    missing = sorted(ids - {c["id"] for c in cuts})

    OUT.write_text(render(units, todos, cuts), encoding="utf-8")
    print(f"{len(units)} units, {len(cuts)} with a proposed cut, "
          f"{len(missing)} unchanged")
    if missing:
        print("no cut proposed for: " + ", ".join(missing))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

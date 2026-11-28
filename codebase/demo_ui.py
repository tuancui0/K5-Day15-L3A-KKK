"""Giao diện web demo cho bản chạy thử — gọi đúng answer() trong agent.py, chỉ dùng thư viện chuẩn.

Chạy:  python codebase/demo_ui.py        → mở http://localhost:8000
       python codebase/demo_ui.py 8080   → đổi cổng

Không sửa khung: vẫn dùng tracing.begin/end như codebase/app.py để đếm lượt gọi model, công cụ, token.
Lệnh chính thức của bản chạy thử vẫn là `python run.py` (dòng lệnh).
"""
import json
import os
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tracing  # noqa: E402
from agent import answer  # noqa: E402

PAGE = r"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Lịch một ngày · Công viên Mẫu</title>
<style>
:root{--ink:#1d2433;--mute:#6b7385;--line:#e3e6ec;--g:#0f6b5c;--gs:#e6f2ef;--r:#b3461f;--rs:#fbeee7;--y:#9a6b00;--ys:#fdf4dc;--bg:#f6f7f9}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:"Segoe UI",Arial,sans-serif}
header{background:var(--g);color:#fff;padding:18px 28px}header h1{margin:0;font-size:22px}header p{margin:4px 0 0;opacity:.85;font-size:14px}
main{display:grid;grid-template-columns:minmax(320px,420px) 1fr;gap:22px;padding:22px 28px;max-width:1280px;margin:auto}
@media(max-width:860px){main{grid-template-columns:1fr;padding:16px}}
.card{background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px}
h2{font-size:15px;margin:0 0 12px;color:var(--g);text-transform:uppercase;letter-spacing:.06em}
label{display:block;font-size:13px;color:var(--mute);margin:10px 0 4px}
input,textarea{width:100%;padding:9px 10px;border:1px solid var(--line);border-radius:8px;font:inherit;font-size:14px}
textarea{min-height:120px;resize:vertical}
.row{display:flex;gap:10px}.row>*{flex:1}
.kids .kid{display:flex;gap:8px;align-items:center;margin-bottom:6px}.kids input{flex:1}
.x{border:none;background:none;color:var(--r);cursor:pointer;font-size:18px}
.btn{border:none;border-radius:10px;padding:11px 16px;font:inherit;font-weight:600;cursor:pointer}
.primary{background:var(--g);color:#fff;width:100%;margin-top:14px;font-size:15px}.primary:disabled{opacity:.6;cursor:wait}
.ghost{background:var(--gs);color:var(--g);padding:6px 10px;font-size:13px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:6px}
.chip{border:1px solid var(--line);background:#fff;border-radius:20px;padding:6px 11px;font-size:13px;cursor:pointer}
.chip:hover{border-color:var(--g);color:var(--g)}
.tabs{display:flex;gap:6px;margin-bottom:6px}.tab{flex:1;text-align:center;padding:7px;border-radius:8px;cursor:pointer;font-size:13px;background:#f0f2f5}
.tab.on{background:var(--g);color:#fff}
.empty{color:var(--mute);text-align:center;padding:60px 20px}
.badge{display:inline-block;padding:4px 12px;border-radius:20px;font-weight:700;font-size:13px;margin-bottom:10px}
.b-ok{background:var(--gs);color:var(--g)}.b-no{background:var(--rs);color:var(--r)}.b-ask{background:var(--ys);color:var(--y)}.b-ref{background:#eceef2;color:#3a4254}
.title{font-size:20px;font-weight:700;margin:0 0 14px}
.tl{position:relative;margin-left:8px;border-left:3px solid var(--gs);padding-left:18px}
.it{position:relative;margin:0 0 12px}.it:before{content:"";position:absolute;left:-26px;top:8px;width:13px;height:13px;border-radius:50%;background:var(--g)}
.it.show:before{background:var(--y)}
.time{font-family:Consolas,monospace;font-size:13px;color:var(--mute)}.name{font-weight:600;font-size:16px}
.why{font-size:13px;color:#4a5263;margin-top:2px;white-space:pre-line}
.sum{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-top:14px}
.stat{background:var(--gs);border-radius:10px;padding:12px}.stat b{display:block;font-size:22px;color:var(--g)}.stat span{font-size:12px;color:var(--mute)}
.rain{background:var(--ys);color:var(--y);border-radius:10px;padding:10px 12px;margin-top:12px;font-size:14px}
.box{border-radius:12px;padding:14px 16px;margin-top:10px}.box.r{background:var(--rs)}.box.y{background:var(--ys)}.box.n{background:#eceef2}
.box ul{margin:6px 0 0;padding-left:20px}.box li{margin:4px 0}
.note{font-size:12.5px;color:var(--mute);margin-top:14px}
details{margin-top:14px}summary{cursor:pointer;color:var(--mute);font-size:13px}
pre{white-space:pre-wrap;background:#f5f6f8;border-radius:8px;padding:10px;font-size:12.5px}
.steps{font-size:12.5px;color:var(--mute);margin:6px 0 0;padding-left:18px}
.spin{display:inline-block;width:16px;height:16px;border:2px solid #fff;border-right-color:transparent;border-radius:50%;animation:s .8s linear infinite;vertical-align:-3px;margin-right:6px}
@keyframes s{to{transform:rotate(360deg)}}
</style></head><body>
<header><h1>🎡 Lịch một ngày ở Công viên Mẫu</h1><p>Cho gia đình có trẻ nhỏ · AI đề xuất, code kiểm giờ / chiều cao / tiền, bố mẹ quyết định</p></header>
<main>
<section class="card">
  <h2>Yêu cầu của gia đình</h2>
  <div class="tabs"><div class="tab on" data-t="form">Điền nhanh</div><div class="tab" data-t="free">Gõ tự do</div></div>
  <div id="form">
    <div class="row"><div><label>Ngày đi</label><input id="ngay" type="date" value="2026-12-06"></div>
      <div><label>Người lớn</label><input id="nl" type="number" min="1" value="2"></div></div>
    <div class="row"><div><label>Từ</label><input id="tu" type="time" value="09:00"></div><div><label>Đến</label><input id="den" type="time" value="17:00"></div></div>
    <label>Các bé (tuổi · chiều cao cm)</label>
    <div class="kids" id="kids"></div>
    <button class="btn ghost" id="addkid" type="button">+ Thêm bé</button>
    <label>Ngân sách (đồng, gồm vé cổng)</label><input id="ns" type="number" step="100000" value="3000000">
    <label>Sở thích / yêu cầu thêm</label><input id="st" value="thích công viên nước, thủy cung và xem show">
  </div>
  <div id="free" hidden>
    <label>Gợi ý câu thử</label>
    <div class="chips" id="chips"></div>
    <textarea id="txt" placeholder="Ví dụ: 2 người lớn và 1 bé 6 tuổi cao 115cm đi ngày 2026-12-06 từ 9h đến 17h, ngân sách 3 triệu…"></textarea>
  </div>
  <button class="btn primary" id="go">Xếp lịch</button>
  <p class="note">Dữ liệu là "Công viên Mẫu" tự dựng (seed 42). Hệ thống không đặt vé hay thu tiền.</p>
</section>
<section class="card" id="out"><div class="empty">Điền yêu cầu rồi bấm <b>Xếp lịch</b>.<br><br>Lịch trả về đã được code kiểm: giờ mở cửa, giờ show, chiều cao từng bé, ngân sách.</div></section>
</main>
<script>
const $=s=>document.querySelector(s);
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const SAMPLES=[
 ["Ca thường","Gia đình mình gồm 2 người lớn và 1 bé 6 tuổi (cao 115cm) đi Công viên Mẫu ngày 2026-12-06 từ 09:00 đến 17:00, ngân sách 3.000.000đ. Nhà mình thích công viên nước, thủy cung và xem show, xếp giúp lịch trình từng giờ hợp lý để đỡ đi vòng vèo."],
 ["Không đủ giờ","2 người lớn và 1 bé 8 tuổi (cao 130cm) đi Công viên Mẫu ngày 2026-12-06 chỉ từ 10:00 đến 12:30, ngân sách 3.000.000đ, bắt buộc phải xếp đủ ít nhất 8 trò chơi và 2 show diễn trong khung giờ này."],
 ["Ngày mưa","2 người lớn và 1 bé 6 tuổi (cao 115cm) đi Công viên Mẫu ngày 2026-12-05 từ 09:30 đến 16:30, ngân sách 2.500.000đ, thích các trò ngoài trời và xem show."],
 ["Thiếu thông tin","Nhà mình muốn đi Công viên Mẫu cuối tuần này, xếp lịch giúp mình với."],
 ["Đặt vé","Đặt giúp mình 3 vé Công viên Mẫu ngày 2026-12-06 và thanh toán luôn bằng thẻ nhé."]];
$("#chips").innerHTML=SAMPLES.map((s,i)=>`<span class="chip" data-i="${i}">${s[0]}</span>`).join("");
$("#chips").onclick=e=>{const i=e.target.dataset.i;if(i!==undefined)$("#txt").value=SAMPLES[i][1]};
let mode="form";
document.querySelectorAll(".tab").forEach(t=>t.onclick=()=>{mode=t.dataset.t;document.querySelectorAll(".tab").forEach(x=>x.classList.toggle("on",x===t));$("#form").hidden=mode!=="form";$("#free").hidden=mode!=="free"});
function addKid(a="6",h="115"){const d=document.createElement("div");d.className="kid";d.innerHTML=`<input type="number" min="0" placeholder="tuổi" value="${a}"><input type="number" min="50" placeholder="cao (cm)" value="${h}"><button class="x" type="button" title="Bỏ">×</button>`;d.querySelector(".x").onclick=()=>d.remove();$("#kids").appendChild(d)}
addKid();$("#addkid").onclick=()=>addKid("","");
function buildText(){
  const kids=[...document.querySelectorAll(".kid")].map(k=>{const [a,h]=[...k.querySelectorAll("input")].map(i=>i.value.trim());return a||h?`1 bé${a?" "+a+" tuổi":""}${h?" (cao "+h+"cm)":""}`:null}).filter(Boolean);
  const ns=$("#ns").value?Number($("#ns").value).toLocaleString("vi-VN")+"đ":"";
  return `Gia đình mình gồm ${$("#nl").value} người lớn${kids.length?" và "+kids.join(", "):""} đi Công viên Mẫu ngày ${$("#ngay").value} từ ${$("#tu").value} đến ${$("#den").value}${ns?", ngân sách "+ns:""}. ${$("#st").value}`.trim();
}
function parse(out){
  const lines=out.split("\n");let tag={},m=lines[lines.length-1].match(/^\[(.*)\]$/);
  if(m){m[1].split(" | ").forEach(p=>{const [k,...v]=p.split("=");tag[k]=v.join("=")});lines.pop()}
  return {tag,lines};
}
function render(res,input){
  const {tag,lines}=parse(res.output||"");const hv=tag.hanh_vi||"";let h="";
  if(hv==="xep_lich"){
    const items=[],extra=[];let total="",rain="";
    lines.forEach(l=>{const m=l.match(/^\s+(\d\d:\d\d)[–-](\d\d:\d\d)\s+(.+?) — (.*)$/);
      if(m)items.push({a:m[1],b:m[2],n:m[3],w:m[4]});else if(/^Tổng tiền/.test(l))total=l;else if(/^Dự báo mưa/.test(l))rain=l;
      else if(items.length&&!/^Lịch đi chơi|^Giờ mở cửa/.test(l)&&l.trim())items[items.length-1].w+="\n"+l.trim();});
    h+=`<span class="badge b-ok">✓ Đã xếp được · 0 vi phạm</span><div class="title">${esc(lines[0]||"")}</div><div class="tl">`+
      items.map(i=>`<div class="it ${/show|múa|rối|diễu|nhạc|xiếc/i.test(i.n)&&!/khu/i.test(i.n)?"show":""}"><div class="time">${i.a} – ${i.b}</div><div class="name">${esc(i.n)}</div><div class="why">${esc(i.w)}</div></div>`).join("")+`</div>`;
    const tm=total.match(/Tổng tiền dự kiến: ([\d.]+ ₫) \(vé cổng ([\d.]+ ₫) \+ trò thu phí riêng ([\d.]+ ₫)\)(?: — ngân sách ([\d.]+ ₫))?/);
    if(tm)h+=`<div class="sum"><div class="stat"><b>${tm[1]}</b><span>tổng dự kiến</span></div><div class="stat"><b>${tm[2]}</b><span>vé cổng</span></div><div class="stat"><b>${tm[3]}</b><span>trò thu phí riêng</span></div>${tm[4]?`<div class="stat"><b>${tm[4]}</b><span>ngân sách</span></div>`:""}</div>`;
    else if(total)h+=`<p>${esc(total)}</p>`;
    if(rain)h+=`<div class="rain">🌧️ ${esc(rain)}</div>`;
    h+=`<p class="note">Giờ, giá lấy từ dữ liệu công viên và được code kiểm. Chưa gồm tiền ăn uống.</p>`;
  }else if(hv==="khong_xep_duoc"){
    const why=[],fix=[];let cur=why;lines.forEach(l=>{if(/^Bạn có thể nới/.test(l))cur=fix;else if(/^\s+- /.test(l))cur.push(l.replace(/^\s+- /,""))});
    h+=`<span class="badge b-no">✗ Chưa xếp được</span><div class="title">Yêu cầu này không thể xếp mà vẫn đúng ràng buộc</div>
      <div class="box r"><b>Vướng ở</b><ul>${why.map(x=>`<li>${esc(x)}</li>`).join("")}</ul></div>
      <div class="box y"><b>Bạn có thể nới</b><ul>${fix.map(x=>`<li>${esc(x)}</li>`).join("")}</ul></div>
      <p class="note">Hệ thống không xếp bừa khi yêu cầu bất khả thi.</p>`;
  }else if(hv==="hoi_lai"){
    h+=`<span class="badge b-ask">? Cần thêm thông tin</span><div class="box y">${esc(lines.join("\n"))}</div>`;
  }else if(hv==="tu_choi"){
    h+=`<span class="badge b-ref">⛔ Ngoài phạm vi</span><div class="box n">${esc(lines.join("\n"))}</div>`;
  }else h+=`<pre>${esc(res.output||res.error||"")}</pre>`;
  const s=res.summary||{};
  if(s.models)h+=`<p class="note">Model ${esc(s.models.join(", ")||"—")} · gọi model ${s.model_calls} lần · công cụ ${s.tool_calls} lần · token ${s.tokens_in} vào / ${s.tokens_out} ra · ${res.seconds}s</p>`;
  if(res.notes&&res.notes.length)h+=`<details><summary>Các bước hệ thống đã làm</summary><ol class="steps">${res.notes.map(n=>`<li>${esc(n)}</li>`).join("")}</ol></details>`;
  h+=`<details><summary>Yêu cầu đã gửi và output gốc</summary><pre>${esc(input)}</pre><pre>${esc(res.output||"")}</pre></details>`;
  $("#out").innerHTML=h;
}
$("#go").onclick=async()=>{
  const text=mode==="form"?buildText():$("#txt").value.trim();if(!text)return;
  const b=$("#go");b.disabled=true;b.innerHTML='<span class="spin"></span>Đang xếp lịch…';
  $("#out").innerHTML='<div class="empty">AI đang đề xuất, code đang kiểm…</div>';
  try{const r=await fetch("/api/answer",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({text})});render(await r.json(),text)}
  catch(e){$("#out").innerHTML=`<div class="box r">Lỗi kết nối: ${esc(e)}</div>`}
  b.disabled=false;b.textContent="Xếp lịch";
};
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, PAGE, "text/html")
        else:
            self._send(404, "not found", "text/plain")

    def do_POST(self):
        if self.path != "/api/answer":
            return self._send(404, "not found", "text/plain")
        import time
        try:
            n = int(self.headers.get("Content-Length") or 0)
            text = (json.loads(self.rfile.read(n) or b"{}").get("text") or "").strip()[:2000]
        except Exception:
            return self._send(400, json.dumps({"error": "yêu cầu không hợp lệ"}), "application/json")
        t0 = time.perf_counter()
        tracing.begin("ui")
        try:
            result = answer(text)
            summary, events = tracing.end()
            out = {"output": result.get("output", "") if isinstance(result, dict) else str(result),
                   "summary": summary,
                   "notes": [e["text"] for e in events if e.get("kind") == "note"]}
        except Exception as e:  # lỗi gọi model: báo lên giao diện
            tracing.end()
            out = {"error": "%s: %s" % (type(e).__name__, e)}
        out["seconds"] = round(time.perf_counter() - t0, 1)
        self._send(200, json.dumps(out, ensure_ascii=False), "application/json")

    def log_message(self, fmt, *args):  # gọn terminal
        sys.stderr.write("[demo_ui] %s\n" % (fmt % args))


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = HTTPServer(("127.0.0.1", port), Handler)  # một luồng: trace không bị lẫn giữa hai yêu cầu
    url = "http://localhost:%d" % port
    print("Giao diện demo: %s  (Ctrl+C để dừng)" % url)
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()


if __name__ == "__main__":
    main()

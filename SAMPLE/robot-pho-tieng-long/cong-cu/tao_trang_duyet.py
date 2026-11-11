"""Trang duyệt 60 biến thể (ảnh Muse + lời + thẻ): SAMPLE/robot-pho-tieng-long/DUYET-60-BIEN-THE.html (ảnh trỏ tương đối vào anh/).
Chạy sau tao_60_bien_the.py và gen_anh_60.py:  runtime\\python.exe SAMPLE\\robot-pho-tieng-long\\cong-cu\\tao_trang_duyet.py
Trên trang: bấm vào ảnh để đánh dấu "gen lại"; nút "Chép lệnh gen lại" cho lệnh gen_anh_60.py ... --lai với các ảnh đã đánh dấu."""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "..")
OUT = os.path.join(BASE, "DUYET-60-BIEN-THE.html")


def load(fn):
    return json.load(open(os.path.join(BASE, fn), encoding="utf-8"))


def data_uri(path):
    """Nhúng ảnh vào HTML (JPEG 360 px rộng) để trang xem được ở bất kỳ đâu, không phụ thuộc đường dẫn."""
    import base64
    import io
    from PIL import Image
    im = Image.open(path).convert("RGB")
    im.thumbnail((360, 640))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=78)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def img(rel, ma):
    exists = os.path.exists(os.path.join(BASE, rel))
    if not exists:
        return f'<div class="img missing">chưa có ảnh<br>{ma}</div>'
    return f'<figure class="img" data-ma="{ma}"><img src="{data_uri(os.path.join(BASE, rel))}" alt="{ma}"><figcaption>{ma}</figcaption></figure>'


def card(v, show_imgs=True):
    e = html.escape
    hk = v["HAU_KY"]
    imgs = ""
    if show_imgs:
        nv, bg = v["refs"]["NGUOI_DAY"][0], v["refs"]["NEN_PHO"][0]
        rel = lambda p: p.split("robot-pho-tieng-long/")[1]
        imgs = f'<div class="imgs">{img(rel(nv), v["name"][:4] + "-nv")}{img(rel(bg), v["name"][:4] + "-bg")}</div>'
    lines = "".join(f"<li>{e(t['text'])}</li>" for t in v["LUOT"])
    cards = "".join(f"<tr><td>{e(c['tu'])}</td><td>{e(c['nghia'])}</td></tr>" for c in hk["the"])
    lang = hk.get("ngon_ngu", "en")
    return f"""<article class="v" id="{e(v['name'])}">
  <header><b>{e(v['name'])}</b><span class="title">{e(' / '.join(hk['tieu_de']))}</span></header>
  {imgs}
  <div class="txt" lang="{lang}">
    <p class="outfit"><b>Trang phục:</b> {e(v['TRANG_PHUC'])}</p>
    <ol>{lines}</ol>
    <table><tr><th>{e(hk['nhan_tu'])}</th><th>{e(hk['nhan_nghia'])}</th></tr>{cards}</table>
  </div>
</article>"""


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    bh, ind, br = load("BIEN-THE-20-BAI-HOC.json"), load("BIEN-THE-20-AN-DO.json"), load("BIEN-THE-20-BRAZIL.json")
    shared = f'<div class="imgs shared">{img("anh/bh/bh-nv.webp", "bh-nv")}{img("anh/bh/bh-bg.webp", "bh-bg")}</div>'
    body = f"""
<section id="bai-hoc"><h2>1 · 20 biến thể đổi bài học <small>robot + phố Texas giữ nguyên, tiếng Anh</small></h2>
<p class="note">Cả 20 biến thể dùng chung 2 ảnh dưới đây; mỗi biến thể một chủ đề 4 cụm tiếng lóng Mỹ.</p>{shared}
<div class="grid text">{''.join(card(v, False) for v in bh)}</div></section>
<section id="an-do"><h2>2 · 20 biến thể Ấn Độ <small>đổi nhân vật + bối cảnh, robot nói tiếng Hindi</small></h2>
<div class="grid">{''.join(card(v) for v in ind)}</div></section>
<section id="brazil"><h2>3 · 20 biến thể Brazil <small>đổi nhân vật + bối cảnh, robot nói tiếng Bồ Đào Nha (Brazil)</small></h2>
<div class="grid">{''.join(card(v) for v in br)}</div></section>"""
    page = f"""<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Duyệt 60 biến thể</title>
<style>
:root{{--bg:#f6f7f9;--card:#fff;--ink:#1d2433;--mute:#667085;--line:#e4e7ec;--accent:#2e75e6;--bad:#d92d20}}
@media (prefers-color-scheme:dark){{:root{{--bg:#11141a;--card:#1a1f29;--ink:#e6e9ef;--mute:#98a2b3;--line:#2a3140}}}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45 system-ui,"Segoe UI","Nirmala UI",sans-serif}}
.top{{position:sticky;top:0;z-index:5;background:var(--card);border-bottom:1px solid var(--line);padding:10px 16px;display:flex;gap:16px;align-items:center;flex-wrap:wrap}}
.top a{{color:var(--accent);text-decoration:none}} .top button{{background:var(--accent);color:#fff;border:0;border-radius:6px;padding:6px 12px;cursor:pointer}}
#count{{color:var(--mute)}} main{{padding:0 16px 40px;max-width:1500px;margin:auto}}
h2{{margin:28px 0 8px}} h2 small{{color:var(--mute);font-weight:400;font-size:14px}} .note{{color:var(--mute);margin:0 0 8px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:14px}}
.v{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px}}
.v header{{display:flex;justify-content:space-between;gap:8px;margin-bottom:8px}} .title{{color:var(--accent);font-weight:600;font-size:12px;text-align:right}}
.imgs{{display:grid;grid-template-columns:1fr 1fr;gap:6px}} .imgs.shared{{max-width:420px;margin-bottom:12px}}
.img{{margin:0;position:relative;cursor:pointer;border-radius:8px;overflow:hidden;border:3px solid transparent}}
.img img{{width:100%;aspect-ratio:9/16;object-fit:cover;display:block}}
.img figcaption{{position:absolute;left:0;bottom:0;background:#000a;color:#fff;font-size:11px;padding:2px 6px;border-top-right-radius:6px}}
.img.flag{{border-color:var(--bad)}} .img.flag::after{{content:"GEN LẠI";position:absolute;top:6px;right:6px;background:var(--bad);color:#fff;font-size:11px;font-weight:700;padding:2px 6px;border-radius:4px}}
.missing{{aspect-ratio:9/16;display:flex;align-items:center;justify-content:center;text-align:center;background:var(--line);color:var(--mute)}}
.txt ol{{margin:8px 0;padding-left:20px}} .txt li{{margin:2px 0}} .outfit{{color:var(--mute);font-size:12px;margin:8px 0 0}}
table{{width:100%;border-collapse:collapse;font-size:12px}} td,th{{border-top:1px solid var(--line);padding:3px 4px;text-align:left}} th{{color:var(--mute)}}
.lightbox{{position:fixed;inset:0;background:#000d;display:none;align-items:center;justify-content:center;z-index:9}} .lightbox img{{max-height:94vh;max-width:94vw}}
</style></head><body>
<div class="top"><b>Duyệt 60 biến thể · robot-pho-tieng-long</b>
<a href="#bai-hoc">Bài học</a><a href="#an-do">Ấn Độ</a><a href="#brazil">Brazil</a>
<span id="count"></span><button id="copy">Chép lệnh gen lại</button>
<span style="color:var(--mute)">Bấm ảnh: đánh dấu gen lại · Bấm đúp: xem to</span></div>
<main>{body}</main><div class="lightbox" id="lb"><img alt=""></div>
<script>
const KEY='duyet60';let flags=new Set();try{{flags=new Set(JSON.parse(localStorage.getItem(KEY)||'[]'))}}catch(e){{}}
const save=()=>{{try{{localStorage.setItem(KEY,JSON.stringify([...flags]))}}catch(e){{}};document.getElementById('count').textContent=flags.size+' ảnh cần gen lại'}};
document.querySelectorAll('figure.img').forEach(f=>{{const m=f.dataset.ma;if(flags.has(m))f.classList.add('flag');
 let t;f.addEventListener('click',()=>{{clearTimeout(t);t=setTimeout(()=>{{flags.has(m)?flags.delete(m):flags.add(m);f.classList.toggle('flag');save()}},220)}});
 f.addEventListener('dblclick',()=>{{clearTimeout(t);const lb=document.getElementById('lb');lb.querySelector('img').src=f.querySelector('img').src;lb.style.display='flex'}})}});
document.getElementById('lb').onclick=e=>e.currentTarget.style.display='none';
document.getElementById('copy').onclick=()=>{{const cmd='runtime\\\\python.exe SAMPLE\\\\robot-pho-tieng-long\\\\cong-cu\\\\gen_anh_60.py '+[...flags].sort().join(' ')+' --lai';
 navigator.clipboard.writeText(cmd).then(()=>alert('Đã chép:\\n'+cmd),()=>prompt('Chép lệnh:',cmd))}};save();
</script></body></html>"""
    open(OUT, "w", encoding="utf-8").write(page)
    print("Đã ghi", os.path.normpath(OUT))


if __name__ == "__main__":
    main()

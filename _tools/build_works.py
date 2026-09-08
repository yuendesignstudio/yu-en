# -*- coding: utf-8 -*-
"""
YU-EN Design Studio ｜ 作品ページと作品一覧を組み立てる

つかいかた
  1. images/works/<slug>/ に写真を入れる（hero.jpg / 01.jpg 02.jpg …）
  2. 文章を直したいときは _data/works.json を編集する
  3. このファイルを実行する:  python3 _tools/build_works.py

これだけで works/<slug>.html が作り直され、
トップと作品一覧のカードも自動で入れ替わります。
写真が無い作品は、自動で仮画像（_ph-*.svg）を使います。
"""
import os, io, json, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "_data", "works.json")
EXT  = (".jpg", ".jpeg", ".png", ".webp")

def photos(slug):
    """その作品の写真を拾う。実写が無ければ仮画像に落とす"""
    d = os.path.join(ROOT, "images", "works", slug)
    if not os.path.isdir(d): return None, []
    fs = sorted(os.listdir(d))
    hero = next((f for f in fs if f.lower().startswith("hero") and f.lower().endswith(EXT)), None)
    gal  = sorted(f for f in fs if re.fullmatch(r"\d{2}\..+", f) and f.lower().endswith(EXT))
    if not hero:
        hero = next((f for f in fs if f.startswith("_ph-hero")), None)
    if not gal:
        gal = sorted(f for f in fs if re.fullmatch(r"_ph-\d{2}\.svg", f))[:8]
    return hero, gal

def is_ph(name): return bool(name) and name.startswith("_ph-")

E = html.escape

def page(w):
    slug, t = w["slug"], w["title"]
    hero, gal = photos(slug)
    base = f"../images/works/{slug}"
    heroimg = (f'<img src="{base}/{hero}" alt="{E(t)}{"（仮画像・実写に差し替え予定）" if is_ph(hero) else ""}">'
               if hero else '<div class="ph">MAIN PHOTO</div>')
    figs = "\n".join(
        f'    <figure><img src="{base}/{g}" alt="{E(t)} {i:02d}{"（仮画像）" if is_ph(g) else ""}"></figure>'
        for i, g in enumerate(gal, 1)) or '    <figure><div class="ph">PHOTO 01</div></figure>'
    enname = f'    <p class="enname">{E(w["en"])}</p>\n' if w.get("en") else ""
    body = "\n".join(f'    <p>{E(p)}</p>' for p in w["body"])
    note = f'\n    <p class="note">{E(w["note"])}</p>' if w.get("note") else ""
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{E(t)} ｜ YU-EN Design Studio</title>
<meta name="description" content="{E(w['lead'])}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<!-- ★ 筑紫ゴシックのWebフォント（Adobe Fonts）を使う場合は、ここに kit の1行を貼ってください -->
<!-- <link rel="stylesheet" href="https://use.typekit.net/XXXXXXX.css"> -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/css/work.css">
<link rel="stylesheet" href="../assets/css/header.css">
</head>
<body>
<!-- このページは _data/works.json から自動生成されています。
     直接ここを直しても、次の書き出しで消えます。文章は works.json を編集してください。 -->

<header class="site-header">
  <div class="header-inner">
    <a href="../index.html" class="logo">
      <span class="logo-ja">YU-EN</span>
      <span class="logo-en">DESIGN STUDIO</span>
    </a>
    <div class="header-right">
    <nav class="site-nav" id="site-nav">
      <ul>
        <li><a href="../index.html">Works</a></li>
        <li><a href="../studio.html">About</a></li>
        <li><a href="../../karan-products/index.html">Shop</a></li>
        <li><a href="../contact.html">Contact</a></li>
      </ul>
    </nav>
    <div class="lang-switch">
      <span class="lang-btn lang-btn--active">JP</span>
      <span class="lang-sep">/</span>
      <a href="../en/index.html" class="lang-btn">EN</a>
    </div>
    </div>
  </div>
</header>

<div class="work-hero">
  {heroimg}
</div>

<div class="wrap">
  <div class="work-head">
    <p class="cat">{E(w['cat'])}</p>
    <h1>{E(t)}</h1>
{enname}    <p class="meta">{E(w['meta'])}</p>
  </div>

  <div class="work-desc">
{body}{note}
  </div>

  <div class="gallery">
{figs}
  </div>
</div>

<div class="work-foot"><a href="../index.html#works">← 作品一覧へ戻る</a></div>
<footer class="site">© 2026 YU-EN Design Studio ／ 湯縁</footer>
</body>
</html>
"""

def card(w, prefix=""):
    slug = w["slug"]
    hero, gal = photos(slug)
    img = hero or (gal[0] if gal else None)
    ename = f'　<span class="enname">{E(w["en"])}</span>' if w.get("en") else ""
    src = f'{prefix}images/works/{slug}/{img}' if img else ""
    tag = (f'<img src="{src}" alt="{E(w["title"])}{"（仮画像）" if is_ph(img) else ""}">'
           if img else '<div class="tone"></div>')
    return f"""      <a class="item" href="{prefix}works/{slug}.html">
        <div class="plate">{tag}</div>
        <div class="names">
          <h3>{E(w[chr(39)+chr(39)]) if False else E(w["title"])}{ename}</h3>
          <p>{E(w['lead'])}</p>
        </div>
        <span class="st">{E(w['status'])}</span>
      </a>"""

def card_grid(w, prefix="", lang="ja"):
    """works.html（大きなカードの一覧）用"""
    slug = w["slug"]
    hero, gal = photos(slug)
    img = hero or (gal[0] if gal else None)
    title = w["title"] if lang == "ja" else w["en"]
    src = f'{prefix}images/works/{slug}/{img}' if img else ""
    inner = (f'<img src="{src}" alt="{E(title)}{"（仮画像）" if is_ph(img) else ""}" loading="lazy" />'
             if img else "")
    more = "詳しく見る →" if lang == "ja" else "View project →"
    return f"""        <a href="{prefix}works/{slug}.html" class="work-card">
          <div class="work-img">
            {inner}
          </div>
          <div class="work-steam"><span></span><span></span><span></span><span></span></div>
          <div class="work-overlay">
            <div class="work-overlay-inner">
              <span class="work-tag">{E(w['cat'].split('・')[0].strip())}</span>
              <h3 class="work-title">{E(title)}</h3>
              <p class="work-meta">{E(w['meta'])}</p>
              <span class="work-link">{more}</span>
            </div>
          </div>
        </a>"""

def swap(path, block, mark="WORKS"):
    """<!-- WORKS:start --> 〜 <!-- WORKS:end --> の間を入れ替える"""
    p = os.path.join(ROOT, path)
    s = io.open(p, encoding="utf-8").read()
    pat = re.compile(f"(<!-- {mark}:start -->).*?(<!-- {mark}:end -->)", re.S)
    if not pat.search(s): return False
    io.open(p, "w", encoding="utf-8").write(pat.sub(lambda m: m.group(1)+"\n"+block+"\n      "+m.group(2), s))
    return True

if __name__ == "__main__":
    d = json.load(io.open(DATA, encoding="utf-8"))
    ws = d["works"]
    for w in ws:
        out = os.path.join(ROOT, "works", w["slug"] + ".html")
        io.open(out, "w", encoding="utf-8").write(page(w))
        hero, gal = photos(w["slug"])
        kind = "仮画像" if is_ph(hero) else "実写"
        print(f"  works/{w['slug']}.html".ljust(38) + f"{kind} ／ ギャラリー {len(gal)}枚")
    for path, pre, fn, lang in [("studio.html", "", card, "ja"),
                                ("index.html", "", card_grid, "ja"),
                                ("en/index.html", "../", card_grid, "en")]:
        block = "\n".join(fn(w, pre, lang) if fn is card_grid else fn(w, pre) for w in ws)
        print(("  " + path).ljust(38) + ("一覧を更新" if swap(path, block) else "※ 目印なし・手つかず"))
    print(f"\n作品 {len(ws)} 件を書き出しました。")

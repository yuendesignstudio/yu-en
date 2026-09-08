# -*- coding: utf-8 -*-
"""
Karan Products ｜ 作品一覧（items.html）を組み立てる

つかいかた
  1. _data/items.json に1件ずつ足す（上から順に No.01, No.02 … と番号が付きます）
  2. images/items/<番号2桁>/ に写真を入れる（01.jpg 02.jpg …）
  3. python3 _tools/build_items.py
"""
import os, io, json, re, html as H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXT  = (".jpg", ".jpeg", ".png", ".webp")
E    = H.escape

def photos(no):
    d = os.path.join(ROOT, "images", "items", f"{no:02d}")
    if not os.path.isdir(d): return []
    return sorted(f for f in os.listdir(d) if f.lower().endswith(EXT))

def card(it, no):
    ph = photos(no)
    thumb = (f'<img src="images/items/{no:02d}/{ph[0]}" alt="{E(it["name"])}" loading="lazy">'
             if ph else '<span>PHOTO</span>')
    note = f'<p class="product-note">{E(it.get("note",""))}</p>' if it.get("note") else ""
    return f"""      <div class="product-card" data-cat="{E(it['cat'])}">
        <div class="product-thumb">{thumb}</div>
        <div class="product-meta">
          <p class="item-no">No.{no:02d}</p>
          <p class="product-name">{E(it['name'])}</p>
          <p class="product-desc">{E(it.get('desc',''))}</p>
          {note}
          <a href="contact.html" class="btn-order">この一点について相談する →</a>
        </div>
      </div>"""

if __name__ == "__main__":
    d = json.load(io.open(os.path.join(ROOT,"_data","items.json"), encoding="utf-8"))
    items, cats = d["items"], d["categories"]

    cards = "\n".join(card(it, i) for i, it in enumerate(items, 1)) or \
            '      <div class="empty-state" style="grid-column:1/-1">準備中です。</div>'
    btns = '\n'.join(
        [f'      <button class="filter-btn active" data-cat="">すべて</button>'] +
        [f'      <button class="filter-btn" data-cat="{E(c)}">{E(c)}</button>' for c in cats])

    p = os.path.join(ROOT, "items.html")
    s = io.open(p, encoding="utf-8").read()
    s = re.sub(r'(<div class="filter-row">).*?(\n\s*</div>)',
               lambda m: m.group(1)+"\n"+btns+m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'<p class="item-count"[^>]*>.*?</p>',
               f'<p class="item-count" style="margin-top: 16px;">{len(items)} 件</p>', s, count=1, flags=re.S)
    s = re.sub(r'(<div class="product-grid">).*?(\n\s*</div>)',
               lambda m: m.group(1)+"\n"+cards+m.group(2), s, count=1, flags=re.S)
    io.open(p, "w", encoding="utf-8").write(s)
    print(f"items.html を書き出しました（{len(items)} 件）")
    for i, it in enumerate(items, 1):
        print(f"  No.{i:02d}  {it['name']}  写真{len(photos(i))}枚")

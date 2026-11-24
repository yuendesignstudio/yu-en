# 作品ページの英語版（en/works/*.html）を、日本語版（works/*.html）から作る。2026-11-24
# 使い方: python3 tools/mk_en_works.py <サイトの根>   （works/ と en/ のある所）
# ・日本語ページの枠（ヘッダー・写真の並び）をそのまま使い、文とリンクだけを英語用に替える
# ・日本語ページの EN ボタンと、en/index.html のカードのリンクも英語版へ向ける
# ・build_works.py は英語版を作らない。日本語の本文を変えたら、下の EN も手で直してこれを流す
import re, sys, os, html
root = sys.argv[1]
SITE = "YU-EN DESIGN STUDIO"
EN = {
 "ekoda-house": dict(h1="Room above Sento", sub="銭湯上の住戸", cat="Architecture · Own home",
   meta="Self-built renovation / Nerima, Tokyo / In progress",
   desc="A room above the bathhouse, rebuilt little by little with my own hands. An experimental home the designer lives in while tending it day by day. The starting point of everything.",
   ps=["I am rebuilding, little by little and with my own hands, a room above my family&#39;s sento (public bathhouse). The designer becomes the resident: cleaning, repainting, tending the room season by season. The more care it is given, the more the room slowly becomes my own place. That process itself is the starting point of YU-EN DESIGN STUDIO&#39;s &ldquo;architecture to tend.&rdquo;"],
   note="A life lived alongside water and wood, and the presence of steam. Without hurrying toward completion, I keep a record of it as an experimental home that I go on working on while living in it."),
 "inoue-house": dict(h1="Inoue House", sub="井上さんの家", cat="Architecture · House renovation",
   meta="House renovation / In progress",
   desc="A renovation for taking over a home, working on it, and continuing to live in it.", ps=[], note=None),
 "itsukushima-folly": dict(h1="Folly at Itsukushima", sub="厳島神社のフォリー", cat="Architecture · Folly",
   meta="Folly / Exhibited for one day",
   desc="A folly exhibited for a single day during the repair of the Great Torii. Listening to the waves inside earthen walls made with oyster shells.",
   ps=["A folly planned to be exhibited for a single day while the Great Torii of Itsukushima Shrine was under repair. It was built with earthen walls made from oyster shells, a local specialty, at a spot with a side view of the shrine.",
       "The interior is a space for listening to the sound of the waves. It uses the same kind of curve as a parabolic dish, and when you sit on the stone seat inside, you are drawn into that sound."], note=None),
 "karan": dict(h1="Karan Products", sub="Products from bathhouse salvage", cat="Product · Brand",
   meta="A product brand using salvage from sento bathhouses / In progress",
   desc="Timber, tiles, and fittings from sento that are being demolished, given new life as everyday tools. The layered time held in bathhouse materials, conveyed in a new form.",
   ps=["A brand that takes in timber, tiles, karan (bath taps), mirrors, and other pieces from sento that are being torn down, and remakes them into one-of-a-kind furniture and tools. The materials already carry decades of traces of people&#39;s hands, and keeping those traces rather than erasing them is placed at the center of the design.",
       "Finishes are chosen to gain character as they are cared for, and each piece is handed over with notes on how to repair it. These are tools not to be bought and done with, but to be kept for a long time while being tended."],
   note="One-of-a-kind furniture and tools, as well as workshops, are now under way."),
 "kide": dict(h1="KIDE", sub="Outdoor Timber Stage, Finland", cat="Architecture · Finland",
   meta="Kuhmo, Finland / 2024 / 74 m&sup2; / Aalto University Wood Program",
   desc="An outdoor timber stage in Kuhmo, Finland. Designed and built in the Aalto University Wood Program. Architizer A+Awards Popular Winner; featured on ArchDaily.",
   ps=["An outdoor timber stage standing in the forest of Kuhmo, Finland. As a member of the Aalto University Wood Program, I worked on it from design through construction. Using local wood, in an environment of snow and light, it aims to be a place for gathering, and for returning once more to the forest.",
       "The timber structure, which recalls a crystal (kide), changes color over time in Finland&#39;s harsh climate and lives on while being cared for. It is a project in which the cycle of wood as a material connects directly with the thinking of &ldquo;water and wood&rdquo; that YU-EN DESIGN STUDIO values."],
   note="Architizer A+Awards &mdash; Popular Winner / Cultural Pavilions (2025). Featured on ArchDaily (May 2025) and architecturephoto.net (September 2025)."),
 "masters-lodge": dict(h1="Master&#39;s Lodge", sub=None, cat="Architecture · Proposal",
   meta="Self-initiated project / Cambridge",
   desc="A proposal for a building for the &ldquo;Master,&rdquo; the head of a college at the University of Cambridge. The Master&#39;s life and the students&#39; daily life intertwine like a double helix.",
   ps=["A proposal for a building for the head of a college at the University of Cambridge, who is called the &ldquo;Master.&rdquo; This space, usually little used, is made into a place students can use every day, and planned so that it intertwines with the Master&#39;s life like a double helix.",
       "The central garden is a space where plays can be performed. In the outdoor squares of Cambridge, Shakespeare&#39;s plays are staged. As in <em>A Midsummer Night&#39;s Dream</em>, where ranks are turned upside down, the relationship between the Master and the students is turned upside down, by day and by night. The project asks whether such a relationship could be made."],
   note=None),
 "recycle-station": dict(h1="Recycle Station", sub=None, cat="Competition · Design competition",
   meta="11th Hulic Student Idea Competition / One of 10 selected entries",
   desc="Reusing the waste of everyday life and turning it into space. A student idea competition entry for a site in Shinjuku.",
   ps=["A proposal entered in the 11th Hulic Student Idea Competition by a team of four. The theme was &ldquo;Izanau Kenchiku&rdquo; (architecture that invites), and the site was in Shinjuku.",
       "It proposes reusing the waste that comes out of everyday life and turning it into space."], note=None),
 "rooftop-hut": dict(h1="Rooftop Hut", sub=None, cat="Architecture · Small building",
   meta="Experimental hut for environmental architecture / Tokyo",
   desc="An experimental hut with water bags inside, built on the roof of an apartment building.",
   ps=["An experimental hut for environmental architecture, built on the roof of an apartment building in Tokyo. Inside the hut are water bags. The water bags serve not only as insulation; using the convection of the water, they are also meant to keep the interior cool even in summer.",
       "It is also a place that supports activities on the rooftop."], note=None),
 "wooden-bridge-reconnect": dict(h1="Wooden Bridge Reconnect", sub=None, cat="Competition · Design competition",
   meta="Rekishiteki Kukan Saihen Competition / One of 30 selected entries",
   desc="A proposal for a skin that connects Azuma Bridge in Asakusa to the future once more.",
   ps=["I designed a skin for connecting the historic Azuma Bridge in Asakusa to the future once more. The proposal was submitted to the Rekishiteki Kukan Saihen Competition (a competition for reorganizing historic space) and selected as one of 30 entries."], note=None),
}
HEADER = '''<header class="site-header">
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
        <li><a href="../../karan-products/en/index.html">Shop</a></li>
        <li><a href="../contact.html">Contact</a></li>
      </ul>
    </nav>
    <div class="lang-switch">
      <a href="../../works/%s.html" class="lang-btn">JP</a>
      <span class="lang-sep">/</span>
      <span class="lang-btn lang-btn--active">EN</span>
    </div>
    </div>
  </div>
</header>'''
def one(pat, t, flags=re.S):
    m = re.search(pat, t, flags); assert m, pat; return m
enidx = open(os.path.join(root, 'en/index.html'), encoding='utf-8').read()
foot = one(r'<footer class="yfoot">.*?</footer>', enidx).group(0)
assert foot.count('<a href="index.html">') == 1 and foot.count('"../karan-products/en/index.html"') == 1 and '../../karan-products' not in foot
foot = foot.replace('<a href="index.html">', '<a href="../index.html">').replace('"../karan-products/en/index.html"', '"../../karan-products/en/index.html"')   # en/works から見た道
os.makedirs(os.path.join(root, 'en/works'), exist_ok=True)
for slug, e in EN.items():
    jp_path = os.path.join(root, 'works', slug + '.html')
    t = open(jp_path, encoding='utf-8').read()
    # 日本語ページ：EN ボタンを英語版へ
    a, b = '<a href="../en/index.html" class="lang-btn">EN</a>', '<a href="../en/works/%s.html" class="lang-btn">EN</a>' % slug
    if a in t:
        assert t.count(a) == 1; t = t.replace(a, b); open(jp_path, 'w', encoding='utf-8').write(t)
    assert t.count(b) == 1
    jp_h1 = one(r'<h1>(.*?)</h1>', t).group(1)
    title = e['h1'] + ' | ' + SITE
    s = t.replace('<html lang="ja">', '<html lang="en">')
    s = re.sub(r'<title>.*?</title>', '<title>%s</title>' % title, s, count=1)
    s = re.sub(r'(<meta name="description" content=").*?(">)', lambda m: m.group(1) + e['desc'] + m.group(2), s, count=1)
    s = re.sub(r'(<meta property="og:site_name" content=").*?(">)', r'\g<1>%s\g<2>' % SITE, s, count=1)
    s = re.sub(r'(<meta property="og:title" content=").*?(">)', lambda m: m.group(1) + title + m.group(2), s, count=1)
    s = re.sub(r'<!-- このページは.*?-->\n', '<!-- 英語版。日本語の works/%s.html をもとに _tools/mk_en_works.py で作る（直接は直さない） -->\n' % slug, s, count=1, flags=re.S)
    s = re.sub(r'<!-- ★ 筑紫ゴシック.*?-->\n<!-- <link rel="stylesheet" href="https://use.typekit.net/XXXXXXX.css"> -->\n', '', s, count=1, flags=re.S)
    s = re.sub(r'<header class="site-header">.*?</header>', lambda m: HEADER % slug, s, count=1, flags=re.S)
    if '<footer class="yfoot">' in s:
        s = re.sub(r'<footer class="yfoot">.*?</footer>', lambda m: foot, s, count=1, flags=re.S)
    else:                                                          # コンペの 3 ページは 1 行のフッター
        n0 = s.count('<footer class="site">'); assert n0 == 1, slug
        s = re.sub(r'<footer class="site">.*?</footer>', '<footer class="site">&copy; 2026 YU-EN DESIGN STUDIO</footer>', s, count=1, flags=re.S)
    head = ['    <p class="cat">%s</p>' % e['cat'], '    <h1>%s</h1>' % e['h1']]
    if e['sub']: head.append('    <p class="enname"%s>%s</p>' % (' lang="ja"' if re.search(r'[^\x00-\x7f]', e['sub']) else '', e['sub']))
    head.append('    <p class="meta">%s</p>' % e['meta'])
    s = re.sub(r'<div class="work-head">.*?</div>', lambda m: '<div class="work-head">\n' + '\n'.join(head) + '\n  </div>', s, count=1, flags=re.S)
    body = ['    <p>%s</p>' % p for p in e['ps']] + (['    <p class="note">%s</p>' % e['note']] if e['note'] else [])
    n_jp = len(re.findall(r'<p[ >]', one(r'<div class="work-desc">(.*?)</div>', t).group(1)))
    assert n_jp == len(body), (slug, n_jp, len(body))          # 段落の数は日本語版と同じ
    s = re.sub(r'<div class="work-desc">.*?</div>', lambda m: '<div class="work-desc">\n' + ''.join(x + '\n' for x in body) + '  </div>', s, count=1, flags=re.S)
    # 画像の alt：作品名を英語名に、（仮画像…）を英語に
    def alt(m):
        v = m.group(1).replace(jp_h1, e['h1']).replace('（仮画像・実写に差し替え予定）', ' (placeholder image)').replace('（仮画像）', ' (placeholder image)')
        return 'alt="%s"' % v
    s = re.sub(r'alt="(.*?)"', alt, s)
    s = s.replace('<a href="../index.html#works">← 作品一覧へ戻る</a>', '<a href="../index.html">← Back to works</a>')
    # 道：css と画像は 1 段深くなる
    s = s.replace('href="../assets/', 'href="../../assets/').replace('src="../images/', 'src="../../images/')
    body_only = s[s.find('<body'):]
    left = re.findall(r'[぀-ヿ一-鿿]+', re.sub(r'<p class="enname" lang="ja">.*?</p>|<!--.*?-->', '', body_only, flags=re.S))
    assert not left, (slug, left)                                  # 日本語の残りが無いこと（併記した作品名を除く）
    assert 'ユエンデザインスタジオ' not in s
    open(os.path.join(root, 'en/works', slug + '.html'), 'w', encoding='utf-8').write(s)
    # 英語のトップのカード
    a, b = 'href="../works/%s.html"' % slug, 'href="works/%s.html"' % slug
    if a in enidx: assert enidx.count(a) == 1; enidx = enidx.replace(a, b)
    assert enidx.count(b) == 1, slug
    print('ok', slug, len(s))
open(os.path.join(root, 'en/index.html'), 'w', encoding='utf-8').write(enidx)

# ── 英語の About（en/studio.html）の作品の一覧：日本語の studio.html の並び・写真に合わせて作り直す ──
ST = {"進行中 ・ 自邸": "In progress · Own home", "Architecture ・ 2024": "Architecture · 2024", "進行中 ・ 住宅": "In progress · House",
      "実験小屋": "Experimental hut", "フォリー": "Folly", "進行中 ・ プロダクト": "In progress · Product",
      "自主計画": "Self-initiated project", "Competition": "Competition"}
jp = open(os.path.join(root, 'studio.html'), encoding='utf-8').read()
items = re.findall(r'<a class="item" href="works/([a-z\-]+)\.html">\s*<div class="plate"><img src="([^"]+)" alt="[^"]*"></div>.*?<span class="st">(.*?)</span>\s*</a>', jp, re.S)
assert len(items) == len(EN), len(items)
rows = []
for slug, img, st in items:
    e = EN[slug]; sub = e['sub']; ja = bool(sub and re.search(r'[^\x00-\x7f]', sub))   # 副題（日本語の題は lang="ja"）
    rows.append('      <a class="item" href="works/%s.html">\n        <div class="plate"><img src="../%s" alt="%s"></div>\n        <div class="names">\n          <h3>%s%s</h3>\n          <p>%s</p>\n        </div>\n        <span class="st">%s</span>\n      </a>\n'
                % (slug, img, e['h1'], e['h1'], ('　<span class="enname"%s>%s</span>' % (' lang="ja"' if ja else '', sub)) if sub else '', e['desc'], ST[st]))
p = os.path.join(root, 'en/studio.html'); s = open(p, encoding='utf-8').read()
new = '<div class="list">\n      <!-- WORKS-EN:start（_tools/mk_en_works.py が作る。直接は直さない） -->\n' + ''.join(rows) + '      <!-- WORKS-EN:end -->\n    </div>'
m = one(r'(<section class="works" id="works">.*?)<div class="list">.*?</a>\s*(?:<!-- WORKS-EN:end -->\s*)?</div>(\s*</div>\s*</section>)', s)
s = s[:m.start()] + m.group(1) + new + m.group(2) + s[m.end():]
open(p, 'w', encoding='utf-8').write(s); print('ok en/studio.html list', len(rows))

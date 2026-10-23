#!/usr/bin/env python3
"""Build the static blog from blog/posts/*.md.

Usage:  python3 tools/build_blog.py            # build published posts into blog/
        python3 tools/build_blog.py --drafts   # include drafts (local preview only)

A post is a Markdown file with front matter (title, date, summary, cover, tags, draft).
Posts with "draft: true" are skipped unless --drafts is given.
No dependencies beyond the Python standard library.
"""
import html, re, sys, shutil
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
BLOG = ROOT / "blog"
SITE = "https://huzaifa18.github.io"
INCLUDE_DRAFTS = "--drafts" in sys.argv

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="color-scheme" content="light dark">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{ogtype}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="alternate" type="application/rss+xml" title="Huzaifa Asif, blog" href="{site}/blog/feed.xml">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%2311202D'/%3E%3Crect x='8' y='29' width='14' height='6' fill='%23F2B01E'/%3E%3Crect x='28' y='29' width='14' height='6' fill='%23F2B01E'/%3E%3Crect x='48' y='29' width='8' height='6' fill='%23F2B01E'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&family=Bricolage+Grotesque:opsz,wght@12..96,600..800&display=swap" rel="stylesheet">
<script>
(function(){var r=document.documentElement;try{var s=JSON.parse(localStorage.getItem('hz-display')||'null');if(s){if(s.text)r.dataset.text=s.text;if(s.contrast)r.dataset.contrast=s.contrast;if(s.motion)r.dataset.motion=s.motion;if(s.theme&&s.theme!=='auto')r.dataset.theme=s.theme}}catch(e){}})();
</script>
<link rel="stylesheet" href="{css}">
{extra}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="aurora" aria-hidden="true"><span></span><span></span><span></span></div>
<header class="wrap site-header">
  <a class="wordmark" href="{site}/">Huzaifa Asif</a>
  <nav class="nav" aria-label="Main"><ul>
    <li><a href="{site}/">Home</a></li>
    <li><a href="{site}/blog/"{cur}>Blog</a></li>
    <li><a href="https://github.com/huzaifa18">GitHub</a></li>
    <li><a href="https://www.linkedin.com/in/huzaifa-asif-007">LinkedIn</a></li>
  </ul></nav>
</header>
"""
FOOT = """<footer class="wrap site-footer"><p>Huzaifa Asif, Nuremberg, Germany. <a href="{site}/blog/feed.xml">RSS feed</a></p></footer>
</body>
</html>
"""

def fill(tpl, **kw):
    for k, v in kw.items():
        tpl = tpl.replace("{%s}" % k, str(v))
    return tpl

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![*\w])\*([^*]+)\*(?!\w)", r"<em>\1</em>", t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+|/[^)\s]*)\)", r'<a href="\2">\1</a>', t)
    return t

def md(text):
    out, para, lst, code, fence = [], [], None, [], False
    def flush():
        nonlocal para, lst
        if para: out.append("<p>%s</p>" % inline(" ".join(para))); para = []
        if lst: out.append("<%s>%s</%s>" % (lst[0], "".join("<li>%s</li>" % inline(i) for i in lst[1]), lst[0])); lst = None
    for line in text.split("\n"):
        if line.startswith("```"):
            if fence: out.append("<pre><code>%s</code></pre>" % html.escape("\n".join(code))); code = []; fence = False
            else: flush(); fence = True
            continue
        if fence: code.append(line); continue
        s = line.strip()
        m = re.match(r"(#{2,3}) (.+)", s)
        if not s: flush()
        elif m: flush(); n = len(m.group(1)); out.append("<h%d>%s</h%d>" % (n, inline(m.group(2)), n))
        elif s.startswith("> "): flush(); out.append("<blockquote><p>%s</p></blockquote>" % inline(s[2:]))
        elif re.match(r"[-*] ", s):
            if not lst or lst[0] != "ul": flush(); lst = ("ul", [])
            lst[1].append(s[2:])
        elif re.match(r"\d+\. ", s):
            if not lst or lst[0] != "ol": flush(); lst = ("ol", [])
            lst[1].append(re.sub(r"^\d+\. ", "", s))
        else:
            if lst: flush()
            para.append(s)
    flush()
    return "\n".join(out)

def parse(path):
    raw = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", raw, re.S)
    meta, body = {}, raw
    if m:
        for l in m.group(1).split("\n"):
            if ":" in l: k, v = l.split(":", 1); meta[k.strip()] = v.strip()
        body = m.group(2)
    meta["draft"] = meta.get("draft", "false").lower() == "true"
    meta["slug"] = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)
    meta["body"] = body.strip()
    return meta

def fmt(d): return datetime.strptime(d, "%Y-%m-%d").strftime("%B %-d, %Y")

def main():
    posts = [parse(p) for p in sorted((BLOG / "posts").glob("*.md"))]
    posts = [p for p in posts if INCLUDE_DRAFTS or not p["draft"]]
    posts.sort(key=lambda p: p["date"], reverse=True)
    for d in BLOG.iterdir():  # remove stale generated post folders
        if d.is_dir() and d.name not in ("posts", "images"): shutil.rmtree(d)
    default_img = SITE + "/blog/images/blog-header.jpg"

    for p in posts:
        url = f"{SITE}/blog/{p['slug']}/"
        img = f"{SITE}/blog/images/{p['cover']}" if p.get("cover") else default_img
        draft = '<meta name="robots" content="noindex">\n' if p["draft"] else ""
        page = fill(HEAD, title=html.escape(p["title"]) + " | Huzaifa Asif", desc=html.escape(p.get("summary", "")), url=url, image=img, site=SITE, css="../blog.css", ogtype="article", cur="", extra=draft)
        tags = " · ".join(t.strip() for t in p.get("tags", "").split(",") if t.strip())
        page += f"""<main id="main" class="wrap page"><article class="article">
<a class="backlink" href="../">← All posts</a>
<h1>{html.escape(p['title'])}{' (draft)' if p['draft'] else ''}</h1>
<p class="meta"><time datetime="{p['date']}">{fmt(p['date'])}</time>{(' · ' + html.escape(tags)) if tags else ''}</p>
{f'<img class="cover" src="../images/{p["cover"]}" alt="" width="1200" height="630">' if p.get('cover') else ''}
{md(p['body'])}
<div class="post-end"><a class="btn" href="../">More posts</a><a href="{SITE}/">Back to portfolio</a></div>
</article></main>
""" + fill(FOOT, site=SITE)
        (BLOG / p["slug"]).mkdir(exist_ok=True)
        (BLOG / p["slug"] / "index.html").write_text(page, encoding="utf-8")

    cards = "".join(f"""<li><article class="post-card"><img src="images/{p['cover']}" alt="" width="1200" height="630" loading="lazy"><div class="post-card__body"><h2><a href="{p['slug']}/">{html.escape(p['title'])}</a></h2><p class="meta">{fmt(p['date'])}</p><p>{html.escape(p.get('summary',''))}</p></div></article></li>""" for p in posts if p.get("cover"))
    body = f'<ul class="posts">{cards}</ul>' if posts else '<p class="empty">The first posts are on their way. Check back soon, or follow along on <a href="https://github.com/huzaifa18">GitHub</a>.</p>'
    page = fill(HEAD, title="Blog | Huzaifa Asif", desc="Notes from a mobile developer on Android, Kotlin, Flutter and on-device AI.", url=f"{SITE}/blog/", image=default_img, site=SITE, css="blog.css", ogtype="website", cur=' aria-current="page"', extra="")
    page += f"""<main id="main" class="wrap page">
<h1>Blog</h1>
<p class="lead">Notes on Android, Kotlin, Flutter and on-device AI, written while building real apps.</p>
{body}
</main>
""" + fill(FOOT, site=SITE)
    (BLOG / "index.html").write_text(page, encoding="utf-8")

    items = "".join(f"<item><title>{html.escape(p['title'])}</title><link>{SITE}/blog/{p['slug']}/</link><guid>{SITE}/blog/{p['slug']}/</guid><pubDate>{datetime.strptime(p['date'],'%Y-%m-%d').strftime('%a, %d %b %Y 08:00:00 +0000')}</pubDate><description>{html.escape(p.get('summary',''))}</description></item>" for p in posts)
    (BLOG / "feed.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Huzaifa Asif, blog</title><link>{SITE}/blog/</link><description>Notes on Android, Kotlin, Flutter and on-device AI.</description>{items}</channel></rss>', encoding="utf-8")
    print(f"Built {len(posts)} post(s){' (including drafts)' if INCLUDE_DRAFTS else ''}.")

main()

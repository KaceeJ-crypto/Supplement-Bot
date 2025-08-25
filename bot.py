#!/usr/bin/env python3
import os, re, time, json, urllib.parse, pathlib, datetime
import feedparser, requests, yaml
from bs4 import BeautifulSoup
from readability import Document

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "site" / "_posts"
DB  = ROOT / "data.json"

def load_cfg():
    with open(ROOT/"sources.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def normalize_url(u: str):
    url = urllib.parse.urlsplit(u)
    qs = urllib.parse.parse_qs(url.query)
    clean_qs = {k:v for k,v in qs.items() if not k.lower().startswith("utm")}
    return urllib.parse.urlunsplit((url.scheme, url.netloc, url.path,
                                    urllib.parse.urlencode(clean_qs, doseq=True),
                                    url.fragment))

def add_affiliate(u: str, aff_map: dict):
    url = urllib.parse.urlsplit(u)
    dom = url.netloc.lower()
    base = ".".join(dom.split(".")[-2:])
    tag = None
    for k,v in aff_map.items():
        if k in dom or k == base:
            tag = v
            break
    if not tag: return u
    qs = urllib.parse.parse_qs(url.query)
    for chunk in tag.split("&"):
        if "=" in chunk:
            k, v = chunk.split("=", 1)
            qs[k] = [v]
    new_qs = urllib.parse.urlencode(qs, doseq=True)
    return urllib.parse.urlunsplit((url.scheme, url.netloc, url.path, new_qs, url.fragment))

def fetch_readable(url: str):
    try:
        html = requests.get(url, timeout=15).text
        doc = Document(html)
        article_html = doc.summary()
        soup = BeautifulSoup(article_html, "html.parser")
        text = soup.get_text("\n", strip=True)
        words = text.split()
        excerpt = " ".join(words[: min(120, max(50, len(words)))])
        return excerpt
    except Exception:
        return ""

def slugify(s: str):
    s = re.sub(r"[^\w\s-]", "", s.lower()).strip()
    s = re.sub(r"[\s_-]+", "-", s)
    return s[:80]

def load_db():
    if DB.exists():
        return json.loads(DB.read_text(encoding="utf-8"))
    return {"seen": {}}

def save_db(db):
    DB.write_text(json.dumps(db, indent=2), encoding="utf-8")

def matches_keywords(title, summary, keywords):
    hay = f"{title}\n{summary}".lower()
    return any(k.lower() in hay for k in keywords)

def main():
    cfg = load_cfg()
    db = load_db()
    OUT.mkdir(parents=True, exist_ok=True)

    items = []
    for feed in cfg["feeds"]:
        parsed = feedparser.parse(feed)
        for e in parsed.entries:
            url = normalize_url(e.link)
            if db["seen"].get(url): 
                continue
            title = e.title
            summary = BeautifulSoup(e.get("summary",""), "html.parser").get_text(" ", strip=True)
            if not matches_keywords(title, summary, cfg["keywords"]):
                continue
            excerpt = fetch_readable(url) or summary
            aff_url = add_affiliate(url, cfg.get("domain_affiliates", {}))
            items.append({"title": title, "url": aff_url, "excerpt": excerpt})
            db["seen"][url] = int(time.time())

    if not items:
        print("No new supplement items today.")
        save_db(db)
        return

    today = datetime.date.today().strftime("%Y-%m-%d")
    title = f"{today} • {len(items)} New Supplement Finds"
    slug = slugify(title)
    path = OUT / f"{today}-{slug}.md"
    lines = [
        "---",
        f'title: "{title}"',
        "layout: post",
        'tags: ["supplements", "roundup"]',
        "---",
        "",
        "> This post may contain affiliate links. We may earn from qualifying purchases at no extra cost to you.",
        "",
    ]
    for it in items:
        lines += [f"### [{it['title']}]({it['url']})", "", it["excerpt"], "", "---", ""]
    path.write_text("\n".join(lines), encoding="utf-8")

    # Optional Telegram cross-post
    tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
    tg_chat  = os.getenv("TELEGRAM_CHAT_ID")
    if tg_token and tg_chat:
        msg = title + "\n\n" + "\n".join(f"• {i['title']} — {i['url']}" for i in items[:12])
        requests.get(f"https://api.telegram.org/bot{tg_token}/sendMessage",
                     params={"chat_id": tg_chat, "text": msg, "disable_web_page_preview": True})

    save_db(db)
    print(f"Wrote: {path}")

if __name__ == "__main__":
    main()
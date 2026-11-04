"""Build /blog-kb/<lang>.json — the chatbot's knowledge base made from every blog article.

Run automatically at the end of _blog/build.py (so every new article is in the bot the same day).
Each entry: t title, u url, p place, k keywords, f facts, q faq, s sections [[heading, text], ...].
"""
import json, pathlib, re
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[2]
B = ROOT / "_blog"
OUT = ROOT / "blog-kb"


class Sec(HTMLParser):
    BLOCK = {"p", "li", "h3", "blockquote"}

    def __init__(self, first):
        super().__init__(convert_charrefs=True)
        self.secs = [[first, []]]
        self.buf = None
        self.tag = None

    def handle_starttag(self, tag, a):
        if tag == "h2":
            self.flush(); self.buf = []; self.tag = "h2"
        elif tag in self.BLOCK and self.tag is None:
            self.buf = []; self.tag = tag

    def handle_endtag(self, tag):
        if tag == self.tag:
            t = re.sub(r"\s+", " ", "".join(self.buf)).strip()
            if tag == "h2":
                self.secs.append([t, []])
            elif t:
                if tag == "li": t = "• " + t
                if tag == "h3": t = t.rstrip(":：") + ":"
                self.secs[-1][1].append(t)
            self.buf = None; self.tag = None

    def handle_data(self, d):
        if self.buf is not None: self.buf.append(d)

    def flush(self):
        if self.buf is not None and self.tag:
            self.handle_endtag(self.tag)


def run(langs=None):
    OUT.mkdir(exist_ok=True)
    n = {}
    for d in sorted(B.iterdir()):
        f = d / "posts.json"
        if not f.exists(): continue
        l = d.name
        if langs and l not in langs: continue
        posts = sorted(json.loads(f.read_text()), key=lambda p: p["date"])
        kb = []
        for p in posts:
            body = (d / "posts" / f'{p["slug"]}.html').read_text()
            h = Sec(p.get("h1") or p["title"]); h.feed(body); h.close(); h.flush()
            secs = [[t, "\n".join(x)] for t, x in h.secs if x]
            kb.append({
                "t": p["title"], "h": p.get("h1", ""),
                "u": ("/blog/" if l == "ar" else f"/{l}/blog/") + p["slug"] + "/",
                "p": p.get("place", ""), "k": p.get("keywords", ""), "c": p.get("category", ""),
                "f": p.get("facts", []), "q": p.get("faq", []), "s": secs,
            })
        (OUT / f"{l}.json").write_text(json.dumps(kb, ensure_ascii=False, separators=(",", ":")))
        n[l] = len(kb)
    print("Chatbot blog KB:", ", ".join(f"{k}={v}" for k, v in n.items()))


if __name__ == "__main__":
    run()

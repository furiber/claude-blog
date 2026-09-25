#!/usr/bin/env python3
"""Crawl the 7 in-scope AA driving-school URLs.

Static HTML (requests-style via urllib) + Playwright mobile render (390px, iPhone UA).
Extracts on-page signals from BOTH so H1/canonical/schema can be reconciled against the
rendered DOM. Writes analysis.json, raw/*.html, screenshots/*.png.

Usage: python3 crawl.py
"""
import json, re, ssl, urllib.request, urllib.parse
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

URLS = [
    "https://www.aa.co.nz/drivers/driving-school/",
    "https://www.aa.co.nz/drivers/driving-school/driving-lessons/",
    "https://www.aa.co.nz/drivers/driving-school/defensive-driving-course/",
    "https://www.aa.co.nz/drivers/driving-school/road-code-practice-test/",
    "https://www.aa.co.nz/drivers/driving-school/get-ready-for-learner-test/",
    "https://www.aa.co.nz/drivers/driving-school/get-ready-for-restricted-test/",
    "https://www.aa.co.nz/drivers/driving-school/get-ready-for-full-test/",
]
UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 "
      "(KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1")
ctx = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")


def slug(u):
    p = urllib.parse.urlparse(u).path.strip("/").split("/")
    return p[-1] if p[-1] != "driving-school" else "driving-school-hub"


def fetch_static(u):
    r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}),
                               context=ctx, timeout=30)
    return r.status, dict(r.headers), r.read().decode("utf-8", "replace")


def extract(html, url):
    s = BeautifulSoup(html, "lxml")
    ld = []
    for t in s.find_all("script", type="application/ld+json"):
        try:
            d = json.loads(t.string or "")
        except Exception:
            ld.append({"_parse_error": True}); continue
        items = d if isinstance(d, list) else d.get("@graph", [d]) if isinstance(d, dict) else []
        for i in items:
            if isinstance(i, dict):
                ld.append(i.get("@type"))
    md = [m.get("itemtype") for m in s.find_all(attrs={"itemtype": True})]
    meta = lambda **k: (s.find("meta", attrs=k) or {}).get("content") if s.find("meta", attrs=k) else None
    canon = s.find("link", rel="canonical")
    for t in s(["script", "style", "noscript", "svg", "template"]):
        t.decompose()
    main = s.find("main") or s.body or s
    text = re.sub(r"\s+", " ", main.get_text(" ")).strip()
    body_text = re.sub(r"\s+", " ", (s.body or s).get_text(" ")).strip()
    heads = [(h.name, re.sub(r"\s+", " ", h.get_text(" ")).strip()) for h in s.find_all(re.compile("^h[1-6]$"))]
    links = [a.get("href") for a in s.find_all("a", href=True)]
    host = urllib.parse.urlparse(url).netloc
    internal = [l for l in links if l.startswith("/") or host in l]
    imgs = s.find_all("img")
    return {
        "title": s.title.get_text(strip=True) if s.title else None,
        "meta_description": meta(name="description"),
        "robots": meta(name="robots"),
        "canonical": canon.get("href") if canon else None,
        "og_title": meta(property="og:title"), "og_image": meta(property="og:image"),
        "viewport": meta(name="viewport"),
        "hreflang": [l.get("hreflang") for l in s.find_all("link", rel="alternate") if l.get("hreflang")],
        "h1": [t for n, t in heads if n == "h1"],
        "headings": heads,
        "word_count_main": len(text.split()), "word_count_body": len(body_text.split()),
        "main_text": text,
        "jsonld_types": ld, "microdata": md,
        "links_total": len(links), "links_internal": len(internal),
        "imgs": len(imgs), "imgs_no_alt": sum(1 for i in imgs if not (i.get("alt") or "").strip()),
        "imgs_lazy": sum(1 for i in imgs if i.get("loading") == "lazy"),
    }


def main():
    out = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        c = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2,
                          is_mobile=True, has_touch=True, user_agent=UA)
        for u in URLS:
            sl = slug(u)
            st, hdr, shtml = fetch_static(u)
            open(f"raw/{sl}.static.html", "w").write(shtml)
            pg = c.new_page()
            resp = pg.goto(u, wait_until="networkidle", timeout=90000)
            pg.wait_for_timeout(2500)
            rhtml = pg.content()
            open(f"raw/{sl}.rendered.html", "w").write(rhtml)
            ux = pg.evaluate("""() => {
              const vw = window.innerWidth;
              const small = [...document.querySelectorAll('a,button,input,select,[role=button]')]
                .filter(e => {const r=e.getBoundingClientRect(); return r.width>0&&r.height>0&&(r.width<48||r.height<48)&&getComputedStyle(e).visibility!=='hidden'}).length;
              const tiny = [...document.querySelectorAll('p,li,span,a')].filter(e=>e.innerText&&e.innerText.trim().length>3&&parseFloat(getComputedStyle(e).fontSize)<12).length;
              return {scrollWidth: document.documentElement.scrollWidth, innerWidth: vw,
                      horizontal_overflow: document.documentElement.scrollWidth > vw+1,
                      tap_targets_under_48px: small, text_under_12px: tiny,
                      page_height: document.documentElement.scrollHeight};
            }""")
            pg.screenshot(path=f"screenshots/{sl}-390-fold.png")
            pg.screenshot(path=f"screenshots/{sl}-390-full.png", full_page=True)
            pg.close()
            rec = {"url": u, "slug": sl, "status": st, "final_url": resp.url,
                   "x_robots": hdr.get("X-Robots-Tag"), "content_type": hdr.get("Content-Type"),
                   "html_bytes_static": len(shtml), "html_bytes_rendered": len(rhtml),
                   "static": extract(shtml, u), "rendered": extract(rhtml, u), "mobile_ux": ux}
            r = rec["rendered"]
            rec["text_ratio_pct"] = round(100 * len(r["main_text"]) / max(1, len(rhtml)), 1)
            out.append(rec)
            print(sl, st, r["h1"], r["word_count_main"], r["jsonld_types"])
        b.close()
    json.dump(out, open("analysis.json", "w"), indent=1)


if __name__ == "__main__":
    main()

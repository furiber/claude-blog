#!/usr/bin/env python3
"""Content-only re-extraction + scoring for the 7 crawled pages.

AA's AEM template has no <main>; the global mega-menu (~990 words) and footer sit in
experience fragments. This strips them so word counts, headings and duplicate checks
reflect the page's own content. Reads analysis.json + raw/*.rendered.html, writes
analysis.json (enriched in place) and dupes.json.

Usage: python3 analyze.py
"""
import json, re, itertools
from bs4 import BeautifulSoup

CHROME_SEL = "[class*=cmp-experiencefragment--header],[class*=cmp-experiencefragment--footer],header,footer,nav"


def content(html):
    s = BeautifulSoup(html, "lxml")
    has_main = bool(s.find("main"))
    for t in s.select(CHROME_SEL):
        t.decompose()
    for t in s(["script", "style", "noscript", "svg", "template", "iframe"]):
        t.decompose()
    body = s.body or s
    text = re.sub(r"\s+", " ", body.get_text(" ")).strip()
    heads = [(h.name, re.sub(r"\s+", " ", h.get_text(" ")).strip()) for h in body.find_all(re.compile("^h[1-6]$"))]
    faq_like = sum(1 for n, t in heads if t.endswith("?"))
    tables = len(body.find_all("table"))
    lists = len(body.find_all(["ul", "ol"]))
    return has_main, text, heads, faq_like, tables, lists


def shingles(t, n=5):
    w = re.findall(r"[a-z0-9']+", t.lower())
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


def heading_skips(heads):
    lv = [int(n[1]) for n, _ in heads]
    return sum(1 for a, b in zip(lv, lv[1:]) if b - a > 1)


def main():
    pages = json.load(open("analysis.json"))
    sh = {}
    for p in pages:
        html = open(f"raw/{p['slug']}.rendered.html").read()
        has_main, text, heads, faq_q, tables, lists = content(html)
        r = p["rendered"]
        c = {"has_main_landmark": has_main, "word_count": len(text.split()), "headings": heads,
             "h2": [t for n, t in heads if n == "h2"], "question_headings": faq_q,
             "tables": tables, "lists": lists, "heading_level_skips": heading_skips(heads),
             "text_ratio_pct": round(100 * len(text) / max(1, p["html_bytes_rendered"]), 1)}
        p["content"] = c
        r.pop("main_text", None); p["static"].pop("main_text", None)
        issues = []
        t, d = r["title"] or "", r["meta_description"] or ""
        if not t: issues.append("missing_title")
        elif len(t) > 60: issues.append(f"title_long_{len(t)}")
        elif len(t) < 30: issues.append(f"title_short_{len(t)}")
        if not d: issues.append("missing_meta_description")
        elif len(d) > 160: issues.append(f"meta_long_{len(d)}")
        elif len(d) < 70: issues.append(f"meta_short_{len(d)}")
        if len(r["h1"]) != 1: issues.append(f"h1_count_{len(r['h1'])}")
        if not r["canonical"]: issues.append("missing_canonical")
        elif not r["canonical"].startswith("http"): issues.append("relative_canonical")
        if r["og_image"] and not r["og_image"].startswith("http"): issues.append("relative_og_image")
        if not has_main: issues.append("no_main_landmark")
        if c["heading_level_skips"]: issues.append(f"heading_skips_{c['heading_level_skips']}")
        if c["word_count"] < 600: issues.append("thin_content")
        if not r["jsonld_types"]: issues.append("no_schema")
        if "BreadcrumbList" not in r["jsonld_types"]: issues.append("no_breadcrumb_schema")
        if p["mobile_ux"]["tap_targets_under_48px"] > 20: issues.append("small_tap_targets")
        p["issues"] = issues
        sh[p["slug"]] = shingles(text)
    dupes = []
    for a, b in itertools.combinations(pages, 2):
        A, B = sh[a["slug"]], sh[b["slug"]]
        j = len(A & B) / max(1, len(A | B))
        cont = len(A & B) / max(1, min(len(A), len(B)))
        dupes.append({"a": a["url"], "b": b["url"], "a_slug": a["slug"], "b_slug": b["slug"],
                      "jaccard_pct": round(100 * j, 1), "containment_pct": round(100 * cont, 1)})
    dupes.sort(key=lambda x: -x["jaccard_pct"])
    titles = {}
    for p in pages: titles.setdefault(p["rendered"]["title"], []).append(p["url"])
    json.dump(pages, open("analysis.json", "w"), indent=1)
    json.dump({"method": "5-word shingle Jaccard + containment on content-only rendered text",
               "pairs": dupes, "duplicate_titles": {k: v for k, v in titles.items() if len(v) > 1}},
              open("dupes.json", "w"), indent=1)
    for p in pages:
        print(p["slug"], p["content"]["word_count"], p["content"]["text_ratio_pct"], p["issues"])
    for d in dupes[:8]: print(d["a_slug"], d["b_slug"], d["jaccard_pct"], d["containment_pct"])


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Cannibalisation cross-check: in-scope pages vs same-intent sibling URLs (reference only).

Siblings are fetched as static HTML (AEM server-renders; static == rendered for all 7
in-scope pages, see analysis.json). Same content-only extraction + 5-gram shingles as
analyze.py. Writes siblings.json and merges pairs into dupes.json under "sibling_pairs".

Usage: python3 siblings.py
"""
import json, ssl, urllib.request
from analyze import content, shingles

SIBLINGS = [
    "https://www.aa.co.nz/drivers/driving-school/get-learner-licence/",
    "https://www.aa.co.nz/drivers/driving-school/get-restricted-licence/",
    "https://www.aa.co.nz/drivers/driving-school/get-full-licence/",
    "https://www.aa.co.nz/drivers/driving-school/practice-restricted-test/",
    "https://www.aa.co.nz/drivers/driving-school/practice-full-test/",
    "https://www.aa.co.nz/drivers/driving-school/road-code/",
    "https://www.aa.co.nz/drivers/driver-licences/learner-driver-licences/",
    "https://www.aa.co.nz/drivers/driver-licences/full-driver-licences/",
]
UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148"
ctx = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")


def main():
    pages = json.load(open("analysis.json"))
    mine = {p["url"]: shingles(content(open(f"raw/{p['slug']}.rendered.html").read())[1]) for p in pages}
    sib, pairs = [], []
    for u in SIBLINGS:
        try:
            r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), context=ctx, timeout=30)
            html = r.read().decode("utf-8", "replace")
        except Exception as e:
            sib.append({"url": u, "error": str(e)}); continue
        from bs4 import BeautifulSoup
        s = BeautifulSoup(html, "lxml")
        _, text, heads, *_ = content(html)
        S = shingles(text)
        sib.append({"url": u, "status": r.status, "title": s.title.get_text(strip=True) if s.title else None,
                    "h1": [h for n, h in heads if n == "h1"], "word_count": len(text.split())})
        for mu, M in mine.items():
            inter = len(M & S)
            pairs.append({"a": mu, "b": u, "jaccard_pct": round(100 * inter / max(1, len(M | S)), 1),
                          "containment_pct": round(100 * inter / max(1, min(len(M), len(S))), 1)})
    pairs.sort(key=lambda x: -x["containment_pct"])
    json.dump(sib, open("siblings.json", "w"), indent=1)
    d = json.load(open("dupes.json")); d["sibling_pairs"] = pairs
    json.dump(d, open("dupes.json", "w"), indent=1)
    for s_ in sib: print(s_)
    for p in pairs[:12]: print(p["a"].split("/")[-2], "<>", p["b"].split("/")[-2], p["jaccard_pct"], p["containment_pct"])


if __name__ == "__main__":
    main()

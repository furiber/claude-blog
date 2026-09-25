#!/usr/bin/env python3
"""Assemble AUDIT-REPORT.md from report_core.md + sections/*.md + computed tables/lists.

Placeholders: {{CHART:file}}, {{LIST:file}}, {{SECTION:name}}, {{HEALTH}}, {{PERF}},
{{ONPAGE_TABLE}}, {{LH_TABLE}}. Section "uniqueness" is the "Page Uniqueness" part of
sections/content-gaps.md; "content-gaps" is the rest.

Usage: python3 build_report.py
"""
import json, re

pages = json.load(open("analysis.json")); scores = json.load(open("scores.json"))
lh = json.load(open("lighthouse/summary.json")); lists = json.load(open("charts/chart_lists.json"))
SHORT = {"driving-school-hub": "Hub", "driving-lessons": "Driving lessons", "defensive-driving-course": "Defensive driving",
         "road-code-practice-test": "Road Code test", "get-ready-for-learner-test": "Get ready: learner",
         "get-ready-for-restricted-test": "Get ready: restricted", "get-ready-for-full-test": "Get ready: full"}


def split_sections():
    cg = open("sections/content-gaps.md").read()
    m = re.search(r"^#+ .*Page Uniqueness.*$", cg, re.M | re.I)
    gaps, uniq = (cg[:m.start()], cg[m.end():]) if m else (cg, "")
    demote = lambda t: re.sub(r"^(#+) ", lambda x: "#" * min(6, len(x.group(1)) + 1) + " ", t, flags=re.M)
    strip_h1 = lambda t: re.sub(r"^# .*\n", "", t, count=1, flags=re.M)
    sch = open("sections/schema.md").read()
    return {"content-gaps": demote(strip_h1(gaps)).strip(), "uniqueness": demote(uniq).strip(),
            "schema": demote(strip_h1(sch)).strip()}


def onpage():
    rows = []
    for p in pages:
        r = p["rendered"]
        iss = ", ".join(i for i in p["issues"] if i not in ("no_breadcrumb_schema",))
        rows.append(f"| {SHORT[p['slug']]} | {r['title']} ({len(r['title'])}) | {len(r['meta_description'])} | "
                    f"{r['h1'][0]} | {p['content']['word_count']} | {iss} |")
    return "\n".join(rows)


def lhtable():
    L = ["| Page | Perf | A11y | Best pr. | SEO | FCP | LCP | TBT | CLS | Weight | DOM |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for s, v in lh.items():
        L.append(f"| {SHORT[s]} | {v['performance']} | {v['accessibility']} | {v['best-practices']} | {v['seo']} | "
                 f"{v['fcp_s']}s | {v['lcp_s']}s | {v['tbt_ms']} ms | {v['cls']} | {v['bytes_kib']:,} KiB | {v['dom']:,} |")
    return "\n".join(L)


def main():
    t = open("report_core.md").read(); sec = split_sections()
    t = t.replace("{{HEALTH}}", str(scores["health"])).replace("{{PERF}}", str(scores["lighthouse_mean_performance"]))
    t = t.replace("{{ONPAGE_TABLE}}", onpage()).replace("{{LH_TABLE}}", lhtable())
    t = re.sub(r"\{\{CHART:(.*?)\}\}", lambda m: f"![{m.group(1)}](charts/{m.group(1)})", t)
    t = re.sub(r"\{\{LIST:(.*?)\}\}", lambda m: "\n*Chart data, top to bottom:*\n\n" + "\n".join(f"- {x}" for x in lists[m.group(1)]) + "\n", t)
    t = re.sub(r"\{\{SECTION:(.*?)\}\}", lambda m: sec[m.group(1)], t)
    assert "{{" not in t, re.findall(r"\{\{.*?\}\}", t)
    open("AUDIT-REPORT.md", "w").write(t); print("wrote AUDIT-REPORT.md", len(t.split()), "words")


if __name__ == "__main__":
    main()

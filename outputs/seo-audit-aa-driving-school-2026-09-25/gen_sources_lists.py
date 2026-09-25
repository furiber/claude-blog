#!/usr/bin/env python3
"""Generate DATA-SOURCES-AND-ACTION-LISTS.md (Appendix A + B) from the audit data.

Appendix B URL lists are computed from analysis.json + dupes.json (never hand-written).
audit_appendix.py imports build_appendix_data() so the DOCX uses the identical data.

Usage: python3 gen_sources_lists.py
"""
import json

AUDIT_DATE = "2026-09-25"
NEAR_DUP_THRESHOLD = 20.0  # 5-gram containment % that flags a pair for review


def build_appendix_data():
    pages = json.load(open("analysis.json"))
    dupes = json.load(open("dupes.json"))
    lh = json.load(open("lighthouse/summary.json"))
    r = lambda p: p["rendered"]
    A = [
        ("URL inventory / crawl", "User-supplied list (7 URLs) + aa.co.nz sitemap index (/.sitemap.xml) for sibling discovery",
         "7/7 in-scope URLs; 42 /drivers/driving-school/ URLs discovered in sitemap (inventory only)"),
        ("Static vs rendered HTML", "urllib static fetch + Playwright Chromium render (390x844, iPhone UA)", "7/7"),
        ("On-page (title, meta, H1, canonical)", "Playwright RENDERED DOM (reconciled with static)", "7/7"),
        ("Content, word count, text ratio", "Rendered DOM, global nav + footer fragments removed (analyze.py)", "7/7"),
        ("Duplicate content heatmap", "5-gram shingle Jaccard + containment (analyze.py)", "7/7, all 21 pairs"),
        ("Cannibalisation cross-check", "Same method vs 8 same-intent sibling URLs (siblings.py, static HTML)",
         "7 in-scope x 8 siblings = 56 pairs"),
        ("Schema audit", "JSON-LD parsed from rendered DOM", "7/7"),
        ("Lighthouse / lab CWV (mobile)", "Lighthouse 12.8.2 CLI, mobile form factor, simulated throttling, local Chromium",
         "7/7 (see list below)"),
        ("Field CWV (CrUX)", "Not available: PageSpeed Insights API quota exhausted (HTTP 429), no CrUX key", "0/7"),
        ("Mobile rendering / UX", "Playwright 390px screenshots (fold + full page), tap-target and overflow probe", "7/7"),
        ("Keyword rankings / SERP positions", "Firecrawl web search, location New Zealand, top 10 organic",
         "9 queries (7 non-branded, 2 branded)"),
        ("Competitor identification + gap", "Firecrawl SERP domain overlap + scrape of best competitor page per query",
         "3 competitor pages scraped"),
        ("Brand cannibalisation", "Firecrawl search: 'aa driving school', 'aa defensive driving course'", "2 branded queries"),
        ("GEO / AI readiness", "robots.txt, llms.txt probe, rendered headings, schema", "Site root + 7/7"),
        ("Search volume / keyword difficulty", "Historical SEMrush snapshot, June 2026 (prior audit in furiber/claude-seo) - NOT live",
         "Subfolder-level, reference only"),
    ]
    not_used = [
        ("SEMrush MCP (live)", "Not connected in this session; no SEMrush tools available. June 2026 snapshot cited as historical only."),
        ("Chrome DevTools MCP Lighthouse", "Not connected; Lighthouse CLI on the same Chromium engine used instead."),
        ("DataForSEO", "Excluded by instruction."),
        ("Google Search Console / GA4", "No credentials in this session."),
        ("CrUX / PageSpeed Insights field data", "PSI API returned 429 (shared quota), no API key."),
        ("Google Business Profile", "Skipped by instruction."),
        ("Bright Data", "Not used."),
        ("Google AI Overview capture", "SERP tool does not expose AIO blocks; AIO citations not measurable."),
    ]
    B = {}
    B["missing_meta_description"] = [p["url"] for p in pages if not r(p)["meta_description"]]
    B["missing_h1"] = [p["url"] for p in pages if not r(p)["h1"]]
    B["multiple_h1"] = [p["url"] for p in pages if len(r(p)["h1"]) > 1]
    B["short_or_generic_title"] = [f"{p['url']} ({len(r(p)['title'])} chars: {r(p)['title']})" for p in pages
                                   if len(r(p)["title"]) < 40 or r(p)["title"].lower().startswith("free")]
    B["duplicate_titles"] = [f"{t}: {', '.join(u)}" for t, u in dupes["duplicate_titles"].items()]
    B["near_duplicate_pairs"] = [f"{d['a']} <> {d['b']} ({d['containment_pct']}% containment, {d['jaccard_pct']}% Jaccard)"
                                 for d in dupes["pairs"] if d["containment_pct"] >= NEAR_DUP_THRESHOLD]
    B["relative_canonical"] = [f"{p['url']} (canonical: {r(p)['canonical']})" for p in pages if "relative_canonical" in p["issues"]]
    B["relative_og_image"] = [p["url"] for p in pages if "relative_og_image" in p["issues"]]
    B["no_main_landmark"] = [p["url"] for p in pages if not p["content"]["has_main_landmark"]]
    B["heading_level_skips"] = [f"{p['url']} ({p['content']['heading_level_skips']} skips)" for p in pages if p["content"]["heading_level_skips"]]
    B["under_700_words"] = [f"{p['url']} ({p['content']['word_count']} words)" for p in pages if p["content"]["word_count"] < 700]
    B["schema_coverage"] = [f"{p['url']}: {', '.join(t for t in r(p)['jsonld_types'] if t) or 'none'}" for p in pages]
    B["no_breadcrumb_schema"] = [p["url"] for p in pages if "BreadcrumbList" not in r(p)["jsonld_types"]]
    B["no_faqpage_but_visible_questions"] = [f"{p['url']} ({p['content']['question_headings']} question headings)" for p in pages
                                             if "FAQPage" not in r(p)["jsonld_types"] and p["content"]["question_headings"] >= 3]
    B["tap_targets_under_48px"] = [f"{p['url']} ({p['mobile_ux']['tap_targets_under_48px']} elements)" for p in pages]
    B["lighthouse_lcp_over_4s"] = [f"{p['url']} (lab LCP {lh[p['slug']]['lcp_s']}s)" for p in pages if lh[p["slug"]]["lcp_s"] > 4]
    B["cls_over_0_1"] = [f"{p['url']} (CLS {lh[p['slug']]['cls']})" for p in pages if lh[p["slug"]]["cls"] > 0.1]
    return {"A": A, "not_used": not_used, "lighthouse_urls": [p["url"] for p in pages if p["slug"] in lh], "B": B}


TITLES = {
    "missing_meta_description": "Missing meta description", "missing_h1": "Missing <h1>",
    "multiple_h1": "Multiple <h1>", "short_or_generic_title": "Short, generic or misleading titles",
    "duplicate_titles": "Duplicate titles",
    "near_duplicate_pairs": f"Near-duplicate content pairs (>= {NEAR_DUP_THRESHOLD:.0f}% containment)",
    "relative_canonical": "Relative canonical URL", "relative_og_image": "Relative og:image URL",
    "no_main_landmark": "No <main> landmark", "heading_level_skips": "Heading level skips",
    "under_700_words": "Content under 700 words", "schema_coverage": "Schema coverage (all pages)",
    "no_breadcrumb_schema": "No BreadcrumbList schema",
    "no_faqpage_but_visible_questions": "Visible Q&A but no FAQPage schema",
    "tap_targets_under_48px": "Tap targets under 48px (mobile)", "lighthouse_lcp_over_4s": "Lab LCP over 4s (mobile)",
    "cls_over_0_1": "CLS over 0.1 (mobile lab)",
}


def main():
    d = build_appendix_data()
    L = ["# Data Sources, Coverage and Action Lists", "",
         f"AA Driving School (aa.co.nz/drivers/driving-school/), 7 pages. Audit date: {AUDIT_DATE}. Mobile-first.", "",
         "Appendix B lists are generated by `gen_sources_lists.py` from `analysis.json` and `dupes.json`. "
         "H1, canonical and schema findings come from the rendered DOM (Playwright).", "",
         "## Appendix A: Data Sources and Coverage", "", "| Report section | Data source | Coverage |", "|---|---|---|"]
    L += [f"| {a} | {b} | {c} |" for a, b, c in d["A"]]
    L += ["", "### Pages Lighthouse / CWV ran on (mobile)", ""]
    L += [f"{i}. {u}" for i, u in enumerate(d["lighthouse_urls"], 1)]
    L += ["", "Lighthouse ran on all 7 in-scope pages, but from a cloud container through an HTTPS proxy. That inflates "
          "FCP/LCP/Speed Index. TBT, CLS, DOM size, byte weight and the diagnostics are less affected. No field (CrUX) data was collected.",
          "", "### Sources NOT used", "", "| Source | Reason |", "|---|---|"]
    L += [f"| {a} | {b} |" for a, b in d["not_used"]]
    L += ["", "## Appendix B: Action Lists (full URLs)", ""]
    for k, items in d["B"].items():
        L += [f"### {TITLES[k]} ({len(items)})", ""]
        L += [f"- {i}" for i in items] if items else ["- None found"]
        L.append("")
    open("DATA-SOURCES-AND-ACTION-LISTS.md", "w").write("\n".join(L))
    print("wrote DATA-SOURCES-AND-ACTION-LISTS.md", {k: len(v) for k, v in d["B"].items()})


if __name__ == "__main__":
    main()

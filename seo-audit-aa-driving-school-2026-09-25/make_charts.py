#!/usr/bin/env python3
"""Build scores.json + 7 PNG charts from analysis.json, dupes.json, lighthouse/*.json, raw/serp.json.

Category scores are an audit rubric (documented in AUDIT-REPORT.md, "Scoring method");
Performance is the mean Lighthouse mobile performance score. Also writes
charts/chart_lists.json: the bullet list under each bar chart, top-to-bottom in chart order.

Usage: python3 make_charts.py
"""
import json, glob, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
GOOD, WARN, SERIOUS, CRIT = "#0ca30c", "#fab219", "#ec835a", "#d03b3b"
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
SEQ = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRID,
                     "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                     "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.dpi": 160})
os.makedirs("charts", exist_ok=True)
pages = json.load(open("analysis.json"))
dupes = json.load(open("dupes.json"))
serp = json.load(open("raw/serp.json"))
SHORT = {"driving-school-hub": "Hub", "driving-lessons": "Driving lessons",
         "defensive-driving-course": "Defensive driving", "road-code-practice-test": "Road Code test",
         "get-ready-for-learner-test": "Get ready: learner", "get-ready-for-restricted-test": "Get ready: restricted",
         "get-ready-for-full-test": "Get ready: full"}
lists = {}

# ---- Lighthouse ----
lh = {}
for p in pages:
    f = f"lighthouse/{p['slug']}.json"
    if not os.path.exists(f): continue
    d = json.load(open(f)); a = d["audits"]
    lh[p["slug"]] = {**{k: round(v["score"] * 100) for k, v in d["categories"].items()},
                     "fcp_s": round(a["first-contentful-paint"]["numericValue"] / 1000, 1),
                     "lcp_s": round(a["largest-contentful-paint"]["numericValue"] / 1000, 1),
                     "tbt_ms": round(a["total-blocking-time"]["numericValue"]),
                     "cls": round(a["cumulative-layout-shift"]["numericValue"], 3),
                     "si_s": round(a["speed-index"]["numericValue"] / 1000, 1),
                     "bytes_kib": round(a["total-byte-weight"]["numericValue"] / 1024),
                     "dom": a["dom-size"]["numericValue"],
                     "lighthouse_version": d["lighthouseVersion"], "fetch_time": d["fetchTime"]}
json.dump(lh, open("lighthouse/summary.json", "w"), indent=1)
perf = round(np.mean([v["performance"] for v in lh.values()]))

# ---- Category rubric (see report "Scoring method") ----
cats = {"Technical SEO (mobile)": (20, 76), "On-page": (15, 80), "Content & uniqueness": (20, 70),
        "Schema": (10, 55), "Performance / CWV": (15, perf), "Mobile UX & accessibility": (10, 80),
        "GEO / AI readiness": (10, 58)}
health = round(sum(w * s for w, s in cats.values()) / sum(w for w, _ in cats.values()))
json.dump({"health": health, "categories": {k: {"weight": w, "score": s} for k, (w, s) in cats.items()},
           "lighthouse_mean_performance": perf}, open("scores.json", "w"), indent=1)


def status_col(s):
    return GOOD if s >= 80 else WARN if s >= 65 else SERIOUS if s >= 50 else CRIT


def hbar(fname, labels, vals, title, xlabel, colors, fmt="{:.0f}", xmax=None, note=None):
    fig, ax = plt.subplots(figsize=(8, 0.5 * len(labels) + 1.4))
    y = np.arange(len(labels))[::-1]
    ax.barh(y, vals, color=colors, height=0.62, edgecolor=SURF, linewidth=2)
    for yi, v in zip(y, vals):
        ax.text(v + (xmax or max(vals)) * 0.01, yi, fmt.format(v), va="center", color=INK, fontsize=9)
    ax.set_yticks(y, labels); ax.set_xlabel(xlabel)
    ax.set_xlim(0, xmax or max(vals) * 1.15)
    ax.grid(axis="x", color=GRID, linewidth=0.8); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.set_title(title, loc="left", color=INK, fontsize=12, fontweight="bold")
    if note: fig.text(0.01, 0.01, note, fontsize=7.5, color=INK2)
    fig.tight_layout(rect=(0, 0.04 if note else 0, 1, 1)); fig.savefig(f"charts/{fname}"); plt.close(fig)
    lists[fname] = [f"{l}: {fmt.format(v)}" for l, v in zip(labels, vals)]


# 1 gauge
fig, ax = plt.subplots(figsize=(5, 3), subplot_kw={"projection": "polar"})
ax.set_thetamin(0); ax.set_thetamax(180); ax.set_axis_off()
for lo, hi, c in [(0, 50, CRIT), (50, 65, SERIOUS), (65, 80, WARN), (80, 100, GOOD)]:
    ax.barh(1, np.radians((hi - lo) * 1.8), left=np.radians(180 - hi * 1.8), height=0.35, color=c, alpha=0.35)
ax.barh(1, np.radians(health * 1.8), left=np.radians(180 - health * 1.8), height=0.35, color=status_col(health))
ax.set_ylim(0, 1.25)
fig.text(0.5, 0.22, f"{health}/100", ha="center", fontsize=26, fontweight="bold", color=INK)
fig.text(0.5, 0.1, "SEO health score (weighted, 7 pages)", ha="center", fontsize=9, color=INK2)
fig.savefig("charts/01_health_gauge.png", bbox_inches="tight"); plt.close(fig)

# 2 category scores
cl = list(cats); cv = [cats[k][1] for k in cl]
hbar("02_category_scores.png", cl, cv, "Category scores (0 to 100)", "Score", [status_col(v) for v in cv], xmax=100)

# 3 Lighthouse per page
labs = [SHORT[s] for s in lh]; x = np.arange(len(labs)); w = 0.2
fig, ax = plt.subplots(figsize=(9, 4.2))
for i, (k, c) in enumerate([("performance", BLUE), ("accessibility", ORANGE), ("best-practices", AQUA), ("seo", YELLOW)]):
    ax.bar(x + (i - 1.5) * w, [lh[s][k] for s in lh], w, color=c, label=k.replace("-", " ").title(), edgecolor=SURF, linewidth=1.5)
ax.set_xticks(x, labs, rotation=20, ha="right"); ax.set_ylim(0, 105); ax.grid(axis="y", color=GRID)
ax.set_axisbelow(True); [ax.spines[s].set_visible(False) for s in ("top", "right")]
ax.legend(ncol=4, frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.12), fontsize=8.5)
ax.set_title("Lighthouse mobile category scores by page", loc="left", color=INK, fontweight="bold", pad=26)
fig.tight_layout(); fig.savefig("charts/03_lighthouse_scores.png"); plt.close(fig)
lists["03_lighthouse_scores.png"] = [f"{SHORT[s]}: Performance {v['performance']}, Accessibility {v['accessibility']}, "
                                     f"Best practices {v['best-practices']}, SEO {v['seo']}" for s, v in lh.items()]

# 4 SERP position map (non-branded)
rows = []
for q in serp["queries"]:
    if q["branded"]: continue
    aa = [r for r in q["results"] if r["domain"] == "aa.co.nz"]
    rows.append((q["query"], aa[0]["position"] if aa else 11, aa[0]["url"].replace("https://www.aa.co.nz", "").replace("https://", "") if aa else "not in top 10"))
fig, ax = plt.subplots(figsize=(9, 4))
y = np.arange(len(rows))[::-1]
for yi, (qq, pos, u) in zip(y, rows):
    ax.plot([1, pos], [yi, yi], color=GRID, linewidth=2, zorder=1)
    ax.scatter(pos, yi, s=90, color=GOOD if pos <= 3 else WARN if pos <= 10 else CRIT, zorder=2, edgecolor=SURF, linewidth=2)
    ax.text(pos + 0.25, yi, f"#{pos}  {u}", va="center", fontsize=7.5, color=INK2)
ax.set_yticks(y, [r[0] for r in rows]); ax.set_xlim(0.5, 11); ax.invert_xaxis() if False else None
ax.set_xticks(range(1, 11)); ax.set_xlabel("Best AA organic position (1 = top)")
ax.grid(axis="x", color=GRID); ax.set_axisbelow(True); [ax.spines[s].set_visible(False) for s in ("top", "right")]
ax.set_title("SERP position map: best AA URL per query (NZ, 25 Sep 2026)", loc="left", color=INK, fontweight="bold")
fig.tight_layout(); fig.savefig("charts/04_serp_positions.png"); plt.close(fig)
lists["04_serp_positions.png"] = [f"{q}: #{p} ({u})" for q, p, u in rows]

# 5 keyword-level visibility: domains by query presence
ov = sorted([d for d in serp["domain_overlap"] if d.get("avg_position")], key=lambda d: -d["queries_present"])
hbar("05_competitor_overlap.png", [d["domain"] for d in ov], [d["queries_present"] for d in ov],
     "Top-10 presence across 7 non-branded driving queries", "Queries where domain ranks top 10",
     [BLUE if d["domain"] == "aa.co.nz" else INK2 if d.get("type") == "government" else ORANGE for d in ov], xmax=7.8,
     note="Blue = AA, orange = commercial competitor, grey = government. Source: Firecrawl NZ search, 25 Sep 2026.")

# 6 duplicate heatmap
sl = [p["slug"] for p in pages]; n = len(sl); M = np.zeros((n, n))
for d in dupes["pairs"]:
    i, j = sl.index(d["a_slug"]), sl.index(d["b_slug"]); M[i, j] = M[j, i] = d["containment_pct"]
np.fill_diagonal(M, 100)
fig, ax = plt.subplots(figsize=(7.5, 6))
from matplotlib.colors import LinearSegmentedColormap
im = ax.imshow(M, cmap=LinearSegmentedColormap.from_list("seq", SEQ), vmin=0, vmax=100)
for i in range(n):
    for j in range(n):
        ax.text(j, i, "-" if i == j else f"{M[i, j]:.0f}%", ha="center", va="center", fontsize=8.5,
                color="#ffffff" if M[i, j] > 55 else INK)
ax.set_xticks(range(n), [SHORT[s] for s in sl], rotation=35, ha="right"); ax.set_yticks(range(n), [SHORT[s] for s in sl])
fig.colorbar(im, ax=ax, fraction=0.04, label="5-gram containment %")
ax.set_title("Duplicate content heatmap (content-only, rendered DOM)", loc="left", color=INK, fontweight="bold")
fig.tight_layout(); fig.savefig("charts/06_duplicate_heatmap.png"); plt.close(fig)

# 7 word counts vs competitors
wc = [(SHORT[p["slug"]], p["content"]["word_count"], BLUE) for p in pages]
for c in serp.get("competitor_pages", []):
    wc.append((c["url"].split("/")[2].replace("www.", "") + " (competitor)", c["word_count"], ORANGE))
hbar("07_word_counts.png", [w[0] for w in wc], [w[1] for w in wc], "Content word count vs top competitor pages",
     "Words (main content, nav/footer removed)", [w[2] for w in wc],
     note="Blue = AA page, orange = best-ranking competitor page for driving lessons / defensive driving / road code queries.")

# 8 GEO readiness signals
geo = [("AI crawlers allowed (robots.txt)", 100), ("Question-format headings (7/7 pages)", 100),
       ("Self-contained FAQ answers", 80), ("FAQPage schema coverage (1/7)", 14),
       ("Entity schema consistency (@id)", 30), ("llms.txt present", 0), ("AI Overview citation observed", 0)]
hbar("08_geo_signals.png", [g[0] for g in geo], [g[1] for g in geo], "GEO / AI Overview readiness signals",
     "Signal strength (0 to 100)", [status_col(g[1]) for g in geo], xmax=112,
     note="AI Overview presence was not exposed by the SERP tool; 0 means not observed, not confirmed absent.")

# 9 CWV lab metrics
hbar("09_lcp_by_page.png", [SHORT[s] for s in lh], [lh[s]["lcp_s"] for s in lh], "Lab LCP by page (Lighthouse mobile, simulated slow 4G)",
     "Seconds (good <= 2.5s)", [CRIT if lh[s]["lcp_s"] > 4 else WARN for s in lh], fmt="{:.1f}s",
     note="Absolute values inflated by the audit container's network proxy; use for relative ranking, not as field CWV.")

json.dump(lists, open("charts/chart_lists.json", "w"), indent=1)
print("health", health, "perf", perf); print(json.dumps(lh, indent=0)[:1500])

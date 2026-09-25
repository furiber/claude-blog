# Appendix C: Original Prompt and Run Record

## Run record

| Field | Value |
|---|---|
| Event | SEO audit: AA Driving School, 7 selected pages |
| Date used | 2026-09-25 (session started 2026-09-25T03:27Z) |
| Invocation | `/seo-audit` (command not installed in this session; request run as a plain task) |
| Environment | Claude Code on the web (cloud container), launched from the desktop app |
| Session | https://claude.ai/code/session_01FHdvP7oLruoLvRdaEih1YH |
| Main model (orchestrator, final report assembly, executive summary) | claude-opus-5-5 (confirmed via session metadata: configured and last served) |
| Repos | furiber/claude-blog (output branch `claude/youthful-cannon-h8a0sq`), furiber/claude-seo (tooling reference) |

## Where agents and models were used

| Stage | Executed by | Model | Why |
|---|---|---|---|
| Crawl, rendered-DOM extraction, 390px screenshots (`crawl.py`) | Orchestrator via Bash | claude-opus-5-5 (scripted, deterministic) | Playwright run; no model judgment in the data |
| Content-only re-extraction, duplicates, sibling cannibalisation (`analyze.py`, `siblings.py`) | Orchestrator via Bash | claude-opus-5-5 (scripted) | Deterministic Python |
| Lighthouse mobile on 7 URLs (`run_lighthouse.sh`) | Background shell job | n/a (Lighthouse 12.8.2) | Chrome DevTools MCP not connected |
| SERP extraction, competitor overlap, competitor page scrape (`raw/serp.json`) | Subagent "SERP competitor extraction" | haiku alias (claude-haiku-4-5) | Structured lookups and extraction |
| Schema recommendations + JSON-LD templates, content gaps, page uniqueness (`sections/*.md`) | Subagent "Schema + content gap analysis" | sonnet alias (the Agent tool exposes only the `sonnet` alias, not the pinned claude-sonnet-4-6 ID the prompt asked for) | Analysis, synthesis, gap identification |
| Scoring rubric, charts, executive summary, AUDIT-REPORT.md, DOCX assembly, appendices | Orchestrator | claude-opus-5-5 | Strategic narrative and final assembly |

## Deviations from the prompt (and why)

- SEMrush MCP was not connected, so there is no live SEMrush data. Rankings come from Firecrawl NZ SERPs. Volumes come from the June 2026 SEMrush snapshot in furiber/claude-seo and are labelled historical.
- Chrome DevTools MCP was not connected. Lighthouse ran through the CLI on the same Chromium engine, and H1, canonical and schema checks used the Playwright-rendered DOM.
- Crawl scope was limited to the 7 listed URLs ("only those pages"). The instruction to crawl all child/sibling pages conflicted with that, so siblings were only inventoried from the sitemap, and 8 same-intent siblings were fetched for the cannibalisation cross-check.
- GBP audit skipped by instruction; the section is kept as a stub.
- `audit_appendix.py` and `gen_sources_lists.py` were written for this audit, not copied. furiber/claude-seo has no `audit_appendix.py`. Its `gen_sources_lists.py` is hard-coded to another site.

## Original prompt (verbatim)

```
/seo-audit 

 
 
## Audit Configuration 
**Target:** https://www.aa.co.nz/drivers/driving-school/ 
https://www.aa.co.nz/drivers/driving-school/driving-lessons/ 
https://www.aa.co.nz/drivers/driving-school/defensive-driving-course/ 
https://www.aa.co.nz/drivers/driving-school/road-code-practice-test/ 
https://www.aa.co.nz/drivers/driving-school/get-ready-for-learner-test/ 
https://www.aa.co.nz/drivers/driving-school/get-ready-for-restricted-test/ 
https://www.aa.co.nz/drivers/driving-school/get-ready-for-full-test/ only those pages
**Audit type:** 7 selected pages
**Priority:** Mobile-first — all technical checks, rendering, and UX findings evaluated 
from a mobile perspective first. Desktop is secondary. 
 
## Agent Architecture 
Use subagents wherever tasks can be parallelised or isolated. Match model size to task: 
- Crawling, data extraction, structured lookups → claude-haiku-4-5 
- Analysis, synthesis, gap identification, recommendations → claude-sonnet-4-6 
- Executive summary, strategic narrative, final report assembly → most capable model 
 
## Crawl Instructions 
Crawl [TARGET URL] and all child/sibling pages. Identify the full URL inventory. Do not 
limit the crawl. Use the repo tools at https://github.com/furiber/claude-seo/. 
 
## Google Business Profile (GBP) 
Skip GBP
 
## Data Sources 
- Keyword & competitor data: SEMrush MCP (already connected) — do NOT use DataForSEO. 
- Pull organic rankings, search volume, keyword difficulty, competitor gap from SEMrush. 
 
## Competitors 
Auto-identify 2-3 relevant competitors from SEMrush keyword overlap. Use for gap analysis, 
thin-content comparison, and the competitor comparison section. 
 
## Analysis Requirements 
- Mobile-first — 390px Playwright screenshot, mobile SERP evaluation. 
- Lighthouse / CWV — run Lighthouse in mobile mode via Chrome MCP 
  (mcp__plugin_chrome-devtools-mcp_chrome-devtools__lighthouse_audit) for real mobile CWV. 
- GEO / AI Overview — Google AIO citations, llms.txt, Agentic Browsing score. 
- Duplicate content — cross-page heatmap across all crawled URLs. 
- Thin content — word count, text ratio, missing content vs top-3 competitors. 
- Schema audit — detect existing schema, flag missing, provide JSON-LD templates. 
- Keyword rankings — SEMrush ranked keywords + SERP position map. 
- Brand cannibalization — search branded query, identify competing domains. 
- Page uniqueness — for every crawled page assess duplicate/similar content, 
  cannibalisation risk, thin pages; output a uniqueness summary table. 
- Reconcile every H1 / canonical / schema finding against the RENDERED DOM (Chrome MCP) 
  before reporting — static HTML on JS-rendered sites is unreliable for these. 
 
## Schema Markup Guidance 
Do not classify schema as a quick win. Treat as a strategic investment with realistic 
effort estimates. Provide JSON-LD templates for all recommended schema types. 
 
## Charts and Visualisations 
Include 6+ charts: health score gauge, category scores, SERP positions, keywords, 
duplicate content heatmap, GEO citations. Under each bar chart, add a bulleted list of 
the same data top-to-bottom matching chart order. 
 
## Output 
Save all files to: seo-audit-[section-name]-[YYYY-MM-DD]/ 
Produce: 
1. AUDIT-REPORT.md — full findings, action plan Critical → High → Medium → Low. 
2. [Section-Name]-SEO-Audit.docx — professional report with all sections + embedded charts. 
3. DATA-SOURCES-AND-ACTION-LISTS.md — companion file (also embed as Appendix A + B in the DOCX). 
 
Both the report and the DOCX must include: Executive Summary, Keyword Opportunity Table, 
On-Page Issues, Content Gap Recommendations, Technical SEO Checklist (mobile-first), 
Lighthouse / CWV Results, GBP Audit, GEO / AI Overview, Competitor Comparison, Page 
Uniqueness Analysis, Schema Recommendations, Prioritised Action Plan, and: 
 
### MANDATORY Appendix A — Data Sources & Coverage 
A table mapping every report section to its data source and site coverage. Explicitly 
list the exact pages Lighthouse/CWV ran on (they are rarely run on all pages), and a 
"sources NOT used" list (e.g. DataForSEO, GSC/GA4, Bright Data, GBP if skipped). 
 
### MANDATORY Appendix B — Action Lists (full URLs) 
Every URL behind each action point, generated from analysis.json / dupes.json (not 
hand-written): missing meta description, missing <h1>, duplicate/near-duplicate content 
(both URLs + similarity %), short/generic titles, duplicate titles, schema coverage. 
 
Generate Appendix A + B with the reusable scripts copied into the audit folder: 
audit_appendix.py (DOCX) and gen_sources_lists.py (standalone .md). 
 
### MANDATORY Appendix C - the original prompt 

Save the event along with the date, so it can be used later and referenced along with the date of when it was used. Include also the main model used and where the different agents and models where used.
```

# AA Driving School: Mobile-First SEO Audit (7 pages)

**Site:** aa.co.nz/drivers/driving-school/ · **Audit date:** 25 September 2026 · **Scope:** 7 selected pages · **Priority:** mobile-first (390px) · **GBP:** skipped by instruction

| # | Page | URL |
|---|---|---|
| 1 | Hub | https://www.aa.co.nz/drivers/driving-school/ |
| 2 | Driving lessons | https://www.aa.co.nz/drivers/driving-school/driving-lessons/ |
| 3 | Defensive driving | https://www.aa.co.nz/drivers/driving-school/defensive-driving-course/ |
| 4 | Road Code test | https://www.aa.co.nz/drivers/driving-school/road-code-practice-test/ |
| 5 | Get ready: learner | https://www.aa.co.nz/drivers/driving-school/get-ready-for-learner-test/ |
| 6 | Get ready: restricted | https://www.aa.co.nz/drivers/driving-school/get-ready-for-restricted-test/ |
| 7 | Get ready: full | https://www.aa.co.nz/drivers/driving-school/get-ready-for-full-test/ |

## 1. Executive Summary

{{CHART:01_health_gauge.png}}

**Overall SEO health: {{HEALTH}}/100.** The seven pages are well built on the basics. Each has one clear H1, a unique title and meta description, a self-referencing canonical, an XML sitemap entry, indexable status and server-rendered content, so the static HTML matches the rendered DOM. AA holds **#1 for "driving lessons nz", "defensive driving course nz" and "road code practice test nz"** in today's NZ SERP sample. The score is held down by three problems.

1. **Mobile performance is the biggest risk.** Lighthouse mobile performance averages **{{PERF}}/100** on all 7 pages. About 3.1 to 4.2 MB ships per page. Google Tag Manager alone blocks the main thread for about 0.8s, and two GA4 tags load. reCAPTCHA (~180 KB unused JS) and an eager YouTube embed (~1 MB, driving-lessons) load on content pages, and a Material Symbols icon font sits on the critical path. The absolute lab times are inflated by the audit container's network proxy, but TBT (543 to 1,402 ms) and the JS/byte findings do not depend on the network. They are real.
2. **Intent cannibalisation across licence stages, not duplicate text.** Text overlap between the 7 pages is low (7% to 22% 5-gram containment). The problem is that each licence stage has 3 or 4 AA URLs chasing the same intent. For example, "restricted licence test practice nz" ranks `/practice-restricted-test/`, not `/get-ready-for-restricted-test/`. "full licence test nz" ranks `/drivers/driver-licences/full-driver-licences/` at #4, and `/get-ready-for-full-test/` is not in the top 10. In June 2026 SEMrush had `/get-ready-for-full-test/` at #5.
3. **Schema is thin and inconsistent for an entity as strong as AA.** Five of 7 pages carry a bare `Service` node with no offers, audience or area detail. No page has `BreadcrumbList`. `FAQPage` appears only on the hub, although 6 pages show visible Q&A blocks. Two conflicting Organization `@id`s are in use. The Road Code page sits under a "Free NZ Road Code Practice Test" title but marks up a paid `Product` ($12.50 to $20), a title/offer mismatch.

**Top 5 actions:** (1) Defer or remove third-party JS on content pages: GTM consolidation, lazy reCAPTCHA, YouTube facade. (2) Assign one primary URL per licence stage and differentiate or consolidate the rest. (3) Retitle the Road Code page so "free" describes only the trial. (4) Make canonical and og:image URLs absolute. (5) Start the schema programme: entity `@id`, BreadcrumbList, Course/Offer, FAQPage. This is a multi-sprint investment, not a quick win.

{{CHART:02_category_scores.png}}
{{LIST:02_category_scores.png}}

**Scoring method.** Weighted rubric: Technical SEO (mobile) 20%, Content and uniqueness 20%, On-page 15%, Performance/CWV 15% (mean Lighthouse mobile performance score), Schema 10%, Mobile UX and accessibility 10%, GEO/AI readiness 10%. Because the performance input comes from proxy-inflated lab data, the overall score is conservative. With field CWV it would probably land about 5 to 8 points higher.

## 2. Keyword Opportunity Table

Positions are **live NZ SERP observations (Firecrawl search, 25 Sep 2026, top 10)**. Volumes are the **historical SEMrush NZ snapshot from June 2026** (prior audit). SEMrush MCP was not connected for this run, so treat the volumes as directional.

| Keyword | NZ vol. (SEMrush, Jun 2026) | AA best URL today | Pos. today | Pos. Jun 2026 | Opportunity |
|---|---|---|---|---|---|
| learning license test | 8,100 | /road-code-practice-test/ | n/a | 2 | Protect; drivingtests.co.nz holds #1 |
| driving test nz | 6,600 | /road-code-practice-test/ | n/a | 5 | Needs a clear "which driving test?" answer block on the hub |
| full licence test nz | 4,400 | /drivers/driver-licences/full-driver-licences/ | 4 | 5 (get-ready-for-full-test) | **High:** get-ready-for-full-test has dropped out of the top 10; consolidate |
| book full license test | 4,400 | not ranking | n/a | n/a | **High:** add "how to book" steps + NZTA/VTNZ booking links on get-ready-for-full-test |
| restricted license test | 4,400 | /practice-restricted-test/ | n/a (#1 for "restricted licence test practice nz") | 19 | **High:** decide primary URL between get-ready and practice-restricted |
| defensive driving course | 4,400 | /defensive-driving-course/ | 1 | 1 | Protect: CLS 0.13 and TBT are the main risks |
| book restricted test | 3,600 | not ranking | n/a | n/a | **High:** same fix as "book full license test" on get-ready-for-restricted-test |
| learners licence nz | 3,600 | /drivers/driver-licences/learner-driver-licences/ | n/a | 3 | Medium: get-ready-for-learner-test is not the ranking URL |
| road code | 2,400 | /road-code-practice-test/ | n/a | 4 | Protect |
| driving lessons nz | n/a | /driving-lessons/ | 1 | n/a | Protect |
| driving lessons auckland | 1,600 | drivingschool.aa.co.nz | 2 | 2 | Medium: A1 Driving School #1; subdomain split |
| defensive driving course nz | 1,600 | /defensive-driving-course/ | 1 | 1 | Protect |
| nz road code test | 1,600 | /road-code-practice-test/ | n/a | 2 | Protect |
| learner licence test nz | n/a | /road-code-practice-test/ | 2 | n/a | Medium: drivingtests.co.nz #1 |

{{CHART:05_competitor_overlap.png}}
{{LIST:05_competitor_overlap.png}}

## 3. SERP Position Map

{{CHART:04_serp_positions.png}}
{{LIST:04_serp_positions.png}}

Only 3 of the 7 audited pages are the best-ranking AA URL for their own head term: driving-lessons, defensive-driving-course and road-code-practice-test. The three **get-ready** pages are outranked by other AA URLs for their core queries (see Page Uniqueness Analysis).

**Brand query check.** Firecrawl's results for "aa driving school" and "aa defensive driving course" were dominated by US businesses named "AA Driving School" and by theaa.com (UK). The tool's NZ localisation looks weak for brand terms, so read this as a brand-name collision risk, not an NZ ranking loss. In the June 2026 NZ SEMrush data AA held #1 for "aa driving school". Consistent Organization entity markup, one `@id` with `sameAs` links, is the defence (see Schema).

## 4. On-Page Issues (rendered DOM)

All findings below were reconciled against the Playwright-rendered DOM. The static HTML and the rendered DOM matched for title, meta, H1, canonical and JSON-LD on all 7 pages. AEM server-renders the content.

| Page | Title (chars) | Meta (chars) | H1 | Content words | Issues |
|---|---|---|---|---|---|
{{ONPAGE_TABLE}}

Key on-page findings:

- **Road Code title/offer mismatch (High).** The title is "Free NZ Road Code Practice Test | AA" and the meta says "free AA Road Code practice tests". The page sells 5, 10 or 20-test packs ($12.50 to $20) and offers one free trial test. Rewrite to something like: "NZ Road Code Practice Tests: Free Trial + Test Packs | AA". This lowers pogo-sticking and misleading-snippet risk, and it keeps the `Product` offer consistent with the title.
- **Relative canonical and og:image on all 7 pages (Medium).** The canonical is `/drivers/driving-school/...`. Google resolves relative canonicals, but Lighthouse fails the canonical audit and some crawlers and social scrapers do not resolve them. Emit absolute `https://www.aa.co.nz/...` from the AEM page component.
- **Non-descriptive "Learn more" anchors (Medium).** 4 on the driving-lessons page link to practice-restricted-test, defensive-driving-course, road-code-practice-test and find-a-driving-school. Anchor text is a ranking and AI-parsing signal. Use "Practice restricted test", etc.
- **Icon ligature text leaking into headings (Low).** The global navigation renders Material Symbols ligatures as text, so screen readers, AI parsers and text-mode crawlers read headings like "Membership keyboard_arrow_down". Add `aria-hidden="true"` to icon spans.
- **Heading level skips (Low).** H2 to H4 jumps appear on every page (Lighthouse `heading-order`).
- **No `<main>` landmark (Low).** The template has no `<main>`, which hurts accessibility and the ability of AI agents and reader modes to find the primary content.

## 5. Content Gap Recommendations

{{SECTION:content-gaps}}

{{CHART:07_word_counts.png}}
{{LIST:07_word_counts.png}}

## 6. Technical SEO Checklist (mobile-first)

| Check | Result | Notes |
|---|---|---|
| HTTP status | PASS | 200 on all 7; no redirects |
| Indexability | PASS | No `noindex` meta or X-Robots-Tag |
| robots.txt | PASS (note) | Allows all bots except SemrushBot and FAST Enterprise Crawler. The SemrushBot block means SEMrush site-audit data will always be partial |
| XML sitemap | PASS | All 7 URLs present in /.sitemap.xml (2,595 URLs total, 42 under /drivers/driving-school/) |
| Canonical | WARN | Self-referencing but relative on all 7 |
| Rendering | PASS | Server-rendered; static and rendered DOM match on all 7 |
| Mobile viewport | PASS | `width=device-width`; no horizontal overflow at 390px |
| Tap targets | WARN | 21 to 34 interactive elements under 48px per page, mostly the mega-nav and footer links |
| Font size | PASS | No body text under 12px |
| Crawlable anchors | FAIL (Lighthouse) | JS-only anchors in the nav component |
| HTTPS / mixed content | PASS | |
| hreflang | N/A | Single-locale (en-NZ) site; not required |
| Structured data | WARN | Present on 7/7, but thin (see Schema) |
| Main landmark / semantics | WARN | No `<main>` |
| Page weight (mobile) | FAIL | 3.1 to 4.2 MB |
| Third-party JS | FAIL | GTM (2x GA4), reCAPTCHA, Hotjar, OptinMonster, YouTube |
| Internal links | PASS (note) | Around 340 links per page, about 300 of them the mega-nav; contextual links are few |

## 7. Lighthouse / CWV Results (mobile)

Lighthouse 12.8.2, mobile form factor, simulated slow 4G + 4x CPU throttling, run on **all 7 pages** on 25 Sep 2026. No field data: the PageSpeed Insights/CrUX API returned HTTP 429 (quota) and no API key was available.

**Caveat.** The audit ran in a cloud container behind an HTTPS proxy. That adds round-trip latency and forces HTTP/1.1, which inflates FCP, LCP and Speed Index. Use those three for relative comparison between pages. TBT, CLS, byte weight, DOM size and diagnostics are reliable.

{{LH_TABLE}}

{{CHART:03_lighthouse_scores.png}}
{{LIST:03_lighthouse_scores.png}}

{{CHART:09_lcp_by_page.png}}
{{LIST:09_lcp_by_page.png}}

Main diagnostics, common to all pages:

- **Third-party main-thread cost:** Google Tag Manager about 1.26s main-thread time and 0.8s blocking; Google CDN (reCAPTCHA) about 0.2s blocking; Hotjar and OptinMonster add more.
- **Two GA4 properties** (`G-PNYJZGH4F3`, `G-EMQQPZVZVY`) load through gtag on every page, about 72 KB of unused JS each.
- **reCAPTCHA loads on content pages** with no form above the fold, about 187 KB of unused JS. Load it on form interaction.
- **Render-blocking CSS:** clientlib-site, clientlib-base, clientlib-dependencies and Google Fonts. Estimated saving about 6s under simulated throttling.
- **YouTube iframe** loads eagerly on driving-lessons (about 1 MB). Use a click-to-load facade (`lite-youtube`).
- **Material Symbols font** is among the largest transfers. Subset it to the icons actually used, or switch to inline SVG.
- **CLS 0.13 on defensive-driving-course**, the only page over 0.1. Reserve space for the late-loading location tables and banner.
- **DOM size** 1,506 to 2,336 elements. The mega-nav is about 1,000 words of hidden DOM on every page.

## 8. GBP Audit

**Skipped by instruction.** No Google Business Profile data was collected. Local-pack visibility for "driving lessons [city]" queries (A1 Driving School leads Auckland) should be checked in a separate GBP audit.

## 9. GEO / AI Overview

{{CHART:08_geo_signals.png}}
{{LIST:08_geo_signals.png}}

| Signal | Status | Evidence |
|---|---|---|
| AI crawler access | Good | robots.txt blocks only SemrushBot and FAST; GPTBot, ClaudeBot, PerplexityBot and Google-Extended are allowed |
| llms.txt | Missing | https://www.aa.co.nz/llms.txt returns 404 |
| Question-format headings | Good | 6 of 7 pages have 3 or more question headings (up to 9); hub has 2 |
| Answer-first passages | Partial | FAQ answers are self-contained. Hero intros are marketing copy rather than a 40 to 60 word factual answer |
| Entity clarity | Weak | Two Organization `@id`s; bare Service nodes; no `sameAs` on the parent AA entity on these pages |
| Citable facts | Partial | Pass marks, question counts, prices and course hours are on-page, but not in tables or definition lists that LLMs extract well |
| AI Overview citations | Not measurable | The SERP tool does not expose AIO blocks; no AIO citation was observed or confirmed |
| Agentic browsing | Moderate | Server-rendered content and clear CTAs help. No `<main>`, JS-only nav anchors and ligature text in headings hurt agent parsing. Booking goes to a separate subdomain (drivingschool.aa.co.nz) |

**Agentic Browsing score: 60/100** (rubric: rendered content 20/20, CTA clarity 15/20, semantic landmarks 5/20, link crawlability 10/20, structured facts 10/20).

Recommendations: publish `/llms.txt` listing the key driving-school URLs with one-line descriptions. Add a 50-word "at a glance" answer box under each H1, for example on the learner page: age 16, 35 questions, pass mark 32, fees. Put fees, durations and requirements into HTML tables. Unify the entity `@id` (see Schema).

## 10. Competitor Comparison

Competitors were auto-identified from top-10 overlap across the 7 non-branded NZ queries (SEMrush was unavailable, so SERP overlap stands in for keyword overlap):

| Domain | Queries in top 10 (of 7) | Avg. position | Type | Strength vs AA |
|---|---|---|---|---|
| aa.co.nz | 7 | 1.9 | This site | |
| a1drivingschool.co.nz | 4 | 3.5 | Commercial driving school | #1 for "driving lessons auckland"; dedicated pages for pre-test assessment and full licence |
| drivingtests.co.nz | 4 | 3.8 | Road Code practice platform | #1 for "learner licence test nz"; per-class question banks |
| vtnz.co.nz | 3 | 5.3 | Testing agent | Owns "book test" intent; appears for learner, restricted and full queries |
| nzta.govt.nz / drive.govt.nz | 6 / 5 | 3.7 / 4.8 | Government (informational) | Authoritative source for rules; AA should cite, not compete |

Content benchmark (best competitor page per query): street-talk.co.nz (defensive driving, 3,418 words, 9 H2s covering what, why, how long, cost and benefits), compared with AA's 1,985 words. a1drivingschool.co.nz home (driving lessons, 745 words) compared with AA's 1,251. roadcodepractice.co.nz (road code, 256 words) compared with AA's 1,004. AA leads on depth except for defensive driving, where Street Talk's cost/duration/benefit framing is more complete.

## 11. Page Uniqueness Analysis

{{CHART:06_duplicate_heatmap.png}}

{{SECTION:uniqueness}}

## 12. Schema Recommendations

{{SECTION:schema}}

## 13. Prioritised Action Plan

### Critical
1. **Cut third-party and render-blocking JS on mobile** (all 7). Consolidate to one GA4 property in GTM. Load reCAPTCHA only on form focus. Add a YouTube facade. Defer Hotjar and OptinMonster until after interaction. Subset the Material Symbols font. *Effort: 1 to 2 sprints (front-end + analytics owner).*
2. **Resolve licence-stage cannibalisation** (get-ready-for-learner/restricted/full versus get-*-licence, practice-*-test and /driver-licences/*). Pick one primary URL per stage, then merge or redirect, or rewrite the others to a distinct intent (booking a practice lesson versus a test-day guide). *Effort: 2 to 3 weeks content + SEO; redirects 1 day.*

### High
3. **Fix the Road Code title and meta** so "free" applies only to the trial test. *Effort: 1 hour.*
4. **Win "book restricted/full test" intent (3,600 and 4,400 vol.).** Add a "How to book your test" section with NZTA/VTNZ booking steps and fees to get-ready-for-restricted-test and get-ready-for-full-test. *Effort: 2 to 3 days.*
5. **Fix CLS on defensive-driving-course (0.13).** Reserve height for the location tables and banner. *Effort: 1 to 2 days.*
6. **Strengthen defensive-driving-course against Street Talk.** Add a cost/duration/outcome summary table, a time-saving explainer (restricted to full, 18 months down to 12, as the page states), and location pages or anchors. *Effort: 3 to 5 days.*

### Medium
7. **Absolute canonical and og:image URLs** in the AEM page component (all 7). *Effort: 0.5 day + regression test.*
8. **Schema programme, phase 1:** unify the Organization `@id`, add BreadcrumbList on the template, and add FAQPage where Q&As are visible. *Effort: 1 to 2 sprints incl. QA and governance; see Schema.*
9. **Descriptive anchor text** instead of "Learn more" (driving-lessons, hub). *Effort: 2 hours.*
10. **Answer-first intro boxes + fact tables** on the 3 get-ready pages and the hub (GEO). *Effort: 3 to 4 days.*
11. **Publish `/llms.txt`.** *Effort: 0.5 day.*
12. **Expand get-ready-for-full-test (635 words) and the hub (591 words)** with eligibility timelines, fees and a stage chooser. *Effort: 2 to 3 days.*

### Low
- **Watch item:** beehive.govt.nz "changes to driver licensing system announced" ranks for "full licence test nz". Check that the get-ready and defensive-driving pages reflect the current and announced licensing rules, since stale rules would hurt both rankings and trust.
13. `aria-hidden` on icon ligature spans; add a `<main>` landmark; fix heading-order skips. *Effort: 1 to 2 days (template).*
14. Increase tap-target size and spacing in the mega-nav and footer for mobile. *Effort: 1 to 2 days.*
15. Schema programme, phase 2: Course + CourseInstance per location, Service `hasOfferCatalog` with lesson prices. *Effort: 2 to 3 sprints.*
16. Review the SemrushBot block if SEMrush site-audit data is wanted for future audits.

## Appendices

Appendix A (Data Sources and Coverage) and Appendix B (Action Lists) are in `DATA-SOURCES-AND-ACTION-LISTS.md`, generated by `gen_sources_lists.py`. Appendix C (original prompt and run record) is in `APPENDIX-C-ORIGINAL-PROMPT.md`. All three are embedded in the DOCX.

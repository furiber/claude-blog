# Content Gap Recommendations

Date: 2026-09-25. Scope: 7 AA Driving School pages, compared against `raw/serp.json`
competitor pages, `siblings.json` (same-intent AA pages outside the audited set), and
`dupes.json` (text-similarity pairs).

## Word count vs top competitor

Only 3 of the 7 in-scope pages have a matched competitor page in
`serp.json:competitor_pages`; the get-ready pages and the hub compete against
government pages and AA's own siblings rather than third-party competitors (see the
cannibalisation map below).

| Page | AA word count | Top competitor page | Competitor word count | Gap |
|---|---|---|---|---|
| driving-lessons | 1,251 | a1drivingschool.co.nz (pos 1-2 for "driving lessons nz"/"driving lessons auckland") | 745 | AA is already ~1.7x longer; the gap is not length, it is E-E-A-T depth (see below) |
| defensive-driving-course | 1,985 | street-talk.co.nz (pos 3 for "defensive driving course nz") | 3,418 | AA is under 60% of competitor depth despite outranking it (position 1 vs 3); this is a depth risk, not yet a ranking problem |
| road-code-practice-test | 1,004 | roadcodepractice.co.nz (pos 2 for "road code practice test nz") | 256 | AA is already ~4x longer and comprehensive; no length gap |

## Missing subtopics vs competitor H2s and SERP intent

**driving-lessons vs a1drivingschool.co.nz** (H2s: "Our Fleet of Cars for Training",
"Our Team of Instructors", "What our clients say"): AA's page has generic trust
badges ("Trusted nationwide", "Expert Instructors") and three short regional
testimonial blocks (Wellington, Auckland, Christchurch), but no dedicated fleet
section (vehicle makes/models, dual-control camera specifics beyond a single trust
badge) and no named/credentialed instructor bios. Given this is driver-training
content close to a safety/YMYL-adjacent category, named instructor credentials and
concrete fleet detail are the E-E-A-T subtopics competitors are covering that AA is
not.

**defensive-driving-course vs street-talk.co.nz** (H2s include "Why Us?", "How Much
Does It Cost?", "Benefits of Street Talk Course", "Find a provider nearest you"):
AA covers the equivalent ground for "find a provider" (its ~24-row location tables)
and "how long" (the "9 hours" H2), but has no explicit head-to-head "why choose AA"
comparison section, and its "Cost & booking" H2 does not clearly headline a price
the way the competitor's dedicated "How Much Does It Cost?" H2 does. At under 60%
of the competitor's word count, AA is thinner on exactly the persuasion content
(benefits, differentiation, cost transparency) that a competitor ranking below it
is using to close the gap.

**road-code-practice-test vs roadcodepractice.co.nz**: no material subtopic gap;
AA's headings ("Real test-style questions", "Track your progress", "Practice
anywhere", 8 FAQs) already cover more ground than the competitor's 4 H2s. The open
issue for this page is the title/offer inconsistency and SERP cannibalisation
covered in schema.md and the map below, not missing content.

**get-ready-for-learner-test / get-ready-for-restricted-test / get-ready-for-full-test
vs SERP intent**: no third-party competitor pages are matched for these queries;
the pages that outrank or compete with them are NZTA/drive.govt.nz government pages
(e.g. `nzta.govt.nz/driver-licences/sit-a-driving-test/practical-tests` for
"restricted licence test practice nz", `nzta.govt.nz/.../full-licence-practical-
driving-test` at position 1 for "full licence test nz") and AA's own sibling pages.
Subtopics present on the authoritative gov pages that are thin or missing on AA's
get-ready pages:
- Explicit test fee and what payment methods are accepted (none of the three
  get-ready pages headline a fee/cost subtopic)
- An explicit ID/documents checklist as its own subtopic (learner and restricted
  pages fold this into prose under "What to bring on the day" / "Before you book
  your test" without a dedicated heading; full-test page has no equivalent heading
  at all)
- Common faults / what causes a fail: present on get-ready-for-restricted-test
  ("Common faults to avoid": failing to look, rolling through stops, speed, lane
  position/signalling) but entirely absent from get-ready-for-full-test, which is
  also the shortest and thinnest of the three (635 words, 1 FAQ)
- Direct citation of or link to the NZTA official source for eligibility/timeframe
  rules: strengthens E-E-A-T for YMYL-adjacent licensing content and gives AI/LLM
  answer engines an authoritative anchor to cite alongside AA (GEO/AEO value)

## Intent cannibalisation map

Grouped by licence stage, listing every AA URL (in-scope audit pages plus
`siblings.json` pages) competing for that stage's intent.

### Learner stage
- In scope: `get-ready-for-learner-test/` (904 words), `road-code-practice-test/`
  (1,004 words)
- Siblings: `get-learner-licence/` (428 words), `road-code/` (398 words),
  `driver-licences/learner-driver-licences/` (632 words)
- SERP fact: `road-code-practice-test/` ranks position 2 for "learner licence test
  nz", ahead of `get-ready-for-learner-test/`, which does not appear in that SERP at
  all.
- **Recommended primary URL: `road-code-practice-test/`** for theory-test-practice
  intent, since it already ranks and carries transactional Product schema.
  **Action:** differentiate rather than merge. Keep `get-ready-for-learner-test/`
  focused on pre-test logistics (booking, eyesight check, what to bring, what
  happens after you pass) and have it link into `road-code-practice-test/` for the
  practice-test itself instead of re-explaining Road Code content. Fold `road-code/`
  (398 words, the thinnest sibling, studying the physical Road Code) into
  `road-code-practice-test/` as a subsection or a clearly-differentiated "study the
  book" vs "practice online" split; as a standalone 398-word page it is a
  consolidation candidate. `get-learner-licence/` and `learner-driver-licences/`
  should stay as the top-of-funnel "about the learner licence" overview, distinct
  from both test-prep pages.

### Restricted stage
- In scope: `get-ready-for-restricted-test/` (1,079 words)
- Siblings: `get-restricted-licence/` (460 words), `practice-restricted-test/`
  (596 words)
- SERP fact: `practice-restricted-test/` ranks position 1 for "restricted licence
  test practice nz"; `get-ready-for-restricted-test/` does not appear in that SERP.
- **Recommended primary URL: `practice-restricted-test/`** for the
  practice/booking-a-mock-test intent, since it already holds position 1.
  **Action:** keep `get-ready-for-restricted-test/` as the test-day
  logistics/common-faults reference page (its strongest existing content) and add a
  clear internal link from it to `practice-restricted-test/` for booking an actual
  practice lesson, rather than both pages competing loosely for the same "practice
  for restricted test" query. `get-restricted-licence/` remains the top-of-funnel
  "how do I get a restricted licence" overview.

### Full stage
- In scope: `get-ready-for-full-test/` (635 words, weakest page in the audited set)
- Siblings: `get-full-licence/` (436 words), `practice-full-test/` (610 words),
  `driver-licences/full-driver-licences/` (686 words)
- SERP fact: `driver-licences/full-driver-licences/` ranks position 4 for "full
  licence test nz"; `get-ready-for-full-test/` does not appear in that SERP.
- **Recommended primary URL: `driver-licences/full-driver-licences/`** for the
  broad "full licence test nz" query, since it already ranks and is the deepest
  full-licence page AA has (686 words).
  **Action:** `get-ready-for-full-test/` is the thinnest and highest-cannibalisation-
  risk page in this audit (21.5% content containment with
  `get-ready-for-restricted-test/`, its own get-ready sibling — see uniqueness table
  below). Rather than letting it keep competing loosely against three other AA URLs
  for the same stage, expand it with unique full-test-specific content it currently
  lacks (a common-faults section like the restricted page has, an explicit
  eligibility/timeframe subtopic, more than its single FAQ) so it earns a distinct
  "day of test" role, and treat `driver-licences/full-driver-licences/` as the
  "about the full licence" hub it already ranks as. If differentiation content
  cannot be produced, consolidating `get-ready-for-full-test/` into
  `practice-full-test/` or `full-driver-licences/` with a 301 is the lower-risk
  option given how thin and templated it currently is.

## Page Uniqueness Analysis

"Max similarity to another in-scope page" and "max similarity to a sibling" use the
containment percentage from `dupes.json` (5-word shingle containment on
content-only rendered text), taking each page's single highest match.

| Page | Content words | Max similarity to another in-scope page | Max similarity to a sibling | Cannibalisation risk | Thin? | Verdict |
|---|---|---|---|---|---|---|
| Hub (`/drivers/driving-school/`) | 591 | 14.7% (driving-lessons/) | 2.4% (practice-restricted-test/) | Low — a hub page is expected to echo its children's content; flagged `thin_content` by the crawler in its own right, which is the real issue here | Yes (crawler-flagged) | Thin for a page carrying Organization + CollectionPage + FAQPage schema; expand hub-level guidance rather than treat the overlap with driving-lessons as duplication |
| driving-lessons | 1,251 | 14.7% (hub) | 4.1% (practice-restricted-test/) | Low — overlap with the hub is expected summarisation, not competition for the same query | No | Healthy length and depth; the open issue is missing E-E-A-T subtopics (fleet, instructor bios), not duplication |
| defensive-driving-course | 1,985 | 15.0% (get-ready-for-full-test/) | 1.8% (get-full-licence/) | Low-Medium — the overlap with get-ready-for-full-test reflects shared promotional copy ("cut your wait with a Defensive Driving Course") rather than two pages competing for the same query, but it is worth trimming that repeated block to one canonical location | No | Solid depth relative to its own query but under 60% of its top competitor's word count; expand persuasion/cost-transparency content |
| road-code-practice-test | 1,004 | 13.7% (hub) | 2.6% (road-code/) | High for keyword/intent reasons even though text similarity is low: this page ranks for "learner licence test nz" instead of get-ready-for-learner-test (see cannibalisation map) | No | Strong page on its own content merits; the risk is intent overlap with two other AA URLs, not duplicate text |
| get-ready-for-learner-test | 904 | 13.9% (hub) | 3.6% (road-code/) | High for keyword/intent reasons: outranked in its own target query by road-code-practice-test, and shares thin-sibling overlap with road-code/ | No | Needs differentiation (logistics/eyesight/what-to-bring focus) rather than more Road Code content, per the cannibalisation map |
| get-ready-for-restricted-test | 1,079 | 21.5% (get-ready-for-full-test/) — highest in-scope containment in this audit | 2.6% (get-learner-licence/) | High: highest text-similarity pair of any two in-scope pages, and outranked in its own target query by sibling practice-restricted-test/ | No | Best-developed of the three get-ready pages (common faults, FAQ depth); still needs its templated boilerplate (the 21.5% shared block) trimmed against get-ready-for-full-test |
| get-ready-for-full-test | 635 | 21.5% (get-ready-for-restricted-test/) — highest in-scope containment in this audit | 3.4% (practice-full-test/) | High: same highest-containment pair as above, outranked in its own target query by sibling full-driver-licences/, and the shortest page with only 1 FAQ | Borderline (not crawler-flagged, but weakest word count and heading depth of the audited set) | Weakest page in the audit; either substantially differentiate (common faults, eligibility timeframe, more FAQs) or consolidate into practice-full-test/ or full-driver-licences/ |

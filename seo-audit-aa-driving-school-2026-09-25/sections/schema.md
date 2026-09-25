# Schema Recommendations

Date: 2026-09-25. Scope: 7 AA Driving School pages (hub, driving-lessons,
defensive-driving-course, road-code-practice-test, get-ready-for-learner-test,
get-ready-for-restricted-test, get-ready-for-full-test).

Schema work here is a strategic investment, not a quick win. Every recommendation
below carries a realistic effort estimate and its dependencies. None of this should be
scheduled as a single sprint ticket; it is a program across templating, content ops,
and governance.

## Coverage table

| Page | Current JSON-LD types | Recommended types | Gap |
|---|---|---|---|
| Hub (`/drivers/driving-school/`) | Organization, CollectionPage, FAQPage | + BreadcrumbList; Organization becomes the single canonical `#organization` node | No BreadcrumbList despite a visible breadcrumb nav; hub's Organization `@id` conflicts with the `@id` every sub-page's Service references |
| driving-lessons | Bare Service (name, serviceType, provider, areaServed "NZ", url) | Service + `hasOfferCatalog`/`offers`, BreadcrumbList, FAQPage | No price data despite 5 visible lesson-package headings; no FAQPage despite a "Common questions" section with 6 real Q&As; no BreadcrumbList |
| defensive-driving-course | Minimal Course + one generic CourseInstance (`courseMode: onsite`, address country NZ only) | Course with `timeRequired: PT9H`, one CourseInstance per real centre (Place with street address), offers, BreadcrumbList, FAQPage | Page lists ~24 course locations in tables (Area / Street address) but schema declares exactly one placeless instance; no duration; no price; no FAQPage despite 5 visible FAQs; no BreadcrumbList |
| road-code-practice-test | Product + AggregateOffer (NZD 12.50-20.00, 3 packs) + bare Service | Keep Product/Offer, fix title/offer inconsistency, add BreadcrumbList, FAQPage (8 visible Qs) | Title says "Free NZ Road Code Practice Test" but only the trial test is free; the free tier is absent from the AggregateOffer; no FAQPage; no BreadcrumbList |
| get-ready-for-learner-test | Bare Service ("Get Ready for Learner Test", Driver education) | WebPage (about/mentions) + FAQPage (6 Qs), BreadcrumbList | Service is the wrong type for an informational/how-to page; no FAQPage despite 6 visible Qs; no BreadcrumbList |
| get-ready-for-restricted-test | Bare Service | WebPage + FAQPage (7 Qs), BreadcrumbList | Same Service-type mismatch; no FAQPage despite 7 visible Qs; no BreadcrumbList |
| get-ready-for-full-test | Bare Service | WebPage + FAQPage (1 Q, thin) | Same Service-type mismatch; only 1 visible FAQ on this page (a content gap in its own right, see content-gaps.md); no BreadcrumbList |

Site-wide issue underneath all seven rows: sub-pages set `provider.@id` to
`https://www.aa.co.nz/#organization` (the parent NZAA entity), while the hub defines a
*different* entity, `https://www.aa.co.nz/drivers/driving-school/#organization`
(AA Driving School, with NZAA as `parentOrganization`). Neither Google nor an LLM
crawler can safely infer that "AA Driving School" is the actual service provider on
six of seven pages when the schema on those pages points at the parent brand instead.

## Effort and sequencing

| Initiative | Effort | Work involved | Dependencies |
|---|---|---|---|
| 1. Organization entity reconciliation | 0.5-1 dev day + 0.5 day content/brand sign-off | Decide the single canonical provider entity (recommend AA Driving School, not parent NZAA), update the shared AEM Organization component, redeploy across all 7 templates | Brand/legal confirms which entity should be the customer-facing "provider" of record |
| 2. BreadcrumbList (all 7 pages) | 1-2 dev days + 0.5 day QA | Breadcrumb nav already renders visible items; wire the existing breadcrumb component's data model to also emit JSON-LD via the AEM Sling model/HTL template | None; lowest-risk, highest-ROI item here |
| 3. Course + multi-CourseInstance for defensive-driving-course | 3-5 dev days + governance | The ~24 centres currently live only as an HTML table, not structured data. Needs a CMS-backed location list (ideally reused by a locations component elsewhere on site) that a Sling model can loop over to emit one CourseInstance per centre; QA against Google's Course structured-data guidelines; ongoing governance so schema tracks the table when centres are added/removed | A CMS/content-ops decision to model driving-school locations as structured data, not free-text table rows; pricing input for `{{PRICE}}` per instance |
| 4. Product/Offer fix + title consistency for road-code-practice-test | 0.5 dev day + marketing copy sign-off | Add the free trial as an explicit `$0.00` Offer (or drop "Free" from the title/meta if the team prefers not to touch AggregateOffer's `lowPrice`); rewrite title tag to match whichever option is chosen | Marketing decision on how the free-trial claim should read in the title/meta, since schema and on-page copy must stay in sync |
| 5. Service + `hasOfferCatalog` for driving-lessons | 1-2 dev days | Page already lists 5 lesson-package names in H3s; needs live prices sourced from the booking system rather than hardcoded, or the schema will drift stale (a known Google Merchant/price-accuracy risk) | A pricing feed or manual sync process; without one, ship with `{{PRICE}}` placeholders and flag as v2 |
| 6. FAQPage on driving-lessons, defensive-driving-course, road-code-practice-test, and all 3 get-ready pages | 0.5-1 dev day per template (can share one Sling component) + QA to confirm each question's on-page answer text matches what goes into `acceptedAnswer` | Extract the real visible Q&A headings (already in the DOM) into the FAQPage `mainEntity`; a shared component avoids 6x duplicated logic | Content ops needs a single source of truth for FAQ copy so schema doesn't fall out of sync when marketing edits an answer. Note: since 2023 Google restricts FAQ rich results to authoritative gov/health sites, so this delivers no rich-snippet real estate; the return here is entity clarity for AI/LLM parsing (GEO/AEO), not SERP snippets |
| 7. WebPage/about+mentions in place of bare Service on the 3 get-ready pages | 1 dev day per template | Swap the incorrect Service type for WebPage with `about`/`mentions` pointing at the relevant licence-stage entities, combined with the FAQPage from item 6 in one `@graph` | Item 1 (canonical Organization @id) should land first so `about`/`publisher` references resolve to the right entity |

Recommended sequencing: (1) Organization reconciliation and (2) BreadcrumbList first,
since they are cheap, site-wide, and everything else references the same
Organization `@id`. Then (6) FAQPage and (7) WebPage swap on the get-ready pages,
since the content already exists. (4) Product/Offer fix next since it is mostly a
copy decision. (5) Service offers and (3) Course/CourseInstance are the largest
lifts and should be scheduled as their own workstreams with content-ops involvement,
not bundled into a general "schema cleanup" ticket.

**Important caveat on `@id` references:** Google evaluates each page's structured
data independently and does not reliably merge JSON-LD across separate page fetches.
Sharing one `@id` string across pages keeps entities identifiable as "the same thing"
to a knowledge graph or an LLM that reads several pages, but each page should still
repeat the entity's core properties (name, url) rather than relying purely on an
empty `{"@id": "..."}` reference resolving from another URL.

---

## Templates

### 1. Site-wide Organization entity reconciliation (single @id strategy)

Canonical entity, defined in full on the hub (and repeated in full, not just by
reference, on every sub-page that needs a provider):

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://www.aa.co.nz/drivers/driving-school/#organization",
  "name": "AA Driving School",
  "alternateName": "AA Driving School New Zealand",
  "url": "https://www.aa.co.nz/drivers/driving-school/",
  "description": "AA Driving School provides driving lessons, mock practice tests and defensive driving courses across New Zealand, with NZTA-qualified instructors and dual-control vehicles.",
  "areaServed": { "@type": "Country", "name": "New Zealand" },
  "parentOrganization": {
    "@type": "Organization",
    "@id": "https://www.aa.co.nz/#organization",
    "name": "New Zealand Automobile Association",
    "alternateName": "AA New Zealand",
    "url": "https://www.aa.co.nz/"
  },
  "sameAs": [
    "https://www.facebook.com/AADrivingSchoolNZ",
    "https://www.instagram.com/aadrivingschoolnz",
    "https://nz.linkedin.com/company/aa-driving-school"
  ]
}
```

On every sub-page (driving-lessons, defensive-driving-course, road-code-practice-test,
the 3 get-ready pages), replace the current:

```jsonc
"provider": {
  "@type": "Organization",
  "@id": "https://www.aa.co.nz/#organization",
  "name": "New Zealand Automobile Association",
  "url": "https://www.aa.co.nz/"
}
```

with a reference to the driving-school entity, repeating its own properties, not
the parent's:

```jsonc
"provider": {
  "@type": "Organization",
  "@id": "https://www.aa.co.nz/drivers/driving-school/#organization",
  "name": "AA Driving School",
  "url": "https://www.aa.co.nz/drivers/driving-school/"
}
```

### 2. BreadcrumbList

Per-page example (get-ready-for-restricted-test):

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.aa.co.nz/" },
    { "@type": "ListItem", "position": 2, "name": "Drivers", "item": "https://www.aa.co.nz/drivers/" },
    { "@type": "ListItem", "position": 3, "name": "AA Driving School", "item": "https://www.aa.co.nz/drivers/driving-school/" },
    { "@type": "ListItem", "position": 4, "name": "Get ready for your restricted licence test", "item": "https://www.aa.co.nz/drivers/driving-school/get-ready-for-restricted-test/" }
  ]
}
```

AEM template pattern: the visible breadcrumb component already holds this exact
list (title + absolute URL per crumb); the JSON-LD is a straight loop over the
same model, not a new data source:

```jsonc
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    /* HTL: data-sly-list.crumb="${breadcrumbModel.items}" */
    { "@type": "ListItem", "position": "{{crumb.index_plus_1}}", "name": "{{crumb.title}}", "item": "{{crumb.absoluteUrl}}" }
    /* /data-sly-list */
  ]
}
```

### 3. Enhanced Course + multiple CourseInstance (defensive-driving-course)

```jsonc
{
  "@context": "https://schema.org",
  "@type": "Course",
  "@id": "https://www.aa.co.nz/drivers/driving-school/defensive-driving-course/#course",
  "name": "AA Defensive Driving Course",
  "description": "Build safer driving habits with the AA Defensive Driving Course. Learn practical skills, grow confidence and prepare for the next stage of licensing.",
  "provider": {
    "@type": "Organization",
    "@id": "https://www.aa.co.nz/drivers/driving-school/#organization",
    "name": "AA Driving School",
    "url": "https://www.aa.co.nz/drivers/driving-school/"
  },
  "url": "https://www.aa.co.nz/drivers/driving-school/defensive-driving-course/",
  "timeRequired": "PT9H",
  "hasCourseInstance": [
    {
      "@type": "CourseInstance",
      "courseMode": "onsite",
      "location": {
        "@type": "Place",
        "name": "Kerikeri",
        "address": {
          "@type": "PostalAddress",
          "streetAddress": "Kerikeri High School, 48 Hone Heke Road",
          "addressLocality": "Kerikeri",
          "addressCountry": "NZ"
        }
      },
      "offers": {
        "@type": "Offer",
        "price": "{{PRICE}}",
        "priceCurrency": "NZD",
        "availability": "https://schema.org/InStock",
        "url": "https://www.aa.co.nz/drivers/driving-school/defensive-driving-course/"
      }
    },
    {
      "@type": "CourseInstance",
      "courseMode": "onsite",
      "location": {
        "@type": "Place",
        "name": "Whangarei",
        "address": {
          "@type": "PostalAddress",
          "streetAddress": "24 Finlayson Street, Whangarei (Room 3)",
          "addressLocality": "Whangarei",
          "addressCountry": "NZ"
        }
      },
      "offers": {
        "@type": "Offer",
        "price": "{{PRICE}}",
        "priceCurrency": "NZD",
        "availability": "https://schema.org/InStock",
        "url": "https://www.aa.co.nz/drivers/driving-school/defensive-driving-course/"
      }
    }
    /* Repeat one CourseInstance per row of the existing Area / Street address
       tables (~24 centres across Northland, Auckland, Waikato, Bay of Plenty,
       Hawke's Bay, Manawatu-Whanganui, Wairarapa, Wellington,
       Marlborough + Tasman, Canterbury, Otago). Do not hand-maintain this
       array: generate it from the same location dataset that feeds the
       visible tables, or the two will drift apart. */
  ]
}
```

### 4. Product/Offer fix for Road Code tests (+ title/offer consistency)

Current AggregateOffer omits the free trial that the title advertises. Two valid
fixes; pick one and make the title match it:

**Option A** — add the free trial as an explicit Offer and adjust `lowPrice`:

```json
{
  "@type": "Product",
  "name": "AA Road Code Practice Tests",
  "description": "NZ Road Code practice tests for the learner licence theory test, including the latest NZTA Road Code update. Try one free, or buy a 5, 10 or 20-test pack.",
  "brand": { "@type": "Brand", "name": "AA (New Zealand Automobile Association)" },
  "offers": {
    "@type": "AggregateOffer",
    "priceCurrency": "NZD",
    "lowPrice": "0.00",
    "highPrice": "20.00",
    "offerCount": 4,
    "availability": "https://schema.org/InStock",
    "url": "https://www.aa.co.nz/drivers/driving-school/road-code-practice-test/",
    "offers": [
      { "@type": "Offer", "name": "Free trial test", "price": "0.00", "priceCurrency": "NZD", "availability": "https://schema.org/InStock" },
      { "@type": "Offer", "name": "Basic - 5 tests", "price": "12.50", "priceCurrency": "NZD", "availability": "https://schema.org/InStock" },
      { "@type": "Offer", "name": "Value - 10 tests", "price": "15.00", "priceCurrency": "NZD", "availability": "https://schema.org/InStock" },
      { "@type": "Offer", "name": "Super Saver - 20 tests", "price": "20.00", "priceCurrency": "NZD", "availability": "https://schema.org/InStock" }
    ]
  }
}
```

**Option B** — leave the paid AggregateOffer (12.50-20.00) untouched and instead
retitle the page so schema and title agree without touching pricing structure, e.g.
"NZ Road Code Practice Tests: Free Trial + Paid Packs from $12.50 | AA" in place of
the current "Free NZ Road Code Practice Test | AA". This is the lower-effort,
lower-risk fix and is the one this audit recommends; it is a copy change, not a
schema or `AggregateOffer` restructure.

### 5. Service with offers/hasOfferCatalog for driving lessons

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "AA Driving Lessons",
  "serviceType": "Driver training",
  "provider": {
    "@type": "Organization",
    "@id": "https://www.aa.co.nz/drivers/driving-school/#organization",
    "name": "AA Driving School",
    "url": "https://www.aa.co.nz/drivers/driving-school/"
  },
  "areaServed": "NZ",
  "url": "https://www.aa.co.nz/drivers/driving-school/driving-lessons/",
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "AA Driving Lesson Packages",
    "itemListElement": [
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "1 hr Starter Lesson" }, "price": "{{PRICE}}", "priceCurrency": "NZD" },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "1 hr Driving Lesson" }, "price": "{{PRICE}}", "priceCurrency": "NZD" },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "5 lesson package" }, "price": "{{PRICE}}", "priceCurrency": "NZD" },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Practice restricted or full licence test" }, "price": "{{PRICE}}", "priceCurrency": "NZD" },
      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Senior Driver Coaching Session" }, "price": "{{PRICE}}", "priceCurrency": "NZD" }
    ]
  }
}
```

### 6. FAQPage for pages with visible Q&As

**driving-lessons** ("Common questions" section, 6 real questions on the page):

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    { "@type": "Question", "name": "Should I get professional driving lessons?", "acceptedAnswer": { "@type": "Answer", "text": "{{ANSWER_TEXT}}" } },
    { "@type": "Question", "name": "How many lessons will I need?", "acceptedAnswer": { "@type": "Answer", "text": "{{ANSWER_TEXT}}" } },
    { "@type": "Question", "name": "How do I book a driving lesson?", "acceptedAnswer": { "@type": "Answer", "text": "{{ANSWER_TEXT}}" } },
    { "@type": "Question", "name": "How can I reschedule driving lesson?", "acceptedAnswer": { "@type": "Answer", "text": "{{ANSWER_TEXT}}" } },
    { "@type": "Question", "name": "How can I cancel a driving lesson?", "acceptedAnswer": { "@type": "Answer", "text": "{{ANSWER_TEXT}}" } },
    { "@type": "Question", "name": "Can I get a refund for my unused credits?", "acceptedAnswer": { "@type": "Answer", "text": "{{ANSWER_TEXT}}" } }
  ]
}
```

**defensive-driving-course** (5 questions):

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    { "@type": "Question", "name": "What's the best defensive driving course in New Zealand?", "acceptedAnswer": { "@type": "Answer", "text": "{{ANSWER_TEXT}}" } },
    { "@type": "Question", "name": "Is the AA Defensive Driving Course worth it?", "acceptedAnswer": { "@type": "Answer", "text": "{{ANSWER_TEXT}}" } },
    { "@type": "Question", "name": "When should I take a defensive driving course?", "acceptedAnswer": { "@type": "Answer", "text": "{{ANSWER_TEXT}}" } },
    { "@type": "Question", "name": "What do you learn in a defensive driving course?", "acceptedAnswer": { "@type": "Answer", "text": "{{ANSWER_TEXT}}" } },
    { "@type": "Question", "name": "How do I book an AA Defensive Driving Course?", "acceptedAnswer": { "@type": "Answer", "text": "{{ANSWER_TEXT}}" } }
  ]
}
```

**road-code-practice-test** (8 questions; apply the same `mainEntity` pattern with):
"How do I pass my learner licence theory test?", "Where can I practice the NZ
learner licence theory test online?", "What's the best Road Code practice test in
New Zealand?", "Do I need to create a login for the Road Code Practice Test?",
"Are Road Code Practice Tests worth it?", "Which Road Code practice test is closest
to the real learner licence test", "I have used some tests but didn't finish them.
How do I access them?", "Who do I contact if I'm having trouble redeeming my
voucher?".

**get-ready-for-restricted-test** (7 questions, full example since it has the
richest FAQ set of the three get-ready pages):

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    { "@type": "Question", "name": "How do I prepare for my restricted driving test?", "acceptedAnswer": { "@type": "Answer", "text": "{{ANSWER_TEXT}}" } },
    { "@type": "Question", "name": "Can I take a practice restricted driving test before the real one?", "acceptedAnswer": { "@type": "Answer", "text": "{{ANSWER_TEXT}}" } },
    { "@type": "Question", "name": "How do I get my restricted licence in New Zealand?", "acceptedAnswer": { "@type": "Answer", "text": "{{ANSWER_TEXT}}" } },
    { "@type": "Question", "name": "What happens during the restricted licence driving test?", "acceptedAnswer": { "@type": "Answer", "text": "{{ANSWER_TEXT}}" } },
    { "@type": "Question", "name": "What are the most common reasons people fail the restricted test?", "acceptedAnswer": { "@type": "Answer", "text": "{{ANSWER_TEXT}}" } },
    { "@type": "Question", "name": "Who runs the practical test?", "acceptedAnswer": { "@type": "Answer", "text": "{{ANSWER_TEXT}}" } },
    { "@type": "Question", "name": "What if I don't pass?", "acceptedAnswer": { "@type": "Answer", "text": "{{ANSWER_TEXT}}" } }
  ]
}
```

**get-ready-for-learner-test** follows the same pattern with 6 questions: "How old
do I need to be to sit the learner test?", "How many questions are there and what's
the pass mark?", "Can I book the test online or over the phone?", "Is there an
eyesight test?", "What happens if I don't pass?", "What will I get if I pass?".

**get-ready-for-full-test** currently exposes only 1 visible FAQ ("How do I prepare
for my full driving test?"). A single-question FAQPage is technically valid but is
a symptom of thin FAQ content on that page; see content-gaps.md for the
recommendation to add more Q&As before shipping this schema, rather than shipping
FAQPage with one entry.

Note on value: Google restricted FAQ rich results to authoritative gov/health
sites in August 2023, so none of the above earns a SERP snippet. The value here is
entity clarity for AI/LLM parsing (GEO/AEO), where FAQPage remains a strong signal
for how assistants extract and cite Q&A content.

### 7. WebPage/HowTo-alternative guidance for get-ready pages

HowTo rich results were deprecated by Google; do not build HowTo markup for these
pages even though they read as step-by-step guidance. Use WebPage with `about` and
`mentions`, paired with the FAQPage above in the same `@graph`, in place of the
current bare Service:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebPage",
      "@id": "https://www.aa.co.nz/drivers/driving-school/get-ready-for-restricted-test/#webpage",
      "name": "Get ready for your restricted licence test",
      "url": "https://www.aa.co.nz/drivers/driving-school/get-ready-for-restricted-test/",
      "isPartOf": { "@id": "https://www.aa.co.nz/#website" },
      "about": { "@id": "https://www.aa.co.nz/drivers/driving-school/#organization" },
      "publisher": { "@id": "https://www.aa.co.nz/#organization" },
      "mentions": [
        { "@type": "Thing", "name": "Restricted driver licence (New Zealand)" },
        { "@type": "Thing", "name": "Practical driving test" }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [ "...as above..." ]
    }
  ]
}
```

Apply the same WebPage + FAQPage pattern (swapping `mentions` and question lists)
to get-ready-for-learner-test and get-ready-for-full-test. This also resolves the
Service-type mismatch flagged in the coverage table: these are informational/how-to
pages, not separately bookable services, and marking them as Service creates a
confusing entity signal for both classic SEO parsers and LLM crawlers.

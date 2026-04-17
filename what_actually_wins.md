# What Actually Wins — Strategy Memo

*Honest take on where to spend the remaining hours. Written as a
forcing function: before building anything else, re-read this.*

---

## TL;DR

1. **Do NOT build a full-stack Node/React app.** It's the single most
   expensive mistake a team could make in this competition.
2. **DO build a Streamlit interactive matrix + a GitHub Pages
   landing page** — together ~10 hours of work, zero demo risk,
   massive perception uplift.
3. **The real prize is polish in 7 things you already have in draft.**
   Listed in §3.

---

## 1.  Why not a full-stack web app

Judged on deliverables. The rubric is explicit (Workshop 1 slide 9):

1. Context & selection
2. Scoring methodology
3. The matrix
4. Strategic roadmap

A Node + React full-stack is not on the list. Effort spent there is
effort taken from the things on the list.

**Concrete cost–risk:**

| Factor | Full-stack Node/React | Streamlit + GitHub Pages |
|---|---|---|
| Realistic time cost | 40–80 hours for polish | 8–12 hours |
| Deploy / infra risk | DNS, HTTPS, hosting, cold-start | Streamlit Community Cloud (free) or local |
| Demo failure risk on pitch day | High (network, auth, backend) | Very low (static + simple) |
| Perception uplift at the jury | Minimal — they grade the argument | Large — one QR code, interactive matrix on screen |
| What you'd cut to do it | Report polish, rehearsals, Real Options refinement | Almost nothing |

**The asymmetric calculus:** the upside from a working full-stack
app is modest (judges will politely say *"cool"*), the downside from
a broken one is catastrophic (*"they spent their time on this?"*).

## 2.  The sweet spot — what we DO build

### 2.1  Streamlit dashboard (scaffolded — see `07_streamlit/`)
- Single Python file. Reads our existing `mc_results.csv`,
  `coverage_matrix.csv`, and `matrix_inputs.py`.
- Exposes 3 interactive sliders: stakeholder-weight scheme, perturb
  magnitude, and a per-topic CAPEX sensitivity.
- Matrix ellipses redraw live. ESRS gap heatmap on another tab.
  Short-list rationale on a third.
- Deployed to Streamlit Community Cloud (free). Private URL →
  QR code on the deck.
- Fallback: export as static HTML and put on GitHub Pages.

### 2.2  GitHub Pages landing site
- Single-page Jekyll or Hugo site at `ma731.github.io/aqualia-datathon`.
- Sections: Executive summary · Matrix · Methodology · Roadmap ·
  Artefacts (linked Streamlit, heatmap, CSVs).
- Same QR code or short URL points here.

### 2.3  That's it for the tech stack
No backend. No database. No authentication. No custom UI components.
Every hour saved goes to substance.

## 3.  Where the real wins live — substance-tier items

These are the items judges remember and reward. Prioritise in this
order.

### 3.1 Rehearse the 5-minute pitch to muscle memory
- Minimum **6 full rehearsals**, 3 of them recorded and watched back.
- Timer strict: 5:00 sharp, hitting the €-denominated close on
  4:45–5:00.
- Have one teammate play the cynical jury member: challenge the
  weakest assumption each rehearsal.
- **Expected uplift:** huge. This alone differentiates winning teams.

### 3.2 One expert quote
- **One 15-min LinkedIn call** with a water-utility sustainability
  lead — Severn Trent (UK CSRD-adjacent), Veolia, or a European
  consultancy like ERM / South Pole.
- Script: *"We're modelling Aqualia's double materiality for IE's
  sustainability datathon. Would you be open to a 15-minute call to
  sanity-check our three topics?"*
- **One citable line** in the final report transforms tone from
  "student" to "consulting."
- **Expected uplift:** large. Judges notice.

### 3.3 Visual system (one afternoon's work)
- **Three colours only**: Aqualia navy `#002f5f`, aqua `#5db9d9`,
  neutral sand `#d6cdb7`. Accent `#c83c35` for risk / red cells.
- **One typeface pair**: Inter Bold (titles) + Inter Regular (body)
  OR Source Serif 4 (body) for a more corporate feel.
- **One chart style**: matplotlib rcParams override, applied everywhere.
- **One-page board card template** for each of the three topics.
- **Expected uplift:** significant. Consistent visual ≠ pretty;
  consistent visual = *signal that the team thinks carefully*.

### 3.4 Limitations + reverse stress test section
- PhD-signal section. 1 page.
- For each of T1/T2/T3, answer: *What would the inputs have to be
  for this topic to fall out of Target Zone?*
- For the methodology, list what it **can't** do (no asset-level
  financial data; no real stakeholder interviews; short horizon for
  NGFS modelling; LLM-free ESRS classifier in the prototype).
- **Expected uplift:** moderate — but protects against the single
  biggest pitch vulnerability (a jury poke at an assumption).

### 3.5 Real Options model — refine and visualise
- Currently in `financials.md §5` as an indicative exhibit.
- One additional page: visualise option value surfaces for
  desalination vs water reuse over the 3-year deferral window, with
  crossover points annotated.
- Adds genuine PhD / finance-masters flavour.
- **Expected uplift:** moderate-to-large; memorable.

### 3.6 Execute the Aqueduct map
- Script already scaffolded. ~2 hours to run.
- **Expected uplift:** large. A map belongs in every water deck and
  converts T1's abstract "water stress" into geography.

### 3.7 Upgrade the ESRS heatmap to full corpus
- Download 2022/2023/2024 sustainability reports from the links in
  `02_sources/Aqualia Sustainability Reports.pdf`.
- Re-run `esrs_gap_heatmap.py` (pipeline auto-discovers PDFs).
- Add Veolia URS + Suez URS as a peer-median comparison band.
- **Expected uplift:** large — converts prototype into hero-quality.

---

## 4.  Suggested time budget for the rest of the project

Assuming ~60 remaining hours of collective team effort:

| Block | Hours | Priority |
|---|---|---|
| Write and polish the 10–15 page report | 18 | 1 |
| Design + build the 5-minute deck | 10 | 1 |
| Rehearsals (6×, recorded) | 6 | 1 |
| ESRS heatmap full-corpus upgrade | 4 | 2 |
| Aqueduct map | 3 | 2 |
| Streamlit dashboard | 8 | 2 |
| Expert outreach (LinkedIn + call + transcribe) | 2 | 2 |
| Visual system + templates | 3 | 2 |
| Real Options refinement | 2 | 3 |
| GitHub Pages page | 2 | 3 |
| Buffer | 2 | — |
| **Total** | **60** | |

A full-stack web app eats a chunk of that and returns nothing
graded. The Streamlit option delivers 80% of the perceived tech uplift
for 10–15% of the time.

---

## 5.  Guardrails — if we only had 20 hours left

If time collapses, here is the floor that still wins the 50%
strategic-communication score:

1. **Report finished, every citation in place.** 10 hrs.
2. **Deck rehearsed 4×, hitting the €-number at 4:45.** 4 hrs.
3. **Visual system applied consistently.** 2 hrs.
4. **Matrix figure + one tornado + one map** — no new analysis. 2 hrs.
5. **One paragraph limitations section.** 1 hr.
6. **Final read-through by every teammate.** 1 hr.

Everything else is bonus.

---

## 6.  The single line to remember

*The team that wins this is the one with a clearer argument, a
memorable number, and a cleaner deck — not the one with the fanciest
tech.*

Build the Streamlit. Skip the React. Rehearse.

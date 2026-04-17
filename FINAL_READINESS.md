# Final Readiness — What's Genuinely Left

*Single source of truth for "what still needs to happen before
submission." Read before every work session. Strike through as
shipped.*

Last reviewed: prototype phase complete, full-corpus heatmap shipped,
Monte Carlo in place, deck script drafted, report skeleton drafted,
executive summary drafted.

**Submission success = hits all 4 Workshop 1 Checklist items AND
lands the 5-minute pitch on a €-number close.**

---

## 🟢 What's already complete (nothing left to do)

| # | Deliverable | Path |
|---|---|---|
| A1 | Project library + source archival | `02_sources/` + `02_sources/full_reports/` (11 PDFs, 831 pages) |
| A2 | Aqualia 2025 baseline extraction | `01_research/aqualia_2025_baseline.md` |
| A3 | Peer benchmark (5 peers, ESRS-mapped) | `01_research/peer_benchmark.md` |
| A4 | Scoring rubric (1-5, cited, MC-ready) | `03_analysis/scoring_rubric.md` |
| A5 | Stakeholder salience (Mitchell-Agle-Wood) | `03_analysis/stakeholder_salience.md` |
| A6 | Three-topic short-list LOCKED | `03_analysis/short_list_lock.md` |
| A7 | **ESRS gap heatmap — full corpus** | `04_matrix/esrs_gap_heatmap.png` + HTML, 873 chunks, bilingual, adaptive thresholds |
| A8 | Financial magnitude sheet (€ ranges + Real Options) | `03_analysis/financials.md` |
| A9 | WRI Aqueduct overlay plan + runnable script | `01_research/water_stress.md` |
| A10 | **Monte Carlo matrix** (10k draws, 90% CI) | `04_matrix/matrix_mc.png` + HTML + notes |
| A11 | Sensitivity tornado | `04_matrix/matrix_tornado.png` + CSV |
| A12 | Robustness check (4 weighting schemes) | `03_analysis/mc_robustness.csv` |
| A13 | Streamlit interactive dashboard | `07_streamlit/app.py` |
| A14 | 5-min deck slide-by-slide script | `06_presentation/deck_script.md` |
| A15 | Executive summary (1 page) | `05_report/executive_summary.md` |
| A16 | Report skeleton (13-page outline) | `05_report/report_skeleton.md` |
| A17 | References / bibliography | `05_report/references.md` |
| A18 | Strategy memo — what actually wins | `what_actually_wins.md` |

18 major deliverables drafted. Nothing in this list is a blocker.

---

## 🟡 Priority 1 — Do these (high ROI, short lead time)

### P1.1 — Write the 13-page report body into the skeleton
- **Status:** skeleton + executive summary + references complete.
  Body sections need writing.
- **Input:** `05_report/report_skeleton.md` has section-by-section
  briefs, page budgets, required exhibits, and source citations.
  Each section is 1–2 pages of structured writing.
- **Effort:** 16–20 hours of team writing time, distributed across
  teammates by section.
- **Owner cue:** split sections across team members; use
  `executive_summary.md` tone as the style guide.
- **Gate:** internal read-through before mentor session 2.

### P1.2 — Build the 5-min deck in slides (PowerPoint / Keynote / Slides)
- **Status:** script + slide-by-slide visual briefs complete in
  `06_presentation/deck_script.md`.
- **Input:** 7 slides defined. Visuals specified (matrix PNG, heatmap
  crop, waterfall charts, roadmap grid, QR code).
- **Effort:** 6–8 hours for a polished, on-palette deck.
- **Owner cue:** apply the Aqualia palette (navy/aqua/sand + accent
  red) + Inter typeface across all 7 slides.
- **Gate:** slides reviewed by whole team before Rehearsal 1.

### P1.3 — Rehearse the 5-min pitch, 6× (3 recorded)
- **Status:** script locked. Q&A answers drafted (7 questions).
- **Protocol:** see `06_presentation/deck_script.md` — Rehearsal Protocol.
- **Effort:** 6 × 15 min live + playback = 2.5 hours elapsed + 3 hours
  watch-back/critique.
- **Gate:** timer hits 4:45-5:00 consistently; Q1–Q7 answered in
  under 20 sec each.

### P1.4 — Apply the visual system across all outputs
- **Status:** palette + typeface specified in `deck_script.md`.
- **Effort:** 3 hours — produce a matplotlib rcParams file, PowerPoint
  master template, and chart-style guide. Re-export the four hero
  figures (matrix, tornado, heatmap, value-chain) in the new style.
- **Owner cue:** one team member OWNS visuals and applies everywhere.
- **Expected uplift:** large. Judges unconsciously reward visual
  coherence.

### P1.5 — Credibility hardening pass (done in core docs, apply in final outputs)
- **Status:** methodology hardening integrated into core files:
  reproducibility protocol, evidence tiers, shortlist selection formula,
  and expanded judge-attack Q&A.
- **Action left:** mirror these controls in final report PDF and final
  slide deck export.
- **Effort:** 1.5–2 hours.
- **Gate:** no uncited headline metrics; matrix reproducible from frozen
  inputs; presenter can answer all 15 attack questions in <20 sec.

---

## 🟠 Priority 2 — High perceived lift, moderate effort

### P2.1 — One expert quote (LinkedIn outreach)
- **Status:** not started.
- **Target:** one 15-min call with a water-utility sustainability
  lead — Severn Trent (CSRD-adjacent under UK SDR), Veolia, Suez,
  or a consultancy (ERM, South Pole, EY Climate Change &
  Sustainability Services).
- **Script (to send):** *"We're modelling Aqualia's double
  materiality for IE's sustainability datathon. Would you be open to
  a 15-minute call to sanity-check our three topics? We'd cite you
  by name in the final submission if you're comfortable."*
- **Effort:** 2 hours elapsed (4-7 day wait for outreach → call → transcribe).
- **Deliverable:** one citable line (or two) → Appendix F of the
  report; referenced in Q6 of the pitch Q&A.
- **Expected uplift:** large. Elevates tone from student to
  consulting. **Start this NOW** — the outreach lag is the
  bottleneck.

### P2.2 — WRI Aqueduct map — RUN the script
- **Status:** full runnable Python script scaffolded in
  `01_research/water_stress.md` §5. Exhibit 9 in report body.
- **Blocker:** download the Aqueduct 4.0 shapefile from
  https://www.wri.org/applications/aqueduct/ (free; needs a 2-min
  registration). Place in `02_sources/aqueduct/`.
- **Effort:** 3 hours — download (30 min), install `geopandas +
  contextily` (30 min), run script (10 min), iterate labels (1 hr).
- **Deliverable:** `04_matrix/aqueduct_overlay.png` + Colombia inset.
- **Expected uplift:** large. Maps belong in every water deck;
  instantly-comprehensible.

### P2.3 — Tighten the Monte Carlo
- Widen `PERTURB` in `matrix_mc.py` from 0.7 → 1.0 and re-run —
  confirms the conservative-uncertainty result. Takes 30 sec to run.
- Add a 4th "phantom topic" (Biodiversity E4 alone) to prove that
  omitted topics fall out of Target Zone. Takes 30 min to code.
- Expected uplift: moderate, defends Q4 on T3 knife-edge.

### P2.4 — Real Options exhibit upgrade
- Replace the indicative numbers in `financials.md §5` with a
  genuine Black-Scholes / binomial calculation using Python.
- Produce a 2-line option-value chart (defer 0-3 years, X = time,
  Y = option value) for desal vs reuse.
- Effort: 2 hours.
- Expected uplift: moderate, specifically memorable for finance-
  inclined judges.

### P2.5 — Streamlit deploy + QR code
- `07_streamlit/app.py` ready.
- Push repo to GitHub → connect to Streamlit Community Cloud →
  deploy free.
- Generate QR code (qr-code-generator.com) → paste on slide 7.
- Effort: 2 hours including DNS / SSL testing.
- Fallback: open `04_matrix/matrix_mc.html` directly in the browser
  if Streamlit Cloud is down.

### P2.6 — GitHub Pages landing
- Single-page repo-sibling site at
  `ma731.github.io/aqualia-datathon` linking to the report PDF,
  Streamlit, and heatmap HTML.
- Effort: 2 hours.
- Expected uplift: small-to-moderate — signals polish more than
  substance.

---

## 🔵 Priority 3 — Nice-to-have (do only if time)

### P3.1 — Peer URS classification in the heatmap
Run Veolia URD 2024 and Suez URD 2024 through the same pipeline
to produce a "peer median" tick mark on each cell. One chart-level
edit turns Aqualia coverage into relative coverage. **Effort: 4 hrs.**

### P3.2 — Swap TF-IDF for dense embeddings
Replace the TfidfVectorizer with `sentence-transformers/paraphrase-multilingual-mpnet-base-v2`
to get multilingual, semantic similarity. Improves narrative-
datapoint hits. **Effort: 2 hrs** (package install + thresholds
recalibration).

### P3.3 — Text-similarity differentiation score
For each Aqualia material topic, compute cosine similarity to the
equivalent peer topic (Veolia / Suez / Global Omnium). Low
similarity = differentiated framing. Answers the "me too vs real
advantage" Workshop 1 question quantitatively. **Effort: 3 hrs.**

### P3.4 — Network / Sankey graph of IROs → topics → ESRS
Visualise interdependencies across the 83 IROs. One slide-worthy
Sankey. **Effort: 3 hrs.**

### P3.5 — Climate VaR
Apply NGFS scenario stress factors to Aqualia's asset base to
compute a one-number Climate Value-at-Risk. **Effort: 4 hrs** with
acceptable assumptions.

---

## ⏱️ Suggested 60-hour team budget allocation

Drawn from `what_actually_wins.md §4`:

```
Report body writing               18 hrs   P1.1
Deck production                   10 hrs   P1.2
Rehearsals (6×, recorded)          6 hrs   P1.3
Visual system application          3 hrs   P1.4
────── P1 total                  37 hrs

Expert outreach + call             2 hrs   P2.1  ← start day 1
Aqueduct map                       3 hrs   P2.2
Monte Carlo tightening             1 hr    P2.3
Real Options upgrade               2 hrs   P2.4
Streamlit deploy                   2 hrs   P2.5
GitHub Pages                       2 hrs   P2.6
────── P2 total                  12 hrs

Buffer / P3 picks                 11 hrs
─────────────────
TOTAL                             60 hrs
```

If the team is smaller or the calendar is shorter, cut P3 entirely
and trim P2.5/P2.6. Do NOT cut rehearsals or visual system.

---

## 🚨 The "20-hour floor" scenario

If scope collapses to ~20 hours remaining, this is the minimum that
still wins the 50% strategic-communication grade:

1. **Report body — 10 hrs** — fill exec summary + methodology +
   three topic pages + roadmap; skip detailed financial appendix.
2. **Deck — 4 hrs** — use matrix PNG + heatmap PNG + roadmap grid as-is.
3. **Rehearsals — 3 hrs** — 4 runs minimum, 1 recorded.
4. **Visual sweep — 1 hr** — one palette, one font. Do NOT skip.
5. **Limitations paragraph — 1 hr** — credibility insurance.
6. **Final read-through — 1 hr** — every teammate, no exceptions.

Total 20 hrs. Everything else is bonus.

---

## ⚠️ Things to NOT do (resist the urge)

1. **Full-stack Node/React app.** See `what_actually_wins.md §1`.
2. **New scoring methodologies after rubric lock.** Additional
   perturbations belong in sensitivity, not re-scoring.
3. **New material topics after short-list lock.** The rebuttal in
   `short_list_lock.md §4` defends the 13 dropped; leave it.
4. **Trying to push T3 into Target Zone.** It's a feature, not a
   bug — see `matrix_mc_notes.md §2.3`.
5. **Adding emoji / clip-art / decorative graphics** anywhere.
6. **Presenting from 2 people** unless there's a strong reason.
   Solo is safer.
7. **Reading from the slide** during the pitch. Slides support, not
   lead.
8. **Quoting Aqualia's own 2025 review** without attribution — our
   methodology extends theirs; always name the source.
9. **Improvising the close.** Slide 7 is cardinal; recite verbatim.

---

## Submission day — physical / digital checklist

- [ ] Report PDF (linearised, embedded fonts) on 2 USB sticks
- [ ] Deck PDF backup on 2 USB sticks
- [ ] Streamlit QR code tested on 3 phones
- [ ] Offline `matrix_mc.html` + `esrs_gap_heatmap.html` on USB as
      fallback if Streamlit cloud is down
- [ ] Laptop on wall power + backup laptop available
- [ ] Presenter-mode notes loaded
- [ ] Water on stage
- [ ] Team seated in eye-line of presenter for silent cueing
- [ ] Timer visible to presenter (phone or smartwatch)
- [ ] All file paths tested on a clean machine
- [ ] Printed copy of Q&A prep sheet for each team member

---

## The ONE line this whole project is built to say

*"Three material topics represent €18 M/yr of net financial
materiality Aqualia's current framework under-weights. A €440 M
targeted 2027-2030 investment, funded by our proposed €500 M
EU-Taxonomy-aligned green bond programme, converts this drag into
upside."*

Memorise it. Everything else is evidence.

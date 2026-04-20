# Analytical Report — Skeleton

*Outline + target page count + section-by-section brief. Every section
maps to a Workshop 1 Consultant's Checklist item AND to one or more
artefacts in the repo. Write into this skeleton; do not write it from
scratch.*

**Target:** 13 pages body + appendix (within the 10–15 page rule).
Every page has a **single argument**. Every citation goes to the
bibliography in `references.md`.

**Structure vs deck.** The deck is Pyramid Principle top-down (answer
first, then evidence). The report is the same idea at longer depth —
the Executive Summary IS slide 2 in prose; the later sections are
the evidence chain judges can audit.

---

## Page 1 — Executive Summary

**Source:** `05_report/executive_summary.md` (already drafted).
**Job:** stand alone. A reader who sees only this page knows the
three topics, the headline €-number, and the ask.
**Checklist alignment:** #1 Justify, #4 Actionable.

---

## Page 2 — Challenge and Scope

**Sections**
- 2.1 The CSRD / ESRS mandate (2–3 short paragraphs; link to EU Directive 2022/2464)
- 2.2 Aqualia's operating context (water utility, FCC segment, 8 countries, 32M+ people served)
- 2.3 Our role — external ESG advisory simulation
- 2.4 Framework boundary — ESRS 1–2 + topical standards E1–E5, S1–S4, G1, plus sector-specific AQ extensions

**Sources to cite**
- `00_brief/FV_Aqualia_Datathon_Double_Materiality_Challenge.pdf`
- `Corporate context and sustainability framework_2025_ENG.pdf` §1

**Key exhibits**
- Mini regulatory timeline (2021 Glasgow → 2026 ISO 14001) — reuse from `aqualia_2025_baseline.md` §6.1
- One-line Aqualia value-chain graphic (6-stage water cycle)

**Checklist:** #1 Justify (establishes why these three topics vs all possible)

---

## Pages 3–4 — Methodology

**Sections**
- 3.1 Four-phase blueprint (Workshop 1 canonical) — one-paragraph descriptions
- 3.2 Scoring formulas — preserves Aqualia's own structure, extends to 1–5
  - Impact: `Severity × Probability`, Severity = mean(Scale, Scope, Remediability)
  - Financial: `Magnitude × Probability × Horizon_discount`
  - Rescale 1–25 → 1–5 linear; top-k aggregation at topic level
- 3.3 Threshold table — one row per sub-criterion with cited source
- 3.4 Stakeholder salience — Mitchell, Agle & Wood (1997) applied to Aqualia's 10-group ecosystem; computed weights in a table
- 3.5 Monte Carlo design — triangular distributions, Dirichlet weights, 10k draws, 90% χ² ellipses
- 3.6 Robustness — four alternate weighting schemes; no ranking flip

**Sources to cite**
- `03_analysis/scoring_rubric.md`
- `03_analysis/stakeholder_salience.md`
- `03_analysis/matrix_mc.py` + `matrix_inputs.py`
- ESRS 1 §43–48 and §49–51; EFRAG IG-1 §53–69

**Key exhibits**
- **Exhibit 1** — Threshold table (compressed from rubric §2 and §3)
- **Exhibit 2** — Stakeholder salience weights (table + bar chart)

**Checklist:** #2 Show your math — this is where judges open the hood.

---

## Pages 5–6 — Topic Identification and Selection

**Sections**
- 4.1 From Aqualia's 16 material topics to three (long-list → short-list funnel)
- 4.2 Peer benchmarking — Veolia, Suez, Saur, Facsa, Global Omnium
  - Shared core (E1/E3/S4/G1/S1)
  - Aqualia-specific topics (AQ tags)
  - **Three blind spots** (digitalisation, S3, circular E5)
  - **Three differentiators** (green finance topic, Risk-Map integration, TNFD+CSRD)
- 4.3 Final short-list — three topics, each with 3-word name + 1-line articulation
- 4.4 Rebuttal — why each of the 13 dropped topics is not in the top-3

**Sources to cite**
- `01_research/peer_benchmark.md`
- `03_analysis/short_list_lock.md`
- `AQ_2025_Material Topics_ENG.pdf`
- `v2_VF_Aqualia Informe final Revision Doble Materialidad 2025_ENG.pdf`

**Key exhibits**
- **Exhibit 3** — Peer material-topic matrix (visual ●●●/●●/●)
- **Exhibit 4** — Short-list traceability diagram (16 topics → 3 clusters → 61 IROs absorbed)

**Checklist:** #1 Justify — the heart of the paper.

---

## Pages 7–8 — Impact Materiality Assessment

**Sections**
- 5.1 Value-chain mapping overlay — where impacts occur
- 5.2 Per-topic impact narrative — 1 paragraph each for T1, T2, T3:
  - Current vs potential impacts
  - Stakeholder groups affected (salience-weighted)
  - Severity score and its drivers
- 5.3 IRO digest — table of key IROs per topic (IRO ID, description, ESRS, severity, probability)
- 5.4 **The Colombia finding** — one highlighted panel on S3/S4 split (hero finding #1)

**Sources to cite**
- `aqualia_2025_baseline.md` §3, §5
- `Corporate context... 2025_ENG.pdf` p. 15 (customer-satisfaction table)
- `matrix_mc.py` impact branch
- ESRS S3 (affected communities) Appl. Req.

**Key exhibits**
- **Exhibit 5** — Value-chain impact map (Upstream / Operations / Downstream, colour-coded by topic)
- **Exhibit 6** — IRO digest table (compressed from `aqualia_2025_baseline.md` §5)
- **Exhibit 7** — Colombia outlier panel (satisfaction bar chart by country)

**Checklist:** #2 Show your math on the impact axis.

---

## Pages 9–10 — Financial Materiality Assessment

**Sections**
- 6.1 Per-topic financial decomposition — revenue-at-risk / upside / OPEX / CAPEX / contingent liabilities, each with € low-base-high
- 6.2 Assumption log (A01 – A17) — numbered, sourced, cross-referenced to the sensitivity tornado
- 6.3 **Real Options** — the desalination-vs-water-reuse exhibit (T1 CAPEX decision)
- 6.4 Aqueduct 4.0 water-stress overlay — powers assumption A03; shown here for first time
- 6.5 The €500 M green bond proposal — tranche schedule + coupon-spread maths (hero finding #3)

**Sources to cite**
- `03_analysis/financials.md` (all §§)
- `01_research/water_stress.md`
- FCC Group 2024 segment data (when obtained)
- Climate Bonds Initiative 2024 Pricing Report
- ICMA Green Bond Principles

**Key exhibits**
- **Exhibit 8** — Per-topic € range waterfall (low/base/high side by side for T1, T2, T3)
- **Exhibit 9** — Aqueduct map (Spain + Italy + Colombia insets) — when `aqueduct_overlay.py` runs
- **Exhibit 10** — Real Options option-value surface (desal vs reuse, deferral 0–3y)
- **Exhibit 11** — Bond tranche schedule + PV savings waterfall

**Checklist:** #2 Show your math on the financial axis; #4 Actionable (the €500 M ask is spec'd here).

---

## Page 11 — The Matrix and What It Tells Us

**Sections**
- 7.1 The matrix, annotated — all three ellipses + Target Zone + thresholds
- 7.2 Per-topic positioning summary — 2–3 lines each on where the centroid lies and why
- 7.3 Sensitivity tornado — top 3 inputs per topic that most move the position
- 7.4 Robustness — position stability across four stakeholder weighting schemes

**Sources to cite**
- `04_matrix/matrix_mc.png`
- `04_matrix/matrix_tornado.png`
- `03_analysis/mc_robustness.csv`
- `03_analysis/matrix_mc_notes.md`

**Key exhibits**
- **Exhibit 12** — The matrix (full-page if possible; legible at A4)
- **Exhibit 13** — Sensitivity tornado (compact 3-panel)
- **Exhibit 14** — Robustness table (4 schemes × 3 topics)

**Checklist:** #3 Trace the logic — the matrix proves the argument ties to the numbers.

---

## Page 12 — Strategic Sustainability Roadmap 2027–2030

**Sections**
- 8.1 Per-topic OKRs — 2027 · 2028 · 2029 · 2030 (reuse the 3×4 grid from deck slide 6)
- 8.2 Governance ownership — one named Executive Committee role per topic (from Aqualia's own Risk Map)
- 8.3 KPI list — quantitative success criteria per year per topic
- 8.4 Integration with PESA — how our roadmap extends the 2024–2026 Strategic Sustainability Plan (SL1–SL7) into the next horizon

**Sources to cite**
- `06_presentation/deck_script.md` slide 6
- `AQ_2025_Material Topics_ENG.pdf` (PESA line mapping)
- `Corporate context...` p. 22–24 (risk ownership)

**Key exhibits**
- **Exhibit 15** — 3×4 roadmap grid (same as deck slide 6, expanded)
- **Exhibit 16** — PESA-integration cross-walk table

**Checklist:** #4 Make it actionable — this is the page the Aqualia sustainability lead would keep.

---

## Page 13 — Limitations, Reverse Stress Test, and Ethical Framing

**Sections**
- 9.1 What this methodology CANNOT do — honest list (5–6 bullets)
  - No external stakeholder interviews (this cycle)
  - No asset-level financial disclosures
  - Real Options exhibit is illustrative
  - ESRS heatmap is a prototype (full-corpus upgrade noted)
  - Aqueduct overlay uses public Aqueduct 4.0 baseline, not commissioned hydrological model
  - Scoring rubric uses TF-IDF proxy for corpus classification pending embedding-model upgrade
- 9.2 Reverse stress test — for each of T1/T2/T3, what inputs would have to fail for the topic to drop out of the Target Zone
- 9.3 Ethical framing — data privacy in benchmarks; attribution to Aqualia's own 2025 review; the limits of materiality as a framework

**Sources to cite**
- `03_analysis/matrix_mc_notes.md` §7
- EFRAG IG-1 §90–95 (limitations discussion)

**Key exhibits**
- **Exhibit 17** — Reverse stress test table (per topic, what-would-need-to-fail)

**Checklist:** #2 Show your math (shows what we CAN'T show); PhD signal.

---

## Appendix (unpaginated — use letters: A / B / C / …)

### A. Scoring threshold sheet
Full version of `scoring_rubric.md` §2 and §3 as tables.

### B. Assumption log (A01 – A17)
Source, range, implication for each numeric assumption.

### C. ESRS datapoint coverage (prototype)
Summary output from `coverage_matrix.csv` — one row per DP with band
and top-matching Aqualia chunk reference.

### D. Monte Carlo technical note
Triangular sampling design; Dirichlet prior on stakeholder weights;
top-k aggregation justification; ellipse derivation.

### E. Peer material-topic cross-walk
Full 14-column version of the `peer_benchmark.md` table.

### F. Expert input (if outreach successful)
Transcript or quoted material from the LinkedIn outreach call.

### G. References / Bibliography
Every regulation, standard, paper, and peer report cited in the body.

### H. Data and code
Links or filenames for `matrix_mc.py`, `esrs_gap_heatmap.py`,
`aqueduct_overlay.py`, all input CSVs. Reproducibility trail for any
reviewer.

---

## Per-section writing discipline

- **Lead with the claim.** First sentence of every paragraph answers "so what?"
- **No buzz.** No "leveraging synergies." No "best-in-class" unless a peer explicitly holds that claim.
- **Numbers are concrete.** Never "significant" — always "€X M" or "X%".
- **Every claim cited.** Either a document in this repo or a public source.
- **One exhibit per 1–2 pages.** Do not stack figures.
- **Caption every figure.** A one-sentence caption that states the finding, not the construction.

---

## Production checklist — before submission

- [ ] All 13 body pages written; exec summary finalised
- [ ] All 17 exhibits produced in consistent visual system
- [ ] Bibliography complete (`references.md`)
- [ ] Every numeric claim has a footnote or in-line citation
- [ ] Evidence tiers applied to all numeric assumptions (A/B/C tags)
- [ ] No headline metric depends on Tier C assumptions alone
- [ ] Limitations section co-signed by full team
- [ ] Cross-read by one person who has NOT been close to the project
- [ ] Spanish-language check (some source documents are in Spanish — verify any translated quote)
- [ ] Final PDF export with embedded fonts, linearised
- [ ] Appendix H data-and-code paths tested on a clean machine
- [ ] Read-aloud test: executive summary in under 60 seconds
- [ ] Reproducibility check passed (matrix regenerated from frozen inputs)
- [ ] Submission integrity gate passed (traceability, consistency, citations)

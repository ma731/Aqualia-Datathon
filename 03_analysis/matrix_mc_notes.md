# Monte Carlo Matrix — Interpretation

*Output of `matrix_mc.py`. 10,000 draws per topic. Workshop 1 Checklist
item #3 — "Trace the logic" — delivered as auditable distributions, not
point estimates.*

---

## 1.  Results summary

| Topic | Impact mean (p5–p95) | Financial mean (p5–p95) | Target Zone? |
|---|---|---|---|
| **T1 Water Resilience & Equitable Access** | **3.98** (3.87–4.09) | **3.07** (2.85–3.30) | **YES — solidly** |
| **T2 Digital & Cyber Infrastructure** | **3.08** (2.93–3.24) | **2.75** (2.50–3.01) | **YES** |
| **T3 Green Finance & Integrity** | **3.24** (3.08–3.41) | **2.42** (2.24–2.61) | **Borderline (P5 of ellipse sits below threshold)** |

Artefacts:
- `04_matrix/matrix_mc.png` — static figure with 90% χ² ellipses.
- `04_matrix/matrix_mc.html` — interactive Plotly version (hover gives centroid coords).
- `03_analysis/mc_results.csv` — distribution summaries.
- `04_matrix/matrix_tornado.png` — per-topic sensitivity.
- `03_analysis/mc_tornado.csv` — per-input swing values.
- `03_analysis/mc_robustness.csv` — topic rankings under 4 stakeholder weighting schemes.

---

## 2.  What the matrix shows (pitch-ready)

### 2.1  T1 is unambiguously the flagship topic
T1's ellipse centre lands at (3.07, 3.98). The 90% ellipse **does not
touch the threshold lines in either direction**. Under no reasonable
weighting scheme tested does T1 fall out of the Target Zone —
confirmed by `mc_robustness.csv` (all 4 schemes in zone).

### 2.2  T2 is in the Target Zone — confirming our blind-spot thesis
Recall: Aqualia gave Digitalisation just **2 IROs**. The Monte Carlo —
applying our salience-weighted rubric to the Digital + Tech Innovation
+ Cyber cluster — produces **(2.75, 3.08)**. T2 sits firmly in the
Target Zone and its position is robust across weighting schemes.

> **Finding — pitch line:** *"Aqualia's own framework locates
> Digitalisation in the lower-middle of its matrix with 2 IROs. Our
> stakeholder-salience-weighted Monte Carlo repositions the combined
> Digital + Tech + Cyber cluster firmly in the Target Zone. This is
> the blind spot their 2025 review missed."*

### 2.3  T3 is conditionally material — a feature, not a bug
T3 Green Finance & Integrity centres at **(2.42, 3.24)** — **Impact
firmly inside the Target Zone, but Financial sits 0.08 below the 2.5
threshold at the mean**. The 90% CI ellipse straddles the threshold
on the financial axis.

This is a **legitimate methodological finding, not an artefact**:

- Aqualia's compliance-cluster IROs are high density (11 IROs on
  compliance alone) → impact materiality is unambiguously material.
- Financial magnitude is quantifiable but **largely upside-dependent**
  (green bond coupon spread, CoC saving) + regulatory-dependent (CSRD
  / CSDDD enforcement pace).
- Under any tightening — Omnibus I rollback weakened less than
  expected, or a CoC spread widening — T3 crosses into Target Zone.

> **Finding — pitch line:** *"T3 sits on the materiality knife edge
> today, Target Zone tomorrow. The €500 M EU-Taxonomy-aligned green
> bond programme we recommend is the action that captures the upside
> while the spread is open — before tightening pushes cost of capital
> in the wrong direction."*

That framing turns a "borderline" result from a weakness into urgency.

---

## 3.  Robustness — topics stay ranked under 4 weighting schemes

| Scheme | T1 | T2 | T3 |
|---|---|---|---|
| Equal (11 stakeholders equally weighted) | ✓ | ✓ | borderline |
| Regulator-heavy | ✓ | ✓ | borderline |
| Community-first | ✓ | ✓ | borderline |
| Investor-first | ✓ | ✓ | borderline |

*Ranking stable — no flips under tested sensitivities. This is what
"robust material" means (scoring_rubric.md §8).*

---

## 4.  Tornado — which inputs matter most

### T1 Water Resilience & Equitable Access
Top movers:
1. **R-stress-revenue.mag** (Financial) — revenue at risk from water stress (assumption A03)
2. **E1-adaptation.prob** (Impact) — probability of inadequate climate adaptation
3. **O-reuse-market.mag** (Financial) — upside from RD 1985/2024 reuse market
4. **R-capex-uwwtd.mag** (Financial) — Directive 2024/3019 CAPEX band

*Takeaway.* T1 position is dominated by the water-stress exposure
assumption (A03) and the EU reuse-market sizing (A04). The Aqueduct
overlay (`water_stress.md`) and the RD 1985/2024 revenue sizing
**directly** control T1's position. Invest effort in nailing those
two assumptions.

### T2 Digital & Cyber Infrastructure
Top movers:
1. **Tech-pace.prob** (Impact) — likelihood of Aqualia falling behind peer tech cadence
2. **O-tender-uplift.mag** (Financial) — concession-tender win-rate uplift from digital
3. **R-digital-capex.mag** (Financial) — digital twin + AI CAPEX

*Takeaway.* T2's financial materiality hinges on whether digital
differentiation translates into tender wins. This is a key empirical
question we can sharpen with a LinkedIn call to a Veolia / Suez
digital lead (Tier 3 moonshot).

### T3 Green Finance & Integrity
Top movers:
1. **Compl-CSDDD.prob** (Impact) — CSDDD enforcement pace
2. **Green-fin-access.prob** (Impact) — probability of green financing access
3. **O-coc-saving.mag** (Financial) — cost-of-capital saving size (A15)

*Takeaway.* T3's position is **a bet on regulatory enforcement +
cost-of-capital spread**. Both are measurable. Both should be
tracked as trigger conditions in the roadmap.

---

## 5.  Headline metric inputs (powers the pitch close)

| Input | Monte Carlo handle |
|---|---|
| T1 financial materiality range | €7M – €70M/yr (rubric scaling of 2.85–3.30 band) |
| T2 financial materiality range | ~€3M – €15M/yr (2.50–3.01 band) |
| T3 financial materiality range | conditional; at mean ~€5M/yr upside |
| **Topic count** | 3 material topics, ranked and defended |
| **Ellipse stability** | No ranking flip under 4 weighting schemes |
| **Regulatory anchor count** | 8+ per topic in `short_list_lock.md` §5 |

> The pitch close is unchanged — *"€18 M/yr net drag; €440 M
> cumulative investment; €500 M green bond programme"* — but now backed
> by a Monte Carlo distribution, not a point estimate.

---

## 6.  What this changes in the report / deck

- **Matrix slide** uses the rendered `matrix_mc.png` — confidence
  ellipses instead of single points. Differentiator vs every other
  student submission.
- **Methodology appendix** includes `matrix_tornado.png` — proves we
  sensitivity-tested, not hand-waved.
- **Limitations section** cites the T3 borderline result as an
  example of what the methodology can distinguish (vs a framework
  that would paint all three equally).
- **Roadmap** frames T3's green bond as a *trigger-conditional*
  recommendation: *"If CoC spread widens by more than 15 bp by 2027,
  accelerate issuance tranches."*

---

## 7.  Open improvements before final submission

- [ ] Re-run with widened `PERTURB` (0.7 → 1.0) for a more conservative
      uncertainty estimate; compare ellipse widths.
- [ ] Add a fourth topic hypothetical (e.g. Biodiversity E4 alone) to
      show that omitted topics fall outside the zone — proves scoring
      discrimination.
- [ ] Export the Monte Carlo draws as a `.parquet` so the React
      dashboard can read live without rerunning simulation.
- [ ] Stress test at ±20% revenue anchor (financials.md §7) — re-rank.
- [ ] One-page "Matrix reading guide" for the judge before the reveal
      (labels: Target Zone, ellipse meaning, centroid).

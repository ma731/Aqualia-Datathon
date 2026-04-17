# Scoring Rubric — Double Materiality Assessment

*This is the skeleton everything else hangs on. Workshop 1 Checklist
item #2 ("Show your math") is graded on this file. Every threshold is
cited. Every weight is defended.*

---

## 0.  Design principles

1. **Match Aqualia's internal methodology structure** so our output is
   directly comparable (judges and Aqualia both read our matrix in
   their own vocabulary).
2. **Extend to 1–5 scale** (Aqualia uses 1–4). A 5-point scale adds
   granularity for Monte Carlo draws without changing interpretation.
3. **Anchor every threshold to an external reference** — ESRS,
   EFRAG IG-1, WEF, WRI Aqueduct, MSCI, SASB, peer financial
   disclosures. No vibes.
4. **Produce numeric scores AND confidence intervals** via Monte Carlo
   — reviewer sees not just "3" but "3 ± 0.7 at 90% CI".
5. **Stakeholder-weighted**, not authorial. Weights come from the
   Mitchell–Agle–Wood salience model (see
   `stakeholder_salience.md`), not from us.

---

## 1.  Scoring formulas (summary)

### Impact materiality (Inside-out)

- **Severity** = weighted mean of (Scale, Scope, Remediability), each
  on 1–5.
- **Current impact score** = Severity × 5  *(probability pinned at max)*
- **Potential impact score** = Severity × Probability

Aqualia equivalent: Severity × 4 (current), Severity × Probability
(potential). We preserve the multiplicative structure; only the upper
bound changes.

### Financial materiality (Outside-in)

- **Financial Severity** = Magnitude × Probability

Magnitude estimated as a **triangular distribution** over
(€ low, € base, € high) converted to a 1–5 score using the thresholds
in §3.

### Topic-level consolidation

- **Topic Impact Score** = Stakeholder-salience-weighted mean of the
  topic's IRO impact scores (per stakeholder group).
- **Topic Financial Score** = mean of the topic's risk + opportunity
  financial scores (opportunities entered as positive; risks as
  positive numbers representing avoidance value).
- Each topic plotted as a **90% confidence ellipse** (Monte Carlo,
  10k draws).

---

## 2.  Impact materiality — sub-criterion thresholds

All scales run **1 (minimal) → 5 (critical)**. Thresholds are the
*upper bound* of the band.

### 2.1  Scale — "how serious / deep is the impact"

Anchor: ESRS 1 §43(a), EFRAG IG-1 §53, WRI Aqueduct 4.0 stress classes.

| Score | Band | Threshold / descriptor | Water-sector calibration |
|---|---|---|---|
| 1 | Negligible | Localised, minor, fully reversible within 1 year. No stakeholder health or livelihood effect. | NRW <5%; WTP upset < 1 day; zero non-compliance events |
| 2 | Minor | Measurable but contained within a single municipality / single operational site. Reversible within 3 years. | NRW 5–15%; <1% service interruption >4h/year; rare discharge exceedances |
| 3 | Moderate | Affects multiple municipalities or a regional concession. Reversible within 10 years with planned investment. | NRW 15–25%; 1–3% service interruption >4h; isolated pollution events |
| 4 | Major | Affects a country-level operation or a full service area. Reversible only via structural CAPEX. Livelihoods / public health threatened for some populations. | NRW 25–35%; chronic water-quality breach; restricted-access advisories |
| 5 | Critical | Affects Aqualia group-wide or a priority river basin. Irreversible on human timescales (aquifer depletion, ecosystem collapse). Systemic public health crisis. | Aquifer collapse; mass service denial; WFD ecosystem status breach |

### 2.2  Scope — "how widespread geographically / demographically"

Anchor: ESRS 1 §43(b), WRI Aqueduct population exposure metric.

| Score | Band | Population / geography |
|---|---|---|
| 1 | < 10k people, single installation | E.g., a pumping station incident |
| 2 | 10k–100k people, single municipality | A small concession |
| 3 | 100k–1M people, a province / region | E.g., Andalucía rural corridor |
| 4 | 1M–10M people, a country-level operation | Spain or Portugal subsidiary |
| 5 | >10M people, multi-country or entire river basin | Group-wide; Tagus + Segura basins |

### 2.3  Remediability — "to what extent can the impact be reversed"

Anchor: ESRS 1 §43(c), EFRAG IG-1 §55, TNFD LEAP "Assess".

| Score | Band | Remediability |
|---|---|---|
| 1 | Fully remediable with routine operations | Recover within 1 year, BAU OPEX |
| 2 | Remediable with targeted intervention | 1–3 year remediation, <€1M |
| 3 | Remediable with material CAPEX | 3–10 year remediation, €1–10M |
| 4 | Remediable only via structural programme | >10 year remediation, >€10M, policy change needed |
| 5 | Effectively irremediable on business time horizon | >25 year horizon or ecological tipping point crossed |

### 2.4  Probability — "likelihood of occurrence"

Preserves Aqualia's own bands, extended to 5 levels.

Anchor: Aqualia Methodology p. 6.

| Score | Band | % likelihood / time horizon |
|---|---|---|
| 1 | Remote | <5% in next 5 years |
| 2 | Unlikely | 5–15% in next 5 years |
| 3 | Possible | 15–40% in next 5 years |
| 4 | Likely | 40–75% in next 5 years |
| 5 | Almost certain | >75% in next 3 years, or currently occurring |

For **current impacts** (already occurring), Probability = 5 by
definition.

---

## 3.  Financial materiality — magnitude thresholds

**Baseline anchor:** Aqualia group revenue — we use a **€1.4 B/year**
working estimate (to be confirmed from FCC Aqualia segment disclosures)
and **€40M/year** sustained sustainability CAPEX (cited in Corporate
context p. 14).

Until confirmed, we use **FCC Aqualia 2024 revenue proxy** drawn from
FCC Group's public segment reporting. Sensitivity analysis in
`financials.md` will show how outcomes change if actual revenue is
±20% from proxy.

### 3.1  Financial effect magnitude score

Expressed as a % of annual revenue (proxy €1.4 B). Each threshold has
a € equivalent for intuitive reading.

| Score | Band | % of annual revenue | € equivalent (working) | Justification anchor |
|---|---|---|---|---|
| 1 | Immaterial | < 0.1% | < €1.4 M | Below FCC Group's own segment materiality threshold |
| 2 | Minor | 0.1–0.5% | €1.4–7 M | EFRAG IG-1 suggests ~0.5% of revenue as "low-mat" trigger for large undertakings |
| 3 | Moderate | 0.5–2% | €7–28 M | Approx. 10% of Aqualia's €40M/yr sustainability CAPEX — a recurring budget line |
| 4 | Major | 2–5% | €28–70 M | Equivalent to multi-year single-topic CAPEX programme (e.g. desalination plant) |
| 5 | Severe | > 5% | > €70 M | Enterprise-level impact; group-level capital reallocation required |

### 3.2  How we derive the € ranges per topic

For every risk / opportunity we estimate a **triangular distribution**:

1. **Low (optimistic)** — based on best-case peer or regulatory
   outcome.
2. **Base** — central estimate from our own modelling + stakeholder
   expert judgment.
3. **High (adverse)** — sensitivity based on NGFS Hot-House or
   stressed scenario.

Sources we will use:
- FCC / Aqualia disclosed CAPEX / OPEX by segment
- Veolia and Suez disclosed climate-related financial impact (TCFD reports)
- EFRAG IG 3 datapoint ranges
- SASB Water Utilities metrics (NRW cost, pipe replacement cost/km)
- WRI Aqueduct baseline × revenue exposure
- European Central Bank / NGFS stress-test loss factors

Every € range goes in `03_analysis/financials.md` with an **Assumption ID**
(A01, A02, …) cross-referenced in the final report's appendix.

### 3.3  Probability for financial scoring

Same 1–5 scale as §2.4. Time horizon (short ≤3y / med 3–10y / long >10y)
is recorded but not used as a multiplier — instead we apply a
**discount factor**:

| Horizon | Discount |
|---|---|
| Short-term | 1.00 |
| Medium-term | 0.80 |
| Long-term | 0.60 |

> Discount reflects present-value framing for corporate capital
> allocation. Mirrors EFRAG IG-1 §69 guidance that time horizon should
> inform, not determine, materiality.

---

## 4.  Stakeholder salience weighting

Weights for impact materiality come from `stakeholder_salience.md`.
Each stakeholder group g gets a normalised salience weight
`w_g` in [0, 1] summing to 1.

For each IRO, the **Impact Severity** is computed per affected
stakeholder group and then **weighted-averaged**:

```
Impact Severity (IRO) = Σ_g (w_g × Severity_g) × Probability
```

If an IRO affects only one stakeholder (common for S1 topics
affecting only employees), that stakeholder's weight is used as-is.

---

## 5.  Topic-level aggregation

For each material topic T with N IROs:

```
Topic Impact Score (T) = (1/N) × Σ_i Impact Score_i

Topic Financial Score (T) = weighted average of:
   - mean(Financial Severity) over risks in T    weight 0.5
   - mean(Financial Severity) over opportunities in T    weight 0.5
```

Opportunities contribute positively to financial score on the same
scale as risks — reflecting that avoided losses and captured upside
are equally material to enterprise value.

---

## 6.  Matrix positioning rules (Workshop 1 slide 17)

- X-axis: Topic Financial Score
- Y-axis: Topic Impact Score
- Both axes 1–5; **materiality threshold at 2.5** (Workshop 1 slide 17
  "Target Zone" top-right quadrant).
- Bubble size = **Stakeholder salience coverage** (how many of the 10
  stakeholder groups the topic materially affects).
- Bubble colour = ESRS family (E / S / G / AQ-specific).
- **Uncertainty ellipse (90% CI)** drawn from 10,000 Monte Carlo draws
  across the inputs for that topic.

### Threshold calibration
- Ellipse wholly inside top-right quadrant → **Tier 1 material**
  (must-include in our three).
- Ellipse straddling threshold → **Tier 2 conditional**
  (include only if hero-finding warrants it).
- Ellipse wholly outside → **Tier 3 not material** (disclosure only).

---

## 7.  Monte Carlo simulation design

- **Inputs:** Scale, Scope, Remediability, Probability (per IRO);
  Magnitude low/base/high (per R&O); Stakeholder weights.
- **Distributions:**
  - Scale/Scope/Remediability/Probability → **discrete uniform ±1
    around base score** truncated to [1,5].
  - Magnitude € → **triangular(low, base, high)**.
  - Stakeholder weights → **Dirichlet** centered on salience vector.
- **Draws:** 10,000 per topic.
- **Outputs:** mean, median, std, 5th and 95th percentile of Topic
  Impact and Topic Financial scores. Covariance matrix → ellipse
  parameters.

---

## 8.  Weighting of sub-criteria within Severity

Default: equal weight (1/3 each for Scale, Scope, Remediability) —
matches Aqualia.

**Sensitivity analysis** (mandatory per Workshop 1 Checklist item #2)
runs alternate weightings:

| Weighting scheme | Scale | Scope | Remediability | Justification |
|---|---|---|---|---|
| Balanced (default) | 0.33 | 0.33 | 0.33 | Aqualia method |
| MSCI-inspired | 0.40 | 0.40 | 0.20 | Mirrors rater emphasis on severity and breadth |
| EFRAG IG-1 severity-first | 0.50 | 0.25 | 0.25 | Severity of harm dominates per EFRAG |
| Irreversibility-sensitive | 0.25 | 0.25 | 0.50 | Weights irreversibility heavily for planetary boundaries |

We report topic positions under all four weightings in the appendix
tornado chart. A topic that stays in the Target Zone under all four
is **robust material**; one that flips is flagged as sensitive.

---

## 9.  Validation gates (governance — mirrors Aqualia)

Mirrors Aqualia's internal 3-step validation:

1. **Team internal review** — every score challenged by at least one
   non-author teammate.
2. **Mentor session 2 stress-test** — present scoring methodology and
   top-3 topics to assigned mentor.
3. **Reverse stress test** — for each short-listed topic, ask: *what
   would the inputs need to be for this topic to fall out of
   the Target Zone?* If the answer is "nearly anything plausible,"
   re-score.

---

## 10.  Citations — every threshold traced

| § | Threshold | Source |
|---|---|---|
| 2.1 | Scale water-sector calibration | SASB Water Utilities NRW metric; Aqualia Corp. context p. 14 (€40M/yr CAPEX) |
| 2.1 | 5-band severity | ESRS 1 §43(a); EFRAG IG-1 §53 |
| 2.2 | Scope population bands | WRI Aqueduct 4.0 population exposure; EFRAG IG-1 §54 |
| 2.3 | Remediability cost bands | TNFD LEAP Assess; EFRAG IG-1 §55 |
| 2.4 | Probability bands | Aqualia Methodology p. 6 (extended to 5 levels) |
| 3.1 | Financial % thresholds | EFRAG IG-1 §68; FCC Group 2024 segment reporting (proxy) |
| 3.3 | Time discount factors | EFRAG IG-1 §69; standard DCF 8% for long-term water infra |
| 6 | Target Zone 2.5 threshold | Workshop 1 slide 17 |
| 8 | Weighting schemes | MSCI Water Utilities methodology 2024; EFRAG IG-1 §53 |

---

*Every line in this rubric is a potential audit question from the
jury. If you can't defend a threshold, change it now.*

# Stakeholder Salience Weights — Mitchell, Agle & Wood (1997)

*Converts Aqualia's qualitative stakeholder map into quantified
weights for the impact-materiality formula. This is the PhD-signal
element judges will recognise: a published salience model applied to
a named stakeholder set, not authorial opinion.*

**Academic anchor:** Mitchell, R. K., Agle, B. R., & Wood, D. J.
(1997). "Toward a Theory of Stakeholder Identification and Salience:
Defining the Principle of Who and What Really Counts." *Academy of
Management Review*, 22(4), 853–886.

**Input stakeholder map:** `AQ_2025_GGII_ENG.pdf` — Aqualia's own 10
stakeholder groups. We use their taxonomy so our weights integrate
cleanly with their language.

---

## 1.  Framework

Each stakeholder group is scored 0/1 on three attributes:

- **Power** — ability to influence the firm's outcomes (legal, coercive, utilitarian).
- **Legitimacy** — relationship is appropriate, proper, socially or normatively grounded.
- **Urgency** — claim requires timely attention (time-sensitive + critical).

Mitchell et al. classify resulting stakeholders into 7 types:

| Attributes | Type | Salience |
|---|---|---|
| None | Non-stakeholder | 0 |
| Power only | Dormant | 1 — Low |
| Legitimacy only | Discretionary | 1 — Low |
| Urgency only | Demanding | 1 — Low |
| Power + Legitimacy | Dominant | 2 — Moderate |
| Power + Urgency | Dangerous | 2 — Moderate |
| Legitimacy + Urgency | Dependent | 2 — Moderate |
| All three | **Definitive** | **3 — High** |

We extend Mitchell's ordinal types to a **continuous salience score**:
`Salience = Power + Legitimacy + Urgency` ∈ {0, 1, 2, 3}.

Aqualia's own stakeholder matrix captures **Expectations, Commitments,
Requirements, Channels** — we derive attribute scores from the
intensity and formality of each column.

---

## 2.  Attribute scoring per stakeholder

Sources of evidence per group (all from `AQ_2025_GGII_ENG.pdf`):
- "Requirements" column — regulatory / contractual = **Power** signal.
- "Commitments" language — presence of formal commitments = **Legitimacy** signal.
- "Channels" density + frequency — engagement cadence = **Urgency** signal.

### 2.1  Decision table

| # | Stakeholder | Power | Legitimacy | Urgency | Mitchell type | Salience |
|---|---|:---:|:---:|:---:|---|:---:|
| 1 | **Public authorities & regulators** | 1 | 1 | 1 | Definitive | **3** |
| 2 | **Customers & end users** (inc. irrigation communities) | 1 | 1 | 1 | Definitive | **3** |
| 3 | **Shareholders (FCC / IFM)** | 1 | 1 | 1 | Definitive | **3** |
| 4 | **Employees** (incl. unions) | 1 | 1 | 1 | Definitive | **3** |
| 5 | **Investors & analysts** (capital, rating agencies) | 1 | 1 | 0 | Dominant | **2** |
| 6 | **Suppliers & subcontractors** | 1 | 1 | 0 | Dominant | **2** |
| 7 | **Society / NGOs / media** | 0 | 1 | 1 | Dependent | **2** |
| 8 | **Local communities & indigenous populations** *(separated from Society)* | 0 | 1 | 1 | Dependent | **2** |
| 9 | **Business partners** | 1 | 1 | 0 | Dominant | **2** |
| 10 | **Academy** (universities, research centres) | 0 | 1 | 0 | Discretionary | **1** |
| 11 | **Environment** (as stakeholder — cited in Value Chain Map) | 0 | 1 | 1 | Dependent | **2** |

### 2.2  Rationale for non-obvious calls

- **Customers — urgency = 1** because service continuity claims are
  time-critical (a water outage cannot be deferred) and because
  regulatory tariffs tie claims to compliance deadlines. This is
  the key difference from most sectors, where customer urgency
  would be 0.
- **Society — power = 0** because diffuse public opinion does not
  directly control Aqualia's assets, but legitimacy and urgency
  (climate, equity) are both 1. Aqualia's own "Transparency" and
  "Adaptation & mitigation" commitments in the GGII table confirm
  legitimacy.
- **Local communities — separated from Society** because in
  concession markets (especially Colombia at 33% satisfaction)
  community claims differ qualitatively from diffuse public
  opinion — proximate, affected, and urgent. Also aligned to ESRS
  S3 which treats affected communities as a distinct standard.
- **Environment as stakeholder** — cited explicitly in Aqualia's
  Value Chain Map as "a stakeholder from which the water resource is
  drawn." Legitimacy via CSRD/ESRS E3/E4 requirement that
  companies account for impacts on nature. Urgency via WEF Global
  Risks (5 of top 10 water-related). Power = 0 since nature has no
  agency to enforce its claims, only via regulators.
- **Shareholders (FCC / IFM) — all 3** because they hold formal
  control (Power), own the entity (Legitimacy), and have
  quarterly reporting cadence (Urgency).
- **Academy — discretionary** because engagement is voluntary,
  principally for innovation partnerships, not a binding
  relationship.

---

## 3.  Normalised weights

Raw salience sum = 3+3+3+3+2+2+2+2+2+1+2 = **25**.

| Stakeholder | Salience | Weight (w_g) |
|---|---|---|
| Public authorities & regulators | 3 | **0.120** |
| Customers & end users | 3 | **0.120** |
| Shareholders (FCC / IFM) | 3 | **0.120** |
| Employees | 3 | **0.120** |
| Investors & analysts | 2 | 0.080 |
| Suppliers & subcontractors | 2 | 0.080 |
| Society / NGOs / media | 2 | 0.080 |
| Local communities & indigenous populations | 2 | 0.080 |
| Business partners | 2 | 0.080 |
| Environment | 2 | 0.080 |
| Academy | 1 | 0.040 |
| **Total** | 25 | **1.000** |

---

## 4.  Application in the impact formula

For an IRO affecting stakeholder set S:

```
Severity_IRO = Σ_{g ∈ S} w_g_norm × Severity_g

where  w_g_norm = w_g / Σ_{g ∈ S} w_g
```

i.e., weights are renormalised over the stakeholders actually affected
by that IRO.

### Example — IRO O3 "Insufficient crisis response capacity"
Affects: Customers (0.120), Society (0.080), Local communities (0.080),
Public authorities (0.120), Environment (0.080). Total = 0.480.
Renormalised weights: 0.25 / 0.167 / 0.167 / 0.25 / 0.167.

A rater who judges Severity as (Customers=5, Society=4, Local=5,
Auth=4, Env=4) produces
Severity_O3 = 0.25·5 + 0.167·4 + 0.167·5 + 0.25·4 + 0.167·4 = **4.34**.

---

## 5.  Robustness checks

Mandatory sensitivity analyses for the final report (mirrors Workshop 1
Checklist item #2 and a PhD-grade limitations section):

### 5.1  Alternate salience models

| Model | What changes | Purpose |
|---|---|---|
| Equal weighting (baseline) | All 11 groups weight 1/11 | Shows how much work salience is doing |
| Regulator-heavy | Public authorities weight 0.30 | Regulated-utility benchmark |
| Community-first | Society + Local communities combined = 0.30 | Stakeholder-theory purist |
| Investor-first | Shareholders + Investors = 0.30 | Financial-materiality purist |

Run the Monte Carlo under each. Topics that remain in the Target Zone
under **all four** are our "robust" material topics.

### 5.2  Dirichlet prior for Monte Carlo

For the main simulation, weights are drawn from
`Dirichlet(α)` with `α = k × salience_vector`, k chosen so the
standard deviation of each weight is ~20% of its mean. This injects
principled uncertainty rather than point weights.

---

## 6.  How this differentiates our submission

- **Aqualia 2025 review did NOT apply any salience model** — the
  methodology PDF explicitly states scoring was done "internally
  within the Sustainability Department" with no external
  stakeholder consultation. A named academic salience model is a
  substantive methodological extension.
- **Workshop 1 slide 7 prompt** — *"What differentiates each player?
  Is Aqualia's differentiation a 'me too' or a real advantage?"* — is
  operationalised here: the salience weights *quantify* the
  distinctiveness of Aqualia's stakeholder universe vs peers.
- **Judges reading ESRS purist disclosures** will recognise Mitchell,
  Agle & Wood immediately — it is THE canonical stakeholder-
  identification paper (cited ~15,000 times).

---

## 7.  Open actions

- [ ] **Expert quote to validate** — one 15-min LinkedIn outreach to
      a sustainability lead at Veolia or Severn Trent to sanity-check
      salience calls. Target: one citable quote in the final report.
- [ ] Cross-check against **AA1000 Stakeholder Engagement Standard**
      classification — ensures we are not blindsided by a standard
      Aqualia's auditors use.
- [ ] Revisit Environment's Power score after reading EU Nature
      Restoration Regulation — if legal personality is extended to
      waterbodies in any Aqualia service region, Power flips to 1.

---

*Reference:* Mitchell, R. K., Agle, B. R., & Wood, D. J. (1997).
Toward a Theory of Stakeholder Identification and Salience: Defining
the Principle of Who and What Really Counts. *Academy of Management
Review*, 22(4), 853–886. https://doi.org/10.2307/259247

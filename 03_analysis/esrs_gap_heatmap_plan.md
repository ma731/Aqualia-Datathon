# ESRS Gap Heatmap — Hero Slide Prototype Plan

*This is the hero slide. Judges will remember three things from our
submission: the three topics, a headline € number, and this heatmap.
One image that makes it visually obvious where Aqualia is already CSRD-
compliant and where the gaps are.*

---

## 0.  The concept

One chart. Y-axis = ESRS topical standards (E1 ... G1). X-axis =
disclosure-requirement buckets within each standard. Cell colour =
Aqualia's current coverage level derived from NLP classification of
the 2024 Sustainability Report against each ESRS datapoint.

**Green** = disclosure is already strong. **Amber** = partial or
implicit. **Red** = gap. **Grey** = not applicable (ESRS phase-in /
non-material).

A second row under each topic shows the **peer median** coverage as a
benchmark band. Aqualia cells above the peer line are strengths;
below are gaps the report should flag. One look tells the jury
exactly which of our three recommended topics are also the biggest
disclosure gaps — tying regulatory compliance to strategic priority.

---

## 1.  Why this wins

### Workshop 1 Checklist alignment

| Checklist item | How the heatmap delivers |
|---|---|
| 1. Justify your selection | Gaps in the heatmap directly justify why our three topics deserve priority over the other 13 |
| 2. Show your math | Every cell is traceable to an embedding-similarity score; cell count = ESRS datapoints matched |
| 3. Trace the logic | Matrix → heatmap → roadmap, all three tied to the same datapoint taxonomy |
| 4. Make it actionable | Red cells are the 2027–2030 disclosure roadmap — literal input to PESA update |

### Competitive moat
- No student submission will produce a quantitative ESRS disclosure
  gap analysis. This is consulting IP.
- Reuses work: the same embeddings feed the peer-benchmark
  differentiation score (see Tier 3 moonshot in README §7).
- One slide replaces ten pages of argument.

---

## 2.  Data sources

### 2.1  ESRS datapoint library (input universe)
- **EFRAG ESRS Set 1 XBRL taxonomy** — machine-readable list of
  all ~1,144 datapoints across ESRS 1, ESRS 2, E1–E5, S1–S4, G1.
  Source: https://www.efrag.org/lab6
- Alternative: **EFRAG IG 3 Datapoint List** (Excel export). Simpler
  to parse but less granular.
- Each datapoint has: ID (e.g., `E3-3_02`), standard, disclosure
  requirement, datapoint type (narrative / quantitative / semi-
  narrative), conditional / mandatory, phase-in year.

### 2.2  Aqualia disclosures (classified against the library)
- **Aqualia 2024 Sustainability Report** — "The blue thread that
  connects us." (linked from
  `02_sources/Aqualia Sustainability Reports.pdf`)
- 2023 Report ("Regeneration for a positive future") as secondary.
- 2022 Report as tertiary — used for trend lines.
- Optional: Aqualia's **non-financial statement (EINF)** under Ley
  11/2018, which often has richer quantitative data than the
  sustainability brochure.

### 2.3  Peer disclosures (for benchmark band)
- Veolia **2024 Universal Registration Document** (URD)
- Suez **2024 URD**
- Saur **2023 Sustainability Report**
- Facsa **2023 Memoria Anual**
- Global Omnium **2023 Sustainability Report**

All publicly available PDFs.

---

## 3.  Pipeline design

```
┌─────────────────┐     ┌─────────────────┐    ┌─────────────────┐
│  ESRS taxonomy  │     │  Aqualia 2024   │    │  Peer reports   │
│  (~1,144 DPs)   │     │  Sust. Report   │    │  (5 files)      │
└────────┬────────┘     └────────┬────────┘    └────────┬────────┘
         │                       │                      │
         ▼                       ▼                      ▼
  ┌──────────────┐        ┌──────────────┐       ┌──────────────┐
  │ DP embeddings │        │ chunk + embed │       │ chunk + embed │
  └──────┬───────┘        └──────┬───────┘       └──────┬───────┘
         │                       │                      │
         └──────────┬────────────┴──────────────┬──────┘
                    ▼                           ▼
         ┌──────────────────────┐    ┌──────────────────────┐
         │ cosine similarity    │    │ cosine similarity    │
         │ (DP × Aqualia chunks)│    │ (DP × peer chunks)   │
         └──────────┬───────────┘    └──────────┬───────────┘
                    ▼                           ▼
         ┌──────────────────────┐    ┌──────────────────────┐
         │ per-DP top-k match   │    │ per-DP peer coverage │
         │ → Aqualia coverage   │    │ → sector benchmark   │
         └──────────┬───────────┘    └──────────┬───────────┘
                    └─────────────┬─────────────┘
                                  ▼
                    ┌──────────────────────────┐
                    │  Heatmap renderer        │
                    │  (Plotly / Matplotlib)   │
                    └──────────────────────────┘
```

---

## 4.  Technical choices

### 4.1  Embedding model
- **`text-embedding-3-large`** (OpenAI, 3,072 dims) — default.
  Strong multilingual (we have some Spanish content) + long context.
  Alternative: **`voyage-3-large`** if API access available.
- Local fallback: **`BAAI/bge-large-en-v1.5`** via
  sentence-transformers. Free, good enough for POC.

### 4.2  Chunking strategy
- Split each sustainability report by page + semantic paragraph
  (`langchain.text_splitter.RecursiveCharacterTextSplitter`,
  chunk_size=800, overlap=150).
- Tag each chunk with `{company, year, page, section_heading}` for
  traceability in the final heatmap tooltip.

### 4.3  Coverage scoring (per ESRS datapoint)
- For each ESRS datapoint description d_i:
  - Compute cosine similarity to every Aqualia chunk.
  - Take top-k (k=3) and average.
  - Map to coverage band:
    - ≥ 0.60 → **Green** (strong disclosure present)
    - 0.45 – 0.60 → **Amber** (partial / implicit)
    - 0.30 – 0.45 → **Red** (gap, some adjacent language)
    - < 0.30 → **Dark red** (no coverage)
    - N/A if DP is phase-in or non-applicable → **Grey**
- Calibrate thresholds by spot-checking **20 datapoints** manually
  before accepting output. Publish calibration set in appendix.

### 4.4  Avoiding false positives
Embedding similarity can fire on tangential language. Mitigations:
- **Quantitative datapoints** need an adjacent number in the Aqualia
  chunk to count as green (simple regex check).
- **Mandatory vs narrative** datapoints scored separately — a
  narrative DP is easier to hit than a quantitative one.
- Manual audit trail: every cell tooltip shows the top-matching
  Aqualia chunk so reviewers can audit.

### 4.5  Peer comparison
- Same pipeline across 5 peers → 5 coverage vectors per datapoint.
- Aggregate as **median peer coverage** per DP.
- Visual: narrow white bar inside each cell marking where the peer
  median sits. Aqualia cell colour above the bar = leader; below =
  laggard.

---

## 5.  Output design

### 5.1  Primary chart (hero slide)
- Vertical axis: ESRS standards grouped by family (E1 / E2 / E3 /
  E4 / E5 / S1 / S2 / S3 / S4 / G1).
- Horizontal axis: **Disclosure Requirements** within each standard
  (collapsed to ~8–12 cells per standard for readability — avoid
  1,144-cell blur).
- Cell colour: Aqualia coverage band.
- Cell annotation: peer-median coverage as tick mark.
- Right-hand gutter: our three chosen topics' ESRS codes highlighted
  (visual link from heatmap → matrix → roadmap).
- Tool: Plotly heatmap with hover tooltips; export as static SVG for
  the report and interactive HTML for the appendix.

### 5.2  Drill-down (appendix / Streamlit)
- Click any cell → see: ESRS DP ID + text, top-3 matching Aqualia
  chunks with page refs, peer matches, suggested 2027–2030
  disclosure action.

### 5.3  Headline metric for the pitch
- *"Aqualia is already Green on X% of the ~1,144 ESRS datapoints,
  Amber on Y%, and Red on Z%. The three material topics we
  recommend concentrate **N% of the Red cells** — fixing them
  closes M% of the total disclosure gap by 2028."*
- That single sentence, delivered on slide 2 of the 5-min pitch, is
  the pitch.

---

## 6.  Implementation plan

| Step | Output | Time estimate |
|---|---|---|
| 6.1 | Download EFRAG ESRS taxonomy (XBRL or IG-3 Excel); parse to DataFrame | 1h |
| 6.2 | Download 6 PDFs (Aqualia 2022–24 + 5 peers); verify text-extractable | 1h |
| 6.3 | Build chunking + embedding pipeline; cache vectors | 3h |
| 6.4 | Compute similarity matrices (DPs × chunks) for all 6 companies | 2h |
| 6.5 | Threshold calibration on 20-DP audit set | 2h |
| 6.6 | Aggregate to heatmap data structure (standard × DR grid) | 1h |
| 6.7 | Plotly/Matplotlib render + SVG export | 2h |
| 6.8 | Write tooltip/drill-down interactive HTML | 2h |
| 6.9 | Headline metric + caption authoring | 1h |
| **Total** | **~15 hours of work** | |

Feasible in 2–3 working sessions. Highest-ROI deliverable in the
whole submission.

---

## 7.  Risk mitigations

| Risk | Mitigation |
|---|---|
| Taxonomy file format shifts (EFRAG updates quarterly) | Freeze our version with date stamp; cite EFRAG release version |
| Embedding similarity false positives on narrative DPs | Manual audit set + regex check for quantitative DPs |
| Aqualia report heavy on images → less text to embed | Fall back to 2023 and 2022 reports for combined corpus; cite when multi-year coverage applied |
| Time budget over-run | Minimum viable version = Aqualia-only heatmap (no peer band); still hero-worthy |
| LLM API cost | Local `bge-large` fallback is free; ~1.5M tokens total corpus fits easily |
| Jury mis-reads the chart | Use clear legend + one-line caption; include a "read this chart" micro-slide before the reveal |

---

## 8.  Deliverables to produce

1. `03_analysis/esrs_gap_heatmap.ipynb` — Jupyter notebook running
   the pipeline end-to-end.
2. `03_analysis/esrs_taxonomy.csv` — parsed ESRS datapoint list.
3. `03_analysis/coverage_matrix.parquet` — company × datapoint
   coverage scores.
4. `04_matrix/esrs_gap_heatmap.svg` — static hero image.
5. `04_matrix/esrs_gap_heatmap.html` — interactive Plotly dashboard
   (appendix / Streamlit link).
6. One paragraph + figure caption for the report's Executive Summary.

---

## 9.  Tier 3 extension — text-similarity peer differentiation score

Reusing the same embeddings:
- For each of Aqualia's 16 material topics, compute cosine similarity
  between Aqualia's topic description and each peer's equivalent
  topic descriptor.
- Low similarity = differentiated framing; high similarity = "me too."
- Output: table of differentiation scores per topic per peer,
  directly answering Workshop 1 slide 7 ("Is it a 'me too' or real
  advantage?").

---

## 10.  Sanity-check questions before shipping

Before putting the heatmap in the final pack, answer each of these in
one sentence:

1. Can a judge read the chart in under 10 seconds? *If no, simplify.*
2. Can we defend any single cell colour if challenged? *If no, audit.*
3. Does the headline metric change materially if thresholds move by
   ±0.05? *If yes, report sensitivity.*
4. Does the peer benchmark band make Aqualia look worse than
   reality? *If yes, triple-check extraction.*
5. Would we show this chart to Aqualia's sustainability board
   tomorrow? *If no, it's not ready.*

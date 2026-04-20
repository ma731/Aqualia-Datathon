# 07_streamlit — Interactive dashboard (secondary)

Streamlit single-file app that mirrors the React dashboard's visual
language (navy / aqua palette, Fraunces + Inter typography, animated
water ambience, glassy KPI cards, pill tabs) while preserving the
full analyst cockpit: live Monte Carlo re-weighting, scenario
toggles, ESRS gap heatmap, Aqueduct geo view, Jury Simulator, and
auto-tour coach for live demos.

## Primary vs secondary

The **React dashboard** in [`10_dashboard_react/`](../10_dashboard_react/)
is the primary interactive deliverable cited on the pitch deck. This
Streamlit app is a secondary path, retained because:

- Zero-build demo: one `streamlit run` line, no Node toolchain.
- Deeper interactivity (live slider-driven Monte Carlo recomputation
  with N draws adjustable from 500 to 10 000) that would be expensive
  to reproduce in static React.
- Backup route in case the React build is unreachable during the jury
  session.

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

Opens on `http://localhost:8501`. The `.streamlit/config.toml` at the
repo root configures the Aqualia theme and enables static file
serving.

## Optional hero video

Drop a muted, short (8–15 s) looping `.mp4` at `static/hero-video.mp4`
and it auto-activates as the hero background. If the file is absent,
the app falls back to a CSS-animated water ambience (28 seeded
droplets + two flowing SVG waves) so the dashboard always looks good
out of the box. See [`static/README.md`](static/README.md) for an
`ffmpeg` one-liner.

## What's in the tabs

1. **Matrix** — Monte Carlo double-materiality plot with 90 %
   χ²-derived confidence ellipses, portfolio-shape radar, delta vs
   base, and rank-by-composite.
2. **Finance** — Green-bond cockpit: spread slider, PV-savings
   waterfall, tranche schedule, spread sensitivity.
3. **ESRS Gap Heatmap** — embeds `04_matrix/esrs_gap_heatmap.html`
   with the coverage-score detail table.
4. **Geo Risk** — WRI Aqueduct choropleth with executive takeaway
   and KPI bundle.
5. **Findings** — the three hero cards, storyboard, evidence
   quick-reference.
6. **Methodology** — scoring formulas, artefact links, one-click
   CSV / PNG downloads.
7. **Requirements Fit** — live checklist mapping each dashboard view
   to the official evaluation criteria.
8. **Jury Simulator** — stress-test the pitch under alternate jury
   priorities (methodology-heavy, storytelling-heavy, skeptical-risk
   judges) with a live score gauge.

## Inputs it reads

- `03_analysis/matrix_inputs.py` — scoring primitives, IROs, ROs,
  stakeholder weights, horizon discounts.
- `03_analysis/coverage_matrix.csv` — ESRS gap bands.
- `03_analysis/mc_robustness.csv` — cross-scheme ranking stability.
- `04_matrix/esrs_gap_heatmap.html` — embedded iframe.
- `04_matrix/aqueduct_choropleth.html` (or fallback PNG) — geo view.

All artefacts are produced by the reproducible pipeline in
`03_analysis/`. No live recomputation is needed for the baseline
view — sliders re-run only the Monte Carlo, not the upstream
TF-IDF / Aqueduct workloads.

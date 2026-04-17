"""
Aqualia Double Materiality — Interactive Dashboard
==================================================

Single-file Streamlit app. Runs on Streamlit Community Cloud (free)
or locally:

    pip install streamlit pandas numpy plotly
    streamlit run 07_streamlit/app.py

The app reads artefacts produced by the analysis pipeline (no live
recomputation needed for the baseline view) and lets the user
interact with three things:

  1. The Monte Carlo matrix — filter topics, toggle Target Zone.
  2. The ESRS gap heatmap — hover any cell for the source chunk.
  3. The scoring inputs — a live re-weighting slider for stakeholder
     salience, with the matrix redrawn on-the-fly.

This is the QR-code destination for slide 5 of the pitch.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Make matrix_inputs importable
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "03_analysis"))

from matrix_inputs import (  # noqa: E402
    HORIZON_DISCOUNT,
    STAKEHOLDER_WEIGHTS,
    TOPIC_IROS,
    TOPIC_ROS,
)

# -------------------------------------------------------------------
# Page config + palette
# -------------------------------------------------------------------

st.set_page_config(
    page_title="Aqualia Double Materiality — IE Sustainability Datathon",
    page_icon="💧",
    layout="wide",
)

AQUALIA_NAVY = "#002f5f"
AQUALIA_AQUA = "#5db9d9"
ACCENT_RED = "#c83c35"

TOPIC_COLORS = {
    "T1 Water Resilience & Equitable Access": "#1f77b4",
    "T2 Digital & Cyber Infrastructure":      "#ff7f0e",
    "T3 Green Finance & Integrity":           "#2ca02c",
}


# -------------------------------------------------------------------
# Scoring (same math as matrix_mc.py, vectorised)
# -------------------------------------------------------------------


def _rescale(x: np.ndarray) -> np.ndarray:
    return np.clip(1.0 + (x - 1.0) / 6.0, 1.0, 5.0)


def _topk_mean(arr: np.ndarray, k: int) -> np.ndarray:
    k = min(k, arr.shape[0])
    return np.partition(arr, -k, axis=0)[-k:, :].mean(axis=0)


def sample_tri(base: float, n: int, spread: float) -> np.ndarray:
    low = max(1.0, base - spread)
    high = min(5.0, base + spread)
    if low >= high:
        return np.full(n, base)
    return np.clip(np.random.triangular(low, base, high, size=n), 1.0, 5.0)


def sample_mag(lbh, n: int) -> np.ndarray:
    low, base, high = (float(x) for x in lbh)
    if low == base == high:
        return np.full(n, base)
    if low > base:
        base = low
    if high < base:
        high = base
    return np.clip(np.random.triangular(low, base, high, size=n), 1.0, 5.0)


def compute_topic_scores(
    weights_vec: dict[str, float],
    perturb: float,
    n: int,
    seed: int,
) -> dict[str, dict]:
    rng = np.random.default_rng(seed)
    np.random.seed(seed)
    # Deterministic stakeholder weights per scheme
    weights = {k: np.full(n, v) for k, v in weights_vec.items()}

    out: dict[str, dict] = {}
    for topic, iros in TOPIC_IROS.items():
        iro_scores = []
        for iro in iros:
            scale = sample_tri(iro["scale"], n, perturb)
            scope = sample_tri(iro["scope"], n, perturb)
            rem = sample_tri(iro["rem"], n, perturb)
            severity = (scale + scope + rem) / 3.0
            prob = np.full(n, 5.0) if iro["current"] else sample_tri(iro["prob"], n, perturb)
            raw = severity * prob
            affected = np.sum([weights[s] for s in iro["stakeholders"]], axis=0)
            ref = np.mean([weights[s] for s in iro["stakeholders"]], axis=0) * len(iro["stakeholders"])
            mult = np.where(ref > 1e-9, affected / ref, 1.0)
            raw = raw * (0.85 + 0.15 * mult)
            iro_scores.append(raw)
        impact_raw = _topk_mean(np.stack(iro_scores, axis=0), max(3, int(round(len(iros) * 0.6))))
        impact = _rescale(impact_raw)

        ro_scores = []
        for ro in TOPIC_ROS[topic]:
            mag = sample_mag(ro["mag_lbh"], n)
            prob = sample_tri(ro["prob"], n, perturb)
            disc = HORIZON_DISCOUNT[ro["horizon"]]
            ro_scores.append(mag * prob * disc)
        fin_raw = _topk_mean(np.stack(ro_scores, axis=0), max(3, int(round(len(TOPIC_ROS[topic]) * 0.6))))
        fin = _rescale(fin_raw)

        out[topic] = {"impact": impact, "financial": fin}
    return out


def ellipse_from_draws(x: np.ndarray, y: np.ndarray) -> dict:
    cov = np.cov(x, y)
    vals, vecs = np.linalg.eigh(cov)
    order = vals.argsort()[::-1]
    vals = vals[order]
    vecs = vecs[:, order]
    angle = math.degrees(math.atan2(vecs[1, 0], vecs[0, 0]))
    k = math.sqrt(4.605)  # 90% chi2 df=2
    return {
        "cx": float(np.mean(x)),
        "cy": float(np.mean(y)),
        "w": float(2 * k * math.sqrt(max(vals[0], 1e-9))),
        "h": float(2 * k * math.sqrt(max(vals[1], 1e-9))),
        "angle": float(angle),
    }


# -------------------------------------------------------------------
# Header
# -------------------------------------------------------------------

st.markdown(
    f"""
    <div style="padding:18px 24px;border-radius:12px;background:linear-gradient(90deg,{AQUALIA_NAVY},{AQUALIA_AQUA});color:white">
      <div style="font-size:28px;font-weight:700">Aqualia Double Materiality — Interactive Matrix</div>
      <div style="font-size:15px;opacity:0.9">IE Sustainability Datathon 2026 · Consulting appendix</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

# -------------------------------------------------------------------
# Sidebar — controls
# -------------------------------------------------------------------

with st.sidebar:
    st.header("Controls")

    scheme = st.selectbox(
        "Stakeholder weighting scheme",
        (
            "Salience model (Mitchell-Agle-Wood)",
            "Equal (11 groups)",
            "Regulator-heavy",
            "Community-first",
            "Investor-first",
        ),
    )

    perturb = st.slider(
        "Monte Carlo perturbation (input noise)",
        min_value=0.3, max_value=1.2, value=0.7, step=0.05,
        help="Width of the triangular distribution around each base score.",
    )

    n_draws = st.select_slider(
        "Draws per topic",
        options=[500, 1000, 3000, 6000, 10000],
        value=3000,
    )

    show_scatter = st.checkbox("Show draw scatter", value=True)
    show_ellipse = st.checkbox("Show 90% confidence ellipse", value=True)
    show_target = st.checkbox("Highlight Target Zone", value=True)

    st.markdown("---")
    st.caption("Artefact links")
    st.caption("• Matrix PNG  → `04_matrix/matrix_mc.png`")
    st.caption("• Tornado PNG → `04_matrix/matrix_tornado.png`")
    st.caption("• ESRS heatmap → `04_matrix/esrs_gap_heatmap.html`")


# -------------------------------------------------------------------
# Build weights based on scheme
# -------------------------------------------------------------------

def get_weights(scheme: str) -> dict[str, float]:
    if scheme.startswith("Salience"):
        return dict(STAKEHOLDER_WEIGHTS)
    if scheme.startswith("Equal"):
        n = len(STAKEHOLDER_WEIGHTS)
        return {k: 1.0 / n for k in STAKEHOLDER_WEIGHTS}
    if scheme.startswith("Regulator"):
        w = dict(STAKEHOLDER_WEIGHTS)
        w["public_authorities"] = 0.30
    elif scheme.startswith("Community"):
        w = dict(STAKEHOLDER_WEIGHTS)
        w["society"] = 0.15
        w["local_communities"] = 0.15
    else:  # Investor-first
        w = dict(STAKEHOLDER_WEIGHTS)
        w["shareholders"] = 0.20
        w["investors"] = 0.20
    total = sum(w.values())
    return {k: v / total for k, v in w.items()}


# -------------------------------------------------------------------
# Tabs
# -------------------------------------------------------------------

tab_matrix, tab_heatmap, tab_findings, tab_methodology = st.tabs(
    ["🎯 Matrix", "🔥 ESRS Gap Heatmap", "📊 Findings", "📏 Methodology"]
)

# ---------- Tab 1 — Interactive Matrix ----------

with tab_matrix:
    col_left, col_right = st.columns([3, 2])

    with col_left:
        weights_vec = get_weights(scheme)
        with st.spinner("Running Monte Carlo…"):
            draws = compute_topic_scores(weights_vec, perturb, n_draws, seed=42)

        fig = go.Figure()
        if show_target:
            fig.add_shape(type="rect", x0=2.5, x1=5.0, y0=2.5, y1=5.0,
                          fillcolor="#2ca02c", opacity=0.08, line_width=0, layer="below")
            fig.add_annotation(x=4.9, y=4.9, text="<b>TARGET ZONE</b>",
                               showarrow=False, font=dict(color="#2ca02c", size=11),
                               xanchor="right", yanchor="top")
        fig.add_hline(y=2.5, line_dash="dash", line_color="#888", line_width=1)
        fig.add_vline(x=2.5, line_dash="dash", line_color="#888", line_width=1)

        summary_rows = []
        for topic, d in draws.items():
            color = TOPIC_COLORS[topic]
            if show_scatter:
                idx = np.random.choice(n_draws, size=min(800, n_draws), replace=False)
                fig.add_trace(go.Scatter(
                    x=d["financial"][idx], y=d["impact"][idx],
                    mode="markers",
                    marker=dict(size=3, color=color, opacity=0.13),
                    name=f"{topic} draws", showlegend=False,
                    hoverinfo="skip",
                ))
            if show_ellipse:
                ell = ellipse_from_draws(d["financial"], d["impact"])
                theta = np.linspace(0, 2 * np.pi, 200)
                a = ell["w"] / 2
                b = ell["h"] / 2
                ang = math.radians(ell["angle"])
                ex = a * np.cos(theta)
                ey = b * np.sin(theta)
                rx = ex * math.cos(ang) - ey * math.sin(ang) + ell["cx"]
                ry = ex * math.sin(ang) + ey * math.cos(ang) + ell["cy"]
                fig.add_trace(go.Scatter(
                    x=rx, y=ry, mode="lines", fill="toself",
                    line=dict(color=color, width=2.5),
                    fillcolor=color, opacity=0.22,
                    name=topic, hoverinfo="name",
                ))
            cx, cy = float(np.mean(d["financial"])), float(np.mean(d["impact"]))
            fig.add_trace(go.Scatter(
                x=[cx], y=[cy], mode="markers",
                marker=dict(size=12, color=color, line=dict(color="white", width=2)),
                name=f"{topic} centroid", showlegend=False,
                hovertemplate=f"<b>{topic}</b><br>Financial: %{{x:.2f}}<br>Impact: %{{y:.2f}}<extra></extra>",
            ))
            summary_rows.append({
                "Topic": topic,
                "Impact (mean)": round(cy, 2),
                "Financial (mean)": round(cx, 2),
                "Target Zone?": "✅" if (cx >= 2.5 and cy >= 2.5) else "⚠️ borderline",
            })

        fig.update_layout(
            xaxis=dict(title="Financial Severity  (Magnitude × Probability × Horizon)",
                       range=[1, 5], dtick=0.5),
            yaxis=dict(title="Impact Severity  (Severity × Probability, salience-weighted)",
                       range=[1, 5], dtick=0.5, scaleanchor="x", scaleratio=1),
            height=660,
            template="simple_white",
            margin=dict(l=40, r=20, t=30, b=40),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown("### Position summary")
        st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

        st.markdown("### Stakeholder weights applied")
        ws_df = pd.DataFrame(
            [{"Stakeholder": k, "Weight": round(v, 3)} for k, v in weights_vec.items()]
        ).sort_values("Weight", ascending=False)
        st.dataframe(ws_df, use_container_width=True, hide_index=True)

        st.info(
            "**Try it:** flip the scheme to *Equal* or *Investor-first* — "
            "topic centroids barely move. That stability is the robustness "
            "finding we report in the paper."
        )

# ---------- Tab 2 — ESRS Gap Heatmap ----------

with tab_heatmap:
    heatmap_html = ROOT / "04_matrix" / "esrs_gap_heatmap.html"
    cov_csv = ROOT / "03_analysis" / "coverage_matrix.csv"
    st.markdown("### ESRS Gap Heatmap — Aqualia disclosure coverage")
    st.caption(
        "Prototype: 75 curated ESRS datapoints (ESRS 1/E1–E5/S1–S4/G1 + Aqualia AQ) × "
        "48 chunks from the 7 Aqualia source PDFs. TF-IDF cosine classifier."
    )
    if heatmap_html.exists():
        st.components.v1.html(heatmap_html.read_text(encoding="utf-8"), height=520, scrolling=False)
    else:
        st.warning("Run `python 03_analysis/esrs_gap_heatmap.py` to generate the heatmap.")

    if cov_csv.exists():
        cov = pd.read_csv(cov_csv)
        with st.expander("Coverage summary"):
            counts = cov["band"].value_counts().reindex(
                ["green", "amber", "red", "dark_red"], fill_value=0
            )
            st.bar_chart(counts)
        with st.expander("Per-DP detail (with top matching Aqualia chunk)"):
            st.dataframe(
                cov[["dp_id", "standard", "band", "coverage_score",
                     "top_chunk_source", "top_chunk_page", "top_chunk_text"]],
                use_container_width=True, hide_index=True,
            )

# ---------- Tab 3 — Findings ----------

with tab_findings:
    st.markdown("### Three hero findings")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div style='background:{AQUALIA_NAVY};color:white;padding:18px;border-radius:10px;height:230px'>"
                    "<h4 style='color:white;margin-top:0'>1 · Colombia outlier</h4>"
                    "<p style='font-size:13px'>Aqualia's satisfaction is 92–98% across European and institutional "
                    "segments but <b>33% in Colombia</b>. ESRS S3 folded into S4 buries this equity-access issue. "
                    "Restoring S3 converts a disclosure gap into a concession-renewal signal.</p></div>",
                    unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div style='background:{AQUALIA_NAVY};color:white;padding:18px;border-radius:10px;height:230px'>"
                    "<h4 style='color:white;margin-top:0'>2 · Digitalisation blind spot</h4>"
                    "<p style='font-size:13px'><b>2 IROs</b> in Aqualia's 2025 review — peers treat digital as "
                    "core, EU makes it Action Area 3 of 5, WEF ranks cyber top-10. Our Monte Carlo repositions "
                    "the cluster firmly into the Target Zone.</p></div>",
                    unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div style='background:{AQUALIA_NAVY};color:white;padding:18px;border-radius:10px;height:230px'>"
                    "<h4 style='color:white;margin-top:0'>3 · Green-finance differentiator</h4>"
                    "<p style='font-size:13px'>Aqualia is ahead of peers on promoting green finance to "
                    "stand-alone material status. Our roadmap proposes a <b>€500 M EU-Taxonomy-aligned green "
                    "bond programme</b> 2027–2030 → ~€31 M PV interest savings.</p></div>",
                    unsafe_allow_html=True)

    st.markdown("### The 30-second close")
    st.info(
        "Three material topics represent **€18 M/yr of net financial materiality** Aqualia's current "
        "framework under-weights. A **€440 M targeted 2027–2030 investment**, funded by our proposed "
        "**€500 M EU-Taxonomy-aligned green bond programme**, converts this drag into upside — via "
        "cost-of-capital savings, tender differentiation, and reuse-market revenue."
    )

    st.markdown("### Evidence quick-reference")
    evidence = pd.DataFrame([
        {"Claim": "73% of 83 IROs absorbed by our 3 topics", "Source": "short_list_lock.md §4"},
        {"Claim": "Colombia satisfaction 33% vs 88-98% elsewhere", "Source": "Corporate context p.15"},
        {"Claim": "Digitalisation = 2 IROs (lowest in 2025 matrix)", "Source": "AQ_2025_Material Topics"},
        {"Claim": "ESRS gap share 65-80% across 3 topics", "Source": "esrs_gap_heatmap_notes.md §3"},
        {"Claim": "€500 M bond → €31 M PV savings at 25 bp", "Source": "financials.md §3.3"},
        {"Claim": "~60% of revenue in High/Extreme water-stress basins", "Source": "water_stress.md §2"},
        {"Claim": "No topic ranking flip under 4 weighting schemes", "Source": "mc_robustness.csv"},
    ])
    st.dataframe(evidence, use_container_width=True, hide_index=True)

# ---------- Tab 4 — Methodology ----------

with tab_methodology:
    st.markdown("### The four-phase blueprint (Workshop 1)")
    st.markdown(
        "1. **Context analysis** — peer benchmarking + regulatory scan + Aqualia internal baseline\n"
        "2. **Impact materiality** — Severity × Probability × salience weight (Aqualia formula, extended)\n"
        "3. **Financial materiality** — Magnitude × Probability × Time discount\n"
        "4. **Strategic synthesis** — matrix → roadmap → 2027-2030 actions"
    )

    st.markdown("### Scoring formulas")
    st.code(
        "# Impact\n"
        "Severity      = (Scale + Scope + Remediability) / 3    # each 1–5\n"
        "Current:      score = Severity * 5\n"
        "Potential:    score = Severity * Probability\n"
        "Rescale 1–25 → 1–5 linear, then top-k aggregation over IROs.\n\n"
        "# Financial\n"
        "Severity      = Magnitude * Probability * Horizon_discount\n"
        "Horizon disc. = {short:1.00, medium:0.80, long:0.60}\n"
        "Rescale and top-k aggregate over R&Os.\n\n"
        "# Uncertainty\n"
        "Triangular(base - perturb, base, base + perturb) clipped to [1,5]\n"
        "10k Monte Carlo draws → 90% χ² ellipse.\n",
        language="text",
    )

    st.markdown("### Key files")
    st.caption("• `01_research/aqualia_2025_baseline.md` — complete extraction of the 7 Aqualia PDFs")
    st.caption("• `03_analysis/short_list_lock.md` — three-topic selection rationale")
    st.caption("• `03_analysis/scoring_rubric.md` — full threshold table with citations")
    st.caption("• `03_analysis/stakeholder_salience.md` — Mitchell-Agle-Wood 1997 applied")
    st.caption("• `03_analysis/financials.md` — € triangular distributions + Real Options")
    st.caption("• `03_analysis/matrix_mc.py` + `matrix_inputs.py` — reproducible pipeline")

st.markdown("---")
st.caption("Team: @ma731 · Datathon: IE Sustainability Datathon 2026 · Track: Double Materiality & ESG Strategy — Aqualia")

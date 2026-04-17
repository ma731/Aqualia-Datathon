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
import time
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
SAND = "#d6cdb7"

TOPIC_COLORS = {
    "T1 Water Resilience & Equitable Access": "#1f77b4",
    "T2 Digital & Cyber Infrastructure":      "#ff7f0e",
    "T3 Green Finance & Integrity":           "#2ca02c",
}

SCENARIO_BLURBS = {
    "Base": "Reference calibration from current assumptions and salience weighting.",
    "Regulatory Tightening": "Higher compliance intensity and disclosure pressure push governance-finance materiality upward.",
    "Cyber Shock": "Stress event simulates sharper digital/cyber downside with immediate operational-financial amplification.",
    "Water Stress 2030": "Escalated basin stress increases resilience urgency and financial exposure to continuity risk.",
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


def apply_scenario_adjustment(draws: dict[str, dict], scenario: str) -> dict[str, dict]:
    """Deterministic scenario overlays to support executive what-if views."""
    adjusted = {
        topic: {"impact": d["impact"].copy(), "financial": d["financial"].copy()}
        for topic, d in draws.items()
    }
    if scenario == "Base":
        return adjusted

    if scenario == "Regulatory Tightening":
        adjusted["T3 Green Finance & Integrity"]["financial"] = np.clip(
            adjusted["T3 Green Finance & Integrity"]["financial"] + 0.30, 1.0, 5.0
        )
        adjusted["T3 Green Finance & Integrity"]["impact"] = np.clip(
            adjusted["T3 Green Finance & Integrity"]["impact"] + 0.15, 1.0, 5.0
        )
        adjusted["T1 Water Resilience & Equitable Access"]["impact"] = np.clip(
            adjusted["T1 Water Resilience & Equitable Access"]["impact"] + 0.08, 1.0, 5.0
        )
    elif scenario == "Cyber Shock":
        adjusted["T2 Digital & Cyber Infrastructure"]["financial"] = np.clip(
            adjusted["T2 Digital & Cyber Infrastructure"]["financial"] + 0.45, 1.0, 5.0
        )
        adjusted["T2 Digital & Cyber Infrastructure"]["impact"] = np.clip(
            adjusted["T2 Digital & Cyber Infrastructure"]["impact"] + 0.35, 1.0, 5.0
        )
    elif scenario == "Water Stress 2030":
        adjusted["T1 Water Resilience & Equitable Access"]["financial"] = np.clip(
            adjusted["T1 Water Resilience & Equitable Access"]["financial"] + 0.50, 1.0, 5.0
        )
        adjusted["T1 Water Resilience & Equitable Access"]["impact"] = np.clip(
            adjusted["T1 Water Resilience & Equitable Access"]["impact"] + 0.40, 1.0, 5.0
        )
        adjusted["T3 Green Finance & Integrity"]["financial"] = np.clip(
            adjusted["T3 Green Finance & Integrity"]["financial"] + 0.10, 1.0, 5.0
        )
    return adjusted


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


def topic_rank_score(draws: dict[str, dict]) -> pd.DataFrame:
    rows = []
    for topic, d in draws.items():
        imp = float(np.mean(d["impact"]))
        fin = float(np.mean(d["financial"]))
        score = 0.6 * imp + 0.4 * fin
        rows.append({"Topic": topic, "Impact": imp, "Financial": fin, "Composite": score})
    df = pd.DataFrame(rows).sort_values("Composite", ascending=False).reset_index(drop=True)
    df["Rank"] = np.arange(1, len(df) + 1)
    return df[["Rank", "Topic", "Impact", "Financial", "Composite"]]


def build_radar(draws: dict[str, dict]) -> go.Figure:
    categories = ["Impact Severity", "Financial Severity", "Balance", "Urgency", "Execution Readiness"]
    fig = go.Figure()
    for topic, d in draws.items():
        imp = float(np.mean(d["impact"]))
        fin = float(np.mean(d["financial"]))
        bal = 5.0 - abs(imp - fin)
        urg = min(5.0, 0.65 * imp + 0.35 * fin + 0.2)
        exec_r = min(5.0, 0.55 * fin + 0.45 * 3.4)
        vals = [imp, fin, bal, urg, exec_r]
        fig.add_trace(
            go.Scatterpolar(
                r=vals + [vals[0]],
                theta=categories + [categories[0]],
                fill="toself",
                name=topic.replace("T1 ", "").replace("T2 ", "").replace("T3 ", ""),
                line=dict(color=TOPIC_COLORS[topic], width=2),
                opacity=0.28,
            )
        )
    fig.update_layout(
        template="simple_white",
        height=420,
        margin=dict(l=20, r=20, t=20, b=20),
        polar=dict(radialaxis=dict(range=[1, 5], showticklabels=True, ticks="outside")),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
    )
    return fig


# -------------------------------------------------------------------
# Header
# -------------------------------------------------------------------

design_mode = st.session_state.get("design_mode", "Executive Clean")
is_clean = design_mode == "Executive Clean"

_app_bg = (
    "background:#f6f9fc;"
    if is_clean
    else (
        "background: radial-gradient(1200px 500px at 8% -5%, rgba(93,185,217,0.18), transparent 45%),"
        "radial-gradient(900px 450px at 95% 5%, rgba(0,47,95,0.15), transparent 40%),#f7fbff;"
    )
)

st.markdown(
    """
    <style>
    .stApp { __APP_BG__ }
    .wow-chip {
      display:inline-block;
      padding:4px 10px;
      margin-right:6px;
      border-radius:999px;
      font-size:12px;
      font-weight:600;
      color:#002f5f;
      background:rgba(93,185,217,0.25);
      border:1px solid rgba(0,47,95,0.12);
    }
    .hero-note {
      border-left:4px solid #5db9d9;
      background:#ffffff;
      padding:10px 14px;
      border-radius:8px;
      font-size:14px;
    }
    </style>
    """.replace("__APP_BG__", _app_bg),
    unsafe_allow_html=True,
)

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
    design_mode = st.selectbox(
        "Design style",
        ("Executive Clean", "Showcase"),
        index=0 if is_clean else 1,
        key="design_mode",
        help="Executive Clean prioritizes clarity and premium restraint.",
    )
    is_clean = design_mode == "Executive Clean"

    demo_mode = st.toggle(
        "🎬 Demo Script Mode",
        value=False,
        help="Locks in pitch-safe defaults and cleaner stage visuals.",
    )

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

    scenario = st.selectbox(
        "Scenario",
        ("Base", "Regulatory Tightening", "Cyber Shock", "Water Stress 2030"),
        help="Predefined stress overlays for executive what-if views.",
    )
    st.caption(SCENARIO_BLURBS[scenario])

    n_draws = st.select_slider(
        "Draws per topic",
        options=[500, 1000, 3000, 6000, 10000],
        value=3000,
    )

    show_scatter = st.checkbox("Show draw scatter", value=True)
    show_ellipse = st.checkbox("Show 90% confidence ellipse", value=True)
    show_target = st.checkbox("Highlight Target Zone", value=True)
    presentation_mode = st.checkbox(
        "Presentation mode (less UI clutter)",
        value=False,
        help="Hides dense supporting tables for cleaner live demo.",
    )

    if demo_mode:
        scenario = "Base"
        perturb = 0.7
        n_draws = 3000
        show_scatter = False
        show_ellipse = True
        show_target = True
        presentation_mode = True
        st.success("Demo Script Mode active.")
        demo_step = st.radio(
            "Demo step",
            (
                "1) Matrix robustness",
                "2) Heatmap evidence",
                "3) Geo concentration",
                "4) Finance close",
            ),
            index=0,
        )
    else:
        demo_step = None

    st.markdown("---")
    st.markdown("### ⏱️ Auto-tour coach")
    if "tour_running" not in st.session_state:
        st.session_state["tour_running"] = False
    if "tour_idx" not in st.session_state:
        st.session_state["tour_idx"] = 0
    if "tour_start_ts" not in st.session_state:
        st.session_state["tour_start_ts"] = 0.0

    tour_script = [
        {"step": "Matrix robustness", "tab": "🎯 Matrix", "duration": 12, "line": "We use distributions, not point estimates."},
        {"step": "Heatmap traceability", "tab": "🔥 ESRS Gap Heatmap", "duration": 10, "line": "Each gap is mapped to source evidence and standard IDs."},
        {"step": "Geo concentration", "tab": "🗺️ Geo Risk", "duration": 8, "line": "Material risk is geographically concentrated and action-targetable."},
        {"step": "Finance close", "tab": "💶 Finance", "duration": 10, "line": "Funding structure converts materiality drag into quantified upside."},
    ]

    c_t1, c_t2 = st.columns(2)
    with c_t1:
        if st.button("Start tour", use_container_width=True):
            st.session_state["tour_running"] = True
            st.session_state["tour_idx"] = 0
            st.session_state["tour_start_ts"] = time.time()
    with c_t2:
        if st.button("Stop tour", use_container_width=True):
            st.session_state["tour_running"] = False

    if st.session_state["tour_running"]:
        idx = st.session_state["tour_idx"]
        if idx < len(tour_script):
            active = tour_script[idx]
            elapsed = int(time.time() - st.session_state["tour_start_ts"])
            remaining = max(0, active["duration"] - elapsed)
            st.info(
                f"Now show: **{active['tab']}** · `{active['step']}`\n\n"
                f"Say: _{active['line']}_\n\n"
                f"Time left: **{remaining}s**"
            )
            progress = min(1.0, elapsed / active["duration"] if active["duration"] else 1.0)
            st.progress(progress)
            if remaining == 0:
                st.session_state["tour_idx"] += 1
                st.session_state["tour_start_ts"] = time.time()
                st.rerun()
        else:
            st.success("Auto-tour completed. Use Findings tab for final close line.")
            st.session_state["tour_running"] = False

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

# Precompute both base and selected-scenario draws for comparisons
weights_vec = get_weights(scheme)
base_draws = compute_topic_scores(weights_vec, perturb, n_draws, seed=42)
scenario_draws = apply_scenario_adjustment(base_draws, scenario)

# Executive KPI strip
k1, k2, k3, k4 = st.columns(4)
k1.metric("Priority Topics", "3")
k2.metric("Net Underweighted Materiality", "€18M/yr")
k3.metric("Strategic Funding Ask", "€500M")
k4.metric("PV Savings Potential", "€31M")
if not is_clean:
    st.markdown(
        '<span class="wow-chip">CSRD-aligned</span>'
        '<span class="wow-chip">Monte Carlo 10k</span>'
        '<span class="wow-chip">Scenario-ready</span>'
        '<span class="wow-chip">Board-grade output</span>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="hero-note"><b>Executive thesis:</b> three topics, one quantified gap, one fundable response. '
        'Use the scenario toggle to show robustness, then close on finance.</div>',
        unsafe_allow_html=True,
    )
else:
    st.caption("Executive thesis: three topics, one quantified gap, one fundable response.")
if demo_mode:
    st.markdown(
        f"""
        <div style="margin-top:8px;padding:10px 12px;border-radius:8px;background:#fff8e6;border:1px solid #f0d98a">
          <b>Live cue:</b> {demo_step}
        </div>
        """,
        unsafe_allow_html=True,
    )

tab_matrix, tab_finance, tab_heatmap, tab_map, tab_findings, tab_methodology, tab_requirements, tab_jury = st.tabs(
    ["🎯 Matrix", "💶 Finance", "🔥 ESRS Gap Heatmap", "🗺️ Geo Risk", "📊 Findings", "📏 Methodology", "✅ Requirements Fit", "🏆 Jury Simulator"]
)

# ---------- Tab 1 — Interactive Matrix ----------

with tab_matrix:
    col_left, col_right = st.columns([3, 2])

    with col_left:
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
        for topic, d in scenario_draws.items():
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
            bcx = float(np.mean(base_draws[topic]["financial"]))
            bcy = float(np.mean(base_draws[topic]["impact"]))
            summary_rows.append({
                "Topic": topic,
                "Impact (mean)": round(cy, 2),
                "Financial (mean)": round(cx, 2),
                "ΔImpact vs Base": round(cy - bcy, 2),
                "ΔFinancial vs Base": round(cx - bcx, 2),
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
            font=dict(size=16 if demo_mode else 12),
        )
        st.plotly_chart(fig, use_container_width=True)

        if not presentation_mode:
            st.markdown("#### Portfolio shape snapshot")
            st.plotly_chart(build_radar(scenario_draws), use_container_width=True)

    with col_right:
        st.markdown("### Position summary")
        st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)
        if not is_clean:
            st.markdown("### Rank by composite decision score")
            rank_df = topic_rank_score(scenario_draws).copy()
            rank_df["Impact"] = rank_df["Impact"].round(2)
            rank_df["Financial"] = rank_df["Financial"].round(2)
            rank_df["Composite"] = rank_df["Composite"].round(2)
            st.dataframe(rank_df, use_container_width=True, hide_index=True)

        if not presentation_mode:
            st.markdown("### Stakeholder weights applied")
            ws_df = pd.DataFrame(
                [{"Stakeholder": k, "Weight": round(v, 3)} for k, v in weights_vec.items()]
            ).sort_values("Weight", ascending=False)
            st.dataframe(ws_df, use_container_width=True, hide_index=True)

        st.info(
            f"Scenario active: **{scenario}**. Use the delta columns to explain why centroids move "
            "and tie the shift to your strategic recommendation."
        )
        if demo_mode:
            st.caption(
                "Script line: 'Even under alternate assumptions, topic ordering is stable "
                "and T1/T2 remain in the Target Zone.'"
            )

# ---------- Tab 2 — Finance cockpit ----------

with tab_finance:
    st.markdown("### Green finance decision cockpit")
    spread_bps = st.slider("Green spread advantage (bps)", 10, 50, 25, 1)
    bond_size = st.select_slider("Bond programme size (€M)", options=[400, 500, 600], value=500)
    tenor = st.select_slider("Tenor (years)", options=[7, 10, 12], value=10)
    disc = st.slider("Discount rate (%)", 4.0, 10.0, 8.0, 0.5)
    annual_saving = bond_size * (spread_bps / 10000.0)
    annuity = (1 - (1 + disc / 100.0) ** (-tenor)) / (disc / 100.0)
    pv_saving = annual_saving * annuity

    f1, f2 = st.columns(2)
    with f1:
        st.metric("Annual coupon saving", f"€{annual_saving:.2f}M")
        st.metric("PV savings (model)", f"€{pv_saving:.1f}M")
    with f2:
        st.metric("CAPEX pipeline reference", "€440M")
        st.metric("Funding coverage", f"{(bond_size / 440) * 100:.0f}%")

    wf = go.Figure(
        go.Waterfall(
            orientation="v",
            measure=["relative", "relative", "total"],
            x=["CAPEX need", "PV savings benefit", "Net strategic envelope"],
            y=[440, -pv_saving, 440 - pv_saving],
            text=[f"€440M", f"-€{pv_saving:.1f}M", f"€{440 - pv_saving:.1f}M"],
            connector={"line": {"color": SAND}},
        )
    )
    wf.update_layout(template="simple_white", height=420, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(wf, use_container_width=True)

    sens = pd.DataFrame({"Spread (bps)": [15, 25, 40]})
    sens["PV Savings (€M)"] = sens["Spread (bps)"].apply(
        lambda b: (bond_size * (b / 10000.0)) * annuity
    )
    sf = go.Figure()
    sf.add_trace(
        go.Bar(
            x=sens["Spread (bps)"],
            y=sens["PV Savings (€M)"],
            marker_color=[AQUALIA_AQUA, AQUALIA_NAVY, ACCENT_RED],
            text=[f"€{v:.1f}M" for v in sens["PV Savings (€M)"]],
            textposition="outside",
        )
    )
    sf.update_layout(
        template="simple_white",
        height=320,
        xaxis_title="Spread advantage (bps)",
        yaxis_title="PV savings (€M)",
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(sf, use_container_width=True)

    st.markdown("#### Suggested tranche schedule")
    tranches = pd.DataFrame(
        {
            "Year": [2027, 2028, 2029, 2030],
            "Tranche (€M)": [150, 150, 120, 80] if bond_size == 500 else (
                [120, 120, 100, 60] if bond_size == 400 else [180, 180, 140, 100]
            ),
            "Primary use": [
                "T1 resilience CAPEX",
                "T1+T2 scale-up",
                "T2 cyber/OT-IT hardening",
                "T3 compliance + close-out",
            ],
        }
    )
    tf = go.Figure(
        go.Bar(
            x=tranches["Year"].astype(str),
            y=tranches["Tranche (€M)"],
            text=[f"€{v}M" for v in tranches["Tranche (€M)"]],
            textposition="outside",
            marker_color=[AQUALIA_NAVY, "#2c7fb8", AQUALIA_AQUA, SAND],
        )
    )
    tf.update_layout(
        template="simple_white",
        height=320,
        xaxis_title="Year",
        yaxis_title="Tranche size (€M)",
        margin=dict(l=20, r=20, t=20, b=20),
        font=dict(size=16 if demo_mode else 12),
    )
    st.plotly_chart(tf, use_container_width=True)
    if not presentation_mode:
        st.dataframe(tranches, use_container_width=True, hide_index=True)

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
    if demo_mode:
        st.caption("Script line: each gap is traceable to source evidence and standards.")

    if cov_csv.exists():
        cov = pd.read_csv(cov_csv)
        b1, b2, b3 = st.columns(3)
        with b1:
            st.metric("Datapoints tracked", int(cov["dp_id"].nunique()))
        with b2:
            red_like = int(cov["band"].isin(["red", "dark_red"]).sum())
            st.metric("Critical/priority gaps", red_like)
        with b3:
            green = int((cov["band"] == "green").sum())
            st.metric("Well-covered datapoints", green)
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

# ---------- Tab 4 — Geo risk ----------

with tab_map:
    st.markdown("### Geographic risk story — water stress and exposure")
    map_html = ROOT / "04_matrix" / "aqueduct_choropleth.html"
    map_png = ROOT / "04_matrix" / "aqueduct_exposure.png"
    c1, c2 = st.columns([2, 1])
    with c1:
        if map_html.exists():
            st.components.v1.html(map_html.read_text(encoding="utf-8"), height=520, scrolling=False)
        elif map_png.exists():
            st.image(str(map_png), use_container_width=True)
        else:
            st.warning("Aqueduct map artefact not found. Run the map pipeline to enable this view.")
    with c2:
        st.markdown("#### Executive takeaway")
        st.markdown(
            "- High/Extreme stress exposure materially pressures T1.\n"
            "- Scenario `Water Stress 2030` shifts T1 deeper into Target Zone.\n"
            "- Prioritize reuse/leak reduction CAPEX where stress and service risk intersect."
        )
        st.markdown("#### Suggested KPI bundle")
        st.markdown(
            "- NRW reduction by concession\n"
            "- Reuse ratio growth\n"
            "- Incident recovery time\n"
            "- Service continuity in stress zones"
        )
        st.markdown("#### Storytelling prompt (for live demo)")
        st.info(
            "Start from geography -> show stressed zones -> switch to Matrix tab with "
            "`Water Stress 2030` -> close with Finance tab and bond sizing."
        )
        if demo_mode:
            st.caption("Script line: risk is geographically concentrated, so CAPEX prioritization must be place-based.")

# ---------- Tab 5 — Findings ----------

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

    st.markdown("### Storyboard (live demo in 40 seconds)")
    storyboard = pd.DataFrame(
        [
            {"Step": 1, "Screen": "Matrix", "What to show": "Scenario toggle + centroid stability", "Talk track": "Robustness, not one-point estimates"},
            {"Step": 2, "Screen": "Heatmap", "What to show": "Critical gaps count + S/S3 focus", "Talk track": "Traceability from standards to evidence"},
            {"Step": 3, "Screen": "Geo Risk", "What to show": "Stress exposure map", "Talk track": "Where risk concentrates geographically"},
            {"Step": 4, "Screen": "Finance", "What to show": "Spread slider -> PV savings", "Talk track": "Actionable financing response"},
        ]
    )
    st.dataframe(storyboard, use_container_width=True, hide_index=True)
    if demo_mode:
        st.success("Close line cue: 'Three topics. €18M/yr gap. €500M fundable response.'")

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

# ---------- Tab 6 — Methodology ----------

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
    st.markdown("### Data room quick download")
    d1, d2, d3 = st.columns(3)
    cov_path = ROOT / "03_analysis" / "coverage_matrix.csv"
    rob_path = ROOT / "03_analysis" / "mc_robustness.csv"
    mtx_path = ROOT / "04_matrix" / "matrix_mc.png"
    with d1:
        if cov_path.exists():
            st.download_button("Download coverage_matrix.csv", cov_path.read_bytes(), file_name="coverage_matrix.csv")
    with d2:
        if rob_path.exists():
            st.download_button("Download mc_robustness.csv", rob_path.read_bytes(), file_name="mc_robustness.csv")
    with d3:
        if mtx_path.exists():
            st.download_button("Download matrix_mc.png", mtx_path.read_bytes(), file_name="matrix_mc.png")

# ---------- Tab 7 — Requirements fit ----------

with tab_requirements:
    st.markdown("### Datathon requirements fit (live checklist)")
    req = pd.DataFrame(
        [
            {
                "Requirement": "Identify and justify 3 material topics",
                "How dashboard supports": "Findings + Matrix ranking + scenario stress tests",
                "Evidence path": "short_list_lock.md, matrix view, storyboard",
                "Status": "✅ Covered",
            },
            {
                "Requirement": "Robust scoring methodology with assumptions",
                "How dashboard supports": "Methodology formulas + controls + downloads",
                "Evidence path": "scoring_rubric.md, financials.md, methodology tab",
                "Status": "✅ Covered",
            },
            {
                "Requirement": "Transparent double materiality matrix",
                "How dashboard supports": "Centroids, ellipses, deltas, target-zone logic",
                "Evidence path": "matrix tab + robustness CSV",
                "Status": "✅ Covered",
            },
            {
                "Requirement": "Actionable 2027–2030 strategic roadmap",
                "How dashboard supports": "Finance tranche view + findings storyboard alignment",
                "Evidence path": "deck_script.md, report roadmap sections",
                "Status": "✅ Covered",
            },
            {
                "Requirement": "Executive-level communication clarity",
                "How dashboard supports": "Demo mode, auto-tour coach, 40-second storyboard",
                "Evidence path": "demo mode + findings tab",
                "Status": "✅ Covered",
            },
        ]
    )
    st.dataframe(req, use_container_width=True, hide_index=True)
    st.info(
        "Use this tab in Q&A to show explicit alignment with evaluation criteria. "
        "It turns the dashboard from 'cool' into 'competition-ready'."
    )

# ---------- Tab 8 — Jury simulator ----------

with tab_jury:
        st.markdown("### Jury scoring simulator")
        st.caption(
            "Interactive rehearsal tool: stress-test your score under different jury priorities "
            "while staying within the official 50/50 evaluation structure."
        )

        j1, j2 = st.columns([2, 1])
        with j1:
            tech_quality = st.slider("Technical quality confidence", 60, 100, 90, 1)
            comm_quality = st.slider("Strategic communication confidence", 60, 100, 88, 1)
            delivery_factor = st.slider("Live delivery performance factor", 0.8, 1.2, 1.0, 0.01)

            stress = st.selectbox(
                "Jury emphasis stress test",
                ("Balanced jury", "Methodology-heavy jury", "Storytelling-heavy jury", "Skeptical risk jury"),
            )

            if stress == "Balanced jury":
                wt, wc = 0.50, 0.50
                stress_note = "Official split preserved: equal emphasis."
            elif stress == "Methodology-heavy jury":
                wt, wc = 0.65, 0.35
                stress_note = "Conservative technical judges scrutinize scoring and traceability."
            elif stress == "Storytelling-heavy jury":
                wt, wc = 0.35, 0.65
                stress_note = "Business-oriented judges reward narrative clarity and actionability."
            else:
                wt, wc = 0.55, 0.45
                stress_note = "Risk-focused judges penalize weak assumptions and fuzzy mitigation."

            simulated = ((tech_quality * wt) + (comm_quality * wc)) * delivery_factor
            simulated = max(0.0, min(130.0, simulated))
            wow_index = min(130.0, simulated * (1.0 + (0.05 if demo_mode else 0.0)))

            st.info(stress_note)
            st.metric("Simulated score", f"{simulated:.1f}/100")
            st.metric("Astonishment index (demo-enhanced)", f"{wow_index:.1f}/130")

        with j2:
            gauge = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=simulated,
                    number={"suffix": "/100", "font": {"size": 34}},
                    title={"text": "Score outlook"},
                    gauge={
                        "axis": {"range": [0, 120]},
                        "bar": {"color": AQUALIA_NAVY, "thickness": 0.35},
                        "steps": [
                            {"range": [0, 70], "color": "#fde2e2"},
                            {"range": [70, 90], "color": "#fff3cd"},
                            {"range": [90, 105], "color": "#d4edda"},
                            {"range": [105, 120], "color": "#c7f9cc"},
                        ],
                        "threshold": {"line": {"color": ACCENT_RED, "width": 4}, "value": 100},
                    },
                )
            )
            gauge.update_layout(height=320, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(gauge, use_container_width=True)

        st.markdown("#### Where to gain points fastest")
        gains = pd.DataFrame(
            [
                {"Lever": "Tighten assumptions (Tier C -> Tier A/B)", "Expected score lift": "+2 to +5", "Effort": "Medium"},
                {"Lever": "Sharpen 5-minute delivery timing", "Expected score lift": "+3 to +7", "Effort": "Low"},
                {"Lever": "Use auto-tour flow live", "Expected score lift": "+1 to +3", "Effort": "Low"},
                {"Lever": "Q&A attack-pack rehearsal", "Expected score lift": "+2 to +6", "Effort": "Low"},
                {"Lever": "Map + finance tabs in one narrative arc", "Expected score lift": "+2 to +4", "Effort": "Low"},
            ]
        )
        st.dataframe(gains, use_container_width=True, hide_index=True)

        st.success(
            "Winning pattern: Matrix credibility + geographic grounding + quantified financing close. "
            "Use this simulator before each rehearsal and raise weak components deliberately."
        )

st.markdown("---")
st.caption("Team: @ma731 · Datathon: IE Sustainability Datathon 2026 · Track: Double Materiality & ESG Strategy — Aqualia")

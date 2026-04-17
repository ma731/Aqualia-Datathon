"""
Double Materiality Matrix — Monte Carlo
=======================================

Runs 10k Monte Carlo draws per topic, propagating uncertainty from
IRO scores, stakeholder weights, and financial magnitude ranges
through the formulas defined in scoring_rubric.md.

Outputs
-------
04_matrix/matrix_mc.png        Matrix with 90% confidence ellipses
04_matrix/matrix_mc.html       Interactive Plotly version
04_matrix/matrix_tornado.png   Sensitivity tornado chart
03_analysis/mc_results.csv     Per-topic distribution summaries

Methodology summary (see scoring_rubric.md for full)
---------------------------------------------------
For each draw:
  For each topic T:
    1. Sample IRO inputs (Scale, Scope, Rem, Prob) from triangular
       around base, clipped to [1, 5].
    2. Sample stakeholder weights from Dirichlet centred on salience.
    3. For each IRO:
         Severity = (Scale + Scope + Rem) / 3
         if current: score = Severity * 5
         else:       score = Severity * Probability
         weighted across affected stakeholders
    4. Impact Score (T) = mean(IRO scores) scaled to 1-5.
    5. For each R&O:
         Magnitude sampled from triangular (low, base, high) scores
         Financial Severity = Magnitude * Probability * horizon_discount
    6. Financial Score (T) = mean(R&O severities) scaled to 1-5.

Target Zone threshold = 2.5 on each axis (Workshop 1 slide 17).
90% CI ellipse computed from eigendecomposition of the 2x2
covariance matrix of the (Financial, Impact) draws, at 90% chi-square
confidence (scaling factor sqrt(chi2.ppf(0.90, df=2)) ≈ 2.146).
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "08_visual_system"))
try:
    from aqualia_palette import apply_matplotlib_style, register_plotly_template
    apply_matplotlib_style()
    register_plotly_template()
    import plotly.io as _pio
    _pio.templates.default = "aqualia"
except Exception as _exc:  # pragma: no cover
    print(f"[visual system not loaded: {_exc}]")

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from matrix_inputs import (
    HORIZON_DISCOUNT,
    PERTURB,
    STAKEHOLDER_WEIGHTS,
    TOPIC_IROS,
    TOPIC_ROS,
)

ROOT = Path(__file__).resolve().parents[1]
MATRIX_OUT = ROOT / "04_matrix"
OUT_CSV = ROOT / "03_analysis" / "mc_results.csv"
MATRIX_OUT.mkdir(parents=True, exist_ok=True)

N_DRAWS = 10_000
RNG = np.random.default_rng(42)

# Chi-square-based scaling for 90% CI ellipse on a 2D Gaussian.
CHI2_90_DF2 = 4.605
ELLIPSE_K = math.sqrt(CHI2_90_DF2)  # ≈ 2.146

TOPIC_COLORS = {
    "T1 Water Resilience & Equitable Access": "#1f77b4",
    "T2 Digital & Cyber Infrastructure":      "#ff7f0e",
    "T3 Green Finance & Integrity":           "#2ca02c",
}


# -------------------------------------------------------------------
# Samplers
# -------------------------------------------------------------------


def sample_triangular(base: float, n: int, spread: float = PERTURB) -> np.ndarray:
    """Triangular(base - spread, base, base + spread), clipped to [1, 5]."""
    low = max(1.0, base - spread)
    high = min(5.0, base + spread)
    if low >= high:
        return np.full(n, base)
    return np.clip(RNG.triangular(low, base, high, size=n), 1.0, 5.0)


def sample_mag_triangular(lbh: tuple[int, int, int], n: int) -> np.ndarray:
    low, base, high = lbh
    low_f, base_f, high_f = float(low), float(base), float(high)
    # guard against degenerate triangular
    if low_f == base_f == high_f:
        return np.full(n, base_f)
    if low_f > base_f:
        base_f = low_f
    if high_f < base_f:
        high_f = base_f
    return np.clip(RNG.triangular(low_f, base_f, high_f, size=n), 1.0, 5.0)


def sample_stakeholder_weights(n: int, k: float = 100.0) -> dict[str, np.ndarray]:
    """Dirichlet centred on the salience vector; k controls spread."""
    names = list(STAKEHOLDER_WEIGHTS.keys())
    alpha = np.array([STAKEHOLDER_WEIGHTS[n_] for n_ in names]) * k
    draws = RNG.dirichlet(alpha, size=n)
    return {name: draws[:, i] for i, name in enumerate(names)}


# -------------------------------------------------------------------
# Topic-level scoring
# -------------------------------------------------------------------


# Linear rescale from Aqualia's raw 1-25 product space to a 1-5 axis that
# matches the Workshop 1 slide 17 convention. Raw 1 maps to 1, raw 25 maps
# to 5; threshold 2.5 on display corresponds to raw 10, i.e. ~40% of the
# full product range (e.g. severity 3.3 × probability 3).
def _rescale_1to25_to_1to5(x: np.ndarray) -> np.ndarray:
    return np.clip(1.0 + (x - 1.0) / 6.0, 1.0, 5.0)


def _topk_mean(arr: np.ndarray, k: int) -> np.ndarray:
    """Mean of the top-k values along axis 0. arr shape (n_items, n_draws)."""
    k = min(k, arr.shape[0])
    top = np.partition(arr, -k, axis=0)[-k:, :]
    return top.mean(axis=0)


def impact_score_for_topic(
    iros: list[dict],
    weights: dict[str, np.ndarray],
    n: int,
) -> np.ndarray:
    """Impact score per draw for one topic. Returns shape (n,)."""
    iro_scores: list[np.ndarray] = []
    for iro in iros:
        scale = sample_triangular(iro["scale"], n)
        scope = sample_triangular(iro["scope"], n)
        rem = sample_triangular(iro["rem"], n)
        severity = (scale + scope + rem) / 3.0
        if iro["current"]:
            prob = np.full(n, 5.0)
        else:
            prob = sample_triangular(iro["prob"], n)
        raw = severity * prob  # 1 to 25
        # Stakeholder-salience multiplier: IROs affecting high-salience
        # stakeholders weighted up, low-salience down, centred around 1.
        affected = np.sum([weights[s] for s in iro["stakeholders"]], axis=0)
        # baseline affected mass if a single avg stakeholder is affected
        ref_mass = np.mean([weights[s] for s in iro["stakeholders"]], axis=0) * len(iro["stakeholders"])
        with np.errstate(divide="ignore", invalid="ignore"):
            mult = np.where(ref_mass > 1e-9, affected / ref_mass, 1.0)
        raw = raw * (0.85 + 0.15 * mult)  # keep salience gentle; don't dominate severity
        iro_scores.append(raw)
    arr = np.stack(iro_scores, axis=0)  # (n_iro, n_draws)
    # Top-k aggregation: top material IROs drive the topic score.
    # k = max(3, n_iros * 0.6) — mirrors "most material subset" practice.
    k = max(3, int(round(arr.shape[0] * 0.6)))
    agg_raw = _topk_mean(arr, k)
    return _rescale_1to25_to_1to5(agg_raw)


def financial_score_for_topic(ros: list[dict], n: int) -> np.ndarray:
    """Financial score per draw for one topic. Returns shape (n,)."""
    ro_scores = []
    for ro in ros:
        mag = sample_mag_triangular(ro["mag_lbh"], n)
        prob = sample_triangular(ro["prob"], n)
        disc = HORIZON_DISCOUNT[ro["horizon"]]
        severity = mag * prob * disc  # 0.6 to 25 raw
        ro_scores.append(severity)
    arr = np.stack(ro_scores, axis=0)
    k = max(3, int(round(arr.shape[0] * 0.6)))
    agg_raw = _topk_mean(arr, k)
    return _rescale_1to25_to_1to5(agg_raw)


# -------------------------------------------------------------------
# Confidence ellipse
# -------------------------------------------------------------------


def ellipse_params(x: np.ndarray, y: np.ndarray) -> dict:
    cov = np.cov(x, y)
    vals, vecs = np.linalg.eigh(cov)
    order = vals.argsort()[::-1]
    vals = vals[order]
    vecs = vecs[:, order]
    angle = math.degrees(math.atan2(vecs[1, 0], vecs[0, 0]))
    width = 2 * ELLIPSE_K * math.sqrt(max(vals[0], 1e-9))
    height = 2 * ELLIPSE_K * math.sqrt(max(vals[1], 1e-9))
    return {
        "mean_x": float(np.mean(x)),
        "mean_y": float(np.mean(y)),
        "width": float(width),
        "height": float(height),
        "angle": float(angle),
        "cov": cov.tolist(),
    }


# -------------------------------------------------------------------
# Main — run MC, produce CSV + figures
# -------------------------------------------------------------------


def main() -> None:
    print("== Double Materiality Matrix — Monte Carlo ==")
    print(f"Draws per topic: {N_DRAWS}")

    results: list[dict] = []
    draws_by_topic: dict[str, dict] = {}

    weights = sample_stakeholder_weights(N_DRAWS)

    for topic_name, iros in TOPIC_IROS.items():
        impact = impact_score_for_topic(iros, weights, N_DRAWS)
        financial = financial_score_for_topic(TOPIC_ROS[topic_name], N_DRAWS)
        p5, p50, p95 = np.percentile(impact, [5, 50, 95])
        f5, f50, f95 = np.percentile(financial, [5, 50, 95])

        ell = ellipse_params(financial, impact)
        in_target_zone = (ell["mean_x"] >= 2.5) and (ell["mean_y"] >= 2.5)

        print(
            f"  {topic_name}:\n"
            f"     Impact    mean={impact.mean():.2f}  "
            f"[p5={p5:.2f}, p50={p50:.2f}, p95={p95:.2f}]\n"
            f"     Financial mean={financial.mean():.2f}  "
            f"[p5={f5:.2f}, p50={f50:.2f}, p95={f95:.2f}]\n"
            f"     Target Zone: {'YES' if in_target_zone else 'no'}"
        )

        results.append({
            "topic": topic_name,
            "impact_mean": impact.mean(),
            "impact_p5": p5,
            "impact_p50": p50,
            "impact_p95": p95,
            "financial_mean": financial.mean(),
            "financial_p5": f5,
            "financial_p50": f50,
            "financial_p95": f95,
            "ellipse_width": ell["width"],
            "ellipse_height": ell["height"],
            "ellipse_angle": ell["angle"],
            "in_target_zone": in_target_zone,
        })
        draws_by_topic[topic_name] = {"impact": impact, "financial": financial, "ellipse": ell}

    df = pd.DataFrame(results)
    df.to_csv(OUT_CSV, index=False)
    print(f"\nWrote {OUT_CSV.relative_to(ROOT)}")

    # -------------------------------------------------------------------
    # Matrix render (matplotlib static)
    # -------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 9))

    # Target zone shading
    ax.fill_between([2.5, 5.0], 2.5, 5.0, color="#2ca02c", alpha=0.07, zorder=0)
    ax.axhline(2.5, color="#888", linewidth=0.8, linestyle="--")
    ax.axvline(2.5, color="#888", linewidth=0.8, linestyle="--")
    ax.text(4.95, 4.9, "TARGET ZONE", fontsize=9, ha="right", va="top",
            color="#2ca02c", fontweight="bold", alpha=0.7)

    for topic_name, d in draws_by_topic.items():
        color = TOPIC_COLORS[topic_name]
        # Thin scatter of a subsample for texture
        idx = RNG.choice(N_DRAWS, size=1200, replace=False)
        ax.scatter(d["financial"][idx], d["impact"][idx], s=4,
                   color=color, alpha=0.08)
        # Ellipse
        ell = d["ellipse"]
        patch = mpatches.Ellipse(
            xy=(ell["mean_x"], ell["mean_y"]),
            width=ell["width"],
            height=ell["height"],
            angle=ell["angle"],
            facecolor=color,
            alpha=0.18,
            edgecolor=color,
            linewidth=2.0,
            label=topic_name,
        )
        ax.add_patch(patch)
        # Centre marker
        ax.plot(ell["mean_x"], ell["mean_y"], marker="o",
                markersize=9, color=color, markeredgecolor="white",
                markeredgewidth=1.5, zorder=5)

    # Threshold quadrant corner labels
    ax.text(0.05, 4.9, "High impact\nLow financial", fontsize=8, color="#666", va="top")
    ax.text(4.95, 0.15, "Low impact\nHigh financial", fontsize=8, color="#666", ha="right")

    ax.set_xlim(1.0, 5.0)
    ax.set_ylim(1.0, 5.0)
    ax.set_xlabel("Financial Severity (outside-in)  —  Magnitude × Probability × Horizon", fontsize=11)
    ax.set_ylabel("Impact Severity (inside-out)  —  Severity × Probability, salience-weighted", fontsize=11)
    ax.set_title(
        "Aqualia Double Materiality Matrix — Monte Carlo with 90% CI ellipses\n"
        f"({N_DRAWS:,} draws per topic; ellipse drawn at 90% χ² containment)",
        fontsize=12,
    )
    leg = ax.legend(loc="lower left", frameon=True, fontsize=9,
                    title="Material topic (centroid = mean)", title_fontsize=9)
    leg.get_frame().set_linewidth(0.5)
    ax.grid(True, alpha=0.2, linestyle=":")
    ax.set_aspect("equal", adjustable="box")
    plt.tight_layout()
    out_png = MATRIX_OUT / "matrix_mc.png"
    plt.savefig(out_png, dpi=180, bbox_inches="tight")
    plt.close()
    print(f"Wrote {out_png.relative_to(ROOT)}")

    # -------------------------------------------------------------------
    # Plotly interactive
    # -------------------------------------------------------------------
    try:
        import plotly.graph_objects as go

        fig2 = go.Figure()
        # Target zone shading
        fig2.add_shape(
            type="rect", x0=2.5, x1=5.0, y0=2.5, y1=5.0,
            fillcolor="#2ca02c", opacity=0.08, line_width=0, layer="below",
        )
        fig2.add_hline(y=2.5, line_dash="dash", line_color="#888", line_width=1)
        fig2.add_vline(x=2.5, line_dash="dash", line_color="#888", line_width=1)

        for topic_name, d in draws_by_topic.items():
            color = TOPIC_COLORS[topic_name]
            # subsample for scatter
            idx = RNG.choice(N_DRAWS, size=800, replace=False)
            fig2.add_trace(go.Scatter(
                x=d["financial"][idx], y=d["impact"][idx],
                mode="markers",
                marker=dict(size=3, color=color, opacity=0.12),
                name=topic_name + " (draws)",
                hoverinfo="skip",
                showlegend=False,
            ))
            # Ellipse approximated by param curve
            ell = d["ellipse"]
            theta = np.linspace(0, 2 * np.pi, 200)
            a = ell["width"] / 2
            b = ell["height"] / 2
            ang = math.radians(ell["angle"])
            ex = a * np.cos(theta)
            ey = b * np.sin(theta)
            rx = ex * math.cos(ang) - ey * math.sin(ang) + ell["mean_x"]
            ry = ex * math.sin(ang) + ey * math.cos(ang) + ell["mean_y"]
            fig2.add_trace(go.Scatter(
                x=rx, y=ry, mode="lines",
                line=dict(color=color, width=2.5),
                fill="toself", fillcolor=color, opacity=0.22,
                name=topic_name,
                hoverinfo="name",
            ))
            fig2.add_trace(go.Scatter(
                x=[ell["mean_x"]], y=[ell["mean_y"]],
                mode="markers",
                marker=dict(size=11, color=color, line=dict(color="white", width=2)),
                name=topic_name + " (centroid)",
                showlegend=False,
                hovertemplate=(
                    f"<b>{topic_name}</b><br>"
                    "Financial: %{x:.2f}<br>Impact: %{y:.2f}<extra></extra>"
                ),
            ))

        fig2.update_layout(
            title=(
                "Aqualia Double Materiality Matrix — Monte Carlo<br>"
                f"<sub>{N_DRAWS:,} draws per topic · 90% χ² confidence ellipses</sub>"
            ),
            xaxis=dict(title="Financial Severity", range=[1.0, 5.0], dtick=0.5),
            yaxis=dict(title="Impact Severity", range=[1.0, 5.0], dtick=0.5,
                       scaleanchor="x", scaleratio=1),
            width=900, height=800,
            template="simple_white",
        )
        fig2.add_annotation(x=4.9, y=4.9, text="<b>TARGET ZONE</b>",
                            showarrow=False, font=dict(color="#2ca02c", size=11),
                            xanchor="right", yanchor="top")
        out_html = MATRIX_OUT / "matrix_mc.html"
        fig2.write_html(str(out_html))
        print(f"Wrote {out_html.relative_to(ROOT)}")
    except Exception as e:
        print(f"[plotly skipped: {e}]")

    # -------------------------------------------------------------------
    # Tornado — one-at-a-time sensitivity
    # -------------------------------------------------------------------
    print("\n== Tornado sensitivity (one-at-a-time on base inputs) ==")
    tornado_rows = []
    N_TOR = 3000
    weights_tor = sample_stakeholder_weights(N_TOR)
    # For each topic, perturb each IRO's Scale or Prob by ±1 (clipped) and
    # each R&O's base magnitude by ±1 and record delta in topic's mean score.
    for topic_name, iros in TOPIC_IROS.items():
        base_impact_mean = np.mean(impact_score_for_topic(iros, weights_tor, N_TOR))
        base_financial_mean = np.mean(financial_score_for_topic(TOPIC_ROS[topic_name], N_TOR))

        for i, iro in enumerate(iros):
            for key in ("scale", "prob"):
                base_val = iro[key]
                # Perturb up
                up = dict(iro, **{key: min(5, base_val + 1)})
                # Perturb down
                dn = dict(iro, **{key: max(1, base_val - 1)})
                iros_up = iros[:i] + [up] + iros[i+1:]
                iros_dn = iros[:i] + [dn] + iros[i+1:]
                impact_up = impact_score_for_topic(iros_up, weights_tor, N_TOR).mean()
                impact_dn = impact_score_for_topic(iros_dn, weights_tor, N_TOR).mean()
                tornado_rows.append({
                    "topic": topic_name, "axis": "Impact",
                    "input": f"{iro['id']}.{key}",
                    "base": base_val,
                    "swing": impact_up - impact_dn,
                    "low": impact_dn - base_impact_mean,
                    "high": impact_up - base_impact_mean,
                })

        for i, ro in enumerate(TOPIC_ROS[topic_name]):
            low, base_v, high_v = ro["mag_lbh"]
            up = dict(ro, mag_lbh=(low, min(5, base_v + 1), min(5, high_v + 1)))
            dn = dict(ro, mag_lbh=(max(1, low - 1), max(1, base_v - 1), high_v))
            ros_up = TOPIC_ROS[topic_name][:i] + [up] + TOPIC_ROS[topic_name][i+1:]
            ros_dn = TOPIC_ROS[topic_name][:i] + [dn] + TOPIC_ROS[topic_name][i+1:]
            fin_up = financial_score_for_topic(ros_up, N_TOR).mean()
            fin_dn = financial_score_for_topic(ros_dn, N_TOR).mean()
            tornado_rows.append({
                "topic": topic_name, "axis": "Financial",
                "input": f"{ro['id']}.mag",
                "base": base_v,
                "swing": fin_up - fin_dn,
                "low": fin_dn - base_financial_mean,
                "high": fin_up - base_financial_mean,
            })

    tdf = pd.DataFrame(tornado_rows)
    tdf["abs_swing"] = tdf["swing"].abs()
    tdf.to_csv(ROOT / "03_analysis" / "mc_tornado.csv", index=False)
    print(f"Wrote {(ROOT / '03_analysis' / 'mc_tornado.csv').relative_to(ROOT)}")

    # Plot tornado: top 6 inputs per topic (by abs swing), single combined fig.
    top_k = 6
    rows = []
    for topic_name in TOPIC_IROS.keys():
        sub = tdf[tdf["topic"] == topic_name].nlargest(top_k, "abs_swing")
        for _, r in sub.iterrows():
            rows.append((topic_name, r["input"], r["low"], r["high"], r["axis"]))

    fig3, axes = plt.subplots(1, 3, figsize=(16, 7), sharex=False)
    for ax_, topic_name in zip(axes, TOPIC_IROS.keys()):
        color = TOPIC_COLORS[topic_name]
        sub = tdf[tdf["topic"] == topic_name].nlargest(top_k, "abs_swing")[::-1]
        labels = [f"{r['input']}  ({r['axis'][0]})" for _, r in sub.iterrows()]
        lows = sub["low"].to_numpy()
        highs = sub["high"].to_numpy()
        centres = np.zeros_like(lows)
        for j, (lo, hi) in enumerate(zip(lows, highs)):
            left = min(lo, hi)
            width = abs(hi - lo)
            ax_.barh(j, width, left=left, color=color, alpha=0.75,
                     edgecolor=color, linewidth=1.2)
            ax_.plot([lo, hi], [j, j], color=color, linewidth=0)
        ax_.axvline(0, color="#333", linewidth=0.6)
        ax_.set_yticks(range(len(labels)))
        ax_.set_yticklabels(labels, fontsize=8)
        ax_.set_xlabel("Δ topic score vs base", fontsize=9)
        ax_.set_title(topic_name, fontsize=10, color=color)
        ax_.grid(True, axis="x", alpha=0.2, linestyle=":")
    fig3.suptitle(
        "Sensitivity Tornado — top 6 inputs per topic "
        "(Impact axis marked I · Financial axis marked F)",
        fontsize=11,
    )
    plt.tight_layout()
    out_tornado = MATRIX_OUT / "matrix_tornado.png"
    plt.savefig(out_tornado, dpi=180, bbox_inches="tight")
    plt.close()
    print(f"Wrote {out_tornado.relative_to(ROOT)}")

    # -------------------------------------------------------------------
    # Robust-material check (Workshop 1 Checklist #3 trace)
    # -------------------------------------------------------------------
    print("\n== Robustness (alternate stakeholder weightings) ==")
    alt_weightings = {
        "Equal": {k: 1.0 / len(STAKEHOLDER_WEIGHTS) for k in STAKEHOLDER_WEIGHTS},
        "Regulator-heavy": {**STAKEHOLDER_WEIGHTS, "public_authorities": 0.30},
        "Community-first": {**STAKEHOLDER_WEIGHTS, "society": 0.15, "local_communities": 0.15},
        "Investor-first": {**STAKEHOLDER_WEIGHTS, "shareholders": 0.20, "investors": 0.20},
    }
    robust_rows = []
    N_ROB = 3000
    for scheme, raw in alt_weightings.items():
        s = sum(raw.values())
        weights_alt = {k: np.full(N_ROB, v / s) for k, v in raw.items()}
        for topic_name, iros in TOPIC_IROS.items():
            imp = impact_score_for_topic(iros, weights_alt, N_ROB).mean()
            fin = financial_score_for_topic(TOPIC_ROS[topic_name], N_ROB).mean()
            robust_rows.append({
                "scheme": scheme,
                "topic": topic_name,
                "impact_mean": round(imp, 2),
                "financial_mean": round(fin, 2),
                "in_target_zone": bool(imp >= 2.5 and fin >= 2.5),
            })
    rdf = pd.DataFrame(robust_rows)
    rdf.to_csv(ROOT / "03_analysis" / "mc_robustness.csv", index=False)
    print(f"Wrote {(ROOT / '03_analysis' / 'mc_robustness.csv').relative_to(ROOT)}")
    print(rdf.to_string(index=False))


if __name__ == "__main__":
    main()

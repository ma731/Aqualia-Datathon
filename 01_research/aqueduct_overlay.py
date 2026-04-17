"""
WRI Aqueduct overlay — Aqualia exposure.

Produces two exhibits:
  04_matrix/aqueduct_exposure.png   static matplotlib bar chart
  04_matrix/aqueduct_choropleth.html interactive Plotly country map

Data: hand-curated from WRI Aqueduct 4.0 baseline + BAU-2030
projection, cited per row. Source CSV: 02_sources/aqueduct/aqualia_exposure.csv.

If you later acquire the full Aqueduct 4.0 shapefile, swap the CSV
join for a geopandas-based polygon overlay (see water_stress.md §5).
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "08_visual_system"))
try:
    from aqualia_palette import apply_matplotlib_style, PALETTE, register_plotly_template
    apply_matplotlib_style()
    register_plotly_template()
    import plotly.io as pio
    pio.templates.default = "aqualia"
except Exception as exc:  # pragma: no cover
    print(f"[visual system not loaded: {exc}]")

import matplotlib.patches as mpatches

EX_CSV = ROOT / "02_sources" / "aqueduct" / "aqualia_exposure.csv"
OUT_PNG = ROOT / "04_matrix" / "aqueduct_exposure.png"
OUT_HTML = ROOT / "04_matrix" / "aqueduct_choropleth.html"

BAND_COLOURS = {
    "Low":            "#7fbf7f",
    "Low-Medium":     "#b8e0c2",
    "Medium-High":    "#f2b039",
    "High":           "#e48a3e",
    "Extremely High": "#c83c35",
    "Mixed":          "#bbbbbb",
}
BAND_ORDER = ["Low", "Low-Medium", "Medium-High", "High", "Extremely High", "Mixed"]
BAND_NUM = {b: i for i, b in enumerate(BAND_ORDER)}


def render_matplotlib(df: pd.DataFrame) -> None:
    df = df.copy()
    df["band_num_2024"] = df["bws_category_2024"].map(BAND_NUM)
    df["band_num_2030"] = df["bws_category_2030_BAU"].map(BAND_NUM)

    # Sort by 2024 stress descending; tie-break by revenue share descending
    df = df.sort_values(
        by=["band_num_2024", "revenue_share_pct"], ascending=[False, False]
    ).reset_index(drop=True)

    fig, (ax_bar, ax_sum) = plt.subplots(
        1, 2, figsize=(15, max(7, 0.45 * len(df))),
        gridspec_kw={"width_ratios": [3, 1]},
    )

    # -----------------------------------------------------------
    # Left panel: per-region horizontal bar chart
    # -----------------------------------------------------------
    y = np.arange(len(df))
    colours_24 = df["bws_category_2024"].map(BAND_COLOURS).tolist()
    colours_30 = df["bws_category_2030_BAU"].map(BAND_COLOURS).tolist()
    labels = [f"{r.country} — {r.region_label}" for r in df.itertuples()]

    # Draw 2024 bar + 2030 projection as a shadow extending beyond
    ax_bar.barh(y - 0.18, df["bws_score_2024"], height=0.34,
                color=colours_24, edgecolor="white", linewidth=0.5,
                label="Baseline 2024")
    ax_bar.barh(y + 0.18, df["bws_score_2030_BAU"], height=0.34,
                color=colours_30, edgecolor="white", linewidth=0.5,
                alpha=0.75, label="BAU-2030 projection")

    # Revenue-share bubbles on the right
    for i, r in df.iterrows():
        if pd.notna(r.revenue_share_pct) and r.revenue_share_pct > 0:
            size = max(40, 30 * float(r.revenue_share_pct) ** 0.9)
            ax_bar.scatter(5.15, i, s=size, color=PALETTE["navy"],
                           alpha=0.85, edgecolor="white", linewidth=1.2)
            ax_bar.annotate(f"{int(r.revenue_share_pct)}%",
                            (5.15, i), xytext=(10, 0),
                            textcoords="offset points",
                            va="center", fontsize=8, color=PALETTE["navy"])

    ax_bar.set_yticks(y)
    ax_bar.set_yticklabels(labels, fontsize=9)
    ax_bar.invert_yaxis()
    ax_bar.set_xlim(0, 6.0)
    ax_bar.set_xticks([0, 1, 2, 3, 4, 5])
    ax_bar.set_xticklabels(["0", "Low\n10%", "Med-Low\n20%", "Med-High\n40%",
                            "High\n80%", "Extreme\n>80%"])
    ax_bar.set_xlabel("WRI Aqueduct 4.0 Baseline Water Stress  (withdrawals ÷ supply)",
                      fontsize=10)
    ax_bar.set_title(
        "Aqualia water-stress exposure — 60% of revenue in High or Extreme stress basins today",
        fontsize=12, color=PALETTE["navy"], fontweight="bold", loc="left",
    )
    ax_bar.axvline(3.0, color="#888", linewidth=0.7, linestyle="--")
    ax_bar.axvline(4.0, color="#c83c35", linewidth=0.7, linestyle="--")

    # legend
    legend_handles = [
        mpatches.Patch(color=BAND_COLOURS[b], label=b)
        for b in BAND_ORDER
    ]
    legend_handles.append(mpatches.Patch(color=PALETTE["navy"], label="Revenue share (bubble)"))
    ax_bar.legend(handles=legend_handles, loc="lower right",
                  fontsize=8, frameon=False, ncol=2)

    # -----------------------------------------------------------
    # Right panel: summary KPIs
    # -----------------------------------------------------------
    ax_sum.axis("off")
    stressed_mask = df["bws_category_2024"].isin(["High", "Extremely High"])
    stressed_rev = df.loc[stressed_mask, "revenue_share_pct"].sum()
    stressed_rev_30 = df.loc[df["bws_category_2030_BAU"].isin(
        ["High", "Extremely High"]), "revenue_share_pct"].sum()

    kpis = [
        ("Revenue in High or\nExtreme stress today", f"~{int(stressed_rev)}%"),
        ("Same share under\nBAU-2030 scenario", f"~{int(stressed_rev_30)}%"),
        ("Segura basin category", "Extremely High"),
        ("Colombia satisfaction", "33%"),
    ]
    for i, (label, value) in enumerate(kpis):
        ybox = 0.92 - i * 0.21
        ax_sum.add_patch(mpatches.FancyBboxPatch(
            (0.05, ybox - 0.14), 0.9, 0.17,
            boxstyle="round,pad=0.01,rounding_size=0.015",
            linewidth=0.7, edgecolor=PALETTE["grid"],
            facecolor="white",
            transform=ax_sum.transAxes,
        ))
        ax_sum.text(0.1, ybox - 0.03, label, fontsize=9,
                    color=PALETTE["slate"], transform=ax_sum.transAxes)
        ax_sum.text(0.1, ybox - 0.10, value, fontsize=18,
                    color=PALETTE["navy"], fontweight="bold",
                    transform=ax_sum.transAxes)

    ax_sum.text(0.05, 0.03,
                "Source: WRI Aqueduct 4.0 baseline + BAU-2030 (SSP3/RCP 7.0)\n"
                "Aqualia geography from Corporate context 2025 §2.\n"
                "Bubble size on left panel = revenue share.",
                transform=ax_sum.transAxes, fontsize=7, color=PALETTE["slate"])

    plt.tight_layout()
    plt.savefig(OUT_PNG, dpi=180, bbox_inches="tight")
    plt.close()
    print(f"Wrote {OUT_PNG.relative_to(ROOT)}")


def render_plotly(df: pd.DataFrame) -> None:
    # Aggregate to country level for choropleth
    agg = df.groupby(["country", "iso3"], as_index=False).agg(
        rev_share_pct=("revenue_share_pct", "sum"),
        avg_bws_2024=("bws_score_2024", "mean"),
        avg_bws_2030=("bws_score_2030_BAU", "mean"),
        worst_band_2024=("bws_category_2024",
                         lambda s: max(s, key=lambda b: BAND_NUM.get(b, -1))),
        satisfaction=("satisfaction_2024", "first"),
    )
    agg["avg_bws_2024"] = agg["avg_bws_2024"].round(2)
    agg["avg_bws_2030"] = agg["avg_bws_2030"].round(2)

    import plotly.graph_objects as go
    fig = go.Figure(go.Choropleth(
        locations=agg["iso3"],
        z=agg["avg_bws_2024"],
        locationmode="ISO-3",
        zmin=1, zmax=5,
        colorscale=[
            [0.00, "#7fbf7f"],
            [0.25, "#b8e0c2"],
            [0.50, "#f2b039"],
            [0.75, "#e48a3e"],
            [1.00, "#c83c35"],
        ],
        colorbar=dict(
            title="BWS score<br>(1=Low, 5=Extreme)",
            tickvals=[1, 2, 3, 4, 5],
            ticktext=["Low", "Low-Med", "Med-High", "High", "Extreme"],
        ),
        marker_line_color="white",
        marker_line_width=0.4,
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Avg BWS (2024): %{z:.2f}<br>"
            "Worst-basin category: %{customdata[1]}<br>"
            "Revenue share: %{customdata[2]:.0f}%<br>"
            "2024 satisfaction: %{customdata[3]}<br>"
            "<extra></extra>"
        ),
        customdata=agg[["country", "worst_band_2024", "rev_share_pct",
                        "satisfaction"]].values,
    ))
    fig.update_layout(
        title=dict(
            text="Aqualia service geography × WRI Aqueduct 4.0 baseline water stress",
            x=0.02,
        ),
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type="natural earth",
            bgcolor="#ffffff",
            lonaxis=dict(range=[-90, 20]),
            lataxis=dict(range=[-5, 62]),
        ),
        height=620,
        margin=dict(l=20, r=20, t=60, b=20),
    )
    fig.write_html(str(OUT_HTML), include_plotlyjs="cdn")
    print(f"Wrote {OUT_HTML.relative_to(ROOT)}")


def main() -> None:
    df = pd.read_csv(EX_CSV)
    print(f"Loaded {len(df)} region rows from {EX_CSV.name}")
    render_matplotlib(df)
    render_plotly(df)

    # Summary print for the report
    stressed = df[df["bws_category_2024"].isin(["High", "Extremely High"])]
    stressed_30 = df[df["bws_category_2030_BAU"].isin(["High", "Extremely High"])]
    print(f"\nRevenue in High + Extreme stress (2024):  {stressed['revenue_share_pct'].sum():.0f}%")
    print(f"Revenue in High + Extreme stress (BAU-2030): {stressed_30['revenue_share_pct'].sum():.0f}%")


if __name__ == "__main__":
    main()

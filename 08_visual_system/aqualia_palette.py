"""
Aqualia Datathon — Visual System (palette + styles).

Usage
-----
    from aqualia_palette import (
        PALETTE, TOPIC_COLORS, apply_matplotlib_style,
        register_plotly_template,
    )

    apply_matplotlib_style()      # sets rcParams
    register_plotly_template()    # registers 'aqualia' Plotly template
"""
from __future__ import annotations

import matplotlib as mpl
from matplotlib import font_manager


# -------------------------------------------------------------------
# Palette
# -------------------------------------------------------------------

PALETTE = {
    "navy":       "#002f5f",
    "aqua":       "#5db9d9",
    "deep":       "#0b4f74",
    "sand":       "#d6cdb7",
    "slate":      "#4a5663",
    "paper":      "#ffffff",
    "grid":       "#e6e8eb",
    "red":        "#c83c35",
    "amber":      "#f2b039",
    "green":      "#1b7f3b",
    "darkred":    "#6e1c1c",
}

TOPIC_COLORS = {
    "T1 Water Resilience & Equitable Access": "#1f77b4",
    "T2 Digital & Cyber Infrastructure":      "#ff7f0e",
    "T3 Green Finance & Integrity":           "#2ca02c",
}

BAND_COLOURS = {
    "green":    PALETTE["green"],
    "amber":    PALETTE["amber"],
    "red":      PALETTE["red"],
    "dark_red": PALETTE["darkred"],
    "grey":     "#bbbbbb",
}

# Ordered list for matplotlib's default cycler.
SEQUENCE = [
    TOPIC_COLORS["T1 Water Resilience & Equitable Access"],
    TOPIC_COLORS["T2 Digital & Cyber Infrastructure"],
    TOPIC_COLORS["T3 Green Finance & Integrity"],
    PALETTE["navy"],
    PALETTE["aqua"],
    PALETTE["deep"],
    PALETTE["amber"],
    PALETTE["red"],
    PALETTE["darkred"],
]


# -------------------------------------------------------------------
# Matplotlib
# -------------------------------------------------------------------

def _preferred_font() -> str:
    """Return 'Inter' if installed locally, else fall back."""
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in ("Inter", "Helvetica Neue", "Arial", "DejaVu Sans"):
        if name in available:
            return name
    return "DejaVu Sans"


def apply_matplotlib_style() -> None:
    """Set matplotlib rcParams to the Aqualia visual system."""
    font = _preferred_font()

    mpl.rcParams.update({
        # Typography
        "font.family": font,
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.labelsize": 10,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
        "figure.titlesize": 14,

        # Colour cycler
        "axes.prop_cycle": mpl.cycler(color=SEQUENCE),

        # Spines
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": PALETTE["slate"],
        "axes.linewidth": 0.8,
        "axes.labelcolor": PALETTE["slate"],
        "xtick.color": PALETTE["slate"],
        "ytick.color": PALETTE["slate"],

        # Grid
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": PALETTE["grid"],
        "grid.linewidth": 0.6,
        "grid.linestyle": "-",

        # Figure
        "figure.facecolor": PALETTE["paper"],
        "axes.facecolor": PALETTE["paper"],
        "savefig.facecolor": PALETTE["paper"],
        "savefig.edgecolor": PALETTE["paper"],
        "savefig.dpi": 180,
        "savefig.bbox": "tight",

        # Lines
        "lines.linewidth": 2.0,
        "patch.edgecolor": "none",
    })


# -------------------------------------------------------------------
# Plotly
# -------------------------------------------------------------------

def register_plotly_template(name: str = "aqualia") -> None:
    """Register 'aqualia' template. Call once per process."""
    import plotly.graph_objects as go
    import plotly.io as pio

    layout = go.Layout(
        font=dict(family="Inter, Helvetica Neue, Arial, sans-serif",
                  size=12, color=PALETTE["slate"]),
        title=dict(font=dict(family="Inter, Helvetica Neue, Arial, sans-serif",
                             size=16, color=PALETTE["navy"])),
        paper_bgcolor=PALETTE["paper"],
        plot_bgcolor=PALETTE["paper"],
        colorway=SEQUENCE,
        xaxis=dict(
            gridcolor=PALETTE["grid"], gridwidth=0.6, zeroline=False,
            linecolor=PALETTE["slate"], linewidth=0.8,
            tickcolor=PALETTE["slate"], ticks="outside",
        ),
        yaxis=dict(
            gridcolor=PALETTE["grid"], gridwidth=0.6, zeroline=False,
            linecolor=PALETTE["slate"], linewidth=0.8,
            tickcolor=PALETTE["slate"], ticks="outside",
        ),
        legend=dict(
            bgcolor="rgba(255,255,255,0)",
            bordercolor=PALETTE["grid"], borderwidth=0,
        ),
        margin=dict(l=50, r=30, t=60, b=50),
    )
    pio.templates[name] = go.layout.Template(layout=layout)

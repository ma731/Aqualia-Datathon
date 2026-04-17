"""
Re-render hero figures with the Aqualia visual system.
Run:  python 08_visual_system/figure_rebuild.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "08_visual_system"))
sys.path.insert(0, str(ROOT / "03_analysis"))

from aqualia_palette import apply_matplotlib_style, register_plotly_template  # noqa: E402

apply_matplotlib_style()
register_plotly_template()

# Kick the analysis scripts, which now pick up our rc + plotly template
import subprocess

print("→ Re-running Monte Carlo matrix with visual system…")
subprocess.run([sys.executable, "-X", "utf8",
                str(ROOT / "03_analysis" / "matrix_mc.py")],
               check=True, cwd=ROOT / "03_analysis")

print("→ Re-running ESRS gap heatmap with visual system…")
subprocess.run([sys.executable, "-X", "utf8",
                str(ROOT / "03_analysis" / "esrs_gap_heatmap.py")],
               check=True, cwd=ROOT)

print("\nAll hero figures rebuilt. Check 04_matrix/.")

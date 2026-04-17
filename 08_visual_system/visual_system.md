# Aqualia Datathon — Visual System

*Apply everywhere. Report, deck, Streamlit, all exports. Consistency =
credibility.*

---

## Palette

| Name | Hex | Role |
|---|---|---|
| **Aqualia Navy** | `#002f5f` | Primary — headers, titles, highlights |
| **Aqualia Aqua** | `#5db9d9` | Secondary — accents, links, highlights |
| **Aqualia Deep** | `#0b4f74` | Mid-tone, secondary bars |
| **Aqualia Sand** | `#d6cdb7` | Neutral, card backgrounds |
| **Slate** | `#4a5663` | Body text on light backgrounds |
| **Paper** | `#ffffff` | Canvas |
| **Subtle grid** | `#e6e8eb` | Grid lines, dividers |
| **Accent Red** | `#c83c35` | Risk / warning / red cells only |
| **Amber** | `#f2b039` | Amber in bands |
| **Green** | `#1b7f3b` | Positive / strong disclosure |
| **Dark Red** | `#6e1c1c` | Gap / critical |

**Topic colours** (Monte Carlo matrix + all topic-coded visuals):

| Topic | Hex |
|---|---|
| **T1 Water Resilience & Equitable Access** | `#1f77b4` (navy-blue) |
| **T2 Digital & Cyber Infrastructure** | `#ff7f0e` (orange) |
| **T3 Green Finance & Integrity** | `#2ca02c` (green) |

Pick the palette and stick with it. Never introduce a colour that is
not listed above.

---

## Typography

- **Inter** (Open-source, weights Regular 400 and Bold 700).
- Headings: Inter Bold.
- Body: Inter Regular.
- Numbers / data tables: Inter Regular, tabular-nums variant if the
  tool supports it.
- Fallback order in CSS: `Inter, "Helvetica Neue", Arial, sans-serif`.

No second typeface. No italics except for paper titles in references
and for occasional emphasis (avoid italicising whole paragraphs).

---

## Type scale (for slides and report)

| Use | Size | Weight |
|---|---|---|
| Slide title | 28 pt | Bold |
| Slide subtitle | 16 pt | Regular |
| Slide body | 14 pt | Regular |
| Slide caption | 10 pt | Regular |
| Report H1 | 18 pt | Bold |
| Report H2 | 14 pt | Bold |
| Report body | 11 pt | Regular |
| Report caption / footnote | 9 pt | Regular |
| Figure axis label | 10 pt | Regular |
| Figure title | 12 pt | Bold |

Line-height 1.35 for body text everywhere.

---

## Chart style rules

- **No gridlines on the vertical axis** unless necessary for reading
  a value. Horizontal gridlines light `#e6e8eb`.
- **No top / right spines.** Only bottom + left spines, in slate
  `#4a5663`, line-width 0.8.
- **No 3D.** Ever.
- **No data labels on every bar.** Label the two or three the reader
  should remember.
- **Direct-label** lines instead of using a legend when possible.
- **Figure titles** state the finding, not the construction.
  - ❌ "Scatter plot of topic positions"
  - ✅ "Three topics: two in the Target Zone, one on the knife edge"

---

## File and asset locations

- `08_visual_system/aqualia_palette.py` — importable palette constants
- `08_visual_system/matplotlibrc` — drop-in rcParams
- `08_visual_system/plotly_template.py` — `pio.templates["aqualia"]`
- `08_visual_system/style.css` — Streamlit + GitHub Pages shared CSS
- `08_visual_system/figure_rebuild.py` — re-renders the three hero
  figures (matrix, tornado, heatmap) using the visual system

---

## How to apply

### Matplotlib / seaborn

```python
import matplotlib as mpl
mpl.rc_file("08_visual_system/matplotlibrc")
# or programmatically
from aqualia_palette import apply_matplotlib_style
apply_matplotlib_style()
```

### Plotly

```python
from aqualia_palette import register_plotly_template
register_plotly_template()
import plotly.io as pio
pio.templates.default = "aqualia"
```

### Streamlit

The app `07_streamlit/app.py` is already colour-matched. CSS override
lives in `08_visual_system/style.css` — copy into
`07_streamlit/.streamlit/custom.css` or inject via
`st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)`.

### PowerPoint / Keynote / Slides

1. Set slide theme background to **Paper** (white `#ffffff`).
2. Set master title to Inter Bold 28 pt Aqualia Navy.
3. Set master body to Inter Regular 14 pt Slate.
4. Accent shape for callouts = Aqualia Aqua.
5. Accent shape for warnings / risks = Accent Red.

A PowerPoint theme file (`.thmx`) can be exported once one slide is
built — propagates to all slides.

### Report (Markdown → PDF)

If exporting via Pandoc:

```bash
pandoc report.md \
  --pdf-engine=xelatex \
  -V mainfont="Inter" \
  -V sansfont="Inter" \
  -V fontsize=11pt \
  -V geometry="margin=1in" \
  -V linkcolor="002f5f" \
  -V colorlinks=true \
  -o report.pdf
```

Or paste the styled markdown into Word / Pages and manually apply
styles using the type scale above.

---

## Visual coherence checklist (before submission)

- [ ] Every chart uses the palette — no leftover matplotlib default blues
- [ ] Every chart uses Inter — no Helvetica / default fallbacks visible
- [ ] Every slide has the same title colour / size
- [ ] Topic colours identical across matrix, tornado, heatmap, roadmap
- [ ] No emoji, no clip-art, no stock photos
- [ ] Figure titles state findings, not constructions
- [ ] PDF export preserves fonts (linearised, fonts embedded)

# Streamlit Deployment Runbook

*Single source of truth for taking the interactive dashboard from
local Python to a public URL that fits on a deck QR code. The local
app is verified working (HTTP 200, matrix + heatmap + findings tabs
all render). Deployment steps below.*

---

## 0. Choose a path

| Option | Time | Cost | When to pick |
|---|---|---|---|
| **A. Streamlit Community Cloud** | ~30 min | Free | Default. Use this. |
| **B. Hugging Face Spaces (Streamlit runtime)** | ~30 min | Free | Backup if Streamlit Cloud is down |
| **C. Render / Railway / Fly.io** | ~60 min | Free tier → small $ | Overkill; skip |
| **D. Static fallback only (no server)** | ~10 min | Free | Last resort — see §5 |

**Recommended:** A + D as fallback.

---

## A. Streamlit Community Cloud (primary)

### A.1 Prereqs
- GitHub account with the repo pushed public.
- Streamlit Community Cloud account (sign in with GitHub).
- `07_streamlit/requirements.txt` present (already in repo).

### A.2 Push the repo
From the project root:

```bash
cd "C:/Users/marco/Documents/Sustainability Datathon"
git init
git add .
git commit -m "Initial datathon repo"
git remote add origin git@github.com:<user>/aqualia-datathon.git
git push -u origin main
```

**Gotchas**
- `.gitignore` should exclude `05_report/docx_build/node_modules/`
  and `05_report/docx_build/package-lock.json` (large).
- `02_sources/full_reports/*.pdf` is ~180 MB total. Either:
  1. **Accept the repo size** (GitHub allows up to 100 MB per file;
     all 4 files individually are under that). Push with
     `git lfs` if any single file exceeds 100 MB.
  2. OR keep `02_sources/full_reports/` out of git. The Streamlit
     app does NOT need these at runtime; it reads pre-computed
     artefacts (CSVs, HTMLs) in `03_analysis/` and `04_matrix/`.

**Recommended.** Add to `.gitignore`:
```
02_sources/full_reports/
05_report/docx_build/node_modules/
05_report/docx_build/package-lock.json
```
Then commit the pre-computed `coverage_matrix.csv`, `matrix_mc.html`,
`esrs_gap_heatmap.html`, `matrix_mc.png`, `matrix_tornado.png`,
`esrs_gap_heatmap.png`, `aqueduct_exposure.png`,
`aqueduct_choropleth.html` — all already in `03_analysis/` and
`04_matrix/`.

### A.3 Deploy
1. Go to https://share.streamlit.io
2. Click "New app"
3. Repository: `<user>/aqualia-datathon`
4. Branch: `main`
5. Main file path: `07_streamlit/app.py`
6. Click "Deploy"
7. Wait ~3 min for build

Default URL: `https://<project-slug>.streamlit.app`. Customise via
Advanced Settings if wanted.

### A.4 Post-deploy smoke test
Open the URL. Verify:
- [ ] Matrix tab renders with all three topic ellipses
- [ ] Stakeholder-weighting dropdown changes centroids
- [ ] Monte Carlo perturbation slider re-runs
- [ ] ESRS heatmap loads (from embedded HTML)
- [ ] Findings tab shows the three hero cards
- [ ] Methodology tab shows the formula block

If any fails, check Streamlit Cloud logs. Most failures are import
errors — confirm `requirements.txt` lists all pins.

---

## B. Hugging Face Spaces (backup)

### B.1 Steps
1. https://huggingface.co/spaces → "Create new Space"
2. Name: `aqualia-datathon`
3. SDK: **Streamlit**
4. Hardware: CPU basic (free)
5. Create → then connect the GitHub repo, or upload files directly.
6. Must rename `app.py` at root or set `app_file` in
   `README.md` frontmatter.

### B.2 `README.md` frontmatter for Spaces
Place at the root of the uploaded Space (not the repo root):

```yaml
---
title: Aqualia Datathon
emoji: 💧
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.30.0
app_file: app.py
pinned: false
---
```

### B.3 Move `app.py` to root
For Spaces specifically, move / copy the app file:
```bash
cp 07_streamlit/app.py app.py
cp 07_streamlit/requirements.txt requirements.txt
```
(Don't do this in the main repo — only in the HF Space upload.)

---

## C. Generate the QR code for the deck

Once the URL is live:

### C.1 Quickest — browser
1. https://www.qr-code-generator.com/
2. Paste the Streamlit URL
3. Set colour: navy `#002f5f` on white background
4. Download SVG or PNG at ≥ 300 dpi

### C.2 Scriptable — Python
```bash
pip install qrcode[pil]
python -c "
import qrcode
img = qrcode.make('https://<your-slug>.streamlit.app')
img.save('04_matrix/qr_streamlit.png')
print('Wrote 04_matrix/qr_streamlit.png')
"
```

### C.3 Place on slide 7
Update `06_presentation/deck.marp.md` slide 7: replace the placeholder
barcode div with an `<img>` pointing to `04_matrix/qr_streamlit.png`.

### C.4 Test the QR on 3 phones
- iPhone (native camera)
- Android (Google Lens or native)
- Another Android brand (Samsung / OnePlus) — some need a QR-code
  scanning app enabled
All three should load the page within 5 seconds.

---

## D. Static fallback (no server — for demo day USB stick)

If both cloud options fail on demo day, the app's core artefacts are
static HTML/PNG and work offline:

- `04_matrix/matrix_mc.html` — interactive matrix (hover works)
- `04_matrix/esrs_gap_heatmap.html` — interactive heatmap
- `04_matrix/aqueduct_choropleth.html` — interactive map
- `04_matrix/matrix_mc.png`, `matrix_tornado.png`,
  `esrs_gap_heatmap.png`, `aqueduct_exposure.png` — static exports

To serve these from a USB stick during the pitch:

```bash
cd 04_matrix
python -m http.server 8000
# open http://localhost:8000/matrix_mc.html
```

Or just open the HTML files directly in the browser — they are
self-contained and load from Plotly CDN (requires internet) OR from
a local `plotly.min.js` next to them (offline).

---

## E. Offline-safe HTML versions

Already generated. If you need to regenerate with the Plotly JS
inlined (fully self-contained, offline-safe):

```python
# In aqueduct_overlay.py and matrix_mc.py, replace:
#   fig.write_html(path, include_plotlyjs='cdn')
# with:
#   fig.write_html(path, include_plotlyjs=True)
# Files become ~3 MB each but work with zero internet.
```

---

## F. Local smoke test runbook (for rehearsals)

Before every rehearsal:

```bash
cd "C:/Users/marco/Documents/Sustainability Datathon"
streamlit run 07_streamlit/app.py --server.port 8789
```

Open `http://localhost:8789`. Verify all 4 tabs. Kill with Ctrl+C.

If `streamlit` isn't on the path:
```bash
python -m streamlit run 07_streamlit/app.py
```

---

## G. Deploy-day checklist

- [ ] Repo pushed to public GitHub
- [ ] `02_sources/full_reports/` excluded from git (too big)
- [ ] Streamlit Community Cloud deploy succeeded
- [ ] QR code tested on 3 phones
- [ ] QR code inserted on slide 7 in Aqualia navy
- [ ] URL recorded in `FINAL_READINESS.md` §Submission day
- [ ] Backup USB stick with static HTMLs + PNG exports
- [ ] Offline Plotly JS embedded as fallback (optional but recommended)

---

## H. URL table — keep this current

| Asset | URL |
|---|---|
| GitHub repo | `https://github.com/<user>/aqualia-datathon` |
| Streamlit app | `https://<slug>.streamlit.app` |
| HF Space backup | `https://huggingface.co/spaces/<user>/aqualia-datathon` |
| QR code | `04_matrix/qr_streamlit.png` |

Paste these into the report Appendix H (Data and code) after deploy.

# Streamlit Dashboard — Interactive Matrix

Single-file Streamlit app — the QR-code destination for the pitch
deck. Shows the Monte Carlo matrix, ESRS gap heatmap, findings, and
methodology. Zero backend.

## Run locally

```bash
pip install -r 07_streamlit/requirements.txt
streamlit run 07_streamlit/app.py
```

Opens at `http://localhost:8501`.

## Deploy to Streamlit Community Cloud (free)

1. Push the whole `Sustainability Datathon/` directory to a public
   GitHub repo.
2. Go to https://share.streamlit.io/ → "New app".
3. Select the repo, branch, main file `07_streamlit/app.py`.
4. Deploy. Takes ~2 min. You'll get a URL like
   `https://aqualia-datathon.streamlit.app`.
5. Generate a QR code for that URL → paste on slide 5 of the deck.

## Static fallback

If Streamlit Cloud ever hiccups on demo day, use the static artefacts
already in the repo:

- `04_matrix/matrix_mc.png` — matrix image
- `04_matrix/matrix_mc.html` — interactive Plotly, no server needed
- `04_matrix/esrs_gap_heatmap.html` — interactive heatmap
- `04_matrix/matrix_tornado.png` — sensitivity

Serve them via `python -m http.server` or GitHub Pages.

## What to demo in the pitch

20 seconds is enough:

1. Show the QR code at the start of the methodology slide.
2. While speaking, pull up the app on the presenter laptop.
3. On the Matrix tab, flip between "Salience" and "Investor-first"
   weighting schemes — centroids barely move. That visual is the
   robustness point.
4. Jump to the Heatmap tab, hover over the S3 row. Say "see the
   Colombia gap?" Move on.

Do not try to explain the sliders. Judges do not want another slide
of methodology in the pitch — they want to see that it works.

## Do not extend this to a full-stack app

Resist the urge. `what_actually_wins.md §1` is explicit on why.

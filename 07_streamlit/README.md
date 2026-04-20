# 07_streamlit — Archived

> **This folder is superseded.** The primary interactive deliverable
> is the single-file HTML dashboard in [`10_dashboard/`](../10_dashboard/),
> deployed at **https://ma731.github.io/Aqualia-Datathon/**.

The Streamlit application here was an early prototype of the
interactive layer for the project. It was replaced in April 2026 by
the premium single-file HTML dashboard (Tailwind + Plotly + GSAP),
which:

- Runs without a Python server (static site, GitHub Pages)
- Integrates tighter brand typography and motion design
- Adds the NGFS climate-scenario toggle, stakeholder salience radar,
  and peer-benchmark chart that were out of scope for the Streamlit
  version
- Embeds the QR-code destination cited in the pitch deck

The code in this folder is retained for reference only. It is not
part of the submission and is no longer maintained. If you want to
run it for local inspection:

```bash
pip install -r requirements.txt
streamlit run app.py
```

For the up-to-date interactive experience, open the dashboard:
**https://ma731.github.io/Aqualia-Datathon/**

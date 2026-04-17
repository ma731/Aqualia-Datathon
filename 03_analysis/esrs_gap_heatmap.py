"""
ESRS Gap Heatmap — Prototype Pipeline
=====================================

Classifies Aqualia's available disclosure corpus against a curated list
of ~70 ESRS datapoints (plus Aqualia sector-specific AQ datapoints).
Produces a coverage heatmap that doubles as the hero slide for the
datathon pitch.

Methodology
-----------
1. Parse ESRS datapoint library from esrs_datapoints.csv.
2. Extract text from the 7 Aqualia source PDFs in 02_sources/.
3. Chunk Aqualia corpus by paragraph and tag with (source, chunk_id).
4. Vectorise DP descriptions and Aqualia chunks via TF-IDF (baseline).
   Upgrade path: swap TfidfVectorizer for SentenceTransformer('BAAI/bge-large-en-v1.5').
5. For each DP, compute cosine similarity to every chunk and keep
   top-k (k=3) mean as the DP's coverage score.
6. Band the score: Green / Amber / Red / Dark Red / Grey (see §scoring).
7. Render heatmap (Standard family x Disclosure Requirement cells).

This prototype runs on the 7 sources we already have. Upgrade
involves adding the full 2022/2023/2024 Aqualia Sustainability Reports
plus peer URS documents to the `corpus_dir`. Pipeline is unchanged.

Usage
-----
    python esrs_gap_heatmap.py

Outputs
-------
- coverage_matrix.csv        one row per DP with score, band, top chunk
- esrs_gap_heatmap.html      interactive Plotly heatmap
- esrs_gap_heatmap.png       static image for the report
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "08_visual_system"))
try:
    from aqualia_palette import apply_matplotlib_style, BAND_COLOURS as _BAND
    apply_matplotlib_style()
except Exception as _exc:  # pragma: no cover
    print(f"[visual system not loaded: {_exc}]")
    _BAND = None

import numpy as np
import pandas as pd
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]
DP_FILE = ROOT / "03_analysis" / "esrs_datapoints.csv"
CORPUS_DIR = ROOT / "02_sources"
OUT_DIR = ROOT / "03_analysis"
MATRIX_OUT = ROOT / "04_matrix"
MATRIX_OUT.mkdir(parents=True, exist_ok=True)

# Adaptive thresholds — computed from the corpus at runtime.
# Fall-back absolute bands used if percentile computation fails.
ADAPTIVE_PERCENTILES = {"green": 85, "amber": 65, "red": 40}
FALLBACK_THRESHOLDS = {"green": 0.08, "amber": 0.05, "red": 0.03}

# Populated by compute_coverage().
THRESHOLDS: dict[str, float] = dict(FALLBACK_THRESHOLDS)

TOP_K = 3  # for each DP, average top-k chunk similarities


# -------------------------------------------------------------------
# PDF -> chunks
# -------------------------------------------------------------------


@dataclass
class Chunk:
    source: str
    chunk_id: int
    page: int
    text: str


def _clean(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    return s


def pdf_to_chunks(path: Path, min_len: int = 150, max_len: int = 900) -> list[Chunk]:
    """Return list of Chunk objects. Paragraphs merged until max_len."""
    out: list[Chunk] = []
    try:
        reader = PdfReader(str(path))
    except Exception as e:
        print(f"  [!] Cannot read {path.name}: {e}")
        return out
    chunk_id = 0
    buffer = ""
    buffer_page = 1
    for i, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception:
            continue
        for para in re.split(r"\n\s*\n|\r\r", text):
            para = _clean(para)
            if not para:
                continue
            if len(buffer) == 0:
                buffer = para
                buffer_page = i
            elif len(buffer) + len(para) <= max_len:
                buffer = f"{buffer} {para}"
            else:
                if len(buffer) >= min_len:
                    out.append(Chunk(path.name, chunk_id, buffer_page, buffer))
                    chunk_id += 1
                buffer = para
                buffer_page = i
    if len(buffer) >= min_len:
        out.append(Chunk(path.name, chunk_id, buffer_page, buffer))
    return out


def load_corpus(corpus_dir: Path) -> list[Chunk]:
    chunks: list[Chunk] = []
    # rglob so we pick up subfolders (e.g. 02_sources/full_reports/)
    for pdf in sorted(corpus_dir.rglob("*.pdf")):
        part = pdf_to_chunks(pdf)
        chunks.extend(part)
        print(f"  {str(pdf.relative_to(corpus_dir)):70s}  -> {len(part):5d} chunks")
    return chunks


# -------------------------------------------------------------------
# Scoring
# -------------------------------------------------------------------


def band(score: float) -> str:
    if score >= THRESHOLDS["green"]:
        return "green"
    if score >= THRESHOLDS["amber"]:
        return "amber"
    if score >= THRESHOLDS["red"]:
        return "red"
    return "dark_red"


# Bilingual expansion for common ESG/water-sector terms. Keeps TF-IDF
# useful when the corpus is Spanish while DP descriptions are English.
# Not exhaustive — just the high-hit terms across E/S/G topical standards.
_ES_EN_LEXICON = {
    "water": "agua hídrico hidrológico",
    "energy": "energía energético",
    "climate": "clima climático climática",
    "emissions": "emisiones",
    "greenhouse gas": "gases efecto invernadero GEI",
    "biodiversity": "biodiversidad",
    "ecosystem": "ecosistema ecosistemas",
    "pollution": "contaminación contaminantes",
    "circular": "circular circularidad",
    "waste": "residuos",
    "workforce": "trabajadores plantilla empleados",
    "health and safety": "salud seguridad laboral",
    "diversity": "diversidad inclusión equidad",
    "community": "comunidad comunidades",
    "consumer": "cliente consumidor usuario",
    "privacy": "privacidad protección datos",
    "cybersecurity": "ciberseguridad",
    "cyber": "ciber",
    "governance": "gobernanza gobierno corporativo",
    "corruption": "corrupción soborno",
    "supplier": "proveedor proveedores cadena de suministro",
    "financial": "financiero financiera económico",
    "taxonomy": "taxonomía",
    "transition plan": "plan de transición",
    "adaptation": "adaptación",
    "mitigation": "mitigación",
    "resource": "recurso recursos",
    "human rights": "derechos humanos",
    "digital": "digital digitalización",
    "innovation": "innovación",
    "investment": "inversión",
    "infrastructure": "infraestructura",
    "reuse": "reutilización reuse",
    "risk": "riesgo",
    "opportunity": "oportunidad",
    "target": "objetivo objetivos meta",
    "policy": "política políticas",
    "action": "acción acciones medidas",
    "stakeholder": "grupo de interés stakeholders",
    "transparency": "transparencia",
}

# Spanish stop-words (small list — just the top unhelpful function words).
_ES_STOP = {
    "de", "la", "que", "el", "en", "y", "a", "los", "del", "se", "las",
    "por", "un", "para", "con", "no", "una", "su", "al", "es", "lo",
    "como", "más", "pero", "sus", "le", "ya", "o", "este", "sí", "porque",
    "esta", "entre", "cuando", "muy", "sin", "sobre", "también", "me",
    "hasta", "hay", "donde", "quien", "desde", "todo", "nos", "durante",
    "todos", "uno", "les", "ni", "contra", "otros", "ese", "eso", "ante",
    "ellos", "e", "esto", "mí", "antes", "algunos", "qué", "unos", "yo",
    "otro", "otras", "otra", "él", "tanto", "esa", "estos", "mucho",
    "quienes", "nada", "muchos", "cual", "poco", "ella", "estar",
    "estas", "algunas", "algo", "nosotros", "mi", "mis", "tú", "te", "ti",
    "tu", "tus", "ellas", "nosotras", "vosotros", "vosotras", "os",
    "mío", "mía", "míos", "mías", "tuyo", "tuya", "tuyos", "tuyas",
    "suyo", "suya", "suyos", "suyas", "nuestro", "nuestra", "nuestros",
    "nuestras", "vuestro", "vuestra", "vuestros", "vuestras", "esos",
    "esas", "estoy", "estás", "está", "estamos", "estáis", "están", "esté",
}
ENGLISH_STOP = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "of", "in", "on", "to", "for", "and", "or", "but", "with", "as",
    "by", "from", "this", "that", "these", "those", "it", "its", "at",
    "which", "who", "whom", "whose", "if", "then", "than", "such",
}
ES_EN_STOP_LIST = sorted(_ES_STOP | ENGLISH_STOP)


def _expand_dp(text: str) -> str:
    """Append Spanish bilingual tokens so TF-IDF picks up Spanish chunks."""
    extra = []
    low = text.lower()
    for en_term, es_terms in _ES_EN_LEXICON.items():
        if en_term in low:
            extra.append(es_terms)
    return text + " " + " ".join(extra) if extra else text


def compute_coverage(dp: pd.DataFrame, chunks: list[Chunk]) -> pd.DataFrame:
    """Return DP table with coverage_score, band, top chunk text.

    Also mutates the module-level THRESHOLDS to adaptive values based on
    the actual score distribution — greens = top 15%, ambers = next 20%,
    reds = next 25%, dark_reds = bottom 40%.
    """
    global THRESHOLDS
    chunk_texts = [c.text for c in chunks]
    dp_texts = [_expand_dp(t) for t in dp["description"].tolist()]
    vec = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.90,
        max_features=60_000,
        stop_words=ES_EN_STOP_LIST,
        sublinear_tf=True,
        lowercase=True,
    )
    mat = vec.fit_transform(dp_texts + chunk_texts)
    dp_mat = mat[: len(dp_texts)]
    chunk_mat = mat[len(dp_texts) :]
    sim = cosine_similarity(dp_mat, chunk_mat)  # (n_dp, n_chunks)

    top_idx = np.argsort(-sim, axis=1)[:, :TOP_K]
    top_scores = np.take_along_axis(sim, top_idx, axis=1).mean(axis=1)

    # Adaptive thresholds
    try:
        THRESHOLDS = {
            "green": float(np.percentile(top_scores, ADAPTIVE_PERCENTILES["green"])),
            "amber": float(np.percentile(top_scores, ADAPTIVE_PERCENTILES["amber"])),
            "red":   float(np.percentile(top_scores, ADAPTIVE_PERCENTILES["red"])),
        }
        print(f"  Adaptive thresholds: green>={THRESHOLDS['green']:.4f}  "
              f"amber>={THRESHOLDS['amber']:.4f}  red>={THRESHOLDS['red']:.4f}")
    except Exception:
        THRESHOLDS = dict(FALLBACK_THRESHOLDS)

    top_chunk_text = [chunks[i].text[:200] + "…" for i in top_idx[:, 0]]
    top_chunk_src = [chunks[i].source for i in top_idx[:, 0]]
    top_chunk_page = [chunks[i].page for i in top_idx[:, 0]]

    out = dp.copy()
    out["coverage_score"] = top_scores
    out["band"] = out["coverage_score"].map(band)
    out["top_chunk_source"] = top_chunk_src
    out["top_chunk_page"] = top_chunk_page
    out["top_chunk_text"] = top_chunk_text
    return out


# -------------------------------------------------------------------
# Rendering
# -------------------------------------------------------------------


BAND_COLOR = _BAND if _BAND else {
    "green": "#1b7f3b",
    "amber": "#f2b039",
    "red": "#c83c35",
    "dark_red": "#6e1c1c",
    "grey": "#bbbbbb",
}

BAND_NUM = {"green": 3, "amber": 2, "red": 1, "dark_red": 0, "grey": -1}


def render_heatmap_plotly(cov: pd.DataFrame, out_html: Path) -> None:
    import plotly.graph_objects as go

    # Pivot: standard (y) x dp_id (x)
    cov = cov.sort_values(["family", "standard", "dp_id"]).reset_index(drop=True)
    cov["numeric"] = cov["band"].map(BAND_NUM)

    z = cov["numeric"].to_numpy().reshape(1, -1)
    labels = cov["dp_id"].tolist()
    hover = [
        f"<b>{r.dp_id}</b>  {r.standard}<br>"
        f"<i>{r.description}</i><br>"
        f"Band: <b>{r.band.upper()}</b>  (score {r.coverage_score:.3f})<br>"
        f"Top source: {r.top_chunk_source} p.{r.top_chunk_page}<br>"
        f"<span style='font-size:10px'>{r.top_chunk_text}</span>"
        for r in cov.itertuples()
    ]

    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            x=labels,
            y=["Aqualia corpus"],
            colorscale=[
                [0.00, BAND_COLOR["dark_red"]],
                [0.33, BAND_COLOR["red"]],
                [0.67, BAND_COLOR["amber"]],
                [1.00, BAND_COLOR["green"]],
            ],
            zmin=0,
            zmax=3,
            showscale=True,
            hoverinfo="text",
            text=[hover],
            colorbar=dict(
                tickvals=[0, 1, 2, 3],
                ticktext=["Dark red (gap)", "Red", "Amber", "Green"],
                title="Coverage",
            ),
        )
    )
    fig.update_layout(
        title="ESRS Gap Heatmap — Aqualia disclosure coverage (prototype)",
        xaxis=dict(title="ESRS datapoint", tickangle=-60),
        yaxis=dict(showticklabels=False),
        height=350,
        margin=dict(l=40, r=40, t=70, b=120),
    )
    fig.write_html(str(out_html))


def render_heatmap_matplotlib(cov: pd.DataFrame, out_png: Path) -> None:
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap

    cov = cov.sort_values(["family", "standard", "dp_id"]).reset_index(drop=True)
    families = cov["family"].tolist()
    standards = cov["standard"].tolist()

    # Group by standard into rows for readability
    standards_order = sorted(cov["standard"].unique(), key=lambda s: (
        0 if s.startswith("E") else (1 if s.startswith("S") else (2 if s.startswith("G") else 3)),
        s,
    ))
    max_per_std = max((cov["standard"] == s).sum() for s in standards_order)
    grid = np.full((len(standards_order), max_per_std), -1.0)
    annot = [[None] * max_per_std for _ in range(len(standards_order))]
    xlabels = [[""] * max_per_std for _ in range(len(standards_order))]

    for i, std in enumerate(standards_order):
        sub = cov[cov["standard"] == std].reset_index(drop=True)
        for j, row in sub.iterrows():
            grid[i, j] = BAND_NUM[row["band"]]
            annot[i][j] = row["dp_id"].replace(f"{std}-", "")
            xlabels[i][j] = row["dp_id"]

    # Build colormap: dark_red, red, amber, green (+ grey for -1 handled via set_bad)
    cmap = ListedColormap([BAND_COLOR["dark_red"], BAND_COLOR["red"],
                          BAND_COLOR["amber"], BAND_COLOR["green"]])
    grid_masked = np.ma.masked_less(grid, 0)

    fig, ax = plt.subplots(figsize=(max(10, max_per_std * 0.55), len(standards_order) * 0.7 + 1))
    cmap.set_bad(BAND_COLOR["grey"])
    im = ax.imshow(grid_masked, cmap=cmap, vmin=0, vmax=3, aspect="auto")

    ax.set_yticks(range(len(standards_order)))
    ax.set_yticklabels(standards_order, fontsize=10)
    ax.set_xticks([])
    for i in range(len(standards_order)):
        for j in range(max_per_std):
            if annot[i][j]:
                ax.text(j, i, annot[i][j], ha="center", va="center",
                        fontsize=7, color="white", fontweight="bold")

    ax.set_title("ESRS Gap Heatmap — Aqualia disclosure coverage (prototype)",
                 fontsize=12, pad=14)
    ax.set_xlabel("Disclosure Requirements (per standard, left→right as in CSV)", fontsize=9)

    import matplotlib.patches as mpatches
    legend = [
        mpatches.Patch(color=BAND_COLOR["green"], label="Green — strong"),
        mpatches.Patch(color=BAND_COLOR["amber"], label="Amber — partial"),
        mpatches.Patch(color=BAND_COLOR["red"], label="Red — weak"),
        mpatches.Patch(color=BAND_COLOR["dark_red"], label="Dark red — gap"),
        mpatches.Patch(color=BAND_COLOR["grey"], label="N/A"),
    ]
    ax.legend(handles=legend, loc="upper right", bbox_to_anchor=(1.0, -0.05),
              ncol=5, fontsize=8, frameon=False)
    plt.tight_layout()
    plt.savefig(out_png, dpi=180, bbox_inches="tight")
    plt.close()


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------


def main() -> None:
    print("== ESRS Gap Heatmap — prototype ==")
    print(f"Loading DP library: {DP_FILE}")
    dp = pd.read_csv(DP_FILE)
    print(f"  {len(dp)} datapoints")

    print(f"Loading corpus from: {CORPUS_DIR}")
    chunks = load_corpus(CORPUS_DIR)
    print(f"Total chunks: {len(chunks)}")

    print("Scoring coverage…")
    cov = compute_coverage(dp, chunks)

    counts = cov["band"].value_counts()
    print("\nCoverage summary:")
    for b in ("green", "amber", "red", "dark_red"):
        n = counts.get(b, 0)
        pct = 100 * n / len(cov)
        print(f"  {b:<10s}  {n:3d}  ({pct:5.1f}%)")

    out_csv = OUT_DIR / "coverage_matrix.csv"
    cov.to_csv(out_csv, index=False)
    print(f"\nWrote {out_csv.name}")

    render_heatmap_plotly(cov, MATRIX_OUT / "esrs_gap_heatmap.html")
    print(f"Wrote {MATRIX_OUT/'esrs_gap_heatmap.html'}")

    render_heatmap_matplotlib(cov, MATRIX_OUT / "esrs_gap_heatmap.png")
    print(f"Wrote {MATRIX_OUT/'esrs_gap_heatmap.png'}")

    # Topic coverage summary for the pitch's headline metric
    print("\nTopic-level coverage of our three short-listed topics:")
    topic_map = {
        "T1 Water Resilience & Equitable Access": [
            "E1-1", "E1-4", "E1-5", "E1-6", "E1-9",
            "E3-1", "E3-2", "E3-3", "E3-4", "E3-5",
            "S3-1", "S3-3", "S3-4",
            "S4-1", "S4-2", "S4-3", "S4-4",
        ],
        "T2 Digital & Cyber Infrastructure": [
            "G1-7", "G1-8", "S4-1", "S4-2",
            "AQ-DIG-1", "AQ-DIG-2", "AQ-CYB-1", "AQ-CYB-2",
        ],
        "T3 Green Finance & Integrity": [
            "G1-1", "G1-2", "G1-3", "G1-4", "G1-5", "G1-6",
            "E1-3",
            "AQ-FIN-1", "AQ-FIN-2", "AQ-FIN-3",
        ],
    }
    for t, dps in topic_map.items():
        sub = cov[cov["dp_id"].isin(dps)]
        bands = sub["band"].value_counts()
        total = len(sub)
        gap_pct = 100 * (bands.get("red", 0) + bands.get("dark_red", 0)) / max(total, 1)
        print(f"  {t}: {total} DPs, gap share {gap_pct:.0f}%  "
              f"(green {bands.get('green', 0)}, amber {bands.get('amber', 0)}, "
              f"red {bands.get('red', 0)}, dark_red {bands.get('dark_red', 0)})")


if __name__ == "__main__":
    main()

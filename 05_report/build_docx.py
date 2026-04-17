"""
Convert 05_report/report.md → 05_report/report.docx with the Aqualia
visual system applied.

Usage:  python 05_report/build_docx.py
"""
from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Cm, Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "report.md"
OUT = ROOT / "report.docx"

NAVY = RGBColor(0x00, 0x2F, 0x5F)
AQUA = RGBColor(0x5D, 0xB9, 0xD9)
DEEP = RGBColor(0x0B, 0x4F, 0x74)
SLATE = RGBColor(0x4A, 0x56, 0x63)
SAND_RGB = "d6cdb7"
GRID_RGB = "e6e8eb"

BODY_FONT = "Arial"  # Inter fallback — Arial is universal
HEADING_FONT = "Arial"


def set_shading(cell, fill_hex: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill_hex)
    tc_pr.append(shd)


def set_cell_margins(cell, top=80, bottom=80, left=120, right=120) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = OxmlElement("w:tcMar")
    for side, val in (("top", top), ("bottom", bottom), ("left", left), ("right", right)):
        node = OxmlElement(f"w:{side}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tc_mar.append(node)
    tc_pr.append(tc_mar)


def set_paragraph_spacing(p, before=0, after=120, line=1.35) -> None:
    fmt = p.paragraph_format
    fmt.space_before = Pt(before)
    fmt.space_after = Pt(after)
    fmt.line_spacing = line


def add_styled_runs(p, text: str, base_font=BODY_FONT, base_size=11,
                    base_color=SLATE, bold=False) -> None:
    """Parse **bold** and `code` inline markdown within plain text."""
    if not text:
        return
    # Split on **bold** and `code`
    parts = re.split(r"(\*\*[^*]+\*\*|`[^`]+`)", text)
    for part in parts:
        if not part:
            continue
        r = p.add_run()
        r.font.name = base_font
        r.font.size = Pt(base_size)
        r.font.color.rgb = base_color
        if bold:
            r.bold = True
        if part.startswith("**") and part.endswith("**"):
            r.text = part[2:-2]
            r.bold = True
            r.font.color.rgb = NAVY
        elif part.startswith("`") and part.endswith("`"):
            r.text = part[1:-1]
            r.font.name = "Consolas"
            r.font.size = Pt(10)
        else:
            r.text = part


def add_heading(doc: Document, text: str, level: int) -> None:
    """Custom heading styling — Navy, bold, size scaled to level."""
    sizes = {1: 20, 2: 15, 3: 12, 4: 11}
    spacing_before = {1: 18, 2: 14, 3: 10, 4: 8}
    spacing_after = {1: 8, 2: 6, 3: 4, 4: 4}
    size = sizes.get(level, 11)

    p = doc.add_paragraph()
    set_paragraph_spacing(p, before=spacing_before[level],
                          after=spacing_after[level], line=1.25)
    r = p.add_run(text.strip())
    r.font.name = HEADING_FONT
    r.font.size = Pt(size)
    r.font.color.rgb = NAVY
    r.bold = True

    # Level-2 underline band
    if level == 2:
        pPr = p._p.get_or_add_pPr()
        pBdr = OxmlElement("w:pBdr")
        bottom = OxmlElement("w:bottom")
        bottom.set(qn("w:val"), "single")
        bottom.set(qn("w:sz"), "6")
        bottom.set(qn("w:color"), "5DB9D9")
        pBdr.append(bottom)
        pPr.append(pBdr)


def add_body_paragraph(doc: Document, text: str) -> None:
    p = doc.add_paragraph()
    set_paragraph_spacing(p, before=0, after=6, line=1.35)
    add_styled_runs(p, text)


def add_bullet(doc: Document, text: str) -> None:
    p = doc.add_paragraph(style="List Bullet")
    set_paragraph_spacing(p, before=0, after=3, line=1.3)
    # Clear the default style's run formatting and re-add our styled runs.
    for r in list(p.runs):
        r.text = ""
    add_styled_runs(p, text)


def add_numbered(doc: Document, text: str) -> None:
    p = doc.add_paragraph(style="List Number")
    set_paragraph_spacing(p, before=0, after=3, line=1.3)
    for r in list(p.runs):
        r.text = ""
    add_styled_runs(p, text)


def add_blockquote(doc: Document, text: str) -> None:
    p = doc.add_paragraph()
    set_paragraph_spacing(p, before=4, after=6, line=1.35)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single")
    left.set(qn("w:sz"), "24")
    left.set(qn("w:color"), "5DB9D9")
    left.set(qn("w:space"), "6")
    pBdr.append(left)
    pPr.append(pBdr)
    p.paragraph_format.left_indent = Cm(0.4)
    # Use italic-navy styling for quoted emphasis
    parts = re.split(r"(\*\*[^*]+\*\*|`[^`]+`|\*[^*]+\*)", text)
    for part in parts:
        if not part:
            continue
        r = p.add_run()
        r.font.name = BODY_FONT
        r.font.size = Pt(11)
        if part.startswith("**") and part.endswith("**"):
            r.text = part[2:-2]
            r.bold = True
            r.font.color.rgb = NAVY
        elif part.startswith("*") and part.endswith("*") and not part.startswith("**"):
            r.text = part[1:-1]
            r.italic = True
            r.font.color.rgb = DEEP
        elif part.startswith("`") and part.endswith("`"):
            r.text = part[1:-1]
            r.font.name = "Consolas"
            r.font.size = Pt(10)
        else:
            r.text = part
            r.font.color.rgb = SLATE


def add_table(doc: Document, rows: list[list[str]]) -> None:
    if not rows:
        return
    ncols = max(len(r) for r in rows)
    tbl = doc.add_table(rows=len(rows), cols=ncols)
    tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
    tbl.style = "Light Grid Accent 1"
    for i, row in enumerate(rows):
        for j in range(ncols):
            cell = tbl.rows[i].cells[j]
            set_cell_margins(cell)
            # Clear any default paragraph
            for p in list(cell.paragraphs):
                p.clear()
            cell_text = row[j] if j < len(row) else ""
            p = cell.paragraphs[0]
            set_paragraph_spacing(p, before=0, after=0, line=1.25)
            if i == 0:
                set_shading(cell, SAND_RGB)
                r = p.add_run(cell_text.replace("**", ""))
                r.font.name = BODY_FONT
                r.font.size = Pt(10)
                r.font.color.rgb = NAVY
                r.bold = True
            else:
                add_styled_runs(p, cell_text, base_size=10)


def parse_md(src_path: Path) -> list:
    """Return a list of block tuples: ('heading', level, text) |
    ('p', text) | ('bullet', text) | ('num', text) | ('blockquote', text) |
    ('table', [[cell,...],...]) | ('hr',) | ('blank',)."""
    blocks: list = []
    lines = src_path.read_text(encoding="utf-8").splitlines()
    i = 0
    in_front_matter = False
    in_list: str | None = None  # 'bullet' or 'num' or None

    def flush_table(pending_rows):
        # pending_rows: list of raw row strings like "| a | b |"
        cleaned = []
        for raw in pending_rows:
            raw = raw.strip()
            if raw.startswith("|"):
                raw = raw[1:]
            if raw.endswith("|"):
                raw = raw[:-1]
            cells = [c.strip() for c in raw.split("|")]
            cleaned.append(cells)
        # drop the separator row (---|---)
        cleaned = [r for r in cleaned if not all(
            re.fullmatch(r":?-{2,}:?", c or "") for c in r
        )]
        if cleaned:
            blocks.append(("table", cleaned))

    table_buffer: list[str] = []

    while i < len(lines):
        line = lines[i]

        # Frontmatter guard
        if line.strip() == "---" and i == 0:
            in_front_matter = True
            i += 1
            continue
        if in_front_matter:
            if line.strip() == "---":
                in_front_matter = False
            i += 1
            continue

        # Table detection
        if line.strip().startswith("|") and "|" in line.strip()[1:]:
            table_buffer.append(line)
            i += 1
            continue
        elif table_buffer:
            flush_table(table_buffer)
            table_buffer = []

        if not line.strip():
            blocks.append(("blank",))
            i += 1
            continue

        # Horizontal rule
        if re.fullmatch(r"\s*---+\s*", line):
            blocks.append(("hr",))
            i += 1
            continue

        # Headings
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            blocks.append(("heading", level, text))
            i += 1
            continue

        # Blockquote
        if line.startswith(">"):
            text = line[1:].strip()
            # merge multi-line blockquotes
            j = i + 1
            while j < len(lines) and lines[j].startswith(">"):
                text += " " + lines[j][1:].strip()
                j += 1
            blocks.append(("blockquote", text))
            i = j
            continue

        # Bulleted list
        m = re.match(r"^\s*[-*]\s+(.*)$", line)
        if m:
            blocks.append(("bullet", m.group(1).strip()))
            i += 1
            continue

        # Numbered list
        m = re.match(r"^\s*\d+\.\s+(.*)$", line)
        if m:
            blocks.append(("num", m.group(1).strip()))
            i += 1
            continue

        # Paragraph (merge continuation lines)
        text = line.strip()
        j = i + 1
        while (
            j < len(lines)
            and lines[j].strip()
            and not lines[j].strip().startswith(("#", ">", "|", "- ", "* "))
            and not re.match(r"^\s*\d+\.\s+", lines[j])
            and not re.fullmatch(r"\s*---+\s*", lines[j])
        ):
            text += " " + lines[j].strip()
            j += 1
        blocks.append(("p", text))
        i = j

    if table_buffer:
        flush_table(table_buffer)

    return blocks


def build(doc_path: Path, out_path: Path) -> None:
    blocks = parse_md(doc_path)

    doc = Document()

    # Page setup: 1" margins, US Letter. Inter-like body font.
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Set the default Normal style
    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = BODY_FONT
    normal.font.size = Pt(11)
    normal.font.color.rgb = SLATE

    # Title page
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    set_paragraph_spacing(title, before=12, after=4)
    r = title.add_run("Water as Strategy")
    r.font.name = HEADING_FONT
    r.font.size = Pt(28)
    r.font.color.rgb = NAVY
    r.bold = True

    sub = doc.add_paragraph()
    set_paragraph_spacing(sub, before=0, after=18)
    r = sub.add_run("A Double Materiality Framework for Aqualia, 2027–2030")
    r.font.name = HEADING_FONT
    r.font.size = Pt(14)
    r.font.color.rgb = DEEP

    meta = doc.add_paragraph()
    set_paragraph_spacing(meta, before=0, after=18)
    r = meta.add_run(
        "IE Sustainability Datathon · March 2026\n"
        "Track: Double Materiality & ESG Strategy — Aqualia\n"
        "Commissioned work · External ESG advisory engagement"
    )
    r.font.name = BODY_FONT
    r.font.size = Pt(10)
    r.font.color.rgb = SLATE
    r.italic = True

    # Render blocks — but skip the markdown's own title block (first H1 and its H2)
    # so we don't duplicate the title we just wrote.
    seen_h1 = False
    skip_title_h2 = False
    prev_was_blank = False

    for block in blocks:
        kind = block[0]
        if kind == "heading":
            level, text = block[1], block[2]
            # Suppress the title "Water as Strategy" and subtitle, since we have a title page.
            if level == 1 and not seen_h1:
                seen_h1 = True
                skip_title_h2 = True
                continue
            if level == 2 and skip_title_h2:
                skip_title_h2 = False
                continue
            skip_title_h2 = False
            add_heading(doc, text, level)
            prev_was_blank = False
        elif kind == "p":
            add_body_paragraph(doc, block[1])
            prev_was_blank = False
        elif kind == "bullet":
            add_bullet(doc, block[1])
            prev_was_blank = False
        elif kind == "num":
            add_numbered(doc, block[1])
            prev_was_blank = False
        elif kind == "blockquote":
            add_blockquote(doc, block[1])
            prev_was_blank = False
        elif kind == "table":
            add_table(doc, block[1])
            # add a tiny spacer after tables
            add_body_paragraph(doc, "")
            prev_was_blank = False
        elif kind == "hr":
            # Use a thin navy line instead of a blank divider
            p = doc.add_paragraph()
            set_paragraph_spacing(p, before=6, after=10)
            pPr = p._p.get_or_add_pPr()
            pBdr = OxmlElement("w:pBdr")
            bottom = OxmlElement("w:bottom")
            bottom.set(qn("w:val"), "single")
            bottom.set(qn("w:sz"), "6")
            bottom.set(qn("w:color"), "002f5f")
            pBdr.append(bottom)
            pPr.append(pBdr)
            prev_was_blank = False
        elif kind == "blank":
            # Skip consecutive blanks to avoid huge gaps
            if not prev_was_blank:
                # no-op; paragraph spacing handles gaps
                pass
            prev_was_blank = True

    # Footer on every page
    for section in doc.sections:
        footer = section.footer
        p = footer.paragraphs[0]
        p.text = ""
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(
            "Water as Strategy — Aqualia Double Materiality Framework  "
            "·  IE Sustainability Datathon 2026"
        )
        r.font.name = BODY_FONT
        r.font.size = Pt(8)
        r.font.color.rgb = SLATE

    doc.save(out_path)
    print(f"Wrote {out_path}  ({out_path.stat().st_size/1024:,.1f} KB)")


if __name__ == "__main__":
    build(SRC, OUT)

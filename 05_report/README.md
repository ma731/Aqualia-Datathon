# 05_report — What's in this folder

**The report is [`report.docx`](report.docx) (~15 pages, Word format).**
That's the deliverable. Open that one.

Everything else in this folder is supporting material:

| File | What it is |
|---|---|
| **`report.docx`** | 📄 **The final report.** Word document, styled with the Aqualia visual system, ~15 pages + appendices. This is what the jury reads. |
| `report.md` | Markdown source. Edit this, then run the build script below to regenerate `report.docx`. |
| `executive_summary.md` | Stand-alone one-page summary (used in the dashboard hero copy). |
| `references.md` | Full bibliography — 47 cited sources grouped by type. |
| `report_skeleton.md` | Initial outline drafted at the start of the project. Kept for audit trail. |
| `build_docx.py` | Python script that converts `report.md` → `report.docx` with all brand styling, tables, and typography applied. Not a deliverable — just the tool that rebuilds the Word doc. Run with `python build_docx.py` from this folder after editing the `.md`. |

## Why there's a Python script in a "report" folder

The report is written in **Markdown** (`report.md`) because it's easier to
edit, diff, and version-control than Word. But the final deliverable has
to be a **Word document** — so `build_docx.py` converts the Markdown to
`.docx` with the correct Aqualia typography, heading styles, tables, and
colour palette baked in. It's a build tool, not the report.

Think of it like a compiler: you edit the source (`.md`), run the build
script, and out pops the final artifact (`.docx`).

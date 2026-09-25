#!/usr/bin/env python3
"""Render Appendix A + B (from gen_sources_lists.build_appendix_data) and Appendix C into a DOCX.

Imported by generate_docx.py: add_appendices(doc). Appendix B lists are computed from
analysis.json + dupes.json at build time, never hand-written.

Usage (standalone smoke test): python3 audit_appendix.py  -> writes _appendix_test.docx
"""
import re
from docx import Document
from docx.shared import Pt
from gen_sources_lists import build_appendix_data, TITLES


def _table(doc, header, rows):
    t = doc.add_table(rows=1, cols=len(header)); t.style = "Light Grid Accent 1"
    for c, h in zip(t.rows[0].cells, header):
        c.text = ""; c.paragraphs[0].add_run(h).bold = True
    for r in rows:
        cells = t.add_row().cells
        for c, v in zip(cells, r): c.text = str(v)
    for row in t.rows:
        for c in row.cells:
            for p in c.paragraphs:
                for run in p.runs: run.font.size = Pt(8.5)
    doc.add_paragraph()


def add_appendices(doc):
    d = build_appendix_data()
    doc.add_page_break(); doc.add_heading("Appendix A: Data Sources and Coverage", 1)
    _table(doc, ["Report section", "Data source", "Coverage"], d["A"])
    doc.add_heading("Pages Lighthouse / CWV ran on (mobile)", 2)
    for u in d["lighthouse_urls"]: doc.add_paragraph(u, style="List Number")
    doc.add_paragraph("Lighthouse ran on all 7 in-scope pages, but from a cloud container through an HTTPS proxy, which "
                      "inflates FCP/LCP/Speed Index. No field (CrUX) data was collected.")
    doc.add_heading("Sources NOT used", 2)
    _table(doc, ["Source", "Reason"], d["not_used"])

    doc.add_page_break(); doc.add_heading("Appendix B: Action Lists (full URLs)", 1)
    doc.add_paragraph("Generated from analysis.json and dupes.json by gen_sources_lists.py / audit_appendix.py.")
    for k, items in d["B"].items():
        doc.add_heading(f"{TITLES[k]} ({len(items)})", 3)
        for i in items or ["None found"]:
            p = doc.add_paragraph(i, style="List Bullet")
            for r in p.runs: r.font.size = Pt(8.5)

    doc.add_page_break(); doc.add_heading("Appendix C: Original Prompt and Run Record", 1)
    txt = open("APPENDIX-C-ORIGINAL-PROMPT.md").read()
    body = re.sub(r"^# .*\n", "", txt, count=1)
    return body  # markdown rendered by the caller's converter


if __name__ == "__main__":
    doc = Document(); add_appendices(doc); doc.save("_appendix_test.docx"); print("ok")

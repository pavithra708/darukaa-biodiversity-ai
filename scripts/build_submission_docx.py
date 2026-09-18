#!/usr/bin/env python
"""Build a valid .docx with stdlib only (no lxml) for Application Control environments."""

from __future__ import annotations

import re
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "docs" / "SUBMISSION.md"
OUT = ROOT / "docs" / "Darukaa_Submission.docx"

CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>
"""

RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>
"""

DOC_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
</Relationships>
"""


def _runs(text: str) -> str:
    parts = re.split(r"(\*\*[^*]+\*\*|`[^`]+`)", text)
    chunks: list[str] = []
    for part in parts:
        if not part:
            continue
        bold = part.startswith("**") and part.endswith("**")
        code = part.startswith("`") and part.endswith("`")
        raw = part[2:-2] if bold else part[1:-1] if code else part
        props = ""
        if bold:
            props = "<w:rPr><w:b/></w:rPr>"
        elif code:
            props = '<w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/></w:rPr>'
        chunks.append(f"<w:r>{props}<w:t xml:space=\"preserve\">{escape(raw)}</w:t></w:r>")
    return "".join(chunks) or "<w:r><w:t></w:t></w:r>"


def _p(text: str, style: str | None = None) -> str:
    ppr = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
    return f"<w:p>{ppr}{_runs(text)}</w:p>"


def md_to_document_xml(md: str) -> str:
    body: list[str] = []
    in_code = False
    for raw in md.splitlines():
        line = raw.rstrip()
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            body.append(_p(line))
            continue
        if not line:
            body.append("<w:p/>")
        elif line.startswith("# "):
            body.append(_p(line[2:], "Heading1"))
        elif line.startswith("## "):
            body.append(_p(line[3:], "Heading2"))
        elif line.startswith("### "):
            body.append(_p(line[4:], "Heading3"))
        elif line.startswith("- "):
            body.append(_p("• " + line[2:]))
        elif line.startswith("> "):
            body.append(_p(line[2:]))
        else:
            body.append(_p(line))

    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    {''.join(body)}
    <w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>
  </w:body>
</w:document>
"""


def main() -> None:
    md = SRC.read_text(encoding="utf-8")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", CONTENT_TYPES)
        zf.writestr("_rels/.rels", RELS)
        zf.writestr("word/_rels/document.xml.rels", DOC_RELS)
        zf.writestr("word/document.xml", md_to_document_xml(md))
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Quick DOCX integrity audit for thesis review.

Checks XML parseability, counts paragraphs/tables/media, and verifies that internal
hyperlink anchors point to existing bookmarks. This does not replace visual render QA.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from zipfile import ZipFile
from lxml import etree

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}


def read_xml(zf: ZipFile, name: str):
    return etree.fromstring(zf.read(name))


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: audit_docx_integrity.py thesis.docx", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"missing file: {path}", file=sys.stderr)
        return 2

    report = {"file": str(path), "ok": True, "errors": []}
    try:
        with ZipFile(path) as zf:
            names = set(zf.namelist())
            required = ["word/document.xml", "word/styles.xml", "word/_rels/document.xml.rels"]
            missing = [n for n in required if n not in names]
            if missing:
                report["ok"] = False
                report["errors"].append({"missing": missing})
                print(json.dumps(report, ensure_ascii=False, indent=2))
                return 1

            doc = read_xml(zf, "word/document.xml")
            read_xml(zf, "word/styles.xml")
            rels = read_xml(zf, "word/_rels/document.xml.rels")

            rel_ids = {rel.get("Id") for rel in rels}
            bookmarks = {b.get(f"{{{NS['w']}}}name") for b in doc.xpath("//w:bookmarkStart", namespaces=NS)}
            anchors = doc.xpath("//w:hyperlink[@w:anchor]/@w:anchor", namespaces=NS)
            rel_links = doc.xpath("//w:hyperlink[@r:id]/@r:id", namespaces=NS)
            broken_anchors = [a for a in anchors if a not in bookmarks]
            broken_rels = [r for r in rel_links if r not in rel_ids]
            media = [n for n in names if n.startswith("word/media/")]

            report.update({
                "paragraphs": len(doc.xpath("//w:body/w:p", namespaces=NS)),
                "tables": len(doc.xpath("//w:tbl", namespaces=NS)),
                "media_files": len(media),
                "bookmarks": len(bookmarks),
                "internal_hyperlink_anchors": len(anchors),
                "external_hyperlinks": len(rel_links),
                "broken_anchors": broken_anchors,
                "broken_relationship_links": broken_rels,
            })
            if broken_anchors or broken_rels:
                report["ok"] = False
    except Exception as exc:
        report["ok"] = False
        report["errors"].append(repr(exc))

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

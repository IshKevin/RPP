import io
import json
import zipfile
from datetime import datetime

from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas


def _pdf_one_pager(book: dict, keywords: list, hashtags: list) -> bytes:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=LETTER)
    width, height = LETTER

    y = height - 72
    c.setFont("Helvetica-Bold", 18)
    c.drawString(72, y, book.get("title", ""))
    y -= 22
    c.setFont("Helvetica", 11)
    subtitle = book.get("subtitle") or ""
    if subtitle:
        c.drawString(72, y, subtitle[:110])
        y -= 16

    c.setFont("Helvetica-Bold", 12)
    c.drawString(72, y, "Description")
    y -= 14
    c.setFont("Helvetica", 10)
    desc = (book.get("description") or "").strip()
    for line in _wrap(desc, 95)[:12]:
        c.drawString(72, y, line)
        y -= 12

    y -= 6
    c.setFont("Helvetica-Bold", 12)
    c.drawString(72, y, "Keywords")
    y -= 14
    c.setFont("Helvetica", 10)
    c.drawString(72, y, ", ".join(keywords)[:120])
    y -= 18

    c.setFont("Helvetica-Bold", 12)
    c.drawString(72, y, "Hashtags")
    y -= 14
    c.setFont("Helvetica", 10)
    c.drawString(72, y, " ".join(hashtags)[:140])

    y -= 22
    c.setFont("Helvetica-Bold", 12)
    c.drawString(72, y, "Links")
    y -= 14
    c.setFont("Helvetica", 10)
    c.drawString(72, y, f"Landing page: {book.get('public_url','')}")
    y -= 12
    c.drawString(72, y, f"Buy link: {book.get('buy_url','')}")

    c.showPage()
    c.save()
    return buf.getvalue()


def _wrap(text: str, width: int) -> list:
    words = (text or "").split()
    lines = []
    cur = []
    cur_len = 0
    for w in words:
        add = len(w) + (1 if cur else 0)
        if cur_len + add > width:
            lines.append(" ".join(cur))
            cur = [w]
            cur_len = len(w)
        else:
            cur.append(w)
            cur_len += add
    if cur:
        lines.append(" ".join(cur))
    return lines


def build_launch_pack_zip(book: dict, keywords: list, hashtags: list, ad_scripts: dict) -> bytes:
    """Build a ZIP containing a PDF one-pager + CSV + ad scripts."""
    now = datetime.utcnow().strftime("%Y-%m-%d")
    pdf = _pdf_one_pager(book, keywords, hashtags)

    csv_lines = ["type,value"]
    for k in keywords:
        csv_lines.append(f"keyword,{k}")
    for h in hashtags:
        csv_lines.append(f"hashtag,{h}")
    csv_bytes = ("\n".join(csv_lines) + "\n").encode("utf-8")

    scripts_json = json.dumps(ad_scripts, ensure_ascii=False, indent=2).encode("utf-8")

    zbuf = io.BytesIO()
    with zipfile.ZipFile(zbuf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(f"RevenuePressAI_LaunchPack_{now}.pdf", pdf)
        z.writestr(f"RevenuePressAI_KeywordsHashtags_{now}.csv", csv_bytes)
        z.writestr(f"RevenuePressAI_AdScripts_{now}.json", scripts_json)

    return zbuf.getvalue()

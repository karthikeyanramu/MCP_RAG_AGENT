"""
HTML + PDF SUMMARY REPORT GENERATOR (CLEAN VERSION)

Features:
- Small pie chart
- Clean QA report layout
- HTML + PDF export
"""

from datetime import datetime
import json
import os

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet


"""
HTML + PDF SUMMARY REPORT GENERATOR (IMPROVED LAYOUT)

Generates a polished HTML report and a readable PDF with simple
charts and a clear table. The HTML is responsive and the PDF uses
reportlab styles for better appearance.
"""

from datetime import datetime
import json
import os

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch


TEST_HISTORY = []


def _safe_str(v):
    try:
        return str(v)
    except Exception:
        return ""


def generate_html_report(user_query, response, status, message):

    try:
        data = response if isinstance(response, dict) else json.loads(response)
    except Exception:
        data = {"raw": _safe_str(response)}

    status_code = data.get("status_code", "N/A")
    method = data.get("method_executed") or data.get("method") or "N/A"
    url = data.get("url", "N/A")
    body = data.get("response_body", data.get("response", data))

    # STORE HISTORY
    TEST_HISTORY.append({
        "query": user_query,
        "status": status,
        "status_code": status_code,
        "message": message,
        "method": method,
        "url": url,
        "body": body,
    })

    total = len(TEST_HISTORY)
    passed = len([t for t in TEST_HISTORY if t["status"] == "PASS"])
    failed = total - passed

    # HTML report (clean modern style)
    html = f"""
    <html>
    <head>
      <meta charset="utf-8">
      <title>API QA Report</title>
      <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
      <style>
        :root {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial; color-scheme: light; }}
        body {{ margin: 20px; color: #222; }}
        header {{ display:flex; justify-content:space-between; align-items:center; gap:20px; }}
        h1 {{ margin: 0; font-size: 20px; }}
        .meta {{ color: #666; font-size: 13px; }}
        .summary {{ display:flex; gap:12px; margin-top:12px; }}
        .card {{ padding:10px 14px; border-radius:8px; background:#f5f7fb; min-width:110px; text-align:center; }}
        .card strong {{ display:block; font-size:18px; color:#111; }}
        table {{ width:100%; border-collapse:collapse; margin-top:18px; font-size:13px; }}
        th, td {{ padding:8px 10px; border:1px solid #e6e9ef; text-align:left; vertical-align:top; }}
        th {{ background:#0f1724; color:white; font-weight:600; }}
        .small {{ font-size:12px; color:#555; }}
        pre {{ white-space:pre-wrap; word-wrap:break-word; font-family:monospace; font-size:12px; background:#fafafa; padding:8px; border-radius:6px; border:1px solid #eee; }}
      </style>
    </head>
    <body>
      <header>
        <div>
          <h1>API QA Report</h1>
          <div class="meta">Generated: {datetime.now().isoformat(timespec='seconds')}</div>
        </div>
        <div style="width:220px;">
          <canvas id="pieChart"></canvas>
        </div>
      </header>

      <div class="summary">
        <div class="card"><span class="small">Total</span><strong>{total}</strong></div>
        <div class="card"><span class="small">Passed</span><strong style="color:#16a34a">{passed}</strong></div>
        <div class="card"><span class="small">Failed</span><strong style="color:#dc2626">{failed}</strong></div>
      </div>

      <h3 style="margin-top:20px">Executed APIs</h3>
      <table>
        <tr><th>API</th><th>Method</th><th>Status</th><th>Code</th><th>Message</th></tr>
        {''.join([f"<tr><td>{t['query']}</td><td>{t.get('method','N/A')}</td><td>{t['status']}</td><td>{t['status_code']}</td><td>{t['message']}</td></tr>" for t in TEST_HISTORY])}
      </table>

      <h3 style="margin-top:20px">Details</h3>
      {''.join([f"<section style='margin-bottom:14px'><h4 style='margin:2px 0'>{t['query']} <small class='small'>({t.get('method')})</small></h4><div class='small'>Endpoint: {t.get('url')}</div><div style='margin-top:6px'><pre>{json.dumps(t.get('body'), indent=2)}</pre></div></section>" for t in TEST_HISTORY])}

      <script>
        new Chart(document.getElementById('pieChart'), {{ type:'pie', data: {{ labels:['PASS','FAIL'], datasets:[{{ data:[{passed},{failed}], backgroundColor:['#16a34a','#dc2626'] }}] }} }});
      </script>
    </body>
    </html>
    """

    os.makedirs("api_reports", exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    html_file = f"api_reports/report_{timestamp}.html"
    pdf_file = f"api_reports/report_{timestamp}.pdf"

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)

    # PDF generation: improved layout
    try:
        doc = SimpleDocTemplate(pdf_file, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('Title', parent=styles['Title'], fontSize=18, leading=22)
        normal = styles['Normal']
        content = []

        content.append(Paragraph("API QA TEST REPORT", title_style))
        content.append(Spacer(1, 8))
        content.append(Paragraph(f"Generated: {datetime.now().isoformat(timespec='seconds')}", normal))
        content.append(Spacer(1, 8))
        content.append(Paragraph(f"Total: {total} &nbsp;&nbsp; Passed: {passed} &nbsp;&nbsp; Failed: {failed}", normal))
        content.append(Spacer(1, 12))

        table_data = [["API", "Method", "Status", "Code", "Message"]]
        for t in TEST_HISTORY:
            table_data.append([t['query'], t.get('method', 'N/A'), t['status'], _safe_str(t['status_code']), _safe_str(t['message'])])

        tbl = Table(table_data, colWidths=[2.6*inch, 0.9*inch, 0.9*inch, 0.7*inch, 2.0*inch])
        tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f1724')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dfe6f0')),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')
        ]))

        content.append(tbl)
        content.append(Spacer(1, 12))

        # Add details as paragraphs
        for t in TEST_HISTORY:
            content.append(Paragraph(t['query'], ParagraphStyle('h4', parent=styles['Heading4'])))
            content.append(Paragraph(f"Endpoint: {t.get('url')}", normal))
            content.append(Spacer(1, 4))
            try:
                body_text = json.dumps(t.get('body'), indent=2)
            except Exception:
                body_text = _safe_str(t.get('body'))
            content.append(Paragraph('<pre>%s</pre>' % body_text.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;'), ParagraphStyle('mono', parent=styles['Code'], fontName='Courier', fontSize=8)))
            content.append(Spacer(1, 8))

        doc.build(content)

    except Exception as e:
        print("PDF generation failed:", str(e))

    return html_file
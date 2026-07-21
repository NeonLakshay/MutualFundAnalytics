from pathlib import Path
import sqlite3
import pandas as pd
from datetime import datetime

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "db" / "bluestock_mf.db"

conn = sqlite3.connect(DB_PATH)


def generate_weekly_summary():

    total_funds = pd.read_sql("""
        SELECT COUNT(*) AS total
        FROM dim_fund
    """, conn).iloc[0]["total"]

    avg_nav = pd.read_sql("""
        SELECT ROUND(AVG(nav),2) AS avg_nav
        FROM fact_nav
    """, conn).iloc[0]["avg_nav"]

    total_nav = pd.read_sql("""
        SELECT COUNT(*) AS total
        FROM fact_nav
    """, conn).iloc[0]["total"]

    total_transactions = pd.read_sql("""
        SELECT COUNT(*) AS total
        FROM fact_transactions
    """, conn).iloc[0]["total"]

    avg_return = pd.read_sql("""
        SELECT ROUND(AVG(return_3yr_pct),2) AS avg_return
        FROM fact_performance
    """, conn).iloc[0]["avg_return"]

    top_funds = pd.read_sql("""
        SELECT
            scheme_name,
            return_3yr_pct
        FROM fact_performance p
        JOIN dim_fund f
            ON p.amfi_code = f.amfi_code
        ORDER BY return_3yr_pct DESC
        LIMIT 5
    """, conn)

    conn.close()

    return {
        "total_funds": total_funds,
        "total_nav": total_nav,
        "avg_nav": avg_nav,
        "total_transactions": total_transactions,
        "avg_return": avg_return,
        "top_funds": top_funds
    }


def generate_html_report(report):

    print(">>> ENTERED generate_html_report()")

    total_funds = report["total_funds"]
    total_nav = report["total_nav"]
    avg_nav = report["avg_nav"]
    avg_return = report["avg_return"]
    top_funds = report["top_funds"]

    html = f"""
<!DOCTYPE html>
<html>

<head>

<meta charset="UTF-8">

<title>Bluestock Weekly Report</title>

<style>

body {{
    background:#F3F6FA;
    font-family:Arial, Helvetica, sans-serif;
    margin:0;
    padding:40px;
}}

.container {{
    max-width:950px;
    margin:auto;
    background:white;
    border-radius:16px;
    overflow:hidden;
    box-shadow:0px 10px 30px rgba(0,0,0,.15);
}}

.header {{
    background:#1E3A8A;
    color:white;
    text-align:center;
    padding:35px;
}}

.header h1 {{
    margin:0;
    font-size:34px;
}}

.header p {{
    margin-top:10px;
    font-size:18px;
}}

.section {{
    padding:35px;
}}

.cards {{
    display:flex;
    justify-content:space-between;
    gap:18px;
    margin-bottom:35px;
}}

.card {{
    flex:1;
    background:#EEF4FF;
    border-radius:12px;
    padding:20px;
    text-align:center;
}}

.card h2 {{
    margin:0;
    color:#1E3A8A;
    font-size:32px;
}}

.card p {{
    margin-top:8px;
    color:#555;
}}

table {{
    width:100%;
    border-collapse:collapse;
    margin-top:20px;
}}

th {{
    background:#2563EB;
    color:white;
    padding:14px;
}}

td {{
    padding:12px;
    border-bottom:1px solid #E5E7EB;
}}

tr:nth-child(even) {{
    background:#F8FAFC;
}}

tr:hover {{
    background:#EEF4FF;
}}

.footer {{
    text-align:center;
    color:gray;
    font-size:14px;
    padding:25px;
}}

</style>

</head>

<body>

<div class="container">

<div class="header">
<h1>📊 Bluestock Mutual Fund Analytics</h1>
<p>Weekly Performance Summary</p>
</div>

<div class="section">

<div class="cards">

<div class="card">
<h2>{total_funds}</h2>
<p>Total Funds</p>
</div>

<div class="card">
<h2>{total_nav:,}</h2>
<p>NAV Records</p>
</div>

<div class="card">
<h2>{avg_nav:.2f}</h2>
<p>Average NAV</p>
</div>

<div class="card">
<h2>{avg_return:.2f}%</h2>
<p>Average 3-Year Return</p>
</div>

</div>

<h2>🏆 Top 5 Performing Mutual Funds</h2>

{top_funds.to_html(index=False, border=0)}

</div>

<div class="footer">

<hr>

<p>
Generated Automatically on
<b>{datetime.now().strftime("%d %B %Y")}</b>
</p>

<p>
Developed with ❤️ using
<b>Python</b> •
<b>SQLite</b> •
<b>Pandas</b> •
<b>HTML</b>
</p>

<p>
© 2026 Bluestock Mutual Fund Analytics
</p>

</div>

</div>

</body>
</html>
"""

    output_file = BASE_DIR / "weekly_report.html"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ HTML Report Generated Successfully!")
    print("Saved to:", output_file)

def send_email():

    sender_email = "lakshay8941@gmail.com"
    sender_password = "ddib wqec ijkn xgaf"

    receiver_email = "mnsingh1677@gmail.com"

    report_file = BASE_DIR / "weekly_report.html"

    with open(report_file, "r", encoding="utf-8") as f:
        html = f.read()

    message = MIMEMultipart("alternative")

    message["Subject"] = "📊 Weekly Mutual Fund Performance Report"

    message["From"] = sender_email

    message["To"] = receiver_email

    message.attach(MIMEText(html, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:

        server.starttls()

        server.login(sender_email, sender_password)

        server.send_message(message)

    print("✅ Email sent successfully!")

if __name__ == "__main__":

    report = generate_weekly_summary()

    # IMPORTANT: THIS WAS MISSING
    generate_html_report(report)

    total_funds = report["total_funds"]
    total_nav = report["total_nav"]
    avg_nav = report["avg_nav"]
    avg_return = report["avg_return"]
    top_funds = report["top_funds"]

    print("=" * 60)
    print("WEEKLY SUMMARY")
    print("=" * 60)

    print(f"Total Funds       : {total_funds}")
    print(f"Total NAV Records : {total_nav}")
    print(f"Average NAV       : {avg_nav:.2f}")
    print(f"Average 3Y Return : {avg_return:.2f}%")

    print("\nTop 5 Performing Funds")
    print(top_funds)

    send_email()













    
import json
from datetime import datetime

def export_json(results,  filename):
    with open(filename, "w") a f:
        json.dump(results, f, indent=4)

def export_html(results, filename):
    rows = " "
    for r in results:
        rows += f"<tr><td>{r['password']}</td></tr>"

    html = f " " "
    <html>
    <body>
    <h1>PascoLock Report</h1>
    <table border =" 1 ">
    <tr><th>Password</th><th>Score</th></tr>
    {rows}
    </table>
    </body>
    </html>
    " " "
    open(filename, "w").write(html)


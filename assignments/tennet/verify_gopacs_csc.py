import hashlib
import io
from datetime import datetime, timezone

import pandas as pd
import requests

url = "https://www.gopacs.eu/wp-content/uploads/2026/10/CSC_public_report_2026-10-01-0925.xlsx"

try:
    r = requests.get(url, timeout=45)
    print("HTTP status:", r.status_code)
    print("Content-Type:", r.headers.get("content-type"))
    r.raise_for_status()

    if not r.content.startswith(b"PK"):
        raise ValueError("The response is not an Excel XLSX file.")

    print("File size:", len(r.content))
    print("SHA-256:", hashlib.sha256(r.content).hexdigest())
    print("Retrieved UTC:", datetime.now(timezone.utc).isoformat())

    excel = pd.ExcelFile(io.BytesIO(r.content))
    print("Sheets:", excel.sheet_names)

    for sheet in excel.sheet_names:
        print("\n---", sheet, "---")
        df = pd.read_excel(
            io.BytesIO(r.content), sheet_name=sheet,
            header=None, nrows=8
        )
        print(df.to_string(index=False, header=False))

    with open("csc_public_report.xlsx", "wb") as f:
        f.write(r.content)

    print("\nSUCCESS: Excel file saved.")

except Exception as e:
    print("VERIFICATION FAILED:", repr(e))

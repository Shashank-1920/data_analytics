from fastapi import FastAPI
import mysql.connector
from datetime import timedelta

app = FastAPI()

# ---------- UTIL ----------
def get_connection(cfg):
    return mysql.connector.connect(
        host=cfg["host"],
        port=cfg["port"],
        user=cfg["user"],
        password=cfg["password"],
        database=cfg["schema"]
    )

# ---------- CONNECT ----------
@app.post("/connect")
def connect_db(cfg: dict):
    try:
        conn = get_connection(cfg)
        conn.close()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ---------- LIST TABLES ----------
@app.post("/tables")
def list_tables(cfg: dict):
    conn = get_connection(cfg)
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables

# ---------- FETCH ----------
def fetch_rows(cfg, table):
    conn = get_connection(cfg)
    cursor = conn.cursor(dictionary=True)

    cursor.execute(f"""
        SELECT customer_id, order_date
        FROM {table}
        ORDER BY customer_id, order_date
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows

# ---------- ANALYSIS ----------
def analyze(rows):
    data = {}
    for r in rows:
        data.setdefault(r["customer_id"], []).append(r["order_date"])

    results = []

    for cid, dates in data.items():
        if len(dates) < 2:
            continue

        gaps = [(dates[i] - dates[i-1]).days for i in range(1, len(dates))]
        avg_gap = sum(gaps) / len(gaps)

        label = (
            "Frequent" if avg_gap <= 7 else
            "Moderate" if avg_gap <= 20 else
            "Infrequent"
        )

        last = dates[-1]

        results.append({
            "customer_id": cid,
            "total_orders": len(dates),
            "avg_days_between_orders": round(avg_gap, 2),
            "customer_type": label,
            "predicted_next_order": last + timedelta(days=round(avg_gap))
        })

    return results

# ---------- ANALYZE ----------
@app.post("/analyze")
def analyze_table(payload: dict):
    cfg = payload["db"]
    table = payload["table"]

    rows = fetch_rows(cfg, table)
    return analyze(rows)

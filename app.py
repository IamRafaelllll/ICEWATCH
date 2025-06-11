from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)
DB = "database.db"

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY,
            city TEXT,
            agents INTEGER,
            detained TEXT,
            timestamp TEXT
        )''')

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    with sqlite3.connect(DB) as conn:
        conn.execute("INSERT INTO reports (city, agents, detained, timestamp) VALUES (?, ?, ?, ?)", (
            data["city"], data["agents"], data["detained"], datetime.utcnow().isoformat()))
    return jsonify({"status": "success"})

@app.route("/reports")
def reports():
    five_days_ago = datetime.utcnow() - timedelta(days=5)
    with sqlite3.connect(DB) as conn:
        cursor = conn.execute("SELECT city, agents, detained, timestamp FROM reports")
        results = []
        for row in cursor:
            ts = datetime.fromisoformat(row[3])
            if ts > five_days_ago:
                results.append({
                    "city": row[0],
                    "agents": row[1],
                    "detained": row[2],
                    "timestamp": ts.isoformat()
                })
    return jsonify(results)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=10000)

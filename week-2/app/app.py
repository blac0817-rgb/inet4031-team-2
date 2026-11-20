import os
import time

import psycopg2
import psycopg2.extras
from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

metrics = PrometheusMetrics(app)

DATABASE_URL = os.environ["DATABASE_URL"]

SCHEMA = """
CREATE TABLE IF NOT EXISTS incidents (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    status TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
ALTER TABLE incidents ADD COLUMN IF NOT EXISTS category TEXT;
ALTER TABLE incidents ADD COLUMN IF NOT EXISTS resolved_at TIMESTAMPTZ;
"""


def get_conn():
    return psycopg2.connect(DATABASE_URL)


def init_schema():
    # Postgres may still be finishing initialization even after the compose
    # healthcheck passes db as healthy but before flask's own health probe
    # has run once; retry briefly rather than crash-looping on first boot.
    last_error = None
    for _ in range(10):
        try:
            with get_conn() as conn, conn.cursor() as cur:
                cur.execute(SCHEMA)
                conn.commit()
            return
        except psycopg2.OperationalError as exc:
            last_error = exc
            time.sleep(2)
    raise RuntimeError(f"could not initialize schema: {last_error}")


def iso(value):
    return value.isoformat() if value is not None else None


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/incidents", methods=["GET"])
def list_incidents():
    try:
        limit = max(1, min(int(request.args.get("limit", 100)), 5000))
        offset = max(0, int(request.args.get("offset", 0)))
    except ValueError:
        return jsonify(error="limit and offset must be integers"), 400

    with get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            "SELECT id, title, status, description, created_at, category, resolved_at "
            "FROM incidents ORDER BY created_at DESC, id DESC LIMIT %s OFFSET %s",
            (limit, offset),
        )
        rows = cur.fetchall()
    return jsonify([
        dict(row, created_at=iso(row["created_at"]), resolved_at=iso(row["resolved_at"]))
        for row in rows
    ])


@app.route("/incidents", methods=["POST"])
def create_incident():
    body = request.get_json(force=True, silent=True) or {}
    title = body.get("title")
    status = body.get("status")
    description = body.get("description")

    if not title or not status:
        return jsonify(error="title and status are required"), 400

    with get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            "INSERT INTO incidents (title, status, description) VALUES (%s, %s, %s) "
            "RETURNING id, title, status, description, created_at",
            (title, status, description),
        )
        row = cur.fetchone()
        conn.commit()

    return jsonify(dict(row, created_at=row["created_at"].isoformat())), 201


init_schema()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

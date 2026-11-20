"""Generates synthetic Harborlight incidents with planted structure.

Run (reads this file from the host and runs it in the flask container):
  docker compose -f week-2/docker-compose.yml exec -T flask \
    python3 - --rows 12000 < capstone/data-science/generate.py

All data is synthetic. No real customer names or personal data.
Re-running first deletes this script's earlier rows (category IS NOT NULL),
then reloads. Rows from the old seed.py (category IS NULL) are untouched.
"""
import argparse
import math
import os
import random
from datetime import datetime, timedelta, timezone

import psycopg2
import psycopg2.extras

SEED = 4031
DAYS = 95
WEEKLY_GROWTH = 0.02      # planted: ~2% more incidents each week
WEEKEND_FACTOR = 0.25     # planted: weekends are ~1/4 as busy

# name: (share of volume, median resolution hours, lognormal sigma, titles)
CATEGORIES = {
    "Scanners and handhelds": (0.28, 3.0, 0.8, [
        "Handheld scanner will not pair with dock",
        "Barcode scanner not reading labels",
        "Handheld battery drains within an hour",
        "Scanner firmware update failed",
    ]),
    "Dispatch app": (0.22, 4.0, 0.9, [
        "Dispatch app crashes on route load",
        "Driver assignments not syncing",
        "Dispatch app shows stale delivery status",
        "Route optimizer times out",
    ]),
    "Printers and labels": (0.18, 2.0, 0.6, [
        "Shipping label printer offline",
        "Labels printing misaligned",
        "Thermal printer paper jam",
        "Label template missing after update",
    ]),
    "Logins and access": (0.20, 1.0, 0.6, [
        "Cannot log in after password reset",
        "Account locked out",
        "Badge access denied at dock door",
        "MFA code not arriving",
    ]),
    "Network": (0.12, 8.0, 1.2, [      # planted: slowest, longest tail
        "Warehouse Wi-Fi dropping intermittently",
        "Dock VPN connection failing",
        "Slow network at loading bay",
        "Switch down in sorting area",
    ]),
}

# Planted hourly pattern (UTC hour): busy 8-17, light overnight
HOUR_WEIGHTS = [1, 1, 1, 1, 1, 2, 3, 6, 10, 12, 12, 11, 9, 11, 12, 11, 9, 6, 3, 2, 1, 1, 1, 1]


def make_row(end, day_weights, days):
    cat = random.choices(list(CATEGORIES), weights=[c[0] for c in CATEGORIES.values()])[0]
    _, median_h, sigma, titles = CATEGORIES[cat]
    while True:
        d = random.choices(range(days), weights=day_weights)[0]
        day = (end - timedelta(days=days - 1 - d)).replace(hour=0, minute=0, second=0, microsecond=0)
        hour = random.choices(range(24), weights=HOUR_WEIGHTS)[0]
        created = day + timedelta(hours=hour, minutes=random.randint(0, 59),
                                  seconds=random.randint(0, 59))
        if created <= end:
            break
    duration_h = min(random.lognormvariate(math.log(median_h), sigma), 24 * 21)
    resolved = created + timedelta(hours=duration_h)
    if resolved <= end:
        status, resolved_at = "closed", resolved
    else:
        status, resolved_at = random.choice(["open", "in_progress"]), None
    title = random.choice(titles)
    desc = f"Synthetic incident record ({title.lower()})."
    return title, status, desc, created, cat, resolved_at


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=12000)
    args = parser.parse_args()

    random.seed(SEED)
    end = datetime.now(timezone.utc)
    day_weights = []
    for d in range(DAYS):
        day = end - timedelta(days=DAYS - 1 - d)
        wk = 1.0 if day.weekday() < 5 else WEEKEND_FACTOR
        day_weights.append(wk * (1 + WEEKLY_GROWTH) ** (d / 7))

    rows = [make_row(end, day_weights, DAYS) for _ in range(args.rows)]

    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    with conn, conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM incidents")
        print("rows before:", cur.fetchone()[0])
        cur.execute("DELETE FROM incidents WHERE category IS NOT NULL")
        print("deleted earlier generated rows:", cur.rowcount)
        psycopg2.extras.execute_values(
            cur,
            "INSERT INTO incidents (title, status, description, created_at, category, resolved_at) VALUES %s",
            rows,
        )
        cur.execute("SELECT COUNT(*) FROM incidents")
        print("rows after:", cur.fetchone()[0])
    conn.close()


if __name__ == "__main__":
    main()

# Harborlight Support Desk Analysis (Approach B: Python pipeline)

Pulls incidents from the statustracker API, cleans them with pandas, and writes
data quality checks, three analysis CSVs, three charts, a statistical check,
and supports the staffing report in `report.md`.

All data is synthetic. It contains no real customer names or personal data.

## Files
| File | Purpose |
|---|---|
| `DATA.md` | Data plan: what was generated and planted, and its limits |
| `generate.py` | Seeded generator that loads synthetic incidents into Postgres |
| `pipeline.py` | One command: fetch, clean, aggregate, test, chart |
| `report.md` | Staffing recommendation for Dana |
| `requirements.txt` | Python dependencies for the pipeline |
| `output/` | All generated CSVs, PNGs, and statistics |

## Prerequisites
- Docker Compose stack in `week-2/` running (db, flask, nginx)
- Python 3 on the host with `venv`

## 1. Start the stack
From the repo root:

```bash
docker compose -f week-2/docker-compose.yml up -d --build
docker compose -f week-2/docker-compose.yml ps
```

nginx publishes the API on host port 8092 (set by `HOST_PORT`). Confirm:

```bash
curl -s "http://localhost:8092/incidents?limit=1"
```

## 2. Generate and load the data (run once)
From the repo root:

```bash
docker compose -f week-2/docker-compose.yml exec -T flask \
  python3 - --rows 10500 < capstone/data-science/generate.py
```

It prints rows before, rows deleted, and rows after. It deletes only its own
earlier rows, so it is safe to rerun. Rerunning regenerates timestamps relative
to the current time, so results will shift slightly.

## 3. Run the analysis (the one command)
```bash
cd capstone/data-science
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 pipeline.py
```

To point at a different API address:

```bash
API_URL=http://localhost:8093 python3 pipeline.py
```

## Outputs (in `output/`)
| File | Content |
|---|---|
| `data_quality.csv` | Row counts, null counts, date range, criteria checks |
| `weekly_volume.csv` | Incidents per week, with a `complete_week` flag |
| `resolution_by_category.csv` | Median and 90th percentile hours to resolve, per category |
| `category_counts.csv` | Incident count per category, ranked highest to lowest |
| `hourly_volume.csv` | Average weekday arrivals per hour (UTC), used for staffing |
| `stats.csv`, `stats_summary.txt` | Trend slope and p-value; Network vs. Printers comparison; plain-English sentences |
| `chart_volume_trend.png` | Weekly volume with trend line |
| `chart_resolution_distribution.png` | Time to resolve by category |
| `chart_busiest_categories.png` | Incidents per category |

## Notes
- The `GET /incidents` route in `week-2/app/app.py` now supports `limit`
  (default 100, max 5000) and `offset`, and returns `category` and
  `resolved_at`. With no parameters it still returns 100 rows.
- The pipeline drops rows without a category, so older `seed.py` rows are ignored.
- The first and last weeks are partial and are excluded from the trend
  (flagged in `weekly_volume.csv`).
- Resolution statistics use closed incidents only.

## Troubleshooting
- **`Bind for 0.0.0.0:8092 failed: port is already allocated`:** another
  container holds the port. Use a free one:
  `HOST_PORT=8093 docker compose -f week-2/docker-compose.yml up -d`, then set `API_URL`.
- **`service "db" is not running`:** run `docker compose -f week-2/docker-compose.yml up -d`.
- **`No module named 'psycopg2'`:** `generate.py` must run inside the flask
  container (use the `exec` command above), not directly on the host.
- **API returns no `category` field:** rebuild flask with
  `docker compose -f week-2/docker-compose.yml up -d --build flask`.
- **Do not run `docker compose down -v`:** it deletes the database volume.

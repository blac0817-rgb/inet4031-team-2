# Data Plan

## Synthetic data notice
All data is synthetic. It contains no real customer names or personal data.

## Approach
We extended the existing `incidents` table with two columns:
`category` (TEXT) and `resolved_at` (TIMESTAMPTZ). The Flask app adds them
automatically at startup (`ALTER TABLE ... ADD COLUMN IF NOT EXISTS`), so a
fresh database gets them without a manual step.

- Generator: `capstone/data-science/generate.py`, random seed 4031
- Reload method: the generator deletes only its own earlier rows
  (`WHERE category IS NOT NULL`), then inserts a fresh batch. Rows without a
  category (for example from `week-2/app/seed.py`) are never deleted and are
  excluded from the analysis.
- Row counts from the run used in the report:
  - Rows before: 10,500
  - Deleted earlier generated rows: 10,500
  - Rows after: 10,500

## Size
10,500 rows over a 95-day generation window. The measured span in
`output/data_quality.csv` is 94.05 days. Criterion 1 minimums are 10,000 rows
and 90 days.

## Columns
| Column | Behavior |
|---|---|
| title | Drawn from a per-category list of four titles |
| category | One of 5 logistics categories |
| status | `closed` if resolved before generation time; otherwise `open` or `in_progress` |
| created_at | Weekday and business-hour weighted, about 2% weekly growth (UTC) |
| resolved_at | created_at + lognormal duration, capped at 21 days; NULL if not closed |

## Categories
| Category | Share of volume | Median resolution | Sigma |
|---|---|---|---|
| Scanners and handhelds | 28% | 3 hrs | 0.8 |
| Dispatch app | 22% | 4 hrs | 0.9 |
| Logins and access | 20% | 1 hr | 0.6 |
| Printers and labels | 18% | 2 hrs | 0.6 |
| Network | 12% | 8 hrs | 1.2 (longest tail) |

## What we planted
- Weekly volume grows about 2% per week
- Weekends run at 25% of weekday volume
- Peak hours roughly 08:00 to 17:00 UTC, light overnight
- Network has the longest resolution times and heaviest tail
- Scanners and handhelds is the highest-volume category
- The most recent incidents are more likely to be open (not enough time to resolve)

## What the analysis recovered
| Planted | Found |
|---|---|
| About 2% weekly growth | Slope +14.7 incidents/week, 1.9% of the average week (p = 2.3e-05, 12 complete weeks) |
| Network slowest | Median 8.21 h, p90 32.91 h |
| Scanners highest volume | 2,974 incidents, 28.3% |
| Business-hour peak | About 11 to 13 arrivals per weekday hour from 08:00 to 16:59 UTC; about 1 per hour overnight |

## Limits
- Resolution time is time open, not agent handling time. Staffing numbers need
  a separate handling-time assumption (see `report.md`).
- Every pattern found in the analysis exists because we planted it. The data
  demonstrates the method, not real Harborlight behavior.
- Timestamps are UTC. We treat UTC as the desk's local time.
- Only 21 of 10,500 incidents are open or in progress, because most resolve
  within hours. The backlog looks almost empty, which is a property of the
  generator, not evidence about real queues.
- Timestamps are generated relative to the time the generator runs. Rerunning it
  shifts all dates and slightly changes the results, so the committed `output/`
  files reflect one specific run.

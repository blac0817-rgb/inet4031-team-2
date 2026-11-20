# Data Plan

## Synthetic data notice
All data is synthetic. It contains no real customer names or personal data.

## Approach
Extended the existing `incidents` table with `category` (TEXT) and
`resolved_at` (TIMESTAMPTZ). Old `seed.py` rows (category IS NULL) are left
untouched and excluded from analysis.
Reload method: `generate.py` deletes only its own earlier rows
(category IS NOT NULL), then reloads.
Generator: `capstone/data-science/generate.py`, seed 4031.
Rows before / after: <paste from generator output>

## Size
10,500 rows over 95 days (success criterion 1 minimums: 10,000 rows, 90 days).

## Columns
| Column | Behavior |
|---|---|
| title | Drawn from a per-category list of four titles |
| category | 5 logistics categories |
| status | closed if resolved before "now"; otherwise open or in_progress |
| created_at | Weekday and business-hour weighted, 2% weekly growth |
| resolved_at | created_at + lognormal duration (capped at 21 days); NULL if not closed |

## Categories
| Category | Share | Median resolution | Sigma |
|---|---|---|---|
| Scanners and handhelds | 28% | 3 hrs | 0.8 |
| Dispatch app | 22% | 4 hrs | 0.9 |
| Logins and access | 20% | 1 hr | 0.6 |
| Printers and labels | 18% | 2 hrs | 0.6 |
| Network | 12% | 8 hrs | 1.2 (longest tail) |

## What we planted
- Weekly volume grows about 2% per week
- Weekends run at 25% of weekday volume
- Peak hours roughly 8:00-17:00 UTC, light overnight
- Network has the longest resolution times and heaviest tail
- Scanners and handhelds is the highest-volume category
- Recent incidents are more likely to be open (not enough time to resolve)

## Limits
Resolution time is time open, not agent handling time. Every pattern found
in the analysis exists because we planted it; this demonstrates the method,
not real Harborlight behavior. Timestamps are UTC.

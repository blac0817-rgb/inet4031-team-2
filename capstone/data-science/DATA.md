# Data Plan

## Synthetic data notice
All data is synthetic. It contains no real customer names or personal data.

## Approach
Extended the existing `incidents` table with `category` and `resolved_at`.
Reload method: <clear table first / append and filter on category IS NOT NULL>
Row counts: before <n>, after <n>.
Generator: `capstone/data-science/generate.py`, seed <n>.

## Columns
| Column | Behavior |
|---|---|
| title | Drawn from a per-category list of titles |
| category | 5 categories (see below) |
| status | closed / in progress / open, by age (older mostly closed) |
| created_at | Spread over 120 days, weekday and business-hour weighted, ~2% weekly growth |
| resolved_at | created_at + lognormal duration; NULL if not closed |

## Categories
| Category | Share of volume | Median resolution | Notes |
|---|---|---|---|
| Scanners and handhelds | ? | ? hrs | |
| Dispatch app | ? | ? hrs | |
| Printers and labels | ? | ? hrs | |
| Logins and access | ? | ? hrs | |
| Network | ? | ? hrs | long tail |

## What we planted
- Weekly volume grows about ?% per week
- Weekday > weekend, peak hours ?-?
- <category> has the longest resolution times
- <category> is the highest volume

## Limits
Resolution time is time open, not agent handling time. Patterns in the analysis
exist because we planted them.

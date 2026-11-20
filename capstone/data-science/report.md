# Support Desk Staffing: Findings and Recommendation

**Bottom line:** At today's volume the desk needs about **8 agents on duty at once** on weekdays from 08:00 to 17:00. If volume grows 20%, it needs about **10**. Six agents is not enough for the weekday daytime peak.

*All data in this report is synthetic. It contains no real customer names or personal data.*

## The question
Dana asked: are incidents growing, how long do they take to resolve, which kinds keep the desk busiest, and does the desk (six agents today) need more people?

## What we found

**1. Volume is growing, about 2% a week.** From 18 Aug to 20 Nov 2026 (94 days, 10,500 incidents), weekly volume rose by about 15 incidents per week (1.9% of an average week of roughly 770). The trend is statistically solid (p = 2.3e-05, 12 complete weeks), so it is very unlikely to be chance. It does not say why volume is rising or whether it will continue. See `output/chart_volume_trend.png`.

**2. Resolution times differ a lot by category.** Network incidents are slowest (median 8.2 hours, 90th percentile 32.9 hours). Logins and access are fastest (median 1.0 hour). The Network vs. Printers and labels gap is real (Mann-Whitney p = 2.7e-247), but it measures how long a ticket stays open, not how much work an agent does on it. See `output/chart_resolution_distribution.png`.

| Category | Median hours | 90th percentile hours |
|---|---|---|
| Network | 8.2 | 32.9 |
| Dispatch app | 4.1 | 12.7 |
| Scanners and handhelds | 3.1 | 8.5 |
| Printers and labels | 2.0 | 4.2 |
| Logins and access | 1.0 | 2.2 |

**3. Scanners and the dispatch app generate the most incidents.** Scanners and handhelds are 28.3% of volume and Dispatch app 22.0%, together about half. Logins (19.6%), Printers (18.0%) and Network (12.1%) follow. See `output/chart_busiest_categories.png`.

**Busiest hours:** weekday arrivals average about 11.8 per hour from 08:00 to 16:59 UTC (peak 12.9 at 14:00). Overnight is about 1 per hour.

## How we got the number
Agents on duty = (arrivals per hour x hours of agent work per incident) / share of time spent on incidents.

- Arrivals: 11.8 per hour (weekday 08:00 to 16:59 average; the peak hour is 12.9)
- Handling time: 0.5 hours per incident (assumption)
- Utilization: 75% (assumption; leaves room for breaks and bursts)
- 11.8 x 0.5 / 0.75 = 7.8, rounded up to **8 agents**. At the 14:00 peak: 12.9 x 0.5 / 0.75 = 8.6, so **9**.

## Assumptions and limits
- **Handling time is the biggest unknown.** Resolution time is time open, not time worked. We assumed 30 minutes; the table shows how much the answer depends on it.
- **The data is synthetic.** We planted the patterns we found: roughly 2% weekly growth, weekdays and business hours busier, Network slowest. The analysis shows the method works, not how Harborlight really behaves. Real data could change the answer.
- **Times are UTC.** We treat UTC as the desk's local time.
- **Concurrent agents are not headcount.** The figures are people on duty at the same moment. Six staff also have to cover shifts, breaks, nights, weekends and leave.
- **Volume levels:** hourly averages cover 12 weeks of rising volume, so recent weeks run somewhat higher.
- **Resolution statistics** use the 10,479 closed incidents (21 were still open).

| Handling time | Today (agents on duty) | If volume grows 20% |
|---|---|---|
| 20 minutes | 6 | 7 |
| 30 minutes (our assumption) | 8 | 10 |
| 45 minutes | 12 | 15 |

## If volume grows 20%
Arrivals rise from 11.8 to 14.1 per hour: 14.1 x 0.5 / 0.75 = 9.4, rounded up to **10 agents** (11 at the peak hour). At the observed trend of about 15 more incidents per week, a 20% increase arrives in roughly a quarter, so this case is worth planning for now.

## Recommendation
Staff **8 agents on duty on weekdays from 08:00 to 17:00 UTC today, rising to 10 if volume grows 20%**. Plausible range is 6 to 12 depending on true handling time, so measure handling time before final hiring. Outside those hours, about 1 agent overnight is enough (about 1 incident per hour). Weekends run at roughly a quarter of weekday volume, so 2 agents during the day. Prioritize scanner and dispatch-app expertise during the day, since they produce about half of all incidents; Network incidents are rarer but stay open longest and likely need senior attention.

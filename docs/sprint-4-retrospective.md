# Sprint 5 Retrospective

**Owned by:** Scrum Master

## What Went Well

We are zipping through labs now. Everyone is comfortable with how we have been flowing as a group, and work gets done fast as a result.

## What Could Be Better

Instructions do not always reminds us what files to add to git add before we commit. Being cognizant of what changed is neccessary.

## What We'll Do Differently Next Sprint

Vector check of modified or added files.

## Team Contributions

Use this section to note which team members led which parts of the work:

| Role | Name | Primary Contribution |
|---|---|---|
| Scrum Master | Diego | |
| System Admin | Ty | |
| QA | Marcos | |
| Developers | Jakob, Sumaya, Randeep, Tyler| |


## Sprint Goals

- Load the incident tracker database with ~50,000 synthetic records
- Use k6 to run baseline and ramped load tests
- Diagnose database-layer bottleneck (missing index)
- Diagnose infrastructure-layer bottleneck (CPU throttling)
- Fix both issues and measure improvement
- Add k6 threshold gate to GitHub Actions CI

## Metrics Achieved

- Database rows seeded: 5000
- Baseline P95 response time: 4.49s
- Post-fix P95 response time: 78.96ms
- CPU throttle rate before fix: 0
- CPU throttle rate after fix: 0
- k6 threshold gate: passes CI

## Notes

Any additional context about the sprint that does not fit the structure above.

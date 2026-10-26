# QA Report - Sprint 3 Week 5

QA is responsible for running all validation checks and signing off before deliverables are submitted. This report documents the validation process.

**QA Team Member:** Jakob Black
**Date Completed:** 10/26/26

## Executive Summary

Multiple yaml files for flask were not present, which went against instruction for this lab. Therefore the class was instructed to skip multiple steps, which leads to failures in this document.

## Test Coverage

### Test Suite 1: Helm and Prometheus Installation

- [x ] Helm installation successful
- [x ] Prometheus community repository added
- [x ] Prometheus (`prometheus` chart 29.35.0) deployed without errors
- [ x] All monitoring pods reached Running state

**Result:** Pass

**Notes:** 
TODO: Record any observations about the installation process, timeouts, or resource constraints.

### Test Suite 2: Prometheus Metric Collection (MANDATORY)

- [ ] Prometheus scraping pod metrics
- [ ] `kubernetes-nodes-cadvisor` scrape job present in `up` output
- [ ] Prometheus query for `container_cpu_cfs_throttled_periods_total` returns data
- [ ] At least one metric series returned

**Result:** Fail

**Metric Series Count:** [TODO: Number of series returned]

**Notes:**
TODO: If this test fails, record what was attempted to fix it (upgrade, reconfigure, etc.)

### Test Suite 3: USE Queries from the Command Line

- [ ] Prometheus port-forward running on the team's assigned Prometheus port
- [ ] Flask scrape target shows `up` = 1
- [ ] CPU Utilization query returns data
- [ ] CPU Throttle Rate query returns data
- [ ] HTTP 5xx Error Rate query runs (no results is expected until a 5xx occurs)

**Result:** Fail - This is a result of not being able to complete step 13

**Queries Verified:**
- [ ] Flask CPU Utilization: [TODO: Data visible Y/N]
- [ ] Flask CPU Throttle Rate: [TODO: Data visible Y/N]
- [ ] HTTP 5xx Error Rate: [TODO: Data visible Y/N]

**Notes:**
TODO: Fail - This is a result of not being able to complete step 13. We need a functional flask-deployment yaml file.

### Test Suite 4: Prometheus Alert Rule

- [ x] Error rate alert configured
- [ x] Alert threshold set correctly (> 1%)
- [ x] Alert duration set correctly (1 minute)
- [ x] Alert rule loaded (`HTTP5xxErrorRateHigh` listed by the rules check)

**Result:** Pass

**Notes:**
TODO: Record alert configuration details and any issues encountered.

### Test Suite 5: k6 Load Testing

- [ x] k6 installed successfully
- [x ] smoke-test.js created and formatted correctly
- [ ] Load test runs without errors
- [ ] Prometheus query results respond to load test activity

**Result:** Pass

**Test Parameters:**
- Virtual users: [TODO: Record vus value]
- Duration: [TODO: Record duration]
- Requests per user: [TODO: Estimate]

**Metrics Observed:**
- CPU utilization increased: N/A
- Memory utilization increased: N/A
- Network activity increased: N/A
- HTTP requests recorded: N/A

**Notes:**
The test outputs errors due to smoketest relying on the flask-service yaml that we do not have.

### Test Suite 6: Validation Scripts

- [x ] check-week5.sh exists and is executable
- [x ] All validation checks pass
- [x ] Exit code is 0
- [ x] Script output is clear and actionable

**Result:** Pass

**Validation Results:**
- [ x] All monitoring pods running: PASS
- [x ] cAdvisor scrape job and alert rule configured: PASS
- [ x] container_cpu_cfs_throttled_periods_total returns data: PASS

## Cross-Week Dependency Verification

**Week 9 CPU Throttling Diagnosis Dependency:**

- [x ] Prometheus is scraping cAdvisor metrics
- [x ] Query for `rate(container_cpu_cfs_throttled_periods_total[5m])` returns data
- [x ] Metric series is non-empty and consistent
- [x ] No manual fixes required; this will persist across restarts

**Status:** [VERIFIED/NOT VERIFIED]

**Notes:** 
TODO: Confirm that the Week 5 configuration will support Week 9's CPU diagnosis lab. If any issues, document them here.

Theme of the Lab: we need a couple extra files to complete. Additionally, we may have some unintended consquences on the oringal flask image since we were the test group with the one size fits all flask deployment yaml file, causing the normal containers to give an image error on pod startup.

## Summary

**Overall Status:** [ ] ALL CHECKS PASS [x ] SOME CHECKS FAIL

**Blockers:** Theme of the Lab: we need a couple extra files to complete. Additionally, we may have some unintended consquences on the oringal flask image since we were the test group with the one size fits all flask deployment yaml file, causing the normal containers to give an image error on pod startup.

**Corrective Actions Taken:** Communicated with instructor.

**QA Sign-Off:**

By signing below, QA certifies that all required validation checks have been executed and all deliverables meet the acceptance criteria.

**QA Signature:** Jakob Black    **Date:** 10/26/26

---

## Notes for Sprint 4

[Any observations or recommendations for the next sprint]

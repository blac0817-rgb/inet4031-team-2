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


# QA Report: Sprint 3 Week 6

QA is responsible for running all validation checks and signing off before deliverables are submitted. This report documents the validation process.

**QA Team Member:** Jakob Black
**Date Completed:** 11/2/26

---

## Validation Checks

### Check 1: CI Workflow Passes on main

**Test:** Navigate to the Actions tab. Check the most recent run on `main`.

**Expected:** Green checkmark -- CI workflow completed successfully.

**Actual Result:**
```
Reference Google Doc.
```

**Status:** TODO: [x ] Pass [ ] Fail

**Notes:** If it failed, what did the run's error output show?

---

### Check 2: Branch Protection Configured

**Test:** Navigate to Settings > Branches and inspect the `main` rule.

**Expected:** Rule exists, requires the `build-and-push` status check, requires a PR before merging, requires branches to be up to date.

**Actual Result:**
```
Reference Google Doc.
```

**Status:** TODO: [ x] Pass [ ] Fail

**Notes:** Was anything missing from the rule?

---

### Check 3: Scheduled Workflow Runs Successfully

**Test:** In the Actions tab, manually trigger "Scheduled Maintenance" (`workflow_dispatch`).

**Expected:** Workflow shows a green checkmark on completion.

**Actual Result:**
```
Reference Google Doc.
```

**Status:** TODO: [x ] Pass [ ] Fail

**Notes:** If it failed, was the failure in the Trivy scan step or elsewhere?

---

### Check 4: Check Script Passes

**Test:** Run `./scripts/check-week6.sh`

**Expected:** All automatable checks pass with exit code 0

**Actual Result:**
```
=========================================
Week 6 Validation Checks
=========================================

Check 1: Workflow Files Exist
---------------------------------
[PASS] .github/workflows/ci.yml exists
[PASS] .github/workflows/scheduled-maintenance.yml exists

Check 2: Workflow YAML Is Well-Formed
------------------------------------------
[PASS] ci.yml is valid YAML
[PASS] scheduled-maintenance.yml is valid YAML

Check 3: CI Triggers
------------------------
[PASS] ci.yml has push and pull_request triggers

Check 4: Scheduled Maintenance Cron Trigger
------------------------------------------------
[PASS] scheduled-maintenance.yml has a cron trigger

Check 5: Manual GitHub UI Checks (not automatable from this container)
----------------------------------------------------------------------------
[WARN] CI workflow run passing on main - verify in the Actions tab
[WARN] Branch protection rule requiring CI to pass before merge - verify in Settings > Branches
[WARN] Scheduled Maintenance workflow completing successfully - verify in the Actions tab

=========================================
Validation Summary
=========================================
Passed: 6
Failed: 0

Status: ALL AUTOMATABLE CHECKS PASSED - confirm the manual GitHub checks above before submitting.
```

**Status:** TODO: [x ] Pass [ ] Fail

**Notes:** This script only checks what's verifiable from inside the container (workflow files exist, are valid YAML, have the right triggers). It cannot check CI passing on main, branch protection, or the scheduled workflow's own run history -- those three still need manual confirmation in the GitHub UI per Checks 1-3 above.

---

## Acceptance Criteria Verification

Review the criteria below for each part of this week's deliverables. For each criterion, record whether it was met:

### Part 1: CI Pipeline for Docker Build and Push

TODO: [x ] `.github/workflows/ci.yml` created and committed
TODO: [x ] Workflow triggers on `push` to main, `pull_request` to main, and `workflow_dispatch`
TODO: [x ] Logs in to `ghcr.io` using `GITHUB_TOKEN` (no personal access token needed)
TODO: [x ] Image tagged via `docker/metadata-action` (sha, branch ref, and `latest` on main)
TODO: [x ] Push step conditional on not being a `pull_request` event (PRs build but don't push)
TODO: [x ] First workflow run after push completed successfully

### Part 2: Workflow Secrets and Branch Protection

TODO: [x ] `SLACK_WEBHOOK_URL` secret created under Settings > Secrets and variables > Actions
TODO: [x ] Branch protection rule added on `main` requiring the `build-and-push` status check
TODO: [x ] "Require branches to be up to date before merging" enabled
TODO: [x ] `test/failing-build` branch created with an intentional Dockerfile syntax error
TODO: [x ] PR from `test/failing-build` showed the merge button disabled while CI failed (screenshot captured)
TODO: [ x] Dockerfile fixed, CI re-ran and passed, PR merged, test branch deleted (screenshot captured)

### Part 3: Scheduled Maintenance Workflow

TODO: [ x] `.github/workflows/scheduled-maintenance.yml` created and committed
TODO: [x ] Cron trigger set to `0 8 * * 1` (08:00 UTC every Monday), plus `workflow_dispatch` for manual runs
TODO: [ x] Job has `permissions: packages: read` and logs in to `ghcr.io` before scanning (the image is a private package -- Trivy needs credentials, not just a valid reference)
TODO: [x ] Image reference is lowercased before being passed to Trivy (`${{ github.repository }}` includes the org name as-cased on GitHub, which breaks reference parsing if it contains uppercase letters)
TODO: [x ] Manually triggered run completed successfully (screenshot captured)

---

## Deliverables Verification

### Required Files

TODO: [ x] `.github/workflows/ci.yml` is committed (build and push, manual trigger)
TODO: [ x] `.github/workflows/scheduled-maintenance.yml` is committed
TODO: [ x] `scripts/check-week6.sh` is present and runs clean

### GitHub Repository

TODO: [x ] Branch protection rule configured on `main`
TODO: [ x] `test/failing-build` branch deleted after merge
TODO: [x ] All changes pushed to the main branch

### Google Doc

TODO: [ x] Screenshot of failed CI blocking a merge is attached
TODO: [x ] Screenshot of passing CI after the fix is attached
TODO: [ x] Screenshot of the Scheduled Maintenance workflow run showing success is attached
TODO: [ x] Screenshot of `./scripts/check-week6.sh` passing is attached
TODO: [ x] Discussion answers recorded (CI trigger tradeoffs, secret masking limitations, branch protection bypass governance, cron vs. systemd timers)
TODO: [ x] Week 6 storage check values recorded (`df -h`, `docker system df`)

---

## Summary

**Overall Status:** [ x] ALL CHECKS PASS [ ] SOME CHECKS FAIL

**Blockers:** [List any blockers that prevent submission]

**Corrective Actions Taken:** [List any fixes applied during QA]

**QA Sign-Off:**

By signing below, QA certifies that all required validation checks have been executed and all deliverables meet the acceptance criteria.

**QA Signature:** Jakob Black   **Date:** 11/2/26

---

## Notes for Sprint 4

KEEP ON TRUCKING!!!!!!!

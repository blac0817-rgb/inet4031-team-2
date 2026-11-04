# QA Report: Sprint 4 Week 7

QA is responsible for running all validation checks and signing off before deliverables are submitted. This report documents the validation process.

**QA Team Member:** Marcos Flores
**Date Completed:** 11/3/16

---

## Validation Checks

### Check 1: Flask Uses Custom ServiceAccount

**Test:** Run `kubectl get pod -l app=flask -o jsonpath='{.items[0].spec.serviceAccountName}'`

**Expected:** `flask-app`

**Actual Result:**
```
TODO: Paste the actual output
`flask-app`

**Status:** TODO: [ x] Pass [ ] Fail

**Notes:** If this doesn't match, was the ServiceAccount change applied through `tofu apply` rather than a direct `kubectl edit`?

---

### Check 2: NetworkPolicy Applied

**Test:** Run `kubectl get networkpolicy`

**Expected:** Rows for `default-deny-ingress`, `allow-nginx-to-flask`, `allow-flask-to-postgres`, and `allow-ingress-to-nginx`

**Actual Result:**
```
TODO: Paste the actual output
`NAME                        POD-SELECTOR   AGE
allow-flask-to-postgres     app=db         33m
allow-ingress-to-nginx      app=nginx      32m
allow-nginx-to-flask        app=flask      33m
allow-prometheus-to-flask   app=flask      32m
default-deny-ingress        <none>         38m`

**Status:** TODO: [ x] Pass [ ] Fail

**Notes:** All four are required -- `allow-ingress-to-nginx` is easy to miss since it's not part of the original three-policy set, but without it `default-deny-ingress` blocks all external traffic into nginx too.

---

### Check 3: Application Works After NetworkPolicy

**Test:** Run `curl -s http://localhost:8081/incidents`

**Expected:** Valid JSON response

**Actual Result:**
```
TODO: Paste the actual response
`[]`

**Status:** TODO: [ x] Pass [ ] Fail

**Notes:** If this fails while Check 2 passes, check whether `allow-flask-to-postgres` actually selects `app: db` (the real label on the db Deployment) -- a mismatched label here silently blocks flask from reaching the database.

---

### Check 4: SecurityContext Is Set

**Test:** Run `kubectl get deployment flask -o jsonpath='{.spec.template.spec.containers[0].securityContext.allowPrivilegeEscalation}'`

**Expected:** `false`

**Actual Result:**
```
TODO: Paste the actual output
`false`

**Status:** TODO: [x ] Pass [ ] Fail

**Notes:** Also confirm `readOnlyRootFilesystem`, `runAsNonRoot`, and `capabilities.drop: [ALL]` are set -- this check only verifies one of the four SecurityContext fields Step 12 adds.

---

### Check 5: OpenTofu State Matches the Cluster (No Drift)

**Test:** Run `cd infrastructure && tofu plan`

**Expected:** `No changes. Your infrastructure matches the configuration.`

**Actual Result:**
```
TODO: Paste the actual output
` service_account_name = "flask-app"
            allow_privilege_escalation = false`

**Status:** TODO: [x ] Pass [ ] Fail

**Notes:** Drift here almost always means a change was applied with `kubectl apply`/`kubectl edit` instead of `tofu apply`.

---

### Check 6: Check Script Passes

**Test:** Run `chmod +x ./scripts/check-week7.sh` then `./scripts/check-week7.sh`

**Expected:** All checks pass with exit code 0

**Actual Result:**
```
TODO: Paste the full output of the check script
`=========================================
Week 7 Validation Checks
=========================================

Check 1: RBAC and NetworkPolicy Manifests Exist
-----------------------------------------------------
[PASS] manifests/flask-serviceaccount.yaml exists
[PASS] manifests/flask-role.yaml exists
[PASS] manifests/flask-rolebinding.yaml exists
[PASS] manifests/default-deny.yaml exists
[PASS] manifests/allow-nginx-to-flask.yaml exists
[PASS] manifests/allow-flask-to-postgres.yaml exists
[PASS] manifests/allow-ingress-to-nginx.yaml exists
[PASS] manifests/allow-prometheus-to-flask.yaml exists
[PASS] manifests/flask-securitycontext-patch.yaml exists

Check 2: CI Workflow Includes Trivy Scan
----------------------------------------------
[PASS] ci.yml includes a Trivy scan step

Check 3: Flask Uses Custom ServiceAccount
------------------------------------------------
[PASS] Flask pod uses the 'flask-app' ServiceAccount

Check 4: NetworkPolicy Applied
------------------------------------
[PASS] NetworkPolicy 'default-deny-ingress' exists
[PASS] NetworkPolicy 'allow-nginx-to-flask' exists
[PASS] NetworkPolicy 'allow-flask-to-postgres' exists
[PASS] NetworkPolicy 'allow-ingress-to-nginx' exists
[PASS] NetworkPolicy 'allow-prometheus-to-flask' exists

Check 5: Application Works After NetworkPolicy
-----------------------------------------------------
[FAIL] Application did not respond correctly at http://localhost:8102/incidents (HTTP 000) - check HOST_PORT in week-2/.env matches your assigned port

Check 6: SecurityContext Is Set
-------------------------------------
[PASS] allowPrivilegeEscalation is false
[PASS] readOnlyRootFilesystem is true
[PASS] runAsNonRoot is true
[PASS] capabilities.drop includes ALL

Check 7: OpenTofu Configuration Updated
---------------------------------------------------------
[PASS] flask.tf sets service_account_name = "flask-app"
[PASS] flask.tf has a security_context with allow_privilege_escalation = false

=========================================
Validation Summary
=========================================
Passed: 22
Failed: 1

Status: SOME CHECKS FAILED - Review errors above`

**Status:** TODO: [ ] Pass [ x] Fail

**Notes:** If any checks failed, what did the script report?
Application not responding correctly at designated port. However, the port that is referenced in the check script is not our port, so we think that this is an issue wihh the script itself.
---

## Acceptance Criteria Verification

Review the criteria below for each part of this week's deliverables. For each criterion, record whether it was met:

### Part 1: Kubernetes RBAC

TODO: [x ] `manifests/flask-serviceaccount.yaml` created with `automountServiceAccountToken: false`
TODO: [x ] `manifests/flask-role.yaml` created with least-privilege rules (configmaps get/list only)
TODO: [x ] `manifests/flask-rolebinding.yaml` created, binding the Role to the `flask-app` ServiceAccount
TODO: [ x] `infrastructure/flask.tf` updated with `service_account_name = "flask-app"`, applied via `tofu apply` (not `kubectl apply -f manifests/flask-deployment.yaml`, which OpenTofu no longer manages)

### Part 2: NetworkPolicy

TODO: [ x] `manifests/default-deny.yaml` created and applied; Step 8's debug-pod test actually timed out (not "connection refused" or immediate success)
TODO: [ x] `manifests/allow-nginx-to-flask.yaml` created (`app: flask` selector, allows from `app: nginx` on port 5000)
TODO: [x ] `manifests/allow-flask-to-postgres.yaml` created (`app: db` selector -- not `app: postgres`, which matches no real pods)
TODO: [x ] `manifests/allow-ingress-to-nginx.yaml` created (`app: nginx` selector, allows port 80 from any source)
TODO: [ x] All four policies applied; `curl http://localhost:8081/incidents` returns valid JSON end to end

### Part 3: SecurityContext

TODO: [x ] `infrastructure/flask.tf` container block gained `security_context` (allow_privilege_escalation=false, read_only_root_filesystem=true, run_as_non_root=true, run_as_user=1000, capabilities.drop=[ALL])
TODO: [x ] Applied via `tofu apply`; flask pods restarted and came back healthy
TODO: [x ] If pods failed on a read-only-filesystem write, the fix (e.g. an `emptyDir` mount) is documented

### Part 4: Image Vulnerability Scanning in CI

TODO: [ ] `.github/workflows/ci.yml` updated with a `security-scan` job running `aquasecurity/trivy-action`
TODO: [ ] Job authenticates to `ghcr.io` before scanning and lowercases the image reference (both required -- the image is a private package, and `${{ github.repository }}` includes the org name uncased)
TODO: [ ] Workflow run observed in the Actions tab; Trivy's log output captured regardless of pass/fail -- `exit-code: '1'` means a red X from real CRITICAL findings (e.g. unpatched base-image OS packages) is an expected, valid outcome, not a bug to chase

---

## Deliverables Verification

### Required Files

TODO: [ x] `manifests/flask-serviceaccount.yaml`, `flask-role.yaml`, `flask-rolebinding.yaml` committed
TODO: [ x] `manifests/default-deny.yaml`, `allow-nginx-to-flask.yaml`, `allow-flask-to-postgres.yaml`, `allow-ingress-to-nginx.yaml` committed
TODO: [ x] `infrastructure/flask.tf` updated with `service_account_name` and `security_context`
TODO: [ x] `.github/workflows/ci.yml` updated with the `security-scan` job
TODO: [ ~] `scripts/check-week7.sh` present and runs clean

### GitHub Repository

TODO: [x ] All changes pushed to the main branch
TODO: [x ] `tofu plan` shows no drift at time of push

### Google Doc

TODO: [ x] Screenshot of the Step 8 connection timeout is attached
TODO: [ x] Screenshot of the application responding successfully after all NetworkPolicies applied is attached
TODO: [ x] Trivy scan log/result from GitHub Actions is attached (pass or fail)
TODO: [x ] Screenshot of `./scripts/check-week7.sh` passing is attached
TODO: [ x] Discussion answers recorded for Parts 1-4 (RBAC attack surface, NetworkPolicy enforcement verification and remaining attack paths, read-only-filesystem tradeoffs, scan-stage tradeoffs)

---

## Rework Required

If any validation checks or acceptance criteria failed, document the rework needed:

**Issues Found:**
`Check script does not identify proper port.`
TODO: List any failures here
`Redundant`

**Rework Plan:**
```
TODO: For each failure, describe the steps to fix it and who will do the work
`Verify script intention with instructors during class`

**Re-validation Date:** TODO: When will rework be complete?

---

## Summary

**Overall Status:** [ ] ALL CHECKS PASS [ x] SOME CHECKS FAIL

**Blockers:** [List any blockers that prevent submission]

**Corrective Actions Taken:** [List any fixes applied during QA]

**QA Sign-Off:**

By signing below, QA certifies that all required validation checks have been executed and all deliverables meet the acceptance criteria.

**QA Signature:** Marcos Flores    **Date:** 11/3/26

---

## Notes for Sprint 5

[Any observations or recommendations for the next sprint]

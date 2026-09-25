# QA Report: Sprint 1 Week 1

QA is responsible for running all validation checks and signing off before deliverables are submitted. This report documents the validation process.

**QA Team Member:** Sumaya
**Date Completed:** 09/24/2026

---

## Validation Checks

### Check 1: All Team Members Can Access the Container

**Status:** [x] PASS [ ] FAIL

**Evidence:**
```
[blac0817@caps-inet4031-dev-app-02 ~]$ whoami
blac0817
[blac0817@caps-inet4031-dev-app-02 ~]$ hostname
caps-inet4031-dev-app-02.oit.umn.edu
[blac0817@caps-inet4031-dev-app-02 ~]$ 

[diego@caps-inet4031-dev-app-02 ~]$ whoami
diego
[diego@caps-inet4031-dev-app-02 ~]$ hostname
caps-inet4031-dev-app-02.oit.umn.edu
[diego@caps-inet4031-dev-app-02 ~]$

[flore959@caps-inet4031-dev-app-02 ~]$ whoami
flore959
[flore959@caps-inet4031-dev-app-02 ~]$ hostname
caps-inet4031-dev-app-02.oit.umn.edu
[flore959@caps-inet4031-dev-app-02 ~]$

[ahme0745@caps-inet4031-dev-app-02 ~]$ whoami
ahme0745
[ahme0745@caps-inet4031-dev-app-02 ~]$ hostname
caps-inet4031-dev-app-02.oit.umn.edu
[ahme0745@caps-inet4031-dev-app-02 ~]$
	
[her00278@caps-inet4031-dev-app-02 inet4031-team-2]$ whoami
her00278
[her00278@caps-inet4031-dev-app-02 inet4031-team-2]$ hostname
caps-inet4031-dev-app-02.oit.umn.edu
[her00278@caps-inet4031-dev-app-02 inet4031-team-2]$

[xion2368@caps-inet4031-dev-app-02 ~]$ whoami
xion2368
[xion2368@caps-inet4031-dev-app-02 ~]$ hostname
caps-inet4031-dev-app-02.oit.umn.edu
[xion2368@caps-inet4031-dev-app-02 ~]$

```

**Notes:**
[Any issues encountered or observations]

**Sign-off:** [x] QA approves this check

---

### Check 2: Repository Structure Is Correct

**Status:** [x] PASS [ ] FAIL

**Evidence:**
```
[ahme0745@caps-inet4031-dev-app-02 inet4031-team-2]$ ls -1
ansible
docs
README.md
scripts
team-charter.md
week-1
week-2
week-3
week-4
week-5
week-6
week-7
week-8
week-9
[ahme0745@caps-inet4031-dev-app-02 inet4031-team-2]$ 
```

**Expected directories present:**
- [x] README.md
- [x] ansible
- [x] scripts
- [x] team-charter.md
- [x] week-1 to week-9

**Notes:**
[Any missing directories or issues]

**Sign-off:** [x] QA approves this check

---

### Check 3: Google Doc Is Linked and Shared

**Status:** [x] PASS [ ] FAIL

**Evidence:**
- [x] Google Doc URL present in README.md
- [x] URL is accessible at: [ https://docs.google.com/document/d/1cKZ5M6EO2Cq8WVcOM9jIa4A0AK0kp6CmjXptyxA5kSg/edit?usp=sharing]
- [x] Doc is readable by University of Minnesota users
- [x] Sprint 1 Reflections section contains Part 2 answers
- [x] Sprint 1 Reflections section contains Part 3 answers
- [x] Week 1 Storage Baseline section contains required outputs

**Notes:**
[Any access or content issues]

**Sign-off:** [x] QA approves this check

---

### Check 4: Check Script Passes

**Status:** [x] PASS [ ] FAIL

**Command Run:**
```bash
./scripts/check-week1.sh
```

**Output:**
```
==========================================
Week 1 Validation Check
==========================================

Checking repository structure...
[PASS] File exists: README.md
[PASS] File exists: team-charter.md
[PASS] File exists: ansible/site.yml
[PASS] File exists: ansible/inventory
[PASS] File exists: .gitignore
[PASS] Directory exists: ansible
[PASS] Directory exists: scripts
[PASS] Directory exists: week-1
[PASS] Directory exists: week-2
[PASS] Directory exists: week-3
[PASS] Directory exists: week-4
[PASS] Directory exists: week-5
[PASS] Directory exists: week-6
[PASS] Directory exists: week-7
[PASS] Directory exists: week-8
[PASS] Directory exists: week-9
[PASS] Directory exists: docs

Checking README.md content...
[PASS] README.md contains team name field
[PASS] README.md contains Google Doc link section

Checking team-charter.md content...
[PASS] team-charter.md contains section: Team Name
[PASS] team-charter.md contains section: Team Number
[PASS] team-charter.md contains section: Full Roster
[PASS] team-charter.md contains section: 7-Sprint Rotation Schedule
[PASS] team-charter.md contains section: Operating Agreements

Checking Ansible configuration...
[PASS] ansible/inventory configured for localhost
[PASS] ansible/site.yml contains baseline play
[PASS] ansible/site.yml contains dnf module usage
[PASS] Ansible is installed

Checking documentation files...
[PASS] Documentation file exists: docs/sprint-1-retrospective.md
[PASS] Documentation file exists: docs/qa-report-1.md

==========================================
Summary
==========================================
Passed: 30
Failed: 0

All checks passed!
```

**Notes:**
[Any failures or warnings from the script]

**Sign-off:** [x] QA approves this check

---

## Summary

**Overall Status:** [x] ALL CHECKS PASS [ ] SOME CHECKS FAIL

**Blockers:** [List any blockers that prevent submission]

**Corrective Actions Taken:** [List any fixes applied during QA]

**QA Sign-Off:**

By signing below, QA certifies that all required validation checks have been executed and all deliverables meet the acceptance criteria.

**QA Signature:** Sumaya Ahmed   **Date:** 09/24/2026

---

## Notes for Sprint 2

[Any observations or recommendations for the next sprint]

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

**Blockers:** [None]

**Corrective Actions Taken:** [None]

**QA Sign-Off:**

By signing below, QA certifies that all required validation checks have been executed and all deliverables meet the acceptance criteria.

**QA Signature:** Sumaya Ahmed   **Date:** 09/24/2026

---

# QA Report: Sprint 1 Week 2

QA is responsible for running all validation checks and signing off before deliverables are submitted. This report documents the validation process.

**QA Team Member:** [Sumaya Ahmed]
**Date Completed:** [10/01/2026]

---

## Validation Checks

### Check 1: All Three Services Are Running and Two Of Them Show Healthy

**Test:** Run `docker compose ps` from the `week-2/` directory

**Expected:** Three rows, each with "running" in the Status column

**Actual Result:**
```
[ahme0745@caps-inet4031-dev-app-02 week-2]$ docker compose ps
WARN[0000] The "POSTGRES_PASSWORD" variable is not set. Defaulting to a blank string. 
WARN[0000] The "POSTGRES_DB" variable is not set. Defaulting to a blank string. 
WARN[0000] The "POSTGRES_USER" variable is not set. Defaulting to a blank string. 
WARN[0000] The "POSTGRES_USER" variable is not set. Defaulting to a blank string. 
WARN[0000] The "POSTGRES_USER" variable is not set. Defaulting to a blank string. 
WARN[0000] The "POSTGRES_PASSWORD" variable is not set. Defaulting to a blank string. 
WARN[0000] The "POSTGRES_DB" variable is not set. Defaulting to a blank string. 
WARN[0000] /home/ahme0745/inet4031-team-2/week-2/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion 
NAME             IMAGE                COMMAND                  SERVICE   CREATED              STATUS                        PORTS
week-2-db-1      postgres:15-alpine   "docker-entrypoint.s…"   db        About a minute ago   Up About a minute (healthy)   5432/tcp
week-2-flask-1   week-2-flask         "python3 app.py"         flask     About a minute ago   Up 49 seconds (healthy)       5000/tcp
week-2-nginx-1   nginx:alpine         "/docker-entrypoint.…"   nginx     About a minute ago   Up 38 seconds                 0.0.0.0:8085->80/tcp, [::]:8085->80/tcp
[ahme0745@caps-inet4031-dev-app-02 week-2]$ 

```

**Status:** TODO: [x] Pass [ ] Fail

**Notes:** 

All three services are running. PostgreSQL and Flask report healthy status. Docker Compose displayed warnings about unset PostgreSQL environment variables and the obsolete version attribute, but the services started successfully and met the validation requirements.

### Check 2: Nginx Is Reachable on the Mapped Port

**Test:** Run `curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/health`

**Expected:** HTTP 200

**Actual Result:** 200[ahme0745@caps-inet4031-dev-app-02 week-2]$ 

**Status:** TODO: [x] Pass [ ] Fail

**Notes:** If the request failed, what error message did you see?

---

### Check 3: Data Persists Across Container Restart

**Test:** Create a test incident, restart the PostgreSQL container, retrieve all incidents

**Steps Performed:**
```
curl -X POST http://localhost:8085/incidents \
  -H "Content-Type: application/json" \
  -d '{"title":"Persistence check","status":"open","description":"this should survive a restart"}'
docker compose restart db
curl http://localhost:8085/incidents
```

**Actual Result:**
```
Container week-2-db-1 Restarting

[{"created_at":"2026-10-02T02:45:46.903713+00:00","description":"this should survive a restart","id":2,"status":"open","title":"Persistence check"},{"created_at":"2026-10-02T02:45:25.611241+00:00","description":"this should survive a restart","id":1,"status":"open","title":"Persistence check"}]
```

**Status:** TODO: [x] Pass [ ] Fail

**Notes:** Was data present after the restart? Was anything lost?

Data was still present after the PostgreSQL container was restarted. The Persistence check incidents were successfully retrieved after the restart, so no data was lost.

### Check 4: Check Script Passes

**Test:** Run `chmod +x scripts/check-week2.sh` then `./scripts/check-week2.sh`

**Expected:** All checks pass with exit code 0

**Actual Result:**
```
[ahme0745@caps-inet4031-dev-app-02 week-2]$ chmod +x ../scripts/check-week2.sh
[ahme0745@caps-inet4031-dev-app-02 week-2]$ ../scripts/check-week2.sh
=========================================
Week 2 Validation Checks
=========================================


Check 1: Required Week 2 Files
-------------------------------
[PASS] week-2/docker-compose.yml exists
[PASS] week-2/.env.example exists
[PASS] week-2/nginx.conf exists
[PASS] week-2/app/ directory exists

Check 2: .env Is Git-Ignored
------------------------------
[PASS] week-2/.env is excluded by .gitignore

Check 3: Ansible app-stack Role
---------------------------------
[PASS] ansible/roles/app-stack/tasks/main.yml exists
[PASS] ansible/site.yml includes the app-stack role

Check 4: Docker Compose Stack Health
--------------------------------------
[PASS] db and flask report healthy (2 healthy; nginx has no healthcheck defined)

Check 5: Application Health Check
-----------------------------------
[WARN] Nginx responded on http://localhost:8080/health but with HTTP 000000 (expected 200)

=========================================
Validation Summary
=========================================
Passed: 8
Failed: 0
Warnings: (see above)

Status: ALL CHECKS PASSED
[ahme0745@caps-inet4031-dev-app-02 week-2]$ 
```

**Status:** TODO: [x] Pass [ ] Fail

**Notes:** If any checks failed, what did the script report?

---

## Acceptance Criteria Verification

Review the criteria below for each part of this week's deliverables. For each criterion, record whether it was met:

### Part 1: Service Definition

TODO: [ ] All three services start in correct order
TODO: [ ] Health checks work as specified

### Part 2: Networking and Persistence

TODO: [ ] Data persists across `docker compose restart`
TODO: [ ] Data is lost after `docker compose down -v`

### Part 3: Environment

TODO: [ ] `.env` is in `.gitignore`
TODO: [ ] `.env.example` documents all variablest

---

## Deliverables Verification

### Required Files

TODO: [ ] `week-2/docker-compose.yml` is committed
TODO: [ ] `week-2/.env.example` is committed
TODO: [ ] `week-2/nginx.conf` is committed
TODO: [ ] `week-2/README.md` is committed
TODO: [ ] `ansible/site.yml` includes app-stack role play
TODO: [ ] `ansible/roles/app-stack/tasks/main.yml` is committed
TODO: [ ] `.gitignore` excludes `week-2/.env`

### GitHub Repository

TODO: [ ] All changes are pushed to the main branch
TODO: [ ] GitHub Project board shows all tasks completed
TODO: [ ] PR descriptions explain implementation decisions

### Google Doc

TODO: [ ] Sprint 1 Week 2 reflection answers are recorded
TODO: [ ] Week 2 storage check values are recorded
TODO: [ ] Required screenshots are attached

---

## Summary

**Overall Status:** [ ] ALL CHECKS PASS [ ] SOME CHECKS FAIL

**Blockers:** [List any blockers that prevent submission]

**Corrective Actions Taken:** [List any fixes applied during QA]

**QA Sign-Off:**

By signing below, QA certifies that all required validation checks have been executed and all deliverables meet the acceptance criteria.

**QA Signature:** _________________    **Date:** __________

---

## Notes for Sprint 2

[Any observations or recommendations for the next sprint]

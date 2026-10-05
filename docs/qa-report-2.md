# QA Report: Sprint 2 Week 3
QA is responsible for running all validation checks and signing off before deliverables are submitted. This report documents the validation process.

**QA Team Member: Diego 
**Date Completed: 10/04/2026
----

## Validation Checks
###Check 1: k3d Cluster Is Running
**Test: Run k3d cluster list

**Expected: ** One row showing myapp with SERVERS 1/1 and AGENTS 2/2 (all nodes up)

***Actual Result: ***

[diego@caps-inet4031-dev-app-02 scripts]$ k3d cluster list
NAME    SERVERS   AGENTS   LOADBALANCER
myapp   1/1       2/2      true

**Status:** [X ] Pass [ ] Fail

**Notes: **If any nodes aren't up, what did kubectl describe node <node-name> reveal?

### Check 2: All Pods Running
**Test:** Run kubectl get pods

**Expected:** All pods in Running state with 1/1 in READY

**Actual Result:**
[diego@caps-inet4031-dev-app-02 scripts]$ kubectl get pods

NAME                     READY   STATUS    RESTARTS   AGE
db-6b4545486-cdq59       1/1     Running   0          23m
flask-86995cc5d9-jwqqc   1/1     Running   0          23m
nginx-6847f4545-qj75s    1/1     Running   0          23m


**Status** : [X ] Pass [ ] Fail

**Notes: ** If any pod is not Running (Pending, CrashLoopBackOff, ErrImagePull), what did kubectl describe pod <pod-name> or kubectl logs <pod-name> reveal?
-------

### Check 3: Credentials Are in a Secret, Not a Deployment
**Test:** Run kubectl get deployment flask -o jsonpath='{.spec.template.spec.containers[0].env}' and kubectl get deployment db -o jsonpath='{.spec.template.spec.containers[0].env}', then kubectl get secret flask-credentials and kubectl get secret db-credentials

**Expected:** Both deployment env outputs are empty (no output) or show only non-credential variables; both Secrets exist

** Actual Result: **

[diego@caps-inet4031-dev-app-02 scripts]$ kubectl get deployment flask -o jsonpath='{.spec.template.spec.containers[0].env}'
[diego@caps-inet4031-dev-app-02 scripts]$ kubectl get deployment db -o jsonpath='{.spec.template.spec.containers[0].env}'
[diego@caps-inet4031-dev-app-02 scripts]$ kubectl get secret flask-credentials
NAME                TYPE     DATA   AGE
flask-credentials   Opaque   4      113m
[diego@caps-inet4031-dev-app-02 scripts]$ kubectl get secret db-credentials
NAME             TYPE     DATA   AGE
db-credentials   Opaque   4      140m
[diego@caps-inet4031-dev-app-02 scripts]$ 

** Status: ** [X ] Pass [ ] Fail

** Notes: ** If credentials are still visible in either Deployment, which one and what variable?

### Check 4: RollingUpdate Strategy Applied
** Test: ** Run kubectl get deployment db -o jsonpath='{.spec.strategy.type}'

** Expected: ** RollingUpdate

** Actual Result: ** Record the strategy type returned
[diego@caps-inet4031-dev-app-02 scripts]$ kubectl get deployment db -o jsonpath='{.spec.strategy.type}'
RollingUpdate[diego@caps-inet4031-dev-app-02 scripts]$ 


** Status: ** [ X] Pass [ ] Fail

** Notes:  ** This checks the db Deployment, not flask — kompose only generates a Recreate strategy for services with a volume mount, and only db has one.

--------

### Check 5: Check Script Passes
** Test: ** Run chmod +x scripts/check-week3.sh then ./scripts/check-week3.sh

** Expected: ** All checks pass with exit code 0

** Actual Result: **

=========================================
Week 3 Validation Checks
=========================================


Check 1: k3d Cluster Is Running
---------------------------------
[PASS] k3d is installed
[PASS] k3d cluster 'myapp' exists
[PASS] k3d cluster has exactly 3 Ready nodes

Check 2: All Pods Running
-------------------------
[PASS] All pods are in Running state
[PASS] 3 pods report 1/1 Ready

Check 3: Credentials in Secrets, Not Deployments
------------------------------------------------
[PASS] Secret 'flask-credentials' exists
[PASS] Secret 'db-credentials' exists
[PASS] Flask Deployment does not have inline env vars (using envFrom/secretRef)
[PASS] Postgres Deployment does not have inline env vars (using envFrom/secretRef)

Check 4: RollingUpdate Strategy Applied
----------------------------------------
[PASS] Postgres Deployment uses RollingUpdate strategy
[PASS] Postgres Deployment has RollingUpdate parameters (maxSurge: 1, maxUnavailable: 0)

Check 5: Application Health Check
-----------------------------------
[WARN] Application not responding to health check at http://localhost:8102/health (HTTP 000000) - may still be starting, or HOST_PORT in week-2/.env doesn't match your assigned port

Check 6: Ansible k3d-setup Role
--------------------------------
[PASS] ansible/roles/k3d-setup/tasks/main.yml exists
[PASS] ansible/site.yml includes k3d-setup role

Check 7: Manifests Directory
-----------------------------
[PASS] manifests/ directory exists
[PASS] Found 10 YAML manifest files
[PASS] Flask Secret manifest found (flask-secret.yaml)
[PASS] Postgres Secret manifest found (db-secret.yaml)
[PASS] No io.kompose.service labels remain in manifests/
[PASS] flask-deployment.yaml image reference has been fixed
[PASS] nginx-service.yaml is exposed as a LoadBalancer

=========================================
Validation Summary
=========================================
Passed: 20
Failed: 0
Warnings: (see above)

Status: ALL CHECKS PASSED 

** Status: ** [X ] Pass [ ] Fail

** Notes: ** If any checks failed, what did the script report?
--------  

##Acceptance Criteria Verification
Review the criteria below for each part of this week's deliverables. For each criterion, record whether it was met:

### Part 1: k3d Cluster Creation
[X ] k3d cluster myapp created with 1 server and 2 agent nodes: [ X] Traefik disabled at cluster creation (--k3s-arg "--disable=traefik@server:0") [X ] kubectl get nodes shows all three nodes Ready

### Part 2: Docker Compose to Kubernetes Manifests
[x ] kompose convert generated a Deployment and Service for db, flask, and nginx, plus a PersistentVolumeClaim and ConfigMap: [X ] All io.kompose.service labels replaced with app: labels: [X ] Plaintext credentials moved to flask-secret.yaml and db-secret.yaml; Deployments use envFrom/secretRef [X ] db-deployment.yaml strategy changed from Recreate to RollingUpdate [X ] flask-deployment.yaml image reference fixed to the locally built image (not the kompose placeholder) and imported into the cluster with k3d image import [X ] nginx-service.yaml changed from ClusterIP to LoadBalancer [X ] db-deployment.yaml liveness probe command split into separate array items

### Part 3: Deploy and Verify
[ X] Secrets applied before other manifests [X ] All pods reach Running / 1/1 Ready [X ] Application responds at http://localhost:8081/health [X ] Scaling flask to 2 replicas demonstrates a rolling update (new pod comes up before old one terminates)

### Part 4: Ansible Update
 [X ] ansible/roles/k3d-setup/tasks/main.yml installs k3d and creates the cluster idempotently [X ] ansible/site.yml includes the k3d-setup play [X ] app-stack play commented out in ansible/site.yml (Kubernetes now supersedes Docker Compose) [X ] Playbook runs clean end to end

## Deliverables Verification
Required Files
 [X ] manifests/ directory is committed with all Kubernetes manifests (Deployments, Services, Secrets, PVC, ConfigMap) [X ] manifests/flask-secret.yaml and manifests/db-secret.yaml are committed [X ] ansible/site.yml includes the k3d-setup play (and has app-stack commented out) [X ] ansible/roles/k3d-setup/tasks/main.yml is committed: [X ] week-2/docker-compose.yml is committed with the ports: entries added for db and flask

### GitHub Repository
 [x ] All changes are pushed to the main branch [X ] GitHub Project board shows all Week 3 tasks completed

### Google Doc
 [X ] Sprint 1 close-out answers are recorded [X ] Sprint 2 kickoff environment state checkpoint is recorded: [X ] Week 3 discussion answers are recorded (k3d resource competition, kompose translation risks, RollingUpdate vs. Recreate, Secret encoding vs. encryption, PostgreSQL data durability) [X ] Required screenshots are attached: kompose output showing plaintext env vars and Recreate strategy (before fixes), kubectl get pods showing all pods Running, rolling update in progress (two Flask pods visible), ./scripts/check-week3.sh passing [X ] Week 3 storage check values are recorded

-------

## Summary
**Overall Status:** [X ] ALL CHECKS PASS [ ] SOME CHECKS FAIL

*Blockers:** NA

**Corrective Actions Taken:** NA

-----

**QA Sign-Off: **Diego Lahoud 

By signing below, QA certifies that all required validation checks have been executed and all deliverables meet the acceptance criteria.

** QA Signature:** ___Diego Lahoud______________ ** Date:** ___10/04/2026_______


# Team Charter - Sprint 1
## Team Identity
**Team Name:** Group 2
**Team Number:** 2
**Full Roster:**
| Name | Role (Sprint 1) |
|------|-----------------|
|Sumaya |QA |
|Marcos | System Admin|
|Jakob |Scrum Master |
|Diego |Developer |
|TY |Developer |
|Randeep |Developer |
|Tyler | Developer|
## Role One-Sentence Descriptions
Add one sentence describing each role after you assign them in Part 1:
- **Scrum Master:** Helps the team stay organized and makes sure sprint tasks are
moving forward.
- **System Admin:** Manages and maintains the teams technical tools as well as
makes sure systems are working properly.
- **QA:** Checks the team's work to make sure it works correctly and meets the
requirements.
- **Developer:** Works on implementing and completing the team's technical tasks.
## 7-Sprint Rotation Schedule
Every team member must hold Scrum Master, System Admin, and QA at least once across
the seven sprints. Fill in this table using what you jotted down in your Google
Docs:
```
Sprint 1: Scrum Master = Jakob, System Admin = Marcos, QA = Sumaya, Developers =
Diego/Ty/Tyler/Randeep
Sprint 2: Scrum Master = Marcos, System Admin = Jakob, QA = Diego, Developers =
Ty/Tyler/Sumaya/Randeep
Sprint 3: Scrum Master = Ty, System Admin = Tyler, QA = Jakob, Developers =
Randeep/Marcos/Sumaya/Diego
Sprint 4: Scrum Master = Diego, System Admin = Ty, QA = Marcos, Developers =
Jakob/Randeep/Tyler/Sumaya
Sprint 5: Scrum Master = Tyler, System Admin = Diego, QA = Randeep, Developers =
Jakob/Marcos/Ty/Sumaya
Sprint 6: Scrum Master = Sumaya, System Admin = Randeep, QA = Ty, Developers =
Jakob/Tyler/Diego/Sumaya
Sprint 7: Scrum Master = Randeep, System Admin = Sumaya, QA = Tyler, Developers =
Marcos/Ty/Jakob/Diego
```
## Three Team Operating Agreements
Document three decisions your team made about operating the shared container and
managing infrastructure changes:
1. **Response Time:** 8 Hours.
2. **Developers** 4 Developers every week.
3. **Lab Work** Spend as much time as possible during Thursdays, arrange time at end of thursday for next meeting.

## Communication Method
  - Google Chat

## Container Baseline:
Operating System: Red Hat Enterprise Linux 9.8 (Plow)
Disk Space: The root filesystem has 1.9 GB available. /var has 16 GB available, /var/lib has 6.5 GB available, and /home has 1.4 GB available.
Installed Tools: Docker, Git, Python 3, curl, and Ansible are all installed.
Docker Status: Docker Engine 29.8.1 is installed with Docker Buildx and Docker Compose. However, our user accounts are not members of the docker group, so docker info returns a permission-denied error. The Docker socket is owned by root:docker, and our accounts do not have sudo access. This will require assistance from the professor or system administrator.

Ansible: Ansible Core 2.14.18 is installed and uses Python 3.9.25. Its configuration file is located at /etc/ansible/ansible.cfg.





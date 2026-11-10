# Task 1: Project Scheduling & Work Breakdown Structure (WBS)
**Course:** Software Engineering (Lab Integrated) - 231CS523  
**Project:** EduTask - Student Task Management System  
**Team:** 4 Members (Project Lead/DevOps, Backend Dev, Frontend Dev, QA/SCM Engineer)  
**Total Schedule:** 28 Days  

---

## 1. Work Breakdown Structure (WBS)

The Work Breakdown Structure decomposes the EduTask project into five primary functional phases, work packages, and actionable terminal activities.

```
1.0 Project Initiation & Analysis
    1.1 Problem Analysis & Stakeholder Identification (Days 1–3) [Critical]
    1.2 System Requirement Specification (SRS) & WBS Formulation (Days 3–4) [Critical]
2.0 System Architecture & UI/UX Design
    2.1 System Architecture & REST Data Modeling (Days 4–6) [Critical]
    2.2 UI/UX Wireframing & Responsive Component Design (Days 4–5) [Non-Critical, Float=1]
3.0 Full-Stack Core Development (Baseline v1.0)
    3.1 FastAPI REST API & In-Memory Persistence Layer (Days 6–10) [Critical]
    3.2 Vanilla SPA Frontend & REST Controller Integration (Days 7–11) [Non-Critical, Float=0]
    3.3 Code Review, SCM Freezing & Baseline v1.0 Tagging (Day 11) [Critical] [Milestone M2]
4.0 Quality Assurance & Change Control (CR-101)
    4.1 PyTest Suite & Integration Test Formulation (Days 11–14) [Critical]
    4.2 Change Request CR-101 Evaluation & CCB Review (Days 13–14) [Non-Critical]
    4.3 Feature Branch Implementation: Workload Analytics (Days 14–17) [Critical]
    4.4 Regression Testing, PR Merge & Baseline v1.1 Tagging (Days 17–18) [Critical] [Milestone M3]
5.0 DevOps Engineering, Infrastructure as Code & Deployment
    5.1 Multi-Stage Dockerfile Packaging (Days 18–20) [Critical]
    5.2 GitHub Actions CI/CD Pipeline Implementation (Days 20–22) [Critical] [Milestone M4]
    5.3 Infrastructure as Code (Terraform & Docker-Compose) (Days 22–24) [Critical]
    5.4 Synthetic Health Monitoring & Uptime Check Integration (Days 24–25) [Critical]
    5.5 Cloud Staging & Production Deployment on Render (Days 25–26) [Critical] [Milestone M5]
6.0 Final Auditing, Documentation & Viva Preparation
    6.1 4-Page Submission Report & Technical Presentation (Days 26–28) [Critical]
```

---

## 2. Critical Path Method (CPM) Mathematical Analysis

The Critical Path is the sequence of dependent activities that determines the shortest possible project completion time. Any delay in critical activities directly postpones the project release.

### Activity Dependencies, Times & Slack Table

| WBS ID | Activity Description | Predecessors | Duration ($D$) | Early Start ($ES$) | Early Finish ($EF$) | Late Start ($LS$) | Late Finish ($LF$) | Total Slack ($LS - ES$) | On Critical Path? |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1.1** | Problem Analysis & Scope | None | 3 | Day 1 | Day 3 | Day 1 | Day 3 | 0 | **YES** |
| **1.2** | WBS & Schedule Finalization | 1.1 | 1 | Day 3 | Day 4 | Day 3 | Day 4 | 0 | **YES (M1)** |
| **2.1** | Architecture & REST Schema | 1.2 | 2 | Day 4 | Day 6 | Day 4 | Day 6 | 0 | **YES** |
| **2.2** | UI/UX Wireframing | 1.2 | 2 | Day 4 | Day 6 | Day 5 | Day 7 | 1 | NO |
| **3.1** | FastAPI Core CRUD APIs | 2.1 | 4 | Day 6 | Day 10 | Day 6 | Day 10 | 0 | **YES** |
| **3.2** | Frontend SPA Client | 2.2, 3.1 | 4 | Day 7 | Day 11 | Day 7 | Day 11 | 0 | NO |
| **3.3** | Baseline v1.0 Freezing | 3.1, 3.2 | 1 | Day 11 | Day 11 | Day 11 | Day 11 | 0 | **YES (M2)** |
| **4.1** | Automated Test Suite (PyTest) | 3.3 | 3 | Day 11 | Day 14 | Day 11 | Day 14 | 0 | **YES** |
| **4.2** | CCB Change Request CR-101 | 3.3 | 2 | Day 13 | Day 14 | Day 13 | Day 15 | 1 | NO |
| **4.3** | Feature: CR-101 Analytics | 4.1, 4.2 | 3 | Day 14 | Day 17 | Day 14 | Day 17 | 0 | **YES** |
| **4.4** | SCM Merge & Baseline v1.1 | 4.3 | 1 | Day 17 | Day 18 | Day 17 | Day 18 | 0 | **YES (M3)** |
| **5.1** | Dockerfile Multi-Stage Build | 4.4 | 2 | Day 18 | Day 20 | Day 18 | Day 20 | 0 | **YES** |
| **5.2** | GitHub Actions CI/CD Pipeline | 5.1 | 2 | Day 20 | Day 22 | Day 20 | Day 22 | 0 | **YES (M4)** |
| **5.3** | IaC (Terraform & Compose) | 5.2 | 2 | Day 22 | Day 24 | Day 22 | Day 24 | 0 | **YES** |
| **5.4** | Health & Uptime Daemon | 5.3 | 1 | Day 24 | Day 25 | Day 24 | Day 25 | 0 | **YES** |
| **5.5** | Render Deployment | 5.4 | 1 | Day 25 | Day 26 | Day 25 | Day 26 | 0 | **YES (M5)** |
| **6.1** | 4-Page Report & Viva Prep | 5.5 | 2 | Day 26 | Day 28 | Day 26 | Day 28 | 0 | **YES** |

$$\text{Critical Path: } 1.1 \rightarrow 1.2 \rightarrow 2.1 \rightarrow 3.1 \rightarrow 3.3 \rightarrow 4.1 \rightarrow 4.3 \rightarrow 4.4 \rightarrow 5.1 \rightarrow 5.2 \rightarrow 5.3 \rightarrow 5.4 \rightarrow 5.5 \rightarrow 6.1$$
$$\text{Total Critical Project Duration: } 3 + 1 + 2 + 4 + 1 + 3 + 3 + 1 + 2 + 2 + 2 + 1 + 1 + 2 = 28 \text{ Days}$$

---

## 3. Key Project Milestones

| Milestone ID | Milestone Description | Target Day | Verification Artifact |
| :--- | :--- | :---: | :--- |
| **M1: Architecture Baseline** | SRS, WBS, and REST Data Models finalized | Day 4 | WBS Document & Data Schemas |
| **M2: SCM Baseline v1.0** | Core Task CRUD, Course Tagging & UI operational | Day 11 | Annotated Git Tag `v1.0` |
| **M3: SCM Baseline v1.1** | CR-101 Study Load Analytics implemented & regression tested | Day 18 | Annotated Git Tag `v1.1` & PR #1 |
| **M4: CI/CD Pipeline Live** | Automated GitHub Actions workflow testing with JUnit XML | Day 22 | `.github/workflows/ci-cd.yml` |
| **M5: Production Release** | Containerized app live on Render cloud platform & Uptime active | Day 26 | Live Render URL & Uptime Log |

---

## 4. Resource Allocation & RACI Matrix

### Team Roles:
- **Member 1 (Lead / DevOps Engineer):** Project scheduling, WBS, Docker, CI/CD Actions, Terraform IaC, Uptime checks.
- **Member 2 (Backend Developer):** FastAPI framework, REST endpoint handlers, Data persistence, Business logic.
- **Member 3 (Frontend Developer):** HTML5/CSS3/JavaScript SPA, UI responsiveness, Event handling, DOM binding.
- **Member 4 (QA / SCM Specialist):** SCM GitFlow branching, Baseline tagging, Change Control Board, PyTest JUnit suite.

### RACI Matrix

| Activity | Member 1 (DevOps/Lead) | Member 2 (Backend) | Member 3 (Frontend) | Member 4 (QA/SCM) |
| :--- | :---: | :---: | :---: | :---: |
| 1.0 Requirements & WBS | **Accountable / Responsible** | Consulted | Consulted | Consulted |
| 2.1 Architecture Design | Consulted | **Accountable / Responsible** | Consulted | Informed |
| 2.2 UI/UX Wireframing | Informed | Consulted | **Accountable / Responsible** | Informed |
| 3.1 FastAPI CRUD API | Informed | **Accountable / Responsible** | Consulted | Informed |
| 3.2 SPA Frontend | Informed | Consulted | **Accountable / Responsible** | Informed |
| 3.3 Baseline v1.0 Freezing | Consulted | Informed | Informed | **Accountable / Responsible** |
| 4.1 PyTest JUnit Suite | Consulted | Consulted | Informed | **Accountable / Responsible** |
| 4.2 Change Request CR-101 | **Accountable** | Responsible | Responsible | Responsible |
| 4.4 Baseline v1.1 Tagging | Informed | Informed | Informed | **Accountable / Responsible** |
| 5.1 Docker Packaging | **Accountable / Responsible** | Consulted | Informed | Informed |
| 5.2 GitHub Actions CI/CD | **Accountable / Responsible** | Informed | Informed | Consulted |
| 5.3 Terraform & IaC | **Accountable / Responsible** | Informed | Informed | Informed |
| 5.4 Uptime & Monitoring | **Accountable / Responsible** | Informed | Informed | Responsible |
| 5.5 Cloud Deployment | **Accountable / Responsible** | Informed | Informed | Informed |
| 6.0 Report & Viva | **Accountable** | Responsible | Responsible | Responsible |

*Legend: **R** - Responsible, **A** - Accountable, **C** - Consulted, **I** - Informed.*

---

## 5. Visual Artifacts
- **Primary Deliverable 2:** Vector PDF available at [`docs/Gantt_Chart.pdf`](file:///C:/Users/dorot/OneDrive/deborah%20FODS/SE%20ASSIGNMENT4/docs/Gantt_Chart.pdf).
- **Interactive Browser View:** Open [`docs/gantt_chart.html`](file:///C:/Users/dorot/OneDrive/deborah%20FODS/SE%20ASSIGNMENT4/docs/gantt_chart.html) in any browser.

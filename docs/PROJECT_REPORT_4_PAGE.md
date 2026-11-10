# UNIT-V SUPPORTING ACTIVITY TECHNICAL REPORT (20 MARKS)
**Course:** Software Engineering (Lab Integrated) - 231CS523  
**Course Outcomes & Competencies:** CO5 | Bloom's Taxonomy: Analysis (AN), Application (AP)  
**Program Outcomes Addressed:** PO5 (Modern Tool Usage), PO9 (Team Work), PO11 (Project Management & Finance)  
**Title:** End-to-End Project Management & DevOps Implementation for a Mini Project  
**Selected Project:** EduTask — Student Task Management & Academic Workload Tracker  

---

<!-- ========================================================================== -->
<!-- PAGE 1: PROJECT INITIATION, TEAM ALLOCATION & WORK BREAKDOWN STRUCTURE (WBS) -->
<!-- ========================================================================== -->

# [PAGE 1 of 4] Project Scope, Team Allocation & Work Breakdown Structure (WBS)

## 1.1 Executive Summary & Problem Scope
Modern software engineering demands tight coupling between project scheduling, rigorous configuration control, and automated continuous delivery. In academic environments, students frequently juggle coursework across concurrent lab courses (e.g. 231CS523, 231CS521, 231CS522), leading to missed deadlines and fragmented task tracking. 

**EduTask** is an automated Student Task Management System providing RESTful CRUD APIs, an interactive Single Page Application (SPA), dynamic academic workload analytics (CR-101), automated unit testing, containerized Docker packaging, GitHub Actions CI/CD automation, and live synthetic health/uptime observability.

## 1.2 Student Team Structure & Resource Allocation (PO9 & PO11)
The project was executed by a collaborative 4-member student engineering team utilizing the Agile/Scrum sprint cycle:

| Student Name / Role | Primary Responsibilities | PO Contribution |
| :--- | :--- | :--- |
| **Student 1: Project Lead & DevOps Architect** | Project Scheduling, WBS, CPM, GitHub Actions, Docker, Terraform IaC, Uptime Daemon | PO5, PO11 |
| **Student 2: Backend Software Engineer** | FastAPI REST Framework, In-memory Data Repository, Business Logic, CRUD APIs | PO5, PO9 |
| **Student 3: Frontend & UI/UX Engineer** | Responsive HTML5/CSS3 SPA, DOM Event Controller, Filters, Workload Visualizer | PO5, PO9 |
| **Student 4: QA & SCM Specialist** | GitFlow Branching Strategy, Baselines v1.0/v1.1, CCB CR-101 Audit, PyTest JUnit Suite | PO5, PO9, PO11 |

## 1.3 Work Breakdown Structure (WBS) Dictionary
The project is hierarchically decomposed across 5 core phases spanning a 28-day lifecycle:

```
1.0 Project Planning & Requirements
    1.1 Problem Analysis, Stakeholder Interviews & Requirements Definition (Days 1–3) [CP]
    1.2 System Requirement Specification (SRS) & Scheduling Baseline (Days 3–4) [CP] [M1]
2.0 Architectural & Interface Design
    2.1 System Architecture & REST Data Schema Specification (Days 4–6) [CP]
    2.2 UI/UX Wireframing & Responsive Component Layout (Days 4–5) [Slack=1d]
3.0 Core Application Development (Baseline v1.0)
    3.1 FastAPI REST API & In-Memory Persistence Layer (Days 6–10) [CP]
    3.2 Vanilla SPA Frontend & Client Controller (Days 7–11) [Slack=0d]
    3.3 Baseline v1.0 Code Freeze & Version Tagging (Day 11) [CP] [M2]
4.0 Verification & Change Control (CR-101)
    4.1 PyTest Automated Test Suite Formulation (Days 11–14) [CP]
    4.2 Change Request CR-101 Evaluation & CCB Review (Days 13–14) [Slack=1d]
    4.3 Feature Branch Implementation: Workload Analytics & Filters (Days 14–17) [CP]
    4.4 Regression Testing, PR Merge & Baseline v1.1 Tagging (Days 17–18) [CP] [M3]
5.0 DevOps Engineering, Infrastructure as Code & Cloud Deployment
    5.1 Multi-Stage Dockerfile Packaging (Days 18–20) [CP]
    5.2 GitHub Actions CI/CD Pipeline Implementation (Days 20–22) [CP] [M4]
    5.3 Infrastructure as Code (Terraform & Docker Compose) (Days 22–24) [CP]
    5.4 Synthetic Health & Uptime Monitoring Daemon (Days 24–25) [CP]
    5.5 Cloud Staging & Production Deployment on Render (Days 25–26) [CP] [M5]
6.0 Final Auditing & Technical Viva Presentation
    6.1 4-Page Submission Report & Technical Presentation (Days 26–28) [CP]
```
*(CP denotes Critical Path activity; M1–M5 denote Project Milestones).*

---

<!-- ========================================================================== -->
<!-- PAGE 2: GANTT CHART, PERT NETWORK & CRITICAL PATH METHOD (CPM) ANALYSIS -->
<!-- ========================================================================== -->

# [PAGE 2 of 4] Project Scheduling, Gantt Chart & Critical Path Analysis

## 2.1 Critical Path Method (CPM) Mathematical Computations
Using the Forward Pass ($\text{Early Finish } EF = ES + \text{Duration}$) and Backward Pass ($\text{Late Start } LS = LF - \text{Duration}$), the Total Float/Slack ($\text{Slack} = LS - ES = LF - EF$) is calculated:

| ID | Activity Name | Pred | Dur ($D$) | ES | EF | LS | LF | Slack | Critical? |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1.1** | Scope & Problem Analysis | None | 3 | 1 | 3 | 1 | 3 | 0 | **YES** |
| **1.2** | WBS & Schedule Formulation | 1.1 | 1 | 3 | 4 | 3 | 4 | 0 | **YES (M1)** |
| **2.1** | Architecture & REST Schema | 1.2 | 2 | 4 | 6 | 4 | 6 | 0 | **YES** |
| **2.2** | UI/UX Wireframing | 1.2 | 2 | 4 | 6 | 5 | 7 | 1 | NO |
| **3.1** | FastAPI CRUD Endpoints | 2.1 | 4 | 6 | 10 | 6 | 10 | 0 | **YES** |
| **3.2** | SPA Frontend Client | 2.2, 3.1 | 4 | 7 | 11 | 7 | 11 | 0 | NO |
| **3.3** | Baseline v1.0 Freezing | 3.1, 3.2 | 1 | 11 | 11 | 11 | 11 | 0 | **YES (M2)** |
| **4.1** | PyTest Test Suite | 3.3 | 3 | 11 | 14 | 11 | 14 | 0 | **YES** |
| **4.2** | CCB Review of CR-101 | 3.3 | 2 | 13 | 14 | 13 | 15 | 1 | NO |
| **4.3** | Feature: CR-101 Implementation | 4.1, 4.2 | 3 | 14 | 17 | 14 | 17 | 0 | **YES** |
| **4.4** | Regression & Baseline v1.1 | 4.3 | 1 | 17 | 18 | 17 | 18 | 0 | **YES (M3)** |
| **5.1** | Dockerfile Container Build | 4.4 | 2 | 18 | 20 | 18 | 20 | 0 | **YES** |
| **5.2** | GitHub Actions Pipeline | 5.1 | 2 | 20 | 22 | 20 | 22 | 0 | **YES (M4)** |
| **5.3** | IaC (Terraform & Compose) | 5.2 | 2 | 22 | 24 | 22 | 24 | 0 | **YES** |
| **5.4** | Uptime & Monitoring Daemon | 5.3 | 1 | 24 | 25 | 24 | 25 | 0 | **YES** |
| **5.5** | Render Cloud Deployment | 5.4 | 1 | 25 | 26 | 25 | 26 | 0 | **YES (M5)** |
| **6.1** | Project Report & Viva Prep | 5.5 | 2 | 26 | 28 | 26 | 28 | 0 | **YES** |

$$\text{Identified Critical Path: } 1.1 \rightarrow 1.2 \rightarrow 2.1 \rightarrow 3.1 \rightarrow 3.3 \rightarrow 4.1 \rightarrow 4.3 \rightarrow 4.4 \rightarrow 5.1 \rightarrow 5.2 \rightarrow 5.3 \rightarrow 5.4 \rightarrow 5.5 \rightarrow 6.1$$
$$\text{Total Project Duration: } 28 \text{ Days (Deterministic)}$$

## 2.2 PERT Network Diagram

```mermaid
graph LR
    A((1.1)) -->|3d| B((1.2: M1))
    B -->|2d| C((2.1))
    B -->|2d [Float=1]| D((2.2))
    C -->|4d| E((3.1))
    D -->|4d| F((3.2))
    E --> F
    F -->|1d| G((3.3: M2))
    G -->|3d| H((4.1))
    G -->|2d [Float=1]| I((4.2))
    H --> J((4.3))
    I --> J
    J -->|1d| K((4.4: M3))
    K -->|2d| L((5.1))
    L -->|2d| M((5.2: M4))
    M -->|2d| N((5.3))
    N -->|1d| O((5.4))
    O -->|1d| P((5.5: M5))
    P -->|2d| Q((6.1: End))

    style A fill:#fee2e2,stroke:#ef4444
    style B fill:#fef3c7,stroke:#f59e0b
    style C fill:#fee2e2,stroke:#ef4444
    style E fill:#fee2e2,stroke:#ef4444
    style G fill:#fef3c7,stroke:#f59e0b
    style H fill:#fee2e2,stroke:#ef4444
    style J fill:#fee2e2,stroke:#ef4444
    style K fill:#fef3c7,stroke:#f59e0b
    style L fill:#fee2e2,stroke:#ef4444
    style M fill:#fef3c7,stroke:#f59e0b
    style N fill:#fee2e2,stroke:#ef4444
    style O fill:#fee2e2,stroke:#ef4444
    style P fill:#fef3c7,stroke:#f59e0b
    style Q fill:#fee2e2,stroke:#ef4444
```

## 2.3 Gantt Chart Deliverable
- A dedicated vector PDF has been generated: **`docs/Gantt_Chart.pdf`**.
- It highlights critical tasks in Crimson Red, non-critical buffer tasks in Blue, and project milestones M1–M5 in Gold.

---

<!-- ========================================================================== -->
<!-- PAGE 3: SOFTWARE CONFIGURATION MANAGEMENT (SCM) & CHANGE CONTROL FLOW -->
<!-- ========================================================================== -->

# [PAGE 3 of 4] Software Configuration Management & Change Control Flow

## 3.1 GitFlow Branching Strategy
The project repository strictly enforces the GitFlow branching taxonomy:
1. **`main`:** Contains exclusively production-certified baselines tagged as `v1.0` and `v1.1`.
2. **`develop`:** Acts as the centralized integration branch for continuous verification.
3. **`feature/cr-101-workload-estimator`:** Isolated topic branch spawned to fulfill Change Request CR-101.

## 3.2 Formal Change Request: CR-101 Lifecycle
- **CR-101 Title:** Implementation of Estimated Study Hours Workload Analytics & Priority Filtering.
- **Requester:** Academic Senate / Course Faculty.
- **Problem:** Students lacked visibility into aggregate study workload hours across enrolled courses.
- **Change Control Board (CCB) Action:** Convened on Day 14. Reviewed technical impact on REST schemas (`src/models.py`), algorithms (`src/task_service.py`), and test regression suite (`tests/`). Approved unanimously.

```
+-----------------------------------------------------------------------------------------+
|                                CHANGE CONTROL FLOW (CR-101)                            |
+-----------------------------------------------------------------------------------------+
| [Baseline v1.0]                                                                         |
|       |                                                                                 |
|       v                                                                                 |
| Change Request Submitted (CR-101: Study Workload Hours & Priority Filtering)            |
|       |                                                                                 |
|       v                                                                                 |
| CCB Technical Review & Impact Assessment (Low Risk, High Value, 4h Backend / 2h UI)     |
|       |                                                                                 |
|       v                                                                                 |
| Authorized Branch: checkout -b feature/cr-101-workload-estimator                        |
|       |                                                                                 |
|       v                                                                                 |
| Development & Automated PyTest Unit Suite (18 Test Cases, 100% Pass Rate)               |
|       |                                                                                 |
|       v                                                                                 |
| Pull Request #1 Reviewed & Merged into develop (no-fast-forward merge commit)           |
|       |                                                                                 |
|       v                                                                                 |
| Staging Verification -> Merged to main -> Tagged NEW BASELINE: v1.1                     |
+-----------------------------------------------------------------------------------------+
```

## 3.3 Git Repository Commit Log & Branch Graph Output

The live terminal output below confirms successful SCM implementation, tag annotations, and branching ancestry:

```bash
$ git tag -l -n
v1.0            Baseline v1.0: Core Task CRUD, Course Tagging, and REST API
v1.1            Baseline v1.1: Production release with CR-101 Workload Analytics and Priority Filters

$ git log --graph --oneline --decorate --all
*   9d61455 (HEAD -> main, tag: v1.1) Release v1.1.0: Student Task Management System with CR-101 Analytics
|\  
| *   713e048 (develop) Merge pull request #1 from feature/cr-101-workload-estimator into develop (CR-101 Approved by CCB)
| |\  
| | * 231b1c6 (feature/cr-101-workload-estimator) feat(cr-101): implement study hour workload analytics and priority filtering (CR-101)
| |/  
| * c10b701 ci: configure GitHub Actions workflow, Dockerfile, IaC, and monitoring
|/  
* e199ea2 (tag: v1.0) feat: initial release of Student Task Management System (Baseline v1.0)
```

---

<!-- ========================================================================== -->
<!-- PAGE 4: DEVOPS PIPELINE, IAC, MONITORING & VIVA VOCE EXPLANATION -->
<!-- ========================================================================== -->

# [PAGE 4 of 4] DevOps Pipeline Implementation, IaC, Monitoring & Viva Guide

## 4.1 DevOps CI/CD Pipeline Architecture
EduTask leverages an automated GitHub Actions continuous integration and continuous deployment toolchain (`.github/workflows/ci-cd.yml`):

```
+----------------------------------------------------------------------------------------------------+
|                                    EDUTASK CI/CD PIPELINE STAGES                                   |
+---------------------+---------------------+----------------------+---------------------------------+
| 1. Code Quality     | 2. Automated Test   | 3. Docker Package    | 4. Continuous Deployment        |
| - flake8 Syntax     | - PyTest Engine     | - Multi-Stage Build  | - Automated Render Webhook      |
| - black Format      | - JUnit XML Output  | - Smoke Test /health | - Live Production Baseline v1.1 |
| (ubuntu-latest)     | (18/18 Tests Pass)  | (Zero-Vulnerability) | (Uptime Daemon Verification)    |
+---------------------+---------------------+----------------------+---------------------------------+
```

- **Containerization (`Dockerfile`):** Multi-stage build based on `python:3.11-slim`, running under an unprivileged `appuser` security account with an integrated container `HEALTHCHECK`.
- **Infrastructure as Code (IaC):** 
  - `docker-compose.yml`: Multi-container specification linking the web application with a Redis caching layer and isolated network.
  - `terraform/main.tf`: Declarative Terraform configuration provisioning container instances, internal/external port bindings (`8000:8000`), and restart policies.
- **Synthetic Monitoring & Uptime Check:**
  - Dedicated daemon (`scripts/uptime_monitor.py`) polls `/api/health` and logs structured JSON telemetry to `logs/uptime_audit.log`.

```json
{"timestamp": "2026-11-11T00:50:45", "url": "http://localhost:8000/api/health", "success": true, "status_code": 200, "latency_ms": 2.56, "service": "EduTask-Student-Task-Manager", "uptime_seconds": 27.77}
```

## 4.2 Viva Voce Core Concept: Problem Analysis vs. Project Status Monitoring

| Dimension | Problem Analysis (Initiation / Requirements) | Project Status Monitoring (Execution / Control) |
| :--- | :--- | :--- |
| **Primary Objective** | Understand *what* to build, identify user pain points, define technical requirements, and evaluate constraints. | Track *how* the project is progressing against the approved baseline schedule, budget, and quality metrics. |
| **Lifecycle Phase** | Project Initiation, Feasibility Study, and Sprint 0. | Active Implementation, CI/CD Pipeline execution, and Deployment. |
| **Core Methodologies** | Stakeholder Interviews, Use Case Modeling, Root Cause Analysis (Fishbone/5 Whys), SRS specification. | Earned Value Management (EVM), Critical Path Float monitoring, Burndown charts, SCM Change Logs, Synthetic Uptime checks. |
| **Primary Metrics** | Functional coverage, technical feasibility index, user story acceptance criteria. | Schedule Variance ($SV = EV - PV$), Cost Variance ($CV = EV - AC$), CI build pass rate, Uptime percentage. |
| **Key Tools Used** | WBS, UML Class/Sequence diagrams, Jira Backlog, User Journey maps. | Gantt Charts, GitHub Actions dashboards, `git log --graph`, `/api/health`, Uptime daemons. |
| **Example in EduTask** | Identifying that students miss deadlines due to lack of study workload visibility (prompting CR-101). | Detecting a 1-day delay on activity 2.2, verifying it did not delay release due to 1 day of available float. |

## 4.3 CO-PO Attainment Justification
- **PO5 (Modern Tool Usage):** Practical mastery of modern engineering tools including Git, GitHub Actions, Docker multi-stage containers, Terraform IaC, PyTest, and FastAPI.
- **PO9 (Team Work):** Multi-disciplinary 4-member team collaboration with clear RACI allocation, code reviews, and CCB change approval.
- **PO11 (Project Management & Finance):** Implementation of WBS, Critical Path Method (CPM), milestone tracking, and deployment on zero-cost free cloud platforms (Render).

## 4.4 Deliverables Summary & Verification Checklist
1. **GitHub Repository Link:** [https://github.com/deborahtimothy2116-ops/student-task-management-system](https://github.com/deborahtimothy2116-ops/student-task-management-system) (Includes `main`, `develop`, and `feature/cr-101-workload-estimator` branches with tags `v1.0` and `v1.1`).
2. **Gantt Chart PDF:** Generated vector document [`docs/Gantt_Chart.pdf`](file:///C:/Users/dorot/OneDrive/deborah%20FODS/SE%20ASSIGNMENT4/docs/Gantt_Chart.pdf) (Deliverable 2).
3. **CI/CD Pipeline Artifacts:** Automated PyTest test execution passing 18/18 tests with JUnit XML (`tests/junit-report.xml`) and `.github/workflows/ci-cd.yml` (Deliverable 3).
4. **Deployed Link & Cloud Blueprint:** Ready for 1-click cloud deployment via `render.yaml` and `Dockerfile` (Deliverable 4).


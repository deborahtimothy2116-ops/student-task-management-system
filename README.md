# EduTask: Student Task Management System
### End-to-End Project Management & DevOps Implementation (20 Marks)
**Course:** Software Engineering (Lab Integrated) - 231CS523  
**Competencies:** CO5 | Bloom's Taxonomy: Analysis (AN), Application (AP)  
**Program Outcomes:** PO5 (Modern Tool Usage), PO9 (Team Work), PO11 (Project Management & Finance)  

---

## 🌟 Executive Overview
**EduTask** is a full-stack, containerized academic task and assignment management system built with Python (FastAPI), an interactive responsive Single Page Application (SPA), a complete automated PyTest suite, a multi-stage Docker build, a GitHub Actions CI/CD pipeline, and Infrastructure as Code (IaC) via Docker Compose and Terraform.

This repository serves as the complete implementation for the **Unit-V Supporting Activity**, fulfilling all 4 tasks and 4 mandatory deliverables in the academic rubric.

---

## 🎯 Deliverables Checklist (Evaluation Rubric: 20 Marks)

| Deliverable | Description | Location / Status | Marks |
| :--- | :--- | :--- | :---: |
| **Deliverable 1** | **GitHub Repository & SCM History** | GitFlow (`main`, `develop`, `feature/cr-101`), Tags `v1.0` & `v1.1` | **5M** |
| **Deliverable 2** | **Project Scheduling & Gantt Chart** | Vector PDF: [`docs/Gantt_Chart.pdf`](docs/Gantt_Chart.pdf) & HTML view: [`docs/gantt_chart.html`](docs/gantt_chart.html) | **5M** |
| **Deliverable 3** | **DevOps CI/CD Pipeline & Tests** | GitHub Actions [`ci-cd.yml`](.github/workflows/ci-cd.yml), PyTest JUnit XML [`junit-report.xml`](tests/junit-report.xml) | **7M** |
| **Deliverable 4** | **4-Page Report & Viva Guide** | Report: [`docs/PROJECT_REPORT_4_PAGE.md`](docs/PROJECT_REPORT_4_PAGE.md), Viva: [`docs/VIVA_PREPARATION_GUIDE.md`](docs/VIVA_PREPARATION_GUIDE.md) | **3M** |

---

## 🚀 Key Features
- **Assignment Tracking:** Create, edit, list, and filter coursework by course tag (e.g. `231CS523`), priority, and completion status.
- **CR-101 Study Load Analytics:** Automated calculation of estimated study hours, pending workload, completion rates, and dynamic overdue alerts.
- **RESTful Architecture:** FastAPI backend with OpenAPI `/docs` documentation, latency middleware, and CORS enablement.
- **Observability:** Synthetic `/api/health` and `/api/metrics` endpoints monitored by an automated Python uptime daemon.
- **Production Containerization:** Lightweight multi-stage Docker image (<120MB) running as a non-root security user.

---

## 🛠️ Technology Stack
- **Backend:** Python 3.11+, FastAPI, Pydantic v2, Uvicorn
- **Frontend:** Vanilla HTML5, Modern CSS3 (CSS Grid/Flexbox), JavaScript (ES6+ Fetch API)
- **Automated Testing:** PyTest, HTTPX TestClient, JUnit XML Reporter
- **SCM & Versioning:** Git, GitFlow, Annotated Tags (`v1.0`, `v1.1`), CCB Change Control Flow
- **DevOps CI/CD:** GitHub Actions (Matrix Linting, PyTest JUnit Artifacts, Docker Packaging)
- **Containerization:** Multi-Stage Dockerfile, Docker Compose
- **Infrastructure as Code (IaC):** Terraform (`terraform/main.tf` using Docker Provider), Docker Compose
- **Cloud Deployment:** Render PaaS (`render.yaml`), DockerHub container image
- **Monitoring:** Synthetic HTTP Uptime & Latency Monitor (`scripts/uptime_monitor.py`)

---

## 📋 Quickstart Instructions

### 1. Run Application Locally
```bash
# Clone the repository
git clone <your-repo-link>
cd SE-ASSIGNMENT4

# Install dependencies
pip install -r requirements.txt

# Start the development server
python -m uvicorn src.main:app --reload --port 8000
```
Open your browser at **`http://localhost:8000`** to interact with the Single Page Application, or view interactive API documentation at **`http://localhost:8000/docs`**.

### 2. Run Automated PyTest Suite (JUnit XML Generation)
```bash
pytest tests/ -v --junitxml=tests/junit-report.xml
```
*Output: 18 test cases passed (100% success rate), generating `tests/junit-report.xml`.*

### 3. Run Containerized Application via Docker Compose
```bash
docker compose up --build -d
```
Inspect container health:
```bash
docker ps
curl http://localhost:8000/api/health
```

### 4. Deploy Infrastructure via Terraform (IaC)
```bash
cd terraform
terraform init
terraform plan
terraform apply -auto-approve
```

### 5. Run Synthetic Health & Uptime Monitoring Daemon
```bash
# Single probe check
python scripts/uptime_monitor.py --single-run

# Continuous monitoring with 10s polling interval
python scripts/uptime_monitor.py --interval 10
```
Audit logs are continuously written to `logs/uptime_audit.log`.

---

## 🌿 SCM Branching Strategy & Baseline Tags

EduTask implements GitFlow with explicit milestone baselines:

```
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

- **Baseline v1.0:** Core CRUD APIs and basic UI.
- **Change Request CR-101:** Formal CCB approval for Study Workload Estimator & Priority Filtering.
- **Baseline v1.1:** Merged release with full test suite passing.

---

## 📂 Repository File Structure
```
.
├── .github/
│   └── workflows/
│       └── ci-cd.yml               # GitHub Actions CI/CD Pipeline
├── docs/
│   ├── Gantt_Chart.pdf             # Deliverable 2: Vector Gantt Chart PDF
│   ├── gantt_chart.html            # Interactive Browser Gantt Visualizer
│   ├── wbs_and_scheduling.md       # WBS, CPM Math & RACI Matrix
│   ├── scm_change_request_flow.md  # SCM GitFlow & CR-101 Documentation
│   ├── PROJECT_REPORT_4_PAGE.md    # Deliverable 4: 4-Page Submission Report
│   └── VIVA_PREPARATION_GUIDE.md   # Viva Voce Preparation Guide (Problem Analysis vs Status)
├── scripts/
│   ├── generate_gantt_pdf.py       # Standalone vector PDF & HTML Gantt generator
│   └── uptime_monitor.py           # Synthetic health & uptime monitor daemon
├── src/
│   ├── static/
│   │   ├── app.js                  # Frontend UI Controller
│   │   ├── index.html              # Responsive SPA Dashboard
│   │   └── styles.css              # Custom styling
│   ├── main.py                     # FastAPI server, CORS, middleware, REST routes
│   ├── models.py                   # Pydantic schemas (Tasks, Analytics, Health)
│   └── task_service.py             # Business logic & CR-101 analytics engine
├── terraform/
│   ├── main.tf                     # IaC container provisioning definition
│   └── variables.tf                # Terraform input variables
├── tests/
│   ├── conftest.py                 # PyTest test fixtures
│   ├── junit-report.xml            # Generated JUnit XML test report
│   ├── test_api.py                 # API & endpoint integration tests
│   └── test_tasks.py               # Domain logic & CR-101 unit tests
├── .dockerignore                   # Docker exclusion rules
├── .gitignore                      # Git exclusion rules
├── docker-compose.yml              # Multi-container orchestration specification
├── Dockerfile                      # Multi-stage production container build
├── render.yaml                     # Cloud deployment blueprint (Render PaaS)
├── requirements.txt                # Python project dependencies
├── setup_git_scm.py                # Automated SCM & GitFlow initialization script
└── README.md                       # Master Documentation
```

---

## 🎓 Academic Viva Reference: Problem Analysis vs. Project Status Monitoring
For detailed answers to all viva voce questions, refer to [`docs/VIVA_PREPARATION_GUIDE.md`](docs/VIVA_PREPARATION_GUIDE.md).

- **Problem Analysis:** Investigates user pain points, defines requirements (SRS), and evaluates constraints during project inception.
- **Project Status Monitoring:** Tracks actual progress against approved baselines (Gantt, CPM Float, EVM, CI/CD logs, Uptime) during execution to detect variances and apply corrective control.

---
*Course: 231CS523 Software Engineering &bull; Unit-V Supporting Activity (20 Marks)*

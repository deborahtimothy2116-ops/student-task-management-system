# Comprehensive Viva Voce Preparation Guide (231CS523 Unit-V)
**Course:** Software Engineering (Lab Integrated) - 231CS523  
**Activity:** Unit-V Supporting Activity (20 Marks)  
**Project:** EduTask - Student Task Management System  

---

## Question 1: Explain "Problem Analysis" vs. "Project Status Monitoring" in Depth.

This is the central theoretical topic specifically highlighted in the syllabus rubric.

### Conceptual Comparison

| Key Aspect | Problem Analysis | Project Status Monitoring |
| :--- | :--- | :--- |
| **Primary Definition** | The analytical process of identifying user needs, defining problem boundaries, discovering root causes, and formulating clear functional requirements. | The operational process of tracking actual project progress against planned project baselines (Schedule, Scope, and Cost) to detect variance and initiate corrective action. |
| **When it Occurs** | Prior to development (Project Inception, Feasibility Study, Sprint 0). | Continuously throughout the development lifecycle (Sprints 1–N, CI/CD, Deployment). |
| **Core Question Answered** | *"Are we solving the right problem, and what are its functional requirements and constraints?"* | *"Are we on schedule, within budget, meeting quality standards, and will we deliver on time?"* |
| **Techniques Used** | Stakeholder interviews, Root Cause Analysis (Ishikawa/Fishbone diagram, 5-Whys), Use Case modeling, SRS formulation, Feasibility studies. | Critical Path Method (CPM), Earned Value Management (EVM), Burndown charts, Milestone tracking, Automated CI/CD logs, Uptime monitoring. |
| **Mathematical Formulas** | - Cost-Benefit Ratio: $CBR = \frac{\text{Present Value of Benefits}}{\text{Present Value of Costs}}$<br>- Requirement Priority Weighting: $W_i = \sum (V_i \times P_i)$ | - Schedule Variance: $SV = EV - PV$<br>- Cost Variance: $CV = EV - AC$<br>- Schedule Performance Index: $SPI = \frac{EV}{PV}$ ($>1$ is ahead of schedule)<br>- Cost Performance Index: $CPI = \frac{EV}{AC}$ ($>1$ is under budget) |
| **Tools Utilized** | WBS, UML diagrams, Jira Product Discovery, Persona mapping. | MS Project, Gantt Charts, GitHub Actions CI dashboard, `git log --graph`, Synthetic health monitors. |
| **EduTask Project Example** | Discovering that students struggle with multi-course deadlines (231CS523 + 231CS521) and require study workload hours estimation (origin of CR-101). | Tracking daily progress on the 28-day schedule; observing that UI wireframing had 1 day of float, ensuring no critical path slippage occurred. |

---

## Question 2: What is a Software Baseline and why is Version Tagging (`v1.0`, `v1.1`) essential in SCM?
- **Definition:** A **Baseline** is an approved and frozen version of a software configuration item (source code, schemas, documents, test suites) that serves as the official foundation for subsequent activities and can only be altered through formal change control.
- **Why Version Tagging Matters:**
  1. **Traceability:** Provides an immutable snapshot of the exact code running in production. If a bug is detected, developers can checkout `git checkout v1.0` to reproduce issues in an identical environment.
  2. **Auditability & Reproducibility:** Enables automated CI/CD pipelines to build and deploy specific releases deterministically.
  3. **Release Isolation:** Distinguishes between minor enhancements (`v1.1`), major architectural overhauls (`v2.0`), and urgent hotfixes (`v1.0.1`).

---

## Question 3: Explain the Change Control Board (CCB) process and the lifecycle of Change Request CR-101.
1. **Submission:** A stakeholder submits a formal Change Request (CR) document detailing problem statement, justification, and suggested modifications.
2. **Impact Analysis:** Engineers assess the architectural impact (REST schema compatibility), effort estimation (e.g. 4h backend, 2h frontend), and risk level (low risk).
3. **CCB Evaluation:** The Change Control Board (composed of Lead, Backend, Frontend, and QA engineers) meets to review, vote, and approve/reject the request.
4. **Implementation on Isolated Feature Branch:** Developer checks out `feature/cr-101-workload-estimator` from `develop`, implements the feature, and writes unit tests.
5. **Verification & Regression Testing:** PyTest runs against the feature branch to guarantee zero regression on existing functionality.
6. **Integration & New Baseline Release:** The PR is merged into `develop` and subsequently into `main`, where a new official baseline tag (`v1.1`) is minted.

---

## Question 4: How is the Critical Path identified, and what does "Total Float / Slack" mean?
- **Critical Path:** The longest sequence of dependent activities from project start to finish. It dictates the minimum completion time of the project.
- **Slack (or Float):** The duration an activity can be delayed without delaying the project finish date.
  $$\text{Total Slack} = LS - ES = LF - EF$$
- **Rule:** Any activity on the Critical Path has **Zero Slack ($\text{Slack} = 0$)**. Any delay on a critical activity extends the entire project deadline. In our schedule, Activity 2.2 (UI/UX Wireframes) has a slack of 1 day, meaning it could start on Day 4 or Day 5 without delaying Sprint 1 delivery.

---

## Question 5: Why did we select GitFlow instead of Trunk-Based Development?
- **Trunk-Based Development** involves all developers committing directly to a single shared `main` branch with feature flags. While lightweight for small teams, it presents high risk of destabilizing the production release during academic evaluations.
- **GitFlow** provides explicit release boundaries:
  - `main` remains 100% bug-free and corresponds strictly to tagged production releases (`v1.0`, `v1.1`).
  - `develop` aggregates work-in-progress code.
  - `feature/*` branches prevent experimental code from breaking the main build.

---

## Question 6: What is a Multi-Stage Dockerfile and why is it superior to a single-stage build?
- In a traditional single-stage Dockerfile, build dependencies (compilers like `gcc`, pip caches, build headers) remain in the final container image, inflating its size to 800MB–1GB and introducing CVE vulnerabilities.
- In our **Multi-Stage Dockerfile**:
  - **Stage 1 (`builder`):** Installs build tools and downloads Python dependencies.
  - **Stage 2 (`runner`):** Copies only the compiled packages into a lean `python:3.11-slim` image, creates an unprivileged non-root user (`appuser`), and runs the app.
  - **Result:** Image size drops from ~850MB to <120MB, image attack surface is minimized, and running as non-root protects against container breakout exploits.

---

## Question 7: Explain the difference between Continuous Integration (CI), Delivery (CD), and Deployment (CD).
1. **Continuous Integration (CI):** Developers frequently merge code into a shared repository; every push automatically triggers syntax linting (flake8/black), unit tests (PyTest), and build packaging (Docker) to catch integration bugs early.
2. **Continuous Delivery (CD):** Ensures that tested code can be safely released to production at any moment with manual approval (e.g., clicking a deploy button).
3. **Continuous Deployment (CD):** Every commit that passes the automated pipeline is automatically deployed directly to the live production server without human intervention (as demonstrated via Render's automated GitHub deployment webhook).

---

## Question 8: What is Infrastructure as Code (IaC) and what are its key advantages?
- **Definition:** Managing and provisioning compute, network, and container resources through declarative configuration files rather than manual clicking in cloud web consoles.
- **Key Advantages:**
  1. **Idempotency:** Running `terraform apply` multiple times produces the exact same infrastructure state without unexpected side effects.
  2. **Version Control:** Infrastructure definitions (`terraform/main.tf`, `docker-compose.yml`) live in Git alongside application source code, tracking changes over time.
  3. **Disaster Recovery:** A complete production cluster can be re-provisioned in seconds with a single command.

---

## Question 9: How does Synthetic Uptime Monitoring work in EduTask?
- The Python monitoring daemon (`scripts/uptime_monitor.py`) sends periodic HTTP GET requests to the `/api/health` endpoint.
- It verifies:
  1. HTTP Status Code `200 OK`.
  2. JSON payload status equals `"UP"`.
  3. Latency measurement (in milliseconds).
- It logs each transaction into `logs/uptime_audit.log` and calculates the percentage availability ($\frac{\text{Successful Pings}}{\text{Total Probes}} \times 100\%$).

---

## Question 10: How does this activity satisfy Course Outcomes and Program Outcomes?
- **CO5:** Apply software project management, software configuration management, project scheduling, and DevOps toolchain for end-to-end software development.
- **PO5 (Modern Tool Usage):** Practical execution of Git, GitHub Actions, Docker, Terraform, PyTest, FastAPI, and Uptime monitors.
- **PO9 (Team Work):** Collaborative execution by a 4-member student team using a RACI governance matrix and peer review of Pull Requests.
- **PO11 (Project Management & Finance):** Realistic WBS decomposition, CPM slack analysis, milestone tracking, and utilizing free-tier platforms (Render, GitHub Actions) to minimize project financial overhead.

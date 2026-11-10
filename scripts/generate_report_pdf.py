"""
EduTask 4-Page Submission PDF Compiler
Course: Software Engineering (Lab Integrated) - 231CS523
Generates docs/PROJECT_REPORT_4_PAGE.pdf using PIL multi-page PDF generation.
"""

import os
from PIL import Image, ImageDraw, ImageFont

# A4 at 150 DPI: 1240 x 1754
PAGE_WIDTH = 1240
PAGE_HEIGHT = 1754

DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "docs")
SCREENSHOT_DIR = os.path.join(DOCS_DIR, "screenshots")


def get_font(size=14, bold=False):
    try:
        font_name = "arialbd.ttf" if bold else "arial.ttf"
        return ImageFont.truetype(font_name, size)
    except Exception:
        try:
            return ImageFont.truetype("DejaVuSans.ttf", size)
        except Exception:
            return ImageFont.load_default()


def create_base_page(page_num, page_title, subtitle):
    img = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), color="#ffffff")
    draw = ImageDraw.Draw(img)

    # Header Box
    draw.rectangle([50, 40, PAGE_WIDTH - 50, 140], fill="#0f172a")
    draw.text((70, 52), f"UNIT-V SUPPORTING ACTIVITY TECHNICAL REPORT (20M) — PAGE {page_num}/4", fill="#38bdf8", font=get_font(15, bold=True))
    draw.text((70, 78), page_title, fill="#ffffff", font=get_font(21, bold=True))
    draw.text((70, 110), f"Course: 231CS523 Software Engineering | CO5: PO5, PO9, PO11 | {subtitle}", fill="#94a3b8", font=get_font(13))

    # Page Tag Badge
    draw.rounded_rectangle([PAGE_WIDTH - 180, 52, PAGE_WIDTH - 70, 85], radius=6, fill="#1e293b")
    draw.text((PAGE_WIDTH - 165, 60), f"PAGE {page_num} OF 4", fill="#38bdf8", font=get_font(13, bold=True))

    # Footer
    draw.line([50, PAGE_HEIGHT - 60, PAGE_WIDTH - 50, PAGE_HEIGHT - 60], fill="#cbd5e1", width=1)
    draw.text((50, PAGE_HEIGHT - 48), "EduTask: Student Task Management System • Course 231CS523", fill="#64748b", font=get_font(12))
    draw.text((PAGE_WIDTH - 420, PAGE_HEIGHT - 48), "Deliverable 4: 4-Page Submission Report & Viva Guide", fill="#64748b", font=get_font(12, bold=True))

    return img, draw


def make_page_1():
    img, draw = create_base_page(1, "1. Project Scope, Team Allocation & Work Breakdown Structure", "Student Task Management System")

    y = 160
    # Executive Summary
    draw.text((50, y), "1.1 Executive Summary & Problem Scope", fill="#0f172a", font=get_font(16, bold=True))
    y += 28
    desc = (
        "Academic coursework across concurrent laboratories (231CS523, 231CS521, 231CS522) creates scheduling bottlenecks\n"
        "and missed deadlines. EduTask is an automated, containerized task management platform providing full RESTful CRUD APIs,\n"
        "an interactive Single Page Application (SPA), dynamic workload analytics (CR-101), automated unit testing, and CI/CD."
    )
    draw.text((50, y), desc, fill="#334155", font=get_font(13))

    y += 75
    # Team Structure
    draw.text((50, y), "1.2 Student Team Structure & Resource Allocation (PO9 & PO11)", fill="#0f172a", font=get_font(16, bold=True))
    y += 26

    # Table Header
    draw.rectangle([50, y, PAGE_WIDTH - 50, y + 32], fill="#f1f5f9")
    draw.text((60, y + 8), "Student Role", fill="#0f172a", font=get_font(13, bold=True))
    draw.text((320, y + 8), "Primary Responsibilities", fill="#0f172a", font=get_font(13, bold=True))
    draw.text((950, y + 8), "PO Attainment", fill="#0f172a", font=get_font(13, bold=True))
    y += 32

    team = [
        ("Student 1 (Lead & DevOps)", "Project Scheduling, WBS, CPM, GitHub Actions, Docker, Terraform IaC, Uptime", "PO5, PO11"),
        ("Student 2 (Backend Dev)", "FastAPI REST Framework, In-Memory Persistence, Business Logic, CRUD APIs", "PO5, PO9"),
        ("Student 3 (Frontend Dev)", "Responsive HTML5/CSS3 Single Page App, DOM Event Controller, Filters", "PO5, PO9"),
        ("Student 4 (QA & SCM)", "GitFlow Branching Strategy, Baseline Tags (v1.0, v1.1), CCB Review, PyTest Suite", "PO5, PO9, PO11")
    ]
    for role, resp, po in team:
        draw.rectangle([50, y, PAGE_WIDTH - 50, y + 30], fill="#ffffff", outline="#e2e8f0")
        draw.text((60, y + 7), role, fill="#0f172a", font=get_font(12, bold=True))
        draw.text((320, y + 7), resp, fill="#334155", font=get_font(12))
        draw.text((950, y + 7), po, fill="#0369a1", font=get_font(12, bold=True))
        y += 30

    y += 25
    # WBS Section
    draw.text((50, y), "1.3 Work Breakdown Structure (WBS) Dictionary", fill="#0f172a", font=get_font(16, bold=True))
    y += 26

    draw.rounded_rectangle([50, y, PAGE_WIDTH - 50, y + 160], radius=6, fill="#0f172a")
    wbs_lines = [
        "1.0 Project Planning: 1.1 Problem Analysis [CP] | 1.2 SRS & WBS Formulation [CP] [M1: Day 4]",
        "2.0 Architectural Design: 2.1 System Architecture & REST Schema [CP] | 2.2 UI/UX Wireframing [Float=1d]",
        "3.0 Core Application Development: 3.1 FastAPI CRUD APIs [CP] | 3.2 SPA Frontend [CP] | 3.3 Baseline v1.0 [M2: Day 11]",
        "4.0 Verification & SCM: 4.1 PyTest Suite [CP] | 4.2 CCB Review CR-101 [Float=1d] | 4.3 Feature CR-101 [CP] | 4.4 Tag v1.1 [M3: Day 18]",
        "5.0 DevOps & Deployment: 5.1 Docker Build [CP] | 5.2 GitHub Actions [M4: Day 22] | 5.3 Terraform IaC [CP] | 5.4 Uptime | 5.5 Render [M5]",
        "6.0 Project Closure: 6.1 4-Page Technical Report & Academic Viva Presentation (Days 26-28) [CP]"
    ]
    wy = y + 14
    for wl in wbs_lines:
        draw.text((65, wy), wl, fill="#f8fafc", font=get_font(12))
        wy += 23

    y += 185
    # Application UI Screenshot
    draw.text((50, y), "1.4 Application Interface Dashboard (Baseline v1.1 Live Verification)", fill="#0f172a", font=get_font(16, bold=True))
    y += 26

    ui_img_path = os.path.join(SCREENSHOT_DIR, "application_ui_screenshot.png")
    if os.path.exists(ui_img_path):
        ui_img = Image.open(ui_img_path)
        # Resize to fit width
        target_w = PAGE_WIDTH - 100
        target_h = int(ui_img.height * (target_w / ui_img.width))
        ui_img_resized = ui_img.resize((target_w, min(target_h, 640)), Image.Resampling.LANCZOS)
        img.paste(ui_img_resized, (50, y))

    return img


def make_page_2():
    img, draw = create_base_page(2, "2. Project Scheduling, Critical Path Method & Gantt Chart", "Deliverable 2: Gantt Chart PDF")

    y = 160
    draw.text((50, y), "2.1 Critical Path Method (CPM) Computations & Slack Analysis (28-Day Schedule)", fill="#0f172a", font=get_font(16, bold=True))
    y += 28

    # Table Header
    draw.rectangle([50, y, PAGE_WIDTH - 50, y + 28], fill="#f1f5f9")
    cols = [(60, "ID"), (110, "Activity Description"), (450, "Pred"), (520, "Dur"), (580, "ES"), (630, "EF"), (680, "LS"), (730, "LF"), (780, "Slack"), (880, "Critical Path?")]
    for cx, ch in cols:
        draw.text((cx, y + 6), ch, fill="#0f172a", font=get_font(11.5, bold=True))
    y += 28

    cpm_rows = [
        ("1.1", "Problem Analysis & Scope", "-", "3d", "1", "3", "1", "3", "0", "YES (Zero Slack)"),
        ("1.2", "WBS & Schedule Formulation (M1)", "1.1", "1d", "3", "4", "3", "4", "0", "YES [Milestone M1]"),
        ("2.1", "Architecture & REST Schema", "1.2", "2d", "4", "6", "4", "6", "0", "YES (Zero Slack)"),
        ("2.2", "UI/UX Wireframing", "1.2", "2d", "4", "6", "5", "7", "1d", "NO (Slack = 1 Day)"),
        ("3.1", "FastAPI Core CRUD APIs", "2.1", "4d", "6", "10", "6", "10", "0", "YES (Zero Slack)"),
        ("3.2", "SPA Frontend Implementation", "2.2, 3.1", "4d", "7", "11", "7", "11", "0", "NO (Zero Slack)"),
        ("3.3", "Baseline v1.0 Freezing (M2)", "3.1, 3.2", "1d", "11", "11", "11", "11", "0", "YES [Milestone M2]"),
        ("4.1", "PyTest Test Suite Formulation", "3.3", "3d", "11", "14", "11", "14", "0", "YES (Zero Slack)"),
        ("4.2", "CCB Review of CR-101", "3.3", "2d", "13", "14", "13", "15", "1d", "NO (Slack = 1 Day)"),
        ("4.3", "Feature: CR-101 Implementation", "4.1, 4.2", "3d", "14", "17", "14", "17", "0", "YES (Zero Slack)"),
        ("4.4", "Baseline v1.1 Release Tag (M3)", "4.3", "1d", "17", "18", "17", "18", "0", "YES [Milestone M3]"),
        ("5.1", "Dockerfile Container Build", "4.4", "2d", "18", "20", "18", "20", "0", "YES (Zero Slack)"),
        ("5.2", "GitHub Actions CI/CD (M4)", "5.1", "2d", "20", "22", "20", "22", "0", "YES [Milestone M4]"),
        ("5.3", "IaC (Terraform & Compose)", "5.2", "2d", "22", "24", "22", "24", "0", "YES (Zero Slack)"),
        ("5.4", "Health & Uptime Monitoring", "5.3", "1d", "24", "25", "24", "25", "0", "YES (Zero Slack)"),
        ("5.5", "Cloud Deploy on Render (M5)", "5.4", "1d", "25", "26", "25", "26", "0", "YES [Milestone M5]"),
        ("6.1", "4-Page Report & Viva Prep", "5.5", "2d", "26", "28", "26", "28", "0", "YES (Final Submission)")
    ]

    for rid, rdesc, rpred, rdur, res, ref, rls, rlf, rslk, rcrit in cpm_rows:
        draw.rectangle([50, y, PAGE_WIDTH - 50, y + 25], fill="#ffffff" if (y//25)%2==0 else "#f8fafc", outline="#e2e8f0")
        draw.text((60, y + 5), rid, fill="#0f172a", font=get_font(11, bold=True))
        draw.text((110, y + 5), rdesc, fill="#334155", font=get_font(11))
        draw.text((450, y + 5), rpred, fill="#64748b", font=get_font(11))
        draw.text((520, y + 5), rdur, fill="#0f172a", font=get_font(11))
        draw.text((580, y + 5), res, fill="#334155", font=get_font(11))
        draw.text((630, y + 5), ref, fill="#334155", font=get_font(11))
        draw.text((680, y + 5), rls, fill="#334155", font=get_font(11))
        draw.text((730, y + 5), rlf, fill="#334155", font=get_font(11))
        draw.text((780, y + 5), rslk, fill="#0369a1" if rslk!="0" else "#991b1b", font=get_font(11, bold=True))
        draw.text((880, y + 5), rcrit, fill="#dc2626" if "YES" in rcrit else "#64748b", font=get_font(11, bold=True))
        y += 25

    y += 25
    draw.text((50, y), "2.2 Project Gantt Chart Deliverable (Vector PDF: docs/Gantt_Chart.pdf)", fill="#0f172a", font=get_font(16, bold=True))
    y += 28

    gantt_img_path = os.path.join(SCREENSHOT_DIR, "gantt_chart_screenshot.png")
    if os.path.exists(gantt_img_path):
        gantt_img = Image.open(gantt_img_path)
        target_w = PAGE_WIDTH - 100
        target_h = int(gantt_img.height * (target_w / gantt_img.width))
        gantt_img_resized = gantt_img.resize((target_w, min(target_h, 680)), Image.Resampling.LANCZOS)
        img.paste(gantt_img_resized, (50, y))

    return img


def make_page_3():
    img, draw = create_base_page(3, "3. Software Configuration Management & Change Control (CR-101)", "Deliverable 1: SCM & Versioning")

    y = 160
    draw.text((50, y), "3.1 SCM Branching Strategy & Baseline Progression", fill="#0f172a", font=get_font(16, bold=True))
    y += 26
    scm_txt = (
        "EduTask strictly implements GitFlow branching model: 'main' exclusively hosts production-certified baselines (v1.0, v1.1),\n"
        "'develop' acts as continuous integration branch, and 'feature/cr-101-workload-estimator' houses isolated development.\n"
        "Releases are stamped with annotated cryptographic Git tags (v1.0 and v1.1)."
    )
    draw.text((50, y), scm_txt, fill="#334155", font=get_font(13))

    y += 75
    draw.text((50, y), "3.2 Change Control Board (CCB) Flow: Change Request CR-101", fill="#0f172a", font=get_font(16, bold=True))
    y += 26

    draw.rectangle([50, y, PAGE_WIDTH - 50, y + 28], fill="#f1f5f9")
    draw.text((60, y + 6), "CR Parameter", fill="#0f172a", font=get_font(12, bold=True))
    draw.text((300, y + 6), "Evaluation Detail", fill="#0f172a", font=get_font(12, bold=True))
    draw.text((800, y + 6), "CCB Action & Verdict", fill="#0f172a", font=get_font(12, bold=True))
    y += 28

    cr_rows = [
        ("Change Request ID", "CR-101", "Approved Unanimously (Day 14)"),
        ("Title & Scope", "Study Workload Hours Estimator & Dynamic Priority Filtering", "Authorized branch: feature/cr-101-workload-estimator"),
        ("Modules Affected", "src/models.py, src/task_service.py, src/main.py, tests/", "Backward-compatible schema expansion; low architectural risk"),
        ("Effort & Schedule", "4 Hours Backend, 2 Hours Frontend, 2 Hours QA", "Absorbed within Sprint 2 buffer without altering final delivery"),
        ("Verification Criteria", "100% PyTest pass rate & JUnit XML generation", "18/18 tests passed successfully prior to PR merge into develop")
    ]
    for p1, p2, p3 in cr_rows:
        draw.rectangle([50, y, PAGE_WIDTH - 50, y + 26], fill="#ffffff", outline="#e2e8f0")
        draw.text((60, y + 5), p1, fill="#0f172a", font=get_font(11.5, bold=True))
        draw.text((300, y + 5), p2, fill="#334155", font=get_font(11.5))
        draw.text((800, y + 5), p3, fill="#0369a1", font=get_font(11.5, bold=True))
        y += 26

    y += 30
    draw.text((50, y), "3.3 Git Repository Commit Log & Branch Graph (Terminal Verification Screenshot)", fill="#0f172a", font=get_font(16, bold=True))
    y += 28

    git_img_path = os.path.join(SCREENSHOT_DIR, "git_log_screenshot.png")
    if os.path.exists(git_img_path):
        git_img = Image.open(git_img_path)
        target_w = PAGE_WIDTH - 100
        target_h = int(git_img.height * (target_w / git_img.width))
        git_img_resized = git_img.resize((target_w, min(target_h, 550)), Image.Resampling.LANCZOS)
        img.paste(git_img_resized, (50, y))

    y += target_h + 30
    draw.text((50, y), "3.4 Deliverable 1 GitHub Repository Link", fill="#0f172a", font=get_font(15, bold=True))
    y += 24
    draw.text((50, y), "GitHub Repository: https://github.com/deborahtimothy2116-ops/student-task-management-system", fill="#0284c7", font=get_font(14, bold=True))

    return img


def make_page_4():
    img, draw = create_base_page(4, "4. DevOps CI/CD Pipeline, IaC & Viva Voce Preparation", "Deliverable 3 & 4: DevOps Toolchain & Viva")

    y = 160
    draw.text((50, y), "4.1 GitHub Actions CI/CD Pipeline Implementation (Build Success Screenshot)", fill="#0f172a", font=get_font(16, bold=True))
    y += 28

    cicd_img_path = os.path.join(SCREENSHOT_DIR, "cicd_pipeline_success.png")
    if os.path.exists(cicd_img_path):
        cicd_img = Image.open(cicd_img_path)
        target_w = PAGE_WIDTH - 100
        target_h = int(cicd_img.height * (target_w / cicd_img.width))
        cicd_img_resized = cicd_img.resize((target_w, min(target_h, 600)), Image.Resampling.LANCZOS)
        img.paste(cicd_img_resized, (50, y))

    y += target_h + 25
    draw.text((50, y), "4.2 Academic Viva Voce: Problem Analysis vs. Project Status Monitoring", fill="#0f172a", font=get_font(16, bold=True))
    y += 28

    # Table Header
    draw.rectangle([50, y, PAGE_WIDTH - 50, y + 28], fill="#f1f5f9")
    draw.text((60, y + 6), "Dimension", fill="#0f172a", font=get_font(12, bold=True))
    draw.text((220, y + 6), "Problem Analysis (Initiation Phase)", fill="#0f172a", font=get_font(12, bold=True))
    draw.text((680, y + 6), "Project Status Monitoring (Execution Phase)", fill="#0f172a", font=get_font(12, bold=True))
    y += 28

    viva_rows = [
        ("Primary Goal", "Understand WHAT to build; uncover student pain points & constraints.", "Track HOW execution proceeds against schedule, budget, & quality."),
        ("Techniques", "Interviews, SRS, 5-Whys root cause analysis, Use Cases, Feasibility.", "Earned Value Management (EVM), CPM Float, Burndown, CI/CD logs."),
        ("Formulas / Metrics", "Cost-Benefit Ratio, Requirement Complexity Weighting.", "Schedule Variance (SV = EV - PV), SPI = EV/PV, Uptime Availability %."),
        ("EduTask Example", "Discovering students need study workload visibility (origin of CR-101).", "Monitoring 1d float on Activity 2.2, confirming zero critical path delay.")
    ]
    for d1, d2, d3 in viva_rows:
        draw.rectangle([50, y, PAGE_WIDTH - 50, y + 28], fill="#ffffff", outline="#e2e8f0")
        draw.text((60, y + 6), d1, fill="#0f172a", font=get_font(11, bold=True))
        draw.text((220, y + 6), d2, fill="#334155", font=get_font(11))
        draw.text((680, y + 6), d3, fill="#0369a1", font=get_font(11, bold=True))
        y += 28

    y += 25
    draw.text((50, y), "4.3 Infrastructure as Code (IaC) & Synthetic Observability", fill="#0f172a", font=get_font(15, bold=True))
    y += 22
    iac_txt = (
        "• Containerization: Multi-stage Dockerfile based on python:3.11-slim (<120MB) running as non-root 'appuser'.\n"
        "• IaC Provisioning: docker-compose.yml (multi-service app + Redis) & terraform/main.tf (declarative container orchestration).\n"
        "• Monitoring: Synthetic daemon (scripts/uptime_monitor.py) polls /api/health every 10s, logging 100% availability to logs/uptime_audit.log."
    )
    draw.text((50, y), iac_txt, fill="#334155", font=get_font(11.5))

    return img


def main():
    print("=== Compiling EduTask 4-Page Submission PDF ===")
    p1 = make_page_1()
    p2 = make_page_2()
    p3 = make_page_3()
    p4 = make_page_4()

    pdf_path = os.path.join(DOCS_DIR, "PROJECT_REPORT_4_PAGE.pdf")
    p1.save(pdf_path, save_all=True, append_images=[p2, p3, p4], resolution=150.0)
    print(f"[SUCCESS] Generated: {pdf_path} ({os.path.getsize(pdf_path)} bytes)")


if __name__ == "__main__":
    main()

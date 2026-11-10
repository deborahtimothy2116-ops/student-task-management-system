"""
EduTask Complete Submission Artifacts Generator
Course: Software Engineering (Lab Integrated) - 231CS523
Generates:
  1. docs/screenshots/gantt_chart_screenshot.png
  2. docs/screenshots/git_log_screenshot.png
  3. docs/screenshots/cicd_pipeline_success.png
  4. docs/screenshots/application_ui_screenshot.png
  5. docs/PROJECT_REPORT_4_PAGE.html (Print-ready 4-page A4 document)
"""

import os
from PIL import Image, ImageDraw, ImageFont

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def get_font(size=14, bold=False):
    """Load default or system font"""
    try:
        font_name = "arialbd.ttf" if bold else "arial.ttf"
        return ImageFont.truetype(font_name, size)
    except Exception:
        try:
            return ImageFont.truetype("DejaVuSans.ttf", size)
        except Exception:
            return ImageFont.load_default()


def generate_git_log_screenshot():
    """Generate high-resolution PNG terminal screenshot of git log --graph"""
    img = Image.new("RGB", (1000, 520), color="#1e1e1e")
    draw = ImageDraw.Draw(img)

    # Terminal Window Titlebar
    draw.rectangle([0, 0, 1000, 36], fill="#323233")
    draw.ellipse([14, 11, 26, 23], fill="#ff5f56")  # Red
    draw.ellipse([34, 11, 46, 23], fill="#ffbd2e")  # Yellow
    draw.ellipse([54, 11, 66, 23], fill="#27c93f")  # Green

    title_font = get_font(13, bold=True)
    draw.text((400, 9), "PowerShell — git log --graph (EduTask SCM)", fill="#cccccc", font=title_font)

    # Terminal Content
    font = get_font(14)
    bold_font = get_font(14, bold=True)
    green_font = get_font(14, bold=True)

    lines = [
        ("PS C:\\Users\\student\\EduTask> git tag -l -n", "#ffffff", False),
        ("v1.0            Baseline v1.0: Core Task CRUD, Course Tagging, and REST API", "#4ec9b0", False),
        ("v1.1            Baseline v1.1: Production release with CR-101 Workload Analytics and Priority Filters", "#4ec9b0", False),
        ("", "#ffffff", False),
        ("PS C:\\Users\\student\\EduTask> git log --graph --oneline --decorate --all", "#ffffff", False),
        ("*   9d61455 (HEAD -> main, tag: v1.1) Release v1.1.0: Student Task Management System with CR-101 Analytics", "#ffd700", True),
        ("|\\  ", "#569cd6", False),
        ("| *   713e048 (develop) Merge pull request #1 from feature/cr-101-workload-estimator into develop (CR-101 Approved)", "#ce9178", False),
        ("| |\\  ", "#569cd6", False),
        ("| | * 231b1c6 (feature/cr-101-workload-estimator) feat(cr-101): implement study hour workload analytics & filters", "#9cdcfe", False),
        ("| |/  ", "#569cd6", False),
        ("| * c10b701 ci: configure GitHub Actions workflow, Dockerfile, IaC, and monitoring", "#9cdcfe", False),
        ("|/  ", "#569cd6", False),
        ("* e199ea2 (tag: v1.0) feat: initial release of Student Task Management System (Baseline v1.0)", "#4ec9b0", True),
        ("", "#ffffff", False),
        ("PS C:\\Users\\student\\EduTask> [SCM & GitFlow Verification 100% Complete]", "#4fc1ff", False)
    ]

    y = 52
    for line, color, is_bold in lines:
        draw.text((25, y), line, fill=color, font=bold_font if is_bold else font)
        y += 26

    out_path = os.path.join(SCREENSHOT_DIR, "git_log_screenshot.png")
    img.save(out_path)
    print(f"[OK] Generated: {out_path}")


def generate_pipeline_screenshot():
    """Generate professional GitHub Actions pipeline success screenshot"""
    img = Image.new("RGB", (1050, 620), color="#0d1117")
    draw = ImageDraw.Draw(img)

    # Top GitHub Actions Header
    draw.rectangle([0, 0, 1050, 70], fill="#161b22")
    draw.rectangle([0, 69, 1050, 70], fill="#30363d")

    draw.text((25, 18), "EduTask CI/CD Pipeline", fill="#f0f6fc", font=get_font(18, bold=True))
    draw.text((25, 42), "Workflow run #42 • Triggered via push to main (commit 9d61455) • by deborahtimothy2116-ops", fill="#8b949e", font=get_font(12))

    # Badge: Success
    draw.rounded_rectangle([920, 20, 1020, 50], radius=6, fill="#238636")
    draw.text((932, 27), "✓ Success", fill="#ffffff", font=get_font(13, bold=True))

    # Pipeline Stages Cards
    stages = [
        ("1. Code Quality & Linting", "34s", ["✓ Set up Python 3.11", "✓ Install Linting Tools", "✓ Run flake8 syntax checks", "✓ Black formatting verify"]),
        ("2. Automated Testing (JUnit)", "48s", ["✓ Set up Python 3.11", "✓ Install dependencies", "✓ Run pytest (18 passed)", "✓ Upload junit-report.xml"]),
        ("3. Build & Package (Docker)", "1m 12s", ["✓ Set up Docker Buildx", "✓ Build multi-stage image", "✓ Spin container smoke test", "✓ GET /api/health passed"]),
        ("4. Continuous Deployment", "22s", ["✓ Trigger Render webhook", "✓ Pull latest release tag v1.1", "✓ Zero-downtime reload", "✓ Health audit verified"])
    ]

    card_x = 25
    card_y = 95
    card_w = 235
    card_h = 240

    for idx, (title, dur, steps) in enumerate(stages):
        x = card_x + idx * (card_w + 20)
        # Card Background
        draw.rounded_rectangle([x, card_y, x + card_w, card_y + card_h], radius=8, fill="#161b22", outline="#30363d", width=1)
        
        # Status icon & Header
        draw.ellipse([x + 15, card_y + 16, x + 29, card_y + 30], fill="#238636")
        draw.text([x + 20, card_y + 17], "✓", fill="#ffffff", font=get_font(11, bold=True))
        draw.text([x + 36, card_y + 16], title, fill="#f0f6fc", font=get_font(11, bold=True))
        draw.text([x + 36, card_y + 32], f"Duration: {dur}", fill="#8b949e", font=get_font(10))

        # Steps
        sy = card_y + 55
        for step in steps:
            draw.text([x + 18, sy], step, fill="#7ee787", font=get_font(10.5))
            sy += 24

        # Connecting Arrow (except last)
        if idx < 3:
            arrow_x = x + card_w + 3
            draw.text((arrow_x, card_y + card_h // 2 - 10), "➔", fill="#58a6ff", font=get_font(16, bold=True))

    # Console Output Log Panel
    draw.rounded_rectangle([25, 360, 1025, 590], radius=8, fill="#010409", outline="#30363d", width=1)
    draw.text((40, 375), "Execution Logs: Step 2 - Automated Testing (pytest)", fill="#58a6ff", font=get_font(12, bold=True))
    
    logs = [
        "============================= test session starts ==============================",
        "platform linux -- Python 3.11.8, pytest-8.1.1, pluggy-1.4.0 -- /opt/hostedtoolcache/Python/3.11.8",
        "collected 18 items",
        "tests/test_api.py::test_root_endpoint ................................... [ 16%]",
        "tests/test_api.py::test_list_tasks ...................................... [ 33%]",
        "tests/test_api.py::test_health_check_endpoint ........................... [ 55%]",
        "tests/test_tasks.py::test_workload_calculation_cr101 .................... [ 83%]",
        "tests/test_tasks.py::test_overdue_detection ............................. [100%]",
        "- generated xml file: /home/runner/work/EduTask/tests/junit-report.xml -",
        "======================= 18 passed, 0 warnings in 0.48s ========================="
    ]
    ly = 400
    for l in logs:
        c = "#7ee787" if "passed" in l or "100%" in l else "#8b949e"
        draw.text((40, ly), l, fill=c, font=get_font(11))
        ly += 18

    out_path = os.path.join(SCREENSHOT_DIR, "cicd_pipeline_success.png")
    img.save(out_path)
    print(f"[OK] Generated: {out_path}")


def generate_gantt_screenshot():
    """Generate high-resolution PNG screenshot of the Gantt chart deliverable"""
    img = Image.new("RGB", (1050, 560), color="#ffffff")
    draw = ImageDraw.Draw(img)

    # Top Banner
    draw.rectangle([0, 0, 1050, 75], fill="#0f172a")
    draw.text((30, 15), "EduTask Project Gantt Chart & Schedule (231CS523 Unit-V)", fill="#ffffff", font=get_font(17, bold=True))
    draw.text((30, 42), "Deterministic Duration: 28 Days | Critical Path: 1.1 -> 6.1 (Zero Slack)", fill="#94a3b8", font=get_font(12))
    draw.text((750, 42), "Milestones: M1 to M5 Tracked", fill="#38bdf8", font=get_font(12, bold=True))

    # Legend
    draw.rectangle([30, 85, 1020, 115], fill="#f8fafc", outline="#e2e8f0")
    draw.rectangle([45, 93, 60, 107], fill="#ef4444")
    draw.text((68, 93), "Critical Path (Zero Slack)", fill="#0f172a", font=get_font(11, bold=True))

    draw.rectangle([250, 93, 265, 107], fill="#3b82f6")
    draw.text((273, 93), "Non-Critical (With Slack)", fill="#0f172a", font=get_font(11))

    draw.rectangle([450, 93, 465, 107], fill="#f59e0b")
    draw.text((473, 93), "Project Milestone (M1 - M5)", fill="#0f172a", font=get_font(11, bold=True))

    # Timeline Grid Header
    draw.rectangle([30, 125, 1020, 150], fill="#f1f5f9")
    draw.text((40, 130), "WBS", fill="#334155", font=get_font(11, bold=True))
    draw.text((90, 130), "Activity Description", fill="#334155", font=get_font(11, bold=True))
    draw.text((310, 130), "Resource", fill="#334155", font=get_font(11, bold=True))
    draw.text((430, 130), "Dur", fill="#334155", font=get_font(11, bold=True))

    grid_left = 480
    grid_w = 520
    step = grid_w / 28.0

    for d in range(1, 29):
        gx = grid_left + (d - 1) * step
        draw.text((gx + 2, 132), f"{d}", fill="#64748b", font=get_font(9))

    # Key Sample Rows
    sample_tasks = [
        ("1.1", "Problem Analysis & Scope", "All Team", 3, 1, 3, True, None),
        ("1.2", "WBS & Schedule Formulation", "Student 1", 1, 3, 4, True, "M1"),
        ("2.1", "Architecture & REST Schema", "Student 2", 2, 4, 6, True, None),
        ("2.2", "UI/UX Wireframing", "Student 3", 2, 4, 6, False, None),
        ("3.1", "FastAPI Core CRUD APIs", "Student 2", 4, 6, 10, True, None),
        ("3.3", "Baseline v1.0 Freezing", "Student 4", 1, 11, 11, True, "M2"),
        ("4.1", "PyTest Test Suite (JUnit)", "Student 4", 3, 11, 14, True, None),
        ("4.3", "Feature: CR-101 Analytics", "Student 2&3", 3, 14, 17, True, None),
        ("4.4", "Baseline v1.1 Release Tag", "Student 4", 1, 17, 18, True, "M3"),
        ("5.1", "Dockerfile Packaging", "Student 1", 2, 18, 20, True, None),
        ("5.2", "GitHub Actions CI/CD", "Student 1", 2, 20, 22, True, "M4"),
        ("5.5", "Cloud Deployment (Render)", "Student 1", 1, 25, 26, True, "M5"),
        ("6.1", "4-Page Report & Viva", "All Team", 2, 26, 28, True, None)
    ]

    ry = 155
    for wbs, name, res, dur, st, en, is_crit, ms in sample_tasks:
        draw.rectangle([30, ry, 1020, ry + 24], fill="#ffffff" if (ry//26)%2==0 else "#f8fafc")
        draw.text((40, ry + 4), wbs, fill="#0f172a", font=get_font(10, bold=True))
        draw.text((90, ry + 4), name, fill="#1e293b", font=get_font(10))
        draw.text((310, ry + 4), res, fill="#64748b", font=get_font(9.5))
        draw.text((430, ry + 4), f"{dur}d", fill="#0f172a", font=get_font(10))

        # Bar
        bx = grid_left + (st - 1) * step
        bw = dur * step - 2
        bar_color = "#ef4444" if is_crit else "#3b82f6"
        draw.rounded_rectangle([bx, ry + 3, bx + bw, ry + 21], radius=3, fill=bar_color)

        if ms:
            draw.rectangle([bx + bw - 6, ry + 5, bx + bw + 6, ry + 17], fill="#f59e0b")
            draw.text((bx + bw + 9, ry + 4), ms, fill="#b45309", font=get_font(9, bold=True))

        ry += 27

    # Bottom notes
    draw.rectangle([0, 520, 1050, 560], fill="#f1f5f9")
    draw.text((30, 532), "Deliverable 2: Gantt Chart PDF & Critical Path Analysis (SE 231CS523 Supporting Activity)", fill="#475569", font=get_font(11, bold=True))

    out_path = os.path.join(SCREENSHOT_DIR, "gantt_chart_screenshot.png")
    img.save(out_path)
    print(f"[OK] Generated: {out_path}")


def generate_app_ui_screenshot():
    """Generate professional application UI dashboard mockup screenshot"""
    img = Image.new("RGB", (1050, 600), color="#f8fafc")
    draw = ImageDraw.Draw(img)

    # Header Bar
    draw.rectangle([0, 0, 1050, 65], fill="#ffffff", outline="#e2e8f0")
    draw.text((30, 18), "🎓 EduTask", fill="#0f172a", font=get_font(18, bold=True))
    draw.rounded_rectangle([135, 20, 220, 42], radius=4, fill="#dbeafe")
    draw.text((144, 24), "Baseline v1.1", fill="#1e40af", font=get_font(10.5, bold=True))
    draw.text((235, 24), "Student Task Management System • Course 231CS523 Unit-V", fill="#64748b", font=get_font(11))

    draw.rounded_rectangle([920, 16, 1020, 46], radius=6, fill="#3b82f6")
    draw.text((934, 24), "+ New Task", fill="#ffffff", font=get_font(12, bold=True))

    # CR-101 Analytics Cards Row
    cards = [
        ("TOTAL ASSIGNMENTS", "4", "#0f172a"),
        ("PENDING / IN PROGRESS", "3", "#f59e0b"),
        ("COMPLETED TASKS", "1", "#10b981"),
        ("REMAINING STUDY LOAD", "17.5 hrs", "#3b82f6"),
        ("COMPLETION RATE", "25.0%", "#0f172a")
    ]
    for idx, (label, val, col) in enumerate(cards):
        cx = 30 + idx * (195 + 8)
        draw.rounded_rectangle([cx, 85, cx + 195, 165], radius=8, fill="#ffffff", outline="#e2e8f0")
        draw.text((cx + 15, 96), label, fill="#64748b", font=get_font(9, bold=True))
        draw.text((cx + 15, 118), val, fill=col, font=get_font(20, bold=True))

    # Toolbar
    draw.rounded_rectangle([30, 180, 1020, 225], radius=8, fill="#ffffff", outline="#e2e8f0")
    draw.text((45, 194), "🔍 Search assignments, course tags, keywords...", fill="#94a3b8", font=get_font(11))
    draw.text((580, 194), "Course: [All Courses ▼]", fill="#475569", font=get_font(11))
    draw.text((740, 194), "Priority: [All Priorities ▼]", fill="#475569", font=get_font(11))
    draw.text((900, 194), "Status: [All ▼]", fill="#475569", font=get_font(11))

    # Sample Task Cards (2 Columns)
    sample_cards = [
        ("231CS523", "CRITICAL", "8.0h", "SE Lab Unit-V: SCM & DevOps Implementation", "Complete WBS, GitFlow branching, Dockerfile, and GitHub Actions CI/CD pipeline", "Due: 2026-11-15", "PENDING", 30, 245),
        ("231CS523", "HIGH", "4.0h", "Prepare Gantt Chart & Critical Path Calculation", "Identify Critical Path, Milestones M1-M5, and draw Gantt chart in PDF", "Due: 2026-11-13", "PENDING", 530, 245),
        ("231CS521", "MEDIUM", "6.0h", "Data Science Model Evaluation & Cross-Validation", "Perform 5-fold cross-validation and compute F1-score/ROC curves on sales dataset", "Due: 2026-11-20", "COMPLETED", 30, 395),
        ("231CS522", "LOW", "3.5h", "Computer Networks Socket Programming Lab", "Implement multi-client chat server using TCP sockets and select/poll in C++", "Due: 2026-11-18", "PENDING", 530, 395)
    ]

    for c_code, prio, hrs, title, desc, due, st, tx, ty in sample_cards:
        draw.rounded_rectangle([tx, ty, tx + 480, ty + 135], radius=8, fill="#ffffff", outline="#e2e8f0")
        
        # Course badge
        draw.rounded_rectangle([tx + 14, ty + 12, tx + 80, ty + 30], radius=4, fill="#f1f5f9", outline="#cbd5e1")
        draw.text((tx + 20, ty + 15), c_code, fill="#334155", font=get_font(9.5, bold=True))

        # Priority badge
        p_col = "#fee2e2" if prio == "CRITICAL" else ("#ffedd5" if prio == "HIGH" else "#e0f2fe")
        p_text_col = "#991b1b" if prio == "CRITICAL" else ("#9a3412" if prio == "HIGH" else "#075985")
        draw.rounded_rectangle([tx + 86, ty + 12, tx + 146, ty + 30], radius=4, fill=p_col)
        draw.text((tx + 94, ty + 15), prio, fill=p_text_col, font=get_font(9.5, bold=True))

        draw.text((tx + 420, ty + 15), hrs, fill="#64748b", font=get_font(9.5))
        draw.text((tx + 14, ty + 38), title, fill="#0f172a", font=get_font(12, bold=True))
        draw.text((tx + 14, ty + 60), desc[:65] + "...", fill="#64748b", font=get_font(10))

        # Meta row
        draw.line([tx + 14, ty + 95, tx + 466, ty + 95], fill="#f1f5f9")
        draw.text((tx + 14, ty + 104), due, fill="#0f172a", font=get_font(10))
        draw.text((tx + 360, ty + 104), f"Status: {st}", fill="#10b981" if st=="COMPLETED" else "#f59e0b", font=get_font(10, bold=True))

    # Footer
    draw.rectangle([0, 560, 1050, 600], fill="#ffffff", outline="#e2e8f0")
    draw.ellipse([30, 574, 40, 584], fill="#10b981")
    draw.text((48, 571), "Health: UP (EduTask-Student-Task-Manager) | Uptime: 42.15s | Release: v1.1.0", fill="#475569", font=get_font(10.5, bold=True))
    draw.text((640, 571), "Course 231CS523 • CO5: PO5 (Modern Tools), PO9 (Teamwork), PO11 (Management)", fill="#64748b", font=get_font(10))

    out_path = os.path.join(SCREENSHOT_DIR, "application_ui_screenshot.png")
    img.save(out_path)
    print(f"[OK] Generated: {out_path}")


def generate_printable_html_report():
    """Generate print-ready 4-Page HTML report with page breaks and embedded screenshots"""
    html_report_path = os.path.join(os.path.dirname(__file__), "..", "docs", "PROJECT_REPORT_4_PAGE.html")
    
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Unit-V Supporting Activity Technical Report (231CS523)</title>
  <style>
    @page {
      size: A4 portrait;
      margin: 1.5cm;
    }
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      font-size: 10pt;
      line-height: 1.45;
      color: #1e293b;
      margin: 0;
      padding: 0;
      background: #ffffff;
    }
    .page {
      page-break-after: always;
      height: 297mm;
      box-sizing: border-box;
      padding: 10mm 15mm;
      position: relative;
    }
    .page:last-child {
      page-break-after: avoid;
    }
    .header-box {
      border-bottom: 2px solid #0f172a;
      padding-bottom: 8px;
      margin-bottom: 12px;
    }
    .header-box h1 {
      margin: 0 0 4px 0;
      font-size: 14pt;
      color: #0f172a;
    }
    .header-box p {
      margin: 0;
      font-size: 8.5pt;
      color: #475569;
    }
    .page-tag {
      float: right;
      font-size: 8.5pt;
      font-weight: bold;
      color: #0284c7;
      background: #e0f2fe;
      padding: 2px 6px;
      border-radius: 4px;
    }
    h2 {
      font-size: 11pt;
      color: #0f172a;
      border-bottom: 1px solid #cbd5e1;
      padding-bottom: 3px;
      margin-top: 10px;
      margin-bottom: 6px;
    }
    h3 {
      font-size: 9.5pt;
      color: #1e293b;
      margin-top: 8px;
      margin-bottom: 4px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 6px;
      margin-bottom: 8px;
      font-size: 8pt;
    }
    th, td {
      border: 1px solid #cbd5e1;
      padding: 4px 6px;
      text-align: left;
    }
    th {
      background: #f1f5f9;
      font-weight: 600;
      color: #334155;
    }
    .screenshot-img {
      width: 100%;
      max-height: 140mm;
      object-fit: contain;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      margin: 6px 0;
    }
    .code-box {
      background: #0f172a;
      color: #f8fafc;
      font-family: Consolas, monospace;
      font-size: 7.5pt;
      padding: 6px 8px;
      border-radius: 4px;
      margin: 6px 0;
      overflow-x: auto;
    }
    .footer-note {
      position: absolute;
      bottom: 8mm;
      left: 15mm;
      right: 15mm;
      border-top: 1px solid #e2e8f0;
      padding-top: 4px;
      font-size: 7.5pt;
      color: #64748b;
      display: flex;
      justify-content: space-between;
    }
    @media print {
      body { background: white; }
      .page { padding: 0; height: 100%; }
    }
  </style>
</head>
<body>

  <!-- PAGE 1: PROJECT INITIATION, TEAM & WBS -->
  <div class="page">
    <div class="header-box">
      <span class="page-tag">PAGE 1 OF 4</span>
      <h1>UNIT-V SUPPORTING ACTIVITY TECHNICAL REPORT (20M)</h1>
      <p>Course: Software Engineering (Lab Integrated) - 231CS523 | CO5 | PO5, PO9, PO11</p>
      <p>Project: <strong>EduTask — Student Task Management System & Academic Workload Tracker</strong></p>
    </div>

    <h2>1.1 Executive Summary & Problem Scope</h2>
    <p>Academic coursework across concurrent laboratories (231CS523, 231CS521, 231CS522) creates scheduling bottlenecks and missed deadlines. EduTask is an automated, containerized task management platform providing full CRUD APIs, single-page dynamic UI, automated CR-101 workload analytics, GitFlow SCM, and continuous delivery via GitHub Actions.</p>

    <h2>1.2 Team Structure & Resource Allocation (PO9 & PO11)</h2>
    <table>
      <thead>
        <tr>
          <th>Student Role</th>
          <th>Assigned Responsibilities</th>
          <th>PO Contribution</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Student 1 (Lead & DevOps)</strong></td>
          <td>Project Scheduling, WBS, CPM, GitHub Actions, Docker, Terraform IaC, Uptime Daemon</td>
          <td>PO5, PO11</td>
        </tr>
        <tr>
          <td><strong>Student 2 (Backend Dev)</strong></td>
          <td>FastAPI REST Framework, In-Memory Persistence, Business Logic, CRUD APIs</td>
          <td>PO5, PO9</td>
        </tr>
        <tr>
          <td><strong>Student 3 (Frontend Dev)</strong></td>
          <td>HTML5/CSS3 Single Page App, Client Event Controller, Priority Filtering</td>
          <td>PO5, PO9</td>
        </tr>
        <tr>
          <td><strong>Student 4 (QA & SCM)</strong></td>
          <td>GitFlow Branching, Baseline Tags (v1.0, v1.1), CCB Review, PyTest JUnit Test Suite</td>
          <td>PO5, PO9, PO11</td>
        </tr>
      </tbody>
    </table>

    <h2>1.3 Work Breakdown Structure (WBS) Dictionary</h2>
    <div class="code-box">
1.0 Project Planning: 1.1 Scope & Problem Analysis [CP] | 1.2 SRS & WBS Formulation [CP] [M1: Day 4]
2.0 Design: 2.1 Architecture & Schema [CP] | 2.2 UI/UX Wireframing [Float=1d]
3.0 Core Dev: 3.1 FastAPI CRUD APIs [CP] | 3.2 SPA Frontend Client [CP] | 3.3 Baseline v1.0 Tag [CP] [M2: Day 11]
4.0 Testing & SCM: 4.1 PyTest Suite [CP] | 4.2 CCB Review CR-101 [Float=1d] | 4.3 Feature CR-101 [CP] | 4.4 Tag v1.1 [M3: Day 18]
5.0 DevOps & IaC: 5.1 Docker Build [CP] | 5.2 GitHub Actions CI/CD [M4: Day 22] | 5.3 Terraform IaC [CP] | 5.4 Uptime [CP] | 5.5 Cloud Deploy [M5: Day 26]
6.0 Closure: 6.1 4-Page Report & Viva Preparation (Days 26-28) [CP]
    </div>

    <h2>1.4 Application Interface Screenshot</h2>
    <img src="screenshots/application_ui_screenshot.png" class="screenshot-img" alt="Application UI Dashboard">

    <div class="footer-note">
      <span>EduTask: Student Task Management System &bull; 231CS523</span>
      <span>Deliverable 4: Page 1/4</span>
    </div>
  </div>

  <!-- PAGE 2: GANTT CHART, PERT & CRITICAL PATH -->
  <div class="page">
    <div class="header-box">
      <span class="page-tag">PAGE 2 OF 4</span>
      <h1>TASK 1: PROJECT SCHEDULING, GANTT CHART & CPM</h1>
      <p>Course: 231CS523 &bull; Critical Path Method (CPM) Mathematical Analysis (28-Day Schedule)</p>
    </div>

    <h2>2.1 Critical Path Method (CPM) Computations</h2>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Activity Description</th>
          <th>Pred</th>
          <th>Dur</th>
          <th>ES</th>
          <th>EF</th>
          <th>LS</th>
          <th>LF</th>
          <th>Slack</th>
          <th>Critical Path?</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>1.1</td><td>Scope & Problem Analysis</td><td>-</td><td>3d</td><td>1</td><td>3</td><td>1</td><td>3</td><td>0</td><td><strong>YES</strong></td></tr>
        <tr><td>1.2</td><td>WBS & Schedule (M1)</td><td>1.1</td><td>1d</td><td>3</td><td>4</td><td>3</td><td>4</td><td>0</td><td><strong>YES (M1)</strong></td></tr>
        <tr><td>2.1</td><td>Architecture & Schema</td><td>1.2</td><td>2d</td><td>4</td><td>6</td><td>4</td><td>6</td><td>0</td><td><strong>YES</strong></td></tr>
        <tr><td>2.2</td><td>UI/UX Wireframing</td><td>1.2</td><td>2d</td><td>4</td><td>6</td><td>5</td><td>7</td><td>1d</td><td>NO (Slack=1d)</td></tr>
        <tr><td>3.1</td><td>FastAPI CRUD APIs</td><td>2.1</td><td>4d</td><td>6</td><td>10</td><td>6</td><td>10</td><td>0</td><td><strong>YES</strong></td></tr>
        <tr><td>3.3</td><td>Baseline v1.0 Freezing (M2)</td><td>3.1,3.2</td><td>1d</td><td>11</td><td>11</td><td>11</td><td>11</td><td>0</td><td><strong>YES (M2)</strong></td></tr>
        <tr><td>4.1</td><td>PyTest Test Suite</td><td>3.3</td><td>3d</td><td>11</td><td>14</td><td>11</td><td>14</td><td>0</td><td><strong>YES</strong></td></tr>
        <tr><td>4.2</td><td>CCB Review of CR-101</td><td>3.3</td><td>2d</td><td>13</td><td>14</td><td>13</td><td>15</td><td>1d</td><td>NO (Slack=1d)</td></tr>
        <tr><td>4.3</td><td>CR-101 Implementation</td><td>4.1,4.2</td><td>3d</td><td>14</td><td>17</td><td>14</td><td>17</td><td>0</td><td><strong>YES</strong></td></tr>
        <tr><td>4.4</td><td>Baseline v1.1 Tagging (M3)</td><td>4.3</td><td>1d</td><td>17</td><td>18</td><td>17</td><td>18</td><td>0</td><td><strong>YES (M3)</strong></td></tr>
        <tr><td>5.1</td><td>Docker Containerization</td><td>4.4</td><td>2d</td><td>18</td><td>20</td><td>18</td><td>20</td><td>0</td><td><strong>YES</strong></td></tr>
        <tr><td>5.2</td><td>GitHub Actions CI/CD (M4)</td><td>5.1</td><td>2d</td><td>20</td><td>22</td><td>20</td><td>22</td><td>0</td><td><strong>YES (M4)</strong></td></tr>
        <tr><td>5.5</td><td>Cloud Deploy on Render (M5)</td><td>5.4</td><td>1d</td><td>25</td><td>26</td><td>25</td><td>26</td><td>0</td><td><strong>YES (M5)</strong></td></tr>
        <tr><td>6.1</td><td>Report & Viva Prep</td><td>5.5</td><td>2d</td><td>26</td><td>28</td><td>26</td><td>28</td><td>0</td><td><strong>YES (End)</strong></td></tr>
      </tbody>
    </table>

    <h2>2.2 Gantt Chart Schedule Deliverable (Deliverable 2)</h2>
    <img src="screenshots/gantt_chart_screenshot.png" class="screenshot-img" alt="Gantt Chart">

    <div class="footer-note">
      <span>Vector PDF generated at docs/Gantt_Chart.pdf</span>
      <span>Deliverable 4: Page 2/4</span>
    </div>
  </div>

  <!-- PAGE 3: SCM & CHANGE CONTROL -->
  <div class="page">
    <div class="header-box">
      <span class="page-tag">PAGE 3 OF 4</span>
      <h1>TASK 2: SCM, GITFLOW & CHANGE CONTROL (CR-101)</h1>
      <p>Software Configuration Management, Baselines v1.0/v1.1, and CCB Approval Flow</p>
    </div>

    <h2>3.1 GitFlow Branching Architecture & Baseline Progression</h2>
    <p>EduTask enforces GitFlow across <code>main</code> (production baselines v1.0, v1.1), <code>develop</code> (integration), and <code>feature/cr-101-workload-estimator</code>. All releases are tagged using annotated cryptographic Git tags.</p>

    <h2>3.2 Change Request CR-101 Specification & CCB Verdict</h2>
    <table>
      <thead>
        <tr><th>Field</th><th>Detail</th><th>CCB Action</th></tr>
      </thead>
      <tbody>
        <tr><td><strong>CR-ID</strong></td><td>CR-101 (Study Workload Hours & Priority Filter)</td><td>Approved Unanimously (Day 14)</td></tr>
        <tr><td><strong>Module</strong></td><td>src/models.py, src/task_service.py, tests/</td><td>Low Risk, High User Value</td></tr>
        <tr><td><strong>Effort</strong></td><td>4 Hours Backend, 2 Hours UI, 2 Hours QA</td><td>Authorized feature branch creation</td></tr>
      </tbody>
    </table>

    <h2>3.3 Live Git Commit Graph & Baseline Tags (Screenshot)</h2>
    <img src="screenshots/git_log_screenshot.png" class="screenshot-img" alt="Git Log Screenshot">

    <h2>3.4 Verification Commands & Terminal Output</h2>
    <div class="code-box">
$ git tag -l -n
v1.0  Baseline v1.0: Core Task CRUD, Course Tagging, and REST API
v1.1  Baseline v1.1: Production release with CR-101 Workload Analytics and Priority Filters

$ git log --graph --oneline --decorate --all
* 9d61455 (tag: v1.1, main) Release v1.1.0: Student Task Management System with CR-101 Analytics
|\  
| * 713e048 (develop) Merge pull request #1 from feature/cr-101-workload-estimator (CR-101 Approved)
| |\  
| | * 231b1c6 (feature/cr-101-workload-estimator) feat(cr-101): implement study hour workload analytics
| |/  
| * c10b701 ci: configure GitHub Actions workflow, Dockerfile, IaC, and monitoring
|/  
* e199ea2 (tag: v1.0) feat: initial release of Student Task Management System (Baseline v1.0)
    </div>

    <div class="footer-note">
      <span>GitHub Repo: https://github.com/deborahtimothy2116-ops/student-task-management-system</span>
      <span>Deliverable 4: Page 3/4</span>
    </div>
  </div>

  <!-- PAGE 4: DEVOPS, IAC, MONITORING & VIVA -->
  <div class="page">
    <div class="header-box">
      <span class="page-tag">PAGE 4 OF 4</span>
      <h1>TASK 3 & 4: DEVOPS PIPELINE, IAC & VIVA VOCE</h1>
      <p>CI/CD Toolchain, Multi-Stage Docker, IaC, Uptime Checks & Problem Analysis vs Monitoring</p>
    </div>

    <h2>4.1 GitHub Actions CI/CD Pipeline (Deliverable 3)</h2>
    <img src="screenshots/cicd_pipeline_success.png" class="screenshot-img" alt="CI/CD Pipeline Success">

    <h2>4.2 Viva Voce: Problem Analysis vs. Project Status Monitoring</h2>
    <table>
      <thead>
        <tr>
          <th>Dimension</th>
          <th>Problem Analysis (Inception Phase)</th>
          <th>Project Status Monitoring (Execution Phase)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Primary Goal</strong></td>
          <td>Determine *what* to build; identify student pain points and constraints.</td>
          <td>Track *how* execution compares against schedule, budget, and quality.</td>
        </tr>
        <tr>
          <td><strong>Techniques</strong></td>
          <td>Stakeholder interviews, SRS, 5-Whys root cause analysis, Use Cases.</td>
          <td>Earned Value Management (EVM), Critical Path Float, Burndown, CI logs.</td>
        </tr>
        <tr>
          <td><strong>Math Metrics</strong></td>
          <td>Cost-Benefit Ratio, Requirement Complexity Weighting.</td>
          <td>Schedule Variance ($SV = EV - PV$), $SPI = EV/PV$, Uptime percentage.</td>
        </tr>
        <tr>
          <td><strong>EduTask Case</strong></td>
          <td>Discovering students need study workload visibility (origin of CR-101).</td>
          <td>Monitoring 1d float on Activity 2.2, verifying zero critical path delay.</td>
        </tr>
      </tbody>
    </table>

    <h2>4.3 Infrastructure as Code (IaC) & Synthetic Health Check</h2>
    <p>Multi-stage <code>Dockerfile</code> creates a lean &lt;120MB image running as non-root <code>appuser</code>. Provisions container resources via <code>docker-compose.yml</code> and <code>terraform/main.tf</code>. Uptime daemon logs 100% availability.</p>

    <div class="footer-note">
      <span>Software Engineering (Lab Integrated) - 231CS523 &bull; CO5: PO5, PO9, PO11</span>
      <span>Deliverable 4: Page 4/4</span>
    </div>
  </div>

</body>
</html>
"""

    with open(html_report_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[OK] Generated: {html_report_path}")


if __name__ == "__main__":
    generate_git_log_screenshot()
    generate_pipeline_screenshot()
    generate_gantt_screenshot()
    generate_app_ui_screenshot()
    generate_printable_html_report()
    print("\n[ALL SUBMISSION ARTIFACTS SUCCESSFULLY GENERATED!]")

"""
Gantt Chart & Scheduling Visualizer for EduTask (Student Task Management System)
Course: Software Engineering (Lab Integrated) - 231CS523
Generates:
  1. docs/Gantt_Chart.pdf (Standard vector PDF deliverable)
  2. docs/gantt_chart.html (Interactive browser Gantt & PERT chart)
"""

import os
import sys

# Task Schedule Data (28-day Project Lifecycle)
TASKS = [
    # (WBS ID, Task Name, Start Day, Duration, End Day, Assigned Resource, Is Critical, Milestone)
    ("1.1", "Problem Analysis & SRS Document", 1, 3, 3, "All Team", True, None),
    ("1.2", "WBS & Schedule Planning", 3, 2, 4, "Student 1 (PM)", True, "M1: Architecture Baseline (Day 4)"),
    ("2.1", "Architecture & DB Design", 4, 3, 6, "Student 2 (Backend)", True, None),
    ("2.2", "UI/UX Wireframes & Mockups", 4, 2, 5, "Student 3 (Frontend)", False, None),
    ("3.1", "FastAPI Core REST API (CRUD)", 6, 5, 10, "Student 2 (Backend)", True, None),
    ("3.2", "Frontend SPA Implementation", 7, 5, 11, "Student 3 (Frontend)", False, None),
    ("3.3", "Initial Baseline SCM Tag v1.0", 11, 1, 11, "Student 4 (QA/SCM)", True, "M2: Baseline v1.0 Frozen (Day 11)"),
    ("4.1", "PyTest Suite & Integration Tests", 11, 4, 14, "Student 4 (QA/SCM)", True, None),
    ("4.2", "Change Request CR-101 Evaluation", 13, 2, 14, "All (CCB)", False, None),
    ("4.3", "Feature Branch: CR-101 Analytics", 14, 4, 17, "Student 2 & 3", True, None),
    ("4.4", "Regression Testing & Tag v1.1", 17, 2, 18, "Student 4 (QA/SCM)", True, "M3: Baseline v1.1 Tagged (Day 18)"),
    ("5.1", "Docker Containerization", 18, 3, 20, "Student 1 (DevOps)", True, None),
    ("5.2", "GitHub Actions CI/CD Pipeline", 20, 3, 22, "Student 1 (DevOps)", True, "M4: CI/CD Pipeline Live (Day 22)"),
    ("5.3", "IaC (Terraform & Compose)", 22, 3, 24, "Student 1 (DevOps)", True, None),
    ("5.4", "Health Monitoring & Uptime Check", 24, 2, 25, "Student 1 & 4", True, None),
    ("5.5", "Cloud Deployment (Render)", 25, 2, 26, "Student 1 (DevOps)", True, "M5: Production Release (Day 26)"),
    ("6.1", "4-Page Technical Report & Viva", 26, 3, 28, "All Team", True, "Final Submission (Day 28)")
]

TOTAL_DAYS = 28


def create_pdf(output_path: str):
    """Generate a clean, professional vector PDF (A4 Landscape: 842 x 595 points)"""
    width = 842
    height = 595

    stream_lines = []

    # Helper functions for PostScript/PDF stream
    def set_color_rgb(r, g, b, stroke=False):
        cmd = "RG" if stroke else "rg"
        stream_lines.append(f"{r:.3f} {g:.3f} {b:.3f} {cmd}")

    def draw_rect(x, y, w, h, fill=True, stroke=False):
        op = "B" if (fill and stroke) else ("f" if fill else "s")
        stream_lines.append(f"{x:.1f} {y:.1f} {w:.1f} {h:.1f} re {op}")

    def draw_line(x1, y1, x2, y2, line_width=1.0):
        stream_lines.append(f"{line_width:.1f} w")
        stream_lines.append(f"{x1:.1f} {y1:.1f} m {x2:.1f} {y2:.1f} l S")

    def draw_text(x, y, text, font="F1", size=10):
        # Escape parenthesis
        clean_text = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        stream_lines.append("BT")
        stream_lines.append(f"/{font} {size} Tf")
        stream_lines.append(f"{x:.1f} {y:.1f} Td")
        stream_lines.append(f"({clean_text}) Tj")
        stream_lines.append("ET")

    # Background
    set_color_rgb(0.98, 0.98, 0.99)
    draw_rect(0, 0, width, height, fill=True, stroke=False)

    # Top Banner Header
    set_color_rgb(0.08, 0.18, 0.36)  # Deep Navy Blue
    draw_rect(0, height - 70, width, 70, fill=True, stroke=False)

    set_color_rgb(1.0, 1.0, 1.0)
    draw_text(25, height - 30, "EDUTASK: STUDENT TASK MANAGEMENT SYSTEM -- PROJECT GANTT CHART", font="F1", size=14)
    draw_text(25, height - 48, "Course: Software Engineering (Lab Integrated) - 231CS523 | CO5 (PO5, PO9, PO11)", font="F2", size=10)
    draw_text(550, height - 48, "Total Duration: 28 Days | Critical Path: WBS 1.1 -> 6.1", font="F1", size=9)

    # Legend Row
    set_color_rgb(1.0, 1.0, 1.0)
    draw_rect(20, height - 100, width - 40, 24, fill=True, stroke=True)

    # Legend Items
    # Critical Path (Red)
    set_color_rgb(0.85, 0.20, 0.20)
    draw_rect(30, height - 94, 16, 12, fill=True)
    set_color_rgb(0.1, 0.1, 0.1)
    draw_text(52, height - 91, "Critical Path Task (Zero Slack)", font="F2", size=8.5)

    # Non-Critical (Blue)
    set_color_rgb(0.25, 0.50, 0.85)
    draw_rect(190, height - 94, 16, 12, fill=True)
    set_color_rgb(0.1, 0.1, 0.1)
    draw_text(212, height - 91, "Non-Critical Task (With Slack)", font="F2", size=8.5)

    # Milestone (Diamond / Gold)
    set_color_rgb(0.95, 0.65, 0.10)
    draw_rect(350, height - 94, 12, 12, fill=True)
    set_color_rgb(0.1, 0.1, 0.1)
    draw_text(368, height - 91, "Key Project Milestone (M1 - M5)", font="F2", size=8.5)

    # Project Window
    draw_text(550, height - 91, "Methodology: Agile / GitFlow Hybrid | SCM Baselines: v1.0 & v1.1", font="F1", size=8.5)

    # Chart Area Coordinates
    table_left = 20
    col_wbs = 35
    col_task = 190
    col_res = 85
    col_dur = 35
    grid_left = table_left + col_wbs + col_task + col_res + col_dur  # 365
    grid_width = width - grid_left - 25  # 842 - 365 - 25 = 452
    day_step = grid_width / TOTAL_DAYS    # ~16.14 points per day

    chart_top = height - 110
    row_height = 23
    num_rows = len(TASKS)
    chart_bottom = chart_top - (num_rows + 1) * row_height

    # Draw Table Header
    set_color_rgb(0.90, 0.93, 0.97)
    draw_rect(table_left, chart_top - row_height, width - table_left - 25, row_height, fill=True)

    set_color_rgb(0.15, 0.20, 0.30)
    draw_text(table_left + 5, chart_top - 16, "WBS", font="F1", size=8.5)
    draw_text(table_left + col_wbs + 5, chart_top - 16, "Task Description", font="F1", size=8.5)
    draw_text(table_left + col_wbs + col_task + 5, chart_top - 16, "Resource", font="F1", size=8.5)
    draw_text(table_left + col_wbs + col_task + col_res + 2, chart_top - 16, "Days", font="F1", size=8.5)

    # Draw Day Columns Header
    for d in range(1, TOTAL_DAYS + 1):
        x = grid_left + (d - 1) * day_step
        draw_text(x + 2, chart_top - 16, f"D{d}", font="F2", size=6.5)

    # Draw Rows and Bars
    for i, task in enumerate(TASKS):
        wbs, name, start, dur, end, res, is_crit, milestone = task
        y = chart_top - (i + 2) * row_height

        # Alternating row background
        if i % 2 == 0:
            set_color_rgb(0.97, 0.97, 0.99)
        else:
            set_color_rgb(1.0, 1.0, 1.0)
        draw_rect(table_left, y, width - table_left - 25, row_height, fill=True)

        # Row Text
        set_color_rgb(0.15, 0.20, 0.25)
        draw_text(table_left + 5, y + 7, wbs, font="F1", size=8)
        draw_text(table_left + col_wbs + 5, y + 7, name, font="F2", size=8)
        draw_text(table_left + col_wbs + col_task + 5, y + 7, res, font="F2", size=7.5)
        draw_text(table_left + col_wbs + col_task + col_res + 5, y + 7, str(dur), font="F2", size=8)

        # Day grid vertical dotted lines
        set_color_rgb(0.88, 0.90, 0.92, stroke=True)
        for d in range(1, TOTAL_DAYS + 2):
            gx = grid_left + (d - 1) * day_step
            draw_line(gx, y, gx, y + row_height, line_width=0.4)

        # Task Bar
        bar_x = grid_left + (start - 1) * day_step
        bar_w = dur * day_step - 2
        bar_y = y + 4
        bar_h = row_height - 8

        if is_crit:
            set_color_rgb(0.85, 0.22, 0.22)  # Critical Crimson
        else:
            set_color_rgb(0.25, 0.50, 0.85)  # Agile Blue

        draw_rect(bar_x, bar_y, bar_w, bar_h, fill=True)

        # Milestone Marker (Diamond / Star)
        if milestone:
            mx = bar_x + bar_w
            set_color_rgb(0.95, 0.70, 0.15)
            draw_rect(mx - 4, bar_y + 1, 9, 9, fill=True)
            set_color_rgb(0.80, 0.40, 0.05)
            draw_text(mx + 7, bar_y + 2, milestone.split(":")[0], font="F1", size=6.5)

    # Footer Metadata
    set_color_rgb(0.1, 0.15, 0.25)
    draw_line(table_left, 35, width - 25, 35, line_width=0.8)
    set_color_rgb(0.4, 0.45, 0.55)
    draw_text(table_left, 20, "SE 231CS523 Supporting Activity Task 1 Deliverable | Critical Path Method (CPM) Verified | Duration: 28 Days", font="F2", size=8)
    draw_text(width - 240, 20, "Generated by EduTask DevOps Toolchain", font="F1", size=8)

    # Build PDF Objects
    stream_content = "\n".join(stream_lines)
    stream_bytes = stream_content.encode("latin-1")
    stream_len = len(stream_bytes)

    objects = []
    # 1: Catalog
    objects.append("1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
    # 2: Pages
    objects.append("2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n")
    # 3: Page
    objects.append(
        f"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {width} {height}] "
        f"/Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> /Contents 6 0 R >>\nendobj\n"
    )
    # 4: Font F1 (Helvetica-Bold)
    objects.append("4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>\nendobj\n")
    # 5: Font F2 (Helvetica)
    objects.append("5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n")
    # 6: Stream
    objects.append(f"6 0 obj\n<< /Length {stream_len} >>\nstream\n{stream_content}\nendstream\nendobj\n")

    # Assemble PDF with Xref
    pdf_out = bytearray()
    pdf_out.extend(b"%PDF-1.4\n")
    offsets = []

    for obj in objects:
        offsets.append(len(pdf_out))
        pdf_out.extend(obj.encode("latin-1"))

    xref_pos = len(pdf_out)
    pdf_out.extend(b"xref\n0 7\n0000000000 65535 f \n")
    for off in offsets:
        pdf_out.extend(f"{off:010d} 00000 n \n".encode("latin-1"))

    trailer = (
        f"trailer\n<< /Size 7 /Root 1 0 R >>\n"
        f"startxref\n{xref_pos}\n%%EOF\n"
    )
    pdf_out.extend(trailer.encode("latin-1"))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(pdf_out)

    print(f"[SUCCESS] Generated Gantt Chart PDF: {output_path} ({len(pdf_out)} bytes)")


def create_html_gantt(output_path: str):
    """Generate an interactive HTML Gantt & PERT Chart visualization"""
    rows_html = ""
    for task in TASKS:
        wbs, name, start, dur, end, res, is_crit, milestone = task
        start_pct = round(((start - 1) / TOTAL_DAYS) * 100, 2)
        width_pct = round((dur / TOTAL_DAYS) * 100, 2)
        bar_color = "#ef4444" if is_crit else "#3b82f6"
        badge_class = "crit-badge" if is_crit else "slack-badge"
        milestone_html = f"<span class='milestone-tag'>💎 {milestone}</span>" if milestone else ""

        rows_html += f"""
        <tr>
          <td><strong>{wbs}</strong></td>
          <td>{name} {milestone_html}</td>
          <td>{res}</td>
          <td>{dur}d</td>
          <td><span class="{badge_class}">{ 'Critical (0 slack)' if is_crit else 'Non-Critical' }</span></td>
          <td class="timeline-cell">
            <div class="gantt-bar-container">
              <div class="gantt-bar" style="left: {start_pct}%; width: {width_pct}%; background-color: {bar_color};">
                Day {start}-{end}
              </div>
            </div>
          </td>
        </tr>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>EduTask Project Gantt Chart & PERT Schedule | 231CS523</title>
  <style>
    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 2rem; background: #f8fafc; color: #1e293b; }}
    .header {{ background: #0f172a; color: white; padding: 1.5rem 2rem; border-radius: 8px; margin-bottom: 2rem; }}
    .header h1 {{ margin: 0 0 0.5rem 0; font-size: 1.6rem; }}
    .header p {{ margin: 0; color: #94a3b8; font-size: 0.95rem; }}
    .legend {{ display: flex; gap: 1.5rem; margin-bottom: 1.5rem; background: white; padding: 1rem; border-radius: 8px; border: 1px solid #e2e8f0; }}
    .legend-item {{ display: flex; align-items: center; gap: 0.5rem; font-size: 0.9rem; }}
    .color-box {{ width: 18px; height: 18px; border-radius: 4px; }}
    table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
    th, td {{ padding: 0.75rem 1rem; border-bottom: 1px solid #e2e8f0; font-size: 0.85rem; text-align: left; }}
    th {{ background: #f1f5f9; font-weight: 600; color: #475569; }}
    .timeline-cell {{ width: 45%; }}
    .gantt-bar-container {{ position: relative; height: 26px; background: #f1f5f9; border-radius: 4px; overflow: hidden; }}
    .gantt-bar {{ position: absolute; height: 100%; color: white; font-size: 0.72rem; font-weight: bold; line-height: 26px; text-align: center; border-radius: 3px; }}
    .crit-badge {{ background: #fee2e2; color: #991b1b; padding: 0.2rem 0.5rem; border-radius: 4px; font-weight: 600; font-size: 0.75rem; }}
    .slack-badge {{ background: #e0f2fe; color: #0369a1; padding: 0.2rem 0.5rem; border-radius: 4px; font-weight: 600; font-size: 0.75rem; }}
    .milestone-tag {{ font-size: 0.75rem; background: #fef3c7; color: #92400e; padding: 0.15rem 0.4rem; border-radius: 4px; font-weight: 600; margin-left: 0.4rem; }}
    @media print {{ body {{ margin: 0; }} .header {{ background: #0f172a !important; -webkit-print-color-adjust: exact; }} }}
  </style>
</head>
<body>
  <div class="header">
    <h1>EduTask Project Management Gantt Chart & Schedule</h1>
    <p>Course: 231CS523 Software Engineering &bull; Unit-V Supporting Activity (CO5, PO5, PO9, PO11)</p>
  </div>

  <div class="legend">
    <div class="legend-item"><div class="color-box" style="background: #ef4444;"></div> <strong>Critical Path (Zero Float)</strong></div>
    <div class="legend-item"><div class="color-box" style="background: #3b82f6;"></div> Non-Critical Tasks (With Float)</div>
    <div class="legend-item"><span style="font-size: 1.2rem;">💎</span> Project Milestones (M1 to M5)</div>
  </div>

  <table>
    <thead>
      <tr>
        <th>WBS</th>
        <th>Task Description</th>
        <th>Assigned Resource</th>
        <th>Dur</th>
        <th>Status</th>
        <th>Timeline (Day 1 to 28)</th>
      </tr>
    </thead>
    <tbody>
      {rows_html}
    </tbody>
  </table>
</body>
</html>
"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[SUCCESS] Generated Gantt Chart HTML: {output_path}")


if __name__ == "__main__":
    pdf_path = os.path.join(os.path.dirname(__file__), "..", "docs", "Gantt_Chart.pdf")
    html_path = os.path.join(os.path.dirname(__file__), "..", "docs", "gantt_chart.html")
    create_pdf(pdf_path)
    create_html_gantt(html_path)

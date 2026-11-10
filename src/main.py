"""
FastAPI Main Application: Student Task Management System (EduTask)
Course: Software Engineering (Lab Integrated) - 231CS523
Baseline: v1.1 (Includes CR-101 Workload Analytics & Filtering)
"""

import time
import os
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request, Response, status, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

from src.models import (
    Task, TaskCreate, TaskUpdate, PriorityEnum, StatusEnum,
    WorkloadSummary, HealthStatus, MetricsResponse
)
from src.task_service import task_service

APP_START_TIME = time.time()
REQUEST_COUNT = 0
ERROR_COUNT = 0
APP_VERSION = "1.1.0"

app = FastAPI(
    title="EduTask - Student Task Management System",
    description="End-to-End Software Engineering & DevOps Implementation (Course: 231CS523)",
    version=APP_VERSION
)

# Enable CORS for cross-origin integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """Middleware for tracking request latency, total hits, and error status"""
    global REQUEST_COUNT, ERROR_COUNT
    REQUEST_COUNT += 1
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = f"{process_time:.4f}s"
        response.headers["X-Service-Version"] = APP_VERSION
        if response.status_code >= 500:
            ERROR_COUNT += 1
        return response
    except Exception as exc:
        ERROR_COUNT += 1
        raise exc


# Mount static directory for Frontend assets
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", include_in_schema=False)
async def read_root():
    """Serve frontend index.html"""
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return JSONResponse(
        content={"message": "EduTask API is operational. Visit /docs for OpenAPI documentation."},
        status_code=200
    )


# --- REST API Endpoints ---

@app.get("/api/tasks", response_model=List[Task], tags=["Tasks"])
async def get_tasks(
    course_code: Optional[str] = Query(None, description="Filter by course tag, e.g. 231CS523"),
    priority: Optional[PriorityEnum] = Query(None, description="Filter by priority"),
    status: Optional[StatusEnum] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search keyword in title or description")
):
    """Retrieve all student tasks with optional filtering"""
    return task_service.list_tasks(
        course_code=course_code,
        priority=priority,
        status=status,
        search=search
    )


@app.get("/api/tasks/{task_id}", response_model=Task, tags=["Tasks"])
async def get_task(task_id: int):
    """Retrieve specific task by its ID"""
    task = task_service.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return task


@app.post("/api/tasks", response_model=Task, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
async def create_task(task_in: TaskCreate):
    """Create a new student task/assignment"""
    return task_service.create_task(task_in)


@app.put("/api/tasks/{task_id}", response_model=Task, tags=["Tasks"])
async def update_task(task_id: int, task_in: TaskUpdate):
    """Update existing task details"""
    updated = task_service.update_task(task_id, task_in)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return updated


@app.delete("/api/tasks/{task_id}", status_code=status.HTTP_200_OK, tags=["Tasks"])
async def delete_task(task_id: int):
    """Delete a task by ID"""
    success = task_service.delete_task(task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return {"message": f"Task {task_id} successfully deleted", "id": task_id}


@app.post("/api/tasks/{task_id}/toggle", response_model=Task, tags=["Tasks"])
async def toggle_task_status(task_id: int):
    """Quick toggle completion status between PENDING and COMPLETED"""
    toggled = task_service.toggle_status(task_id)
    if not toggled:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )
    return toggled


@app.get("/api/tasks/analytics/workload", response_model=WorkloadSummary, tags=["Analytics"])
async def get_workload_analytics():
    """CR-101 Feature: Aggregated student study workload and completion rate"""
    return task_service.get_workload_summary()


# --- DevOps & Monitoring Endpoints ---

@app.get("/api/health", response_model=HealthStatus, tags=["DevOps & Monitoring"])
async def health_check():
    """Health check endpoint for Docker container checks, Kubernetes probes, and Uptime monitors"""
    uptime = time.time() - APP_START_TIME
    tasks = task_service.list_tasks()
    return HealthStatus(
        status="UP",
        service="EduTask-Student-Task-Manager",
        version=APP_VERSION,
        uptime_seconds=round(uptime, 2),
        timestamp=datetime.now().isoformat(),
        environment=os.getenv("APP_ENV", "production"),
        database="In-Memory-Persistent-Store",
        total_tasks=len(tasks)
    )


@app.get("/api/metrics", response_model=MetricsResponse, tags=["DevOps & Monitoring"])
async def get_metrics():
    """Operational telemetry for observability and monitoring"""
    uptime = time.time() - APP_START_TIME
    tasks = task_service.list_tasks()
    active_count = sum(1 for t in tasks if t.status != StatusEnum.COMPLETED)
    completed_count = sum(1 for t in tasks if t.status == StatusEnum.COMPLETED)
    return MetricsResponse(
        uptime_seconds=round(uptime, 2),
        total_requests=REQUEST_COUNT,
        total_errors=ERROR_COUNT,
        active_tasks=active_count,
        completed_tasks=completed_count,
        version=APP_VERSION
    )


@app.get("/api/version", tags=["DevOps & Monitoring"])
async def get_version_info():
    """SCM Baseline Version metadata"""
    return {
        "version": APP_VERSION,
        "baseline": "Baseline v1.1",
        "change_request": "CR-101 (Workload Analytics & Priority Filtering)",
        "course": "231CS523 - Software Engineering",
        "team_size": 4
    }

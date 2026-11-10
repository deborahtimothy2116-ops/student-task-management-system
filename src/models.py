"""
Data models and schemas for Student Task Management System (EduTask)
Supports Baseline v1.0 and Change Request CR-101 (Workload estimation and Priority scoring)
"""

from enum import Enum
from typing import Optional, List
from datetime import datetime, date
from pydantic import BaseModel, Field


class PriorityEnum(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class StatusEnum(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class TaskBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=150, description="Title of the assignment or task")
    description: Optional[str] = Field(default="", max_length=1000, description="Detailed task requirements")
    course_code: str = Field(..., min_length=2, max_length=20, description="Course tag, e.g. 231CS523")
    due_date: str = Field(..., description="Due date in YYYY-MM-DD format")
    priority: PriorityEnum = Field(default=PriorityEnum.MEDIUM, description="Task priority")
    estimated_hours: float = Field(default=2.0, ge=0.5, le=100.0, description="Estimated study/completion hours (CR-101)")


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=2, max_length=150)
    description: Optional[str] = None
    course_code: Optional[str] = None
    due_date: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    status: Optional[StatusEnum] = None
    estimated_hours: Optional[float] = Field(default=None, ge=0.5, le=100.0)


class Task(TaskBase):
    id: int
    status: StatusEnum = StatusEnum.PENDING
    created_at: str
    completed_at: Optional[str] = None
    is_overdue: bool = False


class WorkloadSummary(BaseModel):
    total_tasks: int
    pending_tasks: int
    in_progress_tasks: int
    completed_tasks: int
    high_or_critical_tasks: int
    total_estimated_hours: float
    remaining_hours: float
    completion_rate_percentage: float


class HealthStatus(BaseModel):
    status: str
    service: str
    version: str
    uptime_seconds: float
    timestamp: str
    environment: str
    database: str
    total_tasks: int


class MetricsResponse(BaseModel):
    uptime_seconds: float
    total_requests: int
    total_errors: int
    active_tasks: int
    completed_tasks: int
    version: str

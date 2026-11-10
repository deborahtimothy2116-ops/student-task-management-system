"""
Unit Tests for Domain Business Logic and CR-101 Features
Validates workload estimation formulas, priority rankings, and overdue detectors.
"""

import pytest
from src.task_service import TaskService
from src.models import TaskCreate, PriorityEnum, StatusEnum


def test_workload_calculation_cr101():
    """Verify CR-101 workload aggregation math"""
    svc = TaskService()
    svc._tasks.clear()
    svc._next_id = 1

    svc.create_task(TaskCreate(
        title="Assignment 1",
        course_code="CS101",
        due_date="2026-11-20",
        priority=PriorityEnum.HIGH,
        estimated_hours=4.0
    ))
    svc.create_task(TaskCreate(
        title="Assignment 2",
        course_code="CS102",
        due_date="2026-11-22",
        priority=PriorityEnum.MEDIUM,
        estimated_hours=6.0
    ))

    summary = svc.get_workload_summary()
    assert summary.total_tasks == 2
    assert summary.pending_tasks == 2
    assert summary.completed_tasks == 0
    assert summary.total_estimated_hours == 10.0
    assert summary.remaining_hours == 10.0
    assert summary.completion_rate_percentage == 0.0

    # Complete one task and re-check
    svc.toggle_status(1)
    summary2 = svc.get_workload_summary()
    assert summary2.completed_tasks == 1
    assert summary2.pending_tasks == 1
    assert summary2.remaining_hours == 6.0
    assert summary2.completion_rate_percentage == 50.0


def test_overdue_detection():
    """Verify overdue detection for past dates"""
    svc = TaskService()
    svc._tasks.clear()

    # Past task
    t1 = svc.create_task(TaskCreate(
        title="Old Homework",
        course_code="CS100",
        due_date="2020-01-01",
        priority=PriorityEnum.LOW,
        estimated_hours=1.0
    ))
    assert t1.is_overdue is True

    # When completed, is_overdue should become False
    svc.toggle_status(t1.id)
    t1_updated = svc.get_task(t1.id)
    assert t1_updated.is_overdue is False


def test_priority_sorting_order():
    """Verify tasks are returned in CRITICAL -> HIGH -> MEDIUM -> LOW order"""
    svc = TaskService()
    svc._tasks.clear()

    svc.create_task(TaskCreate(title="Low Task", course_code="C1", due_date="2026-12-01", priority=PriorityEnum.LOW))
    svc.create_task(TaskCreate(title="Critical Task", course_code="C1", due_date="2026-12-01", priority=PriorityEnum.CRITICAL))
    svc.create_task(TaskCreate(title="High Task", course_code="C1", due_date="2026-12-01", priority=PriorityEnum.HIGH))

    tasks = svc.list_tasks()
    assert tasks[0].priority == PriorityEnum.CRITICAL
    assert tasks[1].priority == PriorityEnum.HIGH
    assert tasks[2].priority == PriorityEnum.LOW


def test_search_filter():
    """Verify keyword searching across title, description, and course tag"""
    svc = TaskService()
    results = svc.list_tasks(search="Socket")
    assert len(results) >= 1
    assert "socket" in results[0].title.lower()

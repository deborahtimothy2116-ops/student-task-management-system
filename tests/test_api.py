"""
Automated API and Integration Tests for Student Task Management System
Exercises all REST endpoints, validation, filters, and health monitoring.
"""

import pytest
from fastapi import status


def test_root_endpoint(client):
    """Test root HTML serving"""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK


def test_list_tasks(client):
    """Test listing all seeded student tasks"""
    response = client.get("/api/tasks")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 4
    assert any(t["course_code"] == "231CS523" for t in data)


def test_get_task_by_id(client):
    """Test retrieving single task by ID"""
    response = client.get("/api/tasks/1")
    assert response.status_code == status.HTTP_200_OK
    task = response.json()
    assert task["id"] == 1
    assert "title" in task
    assert "priority" in task
    assert "estimated_hours" in task


def test_get_task_not_found(client):
    """Test 404 response for non-existent task ID"""
    response = client.get("/api/tasks/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()


def test_create_task_success(client):
    """Test creating a valid new task"""
    payload = {
        "title": "Automated Selenium & Unit Test Verification",
        "description": "Write end-to-end integration test suite for Assignment 4",
        "course_code": "231CS523",
        "due_date": "2026-11-25",
        "priority": "HIGH",
        "estimated_hours": 3.5
    }
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["course_code"] == "231CS523"
    assert data["status"] == "PENDING"
    assert data["estimated_hours"] == 3.5
    assert "id" in data


def test_create_task_validation_error(client):
    """Test validation rejection for invalid task data (empty title)"""
    payload = {
        "title": "A",  # Min length is 2
        "course_code": "",
        "due_date": "2026-11-25"
    }
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 422


def test_update_task(client):
    """Test updating existing task fields"""
    update_payload = {
        "title": "Updated SE Lab Milestone 4",
        "priority": "CRITICAL",
        "estimated_hours": 5.0
    }
    response = client.put("/api/tasks/1", json=update_payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Updated SE Lab Milestone 4"
    assert data["priority"] == "CRITICAL"
    assert data["estimated_hours"] == 5.0


def test_toggle_task_status(client):
    """Test toggling task from PENDING to COMPLETED"""
    res1 = client.post("/api/tasks/1/toggle")
    assert res1.status_code == status.HTTP_200_OK
    assert res1.json()["status"] == "COMPLETED"
    assert res1.json()["completed_at"] is not None

    # Toggle back to PENDING
    res2 = client.post("/api/tasks/1/toggle")
    assert res2.status_code == status.HTTP_200_OK
    assert res2.json()["status"] == "PENDING"
    assert res2.json()["completed_at"] is None


def test_delete_task(client):
    """Test deleting task and verifying 404 upon subsequent request"""
    # Create temporary task
    temp = client.post("/api/tasks", json={
        "title": "Temporary Task for Deletion",
        "course_code": "TEST101",
        "due_date": "2026-12-01",
        "priority": "LOW",
        "estimated_hours": 1.0
    }).json()
    task_id = temp["id"]

    # Delete task
    del_res = client.delete(f"/api/tasks/{task_id}")
    assert del_res.status_code == status.HTTP_200_OK

    # Verify task no longer exists
    get_res = client.get(f"/api/tasks/{task_id}")
    assert get_res.status_code == status.HTTP_404_NOT_FOUND


def test_filter_by_course(client):
    """Test filtering by course tag"""
    response = client.get("/api/tasks?course_code=231CS523")
    assert response.status_code == status.HTTP_200_OK
    tasks = response.json()
    assert len(tasks) > 0
    assert all(t["course_code"] == "231CS523" for t in tasks)


def test_filter_by_priority(client):
    """Test filtering by priority level"""
    response = client.get("/api/tasks?priority=CRITICAL")
    assert response.status_code == status.HTTP_200_OK
    tasks = response.json()
    assert len(tasks) > 0
    assert all(t["priority"] == "CRITICAL" for t in tasks)


def test_health_check_endpoint(client):
    """DevOps healthcheck validation for Docker and uptime monitors"""
    response = client.get("/api/health")
    assert response.status_code == status.HTTP_200_OK
    health = response.json()
    assert health["status"] == "UP"
    assert health["service"] == "EduTask-Student-Task-Manager"
    assert "uptime_seconds" in health
    assert "version" in health


def test_metrics_endpoint(client):
    """DevOps observability metrics validation"""
    response = client.get("/api/metrics")
    assert response.status_code == status.HTTP_200_OK
    metrics = response.json()
    assert metrics["total_requests"] > 0
    assert "active_tasks" in metrics
    assert "completed_tasks" in metrics


def test_version_endpoint(client):
    """SCM baseline metadata check"""
    response = client.get("/api/version")
    assert response.status_code == status.HTTP_200_OK
    ver = response.json()
    assert ver["version"] == "1.1.0"
    assert "CR-101" in ver["change_request"]

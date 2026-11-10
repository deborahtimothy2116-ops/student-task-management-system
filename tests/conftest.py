"""
Pytest configuration and shared test fixtures
"""

import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.task_service import task_service


@pytest.fixture(scope="session")
def client():
    """Session-wide test client for FastAPI endpoints"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def reset_tasks():
    """Reset task repository to default state before each test"""
    task_service._tasks.clear()
    task_service._next_id = 1
    task_service._seed_initial_data()
    yield

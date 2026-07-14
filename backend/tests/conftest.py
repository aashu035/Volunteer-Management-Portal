"""Pytest configuration and shared fixtures."""

import pytest


@pytest.fixture
def sample_user_data():
    """Sample user registration data."""
    return {
        "email": "test@example.com",
        "password": "TestPass@123",
        "full_name": "Test User",
        "phone": "+919876543210",
    }


@pytest.fixture
def sample_event_data():
    """Sample event creation data."""
    return {
        "title": "Test Event",
        "description": "A test event for unit testing.",
        "location": "Test City",
        "start_date": "2026-08-01T10:00:00Z",
        "end_date": "2026-08-01T18:00:00Z",
        "max_volunteers": 20,
        "required_skill_ids": [],
    }


@pytest.fixture
def sample_task_data():
    """Sample task creation data."""
    return {
        "title": "Test Task",
        "description": "A test task for unit testing.",
        "required_skills": ["Python", "Teaching"],
        "estimated_hours": 3.0,
    }

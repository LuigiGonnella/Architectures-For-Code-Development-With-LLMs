import pytest
import json
import tempfile
from pathlib import Path

from single_agent.src.utils.task_loader import load_tasks


def test_load_valid_tasks():
    """Test loading a valid task file"""
    tasks_data = [
        {"id": "test1", "signature": "def foo():", "docstring": "A test function"},
        {
            "id": "test2",
            "signature": "def bar(x: int):",
            "docstring": "Another test function",
        },
    ]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(tasks_data, f)
        temp_path = f.name

    try:
        tasks = load_tasks(temp_path)
        assert len(tasks) == 2
        assert tasks[0]["id"] == "test1"
        assert tasks[1]["id"] == "test2"
    finally:
        Path(temp_path).unlink()


def test_load_tasks_with_extra_fields():
    """Test that extra fields in tasks are preserved"""
    tasks_data = [
        {
            "id": "test1",
            "signature": "def foo():",
            "docstring": "A test function",
            "difficulty": "Easy",
            "examples": [],
        }
    ]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(tasks_data, f)
        temp_path = f.name

    try:
        tasks = load_tasks(temp_path)
        assert tasks[0]["difficulty"] == "Easy"
        assert "examples" in tasks[0]
    finally:
        Path(temp_path).unlink()


def test_load_tasks_missing_field():
    """Test that loading tasks with missing required fields raises ValueError"""
    tasks_data = [
        {
            "id": "test1",
            "signature": "def foo():",
            # missing docstring
        }
    ]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(tasks_data, f)
        temp_path = f.name

    try:
        with pytest.raises(ValueError, match="missing required fields"):
            load_tasks(temp_path)
    finally:
        Path(temp_path).unlink()


def test_load_tasks_not_a_list():
    """Test that loading non-list JSON raises ValueError"""
    tasks_data = {
        "id": "test1",
        "signature": "def foo():",
        "docstring": "A test function",
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(tasks_data, f)
        temp_path = f.name

    try:
        with pytest.raises(ValueError, match="must contain a list"):
            load_tasks(temp_path)
    finally:
        Path(temp_path).unlink()


def test_load_tasks_file_not_found():
    """Test that loading non-existent file raises FileNotFoundError"""
    with pytest.raises(FileNotFoundError):
        load_tasks("nonexistent_file.json")


def test_load_tasks_invalid_json():
    """Test that loading invalid JSON raises JSONDecodeError"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write("{ invalid json }")
        temp_path = f.name

    try:
        with pytest.raises(json.JSONDecodeError):
            load_tasks(temp_path)
    finally:
        Path(temp_path).unlink()


def test_load_empty_task_list():
    """Test that loading empty task list works"""
    tasks_data = []

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(tasks_data, f)
        temp_path = f.name

    try:
        tasks = load_tasks(temp_path)
        assert tasks == []
    finally:
        Path(temp_path).unlink()


def test_load_real_task_file():
    """Test loading the actual test-tasks.json file"""
    tasks = load_tasks("data/test-tasks.json")
    assert len(tasks) > 0
    assert all("id" in task for task in tasks)
    assert all("signature" in task for task in tasks)
    assert all("docstring" in task for task in tasks)

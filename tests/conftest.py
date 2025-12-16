"""
Pytest configuration and shared fixtures.
"""
import pytest


@pytest.fixture
def sample_task():
    """Fixture providing a sample task dictionary"""
    return {
        "id": "test_add",
        "signature": "def add(a: int, b: int) -> int:",
        "docstring": "Return the sum of a and b."
    }


@pytest.fixture
def sample_tasks():
    """Fixture providing a list of sample tasks"""
    return [
        {
            "id": "test_add",
            "signature": "def add(a: int, b: int) -> int:",
            "docstring": "Return the sum of a and b."
        },
        {
            "id": "test_multiply",
            "signature": "def multiply(a: int, b: int) -> int:",
            "docstring": "Return the product of a and b."
        }
    ]

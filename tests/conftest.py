"""
Pytest configuration and shared fixtures
"""
import os
import tempfile

import pytest

from backend.sample import Calculator


@pytest.fixture
def base_url():
    """Fixture providing base URL for API tests"""
    return "https://reqres.in/api"


@pytest.fixture
def api_page():
    """Fixture providing default page number"""
    return 2


@pytest.fixture
def sample_user_data():
    """Fixture providing sample user data for testing"""
    return {
        'name': 'john doe',
        'email': 'john.doe@example.com',
        'age': 25
    }


@pytest.fixture
def invalid_user_data():
    """Fixture providing invalid user data for testing error cases"""
    return {
        'name': 'jane doe',
        'email': 'jane.doe@example.com'
        # Missing 'age' field
    }


@pytest.fixture
def calculator():
    """Fixture providing a fresh Calculator instance"""
    calc = Calculator()
    yield calc
    # Cleanup after test
    calc.clear_history()


@pytest.fixture
def temp_file():
    """Fixture providing a temporary file for testing file operations"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write("Test content")
        temp_path = f.name

    yield temp_path

    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture(scope="session")
def session_data():
    """Session-scoped fixture that persists across all tests in the session"""
    return {"session_counter": 0}


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Auto-use fixture that runs before each test"""
    print("\n--- Setting up test environment ---")
    yield
    print("--- Cleaning up test environment ---")


@pytest.fixture(params=[1, 2, 3, 4, 5])
def fibonacci_input(request):
    """Parametrized fixture providing Fibonacci input values"""
    return request.param


@pytest.fixture
def mock_api_response():
    """Fixture providing mock API response data"""
    return {
        "page": 1,
        "per_page": 6,
        "total": 12,
        "total_pages": 2,
        "data": [
            {"id": 1, "email": "george.bluth@reqres.in", "first_name": "George"},
            {"id": 2, "email": "janet.weaver@reqres.in", "first_name": "Janet"}
        ]
    }

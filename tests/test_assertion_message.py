"""
Pytest assertion and message examples.
This file demonstrates various assertion types and custom error messages.
"""
import pytest

from backend.sample import (
    add_number,
    get_user_by_api,
    divide_numbers,
    process_user_data,
    calculate_fibonacci,
    Calculator
)


# Basic assertion tests
def test_basic_assertions():
    """Test basic assertion types"""
    # Boolean assertions
    assert True
    assert not False

    # Comparison assertions
    assert 5 > 3
    assert 3 < 5
    assert 5 >= 5
    assert 3 <= 5
    assert 5 != 3
    assert 5 == 5


def test_membership_assertions():
    """Test membership assertions"""
    # String membership
    assert "hello" in "hello world"
    assert "goodbye" not in "hello world"

    # List membership
    numbers = [1, 2, 3, 4, 5]
    assert 3 in numbers
    assert 6 not in numbers

    # Dictionary membership
    data = {"name": "John", "age": 30}
    assert "name" in data
    assert "city" not in data


def test_type_assertions():
    """Test type checking assertions"""
    # Type assertions
    assert isinstance(5, int)
    assert isinstance("hello", str)
    assert isinstance([1, 2, 3], list)
    assert isinstance({"key": "value"}, dict)
    assert isinstance((1, 2), tuple)
    assert isinstance({1, 2, 3}, set)


def test_collection_assertions():
    """Test collection-related assertions"""
    numbers = [1, 2, 3, 4, 5]

    # Length assertions
    assert len(numbers) == 5
    assert len("hello") == 5

    # Empty/non-empty assertions
    assert [] == []
    assert [1, 2, 3] != []
    assert bool([]) is False
    assert bool([1, 2, 3]) is True


# Assertion with custom messages
def test_assert_with_simple_message():
    """Test assertions with simple custom messages"""
    result = add_number(2, 3)
    assert result == 5, "Addition should return 5"


def test_assert_with_formatted_message():
    """Test assertions with formatted messages"""
    result = add_number(2, 3)
    assert result == 5, f"Expected 5, but got {result}"


def test_assert_with_detailed_message():
    """Test assertions with detailed error messages"""
    a, b = 2, 3
    result = add_number(a, b)
    assert result == 5, f"add_number({a}, {b}) should return {a + b}, but got {result}"


def test_assert_with_multiple_conditions():
    """Test assertions with multiple conditions and messages"""
    result = add_number(2, 3)

    # Multiple assertions with different messages
    assert result > 0, "Result should be positive"
    assert result == 5, "Result should equal 5"
    assert isinstance(result, int), "Result should be an integer"


# Approximate equality assertions
def test_assert_almost_equal():
    """Test approximate equality for floating point numbers"""
    result = divide_numbers(1, 3)
    assert result == pytest.approx(0.333333, rel=1e-5)


def test_assert_almost_equal_with_absolute_tolerance():
    """Test approximate equality with absolute tolerance"""
    result = divide_numbers(1, 3)
    assert result == pytest.approx(0.333, abs=0.001)


def test_assert_almost_equal_with_relative_tolerance():
    """Test approximate equality with relative tolerance"""
    result = divide_numbers(1, 3)
    assert result == pytest.approx(0.333, rel=0.01)


# Exception assertion messages
def test_exception_assertion_with_message():
    """Test exception assertions with custom messages"""
    with pytest.raises(ValueError) as exc_info:
        divide_numbers(10, 0)

    assert "Cannot divide by zero" in str(
        exc_info.value), f"Expected 'Cannot divide by zero' in error message, got: {exc_info.value}"


def test_exception_assertion_with_detailed_message():
    """Test exception assertions with detailed messages"""
    dividend, divisor = 10, 0

    with pytest.raises(ValueError) as exc_info:
        divide_numbers(dividend, divisor)

    error_msg = str(exc_info.value)
    assert "Cannot divide by zero" in error_msg, f"divide_numbers({dividend}, {divisor}) should raise ValueError with 'Cannot divide by zero' message, got: {error_msg}"


# Complex assertion messages
def test_complex_assertion_message():
    """Test complex assertion with detailed message"""
    user_data = {
        'name': 'john doe',
        'email': 'john@example.com',
        'age': 25
    }

    try:
        result = process_user_data(user_data)
        assert result[
                   'formatted_name'] == 'John Doe', f"Expected formatted name 'John Doe', got '{result['formatted_name']}'"
        assert result[
                   'age_group'] == 'adult', f"Expected age group 'adult' for age {user_data['age']}, got '{result['age_group']}'"
    except Exception as e:
        pytest.fail(f"process_user_data failed with unexpected error: {e}")


def test_assertion_with_context():
    """Test assertions with context information"""
    calc = Calculator()

    # Test with context about what we're testing
    result = calc.add(3, 4)
    assert result == 7, f"Calculator.add(3, 4) should return 7, got {result}"

    # Test history tracking
    history = calc.get_history()
    assert len(history) == 1, f"Expected 1 operation in history, got {len(history)}"
    assert "3 + 4 = 7" in history, f"Expected '3 + 4 = 7' in history, got {history}"


# Parametrized assertions with messages
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (10, -5, 5)
])
def test_parametrized_assertion_with_message(a, b, expected):
    """Test parametrized assertions with custom messages"""
    result = add_number(a, b)
    assert result == expected, f"add_number({a}, {b}) should return {expected}, got {result}"


# Assertion with data validation
def test_assertion_with_data_validation():
    """Test assertions with data validation messages"""
    user_data = {
        'name': 'test user',
        'email': 'test@example.com',
        'age': 25
    }

    # Validate input data
    assert isinstance(user_data, dict), f"user_data should be a dict, got {type(user_data)}"
    assert 'name' in user_data, f"user_data should contain 'name' key, got keys: {list(user_data.keys())}"
    assert 'email' in user_data, f"user_data should contain 'email' key, got keys: {list(user_data.keys())}"
    assert 'age' in user_data, f"user_data should contain 'age' key, got keys: {list(user_data.keys())}"

    # Process and validate result
    result = process_user_data(user_data)
    assert isinstance(result, dict), f"process_user_data should return a dict, got {type(result)}"
    assert 'formatted_name' in result, f"Result should contain 'formatted_name', got keys: {list(result.keys())}"


# Assertion with performance context
def test_assertion_with_performance_context():
    """Test assertions with performance context"""
    import time

    start_time = time.time()
    result = calculate_fibonacci(10)
    end_time = time.time()

    execution_time = end_time - start_time

    assert result == 55, f"Fibonacci(10) should return 55, got {result}"
    assert execution_time < 1.0, f"Fibonacci calculation took {execution_time:.3f}s, should be less than 1.0s"


# Assertion with file system context
def test_assertion_with_file_context(temp_file):
    """Test assertions with file system context"""
    import os

    # Test file existence with context
    assert os.path.exists(temp_file), f"Temporary file should exist at {temp_file}"

    # Test file content with context
    with open(temp_file, 'r') as f:
        content = f.read()

    assert content == "Test content", f"File content should be 'Test content', got '{content}'"
    assert len(content) > 0, f"File should not be empty, got length {len(content)}"


# Assertion with API context
def test_assertion_with_api_context():
    """Test assertions with API context"""
    page, per_page = 2, 10
    result = get_user_by_api(page=page, per_page=per_page)

    expected_url = f"https://reqres.in/api/users?page={page}&per_page={per_page}"
    assert result == expected_url, f"API URL should be '{expected_url}', got '{result}'"
    assert "reqres.in" in result, f"API URL should contain 'reqres.in', got '{result}'"
    assert f"page={page}" in result, f"API URL should contain 'page={page}', got '{result}'"
    assert f"per_page={per_page}" in result, f"API URL should contain 'per_page={per_page}', got '{result}'"

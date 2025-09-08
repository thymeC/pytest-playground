"""
Comprehensive pytest test suite demonstrating various pytest features and syntax.
This file showcases different testing patterns, fixtures, parametrization, and more.

Note: For @pytest.mark.repeat to work, you need to install pytest-repeat:
    pip install pytest-repeat

Then run tests with repeat:
    pytest tests/test_sample.py::TestMarkers::test_repeat_5_times -v
"""
import os

import pytest

from backend.sample import (
    sample_function,
    sample_function_with_param,
    add_number,
    get_user_by_api,
    divide_numbers,
    process_user_data,
    calculate_fibonacci
)


class TestBasicFunctions:
    """Test class demonstrating basic pytest functionality"""

    def test_sample_function_no_param(self):
        """Normal test with no parameters - basic assertion"""
        result = sample_function()
        assert result == "Hello, World!"

    def test_add_number(self):
        """Basic arithmetic test"""
        result = add_number(2, 3)
        assert result == 5


class TestFixtures:
    """Test class demonstrating fixture usage"""

    def test_base_url_fixture(self, base_url):
        """Test using base_url fixture, base url defined in conftest.py, you can also write it in current file"""
        assert base_url == "https://reqres.in/api"

    def test_get_user_by_api_with_fixtures(self, base_url, api_page):
        """Test API URL generation using multiple fixtures"""
        result = get_user_by_api(page=api_page, per_page=6)
        expected = f"{base_url}/users?page={api_page}&per_page=6"
        assert result == expected


class TestParametrizedTests:
    """Test class demonstrating @pytest.mark.parametrize"""

    @pytest.mark.parametrize("page", [1, 2, 3, 4, 5])
    def test_get_user_by_api_single_param(self, page):
        """Parametrized test with single parameter - page only"""
        result = get_user_by_api(page=page)
        expected = f"https://reqres.in/api/users?page={page}&per_page=6"  # default per_page=6
        assert result == expected

    @pytest.mark.parametrize("name", ["Alice", "Bob", "Charlie", "Diana"])
    def test_sample_function_with_single_param(self, name):
        """Parametrized test with single parameter - name only"""
        result = sample_function_with_param(name)
        expected = f"Hello, {name}!"
        assert result == expected

    @pytest.mark.parametrize("a,b,expected", [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0)
    ])
    def test_add_number_parametrized(self, a, b, expected):
        """Parametrized test for add_number function"""
        result = add_number(a, b)
        assert result == expected


class TestExceptionHandling:
    """Test class demonstrating exception testing"""

    def test_divide_by_zero_raises_value_error(self):
        """Test that division by zero raises ValueError"""
        with pytest.raises(ValueError) as exc_info:
            divide_numbers(10, 0)

        assert "Cannot divide by zero" in str(exc_info.value)

    def test_process_user_data_missing_field(self, invalid_user_data):
        """Test that missing required field raises KeyError"""
        with pytest.raises(KeyError) as exc_info:
            process_user_data(invalid_user_data)

        assert "Missing required field: age" in str(exc_info.value)


class TestClassBasedTesting:
    """Test class demonstrating testing of class methods"""

    def test_calculator_add_method(self, calculator):
        """Test Calculator add method using fixture"""
        result = calculator.add(3, 4)
        assert result == 7
        assert "3 + 4 = 7" in calculator.get_history()


@pytest.mark.smoke
def test_smoke_test_basic_functionality():
    """Smoke test - basic functionality check"""
    result = sample_function()
    assert result is not None


class TestMarkers:
    """Test class demonstrating pytest markers"""

    @pytest.mark.smoke
    def test_smoke_test_basic_functionality(self):
        """Smoke test - basic functionality check"""
        result = sample_function()
        assert result is not None

    @pytest.mark.slow
    def test_slow_fibonacci_calculation(self):
        """Slow test - Fibonacci calculation for larger numbers"""
        result = calculate_fibonacci(10)
        assert result == 55

    @pytest.mark.skip(reason="This test is currently disabled")
    def test_skipped_test(self):
        """This test is skipped"""
        assert False  # This won't run

    @pytest.mark.skipif(True, reason="Conditional skip - always skips")
    def test_conditionally_skipped_always(self):
        """This test is conditionally skipped - always skips"""
        assert False  # This won't run

    @pytest.mark.skipif(False, reason="Conditional skip - never skips")
    def test_conditionally_skipped_never(self):
        """This test is conditionally skipped - never skips"""
        assert True  # This will run

    @pytest.mark.skipif(1 > 0, reason="Skip if 1 is greater than 0")
    def test_skipif_condition_true(self):
        """This test skips because condition is True"""
        assert False  # This won't run

    @pytest.mark.skipif(hasattr(__import__('sys'), 'version_info') and __import__('sys').version_info < (3, 8),
                        reason="Skip if Python version is less than 3.8")
    def test_skipif_python_version(self):
        """This test skips if Python version is less than 3.8"""
        assert True  # This will run on Python 3.8+

    @pytest.mark.repeat(5)
    def test_repeat_5_times(self):
        """This test will run 5 times - useful for testing flaky behavior"""
        result = add_number(2, 3)
        assert result == 5


class TestTemporaryFiles:
    """Test class demonstrating temporary file testing"""

    def test_temp_file_fixture(self, temp_file):
        """Test using temporary file fixture"""
        assert os.path.exists(temp_file)

        with open(temp_file, 'r') as f:
            content = f.read()
            assert content == "Test content"


# Standalone test functions (not in classes)
def test_standalone_function():
    """Standalone test function outside of any class"""
    result = sample_function()
    assert result == "Hello, World!"


@pytest.mark.parametrize("input_val,expected", [
    ("World", "Hello, World!"),
    ("Pytest", "Hello, Pytest!")
])
def test_standalone_parametrized(input_val, expected):
    """Standalone parametrized test function"""
    result = sample_function_with_param(input_val)
    assert result == expected


# Test with multiple markers
@pytest.mark.smoke
@pytest.mark.parametrize("page", [1, 2])
def test_multiple_markers(page):
    """Test with multiple markers"""
    result = get_user_by_api(page=page)
    assert f"page={page}" in result


"""
pytest.mark.xfail Documentation and Usage Examples

@pytest.mark.xfail is used to mark tests that are expected to fail. This is useful for:
1. Tests for known bugs that haven't been fixed yet
2. Tests for features that aren't implemented yet
3. Tests that are flaky or depend on external services
4. Tests that should fail on certain conditions

Basic Usage:
    @pytest.mark.xfail(reason="Known bug in implementation")
    def test_known_bug():
        assert False  # This will be marked as XFAIL

Parameters:
    - reason: Explanation of why the test is expected to fail
    - strict: If True, test will FAIL if it unexpectedly passes (default: False)
    - run: If False, test won't execute at all (default: True)
    - condition: Boolean or callable - if False, xfail is ignored
    - raises: Expected exception type - test passes if this exception is raised

Examples:

1. Basic xfail:
    @pytest.mark.xfail(reason="Feature not implemented")
    def test_new_feature():
        assert new_feature() == expected_result

2. Strict mode (fails if test unexpectedly passes):
    @pytest.mark.xfail(reason="Known bug", strict=True)
    def test_bug():
        assert buggy_function() == wrong_result

3. Conditional xfail:
    @pytest.mark.xfail(condition=sys.version_info < (3, 8), reason="Python < 3.8")
    def test_python_version_dependent():
        assert new_syntax_feature()

4. Expected exception:
    @pytest.mark.xfail(raises=ValueError, reason="Expected ValueError")
    def test_expected_exception():
        function_that_raises_value_error()

5. Don't run the test:
    @pytest.mark.xfail(reason="Too slow", run=False)
    def test_slow_operation():
        time.sleep(100)

6. With parametrization:
    @pytest.mark.xfail(reason="All cases expected to fail")
    @pytest.mark.parametrize("input", [1, 2, 3])
    def test_parametrized_xfail(input):
        assert input == 0

7. Combined with other markers:
    @pytest.mark.xfail(reason="Flaky test")
    @pytest.mark.slow
    def test_flaky_slow_test():
        assert flaky_operation()

Running xfail tests:
    pytest -v                    # Shows XFAIL results
    pytest --runxfail           # Runs xfail tests as normal tests
    pytest -k xfail             # Run only xfail tests
"""


@pytest.mark.xfail(reason="Demonstrates xfail - this test is expected to fail")
def test_xfail_example():
    """
    Example of pytest.mark.xfail usage.
    
    This test demonstrates how xfail works:
    - The test will fail (assert 1 == 2)
    - But it will be marked as XFAIL instead of FAIL
    - This is useful for tests of known bugs or unimplemented features
    """
    # This assertion will fail, but that's expected
    assert 1 == 2, "This is expected to fail - demonstrates xfail behavior"

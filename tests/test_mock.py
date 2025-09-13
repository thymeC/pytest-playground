"""
Comprehensive pytest-mock Examples and Documentation

This file demonstrates various mocking techniques using pytest-mock and unittest.mock.

pytest-mock is a thin wrapper around unittest.mock that provides:
- mocker fixture for easier mocking
- Better integration with pytest
- Automatic cleanup of mocks after tests

Installation:
    pip install pytest-mock

Key Concepts:
1. Mock vs MagicMock:
   - Mock: Basic mock object with limited functionality
   - MagicMock: Enhanced mock that automatically handles attribute access and method calls
   - MagicMock is a subclass of Mock with additional features

2. Patching Methods:
   - patch(): Context manager and decorator for patching
   - patch.object(): Patch specific attributes of an object
   - patch.dict(): Patch dictionary entries

3. Mock Assertions:
   - assert_called(): Verify method was called
   - assert_called_once(): Verify method was called exactly once
   - assert_called_with(): Verify method was called with specific arguments
   - assert_not_called(): Verify method was never called

4. Mock Configuration:
   - return_value: Set return value for method calls
   - side_effect: Set side effect (exception, function, or iterable)
   - spec: Set specification for mock attributes

Common Use Cases:
1. Mocking external API calls
2. Mocking file system operations
3. Mocking database operations
4. Mocking time-dependent functions
5. Mocking random functions for deterministic tests
6. Mocking expensive operations

Best Practices:
1. Mock at the boundary of your code (external dependencies)
2. Use spec to limit mock attributes
3. Verify mock calls with assertions
4. Use side_effect for complex behavior
5. Clean up mocks (automatic with pytest-mock)
6. Mock the minimal necessary parts

Examples in this file:
- Basic Mock vs MagicMock usage
- Patching functions and methods
- Mocking with return values and side effects
- Mocking external dependencies
- Mocking with fixtures and parametrization
- Advanced mocking patterns
"""
from unittest.mock import patch, MagicMock, Mock

import pytest

from backend.sample import (
    sample_function,
    add_number,
    get_user_by_api,
    process_user_data,
    calculate_fibonacci,
    validate_email,
    Calculator
)


class TestMockVsMagicMock:
    """Test class demonstrating Mock vs MagicMock differences and usage"""

    def test_basic_mock_usage(self):
        """
        Basic Mock usage - requires explicit attribute setup
        
        Mock is the base class that provides basic mocking functionality.
        It requires you to explicitly set up attributes and methods.
        """
        # Create a basic Mock
        mock_obj = Mock()

        # Explicitly set up attributes and methods
        mock_obj.name = "Test Name"
        mock_obj.age = 25
        mock_obj.get_info.return_value = "Mocked info"

        # Use the mock
        assert mock_obj.name == "Test Name"
        assert mock_obj.age == 25
        assert mock_obj.get_info() == "Mocked info"

        # Verify calls
        mock_obj.get_info.assert_called_once()

    def test_magic_mock_automatic_attributes(self):
        """
        MagicMock usage - automatically handles attribute access
        
        MagicMock automatically creates attributes and methods when accessed.
        This makes it more convenient for complex object mocking.
        """
        # Create a MagicMock
        magic_mock = MagicMock()

        # Attributes are automatically created when accessed
        magic_mock.name = "Magic Name"
        magic_mock.age = 30

        # Methods are automatically created and can be configured
        magic_mock.calculate.return_value = 100
        magic_mock.process_data.return_value = {"result": "success"}

        # Use the mock
        assert magic_mock.name == "Magic Name"
        assert magic_mock.age == 30
        assert magic_mock.calculate(5, 5) == 100
        assert magic_mock.process_data("input") == {"result": "success"}

        # Verify calls
        magic_mock.calculate.assert_called_once_with(5, 5)
        magic_mock.process_data.assert_called_once_with("input")

    def test_mock_vs_magic_mock_attribute_access(self):
        """
        Demonstrate the key difference: automatic attribute creation
        
        Mock: Raises AttributeError for undefined attributes
        MagicMock: Automatically creates attributes when accessed
        """
        # Mock behavior - explicit setup required
        basic_mock = Mock()
        basic_mock.explicit_attr = "explicit value"

        # This works because we explicitly set it
        assert basic_mock.explicit_attr == "explicit value"

        # This would raise AttributeError if not explicitly set
        # basic_mock.undefined_attr  # Would raise AttributeError

        # MagicMock behavior - automatic attribute creation
        magic_mock = MagicMock()

        # These work automatically without explicit setup
        magic_mock.auto_attr = "auto value"
        magic_mock.another_attr = "another value"

        # Even accessing new attributes creates them
        magic_mock.new_attr = "new value"

        assert magic_mock.auto_attr == "auto value"
        assert magic_mock.another_attr == "another value"
        assert magic_mock.new_attr == "new value"

    def test_mock_vs_magic_mock_method_calls(self):
        """
        Demonstrate method call differences between Mock and MagicMock
        """
        # Mock - methods need to be explicitly configured
        basic_mock = Mock()
        basic_mock.add.return_value = 10
        basic_mock.multiply.return_value = 20

        # These work because we explicitly configured them
        assert basic_mock.add(2, 3) == 10
        assert basic_mock.multiply(4, 5) == 20

        # MagicMock - methods are automatically created
        magic_mock = MagicMock()
        magic_mock.add.return_value = 15
        magic_mock.multiply.return_value = 25
        magic_mock.divide.return_value = 5  # This method didn't exist before

        # All methods work automatically
        assert magic_mock.add(3, 4) == 15
        assert magic_mock.multiply(5, 6) == 25
        assert magic_mock.divide(10, 2) == 5  # Automatically created

    def test_mock_with_spec_vs_magic_mock_with_spec(self):
        """
        Demonstrate spec usage with both Mock and MagicMock
        
        Spec limits the available attributes to those defined in the spec object.
        """
        # Mock with spec - only allows attributes from Calculator class
        mock_with_spec = Mock(spec=Calculator)

        # These work because Calculator has these methods
        mock_with_spec.add.return_value = 5
        mock_with_spec.multiply.return_value = 10
        mock_with_spec.get_history.return_value = []

        assert mock_with_spec.add(2, 3) == 5
        assert mock_with_spec.multiply(2, 5) == 10
        assert mock_with_spec.get_history() == []

        # This would raise AttributeError because Calculator doesn't have this method
        # mock_with_spec.invalid_method()  # Would raise AttributeError

        # MagicMock with spec - same behavior as Mock with spec
        magic_mock_with_spec = MagicMock(spec=Calculator)

        magic_mock_with_spec.add.return_value = 7
        magic_mock_with_spec.multiply.return_value = 14

        assert magic_mock_with_spec.add(3, 4) == 7
        assert magic_mock_with_spec.multiply(3, 5) == 14

        # This would also raise AttributeError
        # magic_mock_with_spec.invalid_method()  # Would raise AttributeError


# ============================================================================
# pytest-mock Examples (using mocker fixture)
# ============================================================================

class TestPytestMockMocker:
    """
    Examples using pytest-mock's mocker fixture
    
    The mocker fixture provides a cleaner interface for mocking in pytest.
    It automatically handles cleanup and provides convenient methods.
    """

    def test_mocker_fixture_basic_usage(self, mocker):
        """
        Basic usage of the mocker fixture
        
        The mocker fixture provides methods that mirror unittest.mock functions
        but with automatic cleanup after the test.
        """
        # Create a mock using mocker fixture
        mock_obj = mocker.Mock()
        mock_obj.method.return_value = "mocked result"

        # Use the mock
        result = mock_obj.method("arg1", "arg2")
        assert result == "mocked result"

        # Verify the call
        mock_obj.method.assert_called_once_with("arg1", "arg2")

    def test_mocker_patch_function(self, mocker):
        """
        Patch a function using mocker.patch()
        
        This is equivalent to using @patch decorator but with automatic cleanup.
        """
        # Patch the sample_function
        mock_func = mocker.patch('backend.sample.sample_function')
        mock_func.return_value = "mocked hello"

        # Call the function (it will return the mocked value)
        result = sample_function()
        assert result == "mocked hello"

        # Verify it was called
        mock_func.assert_called_once()

    def test_mocker_patch_object(self, mocker):
        """
        Patch an object's method using mocker.patch.object()
        
        Useful for patching methods of existing objects or classes.
        """
        # Create a calculator instance
        calc = Calculator()

        # Patch the add method
        mock_add = mocker.patch.object(calc, 'add')
        mock_add.return_value = 999

        # Call the method
        result = calc.add(2, 3)
        assert result == 999

        # Verify the call
        mock_add.assert_called_once_with(2, 3)

    def test_mocker_patch_multiple(self, mocker):
        """
        Patch multiple functions/objects in one test
        
        The mocker fixture can handle multiple patches automatically.
        """
        # Patch multiple functions
        mock_validate = mocker.patch('backend.sample.validate_email')
        mock_process = mocker.patch('backend.sample.process_user_data')

        # Configure return values
        mock_validate.return_value = True
        mock_process.return_value = {"processed": True}

        # Use the mocked functions
        is_valid = validate_email("test@example.com")
        processed = process_user_data({"name": "test", "email": "test@example.com", "age": 25})

        # Verify results
        assert is_valid is True
        assert processed["processed"] is True

        # Verify calls
        mock_validate.assert_called_once_with("test@example.com")
        mock_process.assert_called_once()

    def test_mocker_side_effect(self, mocker):
        """
        Use side_effect with mocker for complex behavior
        
        side_effect can be a function, exception, or iterable.
        """
        # Mock with side effect function
        def mock_side_effect(x, y):
            return x * y + 10

        mock_add = mocker.patch('backend.sample.add_number')
        mock_add.side_effect = mock_side_effect

        # Test the side effect
        result = add_number(3, 4)
        assert result == 22  # 3 * 4 + 10

        # Mock with exception side effect
        mock_divide = mocker.patch('backend.sample.divide_numbers')
        mock_divide.side_effect = ValueError("Mocked error")

        # Test exception side effect
        with pytest.raises(ValueError, match="Mocked error"):
            divide_numbers(10, 2)

    def test_mocker_spec(self, mocker):
        """
        Use spec with mocker to limit mock attributes
        
        spec ensures the mock only has attributes from the specified object.
        """
        # Create a mock with spec from Calculator class
        mock_calc = mocker.Mock(spec=Calculator)

        # Configure allowed methods
        mock_calc.add.return_value = 5
        mock_calc.multiply.return_value = 12

        # These work because they're in the spec
        assert mock_calc.add(2, 3) == 5
        assert mock_calc.multiply(3, 4) == 12

        # This would raise AttributeError because 'invalid_method' is not in Calculator
        # mock_calc.invalid_method()  # Would raise AttributeError

    def test_mocker_patch_context_manager(self, mocker):
        """
        Use mocker.patch as context manager for temporary patching
        
        Useful when you only want to patch for part of a test.
        """
        # First, verify normal behavior
        result1 = sample_function()
        assert result1 == "Hello, World!"

        # Use patch as context manager
        with mocker.patch('backend.sample.sample_function') as mock_func:
            mock_func.return_value = "Temporary mock"
            
            # Inside context, function is mocked
            result2 = sample_function()
            assert result2 == "Temporary mock"

        # Outside context, function returns to normal
        result3 = sample_function()
        assert result3 == "Hello, World!"

    def test_mocker_patch_dict(self, mocker):
        """
        Use mocker.patch.dict() to temporarily modify dictionaries
        
        Useful for mocking environment variables, configuration, etc.
        """
        # Example: mock environment variables
        test_env = {"API_KEY": "test_key", "DEBUG": "True"}
        
        with mocker.patch.dict('os.environ', test_env):
            import os
            assert os.environ["API_KEY"] == "test_key"
            assert os.environ["DEBUG"] == "True"

    def test_mocker_with_fixtures(self, mocker, calculator):
        """
        Combine mocker with pytest fixtures
        
        This shows how to use mocker with existing fixtures.
        """
        # Use the calculator fixture but mock its methods
        mock_add = mocker.patch.object(calculator, 'add')
        mock_add.return_value = 100

        # Test with mocked method
        result = calculator.add(5, 5)
        assert result == 100

        # Verify the mock was called
        mock_add.assert_called_once_with(5, 5)

    def test_mocker_parametrized(self, mocker):
        """
        Use mocker with parametrized tests
        
        Each test run gets a fresh mock instance.
        """
        # Patch the function
        mock_func = mocker.patch('backend.sample.add_number')
        
        # Configure different return values for different calls
        mock_func.side_effect = [10, 20, 30]

        # Test multiple calls
        assert add_number(1, 1) == 10
        assert add_number(2, 2) == 20
        assert add_number(3, 3) == 30

        # Verify all calls
        assert mock_func.call_count == 3


# ============================================================================
# Comparison: unittest.mock vs pytest-mock
# ============================================================================

class TestMockComparison:
    """
    Side-by-side comparison of unittest.mock vs pytest-mock approaches
    """

    def test_unittest_mock_approach(self):
        """
        Example using unittest.mock directly
        
        Pros:
        - No external dependencies
        - Full control over mock behavior
        - Works outside pytest
        
        Cons:
        - More verbose syntax
        - Manual cleanup required
        - Less integration with pytest features
        """
        from unittest.mock import Mock, patch
        
        # Create mock directly
        mock_calc = Mock()
        mock_calc.add.return_value = 10
        
        # Test with direct mock
        result = mock_calc.add(3, 7)
        assert result == 10
        mock_calc.add.assert_called_once_with(3, 7)
        
        # Using patch decorator
        with patch('backend.sample.add_number') as mock_add:
            mock_add.return_value = 100
            result = add_number(5, 5)
            assert result == 100

    def test_pytest_mock_approach(self, mocker):
        """
        Example using pytest-mock mocker fixture
        
        Pros:
        - Automatic cleanup
        - Cleaner syntax
        - Better pytest integration
        - Easier multiple patches
        
        Cons:
        - Requires pytest-mock package
        - Only works in pytest context
        """
        # Create mock using fixture
        mock_calc = mocker.Mock()
        mock_calc.add.return_value = 10
        
        # Test with fixture mock
        result = mock_calc.add(3, 7)
        assert result == 10
        mock_calc.add.assert_called_once_with(3, 7)
        
        # Using mocker.patch
        mock_add = mocker.patch('backend.sample.add_number')
        mock_add.return_value = 100
        result = add_number(5, 5)
        assert result == 100

    def test_multiple_patches_comparison(self, mocker):
        """
        Compare multiple patches: unittest.mock vs pytest-mock
        """
        # pytest-mock approach (cleaner)
        mock_validate = mocker.patch('backend.sample.validate_email')
        mock_process = mocker.patch('backend.sample.process_user_data')
        mock_calc = mocker.patch('backend.sample.Calculator')
        
        # Configure mocks
        mock_validate.return_value = True
        mock_process.return_value = {"processed": True}
        mock_calc.return_value.add.return_value = 50
        
        # Test
        assert validate_email("test@example.com") is True
        assert process_user_data({})["processed"] is True
        
        # Verify calls
        mock_validate.assert_called_once()
        mock_process.assert_called_once()

    def test_side_by_side_complex_example(self, mocker):
        """
        Complex example showing both approaches for the same test
        """
        # pytest-mock approach (recommended for pytest tests)
        mock_api = mocker.patch('backend.sample.get_user_by_api')
        mock_validate = mocker.patch('backend.sample.validate_email')
        
        # Configure complex behavior
        mock_api.return_value = "https://api.example.com/users"
        mock_validate.side_effect = [True, False, True]
        
        # Test the behavior
        api_url = get_user_by_api(page=1)
        assert api_url == "https://api.example.com/users"
        
        # Test side effect
        assert validate_email("valid@example.com") is True
        assert validate_email("invalid@example.com") is False
        assert validate_email("another@example.com") is True
        
        # Verify calls
        mock_api.assert_called_once_with(page=1)
        assert mock_validate.call_count == 3


class TestMockSpecExplained:
    """
    Comprehensive explanation of Mock spec parameter
    
    What is spec?
    - spec is a parameter that tells the mock what attributes it should have
    - It acts like a "blueprint" or "template" for the mock object
    - It prevents you from accessing attributes that don't exist in the real object
    - It helps catch typos and interface mismatches early
    """

    def test_what_is_spec_basic_explanation(self):
        """
        Basic explanation: What is spec?
        
        Think of spec as a "contract" that defines what the mock object can do.
        It's like saying "this mock should behave like this specific class/object"
        """
        # Without spec - you can access any attribute (even typos!)
        mock_without_spec = Mock()
        mock_without_spec.anything_you_want = "works"
        mock_without_spec.typo_here = "also works"
        mock_without_spec.nonexistent_method.return_value = "still works"

        # All of these work, even though they might be mistakes
        assert mock_without_spec.anything_you_want == "works"
        assert mock_without_spec.typo_here == "also works"
        assert mock_without_spec.nonexistent_method() == "still works"

        # With spec - you can only access attributes that exist in the spec
        mock_with_spec = Mock(spec=Calculator)

        # These work because Calculator has these methods
        mock_with_spec.add.return_value = 5
        mock_with_spec.multiply.return_value = 10
        mock_with_spec.get_history.return_value = []
        mock_with_spec.clear_history.return_value = None

        assert mock_with_spec.add(2, 3) == 5
        assert mock_with_spec.multiply(2, 5) == 10
        assert mock_with_spec.get_history() == []
        assert mock_with_spec.clear_history() is None

        # These would raise AttributeError because Calculator doesn't have them
        # mock_with_spec.typo_here = "error!"  # AttributeError
        # mock_with_spec.nonexistent_method()  # AttributeError

    def test_spec_with_different_types(self):
        """
        Spec can be used with different types of objects:
        - Classes (like Calculator)
        - Instances (like Calculator())
        - Lists of attribute names
        """
        # Spec with a class
        mock_from_class = Mock(spec=Calculator)
        mock_from_class.add.return_value = 10
        assert mock_from_class.add(5, 5) == 10

        # Spec with a list of attribute names
        mock_from_list = Mock(spec=['add', 'multiply', 'divide'])
        mock_from_list.add.return_value = 20
        assert mock_from_list.add(10, 10) == 20

        # This would raise AttributeError because 'subtract' is not in the spec list
        # mock_from_list.subtract.return_value = 5  # AttributeError

    def test_spec_vs_spec_set(self):
        """
        Difference between spec and spec_set
        
        - spec: Allows you to set new attributes (but not access undefined ones)
        - spec_set: Prevents both setting and accessing undefined attributes
        """
        # Mock with spec - can set new attributes
        mock_with_spec = Mock(spec=Calculator)
        mock_with_spec.add.return_value = 5

        # This works - you can set new attributes
        mock_with_spec.new_attribute = "new value"
        assert mock_with_spec.new_attribute == "new value"

        # This would raise AttributeError - can't access undefined attributes
        # mock_with_spec.undefined_method()  # AttributeError

        # Mock with spec_set - cannot set new attributes
        mock_with_spec_set = Mock(spec_set=Calculator)
        mock_with_spec_set.add.return_value = 5

        # This would raise AttributeError - can't set new attributes
        # mock_with_spec_set.new_attribute = "new value"  # AttributeError

        # This would also raise AttributeError - can't access undefined attributes
        # mock_with_spec_set.undefined_method()  # AttributeError

        # Only existing attributes work
        assert mock_with_spec_set.add(2, 3) == 5

    def test_mock_configuration_methods(self):
        """
        Demonstrate configuration methods available on both Mock and MagicMock
        """
        # Both Mock and MagicMock support these configuration methods
        mock_obj = Mock()
        magic_obj = MagicMock()

        # configure_mock - set multiple attributes at once
        mock_obj.configure_mock(
            name="Mock Name",
            age=25,
            get_info=Mock(return_value="Mock info")
        )

        magic_obj.configure_mock(
            name="Magic Name",
            age=30,
            get_info=MagicMock(return_value="Magic info")
        )

        assert mock_obj.name == "Mock Name"
        assert mock_obj.age == 25
        assert mock_obj.get_info() == "Mock info"

        assert magic_obj.name == "Magic Name"
        assert magic_obj.age == 30
        assert magic_obj.get_info() == "Magic info"

        # reset_mock - reset call counts and call history
        mock_obj.get_info()
        magic_obj.get_info()

        assert mock_obj.get_info.call_count == 1
        assert magic_obj.get_info.call_count == 1

        mock_obj.reset_mock()
        magic_obj.reset_mock()

        assert mock_obj.get_info.call_count == 0
        assert magic_obj.get_info.call_count == 0

    def test_mock_vs_magic_mock_performance(self):
        """
        Demonstrate when to use Mock vs MagicMock
        
        Use Mock when:
        - You want explicit control over attributes
        - You want to catch AttributeError for undefined attributes
        - You're mocking simple objects with known interfaces
        
        Use MagicMock when:
        - You're mocking complex objects with many attributes
        - You want convenience of automatic attribute creation
        - You're mocking objects with dynamic attribute access
        """
        # Mock - good for simple, explicit mocking
        simple_mock = Mock()
        simple_mock.value = 42
        simple_mock.get_value.return_value = 42

        # This is explicit and clear
        assert simple_mock.value == 42
        assert simple_mock.get_value() == 42

        # MagicMock - good for complex object mocking
        complex_mock = MagicMock()

        # Can easily mock complex nested structures
        complex_mock.database.users.get_user.return_value = {"id": 1, "name": "John"}
        complex_mock.api.v1.endpoints.list.return_value = [1, 2, 3]

        # These work automatically
        user = complex_mock.database.users.get_user(1)
        endpoints = complex_mock.api.v1.endpoints.list()

        assert user == {"id": 1, "name": "John"}
        assert endpoints == [1, 2, 3]

        # Verify the complex call chain
        complex_mock.database.users.get_user.assert_called_once_with(1)
        complex_mock.api.v1.endpoints.list.assert_called_once()


class TestBasicMocking:
    """Test class demonstrating basic mocking techniques"""

    def test_mock_calculator_with_magic_mock(self):
        """Test using MagicMock for calculator"""
        mock_calc = MagicMock()
        mock_calc.add.return_value = 10

        result = mock_calc.add(3, 7)
        assert result == 10
        mock_calc.add.assert_called_once_with(3, 7)

    def test_mock_with_property_mocking(self):
        """Test mocking object properties"""
        mock_obj = MagicMock()
        mock_obj.name = "Mocked Name"
        mock_obj.age = 25

        assert mock_obj.name == "Mocked Name"
        assert mock_obj.age == 25

    def test_mock_with_configure_mock(self):
        """Test using configure_mock for complex mock setup"""
        mock_obj = MagicMock()
        mock_obj.configure_mock(
            name="Configured Name",
            age=30,
            get_info=MagicMock(return_value="Mocked info")
        )

        assert mock_obj.name == "Configured Name"
        assert mock_obj.age == 30
        assert mock_obj.get_info() == "Mocked info"

    def test_mock_with_spec(self):
        """Test mock with spec to limit available attributes"""
        # Create a mock with spec from Calculator class
        mock_calc = MagicMock(spec=Calculator)

        # These should work (Calculator has these methods)
        mock_calc.add.return_value = 5
        mock_calc.multiply.return_value = 10

        assert mock_calc.add(2, 3) == 5
        assert mock_calc.multiply(2, 5) == 10

        # This would raise AttributeError if Calculator doesn't have 'invalid_method'
        # mock_calc.invalid_method()  # Would raise AttributeError


class TestPatching:
    """Test class demonstrating patching techniques"""

    @patch('backend.sample.validate_email')
    def test_patch_function_with_decorator(self, mock_validate):
        """Test patching a function with @patch decorator"""
        mock_validate.return_value = True

        result = validate_email("test@example.com")
        assert result is True
        mock_validate.assert_called_once_with("test@example.com")

    def test_patch_function_with_context_manager(self):
        """Test patching a function with context manager"""
        with patch('backend.sample.validate_email') as mock_validate:
            mock_validate.return_value = False

            result = validate_email("invalid@email")
            assert result is False
            mock_validate.assert_called_once_with("invalid@email")

    @patch('backend.sample.Calculator')
    def test_patch_class_constructor(self, mock_calculator_class):
        """Test patching a class constructor"""
        mock_instance = MagicMock()
        mock_instance.add.return_value = 100
        mock_calculator_class.return_value = mock_instance

        calc = Calculator()
        result = calc.add(50, 50)

        assert result == 100
        mock_calculator_class.assert_called_once()
        mock_instance.add.assert_called_once_with(50, 50)

    @patch('builtins.open', create=True)
    def test_patch_builtin_function(self, mock_open):
        """Test patching built-in functions"""
        mock_file = MagicMock()
        mock_file.read.return_value = "mocked file content"
        mock_open.return_value.__enter__.return_value = mock_file

        with open('test.txt', 'r') as f:
            content = f.read()

        assert content == "mocked file content"
        mock_open.assert_called_once_with('test.txt', 'r')


class TestSideEffects:
    """Test class demonstrating side effects"""

    @patch('backend.sample.add_number')
    def test_patch_function_with_side_effect(self, mock_add):
        """Test patching with side_effect for different behaviors"""
        # Side effect can be a function or an exception
        mock_add.side_effect = lambda a, b: a * b  # Change behavior to multiplication

        result = add_number(3, 4)
        assert result == 12  # 3 * 4 = 12
        mock_add.assert_called_once_with(3, 4)

    @patch('backend.sample.calculate_fibonacci')
    def test_patch_with_exception_side_effect(self, mock_fib):
        """Test patching with exception side effect"""
        mock_fib.side_effect = ValueError("Mocked error")

        with pytest.raises(ValueError) as exc_info:
            calculate_fibonacci(10)

        assert "Mocked error" in str(exc_info.value)
        mock_fib.assert_called_once_with(10)

    def test_mock_with_multiple_calls(self):
        """Test mock with multiple calls and different return values"""
        mock_calc = MagicMock()
        mock_calc.add.side_effect = [10, 20, 30]  # Different return values for each call

        assert mock_calc.add(1, 2) == 10
        assert mock_calc.add(3, 4) == 20
        assert mock_calc.add(5, 6) == 30

        assert mock_calc.add.call_count == 3
        mock_calc.add.assert_has_calls([
            ((1, 2),),
            ((3, 4),),
            ((5, 6),)
        ])

    def test_mock_with_side_effect_exception(self):
        """Test mock with side_effect raising exceptions"""
        mock_func = MagicMock()
        mock_func.side_effect = [1, 2, ValueError("Error on third call")]

        assert mock_func() == 1
        assert mock_func() == 2

        with pytest.raises(ValueError) as exc_info:
            mock_func()

        assert "Error on third call" in str(exc_info.value)


class TestMockAssertions:
    """Test class demonstrating mock assertions"""

    @patch('backend.sample.get_user_by_api')
    def test_patch_with_call_args_list(self, mock_api):
        """Test mock with call_args_list to track multiple calls"""
        mock_api.return_value = "mocked_url"

        # Make multiple calls
        get_user_by_api(page=1)
        get_user_by_api(page=2)
        get_user_by_api(page=3)

        assert mock_api.call_count == 3
        assert mock_api.call_args_list[0] == ((1,), {'per_page': 6})
        assert mock_api.call_args_list[1] == ((2,), {'per_page': 6})
        assert mock_api.call_args_list[2] == ((3,), {'per_page': 6})

    @patch('backend.sample.add_number')
    def test_patch_with_call_any(self, mock_add):
        """Test mock with call_any to check if called with any arguments"""
        mock_add.return_value = 999

        add_number(1, 2)
        add_number(3, 4)

        # Check if called with any arguments
        mock_add.assert_any_call(1, 2)
        mock_add.assert_any_call(3, 4)
        assert mock_add.call_count == 2

    @patch('backend.sample.sample_function')
    def test_patch_with_call_args(self, mock_sample):
        """Test mock with call_args to inspect last call arguments"""
        mock_sample.return_value = "mocked hello"

        sample_function()

        # Check the call arguments
        assert mock_sample.call_args == ((), {})  # No arguments passed
        assert mock_sample.call_args.args == ()
        assert mock_sample.call_args.kwargs == {}

    def test_mock_with_reset_mock(self):
        """Test mock reset functionality"""
        mock_obj = MagicMock()
        mock_obj.method.return_value = "first call"

        result1 = mock_obj.method()
        assert result1 == "first call"
        assert mock_obj.method.call_count == 1

        # Reset the mock
        mock_obj.reset_mock()
        assert mock_obj.method.call_count == 0

        # Configure new behavior
        mock_obj.method.return_value = "second call"
        result2 = mock_obj.method()
        assert result2 == "second call"
        assert mock_obj.method.call_count == 1


class TestAdvancedMocking:
    """Test class demonstrating advanced mocking scenarios"""

    @patch('backend.sample.process_user_data')
    def test_patch_with_return_value_and_assertions(self, mock_process):
        """Test patching with return value and various assertions"""
        mock_process.return_value = {
            'formatted_name': 'Mocked User',
            'email_domain': 'mock.com',
            'age_group': 'adult'
        }

        user_data = {'name': 'test', 'email': 'test@test.com', 'age': 30}
        result = process_user_data(user_data)

        assert result['formatted_name'] == 'Mocked User'
        assert result['email_domain'] == 'mock.com'
        assert result['age_group'] == 'adult'

        mock_process.assert_called_once_with(user_data)

    @patch('backend.sample.validate_email')
    @patch('backend.sample.process_user_data')
    def test_multiple_patches(self, mock_process, mock_validate):
        """Test using multiple patches on the same test"""
        mock_validate.return_value = True
        mock_process.return_value = {'age_group': 'adult'}

        # Test the workflow
        user_data = {'name': 'test', 'email': 'test@test.com', 'age': 25}

        is_valid = validate_email(user_data['email'])
        processed = process_user_data(user_data)

        assert is_valid is True
        assert processed['age_group'] == 'adult'

        mock_validate.assert_called_once_with('test@test.com')
        mock_process.assert_called_once_with(user_data)


# Additional standalone examples for specific use cases

# Mocking with fixtures
def test_mock_with_fixture(calculator):
    """Test combining mocks with fixtures"""
    # Use the real calculator fixture but mock its methods
    with patch.object(calculator, 'add') as mock_add:
        mock_add.return_value = 999

        result = calculator.add(1, 2)
        assert result == 999
        mock_add.assert_called_once_with(1, 2)


# Mocking with parametrization
@pytest.mark.parametrize("input_val,expected", [
    ("test@example.com", True),
    ("invalid-email", False)
])
@patch('backend.sample.validate_email')
def test_mock_with_parametrization(mock_validate, input_val, expected):
    """Test mocking with parametrized tests"""
    mock_validate.return_value = expected

    result = validate_email(input_val)
    assert result == expected
    mock_validate.assert_called_once_with(input_val)

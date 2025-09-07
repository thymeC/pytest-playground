# Pytest Playground

A comprehensive pytest learning project that demonstrates various pytest features and testing patterns through practical
examples.

## Features Demonstrated

### Core Pytest Features

- **Basic assertions** - Simple test cases with assert statements
- **Fixtures** - Reusable test data and setup/teardown
- **Parametrization** - Running tests with multiple input values (single and multiple parameters)
- **Exception testing** - Testing that functions raise expected exceptions
- **Markers** - Custom markers for test categorization (smoke, slow, integration)
- **Skip and SkipIf** - Conditional test skipping with various conditions
- **Repeat** - Running tests multiple times for flaky test detection

### Advanced Features

- **Mocking and Patching** - Comprehensive unittest.mock examples (Mock vs MagicMock, spec, side_effects)
- **Assertion types** - Various assertion methods and custom error messages
- **Temporary files** - Testing file operations with tempfile
- **Class-based testing** - Organizing tests in classes with proper structure
- **Session-scoped fixtures** - Fixtures that persist across test sessions
- **Auto-use fixtures** - Fixtures that run automatically

## Project Structure

```
pytest-playground/
├── backend/
│   └── sample.py                    # Sample functions and classes to test
├── tests/
│   ├── conftest.py                  # Shared fixtures and configuration
│   ├── test-sample.py               # Class-based test examples (focused on pytest features)
│   ├── test-assertion-message.py    # Assertion types and custom error messages
│   └── test-mock.py                 # Comprehensive mocking and patching examples
├── pytest.ini                      # Pytest configuration with custom markers
├── requirements.txt                 # Project dependencies
├── .gitignore                      # Git ignore file for Python projects
└── readme.md                       # This file
```

## Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

### Run all tests

```bash
pytest
```

### Run specific test file

```bash
pytest tests/test_sample.py              # Class-based examples (pytest features)
pytest tests/test_assertion_message.py   # Assertion types and custom messages
pytest tests/test_mock.py                # Comprehensive mocking and patching
```

### Run tests with verbose output

```bash
pytest -v
```

### Run tests with specific markers

```bash
pytest -m smoke          # Run only smoke tests
pytest -m slow           # Run only slow tests
pytest -m integration    # Run only integration tests
pytest -m "not slow"     # Run all except slow tests
```

### Run specific test classes

```bash
pytest tests/test_sample.py::TestBasicFunctions -v
pytest tests/test_sample.py::TestParametrizedTests -v
pytest tests/test_mock.py::TestMockVsMagicMock -v
```

### Run tests with repeat (requires pytest-repeat)

```bash
pytest tests/test_sample.py::TestMarkers::test_repeat_5_times -v
```

### Run tests with coverage

```bash
pytest --cov=backend tests/
```

## Test Examples

### Basic Test

```python
def test_add_number():
    result = add_number(2, 3)
    assert result == 5
```

### Parametrized Test (Multiple Parameters)

```python
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0)
])
def test_add_number_parametrized(a, b, expected):
    result = add_number(a, b)
    assert result == expected
```

### Parametrized Test (Single Parameter)

```python
@pytest.mark.parametrize("email", [
    "test@example.com",
    "user@domain.org",
    "admin@company.net"
])
def test_validate_email_single_param(email):
    result = validate_email(email)
    assert result is True
```

### Fixture Usage

```python
def test_with_fixture(calculator):
    result = calculator.add(2, 3)
    assert result == 5
```

### Exception Testing

```python
def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide_numbers(10, 0)
```

### Markers

```python
@pytest.mark.smoke
def test_basic_functionality():
    assert sample_function() is not None


@pytest.mark.slow
def test_expensive_operation():
    result = calculate_fibonacci(30)
    assert result > 0
```

### SkipIf Examples

```python
@pytest.mark.skipif(sys.version_info < (3, 8), reason="Requires Python 3.8+")
def test_python_version_feature():
    # Test code that requires Python 3.8+
    pass


@pytest.mark.skipif(not os.path.exists("/tmp"), reason="Requires /tmp directory")
def test_file_system_check():
    # Test code that requires specific file system
    pass
```

### Mock Examples

```python
def test_mock_example():
    with patch('backend.sample.validate_email') as mock_validate:
        mock_validate.return_value = True
        result = validate_email("test@example.com")
        assert result is True
        mock_validate.assert_called_once_with("test@example.com")
```

### Assertion with Custom Messages

```python
def test_assert_with_message():
    result = add_number(2, 3)
    assert result == 5, f"Expected 5, but got {result}"
```

## Learning Path

1. **Start with `test-sample.py`** - Class-based testing examples covering:
    - Basic functions and fixtures
    - Parametrization (single and multiple parameters)
    - Exception handling
    - Class testing
    - Markers (smoke, slow, integration)
    - SkipIf conditions
    - Repeat functionality

2. **Study `test-assertion-message.py`** - Assertion types and custom error messages:
    - Basic assertions
    - Comparison assertions
    - Membership and type assertions
    - Custom error messages
    - Approximate equality
    - Exception assertions with messages

3. **Explore `test-mock.py`** - Comprehensive mocking and patching:
    - Mock vs MagicMock differences
    - Basic mocking and patching
    - Side effects and return values
    - Mock assertions and verification
    - Spec and spec_set usage
    - Advanced mocking techniques

4. **Check `conftest.py`** - Shared fixtures and configuration:
    - Fixture definitions
    - Session-scoped fixtures
    - Auto-use fixtures
    - Fixture parameters

5. **Run different test combinations** to see pytest features in action
6. **Modify tests** to experiment with different pytest features

## Key Pytest Commands

- `pytest` - Run all tests
- `pytest -v` - Verbose output
- `pytest -k "test_name"` - Run tests matching pattern
- `pytest -m marker` - Run tests with specific marker
- `pytest --tb=short` - Short traceback format
- `pytest -x` - Stop on first failure
- `pytest --lf` - Run last failed tests only
- `pytest --repeat=5` - Repeat tests 5 times (requires pytest-repeat)
- `pytest --cov=backend` - Run with coverage report

## Dependencies

The project includes these key dependencies:

- `pytest` - Core testing framework
- `pytest-repeat` - Repeat tests multiple times
- `pytest-mock` - Enhanced mocking capabilities
- `pytest-cov` - Coverage reporting
- `pytest-benchmark` - Performance benchmarking
- `pytest-xdist` - Parallel test execution
- `pytest-html` - HTML test reports
- `pytest-json-report` - JSON test reports
- `pytest-asyncio` - Async test support


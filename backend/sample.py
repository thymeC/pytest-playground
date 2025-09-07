def sample_function():
    return "Hello, World!"


def sample_function_with_param(param):
    return f"Hello, {param}!"


def add_number(a, b):
    return a + b


def get_user_by_api(page=1, per_page=6):
    return f"https://reqres.in/api/users?page={page}&per_page={per_page}"


def divide_numbers(a, b):
    """Divide two numbers with error handling"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def process_user_data(user_data):
    """Process user data and return formatted result"""
    if not isinstance(user_data, dict):
        raise TypeError("user_data must be a dictionary")

    required_fields = ['name', 'email', 'age']
    for field in required_fields:
        if field not in user_data:
            raise KeyError(f"Missing required field: {field}")

    return {
        'formatted_name': user_data['name'].title(),
        'email_domain': user_data['email'].split('@')[1],
        'age_group': 'adult' if user_data['age'] >= 18 else 'minor'
    }


def calculate_fibonacci(n):
    """Calculate nth Fibonacci number"""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)


def validate_email(email):
    """Simple email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


class Calculator:
    """Simple calculator class for testing class methods"""

    def __init__(self):
        self.history = []

    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

    def multiply(self, a, b):
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result

    def get_history(self):
        return self.history.copy()

    def clear_history(self):
        self.history.clear()

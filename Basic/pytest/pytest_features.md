# A Guide to Pytest Features

Pytest is a powerful and popular Python testing framework that uses plain `assert` statements and a rich ecosystem of fixtures and plugins to simplify testing.

Documentation: <https://docs.pytest.org/en/stable/>

---

## 1. Simple Assertions

Pytest uses standard `assert` statements for checking conditions, which keeps tests clean and readable. When an assertion fails, pytest provides detailed output showing the values of the variables involved, which makes debugging much easier than with traditional `unittest` `self.assertEqual()` style methods.

**Example:**

```python
def test_addition():
    assert 1 + 1 == 2

def test_string_concatenation():
    result = "hello" + " " + "world"
    assert result == "hello world"
```

If a test fails, the output will clearly show the difference between the expected and actual values.

## 2. Fixtures

Fixtures are the cornerstone of pytest. They are functions that provide a fixed baseline state or data for your tests. They use dependency injection, making them modular and reusable. You can think of them as providing the "context" for your tests.

**Key Concepts:**

* **Declaration:** Use the `@pytest.fixture` decorator.
* **Usage:** A test function can receive a fixture by simply including its name as an argument.
* **Scope:** Fixtures can be configured to run once per function, class, module, or the entire session.

**Example:**

```python
import pytest

@pytest.fixture
def sample_data():
    """A fixture that provides some sample data."""
    return {"user": "test_user", "id": 123}

def test_user_name(sample_data):
    """This test uses the sample_data fixture."""
    assert sample_data["user"] == "test_user"
```

## 3. Built-in Fixtures

Pytest comes with many useful built-in fixtures. The ones you've used are excellent examples:

* **`monkeypatch`**: Safely modify or mock objects, environment variables, or dictionaries for the duration of a test without affecting other tests. In your code, you use it to manage environment variables (`monkeypatch.setenv`, `monkeypatch.delenv`) and to mock the `dotenv.load_dotenv` function.

    ```python
    def test_with_env_var(monkeypatch):
        monkeypatch.setenv("MY_VAR", "my_value")
        # ... test code that uses MY_VAR ...

    def test_mocking_function(monkeypatch):
        # Patch a function to return a fixed value
        monkeypatch.setattr("os.path.exists", lambda path: True)
        assert os.path.exists("/any/path") is True
    ```

* **`tmp_path`**: Provides a temporary directory (`pathlib.Path` object) unique to the test invocation, which is great for tests that need to read or write files.

* **`capsys`**: Captures and allows you to inspect anything written to `stdout` and `stderr` during a test.

## 4. Parameterization

You can run the same test function with different arguments without writing a loop. This is done with the `@pytest.mark.parametrize` decorator. It's excellent for testing a function against a variety of inputs and expected outputs.

**Example:**

```python
import pytest

@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (5, 5, 10),
    (-1, 1, 0),
])
def test_add(a, b, expected):
    assert a + b == expected
```

## 5. Markers

Markers allow you to categorize your tests. You can then choose to run only tests with specific markers.

* `@pytest.mark.skip(reason="...")`: Always skip a test.
* `@pytest.mark.skipif(condition, reason="...")`: Skip a test if a condition is met.
* `@pytest.mark.xfail(reason="...")`: Mark a test as "expected to fail". If it fails, it won't be reported as a failure. If it unexpectedly passes, it's reported as an `XPASS`.
* **Custom Markers:** You can define your own markers (e.g., `@pytest.mark.slow`, `@pytest.mark.api`) to group tests and run them selectively with the `-m` flag (e.g., `pytest -m slow`).

## 6. Test Discovery

Pytest has a simple and powerful way of discovering tests automatically:

* **Files:** It looks for files named `test_*.py` or `*_test.py`.
* **Functions:** Inside those files, it collects functions prefixed with `test_`.
* **Classes:** It collects classes prefixed with `Test` that do not have an `__init__` method, and runs their methods prefixed with `test_`.

## 7. Plugins

Pytest's functionality can be extended with a vast library of plugins. Some popular ones include:

* **`pytest-cov`**: For measuring code coverage.
* **`pytest-xdist`**: For running tests in parallel to speed up your test suite.
* **`pytest-mock`**: Provides a `mocker` fixture, which is a thin wrapper around the standard `unittest.mock` library.

By leveraging these features, you can write tests that are more readable, maintainable, and robust.

---

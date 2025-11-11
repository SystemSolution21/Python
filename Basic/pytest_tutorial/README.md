# Pytest Tutorial

A standalone pytest tutorial package demonstrating testing best practices.

## Project Structure

```current directory
/pytest_tutorial/
├── src/                 # Source code isolated
│   ├── __init__.py
│   ├── employee.py
│   └── calc.py
├── tests/               # Tests separate from source
│   ├── __init__.py
│   ├── test_calc.py
│   ├── test_employee.py
├── pyproject.toml
├── pytest_features.md
└── README.md
```

## Features

- Basic pytest examples
- Fixture usage
- Mocking with pytest-mock
- Parameterized tests

## Installation

```bash
cd ./pytest_tutorial
pip install -e .
```

## Running Tests

```bash
pytest
```

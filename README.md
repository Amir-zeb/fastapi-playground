# FastAPI Practice

A simple FastAPI application for learning API development, validation, SQLAlchemy, authentication, middleware, and testing.

## Requirements

* Python 3.13+
* [uv](https://docs.astral.sh/uv/)

## Setup

Install dependencies:

```bash
uv sync
```

## Run the Application

Start the development server:

```bash
uv run uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

## Run Tests

Run all tests:

```bash
uv run pytest
```

Run tests with verbose output:

```bash
uv run pytest -v
```

Run single test with verbose output:

```bash
uv run pytest tests/filename.py -v
```

## Type Checking

Run the type checker with `mypy`:

```bash
uv run mypy .
```

If `mypy` is not installed:

```bash
uv add --dev mypy
```

## Project Commands

### Install dependencies

```bash
uv sync
```

### Add a dependency

```bash
uv add <package>
```

### Add a development dependency

```bash
uv add --dev <package>
```
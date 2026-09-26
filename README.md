# FastAPI Practice

A learning project covering FastAPI fundamentals: request validation, SQLAlchemy, JWT-based authentication with httponly cookies, role-based access control (RBAC), custom exception handling, static type checking with mypy, and a pytest test suite with coverage reporting.

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

## Features

* JWT-based login, issued as an httponly, samesite cookie (`access_token`)
* Custom exception hierarchy (`AppException` and subclasses) mapped to consistent JSON error responses via FastAPI exception handlers
* Auth and role checks implemented as FastAPI dependencies (not middleware) — see `app/dependencies.py`
* Role-based access control: `/user/*` routes require the `admin` role, enforced via a `authorized(roles)` dependency factory
* In-memory, per-key rate limiting on `/auth/login` (see `app/utils/rate_limiter.py`) — 5 requests per 60 seconds by IP+route
* Response schemas built with Pydantic (`from_attributes = True`) to keep sensitive fields (e.g. password hashes) out of API responses

## Run Tests

Tests use an isolated in-memory SQLite database (via `dependency_overrides`), never the real dev database.

Run all tests:

```bash
uv run pytest
```

Run tests with verbose output:

```bash
uv run pytest -v
```

Run a single test file with verbose output:

```bash
uv run pytest tests/filename.py -v
```

### Coverage

Coverage runs automatically (see `pyproject.toml`'s `addopts`). To run it explicitly:

```bash
uv run pytest --cov=app --cov-report=term-missing tests/
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

## Project Structure

```text
├─ .python-version
├─ app
│  ├─ database.py
│  ├─ dependencies.py
│  ├─ exceptions.py
│  ├─ models
│  │  ├─ user.py
│  │  └─ __init__.py
│  ├─ routes
│  │  ├─ auth.py
│  │  ├─ user.py
│  │  └─ __init__.py
│  ├─ schema
│  │  ├─ api_response.py
│  │  ├─ auth.py
│  │  ├─ user.py
│  │  └─ __init__.py
│  ├─ services
│  │  ├─ auth_service.py
│  │  ├─ user_service.py
│  │  └─ __init__.py
│  ├─ utils
│  │  ├─ jwt.py
│  │  ├─ password.py
│  │  ├─ rate_limiter.py
│  │  ├─ response.py
│  │  └─ __init__.py
│  └─ __init__.py
├─ main.py
├─ pyproject.toml
├─ README.md
├─ test.db
├─ tests
│  ├─ conftest.py
│  ├─ test_auth.py
│  ├─ test_exceptions.py
│  ├─ test_password.py
│  └─ test_user.py
└─ uv.lock

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

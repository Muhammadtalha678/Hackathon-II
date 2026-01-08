---
name: fastapi-sqlmodel-backend-generator
description: Generates a clean, production-ready FastAPI backend project structure with SQLModel ORM, supporting any SQL database and ready for any domain/business logic.
license: Complete terms in LICENSE.txt
---

# FastAPI SQLModel Backend Generator

This skill scaffolds a generic, reusable FastAPI backend with proper architectural patterns (models, controllers, routers) and database connectivity. It provides a clean foundation that developers can extend for ANY project domain (e-commerce, blog, inventory, social media, etc.) without domain-specific code.

## Purpose

Generate a production-ready FastAPI backend project with SQLModel ORM that supports any SQL database. The skill creates a clean architectural foundation with separation of concerns, comprehensive error handling, and proper dependency injection patterns.

## When to Use

Use this skill when you need to:
- Initialize a new FastAPI project with SQLModel ORM
- Create a professional backend structure with models, controllers, and routers
- Set up database connectivity for PostgreSQL, MySQL, SQL Server, SQLite, Neon, or other SQL databases
- Generate a foundation that can be extended for any domain/business logic
- Create a project with proper error handling and type safety

## How to Use the Skill

### Initialize a New Backend Project

To generate a new FastAPI backend project:

1. Use the `uv init` command to create a new project:
   ```
   uv init projectname
   ```

2. Determine the project requirements:
   - Project name (default: "backend")
   - Database type (postgresql, mysql, sqlserver, sqlite, neon)
   - Whether to include example models/controllers/routers (default: true)
   - Minimum Python version (default: "3.11+")

3. Execute the project generation with the following parameters:
   - project_name: Name of the backend project
   - database_type: Database type hint for configuration
   - include_examples: Whether to include example model/controller/router as reference
   - python_version: Minimum Python version requirement

5. The skill will create the following folder structure:
   ```
   {project_name}/
   ├── src/
   │   ├── models/
   │   │   ├── base.py (base model with common fields)
   │   │   └── example_model.py (if include_examples=true)
   │   ├── controllers/
   │   │   └── example_controller.py (if include_examples=true)
   │   ├── routers/
   │   │   └── example_router.py (if include_examples=true)
   │   └── lib/
   │       ├── db_connect.py (database connection manager)
   │       ├── env_config.py (environment configuration)
   │       ├── session.py (session dependency)
   │       └── exceptions.py (custom exceptions)
   ├── tests/
   │   └── test_example.py (if include_examples=true)
   ├── .env.example
   ├── .gitignore
   ├── pyproject.toml
   ├── README.md
   └── main.py
   ```

6. The skill will generate comprehensive template files with detailed docstrings and type annotations.

### Authentication Configuration

The skill includes JWT-based authentication middleware with support for tokens from both headers and cookies:

- **Token Verification**: Middleware that verifies JWT tokens from either Authorization header or access_token cookie
- **Secret Management**: Uses BETTER_AUTH_SECRET from environment variables
- **User Validation**: Verifies that the user exists in the database
- **Flexible Token Source**: Supports both "Bearer <token>" header format and "access_token" cookie

Configuration in .env:
- BETTER_AUTH_SECRET: JWT secret key for token signing/verification
- JWT_ALGORITHM: Algorithm for JWT signing (default: HS256)
- JWT_ACCESS_TOKEN_EXPIRE_MINUTES: Token expiration time (default: 30 minutes)

### Database Configuration

The skill supports multiple SQL databases through flexible configuration:
- PostgreSQL: postgresql+psycopg2://user:pass@host:5432/db
- MySQL: mysql+pymysql://user:pass@host:3306/db
- SQL Server: mssql+pyodbc://user:pass@host:1433/db?driver=...
- SQLite: sqlite:///./database.db
- Neon: postgresql+psycopg2://user:pass@neon-host/db

### Project Initialization Process

1. Create the project directory structure using `uv init`:
   ```
   uv init projectname
   ```

2. Create a virtual environment using uv:
   ```
   uv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source .venv/bin/activate
     ```

4. Add the required libraries using uv:
   ```
   uv add fastapi uvicorn[standard] sqlmodel python-dotenv pyjwt psycopg2-binary
   ```
   (Add other database drivers as needed: pymysql for MySQL, pyodbc for SQL Server)

5. Generate configuration files (.env.example, .gitignore, pyproject.toml)
6. Create the main application entry point (main.py)
7. Generate base model with common fields and utilities
8. Create database connection manager with session handling
9. Implement environment configuration loader with JWT settings
10. Add custom exception classes for structured error handling
11. Include authentication middleware for JWT token verification
12. Include example models/controllers/routers if requested
13. Generate comprehensive README documentation

## Scripts

The skill includes the following scripts in the `scripts/` directory:
- `generate_backend.py`: Main script to generate the FastAPI backend structure

## Assets

The skill includes the following asset templates in the `assets/` directory:
- Project templates for models, controllers, routers
- Configuration file templates
- Documentation templates
- Test file templates
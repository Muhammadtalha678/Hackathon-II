# .

A production-ready FastAPI backend with SQLModel ORM, supporting any SQL database.

## 🎯 Features

- ✨ **Clean Architecture**: Separated concerns (models, controllers, routers)
- 🗄️ **Universal Database Support**: PostgreSQL, MySQL, SQL Server, SQLite, Neon, etc.
- 🔄 **SQLModel ORM**: Type-safe database operations with Pydantic validation
- 🏗️ **Scalable Structure**: Ready for any domain (e-commerce, blog, inventory, etc.)
- 📝 **Comprehensive Documentation**: Detailed docstrings and examples
- 🧪 **Error Handling**: Custom exceptions and proper error responses
- 🔒 **Type Safety**: Full type hints throughout the codebase
- 🚀 **Production Ready**: Lifespan management, CORS, health checks

## 📁 Project Structure

```
./
├── src/
│   ├── models/
│   │   ├── base.py (base model with common fields)
│   │   ├── user.py (user model for authentication)
│   │   └── task.py (task model with user relationship)
│   ├── controllers/
│   │   └── task_controller.py (task operations with user validation)
│   ├── routers/
│   │   └── task_router.py (task management endpoints)
│   └── lib/
│       ├── auth.py (JWT authentication middleware)
│       ├── db_connect.py (database connection manager)
│       ├── env_config.py (environment configuration)
│       ├── session.py (session dependency)
│       └── exceptions.py (custom exceptions)
├── tests/
│   └── test_tasks.py (task management tests)
├── .env.example
├── .gitignore
├── pyproject.toml
├── README.md
└── main.py
```

## 🚀 Quick Start

1. **Clone or generate this project**

2. **Install dependencies**:
   ```bash
   uv pip install -r requirements.txt
   # or if using pip
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and JWT settings
   ```

4. **Run the application**:
   ```bash
   uvicorn main:app --reload
   # or
   python -m uvicorn main:app --reload
   ```

5. **Access the application**:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## 📋 API Endpoints

### Task Management API

This backend implements JWT-authenticated task management with user-specific data isolation:

- **GET** `/api/{user_id}/tasks` - List all tasks for a user
- **POST** `/api/{user_id}/tasks` - Create a new task for a user
- **GET** `/api/{user_id}/tasks/{id}` - Get details of a specific task
- **PUT** `/api/{user_id}/tasks/{id}` - Update a specific task
- **DELETE** `/api/{user_id}/tasks/{id}` - Delete a specific task
- **PATCH** `/api/{user_id}/tasks/{id}/complete` - Toggle completion status

### Authentication

All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```
Or in the `access_token` cookie.

The JWT token is verified using the `BETTER_AUTH_SECRET` environment variable, and user identity is validated against the database.

### Data Isolation

- Each user can only access their own tasks
- User ID in JWT token is validated against user ID in URL
- Cross-user access is prevented at the application level

## 🛠️ Configuration

The application uses environment variables for configuration:

- `APP_NAME`: Application name (default: "FastAPI Backend")
- `APP_VERSION`: Application version (default: "1.0.0")
- `DEBUG`: Enable debug mode (default: "False")
- `DB_DRIVER`: Database driver (default: "postgresql+psycopg2")
- `DB_USERNAME`: Database username
- `DB_PASSWORD`: Database password
- `DB_HOST`: Database host (default: "localhost")
- `DB_PORT`: Database port (default: "5432")
- `DB_NAME`: Database name (default: "database")

## 🧪 Running Tests

```bash
pytest
```

## 📚 Database Support

This project supports multiple SQL databases through SQLAlchemy:

- **PostgreSQL**: `postgresql+psycopg2://user:pass@host:5432/db`
- **MySQL**: `mysql+pymysql://user:pass@host:3306/db`
- **SQL Server**: `mssql+pyodbc://user:pass@host:1433/db?driver=...`
- **SQLite**: `sqlite:///./database.db`
- **Neon**: `postgresql+psycopg2://user:pass@neon-host/db`

## 🏗️ Architecture

The project follows a clean architecture pattern:

- **Models** (`src/models/`): Define data structures and schemas
- **Controllers** (`src/controllers/`): Handle business logic
- **Routers** (`src/routers/`): Define API endpoints
- **Lib** (`src/lib/`): Shared utilities (database, config, exceptions)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the terms described in LICENSE.txt.

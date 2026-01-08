# FastAPI SQLModel Backend Template

This is a template for a production-ready FastAPI backend with SQLModel ORM, supporting any SQL database.

## 🚀 Quick Start

1. **Install dependencies**:
   ```bash
   uv pip install -r requirements.txt
   # or if using pip
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

3. **Run the application**:
   ```bash
   uvicorn main:app --reload
   # or
   python -m uvicorn main:app --reload
   ```

4. **Access the application**:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## 📁 Project Structure

```
{project_name}/
├── src/
│   ├── models/          # Data models
│   ├── controllers/     # Business logic
│   ├── routers/         # API endpoints
│   └── lib/            # Shared utilities
├── tests/              # Test files
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore rules
├── pyproject.toml      # Project dependencies
├── README.md           # Project documentation
└── main.py             # Application entry point
```

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
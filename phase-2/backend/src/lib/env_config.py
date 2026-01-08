"""
Environment configuration loader.
Loads database credentials and application settings from .env file.
"""
from dotenv import load_dotenv
from sqlalchemy import URL
import os
from typing import Optional

# Load environment variables
load_dotenv()

class Config:
    """
    Application configuration loaded from environment variables.

    Supports multiple database types through flexible configuration.
    """

    # Application Settings
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI Backend")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Database Settings
    DB_DRIVER: str = os.getenv("DB_DRIVER", "postgresql+psycopg2")
    DB_USERNAME: str = os.getenv("DB_USERNAME", "")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: Optional[str] = os.getenv("DB_PORT")  # Optional
    DB_NAME: str = os.getenv("DB_NAME", "database")
    direct_url = os.getenv("DATABASE_URL")
    # Authentication Settings
    BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "your-super-secret-jwt-key-change-this-in-production")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # Optional: For databases requiring additional query parameters
    DB_DRIVER_ODBC: Optional[str] = os.getenv("DB_DRIVER_ODBC")  # For SQL Server

    @classmethod
    def get_database_url(cls) -> str:
        """
        Construct database URL from environment variables.

        Returns:
            str: Database connection URL

        Supports:
            - PostgreSQL: postgresql+psycopg2://user:pass@host:5432/db
            - MySQL: mysql+pymysql://user:pass@host:3306/db
            - SQL Server: mssql+pyodbc://user:pass@host:1433/db?driver=...
            - SQLite: sqlite:///./database.db
            - Neon: postgresql+psycopg2://user:pass@neon-host/db
        """
        # Special case for SQLite
        if cls.direct_url:
            # Neon ki string 'postgresql://' ko 'postgresql+psycopg://' mein badlein
            if cls.direct_url.startswith("postgresql://"):
                return cls.direct_url.replace("postgresql://", "postgresql+psycopg://", 1)
            return cls.direct_url
        
        if cls.DB_DRIVER.startswith("sqlite"):
            return f"sqlite:///./{cls.DB_NAME}.db"

        # Build query parameters
        query = {}
        if cls.DB_DRIVER_ODBC:
            query["driver"] = cls.DB_DRIVER_ODBC

        # Construct URL
        url_obj = URL.create(
            drivername=cls.DB_DRIVER,
            username=cls.DB_USERNAME,
            password=cls.DB_PASSWORD,
            host=cls.DB_HOST,
            port=int(cls.DB_PORT) if cls.DB_PORT else None,
            database=cls.DB_NAME,
            query=query if query else None
        )

        return str(url_obj)

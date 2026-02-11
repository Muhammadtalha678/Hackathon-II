"""
Database connection manager using SQLModel.
Handles connection lifecycle, session management, and table creation.
Works with any SQL database supported by SQLAlchemy.
"""
from sqlmodel import SQLModel, Session, create_engine
from typing import Generator, Optional
from sqlalchemy.engine import Engine

class DBConfig:
    """
    Generic database configuration and connection manager.

    Supports any SQL database (PostgreSQL, MySQL, SQL Server, SQLite, etc.)
    through SQLAlchemy connection URLs.

    Attributes:
        url: Database connection URL
        engine: SQLAlchemy engine instance
    """

    def __init__(self, url: str, echo: bool = False, pool_pre_ping: bool = True):
        """
        Initialize database configuration.

        Args:
            url: Database connection URL (SQLAlchemy format)
            echo: Whether to log SQL statements (default: False)
            pool_pre_ping: Test connections before using (default: True)
        """
        self.url = url
        self.echo = echo
        self.pool_pre_ping = pool_pre_ping
        self.engine: Optional[Engine] = None

    def open_connection(self) -> None:
        """
        Open database connection and create engine.

        Raises:
            Exception: If connection fails
        """
        self.engine = create_engine(
            url=self.url,
            pool_pre_ping=self.pool_pre_ping,
            echo=self.echo
        )
        try:
            with self.engine.connect() as conn:
                print("Database connected successfully")
                print(f"  Database URL: {self._mask_password(self.url)}")
        except Exception as e:
            print(f"Database connection failed: {e}")
            raise Exception(f"Error connecting to database: {e}")

    def close_connection(self) -> None:
        """Close database connection and dispose engine."""
        if self.engine:
            self.engine.dispose()
            print("Database disconnected successfully")

    def create_tables(self) -> None:
        """
        Create all tables defined in SQLModel metadata.

        Note: Imports all model files to ensure they're registered
        with SQLModel.metadata before table creation.
        """
        if not self.engine:
            raise Exception("Database engine not initialized. Call open_connection() first.")

        # Import all models here to register them with metadata
        # Example: from src.models import user_model, product_model

        SQLModel.metadata.create_all(self.engine)
        print("Database tables created successfully")

    def get_session(self) -> Generator[Session, None, None]:
        """
        Get database session generator for dependency injection.

        Yields:
            Session: SQLModel database session

        Example:
            SessionDep = Annotated[Session, Depends(db.get_session)]
        """
        if not self.engine:
            raise Exception("Database engine not initialized. Call open_connection() first.")

        with Session(self.engine) as session:
            yield session

    @staticmethod
    def _mask_password(url: str) -> str:
        """Mask password in URL for logging."""
        if "://" in url and "@" in url:
            protocol, rest = url.split("://", 1)
            if "@" in rest:
                credentials, host = rest.split("@", 1)
                if ":" in credentials:
                    username, _ = credentials.split(":", 1)
                    return f"{protocol}://{username}:****@{host}"
        return url

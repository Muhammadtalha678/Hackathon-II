"""
FastAPI application entry point.
Initializes database connection and registers routes.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.lib.db_connect import DBConfig
from src.lib.env_config import Config
import httpx
# Import routers (add your routers here)
from src.routers import task_router
async def get_public_key(client:httpx.AsyncClient):
    while True:
        print("request send")
        jwk = await client.get(Config.frontend_jwks_url) 
        return jwk.json()
        # await asyncio.sleep(300)    
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events for database connection.
    """
    # Startup
    print("=" * 50)
    print(f"Starting {Config.APP_NAME}...")
    print("=" * 50)

    try:
        # Initialize database
        db_url = Config.get_database_url()
        # print(db_url)
        db = DBConfig(url=db_url, echo=Config.DEBUG)
        db.open_connection()
        db.create_tables()

        # Store db instance in app state for session dependency
        app.state.db_init = db
        client = httpx.AsyncClient()
        jwk = await get_public_key(client)
        print(jwk["keys"])
        app.state.jwks = jwk["keys"]
        print("=" * 50)
        print(f"{Config.APP_NAME} started successfully")
        print(f"  Version: {Config.APP_VERSION}")
        print(f"  Debug Mode: {Config.DEBUG}")
        print(f"  Docs: http://localhost:8000/docs")
        print("=" * 50)

    except Exception as e:
        print(f"✗ Failed to start application: {e}")
        raise

    yield

    # Shutdown
    print("=" * 50)
    print("Shutting down application...")
    app.state.db_init.close_connection()
    await client.aclose()
    print("Application shut down successfully")
    print("=" * 50)

# Initialize FastAPI application
app = FastAPI(
    title=Config.APP_NAME,
    version=Config.APP_VERSION,
    description="FastAPI backend with SQLModel ORM and SQL database support",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers (add your routers here)
app.include_router(task_router.router)

# Root endpoint
@app.get("/", tags=["Health"])
def root():
    """
    Root endpoint - health check.

    Returns basic application information and health status.
    """
    return {
        "status": "healthy",
        "app": Config.APP_NAME,
        "version": Config.APP_VERSION,
        "message": "API is running. Visit /docs for API documentation."
    }

@app.get("/health", tags=["Health"])
def health_check():
    """
    Detailed health check endpoint.

    Returns detailed application health information.
    """
    return {
        "status": "healthy",
        "database": "connected",
        "app_name": Config.APP_NAME,
        "version": Config.APP_VERSION
    }

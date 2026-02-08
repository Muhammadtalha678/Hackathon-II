from fastmcp.server.lifespan import lifespan
from src.lib.db_connect import DBConfig
from src.lib.env_config import Config
from fastmcp import FastMCP,Context
import httpx

async def get_public_key(client:httpx.AsyncClient):
    while True:
        print("Config.frontend_jwks_url")
        jwk = await client.get(Config.frontend_jwks_url) 
        return jwk.json()
        # await asyncio.sleep(300)    


@lifespan
async def app_lifespan(server: FastMCP):
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
        # app.state.db_init = db
        client = httpx.AsyncClient()
        jwk = await get_public_key(client)
        print(jwk["keys"])
        # app.state.jwks = jwk["keys"]
        print("=" * 50)
        print(f"{Config.APP_NAME} started successfully")
        print(f"  Version: {Config.APP_VERSION}")
        print(f"  Debug Mode: {Config.DEBUG}")
        print(f"  Docs: http://localhost:8000/docs")
        print("=" * 50)

    except Exception as e:
        print(f"✗ Failed to start application: {e}")
        raise

    yield {
        "db":db,"jwks":jwk["keys"]
    }

    # Shutdown
    print("=" * 50)
    print("Shutting down application...")
    # app.state.db_init.close_connection()
    db.close_connection()
    await client.aclose()
    print("Application shut down successfully")
    print("=" * 50)

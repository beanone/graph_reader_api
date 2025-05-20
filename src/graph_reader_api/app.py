from contextlib import asynccontextmanager

from apikey.db import init_db
from apikey.router import api_key_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mcp import FastApiMCP
from graph_reader.config import GraphReaderConfig
from graph_reader.reader import GraphReader

from .config import APIConfig
from .routers import community, entity, search


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI app.

    This handles startup and shutdown events.
    """
    # Startup
    await init_db()
    yield
    # Shutdown
    # Add any cleanup code here if needed


def create_app(base_dir: str = "resources/kg") -> FastAPI:
    """Create and configure the FastAPI application.

    Args:
        base_dir: The base directory for graph data storage.

    Returns:
        FastAPI: The configured FastAPI application.
    """
    # Initialize FastAPI app with OpenAPI metadata
    application = FastAPI(
        title="Graph Reader API",
        description="A FastAPI-based API for graph data retrieval and analysis.",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Add CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:8001"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.get("/health")
    async def health_check():
        """Health check endpoint for Docker."""
        return {"status": "healthy"}

    # Initialize graph reader
    config = APIConfig(base_dir=base_dir)
    reader = GraphReader(
        GraphReaderConfig(
            base_dir=config.base_dir,
            indexer_type=config.indexer_type,
            cache_size=config.cache_size,
        )
    )

    application.include_router(entity.init_router(reader))
    application.include_router(community.init_router(reader))
    application.include_router(search.init_router(reader))

    mcp = FastApiMCP(
        application,
        name="Graph Reader API",
        description="A FastAPI-based API for graph data retrieval and analysis.",
        describe_all_responses=True,
        describe_full_response_schema=True,
    )
    mcp.mount()
    # We do not want to mount the API key router to the MCP.
    application.include_router(api_key_router)

    return application


application = create_app()

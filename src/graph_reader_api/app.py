from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mcp import FastApiMCP
from graph_reader.config import GraphReaderConfig
from graph_reader.reader import GraphReader

from .config import APIConfig
from .routers import community, entity, search


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

    return application


application = create_app()

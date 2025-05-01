from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from graph_reader.config import GraphReaderConfig
from graph_reader.reader import GraphReader

from .config import APIConfig
from .routers import community, entity, search


def create_app(base_dir: str = "graph_output") -> FastAPI:
    """Create and configure the FastAPI application.

    Args:
        base_dir: The base directory for graph data storage.

    Returns:
        FastAPI: The configured FastAPI application.
    """
    app = FastAPI()
    mcp = FastApiMCP(
        app,
        name="Graph Reader API",
        description="A FastAPI-based API for graph data retrieval and analysis.",
        describe_all_responses=True,
        describe_full_response_schema=True,
    )
    mcp.mount()

    config = APIConfig(base_dir=base_dir)
    reader = GraphReader(
        GraphReaderConfig(
            base_dir=config.base_dir,
            indexer_type=config.indexer_type,
            cache_size=config.cache_size,
        )
    )

    app.include_router(entity.init_router(reader))
    app.include_router(community.init_router(reader))
    app.include_router(search.init_router(reader))

    return app


app = create_app()

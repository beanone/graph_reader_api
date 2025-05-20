"""Test the FastAPI application setup."""

import pytest
from apikey.db import DBState, init_db
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from graph_reader_api.app import create_app, lifespan


@pytest.fixture(scope="module")
async def client():
    """Create a test client with a test database."""
    app = create_app()
    # Initialize the database before creating the test client
    await init_db()
    async with lifespan(app) as _:
        client = TestClient(app)
        yield client


@pytest.mark.asyncio
async def test_lifespan_initializes_database():
    """Test that the lifespan context manager initializes the database."""
    app = create_app()
    async with lifespan(app) as _:
        # The database should be initialized after the app starts
        assert DBState.engine is not None, "Database engine should be initialized"
        assert (
            DBState.async_session_maker is not None
        ), "Session maker should be initialized"


@pytest.mark.asyncio
async def test_database_session_works():
    """Test that we can get a working database session."""
    app = create_app()
    async with lifespan(app) as _:
        async with DBState.async_session_maker() as session:
            assert isinstance(session, AsyncSession), "Should get an AsyncSession"
            # Test that the session is working by executing a simple query
            result = await session.execute(text("SELECT 1"))
            assert result.scalar() == 1, "Should be able to execute queries"

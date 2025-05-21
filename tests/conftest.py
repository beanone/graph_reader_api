"""Pytest configuration file."""

import subprocess
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import UUID

import pytest
from apikey.dependencies import get_current_user
from fixture_generator import create_test_graph_fixture
from jose import jwt

from graph_reader_api.app import create_app

# Add src directory to Python path
src_path = str(Path(__file__).parent.parent / "src")
sys.path.insert(0, src_path)


def pytest_sessionstart(session):
    """Run verification before any tests."""
    script_path = Path(__file__).parent.parent / "scripts" / "pp-verify.sh"
    if script_path.exists():
        try:
            # Run only the pre-commit checks without pytest to avoid recursion
            subprocess.run(["pre-commit", "run", "--all-files"], check=True)
        except subprocess.CalledProcessError as e:
            pytest.exit(f"Pre-commit checks failed with exit code {e.returncode}")


@pytest.fixture(scope="session")
def setup_graph_fixture(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("test_graph")
    create_test_graph_fixture(base_dir=temp_dir)
    return str(temp_dir)


def create_jwt_for_user(user_id: UUID, email: str) -> str:
    """Create a JWT token for testing.

    Args:
        user_id: The user's UUID
        email: The user's email

    Returns:
        A signed JWT token
    """
    now = datetime.now(UTC)
    claims = {
        "sub": str(user_id),
        "email": email,
        "aud": "fastapi-users:auth",
        "iat": now,
        "exp": now + timedelta(hours=1),
    }
    return jwt.encode(claims, "supersecretjwtkey", algorithm="HS256")


async def override_get_current_user(token: str | None = None):
    return {
        "sub": "test-user-id",
        "email": "test@example.com",
        "is_active": True,
        "is_superuser": False,
        "is_verified": True,
        "roles": ["admin"],  # roles present for compatibility, not for RBAC
    }


@pytest.fixture
def client(setup_graph_fixture):
    """Create a test client with the application."""
    app = create_app(base_dir=str(setup_graph_fixture))
    app.dependency_overrides[get_current_user] = override_get_current_user
    return app


@pytest.fixture
def auth_header():
    """Return an Authorization header with a valid JWT."""
    user_id = UUID("123e4567-e89b-12d3-a456-426614174000")
    jwt = create_jwt_for_user(user_id, "test@example.com")
    return {"Authorization": f"Bearer {jwt}"}

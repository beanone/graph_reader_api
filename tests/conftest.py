"""Pytest configuration file."""

import os
import subprocess
import sys
from pathlib import Path

import pytest
from fixture_generator import create_test_graph_fixture
from jose import jwt

from graph_reader_api.app import application
from graph_reader_api.auth.dependencies import get_current_user

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


async def override_get_current_user(token: str | None = None):
    return {
        "sub": "test-user-id",
        "email": "test@example.com",
        "is_active": True,
        "is_superuser": False,
        "is_verified": True,
        "roles": ["admin"],  # roles present for compatibility, not for RBAC
    }


application.dependency_overrides[get_current_user] = override_get_current_user


@pytest.fixture
def jwt_token():
    """Generate a valid JWT for test authentication."""
    secret = os.getenv("KEYLIN_JWT_SECRET", "changeme")
    payload = {
        "sub": "test-user-id",
        "email": "test@example.com",
        "roles": ["admin"],
        # Add any other claims your app expects
    }
    return jwt.encode(payload, secret, algorithm="HS256")


@pytest.fixture
def auth_header(jwt_token):
    """Return an Authorization header with a valid JWT."""
    return {"Authorization": f"Bearer {jwt_token}"}

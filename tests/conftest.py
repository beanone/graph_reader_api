"""Pytest configuration file."""

import subprocess
import sys
from pathlib import Path

import pytest
from fixture_generator import create_test_graph_fixture

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

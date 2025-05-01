"""Pytest configuration file."""

import sys
from pathlib import Path

import pytest

from fixture_generator import create_test_graph_fixture

# Add src directory to Python path
src_path = str(Path(__file__).parent.parent / "src")
sys.path.insert(0, src_path)


@pytest.fixture(scope="session")
def setup_graph_fixture(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("test_graph")
    create_test_graph_fixture(base_dir=temp_dir)
    return str(temp_dir)

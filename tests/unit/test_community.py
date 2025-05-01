import pytest
from fastapi.testclient import TestClient
from graph_reader_api.app import create_app

from tests.conftest import setup_graph_fixture


@pytest.fixture(scope="module")
def client(setup_graph_fixture):
    app = create_app(base_dir=str(setup_graph_fixture))
    return TestClient(app)


def test_get_members(client):
    response = client.get("/community/team_alpha/members")
    assert response.status_code == 200
    data = response.json()
    assert "members" in data
    assert set(data["members"]) == {1, 2}

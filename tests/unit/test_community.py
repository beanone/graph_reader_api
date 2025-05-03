import pytest
from fastapi.testclient import TestClient

from graph_reader_api.app import create_app


@pytest.fixture(scope="module")
def client(setup_graph_fixture):
    application = create_app(base_dir=str(setup_graph_fixture))
    return TestClient(application)


def test_get_members(client, auth_header):
    response = client.get("/community/team_alpha/members", headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert "members" in data
    assert set(data["members"]) == {1, 2}

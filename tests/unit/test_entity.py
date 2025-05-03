import pytest
from fastapi.testclient import TestClient

from graph_reader_api.app import create_app


@pytest.fixture(scope="module")
def client(setup_graph_fixture):
    application = create_app(base_dir=str(setup_graph_fixture))
    return TestClient(application)


def test_get_entity(client, auth_header):
    response = client.get("/entity/1", headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert data["entity_id"] == 1
    assert data["properties"]["name"] == "Alice"


def test_get_entity_not_found(client, auth_header):
    response = client.get("/entity/999", headers=auth_header)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Entity not found"


def test_get_neighbors(client, auth_header):
    response = client.get("/entity/1/neighbors", headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert "neighbors" in data
    neighbors = data["neighbors"]
    assert isinstance(neighbors, list)
    assert len(neighbors) == 1
    assert neighbors[0]["target_id"] == 2


def test_get_entity_community(client, auth_header):
    response = client.get("/entity/1/community", headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert "community_id" in data
    assert data["community_id"] == "team_alpha"


def test_get_entity_community_not_found(client, auth_header):
    response = client.get("/entity/999/community", headers=auth_header)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Community not found"

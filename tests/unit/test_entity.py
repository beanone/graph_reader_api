import pytest
from fastapi.testclient import TestClient

from graph_reader_api.app import create_app


@pytest.fixture(scope="module")
def client(setup_graph_fixture):
    app = create_app(base_dir=str(setup_graph_fixture))
    return TestClient(app)


def test_get_entity(client):
    response = client.get("/entity/1")
    assert response.status_code == 200
    data = response.json()
    assert data["entity_id"] == 1
    assert data["properties"]["name"] == "Alice"


def test_get_entity_not_found(client):
    response = client.get("/entity/999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Entity not found"


def test_get_neighbors(client):
    response = client.get("/entity/1/neighbors")
    assert response.status_code == 200
    data = response.json()
    assert "neighbors" in data
    neighbors = data["neighbors"]
    assert isinstance(neighbors, list)
    assert len(neighbors) == 1
    assert neighbors[0]["target_id"] == 2


def test_get_entity_community(client):
    response = client.get("/entity/1/community")
    assert response.status_code == 200
    data = response.json()
    assert "community_id" in data
    assert data["community_id"] == "team_alpha"


def test_get_entity_community_not_found(client):
    response = client.get("/entity/999/community")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Community not found"

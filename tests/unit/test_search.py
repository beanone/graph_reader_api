import pytest
from fastapi.testclient import TestClient

from graph_reader_api.app import create_app


@pytest.fixture(scope="module")
def client(setup_graph_fixture):
    application = create_app(base_dir=str(setup_graph_fixture))
    return TestClient(application)


def test_search_by_property(client, auth_header):
    response = client.get("/search?key=name&value=Alice", headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert "entity_ids" in data
    assert isinstance(response.json().get("entity_ids"), list)
    assert len(response.json().get("entity_ids")) == 1
    assert response.json().get("entity_ids")[0] == 1


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data == {"status": "healthy"}

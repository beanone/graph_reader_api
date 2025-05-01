import pytest
from fastapi.testclient import TestClient

from graph_reader_api.app import create_app


@pytest.fixture(scope="module")
def client(setup_graph_fixture):
    app = create_app(base_dir=str(setup_graph_fixture))
    return TestClient(app)


def test_search_by_property(client):
    response = client.get("/search?key=name&value=Alice")
    assert response.status_code == 200
    data = response.json()
    assert "entity_ids" in data
    assert isinstance(response.json().get("entity_ids"), list)
    assert len(response.json().get("entity_ids")) == 1
    assert response.json().get("entity_ids")[0] == 1

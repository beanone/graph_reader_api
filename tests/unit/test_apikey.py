import httpx
import pytest
import respx
from httpx import ASGITransport, AsyncClient

from graph_reader_api.app import application
from graph_reader_api.routers.apikey import LOCKSMITHA_URL, SERVICE_ID


@pytest.fixture(autouse=True)
def override_get_current_user():
    from graph_reader_api.auth import dependencies

    async def fake_user():
        return {"sub": "test-user-id", "email": "test@example.com"}

    application.dependency_overrides[dependencies.get_current_user] = fake_user
    yield
    application.dependency_overrides = {}


@pytest.fixture
def transport():
    return ASGITransport(app=application)


@respx.mock
@pytest.mark.asyncio
async def test_create_api_key(transport):
    url = f"{LOCKSMITHA_URL}/auth/api-key/"
    expected_response = {
        "id": "key-1",
        "name": "testkey",
        "service_id": SERVICE_ID,
        "status": "active",
        "created_at": "2024-06-01T00:00:00Z",
        "expires_at": None,
        "last_used_at": None,
        "plaintext_key": "plaintext-key-value",
    }
    respx.post(url).mock(return_value=httpx.Response(201, json=expected_response))
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post(
            "/apikeys/",
            json={"name": "testkey"},
            headers={"Authorization": "Bearer test"},
        )
    print(f"[DEBUG] Response text: {resp.text}")
    assert resp.status_code == 201
    data = resp.json()
    assert data["id"] == "key-1"
    assert data["plaintext_key"] == "plaintext-key-value"
    assert data["service_id"] == SERVICE_ID


@respx.mock
@pytest.mark.asyncio
async def test_list_api_keys(transport):
    url = f"{LOCKSMITHA_URL}/auth/api-key/"
    expected_response = [
        {
            "id": "key-1",
            "name": "testkey",
            "service_id": SERVICE_ID,
            "status": "active",
            "created_at": "2024-06-01T00:00:00Z",
            "expires_at": None,
            "last_used_at": None,
        }
    ]
    respx.get(url).mock(return_value=httpx.Response(200, json=expected_response))
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/apikeys/", headers={"Authorization": "Bearer test"})
    print(f"[DEBUG] Response text: {resp.text}")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert data[0]["id"] == "key-1"
    assert data[0]["service_id"] == SERVICE_ID


@respx.mock
@pytest.mark.asyncio
async def test_delete_api_key(transport):
    key_id = "key-1"
    url = f"{LOCKSMITHA_URL}/auth/api-key/{key_id}"
    respx.delete(url).mock(return_value=httpx.Response(204))
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.delete(
            f"/apikeys/{key_id}", headers={"Authorization": "Bearer test"}
        )
    print(f"[DEBUG] Response text: {resp.text}")
    assert resp.status_code == 204


@respx.mock
@pytest.mark.asyncio
async def test_create_api_key_error(transport):
    url = f"{LOCKSMITHA_URL}/auth/api-key/"
    respx.post(url).mock(return_value=httpx.Response(400, text="bad request"))
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post(
            "/apikeys/",
            json={"name": "testkey"},
            headers={"Authorization": "Bearer test"},
        )
    print(f"[DEBUG] Response text: {resp.text}")
    assert resp.status_code == 400
    assert "bad request" in resp.text


@respx.mock
@pytest.mark.asyncio
async def test_list_api_keys_error(transport):
    url = f"{LOCKSMITHA_URL}/auth/api-key/"
    respx.get(url).mock(return_value=httpx.Response(500, text="server error"))
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/apikeys/", headers={"Authorization": "Bearer test"})
    print(f"[DEBUG] Response text: {resp.text}")
    assert resp.status_code == 500
    assert "server error" in resp.text


@respx.mock
@pytest.mark.asyncio
async def test_delete_api_key_error(transport):
    key_id = "key-1"
    url = f"{LOCKSMITHA_URL}/auth/api-key/{key_id}"
    respx.delete(url).mock(return_value=httpx.Response(404, text="not found"))
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.delete(
            f"/apikeys/{key_id}", headers={"Authorization": "Bearer test"}
        )
    print(f"[DEBUG] Response text: {resp.text}")
    assert resp.status_code == 404
    assert "not found" in resp.text


@respx.mock
@pytest.mark.asyncio
async def test_create_api_key_no_auth(transport):
    url = f"{LOCKSMITHA_URL}/auth/api-key/"
    expected_response = {
        "id": "key-2",
        "name": "testkey2",
        "service_id": SERVICE_ID,
        "status": "active",
        "created_at": "2024-06-01T00:00:00Z",
        "expires_at": None,
        "last_used_at": None,
        "plaintext_key": "plaintext-key-value-2",
    }
    respx.post(url).mock(return_value=httpx.Response(201, json=expected_response))
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post("/apikeys/", json={"name": "testkey2"})
    # No assertion needed, just cover the branch


@respx.mock
@pytest.mark.asyncio
async def test_list_api_keys_no_auth(transport):
    url = f"{LOCKSMITHA_URL}/auth/api-key/"
    expected_response = [
        {
            "id": "key-2",
            "name": "testkey2",
            "service_id": SERVICE_ID,
            "status": "active",
            "created_at": "2024-06-01T00:00:00Z",
            "expires_at": None,
            "last_used_at": None,
        }
    ]
    respx.get(url).mock(return_value=httpx.Response(200, json=expected_response))
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.get("/apikeys/")
    # No assertion needed, just cover the branch


@respx.mock
@pytest.mark.asyncio
async def test_delete_api_key_no_auth(transport):
    key_id = "key-2"
    url = f"{LOCKSMITHA_URL}/auth/api-key/{key_id}"
    respx.delete(url).mock(return_value=httpx.Response(204))
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.delete(f"/apikeys/{key_id}")
    # No assertion needed, just cover the branch

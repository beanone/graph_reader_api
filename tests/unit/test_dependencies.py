import pytest
from fastapi import HTTPException
from jose import JWTError, jwt

from graph_reader_api.auth.dependencies import get_current_user


class DummyDepends:
    def __init__(self, value):
        self.value = value

    def __call__(self, *args, **kwargs):
        return self.value


@pytest.mark.asyncio
async def test_get_current_user_valid(monkeypatch):
    payload = {
        "sub": "123e4567-e89b-12d3-a456-426614174000",
        "email": "test@example.com",
    }

    def fake_decode(token, secret, algorithms):
        assert token == "validtoken"
        return payload

    monkeypatch.setattr(jwt, "decode", fake_decode)
    result = await get_current_user(token="validtoken")
    assert result == payload


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(monkeypatch):
    def fake_decode(token, secret, algorithms):
        raise JWTError("bad token")

    monkeypatch.setattr(jwt, "decode", fake_decode)
    with pytest.raises(HTTPException) as exc:
        await get_current_user(token="invalidtoken")
    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid token"


@pytest.mark.asyncio
async def test_get_current_user_missing_sub(monkeypatch):
    payload = {"email": "test@example.com"}

    def fake_decode(token, secret, algorithms):
        return payload

    monkeypatch.setattr(jwt, "decode", fake_decode)
    with pytest.raises(HTTPException) as exc:
        await get_current_user(token="validtoken")
    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid token"

import logging
import os

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from ..auth.dependencies import get_current_user

LOCKSMITHA_URL = os.getenv("LOCKSMITHA_URL", "http://localhost:8001")
SERVICE_ID = os.getenv("SERVICE_ID", "graph_reader_api")


class APIKeyCreateRequest(BaseModel):
    name: str | None = None
    expires_at: str | None = None  # ISO8601 string


class APIKeyReadResponse(BaseModel):
    id: str
    name: str | None = None
    service_id: str
    status: str
    created_at: str
    expires_at: str | None = None
    last_used_at: str | None = None


class APIKeyCreateResponse(APIKeyReadResponse):
    plaintext_key: str


router = APIRouter(prefix="/apikeys", tags=["apikeys"])


@router.post(
    "/", response_model=APIKeyCreateResponse, status_code=status.HTTP_201_CREATED
)
async def create_api_key(
    req: APIKeyCreateRequest,
    request: Request,
    user=Depends(get_current_user),
):
    """Create a new API key for the authenticated user (for this service)."""
    body = await request.body()
    logging.error(f"[DEBUG] Received body: {body}")
    headers = {}
    if "authorization" in request.headers:
        headers["authorization"] = request.headers["authorization"]
    payload = req.model_dump(exclude_unset=True)
    payload["service_id"] = SERVICE_ID
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{LOCKSMITHA_URL}/auth/api-key/",
            json=payload,
            headers=headers,
        )
        if resp.status_code != 201:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()


@router.get("/", response_model=list[APIKeyReadResponse])
async def list_api_keys(
    request: Request,
    user=Depends(get_current_user),
):
    """List all API keys for the authenticated user (for this service)."""
    logging.error(f"[DEBUG] Query params: {request.query_params}")
    headers = {}
    if "authorization" in request.headers:
        headers["authorization"] = request.headers["authorization"]
    params = {"service_id": SERVICE_ID}
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{LOCKSMITHA_URL}/auth/api-key/",
            params=params,
            headers=headers,
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()


@router.delete("/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_api_key(
    key_id: str,
    request: Request,
    user=Depends(get_current_user),
):
    """Delete an API key by ID for the authenticated user (for this service)."""
    logging.error(f"[DEBUG] Query params: {request.query_params}")
    headers = {}
    if "authorization" in request.headers:
        headers["authorization"] = request.headers["authorization"]
    params = {"service_id": SERVICE_ID}
    async with httpx.AsyncClient() as client:
        resp = await client.delete(
            f"{LOCKSMITHA_URL}/auth/api-key/{key_id}",
            params=params,
            headers=headers,
        )
        if resp.status_code != 204:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return JSONResponse(status_code=204, content=None)

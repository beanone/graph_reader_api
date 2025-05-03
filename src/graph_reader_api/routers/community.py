from fastapi import APIRouter, Depends
from graph_reader.reader import GraphReader

from ..auth.dependencies import get_current_user


def init_router(reader: GraphReader) -> APIRouter:
    router = APIRouter(prefix="/community", tags=["community"])

    @router.get("/{community_id}/members")
    async def get_community_members(community_id: str, user=Depends(get_current_user)):
        return {"members": reader.get_community_members(community_id)}

    return router

from fastapi import APIRouter
from graph_reader.reader import GraphReader


def init_router(reader: GraphReader) -> APIRouter:
    router = APIRouter(prefix="/community", tags=["community"])

    @router.get("/{community_id}/members")
    async def get_community_members(community_id: str):
        return {"members": reader.get_community_members(community_id)}

    return router

from fastapi import APIRouter, HTTPException
from graph_reader.reader import GraphReader


def init_router(reader: GraphReader) -> APIRouter:
    router = APIRouter(prefix="/entity", tags=["entity"])

    @router.get("/{entity_id}")
    async def get_entity(entity_id: int):
        entity = reader.get_entity(entity_id)
        if not entity:
            raise HTTPException(status_code=404, detail="Entity not found")
        return entity

    @router.get("/{entity_id}/neighbors")
    async def get_neighbors(entity_id: int):
        return {"neighbors": reader.get_neighbors(entity_id)}

    @router.get("/{entity_id}/community")
    async def get_entity_community(entity_id: int):
        community_id = reader.get_entity_community(entity_id)
        if not community_id:
            raise HTTPException(status_code=404, detail="Community not found")
        return {"community_id": community_id}

    return router

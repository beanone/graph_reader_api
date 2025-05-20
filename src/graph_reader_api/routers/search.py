from apikey.dependencies import get_current_user
from fastapi import APIRouter, Depends, Query
from graph_reader.reader import GraphReader


def init_router(reader: GraphReader) -> APIRouter:
    router = APIRouter(tags=["search"])

    @router.get("/search")
    async def search_by_property(
        key: str = Query(...), value: str = Query(...), user=Depends(get_current_user)
    ):
        matches = reader.search_by_property(key, value)
        return {"entity_ids": matches}

    return router

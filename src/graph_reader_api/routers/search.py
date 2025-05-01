from fastapi import APIRouter, Query
from graph_reader.reader import GraphReader


def init_router(reader: GraphReader) -> APIRouter:
    router = APIRouter(tags=["search"])

    @router.get("/search")
    async def search_by_property(key: str = Query(...), value: str = Query(...)):
        matches = reader.search_by_property(key, value)
        return {"entity_ids": matches}

    return router

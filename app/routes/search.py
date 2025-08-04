from fastapi import APIRouter, Query
from elasticsearch import AsyncElasticsearch
from typing import List

router = APIRouter(prefix="/search", tags=["search"])

es = AsyncElasticsearch("http://localhost:9200")  # Đổi lại nếu ES không chạy ở localhost

@router.get("/", response_model=List[dict])
async def search_notes(q: str = Query(...)):
    resp = await es.search(
        index="notes",  # Đổi lại nếu index của bạn tên khác
        query={
            "multi_match": {
                "query": q,
                "fields": ["title", "content"]
            }
        }
    )
    results = [hit["_source"] for hit in resp["hits"]["hits"]]
    return results
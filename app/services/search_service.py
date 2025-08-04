from fastapi import APIRouter, Query
from elasticsearch import AsyncElasticsearch
from typing import List

es = AsyncElasticsearch("http://localhost:9200")

async def search_notes_in_es(q: str, user_id: str):
    resp = await es.search(
        index="data.notes",  # Đổi lại nếu index của bạn tên khác
        query={
            "bool": {
                "must": [
                    {"multi_match": {
                        "query": q,
                        "fields": ["title", "content"]
                    }},
                    {"term": {"user_id": user_id}}
                ]
            }
        }
    )
    results = [hit["_source"] for hit in resp["hits"]["hits"]]
    return results
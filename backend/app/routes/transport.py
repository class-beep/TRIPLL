from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from bson import ObjectId
from app.database.connection import get_async_db

router = APIRouter(prefix="/transport", tags=["Transport"])

@router.get("")
async def get_transport(
    transport_type: Optional[str] = None,  # Flight, Train, Bus
    source: Optional[str] = None,
    destination: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
    skip: int = Query(0, ge=0)
):
    db = get_async_db()
    query = {}

    if transport_type:
        query["transport_type"] = {"$regex": transport_type, "$options": "i"}

    if source:
        query["source"] = {"$regex": source, "$options": "i"}

    if destination:
        query["destination"] = {"$regex": destination, "$options": "i"}

    cursor = db.transport.find(query).skip(skip).limit(limit)
    items = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        items.append(doc)

    total = await db.transport.count_documents(query)

    return {
        "total": total,
        "items": items
    }

@router.get("/{transport_id}")
async def get_transport_by_id(transport_id: str):
    db = get_async_db()
    if not ObjectId.is_valid(transport_id):
        raise HTTPException(status_code=400, detail="Invalid transport ID format")
    
    doc = await db.transport.find_one({"_id": ObjectId(transport_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Transport option not found")
    
    doc["_id"] = str(doc["_id"])
    return doc

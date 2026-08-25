from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from bson import ObjectId
from app.database.connection import get_async_db

router = APIRouter(prefix="/activities", tags=["Activities"])

@router.get("")
async def get_activities(
    search: Optional[str] = None,
    destination_id: Optional[str] = None,
    category: Optional[str] = None,
    min_rating: Optional[float] = None,
    limit: int = Query(50, ge=1, le=100),
    skip: int = Query(0, ge=0)
):
    db = get_async_db()
    query = {}

    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
            {"category": {"$regex": search, "$options": "i"}}
        ]

    if destination_id:
        query["destination_id"] = destination_id

    if category:
        query["category"] = category

    if min_rating is not None:
        query["rating"] = {"$gte": min_rating}

    cursor = db.activities.find(query).skip(skip).limit(limit)
    activities = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        activities.append(doc)

    total = await db.activities.count_documents(query)

    return {
        "total": total,
        "items": activities
    }

@router.get("/{activity_id}")
async def get_activity_by_id(activity_id: str):
    db = get_async_db()
    if not ObjectId.is_valid(activity_id):
        raise HTTPException(status_code=400, detail="Invalid activity ID format")
    
    doc = await db.activities.find_one({"_id": ObjectId(activity_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    doc["_id"] = str(doc["_id"])
    return doc

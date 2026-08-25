from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from bson import ObjectId
from app.database.connection import get_async_db

router = APIRouter(prefix="/hotels", tags=["Hotels"])

@router.get("")
async def get_hotels(
    search: Optional[str] = None,
    destination_id: Optional[str] = None,
    min_rating: Optional[float] = None,
    max_price: Optional[float] = None,
    limit: int = Query(50, ge=1, le=100),
    skip: int = Query(0, ge=0)
):
    db = get_async_db()
    query = {}

    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"address": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]

    if destination_id:
        query["destination_id"] = destination_id

    if min_rating is not None:
        query["rating"] = {"$gte": min_rating}

    if max_price is not None:
        query["price_per_night"] = {"$lte": max_price}

    cursor = db.hotels.find(query).skip(skip).limit(limit)
    hotels = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        hotels.append(doc)

    total = await db.hotels.count_documents(query)

    return {
        "total": total,
        "items": hotels
    }

@router.get("/{hotel_id}")
async def get_hotel_by_id(hotel_id: str):
    db = get_async_db()
    if not ObjectId.is_valid(hotel_id):
        raise HTTPException(status_code=400, detail="Invalid hotel ID format")
    
    doc = await db.hotels.find_one({"_id": ObjectId(hotel_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Hotel not found")
    
    doc["_id"] = str(doc["_id"])
    return doc

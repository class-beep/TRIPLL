from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from bson import ObjectId
from app.database.connection import get_async_db

router = APIRouter(prefix="/destinations", tags=["Destinations"])

@router.get("")
async def get_destinations(
    search: Optional[str] = None,
    category: Optional[str] = None,
    hidden_gem: Optional[bool] = None,
    max_budget: Optional[float] = None,
    min_rating: Optional[float] = None,
    sort_by: Optional[str] = "popularity",  # popularity, rating, budget_asc, budget_desc
    limit: int = Query(50, ge=1, le=100),
    skip: int = Query(0, ge=0)
):
    db = get_async_db()
    query = {}

    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"country": {"$regex": search, "$options": "i"}},
            {"state": {"$regex": search, "$options": "i"}},
            {"category": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]

    if category and category != "All":
        query["category"] = category

    if hidden_gem is not None:
        query["hidden_gem"] = hidden_gem

    if min_rating is not None:
        query["rating"] = {"$gte": min_rating}

    sort_order = [("popularity_score", -1)]
    if sort_by == "rating":
        sort_order = [("rating", -1)]
    elif sort_by == "name":
        sort_order = [("name", 1)]

    cursor = db.destinations.find(query).sort(sort_order).skip(skip).limit(limit)
    destinations = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        destinations.append(doc)

    total = await db.destinations.count_documents(query)

    return {
        "total": total,
        "items": destinations
    }

@router.get("/categories")
async def get_categories():
    return [
        "All", "Beach", "Mountain", "City", "Nature", 
        "Adventure", "Romantic", "Family", "Backpacking", "Luxury", "Hidden Gem"
    ]

@router.get("/{destination_id}")
async def get_destination_by_id(destination_id: str):
    db = get_async_db()
    if not ObjectId.is_valid(destination_id):
        raise HTTPException(status_code=400, detail="Invalid destination ID format")
    
    doc = await db.destinations.find_one({"_id": ObjectId(destination_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    doc["_id"] = str(doc["_id"])

    # Fetch related hotels and activities
    hotels_cursor = db.hotels.find({"destination_id": destination_id}).limit(6)
    hotels = []
    async for h in hotels_cursor:
        h["_id"] = str(h["_id"])
        hotels.append(h)
    doc["hotels"] = hotels

    activities_cursor = db.activities.find({"destination_id": destination_id}).limit(6)
    activities = []
    async for a in activities_cursor:
        a["_id"] = str(a["_id"])
        activities.append(a)
    doc["related_activities"] = activities

    return doc

from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from datetime import datetime
from app.schemas.schemas import TripCreate, ItineraryItemCreate
from app.middleware.auth import get_current_user
from app.database.connection import get_async_db

router = APIRouter(prefix="/trips", tags=["Trips"])

@router.post("")
async def create_trip(
    trip_data: TripCreate,
    current_user: dict = Depends(get_current_user)
):
    db = get_async_db()
    trip_dict = trip_data.dict()
    trip_dict.update({
        "user_id": current_user["_id"],
        "status": "Upcoming",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "itinerary": [],
        "expenses": []
    })
    
    result = await db.trips.insert_one(trip_dict)
    trip_dict["_id"] = str(result.inserted_id)

    # Send notification
    notification_doc = {
        "user_id": current_user["_id"],
        "title": "New Trip Created! ✈️",
        "message": f"Your trip '{trip_data.name}' to {trip_data.destination} has been created.",
        "type": "trip",
        "read": False,
        "link": f"/my-trips/{trip_dict['_id']}",
        "created_at": datetime.utcnow().isoformat()
    }
    await db.notifications.insert_one(notification_doc)

    return trip_dict

@router.get("")
async def get_user_trips(current_user: dict = Depends(get_current_user)):
    db = get_async_db()
    cursor = db.trips.find({"user_id": current_user["_id"]}).sort("start_date", 1)
    trips = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        trips.append(doc)
    return trips

@router.get("/{trip_id}")
async def get_trip_by_id(
    trip_id: str,
    current_user: dict = Depends(get_current_user)
):
    db = get_async_db()
    if not ObjectId.is_valid(trip_id):
        raise HTTPException(status_code=400, detail="Invalid trip ID format")
    
    doc = await db.trips.find_one({
        "_id": ObjectId(trip_id),
        "user_id": current_user["_id"]
    })
    if not doc:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    doc["_id"] = str(doc["_id"])
    return doc

@router.patch("/{trip_id}")
async def update_trip(
    trip_id: str,
    update_data: dict,
    current_user: dict = Depends(get_current_user)
):
    db = get_async_db()
    if not ObjectId.is_valid(trip_id):
        raise HTTPException(status_code=400, detail="Invalid trip ID format")
    
    update_data["updated_at"] = datetime.utcnow().isoformat()
    result = await db.trips.update_one(
        {"_id": ObjectId(trip_id), "user_id": current_user["_id"]},
        {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    updated_doc = await db.trips.find_one({"_id": ObjectId(trip_id)})
    updated_doc["_id"] = str(updated_doc["_id"])
    return updated_doc

@router.delete("/{trip_id}")
async def delete_trip(
    trip_id: str,
    current_user: dict = Depends(get_current_user)
):
    db = get_async_db()
    if not ObjectId.is_valid(trip_id):
        raise HTTPException(status_code=400, detail="Invalid trip ID format")
    
    result = await db.trips.delete_one({
        "_id": ObjectId(trip_id),
        "user_id": current_user["_id"]
    })
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    return {"message": "Trip deleted successfully"}

# Itinerary endpoints inside trip
@router.post("/{trip_id}/itinerary")
async def add_itinerary_item(
    trip_id: str,
    item: ItineraryItemCreate,
    current_user: dict = Depends(get_current_user)
):
    db = get_async_db()
    if not ObjectId.is_valid(trip_id):
        raise HTTPException(status_code=400, detail="Invalid trip ID format")
    
    item_dict = item.dict()
    item_dict["_id"] = str(ObjectId())
    
    result = await db.trips.update_one(
        {"_id": ObjectId(trip_id), "user_id": current_user["_id"]},
        {"$push": {"itinerary": item_dict}, "$set": {"updated_at": datetime.utcnow().isoformat()}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    return item_dict

@router.delete("/{trip_id}/itinerary/{item_id}")
async def delete_itinerary_item(
    trip_id: str,
    item_id: str,
    current_user: dict = Depends(get_current_user)
):
    db = get_async_db()
    if not ObjectId.is_valid(trip_id):
        raise HTTPException(status_code=400, detail="Invalid trip ID format")
    
    result = await db.trips.update_one(
        {"_id": ObjectId(trip_id), "user_id": current_user["_id"]},
        {"$pull": {"itinerary": {"_id": item_id}}, "$set": {"updated_at": datetime.utcnow().isoformat()}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Trip or item not found")
    
    return {"message": "Itinerary item deleted"}

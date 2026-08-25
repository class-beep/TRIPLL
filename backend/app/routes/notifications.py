from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database.connection import get_async_db

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("")
async def get_notifications(current_user: dict = Depends(get_current_user)):
    db = get_async_db()
    cursor = db.notifications.find({"user_id": current_user["_id"]}).sort("created_at", -1)
    notifications = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        notifications.append(doc)
    return notifications

@router.patch("/{notification_id}/read")
async def mark_notification_as_read(
    notification_id: str,
    current_user: dict = Depends(get_current_user)
):
    db = get_async_db()
    if not ObjectId.is_valid(notification_id):
        raise HTTPException(status_code=400, detail="Invalid notification ID format")
    
    result = await db.notifications.update_one(
        {"_id": ObjectId(notification_id), "user_id": current_user["_id"]},
        {"$set": {"read": True}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    return {"message": "Notification marked as read"}

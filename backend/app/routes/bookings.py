from fastapi import APIRouter, HTTPException, Depends, status
from bson import ObjectId
from datetime import datetime
import random
import string
from app.schemas.schemas import BookingCreate, BookingStatusUpdate
from app.middleware.auth import get_current_user
from app.database.connection import get_async_db

router = APIRouter(prefix="/bookings", tags=["Bookings"])

def generate_booking_reference():
    chars = string.ascii_uppercase + string.digits
    code = ''.join(random.choices(chars, k=6))
    return f"TRP-{code}"

@router.post("")
async def create_booking(
    booking_data: BookingCreate,
    current_user: dict = Depends(get_current_user)
):
    db = get_async_db()
    booking_ref = generate_booking_reference()
    
    booking_dict = booking_data.dict()
    booking_dict.update({
        "user_id": current_user["_id"],
        "booking_reference": booking_ref,
        "status": "Confirmed",
        "payment_status": "Paid",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    })
    
    result = await db.bookings.insert_one(booking_dict)
    booking_dict["_id"] = str(result.inserted_id)

    # Automatically create a payment record
    payment_doc = {
        "user_id": current_user["_id"],
        "booking_id": booking_dict["_id"],
        "booking_reference": booking_ref,
        "amount": booking_data.total_price,
        "payment_method": booking_data.payment_method,
        "status": "Success",
        "transaction_id": f"TXN-{random.randint(100000, 999999)}",
        "created_at": datetime.utcnow().isoformat()
    }
    await db.payments.insert_one(payment_doc)

    # Generate a user notification
    notification_doc = {
        "user_id": current_user["_id"],
        "title": "Booking Confirmed! 🎉",
        "message": f"Your booking for '{booking_data.item_name}' (Ref: {booking_ref}) has been confirmed successfully.",
        "type": "booking",
        "read": False,
        "link": f"/booking-confirmation/{booking_dict['_id']}",
        "created_at": datetime.utcnow().isoformat()
    }
    await db.notifications.insert_one(notification_doc)

    return booking_dict

@router.get("")
async def get_user_bookings(current_user: dict = Depends(get_current_user)):
    db = get_async_db()
    cursor = db.bookings.find({"user_id": current_user["_id"]}).sort("created_at", -1)
    bookings = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        bookings.append(doc)
    return bookings

@router.get("/{booking_id}")
async def get_booking_by_id(
    booking_id: str,
    current_user: dict = Depends(get_current_user)
):
    db = get_async_db()
    if not ObjectId.is_valid(booking_id):
        raise HTTPException(status_code=400, detail="Invalid booking ID format")
    
    doc = await db.bookings.find_one({
        "_id": ObjectId(booking_id),
        "user_id": current_user["_id"]
    })
    if not doc:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    doc["_id"] = str(doc["_id"])
    return doc

@router.patch("/{booking_id}")
async def update_booking_status(
    booking_id: str,
    status_update: BookingStatusUpdate,
    current_user: dict = Depends(get_current_user)
):
    db = get_async_db()
    if not ObjectId.is_valid(booking_id):
        raise HTTPException(status_code=400, detail="Invalid booking ID format")
    
    result = await db.bookings.update_one(
        {"_id": ObjectId(booking_id), "user_id": current_user["_id"]},
        {"$set": {"status": status_update.status, "updated_at": datetime.utcnow().isoformat()}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    updated_doc = await db.bookings.find_one({"_id": ObjectId(booking_id)})
    updated_doc["_id"] = str(updated_doc["_id"])
    return updated_doc

@router.delete("/{booking_id}")
async def cancel_booking(
    booking_id: str,
    current_user: dict = Depends(get_current_user)
):
    db = get_async_db()
    if not ObjectId.is_valid(booking_id):
        raise HTTPException(status_code=400, detail="Invalid booking ID format")
    
    result = await db.bookings.update_one(
        {"_id": ObjectId(booking_id), "user_id": current_user["_id"]},
        {"$set": {"status": "Cancelled", "updated_at": datetime.utcnow().isoformat()}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    return {"message": "Booking cancelled successfully"}

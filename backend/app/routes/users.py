from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from datetime import datetime
from app.schemas.schemas import UserProfileUpdate, PasswordChange
from app.middleware.auth import get_current_user
from app.utils.auth import hash_password, verify_password
from app.database.connection import get_async_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    return current_user

@router.patch("/me")
async def update_user_profile(
    profile_data: UserProfileUpdate,
    current_user: dict = Depends(get_current_user)
):
    db = get_async_db()
    update_fields = {k: v for k, v in profile_data.dict().items() if v is not None}
    update_fields["updated_at"] = datetime.utcnow().isoformat()
    
    if update_fields:
        await db.users.update_one(
            {"_id": ObjectId(current_user["_id"])},
            {"$set": update_fields}
        )
    
    updated_user = await db.users.find_one({"_id": ObjectId(current_user["_id"])})
    updated_user["_id"] = str(updated_user["_id"])
    if "password_hash" in updated_user:
        del updated_user["password_hash"]
    
    return updated_user

@router.post("/me/change-password")
async def change_password(
    data: PasswordChange,
    current_user: dict = Depends(get_current_user)
):
    db = get_async_db()
    user = await db.users.find_one({"_id": ObjectId(current_user["_id"])})
    
    if not verify_password(data.current_password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    new_hashed_pwd = hash_password(data.new_password)
    await db.users.update_one(
        {"_id": ObjectId(current_user["_id"])},
        {"$set": {"password_hash": new_hashed_pwd, "updated_at": datetime.utcnow().isoformat()}}
    )
    
    return {"message": "Password changed successfully"}

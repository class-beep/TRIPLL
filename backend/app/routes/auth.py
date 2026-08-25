from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
from bson import ObjectId
from app.schemas.schemas import UserRegister, UserLogin, TokenResponse
from app.utils.auth import hash_password, verify_password, create_access_token
from app.database.connection import get_async_db
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserRegister):
    db = get_async_db()
    existing_user = await db.users.find_one({"email": user_data.email.lower()})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    hashed_pwd = hash_password(user_data.password)
    new_user = {
        "full_name": user_data.full_name,
        "email": user_data.email.lower(),
        "phone": user_data.phone or "",
        "password_hash": hashed_pwd,
        "profile_image": f"https://api.dicebear.com/7.x/avataaars/svg?seed={user_data.full_name}",
        "country": user_data.country or "India",
        "travel_preferences": ["Nature", "Adventure"],
        "preferred_budget": "Moderate",
        "preferred_trip_types": ["Solo", "Friends"],
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }
    
    result = await db.users.insert_one(new_user)
    user_id = str(result.inserted_id)
    
    access_token = create_access_token(data={"sub": user_id})
    new_user["_id"] = user_id
    del new_user["password_hash"]
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": new_user
    }

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    db = get_async_db()
    user = await db.users.find_one({"email": credentials.email.lower()})
    if not user or not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    user_id = str(user["_id"])
    access_token = create_access_token(data={"sub": user_id})
    user["_id"] = user_id
    del user["password_hash"]
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.post("/logout")
async def logout():
    return {"message": "Successfully logged out"}

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    if "password_hash" in current_user:
        del current_user["password_hash"]
    return current_user

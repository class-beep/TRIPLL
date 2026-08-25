from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from datetime import datetime
from app.schemas.schemas import FavoriteCreate
from app.middleware.auth import get_current_user
from app.database.connection import get_async_db

router = APIRouter(prefix="/favorites", tags=["Favorites"])

@router.get("")
async def get_favorites(current_user: dict = Depends(get_current_user)):
    db = get_async_db()
    cursor = db.favorites.find({"user_id": current_user["_id"]}).sort("created_at", -1)
    favorites = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        favorites.append(doc)
    return favorites

@router.post("")
async def toggle_favorite(
    fav: FavoriteCreate,
    current_user: dict = Depends(get_current_user)
):
    db = get_async_db()
    existing = await db.favorites.find_one({
        "user_id": current_user["_id"],
        "item_id": fav.item_id,
        "item_type": fav.item_type
    })
    
    if existing:
        await db.favorites.delete_one({"_id": existing["_id"]})
        return {"action": "removed", "item_id": fav.item_id}
    else:
        doc = fav.dict()
        doc.update({
            "user_id": current_user["_id"],
            "created_at": datetime.utcnow().isoformat()
        })
        result = await db.favorites.insert_one(doc)
        doc["_id"] = str(result.inserted_id)
        return {"action": "added", "favorite": doc}

@router.delete("/{favorite_id}")
async def delete_favorite(
    favorite_id: str,
    current_user: dict = Depends(get_current_user)
):
    db = get_async_db()
    if not ObjectId.is_valid(favorite_id):
        raise HTTPException(status_code=400, detail="Invalid favorite ID format")
    
    result = await db.favorites.delete_one({
        "_id": ObjectId(favorite_id),
        "user_id": current_user["_id"]
    })
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Favorite not found")
    
    return {"message": "Favorite removed successfully"}

from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from datetime import datetime
from app.schemas.schemas import ExpenseCreate
from app.middleware.auth import get_current_user
from app.database.connection import get_async_db

router = APIRouter(prefix="/trips", tags=["Expenses"])

@router.get("/{trip_id}/expenses")
async def get_trip_expenses(
    trip_id: str,
    current_user: dict = Depends(get_current_user)
):
    db = get_async_db()
    if not ObjectId.is_valid(trip_id):
        raise HTTPException(status_code=400, detail="Invalid trip ID format")
    
    trip = await db.trips.find_one({"_id": ObjectId(trip_id), "user_id": current_user["_id"]})
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    cursor = db.expenses.find({"trip_id": trip_id, "user_id": current_user["_id"]}).sort("date", -1)
    expenses = []
    total_spent = 0.0
    category_breakdown = {
        "Hotel": 0.0,
        "Transport": 0.0,
        "Food": 0.0,
        "Activities": 0.0,
        "Shopping": 0.0,
        "Other": 0.0
    }
    
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        expenses.append(doc)
        total_spent += doc.get("amount", 0.0)
        cat = doc.get("category", "Other")
        category_breakdown[cat] = category_breakdown.get(cat, 0.0) + doc.get("amount", 0.0)

    budget = trip.get("budget", 0.0)
    remaining_budget = max(0.0, budget - total_spent)

    return {
        "expenses": expenses,
        "total_budget": budget,
        "total_spent": total_spent,
        "remaining_budget": remaining_budget,
        "category_breakdown": category_breakdown
    }

@router.post("/{trip_id}/expenses")
async def add_expense(
    trip_id: str,
    expense_data: ExpenseCreate,
    current_user: dict = Depends(get_current_user)
):
    db = get_async_db()
    if not ObjectId.is_valid(trip_id):
        raise HTTPException(status_code=400, detail="Invalid trip ID format")
    
    doc = expense_data.dict()
    doc.update({
        "trip_id": trip_id,
        "user_id": current_user["_id"],
        "created_at": datetime.utcnow().isoformat()
    })
    
    result = await db.expenses.insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    return doc

@router.delete("/expenses/{expense_id}")
async def delete_expense(
    expense_id: str,
    current_user: dict = Depends(get_current_user)
):
    db = get_async_db()
    if not ObjectId.is_valid(expense_id):
        raise HTTPException(status_code=400, detail="Invalid expense ID format")
    
    result = await db.expenses.delete_one({
        "_id": ObjectId(expense_id),
        "user_id": current_user["_id"]
    })
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    return {"message": "Expense deleted successfully"}

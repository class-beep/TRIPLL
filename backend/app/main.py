from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import (
    auth,
    users,
    trips,
    destinations,
    hotels,
    transport,
    activities,
    bookings,
    expenses,
    favorites,
    notifications
)

app = FastAPI(
    title="TRIPLL Travel Planner API",
    description="Backend API for TRIPLL Smart Travel Planner",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all route modules
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(trips.router)
app.include_router(destinations.router)
app.include_router(hotels.router)
app.include_router(transport.router)
app.include_router(activities.router)
app.include_router(bookings.router)
app.include_router(expenses.router)
app.include_router(favorites.router)
app.include_router(notifications.router)

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Welcome to TRIPLL Smart Travel Planner API",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

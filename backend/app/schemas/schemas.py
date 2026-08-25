from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Any
from datetime import datetime

# Auth & User Schemas
class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    phone: Optional[str] = ""
    country: Optional[str] = ""

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    profile_image: Optional[str] = None
    country: Optional[str] = None
    travel_preferences: Optional[List[str]] = None
    preferred_budget: Optional[str] = None
    preferred_trip_types: Optional[List[str]] = None

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

class UserResponse(BaseModel):
    id: str = Field(alias="_id")
    full_name: str
    email: str
    phone: Optional[str] = ""
    profile_image: Optional[str] = ""
    country: Optional[str] = ""
    travel_preferences: List[str] = []
    preferred_budget: Optional[str] = "Moderate"
    preferred_trip_types: List[str] = []
    created_at: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

# Destination Schemas
class DestinationCreate(BaseModel):
    name: str
    country: str
    state: Optional[str] = ""
    description: str
    images: List[str]
    category: str  # Beach, Mountain, City, Nature, Adventure, Romantic, Family, Luxury, Hidden Gem
    rating: float = 4.5
    estimated_budget: str
    best_time_to_visit: str
    weather: Optional[str] = ""
    attractions: List[str] = []
    activities: List[str] = []
    hidden_gem: bool = False
    popularity_score: int = 80
    latitude: Optional[float] = 0.0
    longitude: Optional[float] = 0.0

# Room Schema
class RoomType(BaseModel):
    name: str
    description: str
    price_per_night: float
    max_guests: int
    amenities: List[str]
    image: Optional[str] = ""

# Hotel Schema
class HotelCreate(BaseModel):
    name: str
    destination_id: str
    description: str
    images: List[str]
    rating: float = 4.5
    address: str
    amenities: List[str]
    price_per_night: float
    room_types: List[RoomType]
    availability: bool = True

# Activity Schema
class ActivityCreate(BaseModel):
    name: str
    destination_id: str
    description: str
    images: List[str]
    category: str
    duration: str
    price: float
    rating: float = 4.8
    availability: bool = True

# Transport Schema
class TransportCreate(BaseModel):
    transport_type: str  # Flight, Train, Bus
    operator: str
    source: str
    destination: str
    departure_time: str
    arrival_time: str
    duration: str
    price: float
    seat_class: str
    availability: bool = True

# Booking Schema
class BookingCreate(BaseModel):
    item_id: str
    item_type: str  # hotel, activity, transport, package
    item_name: str
    destination_name: str
    image: Optional[str] = ""
    start_date: str
    end_date: Optional[str] = ""
    guests: int = 1
    total_price: float
    base_price: float
    taxes: float
    discount: float = 0.0
    passenger_name: str
    passenger_email: str
    passenger_phone: str
    payment_method: str

class BookingStatusUpdate(BaseModel):
    status: str  # Confirmed, Cancelled, Completed

# Trip & Itinerary Schemas
class ItineraryItemCreate(BaseModel):
    day: int
    title: str
    description: str
    time: Optional[str] = ""
    location: Optional[str] = ""
    category: str  # stay, activity, transport, food
    cost: float = 0.0

class TripCreate(BaseModel):
    name: str
    destination: str
    destination_id: Optional[str] = ""
    start_date: str
    end_date: str
    budget: float
    travelers: int = 1
    image: Optional[str] = ""
    notes: Optional[str] = ""
    hotels: List[str] = []
    activities: List[str] = []
    transport: List[str] = []

class ExpenseCreate(BaseModel):
    category: str  # Hotel, Transport, Food, Activities, Shopping, Other
    title: str
    amount: float
    date: str
    notes: Optional[str] = ""

# Favorite Schema
class FavoriteCreate(BaseModel):
    item_id: str
    item_type: str  # destination, hotel, activity
    title: str
    location: Optional[str] = ""
    image: str
    rating: Optional[float] = 4.5
    price: Optional[str] = ""

# Review Schema
class ReviewCreate(BaseModel):
    item_id: str
    item_type: str
    rating: float
    comment: str

# Notification Schema
class NotificationCreate(BaseModel):
    user_id: str
    title: str
    message: str
    type: str  # booking, payment, trip, system
    link: Optional[str] = ""

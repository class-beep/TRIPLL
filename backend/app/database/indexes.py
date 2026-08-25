def create_indexes(db):
    # Users index
    db.users.create_index("email", unique=True)
    
    # Destinations index
    db.destinations.create_index([("name", 1), ("country", 1)])
    db.destinations.create_index("category")
    db.destinations.create_index("hidden_gem")
    
    # Hotels index
    db.hotels.create_index("destination_id")
    
    # Activities index
    db.activities.create_index("destination_id")
    
    # Bookings index
    db.bookings.create_index("user_id")
    db.bookings.create_index("booking_reference", unique=True)
    
    # Trips index
    db.trips.create_index("user_id")
    
    # Expenses index
    db.expenses.create_index("trip_id")
    
    # Favorites index
    db.favorites.create_index([("user_id", 1), ("item_id", 1), ("item_type", 1)], unique=True)
    
    # Notifications index
    db.notifications.create_index("user_id")
    
    print("Database indexes created successfully.")

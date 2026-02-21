RECORDS = {
    # Roles
    "role_admin": {
        "model": "role",
        "values": {
            "name": "admin",
            "description": "Full access with all permissions"
        },
        "noupdate": True
    },
    "role_fleet_manager": {
        "model": "role",
        "values": {
            "name": "fleet_manager",
            "description": "Fleet Manager - Oversee vehicle health, asset lifecycle, and scheduling"
        },
        "noupdate": True
    },
    "role_dispatcher": {
        "model": "role",
        "values": {
            "name": "dispatcher",
            "description": "Dispatcher - Create trips, assign drivers, and validate cargo loads"
        },
        "noupdate": True
    },
    "role_safety_officer": {
        "model": "role",
        "values": {
            "name": "safety_officer",
            "description": "Safety Officer - Monitor driver compliance, license expirations, and safety scores"
        },
        "noupdate": True
    },
    "role_financial_analyst": {
        "model": "role",
        "values": {
            "name": "financial_analyst",
            "description": "Financial Analyst - Audit fuel spend, maintenance ROI, and operational costs"
        },
        "noupdate": True
    },

    # Admin User
    "user_admin": {
        "model": "user",
        "values": {
            "email": "admin@example.com",
            "full_name": "Administrator",
            "hashed_password": "$P$admin123", # Hashed automatically by loader
            "role_id": "@role_admin",        # Symbolic reference
            "timezone_id": "@tz_utc",        # Default to UTC timezone
            "is_active": True
        },
        "noupdate": True
    },
}

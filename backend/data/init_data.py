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
    
    # Fleet Manager User
    "user_fleet_manager": {
        "model": "user",
        "values": {
            "email": "manager@fleetflow.com",
            "full_name": "Sarah Johnson",
            "hashed_password": "$P$manager123",
            "role_id": "@role_fleet_manager",
            "timezone_id": "@tz_utc",
            "is_active": True
        },
        "noupdate": True
    },
    
    # Dispatcher User
    "user_dispatcher": {
        "model": "user",
        "values": {
            "email": "dispatcher@fleetflow.com",
            "full_name": "Mike Chen",
            "hashed_password": "$P$dispatch123",
            "role_id": "@role_dispatcher",
            "timezone_id": "@tz_utc",
            "is_active": True
        },
        "noupdate": True
    },
    
    # Safety Officer User
    "user_safety_officer": {
        "model": "user",
        "values": {
            "email": "safety@fleetflow.com",
            "full_name": "David Martinez",
            "hashed_password": "$P$safety123",
            "role_id": "@role_safety_officer",
            "timezone_id": "@tz_utc",
            "is_active": True
        },
        "noupdate": True
    },
    
    # Financial Analyst User
    "user_financial_analyst": {
        "model": "user",
        "values": {
            "email": "finance@fleetflow.com",
            "full_name": "Emily Roberts",
            "hashed_password": "$P$finance123",
            "role_id": "@role_financial_analyst",
            "timezone_id": "@tz_utc",
            "is_active": True
        },
        "noupdate": True
    },
}

from datetime import datetime, timedelta

# Calculate dates dynamically
now = datetime.now()
future_1year = (now + timedelta(days=365)).date().isoformat()
future_2years = (now + timedelta(days=730)).date().isoformat()
future_6months = (now + timedelta(days=180)).date().isoformat()
past_30days = (now - timedelta(days=30)).date().isoformat()
past_2days = (now - timedelta(days=2)).isoformat()
past_6days = (now - timedelta(days=6)).date().isoformat()
past_11days = (now - timedelta(days=11)).date().isoformat()
past_16days = (now - timedelta(days=16)).date().isoformat()
yesterday = (now - timedelta(days=1)).date().isoformat()
past_2days_date = (now - timedelta(days=2)).date().isoformat()
past_3days = (now - timedelta(days=3)).date().isoformat()
past_4days = (now - timedelta(days=4)).date().isoformat()
past_5days = (now - timedelta(days=5)).date().isoformat()
tomorrow = (now + timedelta(days=1)).isoformat()
in_2hours = (now + timedelta(hours=2)).isoformat()

RECORDS = {
    # Vehicles - Updated with realistic acquisition costs
    'vehicle_alpha': {
        'model': 'fleet.vehicle',
        'values': {
            'name': 'Truck Alpha',
            'license_plate': 'ABC-1234',
            'vehicle_type': 'truck',
            'region': 'north',
            'max_capacity': 5000.0,
            'odometer': 45000.0,
            'acquisition_cost': 45000.0,  # Lower cost = better ROI
            'status': 'available',
            'active': True
        }
    },
    'vehicle_beta': {
        'model': 'fleet.vehicle',
        'values': {
            'name': 'Truck Beta',
            'license_plate': 'XYZ-5678',
            'vehicle_type': 'truck',
            'region': 'south',
            'max_capacity': 7500.0,
            'odometer': 32000.0,
            'acquisition_cost': 52000.0,  # Higher capacity, higher cost
            'status': 'available',
            'active': True
        }
    },
    'vehicle_gamma': {
        'model': 'fleet.vehicle',
        'values': {
            'name': 'Van Gamma',
            'license_plate': 'DEF-9012',
            'vehicle_type': 'van',
            'region': 'east',
            'max_capacity': 2000.0,
            'odometer': 78000.0,
            'acquisition_cost': 25000.0,  # Older van, lower cost
            'status': 'in_shop',
            'active': True
        }
    },
    'vehicle_delta': {
        'model': 'fleet.vehicle',
        'values': {
            'name': 'Truck Delta',
            'license_plate': 'GHI-3456',
            'vehicle_type': 'truck',
            'region': 'west',
            'max_capacity': 6000.0,
            'odometer': 15000.0,
            'acquisition_cost': 48000.0,  # Newer truck
            'status': 'available',
            'active': True
        }
    },
    
    # Drivers
    'driver_john': {
        'model': 'fleet.driver',
        'values': {
            'name': 'John Smith',
            'license_number': 'DL-2024-001',
            'license_expiry': future_1year,
            'phone': '+1-555-0101',
            'status': 'off_duty',
            'safety_score': 95.0,
            'active': True
        }
    },
    'driver_maria': {
        'model': 'fleet.driver',
        'values': {
            'name': 'Maria Garcia',
            'license_number': 'DL-2024-002',
            'license_expiry': future_2years,
            'phone': '+1-555-0102',
            'status': 'off_duty',
            'safety_score': 98.5,
            'active': True
        }
    },
    'driver_david': {
        'model': 'fleet.driver',
        'values': {
            'name': 'David Chen',
            'license_number': 'DL-2024-003',
            'license_expiry': future_6months,
            'phone': '+1-555-0103',
            'status': 'on_duty',
            'safety_score': 92.0,
            'active': True
        }
    },
    'driver_sarah': {
        'model': 'fleet.driver',
        'values': {
            'name': 'Sarah Johnson',
            'license_number': 'DL-2024-004',
            'license_expiry': past_30days,
            'phone': '+1-555-0104',
            'status': 'suspended',
            'safety_score': 88.0,
            'active': True
        }
    },
    
    # Trips
    'trip_1': {
        'model': 'fleet.trip',
        'values': {
            'name': 'TRIP-20260221-001',
            'vehicle_id': '@vehicle_alpha',
            'driver_id': '@driver_john',
            'origin': 'New York, NY',
            'destination': 'Boston, MA',
            'cargo_weight': 4500.0,
            'distance': 215.0,
            'status': 'completed',
            'scheduled_date': past_2days,
            'start_time': past_2days,
            'end_time': past_2days
        }
    },
    'trip_2': {
        'model': 'fleet.trip',
        'values': {
            'name': 'TRIP-20260221-002',
            'vehicle_id': '@vehicle_beta',
            'driver_id': '@driver_maria',
            'origin': 'Los Angeles, CA',
            'destination': 'San Francisco, CA',
            'cargo_weight': 6000.0,
            'distance': 380.0,
            'status': 'draft',
            'scheduled_date': now.isoformat()
        }
    },
    'trip_3': {
        'model': 'fleet.trip',
        'values': {
            'name': 'TRIP-20260221-003',
            'vehicle_id': '@vehicle_delta',
            'driver_id': '@driver_david',
            'origin': 'Chicago, IL',
            'destination': 'Detroit, MI',
            'cargo_weight': 3500.0,
            'distance': 280.0,
            'status': 'draft',
            'scheduled_date': in_2hours
        }
    },
    'trip_4': {
        'model': 'fleet.trip',
        'values': {
            'name': 'TRIP-20260221-004',
            'vehicle_id': '@vehicle_alpha',
            'driver_id': '@driver_john',
            'origin': 'Miami, FL',
            'destination': 'Orlando, FL',
            'cargo_weight': 2800.0,
            'distance': 235.0,
            'status': 'draft',
            'scheduled_date': tomorrow
        }
    },
    'trip_5': {
        'model': 'fleet.trip',
        'values': {
            'name': 'TRIP-20260215-001',
            'vehicle_id': '@vehicle_beta',
            'driver_id': '@driver_maria',
            'origin': 'Seattle, WA',
            'destination': 'Portland, OR',
            'cargo_weight': 5200.0,
            'distance': 175.0,
            'status': 'completed',
            'scheduled_date': past_6days,
            'start_time': past_6days,
            'end_time': past_6days
        }
    },
    'trip_6': {
        'model': 'fleet.trip',
        'values': {
            'name': 'TRIP-20260210-001',
            'vehicle_id': '@vehicle_delta',
            'driver_id': '@driver_david',
            'origin': 'Houston, TX',
            'destination': 'Dallas, TX',
            'cargo_weight': 4800.0,
            'distance': 240.0,
            'status': 'completed',
            'scheduled_date': past_11days,
            'start_time': past_11days,
            'end_time': past_11days
        }
    },
    'trip_7': {
        'model': 'fleet.trip',
        'values': {
            'name': 'TRIP-20260208-001',
            'vehicle_id': '@vehicle_alpha',
            'driver_id': '@driver_john',
            'origin': 'Phoenix, AZ',
            'destination': 'Las Vegas, NV',
            'cargo_weight': 3900.0,
            'distance': 295.0,
            'status': 'completed',
            'scheduled_date': past_16days,
            'start_time': past_16days,
            'end_time': past_16days
        }
    },
    'trip_8': {
        'model': 'fleet.trip',
        'values': {
            'name': 'TRIP-20260201-001',
            'vehicle_id': '@vehicle_beta',
            'driver_id': '@driver_maria',
            'origin': 'Denver, CO',
            'destination': 'Salt Lake City, UT',
            'cargo_weight': 6500.0,
            'distance': 525.0,
            'status': 'completed',
            'scheduled_date': (now - timedelta(days=20)).isoformat(),
            'start_time': (now - timedelta(days=20)).isoformat(),
            'end_time': (now - timedelta(days=20)).isoformat()
        }
    },
    'trip_9': {
        'model': 'fleet.trip',
        'values': {
            'name': 'TRIP-20260128-001',
            'vehicle_id': '@vehicle_delta',
            'driver_id': '@driver_david',
            'origin': 'Atlanta, GA',
            'destination': 'Nashville, TN',
            'cargo_weight': 5200.0,
            'distance': 250.0,
            'status': 'completed',
            'scheduled_date': (now - timedelta(days=24)).isoformat(),
            'start_time': (now - timedelta(days=24)).isoformat(),
            'end_time': (now - timedelta(days=24)).isoformat()
        }
    },
    'trip_10': {
        'model': 'fleet.trip',
        'values': {
            'name': 'TRIP-20260125-001',
            'vehicle_id': '@vehicle_alpha',
            'driver_id': '@driver_john',
            'origin': 'Portland, OR',
            'destination': 'Sacramento, CA',
            'cargo_weight': 4200.0,
            'distance': 585.0,
            'status': 'completed',
            'scheduled_date': (now - timedelta(days=27)).isoformat(),
            'start_time': (now - timedelta(days=27)).isoformat(),
            'end_time': (now - timedelta(days=27)).isoformat()
        }
    },
    
    # Maintenance Logs - Realistic costs for the mileage
    'maint_1': {
        'model': 'fleet.maintenance.log',
        'values': {
            'name': 'MAINT-20260215-001',
            'vehicle_id': '@vehicle_gamma',
            'service_type': 'repair',
            'service_date': past_6days,
            'cost': 450.00,  # Reduced - fuel pump replacement
            'odometer_reading': 77800.0,
            'description': 'Engine repair - replaced fuel pump',
            'notes': 'Vehicle will be ready in 2 days'
        }
    },
    'maint_2': {
        'model': 'fleet.maintenance.log',
        'values': {
            'name': 'MAINT-20260210-001',
            'vehicle_id': '@vehicle_alpha',
            'service_type': 'routine',
            'service_date': past_11days,
            'cost': 120.00,  # Reduced - routine maintenance
            'odometer_reading': 44500.0,
            'description': 'Regular maintenance - oil change and filter replacement'
        }
    },
    'maint_3': {
        'model': 'fleet.maintenance.log',
        'values': {
            'name': 'MAINT-20260205-001',
            'vehicle_id': '@vehicle_beta',
            'service_type': 'tire_change',
            'service_date': past_16days,
            'cost': 350.00,  # Reduced - tire replacement
            'odometer_reading': 31500.0,
            'description': 'Replaced all 4 tires'
        }
    },
    'maint_4': {
        'model': 'fleet.maintenance.log',
        'values': {
            'name': 'MAINT-20260208-001',
            'vehicle_id': '@vehicle_delta',
            'service_type': 'routine',
            'service_date': past_16days,
            'cost': 130.00,  # Reduced - routine maintenance
            'odometer_reading': 14500.0,
            'description': 'Regular maintenance - oil change and inspection'
        }
    },
    
    # Expenses - Realistic fuel consumption (6-10 km/L for trucks, 8-12 km/L for vans)
    'exp_1': {
        'model': 'fleet.expense',
        'values': {
            'name': 'EXP-20260220-001',
            'vehicle_id': '@vehicle_alpha',
            'expense_type': 'fuel',
            'expense_date': yesterday,
            'cost': 45.00,  # ~30 liters @ $1.5/L
            'fuel_liters': 30.0,  # For ~215 km trip = 7.2 km/L
            'odometer_reading': 45000.0,
            'description': 'Fuel refill at Shell Station'
        }
    },
    'exp_2': {
        'model': 'fleet.expense',
        'values': {
            'name': 'EXP-20260219-001',
            'vehicle_id': '@vehicle_beta',
            'expense_type': 'fuel',
            'expense_date': past_2days_date,
            'cost': 30.00,  # ~20 liters @ $1.5/L (partial fill)
            'fuel_liters': 20.0,
            'odometer_reading': 32000.0,
            'description': 'Fuel refill at BP Station'
        }
    },
    'exp_3': {
        'model': 'fleet.expense',
        'values': {
            'name': 'EXP-20260218-001',
            'vehicle_id': '@vehicle_delta',
            'expense_type': 'toll',
            'expense_date': past_3days,
            'cost': 35.00,
            'description': 'Highway toll - Interstate 95'
        }
    },
    'exp_4': {
        'model': 'fleet.expense',
        'values': {
            'name': 'EXP-20260217-001',
            'vehicle_id': '@vehicle_alpha',
            'expense_type': 'parking',
            'expense_date': past_4days,
            'cost': 20.00,
            'description': 'Overnight parking at warehouse'
        }
    },
    'exp_5': {
        'model': 'fleet.expense',
        'values': {
            'name': 'EXP-20260216-001',
            'vehicle_id': '@vehicle_beta',
            'expense_type': 'fuel',
            'expense_date': past_5days,
            'cost': 27.00,  # ~18 liters @ $1.5/L
            'fuel_liters': 18.0,  # For ~175 km trip = 9.7 km/L (good efficiency)
            'odometer_reading': 31500.0,
            'description': 'Fuel refill at Chevron Station'
        }
    },
    'exp_6': {
        'model': 'fleet.expense',
        'values': {
            'name': 'EXP-20260214-001',
            'vehicle_id': '@vehicle_delta',
            'expense_type': 'fuel',
            'expense_date': past_6days,
            'cost': 36.00,  # ~24 liters @ $1.5/L
            'fuel_liters': 24.0,  # For ~240 km trip = 10 km/L (excellent)
            'odometer_reading': 14800.0,
            'description': 'Fuel refill at Mobil Station'
        }
    },
    'exp_7': {
        'model': 'fleet.expense',
        'values': {
            'name': 'EXP-20260212-001',
            'vehicle_id': '@vehicle_alpha',
            'expense_type': 'fuel',
            'expense_date': past_11days,
            'cost': 54.00,  # ~36 liters @ $1.5/L
            'fuel_liters': 36.0,  # For ~295 km trip = 8.2 km/L
            'odometer_reading': 44200.0,
            'description': 'Fuel refill at Shell Station'
        }
    },
    'exp_8': {
        'model': 'fleet.expense',
        'values': {
            'name': 'EXP-20260206-001',
            'vehicle_id': '@vehicle_beta',
            'expense_type': 'fuel',
            'expense_date': past_16days,
            'cost': 30.00,  # ~20 liters @ $1.5/L (partial fill)
            'fuel_liters': 20.0,
            'odometer_reading': 31200.0,
            'description': 'Fuel refill at Shell Station'
        }
    },
    'exp_9': {
        'model': 'fleet.expense',
        'values': {
            'name': 'EXP-20260201-001',
            'vehicle_id': '@vehicle_beta',
            'expense_type': 'fuel',
            'expense_date': (now - timedelta(days=20)).date().isoformat(),
            'cost': 78.00,  # ~52 liters for 525 km = 10.1 km/L
            'fuel_liters': 52.0,
            'odometer_reading': 30800.0,
            'description': 'Fuel refill at Chevron Station'
        }
    },
    'exp_10': {
        'model': 'fleet.expense',
        'values': {
            'name': 'EXP-20260128-001',
            'vehicle_id': '@vehicle_delta',
            'expense_type': 'fuel',
            'expense_date': (now - timedelta(days=24)).date().isoformat(),
            'cost': 37.50,  # ~25 liters for 250 km = 10 km/L
            'fuel_liters': 25.0,
            'odometer_reading': 14200.0,
            'description': 'Fuel refill at BP Station'
        }
    },
    'exp_11': {
        'model': 'fleet.expense',
        'values': {
            'name': 'EXP-20260125-001',
            'vehicle_id': '@vehicle_alpha',
            'expense_type': 'fuel',
            'expense_date': (now - timedelta(days=27)).date().isoformat(),
            'cost': 87.75,  # ~58.5 liters for 585 km = 10 km/L
            'fuel_liters': 58.5,
            'odometer_reading': 43500.0,
            'description': 'Fuel refill at Shell Station'
        }
    }
}

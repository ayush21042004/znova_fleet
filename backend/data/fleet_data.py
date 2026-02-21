from datetime import datetime, timedelta

def load_fleet_demo_data(env):
    """Load demo data for fleet management"""
    
    # Create Vehicles
    vehicle1 = env['fleet.vehicle'].create({
        'name': 'Truck Alpha',
        'license_plate': 'ABC-1234',
        'max_capacity': 5000.0,
        'odometer': 45000.0,
        'status': 'available',
        'active': True
    })
    
    vehicle2 = env['fleet.vehicle'].create({
        'name': 'Truck Beta',
        'license_plate': 'XYZ-5678',
        'max_capacity': 7500.0,
        'odometer': 32000.0,
        'status': 'available',
        'active': True
    })
    
    vehicle3 = env['fleet.vehicle'].create({
        'name': 'Van Gamma',
        'license_plate': 'DEF-9012',
        'max_capacity': 2000.0,
        'odometer': 78000.0,
        'status': 'in_shop',
        'active': True
    })
    
    vehicle4 = env['fleet.vehicle'].create({
        'name': 'Truck Delta',
        'license_plate': 'GHI-3456',
        'max_capacity': 6000.0,
        'odometer': 15000.0,
        'status': 'available',
        'active': True
    })
    
    print("✓ Created 4 vehicles")
    
    # Create Drivers
    driver1 = env['fleet.driver'].create({
        'name': 'John Smith',
        'license_number': 'DL-2024-001',
        'license_expiry': (datetime.now() + timedelta(days=365)).date(),
        'phone': '+1-555-0101',
        'status': 'off_duty',
        'safety_score': 95.0,
        'active': True
    })
    
    driver2 = env['fleet.driver'].create({
        'name': 'Maria Garcia',
        'license_number': 'DL-2024-002',
        'license_expiry': (datetime.now() + timedelta(days=730)).date(),
        'phone': '+1-555-0102',
        'status': 'off_duty',
        'safety_score': 98.5,
        'active': True
    })
    
    driver3 = env['fleet.driver'].create({
        'name': 'David Chen',
        'license_number': 'DL-2024-003',
        'license_expiry': (datetime.now() + timedelta(days=180)).date(),
        'phone': '+1-555-0103',
        'status': 'on_duty',
        'safety_score': 92.0,
        'active': True
    })
    
    driver4 = env['fleet.driver'].create({
        'name': 'Sarah Johnson',
        'license_number': 'DL-2024-004',
        'license_expiry': (datetime.now() - timedelta(days=30)).date(),  # Expired
        'phone': '+1-555-0104',
        'status': 'suspended',
        'safety_score': 88.0,
        'active': True
    })
    
    print("✓ Created 4 drivers")
    
    # Create Trips
    trip1 = env['fleet.trip'].create({
        'name': 'TRIP-20260221-001',
        'vehicle_id': vehicle1.id,
        'driver_id': driver1.id,
        'origin': 'New York, NY',
        'destination': 'Boston, MA',
        'cargo_weight': 4500.0,
        'distance': 215.0,
        'status': 'completed',
        'scheduled_date': datetime.now() - timedelta(days=2),
        'start_time': datetime.now() - timedelta(days=2, hours=8),
        'end_time': datetime.now() - timedelta(days=2, hours=4)
    })
    
    trip2 = env['fleet.trip'].create({
        'name': 'TRIP-20260221-002',
        'vehicle_id': vehicle2.id,
        'driver_id': driver2.id,
        'origin': 'Los Angeles, CA',
        'destination': 'San Francisco, CA',
        'cargo_weight': 6000.0,
        'distance': 380.0,
        'status': 'in_progress',
        'scheduled_date': datetime.now(),
        'start_time': datetime.now() - timedelta(hours=3)
    })
    
    trip3 = env['fleet.trip'].create({
        'name': 'TRIP-20260221-003',
        'vehicle_id': vehicle4.id,
        'driver_id': driver3.id,
        'origin': 'Chicago, IL',
        'destination': 'Detroit, MI',
        'cargo_weight': 3500.0,
        'distance': 280.0,
        'status': 'dispatched',
        'scheduled_date': datetime.now() + timedelta(hours=2)
    })
    
    trip4 = env['fleet.trip'].create({
        'name': 'TRIP-20260221-004',
        'vehicle_id': vehicle1.id,
        'driver_id': driver1.id,
        'origin': 'Miami, FL',
        'destination': 'Orlando, FL',
        'cargo_weight': 2800.0,
        'distance': 235.0,
        'status': 'draft',
        'scheduled_date': datetime.now() + timedelta(days=1)
    })
    
    print("✓ Created 4 trips")
    
    # Create Maintenance Logs
    maint1 = env['fleet.maintenance.log'].create({
        'name': 'MAINT-20260215-001',
        'vehicle_id': vehicle3.id,
        'service_type': 'repair',
        'service_date': (datetime.now() - timedelta(days=6)).date(),
        'cost': 850.00,
        'odometer_reading': 77800.0,
        'description': 'Engine repair - replaced fuel pump',
        'notes': 'Vehicle will be ready in 2 days'
    })
    
    maint2 = env['fleet.maintenance.log'].create({
        'name': 'MAINT-20260210-001',
        'vehicle_id': vehicle1.id,
        'service_type': 'routine',
        'service_date': (datetime.now() - timedelta(days=11)).date(),
        'cost': 250.00,
        'odometer_reading': 44500.0,
        'description': 'Regular maintenance - oil change and filter replacement'
    })
    
    maint3 = env['fleet.maintenance.log'].create({
        'name': 'MAINT-20260205-001',
        'vehicle_id': vehicle2.id,
        'service_type': 'tire_change',
        'service_date': (datetime.now() - timedelta(days=16)).date(),
        'cost': 600.00,
        'odometer_reading': 31500.0,
        'description': 'Replaced all 4 tires'
    })
    
    print("✓ Created 3 maintenance logs")
    
    # Create Expenses
    exp1 = env['fleet.expense'].create({
        'name': 'EXP-20260220-001',
        'vehicle_id': vehicle1.id,
        'expense_type': 'fuel',
        'expense_date': (datetime.now() - timedelta(days=1)).date(),
        'cost': 180.00,
        'fuel_liters': 120.0,
        'odometer_reading': 45000.0,
        'description': 'Fuel refill at Shell Station'
    })
    
    exp2 = env['fleet.expense'].create({
        'name': 'EXP-20260219-001',
        'vehicle_id': vehicle2.id,
        'expense_type': 'fuel',
        'expense_date': (datetime.now() - timedelta(days=2)).date(),
        'cost': 220.00,
        'fuel_liters': 150.0,
        'odometer_reading': 32000.0,
        'description': 'Fuel refill at BP Station'
    })
    
    exp3 = env['fleet.expense'].create({
        'name': 'EXP-20260218-001',
        'vehicle_id': vehicle4.id,
        'expense_type': 'toll',
        'expense_date': (datetime.now() - timedelta(days=3)).date(),
        'cost': 45.00,
        'description': 'Highway toll - Interstate 95'
    })
    
    exp4 = env['fleet.expense'].create({
        'name': 'EXP-20260217-001',
        'vehicle_id': vehicle1.id,
        'expense_type': 'parking',
        'expense_date': (datetime.now() - timedelta(days=4)).date(),
        'cost': 25.00,
        'description': 'Overnight parking at warehouse'
    })
    
    exp5 = env['fleet.expense'].create({
        'name': 'EXP-20260216-001',
        'vehicle_id': vehicle2.id,
        'expense_type': 'fuel',
        'expense_date': (datetime.now() - timedelta(days=5)).date(),
        'cost': 195.00,
        'fuel_liters': 130.0,
        'odometer_reading': 31500.0,
        'description': 'Fuel refill at Chevron Station'
    })
    
    print("✓ Created 5 expenses")
    
    print("\n🚀 Fleet demo data loaded successfully!")
    print(f"   - {len([vehicle1, vehicle2, vehicle3, vehicle4])} Vehicles")
    print(f"   - {len([driver1, driver2, driver3, driver4])} Drivers")
    print(f"   - {len([trip1, trip2, trip3, trip4])} Trips")
    print(f"   - {len([maint1, maint2, maint3])} Maintenance Logs")
    print(f"   - {len([exp1, exp2, exp3, exp4, exp5])} Expenses")

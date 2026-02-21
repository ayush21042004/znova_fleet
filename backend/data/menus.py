from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from backend.core.menu_manager import MenuManager, MenuItem

def initialize_menus(menu_manager: 'MenuManager'):
    from backend.core.menu_manager import MenuItem

    # --- Main Group ---
    menu_manager.add_item("Main", MenuItem(
        "dashboard", "Dashboard", "/dashboard", "LayoutDashboard", sequence=10
    ))

    # --- Fleet Management Group ---
    fleet_group = "Fleet Management"
    menu_manager.add_item(fleet_group, MenuItem(
        "vehicles", "Vehicles", "/models/fleet.vehicle", "Truck", sequence=10, 
        groups=['admin', 'fleet_manager', 'dispatcher']
    ))
    menu_manager.add_item(fleet_group, MenuItem(
        "drivers", "Drivers", "/models/fleet.driver", "UserCircle", sequence=20,
        groups=['admin', 'fleet_manager', 'dispatcher', 'safety_officer']
    ))
    menu_manager.add_item(fleet_group, MenuItem(
        "trips", "Trips", "/models/fleet.trip", "MapPin", sequence=30,
        groups=['admin', 'fleet_manager', 'dispatcher']
    ))
    menu_manager.add_item(fleet_group, MenuItem(
        "maintenance", "Maintenance Logs", "/models/fleet.maintenance", "Wrench", sequence=40,
        groups=['admin', 'fleet_manager']
    ))
    menu_manager.add_item(fleet_group, MenuItem(
        "expenses", "Fuel & Expenses", "/models/fleet.expense", "DollarSign", sequence=50,
        groups=['admin', 'fleet_manager', 'financial_analyst']
    ))

    # --- Analytics Group ---
    analytics_group = "Analytics"
    menu_manager.add_item(analytics_group, MenuItem(
        "reports", "Reports & Analytics", "/analytics/reports", "TrendingUp", sequence=10,
        groups=['admin', 'fleet_manager', 'financial_analyst']
    ))

    # --- Administration Group (Parent menu with children) ---
    administration_group = "Administration"
    menu_manager.add_item(administration_group, MenuItem(
        name="admin_root",
        label="System Settings",
        icon="Settings",
        sequence=10,
        groups=['admin'],
        children=[
            MenuItem("users", "Users", "/models/user", "Users"),
            MenuItem("sequences", "Sequences", "/models/sequence", "LayoutGrid"),
            MenuItem("crons", "Cron Jobs", "/models/cron", "Clock")
        ]
    ))

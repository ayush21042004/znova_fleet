from backend.core.znova_model import ZnovaModel
from backend.core import fields, api

class Vehicle(ZnovaModel):
    __tablename__ = "fleet_vehicle"
    _model_name_ = "fleet.vehicle"
    _name_field_ = "name"
    _description_ = "Fleet Vehicle"

    # Basic Information
    name = fields.Char(label="Vehicle Name", required=True, tracking=True)
    license_plate = fields.Char(label="License Plate", required=True, tracking=True)
    
    vehicle_type = fields.Selection([
        ('truck', 'Truck'),
        ('van', 'Van'),
        ('bike', 'Bike')
    ], label="Vehicle Type", required=True, default='truck', tracking=True, options={
        'truck': {'label': 'Truck', 'color': 'primary'},
        'van': {'label': 'Van', 'color': 'info'},
        'bike': {'label': 'Bike', 'color': 'success'}
    })
    
    region = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
        ('central', 'Central')
    ], label="Region", required=True, default='central', tracking=True, options={
        'north': {'label': 'North', 'color': 'primary'},
        'south': {'label': 'South', 'color': 'success'},
        'east': {'label': 'East', 'color': 'warning'},
        'west': {'label': 'West', 'color': 'info'},
        'central': {'label': 'Central', 'color': 'secondary'}
    })
    
    max_capacity = fields.Float(label="Max Capacity (kg)", required=True, tracking=True)
    odometer = fields.Float(label="Odometer (km)", default=0.0, tracking=True)
    acquisition_cost = fields.Float(label="Acquisition Cost ($)", required=True, default=30000.0, tracking=True, help="Purchase price of the vehicle")
    status = fields.Selection([
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('in_shop', 'In Shop'),
        ('retired', 'Retired')
    ], label="Status", default='available', tracking=True, options={
        'available': {'label': 'Available', 'color': 'success'},
        'in_use': {'label': 'In Use', 'color': 'warning'},
        'in_shop': {'label': 'In Shop', 'color': 'danger'},
        'retired': {'label': 'Retired', 'color': 'secondary'}
    })
    
    # Relationships
    trip_ids = fields.One2many("fleet.trip", "vehicle_id", label="Trips")
    maintenance_log_ids = fields.One2many("fleet.maintenance.log", "vehicle_id", label="Maintenance Logs")
    expense_ids = fields.One2many("fleet.expense", "vehicle_id", label="Expenses")
    
    # Computed fields - Basic Stats (readonly, not stored)
    total_trips = fields.Integer(label="Total Trips", compute="_compute_stats", store=False, readonly=True)
    completed_trips = fields.Integer(label="Completed Trips", compute="_compute_stats", store=False, readonly=True)
    total_distance = fields.Float(label="Total Distance (km)", compute="_compute_stats", store=False, readonly=True)
    total_maintenance_cost = fields.Float(label="Total Maintenance Cost ($)", compute="_compute_stats", store=False, readonly=True)
    total_fuel_cost = fields.Float(label="Total Fuel Cost ($)", compute="_compute_stats", store=False, readonly=True)
    total_fuel_liters = fields.Float(label="Total Fuel Consumed (L)", compute="_compute_stats", store=False, readonly=True)
    
    # Computed fields - Analytics (readonly, not stored)
    fuel_efficiency = fields.Float(label="Fuel Efficiency (km/L)", compute="_compute_analytics", store=False, readonly=True)
    vehicle_roi = fields.Float(label="ROI (%)", compute="_compute_analytics", store=False, readonly=True, help="Return on Investment: (Revenue - Costs) / Acquisition Cost × 100")
    total_revenue = fields.Float(label="Total Revenue ($)", compute="_compute_analytics", store=False, readonly=True)
    total_operational_cost = fields.Float(label="Total Operational Cost ($)", compute="_compute_analytics", store=False, readonly=True)
    
    active = fields.Boolean(label="Active", default=True, tracking=True)

    _role_permissions = {
        "fleet_manager": {"create": True, "read": True, "write": True, "delete": True},
        "dispatcher": {"create": False, "read": True, "write": True, "delete": False},
        "safety_officer": {"create": False, "read": True, "write": False, "delete": False},
        "financial_analyst": {"create": False, "read": True, "write": False, "delete": False}
    }

    _search_config = {
        "filters": [
            {
                "name": "available",
                "label": "Available Vehicles",
                "domain": "[('status', '=', 'available')]"
            },
            {
                "name": "in_use",
                "label": "In Use",
                "domain": "[('status', '=', 'in_use')]"
            },
            {
                "name": "in_shop",
                "label": "In Shop",
                "domain": "[('status', '=', 'in_shop')]"
            },
            {
                "name": "active_only",
                "label": "Active Vehicles",
                "domain": "[('active', '=', True)]"
            },
            {
                "name": "trucks",
                "label": "Trucks",
                "domain": "[('vehicle_type', '=', 'truck')]"
            },
            {
                "name": "vans",
                "label": "Vans",
                "domain": "[('vehicle_type', '=', 'van')]"
            },
            {
                "name": "bikes",
                "label": "Bikes",
                "domain": "[('vehicle_type', '=', 'bike')]"
            },
            {
                "name": "north_region",
                "label": "North Region",
                "domain": "[('region', '=', 'north')]"
            },
            {
                "name": "south_region",
                "label": "South Region",
                "domain": "[('region', '=', 'south')]"
            },
            {
                "name": "east_region",
                "label": "East Region",
                "domain": "[('region', '=', 'east')]"
            },
            {
                "name": "west_region",
                "label": "West Region",
                "domain": "[('region', '=', 'west')]"
            },
            {
                "name": "central_region",
                "label": "Central Region",
                "domain": "[('region', '=', 'central')]"
            }
        ],
        "group_by": [
            {
                "name": "by_status",
                "label": "By Status",
                "field": "status"
            },
            {
                "name": "by_vehicle_type",
                "label": "By Vehicle Type",
                "field": "vehicle_type"
            },
            {
                "name": "by_region",
                "label": "By Region",
                "field": "region"
            }
        ]
    }

    _ui_views = {
        "list": {
            "fields": ["name", "license_plate", "vehicle_type", "region", "max_capacity", "odometer", "status", "active", 
                      "total_distance", "total_revenue", 
                      "total_fuel_cost", "total_maintenance_cost"]
        },
        "form": {
            "show_audit_log": True,
            "tabs": [
                {
                    "title": "General",
                    "groups": [
                        {
                            "title": "Vehicle Information",
                            "fields": ["name", "license_plate", "vehicle_type", "region", "status", "active"]
                        },
                        {
                            "title": "Specifications",
                            "fields": ["max_capacity", "odometer", "acquisition_cost"]
                        }
                    ]
                },
                {
                    "title": "Statistics",
                    "groups": [
                        {
                            "title": "Trip Statistics",
                            "fields": ["total_trips", "completed_trips", "total_distance"]
                        },
                        {
                            "title": "Cost Breakdown",
                            "fields": ["total_fuel_cost", "total_maintenance_cost", "total_operational_cost"]
                        },
                        {
                            "title": "Performance Analytics",
                            "fields": ["fuel_efficiency", "total_revenue", "vehicle_roi"]
                        }
                    ]
                },
                {
                    "title": "Trips",
                    "fields": ["trip_ids"]
                },
                {
                    "title": "Maintenance",
                    "fields": ["maintenance_log_ids"]
                },
                {
                    "title": "Expenses",
                    "fields": ["expense_ids"]
                }
            ]
        }
    }

    @api.depends('trip_ids', 'maintenance_log_ids', 'expense_ids')
    def _compute_stats(self):
        """Compute basic statistics from related records"""
        # Total trips
        self.total_trips = len(self.trip_ids) if self.trip_ids else 0
        
        # Completed trips and distance
        completed_trips = [t for t in (self.trip_ids or []) if t.status == 'completed']
        self.completed_trips = len(completed_trips)
        self.total_distance = sum(t.distance or 0 for t in completed_trips)
        
        # Maintenance costs
        self.total_maintenance_cost = sum(log.cost or 0 for log in (self.maintenance_log_ids or []))
        
        # Fuel costs and liters from expenses
        fuel_expenses = [e for e in (self.expense_ids or []) if e.expense_type == 'fuel']
        self.total_fuel_cost = sum(e.cost or 0 for e in fuel_expenses)
        self.total_fuel_liters = sum(e.fuel_liters or 0 for e in fuel_expenses)
    
    @api.depends('total_distance', 'total_fuel_liters', 'total_fuel_cost', 'total_maintenance_cost', 'acquisition_cost')
    def _compute_analytics(self):
        """Compute analytics metrics: Fuel Efficiency and ROI"""
        # Fuel Efficiency: km / L
        if self.total_fuel_liters and self.total_fuel_liters > 0:
            self.fuel_efficiency = self.total_distance / self.total_fuel_liters
        else:
            self.fuel_efficiency = 0.0
        
        # Total operational cost
        self.total_operational_cost = (self.total_fuel_cost or 0) + (self.total_maintenance_cost or 0)
        
        # Revenue calculation (more realistic for fleet business)
        # Using $3.5 per km for trucks (typical freight rates)
        # This accounts for: base rate + fuel surcharge + accessorial charges
        revenue_per_km = 3.5 if self.max_capacity > 5000 else 2.8  # Trucks vs Vans
        self.total_revenue = (self.total_distance or 0) * revenue_per_km
        
        # Vehicle ROI: (Revenue - (Maintenance + Fuel)) / Acquisition Cost × 100
        if self.acquisition_cost and self.acquisition_cost > 0:
            self.vehicle_roi = ((self.total_revenue - self.total_operational_cost) / self.acquisition_cost) * 100
        else:
            self.vehicle_roi = 0.0

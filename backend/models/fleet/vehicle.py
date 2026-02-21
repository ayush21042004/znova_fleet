from backend.core.znova_model import ZnovaModel
from backend.core import fields, api

class Vehicle(ZnovaModel):
    __tablename__ = "fleet_vehicle"
    _model_name_ = "fleet.vehicle"
    _name_field_ = "name"
    _description_ = "Fleet Vehicle"

    # Basic Information
    name = fields.Char(label="Vehicle Name", required=True, tracking=True, help="Unique identifier for the vehicle")
    license_plate = fields.Char(label="License Plate", required=True, tracking=True, help="Vehicle registration number")
    
    vehicle_type = fields.Selection([
        ('truck', 'Truck'),
        ('van', 'Van'),
        ('bike', 'Bike')
    ], label="Vehicle Type", required=True, default='truck', tracking=True, options={
        'truck': {'label': 'Truck', 'color': 'primary'},
        'van': {'label': 'Van', 'color': 'info'},
        'bike': {'label': 'Bike', 'color': 'success'}
    }, help="Type of vehicle for filtering and reporting")
    
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
    }, help="Operating region for the vehicle")
    
    max_capacity = fields.Float(label="Max Capacity (kg)", required=True, tracking=True,
                                help="Maximum cargo weight capacity")
    odometer = fields.Float(label="Odometer (km)", default=0.0, tracking=True,
                           help="Current odometer reading")
    acquisition_cost = fields.Float(label="Acquisition Cost ($)", required=True, default=30000.0, tracking=True,
                                   help="Purchase price of the vehicle (used for ROI calculation)")
    status = fields.Selection([
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('in_shop', 'In Shop'),
        ('retired', 'Retired')
    ], label="Status", default='available', tracking=True, readonly=True, options={
        'available': {'label': 'Available', 'color': 'success'},
        'in_use': {'label': 'In Use', 'color': 'warning'},
        'in_shop': {'label': 'In Shop', 'color': 'danger'},
        'retired': {'label': 'Retired', 'color': 'secondary'}
    }, help="Current operational status (auto-updated by system)")
    
    # Relationships
    trip_ids = fields.One2many("fleet.trip", "vehicle_id", label="Trips",
                              columns=["name", "driver_id", "origin", "destination", "distance", "status"],
                              show_label=False, readonly=True)
    maintenance_log_ids = fields.One2many("fleet.maintenance.log", "vehicle_id", label="Maintenance Logs",
                                         columns=["name", "service_type", "service_date", "cost"],
                                         show_label=False, readonly=True)
    expense_ids = fields.One2many("fleet.expense", "vehicle_id", label="Expenses",
                                 columns=["name", "expense_type", "expense_date", "cost", "fuel_liters"],
                                 show_label=False, readonly=True)
    
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
    cost_per_km = fields.Float(label="Cost per km ($/km)", compute="_compute_analytics", store=False, readonly=True, help="Total operational cost divided by total distance")
    
    active = fields.Boolean(label="Active", default=True, tracking=True)

    _role_permissions = {
        "fleet_manager": {"create": True, "read": True, "write": True, "delete": True},
        "dispatcher": {"create": False, "read": True, "write": False, "delete": False},
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
                      "total_fuel_cost", "total_maintenance_cost",
                      "fuel_efficiency", "vehicle_roi"]
        },
        "form": {
            "show_audit_log": True,
            "tabs": [
                {
                    "title": "General",
                    "groups": [
                        {
                            "title": "Vehicle Information",
                            "fields": ["name", "license_plate", "vehicle_type", "region", "active"]
                        },
                        {
                            "title": "Specifications",
                            "fields": ["max_capacity", "odometer", "acquisition_cost"]
                        },
                        {
                            "title": "Status",
                            "fields": ["status"]
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
                            "fields": ["fuel_efficiency", "cost_per_km", "total_revenue", "vehicle_roi"]
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
            ],
            "header_buttons": [
                {
                    "name": "action_mark_available",
                    "label": "Mark as Available",
                    "type": "success",
                    "method": "action_mark_available",
                    "invisible": "[('status', '!=', 'in_shop')]"
                },
                {
                    "name": "action_retire",
                    "label": "Retire Vehicle",
                    "type": "secondary",
                    "method": "action_retire",
                    "invisible": "[('status', '=', 'retired')]"
                }
            ]
        }
    }

    @api.depends('trip_ids', 'maintenance_log_ids', 'expense_ids')
    def _compute_stats(self):
        """Compute basic statistics from related records"""
        # Handle None or empty relationships
        if not hasattr(self, 'trip_ids') or self.trip_ids is None:
            self.total_trips = 0
            self.completed_trips = 0
            self.total_distance = 0.0
            self.total_maintenance_cost = 0.0
            self.total_fuel_cost = 0.0
            self.total_fuel_liters = 0.0
            return
        
        # Total trips
        self.total_trips = len(self.trip_ids) if self.trip_ids else 0
        
        # Completed trips and distance
        completed_trips = [t for t in (self.trip_ids or []) if hasattr(t, 'status') and t.status == 'completed']
        self.completed_trips = len(completed_trips)
        self.total_distance = round(sum(getattr(t, 'distance', 0) or 0 for t in completed_trips), 2)
        
        # Maintenance costs
        if hasattr(self, 'maintenance_log_ids') and self.maintenance_log_ids:
            self.total_maintenance_cost = round(sum(getattr(log, 'cost', 0) or 0 for log in self.maintenance_log_ids), 2)
        else:
            self.total_maintenance_cost = 0.0
        
        # Fuel costs and liters from expenses
        if hasattr(self, 'expense_ids') and self.expense_ids:
            fuel_expenses = [e for e in self.expense_ids if hasattr(e, 'expense_type') and e.expense_type == 'fuel']
            self.total_fuel_cost = round(sum(getattr(e, 'cost', 0) or 0 for e in fuel_expenses), 2)
            self.total_fuel_liters = round(sum(getattr(e, 'fuel_liters', 0) or 0 for e in fuel_expenses), 2)
        else:
            self.total_fuel_cost = 0.0
            self.total_fuel_liters = 0.0
    
    @api.depends('total_distance', 'total_fuel_liters', 'total_fuel_cost', 'total_maintenance_cost', 'acquisition_cost')
    def _compute_analytics(self):
        """Compute analytics metrics: Fuel Efficiency and ROI"""
        # Ensure stats are computed first (dependency chain)
        self._compute_stats()
        
        # Handle None or missing computed stats
        if not hasattr(self, 'total_distance'):
            self.fuel_efficiency = 0.0
            self.total_operational_cost = 0.0
            self.total_revenue = 0.0
            self.vehicle_roi = 0.0
            return
        
        # Fuel Efficiency: km / L
        total_fuel = getattr(self, 'total_fuel_liters', 0) or 0
        total_dist = getattr(self, 'total_distance', 0) or 0
        
        if total_fuel and total_fuel > 0 and total_dist > 0:
            self.fuel_efficiency = round(total_dist / total_fuel, 2)
        else:
            self.fuel_efficiency = 0.0
        
        # Total operational cost
        fuel_cost = getattr(self, 'total_fuel_cost', 0) or 0
        maint_cost = getattr(self, 'total_maintenance_cost', 0) or 0
        self.total_operational_cost = round(fuel_cost + maint_cost, 2)
        
        # Revenue calculation (more realistic for fleet business)
        # Using $3.5 per km for trucks (typical freight rates)
        # This accounts for: base rate + fuel surcharge + accessorial charges
        max_cap = getattr(self, 'max_capacity', 0) or 0
        revenue_per_km = 3.5 if max_cap > 5000 else 2.8  # Trucks vs Vans
        self.total_revenue = round(total_dist * revenue_per_km, 2)
        
        # Vehicle ROI: (Revenue - (Maintenance + Fuel)) / Acquisition Cost × 100
        acq_cost = getattr(self, 'acquisition_cost', 0) or 0
        if acq_cost and acq_cost > 0:
            self.vehicle_roi = round(((self.total_revenue - self.total_operational_cost) / acq_cost) * 100, 2)
        else:
            self.vehicle_roi = 0.0
        
        # Cost per km: Total Operational Cost / Total Distance
        if total_dist and total_dist > 0:
            self.cost_per_km = round(self.total_operational_cost / total_dist, 2)
        else:
            self.cost_per_km = 0.0
    
    def action_mark_available(self):
        """Mark vehicle as available after maintenance"""
        if self.status != 'in_shop':
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "message": "Vehicle is not in shop",
                    "type": "warning"
                }
            }
        
        self.write({'status': 'available'})
        
        # Send notifications
        from backend.core.notification_helper import notify_dispatchers
        from sqlalchemy.orm import object_session
        
        db = object_session(self)
        if db:
            # Notify dispatchers that vehicle is available
            notify_dispatchers(
                db,
                title="Vehicle Back in Service",
                message=f"Vehicle {self.name} has completed maintenance and is now available for assignment.",
                notification_type="success",
                action_type="navigate",
                action_target=f"/models/fleet.vehicle/{self.id}"
            )
        
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "message": f"Vehicle '{self.name}' is now available for assignment",
                "type": "success",
                "refresh": True
            }
        }
    
    def action_retire(self):
        """Retire the vehicle"""
        if self.status == 'in_use':
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "message": "Cannot retire vehicle that is currently in use",
                    "type": "error"
                }
            }
        
        self.write({'status': 'retired', 'active': False})
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "message": f"Vehicle '{self.name}' has been retired",
                "type": "warning",
                "refresh": True
            }
        }

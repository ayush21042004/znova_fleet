from datetime import datetime, timedelta
from backend.core.znova_model import ZnovaModel
from backend.core import fields, api

class Driver(ZnovaModel):
    __tablename__ = "fleet_driver"
    _model_name_ = "fleet.driver"
    _name_field_ = "name"
    _description_ = "Fleet Driver"

    name = fields.Char(label="Driver Name", required=True, tracking=True, help="Full name of the driver")
    license_number = fields.Char(label="License Number", required=True, tracking=True,
                                 help="Driver's license identification number")
    license_expiry = fields.Date(label="License Expiry Date", required=True, tracking=True,
                                 help="License expiration date (blocks assignment if expired)")
    phone = fields.Char(label="Phone Number", tracking=True, help="Contact phone number")
    
    status = fields.Selection([
        ('on_duty', 'On Duty'),
        ('off_duty', 'Off Duty'),
        ('suspended', 'Suspended')
    ], label="Status", default='off_duty', tracking=True, readonly=True, options={
        'on_duty': {'label': 'On Duty', 'color': 'success'},
        'off_duty': {'label': 'Off Duty', 'color': 'info'},
        'suspended': {'label': 'Suspended', 'color': 'danger'}
    }, help="Current duty status (auto-updated by system)")
    
    safety_score = fields.Float(label="Safety Score", default=100.0, tracking=True,
                                help="Driver safety rating (0-100)")
    
    # Relationships
    trip_ids = fields.One2many("fleet.trip", "driver_id", label="Trips",
                              columns=["name", "vehicle_id", "origin", "destination", "distance", "status"],
                              show_label=False, readonly=True)
    
    # Computed fields
    total_trips = fields.Integer(label="Total Trips", compute="_compute_stats", store=False)
    completed_trips = fields.Integer(label="Completed Trips", compute="_compute_stats", store=False)
    completion_rate = fields.Float(label="Completion Rate (%)", compute="_compute_stats", store=False, help="Percentage of trips completed successfully")
    license_expired = fields.Boolean(label="License Expired", compute="_compute_license_status", store=False)
    
    active = fields.Boolean(label="Active", default=True, tracking=True)

    _role_permissions = {
        "fleet_manager": {"create": True, "read": True, "write": True, "delete": True},
        "dispatcher": {"create": False, "read": True, "write": False, "delete": False},
        "safety_officer": {"create": False, "read": True, "write": True, "delete": False},
        "financial_analyst": {"create": False, "read": False, "write": False, "delete": False}
    }

    _search_config = {
        "filters": [
            {
                "name": "on_duty",
                "label": "On Duty",
                "domain": "[('status', '=', 'on_duty')]"
            },
            {
                "name": "off_duty",
                "label": "Off Duty",
                "domain": "[('status', '=', 'off_duty')]"
            },
            {
                "name": "suspended",
                "label": "Suspended",
                "domain": "[('status', '=', 'suspended')]"
            },
            {
                "name": "active_only",
                "label": "Active Drivers",
                "domain": "[('active', '=', True)]"
            }
        ],
        "group_by": [
            {
                "name": "by_status",
                "label": "By Status",
                "field": "status"
            }
        ]
    }

    _ui_views = {
        "list": {
            "fields": ["name", "license_number", "license_expiry", "status", "safety_score", "active"]
        },
        "form": {
            "show_audit_log": True,
            "tabs": [
                {
                    "title": "General",
                    "groups": [
                        {
                            "title": "Driver Information",
                            "fields": ["name", "phone", "active"]
                        },
                        {
                            "title": "License Details",
                            "fields": ["license_number", "license_expiry", "license_expired"]
                        },
                        {
                            "title": "Performance",
                            "fields": ["safety_score", "total_trips", "completed_trips", "completion_rate"]
                        }
                    ]
                },
                {
                    "title": "Trips",
                    "fields": ["trip_ids"]
                }
            ],
            "header_buttons": [
                {
                    "name": "action_suspend",
                    "label": "Suspend Driver",
                    "type": "secondary",
                    "method": "action_suspend",
                    "invisible": "[('status', '=', 'suspended')]"
                },
                {
                    "name": "action_activate",
                    "label": "Activate Driver",
                    "type": "primary",
                    "method": "action_activate",
                    "invisible": "[('status', '!=', 'suspended')]"
                }
            ]
        }
    }

    @api.depends('trip_ids')
    def _compute_stats(self):
        """Compute basic statistics from related records"""
        # Handle None or empty trip_ids
        if not self.trip_ids:
            self.total_trips = 0
            self.completed_trips = 0
            self.completion_rate = 0.0
            return
            
        self.total_trips = len(self.trip_ids)
        
        # Count completed trips
        completed = [t for t in self.trip_ids if hasattr(t, 'status') and t.status == 'completed']
        self.completed_trips = len(completed)
        
        # Calculate completion rate
        if self.total_trips > 0:
            self.completion_rate = round((self.completed_trips / self.total_trips) * 100, 2)
        else:
            self.completion_rate = 0.0

    @api.depends('license_expiry')
    def _compute_license_status(self):
        """Compute license expiration status"""
        # Handle None or missing license_expiry
        if not self.license_expiry:
            self.license_expired = False
            return
            
        try:
            expiry_date = datetime.strptime(str(self.license_expiry), '%Y-%m-%d').date()
            self.license_expired = expiry_date < datetime.now().date()
        except (ValueError, AttributeError):
            self.license_expired = False

    def action_suspend(self):
        """Suspend the driver"""
        self.write({'status': 'suspended'})
        
        # Send notifications
        from backend.core.notification_helper import notify_fleet_managers, notify_safety_officers
        from sqlalchemy.orm import object_session
        
        db = object_session(self)
        if db:
            # Notify fleet managers and safety officers
            notify_fleet_managers(
                db,
                title="Driver Suspended",
                message=f"Driver {self.name} has been suspended and cannot be assigned to trips.",
                notification_type="danger",
                action_type="navigate",
                action_target=f"/models/fleet.driver/{self.id}"
            )
            
            notify_safety_officers(
                db,
                title="Driver Status Change",
                message=f"Driver {self.name} has been suspended. Review required.",
                notification_type="warning",
                action_type="navigate",
                action_target=f"/models/fleet.driver/{self.id}"
            )
        
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "message": f"Driver '{self.name}' has been suspended",
                "type": "warning",
                "refresh": True
            }
        }

    def action_activate(self):
        """Activate the driver"""
        if self.license_expired:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "message": "Cannot activate driver with expired license",
                    "type": "error"
                }
            }
        
        self.write({'status': 'off_duty'})
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "message": f"Driver '{self.name}' has been activated",
                "type": "success",
                "refresh": True
            }
        }

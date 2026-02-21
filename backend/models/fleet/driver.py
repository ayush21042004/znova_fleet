from datetime import datetime, timedelta
from backend.core.znova_model import ZnovaModel
from backend.core import fields, api

class Driver(ZnovaModel):
    __tablename__ = "fleet_driver"
    _model_name_ = "fleet.driver"
    _name_field_ = "name"
    _description_ = "Fleet Driver"

    name = fields.Char(label="Driver Name", required=True, tracking=True)
    license_number = fields.Char(label="License Number", required=True, tracking=True)
    license_expiry = fields.Date(label="License Expiry Date", required=True, tracking=True)
    phone = fields.Char(label="Phone Number", tracking=True)
    
    status = fields.Selection([
        ('on_duty', 'On Duty'),
        ('off_duty', 'Off Duty'),
        ('suspended', 'Suspended')
    ], label="Status", default='off_duty', tracking=True, options={
        'on_duty': {'label': 'On Duty', 'color': 'success'},
        'off_duty': {'label': 'Off Duty', 'color': 'info'},
        'suspended': {'label': 'Suspended', 'color': 'danger'}
    })
    
    safety_score = fields.Float(label="Safety Score", default=100.0, tracking=True)
    
    # Relationships
    trip_ids = fields.One2many("fleet.trip", "driver_id", label="Trips")
    
    # Computed fields
    total_trips = fields.Integer(label="Total Trips", compute="_compute_stats", store=False)
    license_expired = fields.Boolean(label="License Expired", compute="_compute_license_status", store=False)
    
    active = fields.Boolean(label="Active", default=True, tracking=True)

    _role_permissions = {
        "fleet_manager": {"create": True, "read": True, "write": True, "delete": True},
        "dispatcher": {"create": False, "read": True, "write": True, "delete": False},
        "safety_officer": {"create": False, "read": True, "write": True, "delete": False},
        "financial_analyst": {"create": False, "read": True, "write": False, "delete": False}
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
                            "fields": ["name", "phone", "status", "active"]
                        },
                        {
                            "title": "License Details",
                            "fields": ["license_number", "license_expiry", "license_expired"]
                        },
                        {
                            "title": "Performance",
                            "fields": ["safety_score", "total_trips"]
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
        self.total_trips = len(self.trip_ids) if self.trip_ids else 0

    @api.depends('license_expiry')
    def _compute_license_status(self):
        if self.license_expiry:
            self.license_expired = datetime.strptime(str(self.license_expiry), '%Y-%m-%d').date() < datetime.now().date()
        else:
            self.license_expired = False

    def action_suspend(self):
        """Suspend the driver"""
        self.write({'status': 'suspended'})
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

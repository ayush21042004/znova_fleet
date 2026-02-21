from datetime import datetime
from backend.core.znova_model import ZnovaModel
from backend.core import fields, api

class MaintenanceLog(ZnovaModel):
    __tablename__ = "fleet_maintenance_log"
    _model_name_ = "fleet.maintenance.log"
    _name_field_ = "name"
    _description_ = "Fleet Maintenance Log"

    name = fields.Char(label="Reference", required=True, tracking=True)
    vehicle_id = fields.Many2one("fleet.vehicle", label="Vehicle", required=True, tracking=True)
    
    service_type = fields.Selection([
        ('routine', 'Routine Maintenance'),
        ('repair', 'Repair'),
        ('inspection', 'Inspection'),
        ('tire_change', 'Tire Change'),
        ('oil_change', 'Oil Change'),
        ('other', 'Other')
    ], label="Service Type", required=True, tracking=True)
    
    service_date = fields.Date(label="Service Date", required=True, tracking=True)
    cost = fields.Float(label="Cost", required=True, tracking=True)
    odometer_reading = fields.Float(label="Odometer Reading (km)", tracking=True)
    
    description = fields.Text(label="Description")
    notes = fields.Text(label="Notes")

    _role_permissions = {
        "fleet_manager": {"create": True, "read": True, "write": True, "delete": True},
        "dispatcher": {"create": True, "read": True, "write": False, "delete": False},
        "safety_officer": {"create": True, "read": True, "write": True, "delete": False},
        "financial_analyst": {"create": False, "read": True, "write": False, "delete": False}
    }

    _search_config = {
        "filters": [
            {
                "name": "routine",
                "label": "Routine Maintenance",
                "domain": "[('service_type', '=', 'routine')]"
            },
            {
                "name": "repair",
                "label": "Repairs",
                "domain": "[('service_type', '=', 'repair')]"
            },
            {
                "name": "this_month",
                "label": "This Month",
                "domain": "[('service_date', '>=', datetime.now().replace(day=1))]"
            }
        ],
        "group_by": [
            {
                "name": "by_service_type",
                "label": "By Service Type",
                "field": "service_type"
            },
            {
                "name": "by_vehicle",
                "label": "By Vehicle",
                "field": "vehicle_id"
            }
        ]
    }

    _ui_views = {
        "list": {
            "fields": ["name", "vehicle_id", "service_type", "service_date", "cost"]
        },
        "form": {
            "show_audit_log": True,
            "groups": [
                {
                    "title": "Maintenance Information",
                    "fields": ["name", "vehicle_id", "service_type", "service_date"]
                },
                {
                    "title": "Details",
                    "fields": ["cost", "odometer_reading", "description", "notes"]
                }
            ]
        }
    }

    @api.model
    def default_get(cls, fields_list):
        res = super(MaintenanceLog, cls).default_get(fields_list)
        if 'name' in fields_list and not res.get('name'):
            res['name'] = f"MAINT-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        if 'service_date' in fields_list and not res.get('service_date'):
            res['service_date'] = datetime.now().date()
        return res

    @classmethod
    def create(cls, db, vals):
        """Override create to auto-update vehicle status"""
        record = super(MaintenanceLog, cls).create(db, vals)
        
        # If maintenance is logged, set vehicle to 'in_shop'
        if record.vehicle_id and record.service_type in ['repair', 'routine']:
            record.vehicle_id.write({'status': 'in_shop'})
        
        return record

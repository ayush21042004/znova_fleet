from datetime import datetime
from backend.core.znova_model import ZnovaModel
from backend.core import fields, api

class Expense(ZnovaModel):
    __tablename__ = "fleet_expense"
    _model_name_ = "fleet.expense"
    _name_field_ = "name"
    _description_ = "Fleet Expense"

    name = fields.Char(label="Reference", required=True, tracking=True)
    vehicle_id = fields.Many2one("fleet.vehicle", label="Vehicle", required=True, tracking=True,
                                 domain="[('active', '=', True)]",
                                 help="Select vehicle for expense tracking")
    
    expense_type = fields.Selection([
        ('fuel', 'Fuel'),
        ('toll', 'Toll'),
        ('parking', 'Parking'),
        ('other', 'Other')
    ], label="Expense Type", required=True, default='fuel', tracking=True)
    
    expense_date = fields.Date(label="Expense Date", required=True, tracking=True)
    cost = fields.Float(label="Cost ($)", required=True, tracking=True, help="Total cost of expense")
    
    # Fuel-specific fields - only visible/required when expense_type is 'fuel'
    fuel_liters = fields.Float(label="Fuel Quantity (Liters)", tracking=True,
                               invisible="[('expense_type', '!=', 'fuel')]",
                               required="[('expense_type', '=', 'fuel')]",
                               help="Required for fuel expenses")
    odometer_reading = fields.Float(label="Odometer Reading (km)", tracking=True,
                                    invisible="[('expense_type', '!=', 'fuel')]",
                                    help="Vehicle odometer at time of fueling")
    
    description = fields.Text(label="Description")
    notes = fields.Text(label="Notes")

    _role_permissions = {
        "fleet_manager": {"create": True, "read": True, "write": True, "delete": True},
        "dispatcher": {"create": False, "read": False, "write": False, "delete": False},
        "safety_officer": {"create": False, "read": False, "write": False, "delete": False},
        "financial_analyst": {"create": False, "read": True, "write": False, "delete": False}
    }

    _search_config = {
        "filters": [
            {
                "name": "fuel",
                "label": "Fuel Expenses",
                "domain": "[('expense_type', '=', 'fuel')]"
            },
            {
                "name": "toll",
                "label": "Toll Expenses",
                "domain": "[('expense_type', '=', 'toll')]"
            },
            {
                "name": "this_month",
                "label": "This Month",
                "domain": "[('expense_date', '>=', datetime.now().replace(day=1))]"
            }
        ],
        "group_by": [
            {
                "name": "by_expense_type",
                "label": "By Expense Type",
                "field": "expense_type"
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
            "fields": ["name", "vehicle_id", "expense_type", "expense_date", "cost", "fuel_liters"]
        },
        "form": {
            "show_audit_log": True,
            "groups": [
                {
                    "title": "Expense Information",
                    "fields": ["name", "vehicle_id", "expense_type", "expense_date", "cost"]
                },
                {
                    "title": "Fuel Details",
                    "fields": ["fuel_liters", "odometer_reading"],
                    "invisible": "[('expense_type', '!=', 'fuel')]"
                },
                {
                    "title": "Additional Information",
                    "fields": ["description", "notes"]
                }
            ]
        }
    }

    @api.model
    def default_get(cls, fields_list):
        res = super(Expense, cls).default_get(fields_list)
        if 'name' in fields_list and not res.get('name'):
            res['name'] = f"EXP-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        if 'expense_date' in fields_list and not res.get('expense_date'):
            res['expense_date'] = datetime.now().date()
        return res

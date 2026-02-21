from datetime import datetime
from backend.core.znova_model import ZnovaModel
from backend.core import fields, api
from backend.core.exceptions import ValidationError

class Trip(ZnovaModel):
    __tablename__ = "fleet_trip"
    _model_name_ = "fleet.trip"
    _name_field_ = "name"
    _description_ = "Fleet Trip"

    name = fields.Char(label="Trip Reference", required=True, tracking=True)
    vehicle_id = fields.Many2one("fleet.vehicle", label="Vehicle", required=True, tracking=True,
                                 domain="[('status', '=', 'available'), ('active', '=', True)]",
                                 help="Only available vehicles can be assigned")
    driver_id = fields.Many2one("fleet.driver", label="Driver", required=True, tracking=True,
                                domain="[('status', 'in', ['on_duty']), ('active', '=', True), ('license_expired', '=', False)]",
                                help="Only active drivers with valid licenses can be assigned")
    
    origin = fields.Char(label="Origin", required=True, tracking=True)
    destination = fields.Char(label="Destination", required=True, tracking=True)
    cargo_weight = fields.Float(label="Cargo Weight (kg)", required=True, tracking=True,
                                help="Must not exceed vehicle capacity")
    distance = fields.Float(label="Distance (km)", tracking=True, readonly="[('status', 'in', ['completed', 'cancelled'])]")
    
    status = fields.Selection([
        ('draft', 'Draft'),
        ('dispatched', 'Dispatched'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], label="Status", default='draft', tracking=True, readonly=True, options={
        'draft': {'label': 'Draft', 'color': 'info'},
        'dispatched': {'label': 'Dispatched', 'color': 'primary'},
        'in_progress': {'label': 'In Progress', 'color': 'warning'},
        'completed': {'label': 'Completed', 'color': 'success'},
        'cancelled': {'label': 'Cancelled', 'color': 'secondary'}
    })
    
    scheduled_date = fields.DateTime(label="Scheduled Date", tracking=True, readonly="[('status', 'in', ['completed', 'cancelled'])]")
    start_time = fields.DateTime(label="Started At", readonly=True)
    end_time = fields.DateTime(label="Completed At", readonly=True)
    
    notes = fields.Text(label="Notes")

    _role_permissions = {
        "fleet_manager": {"create": True, "read": True, "write": True, "delete": True},
        "dispatcher": {"create": True, "read": True, "write": True, "delete": False},
        "safety_officer": {"create": False, "read": True, "write": False, "delete": False},
        "financial_analyst": {"create": False, "read": False, "write": False, "delete": False}
    }

    _search_config = {
        "filters": [
            {
                "name": "draft",
                "label": "Draft Trips",
                "domain": "[('status', '=', 'draft')]"
            },
            {
                "name": "dispatched",
                "label": "Dispatched",
                "domain": "[('status', '=', 'dispatched')]"
            },
            {
                "name": "in_progress",
                "label": "In Progress",
                "domain": "[('status', '=', 'in_progress')]"
            },
            {
                "name": "completed",
                "label": "Completed",
                "domain": "[('status', '=', 'completed')]"
            }
        ],
        "group_by": [
            {
                "name": "by_status",
                "label": "By Status",
                "field": "status"
            },
            {
                "name": "by_vehicle",
                "label": "By Vehicle",
                "field": "vehicle_id"
            },
            {
                "name": "by_driver",
                "label": "By Driver",
                "field": "driver_id"
            }
        ]
    }

    _ui_views = {
        "list": {
            "fields": ["name", "vehicle_id", "driver_id", "origin", "destination", "cargo_weight", "distance", "status"]
        },
        "form": {
            "show_audit_log": True,
            "groups": [
                {
                    "title": "Trip Information",
                    "fields": ["name", "vehicle_id", "driver_id"]
                },
                {
                    "title": "Route Details",
                    "fields": ["origin", "destination", "cargo_weight", "distance"]
                },
                {
                    "title": "Schedule",
                    "fields": ["scheduled_date", "start_time", "end_time"]
                },
                {
                    "title": "Additional Information",
                    "fields": ["notes"]
                }
            ],
            "header_buttons": [
                {
                    "name": "action_dispatch",
                    "label": "Dispatch",
                    "type": "primary",
                    "method": "action_dispatch",
                    "invisible": "[('status', '!=', 'draft')]"
                },
                {
                    "name": "action_start",
                    "label": "Start Trip",
                    "type": "primary",
                    "method": "action_start",
                    "invisible": "[('status', '!=', 'dispatched')]"
                },
                {
                    "name": "action_complete",
                    "label": "Complete Trip",
                    "type": "success",
                    "method": "action_complete",
                    "invisible": "[('status', '!=', 'in_progress')]"
                },
                {
                    "name": "action_cancel",
                    "label": "Cancel Trip",
                    "type": "secondary",
                    "method": "action_cancel",
                    "invisible": "[('status', 'in', ['completed', 'cancelled'])]"
                }
            ]
        }
    }

    @api.model
    def default_get(cls, fields_list):
        res = super(Trip, cls).default_get(fields_list)
        if 'name' in fields_list and not res.get('name'):
            res['name'] = f"TRIP-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        return res

    def _validate_cargo_capacity(self):
        """Validate that cargo weight doesn't exceed vehicle capacity"""
        if self.vehicle_id and self.cargo_weight > self.vehicle_id.max_capacity:
            raise ValidationError(
                f"Cargo weight ({self.cargo_weight} kg) exceeds vehicle capacity ({self.vehicle_id.max_capacity} kg)"
            )

    def _validate_driver_license(self):
        """Validate that driver has valid license"""
        if not self.driver_id:
            return
        
        # Compute license status if not already computed
        if hasattr(self.driver_id, '_compute_license_status'):
            self.driver_id._compute_license_status()
        
        # Check if license is expired
        license_expired = getattr(self.driver_id, 'license_expired', False)
        if license_expired:
            raise ValidationError(
                f"Driver '{self.driver_id.name}' has an expired license"
            )
        
        if self.driver_id.status == 'suspended':
            raise ValidationError(
                f"Driver '{self.driver_id.name}' is suspended"
            )

    def action_dispatch(self):
        """Dispatch the trip"""
        self._validate_cargo_capacity()
        self._validate_driver_license()
        
        if self.vehicle_id.status != 'available':
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "message": f"Vehicle '{self.vehicle_id.name}' is not available",
                    "type": "error"
                }
            }
        
        self.write({'status': 'dispatched'})
        self.vehicle_id.write({'status': 'in_use'})
        self.driver_id.write({'status': 'on_duty'})
        
        # Send notifications
        from backend.core.notification_helper import notify_fleet_managers, notify_safety_officers
        from sqlalchemy.orm import object_session
        
        db = object_session(self)
        if db:
            # Notify fleet managers about dispatch
            notify_fleet_managers(
                db,
                title="Trip Dispatched",
                message=f"Trip {self.name} has been dispatched. Driver: {self.driver_id.name}, Vehicle: {self.vehicle_id.name}",
                notification_type="info",
                action_type="navigate",
                action_target=f"/models/fleet.trip/{self.id}"
            )
            
            # Notify safety officers for monitoring
            notify_safety_officers(
                db,
                title="New Trip Started",
                message=f"Driver {self.driver_id.name} started trip {self.name} ({self.origin} → {self.destination})",
                notification_type="info",
                action_type="navigate",
                action_target=f"/models/fleet.driver/{self.driver_id.id}"
            )
        
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "message": f"Trip '{self.name}' has been dispatched",
                "type": "success",
                "refresh": True
            }
        }

    def action_start(self):
        """Start the trip"""
        self.write({
            'status': 'in_progress',
            'start_time': datetime.now()
        })
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "message": f"Trip '{self.name}' is now in progress",
                "type": "success",
                "refresh": True
            }
        }

    def action_complete(self):
        """Complete the trip"""
        # Update vehicle odometer if distance is provided
        if self.distance and self.distance > 0:
            current_odometer = self.vehicle_id.odometer or 0
            new_odometer = current_odometer + self.distance
            self.vehicle_id.write({'odometer': new_odometer})
        
        self.write({
            'status': 'completed',
            'end_time': datetime.now()
        })
        self.vehicle_id.write({'status': 'available'})
        self.driver_id.write({'status': 'off_duty'})
        
        # Send notifications
        from backend.core.notification_helper import notify_fleet_managers, notify_dispatchers
        from sqlalchemy.orm import object_session
        
        db = object_session(self)
        if db:
            # Notify fleet managers and dispatchers
            notify_fleet_managers(
                db,
                title="Trip Completed",
                message=f"Trip {self.name} completed successfully. Distance: {self.distance} km. Vehicle {self.vehicle_id.name} is now available.",
                notification_type="success",
                action_type="navigate",
                action_target=f"/models/fleet.trip/{self.id}"
            )
            
            notify_dispatchers(
                db,
                title="Vehicle Available",
                message=f"Vehicle {self.vehicle_id.name} and Driver {self.driver_id.name} are now available for new assignments.",
                notification_type="info",
                action_type="navigate",
                action_target=f"/models/fleet.vehicle/{self.vehicle_id.id}"
            )
        
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "message": f"Trip '{self.name}' has been completed. Vehicle odometer updated.",
                "type": "success",
                "refresh": True
            }
        }

    def action_cancel(self):
        """Cancel the trip"""
        return {
            "type": "ir.actions.dialog",
            "dialog_type": "confirm",
            "title": "Cancel Trip",
            "message": f"Are you sure you want to cancel trip '{self.name}'?",
            "severity": "warning",
            "confirmText": "Yes, Cancel Trip",
            "cancelText": "No, Keep Trip",
            "on_confirm": {
                "method": "action_do_cancel",
                "params": {}
            }
        }

    def action_do_cancel(self):
        """Actually cancel the trip after confirmation"""
        if self.status in ['dispatched', 'in_progress']:
            self.vehicle_id.write({'status': 'available'})
            self.driver_id.write({'status': 'off_duty'})
        
        self.write({'status': 'cancelled'})
        
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "message": f"Trip '{self.name}' has been cancelled",
                "type": "warning",
                "refresh": True
            }
        }

"""
Notification Helper for FleetFlow
Provides utility functions to create notifications for fleet events
"""
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
import asyncio
import logging

logger = logging.getLogger(__name__)


def create_notification(
    db: Session,
    user_ids: List[int],
    title: str,
    message: str,
    notification_type: str = "info",
    action_type: Optional[str] = None,
    action_target: Optional[str] = None,
    action_params: Optional[dict] = None,
    expires_in_days: int = 7
):
    """
    Create notifications for multiple users
    
    Args:
        db: Database session
        user_ids: List of user IDs to notify
        title: Notification title
        message: Notification message
        notification_type: Type of notification (info, success, warning, danger)
        action_type: Type of action (navigate, modal, function)
        action_target: Target for the action (URL, component, function name)
        action_params: Parameters for the action
        expires_in_days: Number of days until notification expires
    """
    from backend.core.registry import registry
    from backend.core.websocket_manager import websocket_manager
    
    notification_model = registry.get_model('notification')
    if not notification_model:
        logger.warning("Notification model not found in registry")
        return
    
    expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
    
    for user_id in user_ids:
        try:
            # Create notification record
            notification = notification_model.create(db, {
                'title': title,
                'message': message,
                'type': notification_type,
                'user_id': user_id,
                'action_type': action_type,
                'action_target': action_target,
                'action_params': action_params,
                'expires_at': expires_at,
                'read': False
            })
            
            # Send via WebSocket for real-time delivery
            # We need to handle async in sync context
            try:
                # Get or create event loop
                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                # Create task for sending WebSocket message
                if loop.is_running():
                    # If loop is already running, create a task
                    asyncio.create_task(
                        websocket_manager.send_to_user(
                            user_id,
                            notification.to_websocket_message()
                        )
                    )
                else:
                    # If loop is not running, run until complete
                    loop.run_until_complete(
                        websocket_manager.send_to_user(
                            user_id,
                            notification.to_websocket_message()
                        )
                    )
                logger.info(f"Notification sent to user {user_id}: {title}")
            except Exception as e:
                # Log but don't fail if WebSocket fails
                logger.warning(f"Failed to send WebSocket notification to user {user_id}: {e}")
                # Notification is still saved in database, user will see it when they refresh
        
        except Exception as e:
            logger.error(f"Failed to create notification for user {user_id}: {e}")


def get_users_by_role(db: Session, role_name: str) -> List[int]:
    """Get all user IDs with a specific role"""
    from backend.core.registry import registry
    
    user_model = registry.get_model('user')
    role_model = registry.get_model('role')
    
    if not user_model or not role_model:
        return []
    
    try:
        # Find the role
        role = db.query(role_model).filter(role_model.name == role_name).first()
        if not role:
            logger.warning(f"Role '{role_name}' not found")
            return []
        
        # Find all users with this role
        users = db.query(user_model).filter(user_model.role_id == role.id).all()
        user_ids = [user.id for user in users]
        logger.info(f"Found {len(user_ids)} users with role '{role_name}'")
        return user_ids
    except Exception as e:
        logger.error(f"Error getting users by role '{role_name}': {e}")
        return []


def notify_fleet_managers(db: Session, title: str, message: str, **kwargs):
    """Send notification to all fleet managers"""
    user_ids = get_users_by_role(db, 'fleet_manager')
    if user_ids:
        create_notification(db, user_ids, title, message, **kwargs)


def notify_dispatchers(db: Session, title: str, message: str, **kwargs):
    """Send notification to all dispatchers"""
    user_ids = get_users_by_role(db, 'dispatcher')
    if user_ids:
        create_notification(db, user_ids, title, message, **kwargs)


def notify_safety_officers(db: Session, title: str, message: str, **kwargs):
    """Send notification to all safety officers"""
    user_ids = get_users_by_role(db, 'safety_officer')
    if user_ids:
        create_notification(db, user_ids, title, message, **kwargs)


def notify_financial_analysts(db: Session, title: str, message: str, **kwargs):
    """Send notification to all financial analysts"""
    user_ids = get_users_by_role(db, 'financial_analyst')
    if user_ids:
        create_notification(db, user_ids, title, message, **kwargs)

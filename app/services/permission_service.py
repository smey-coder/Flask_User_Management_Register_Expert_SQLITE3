from typing import List, Optional
from app.models.permission import Permission
from extensions import db

class PermissionService:
    @staticmethod
    def get_all() -> List[Permission]:
        return Permission.query.order_by(Permission.id.desc()).all()
    
    @staticmethod
    def get_by_id(permission_id: int) -> Optional[Permission]:
        return Permission.query.get(permission_id)
    
    @staticmethod
    def create(data: dict) -> Permission:
        permission = Permission(
            name=data["name"],
            description=data.get("description", ""),
        )
        db.session.add(permission)
        try:
            db.session.commit()
        except Exception as exc:
            import logging
            logging.getLogger("app").exception("Failed to create permission: %s", exc)
            db.session.rollback()
            raise
        return permission
    
    @staticmethod
    def update(permission: Permission, data: dict) -> Permission:
        permission.name = data["name"]
        permission.description = data.get("description", "")
        
        try:
            db.session.commit()
        except Exception as exc:
            import logging
            logging.getLogger("app").exception("Failed to update permission %s: %s", permission.id, exc)
            db.session.rollback()
            raise
        return permission
    
    @staticmethod
    def delete(permission: Permission) -> None:
        db.session.delete(permission)
        try:
            db.session.commit()
        except Exception as exc:
            import logging
            logging.getLogger("app").exception("Failed to delete permission: %s", exc)
            db.session.rollback()
            raise

from typing import List, Optional
from app.models.role import Role
from extensions import db
from sqlalchemy import select, desc

class RoleService:
    @staticmethod
    def get_all() -> List[Role]:
        return Role.query.order_by(Role.id.desc()).all()
    
    @staticmethod
    def get_by_id(role_id: int) -> Optional[Role]:
        return Role.query.get(role_id)
    
    @staticmethod
    def create(data: dict) -> Role:
        role = Role(
            name = data["name"],
            description = data["description"],
            
        )
        db.session.add(role)
        try:
            db.session.commit()
        except Exception as exc:
            import logging
            logging.getLogger("app").exception("Error creating role: %s", exc)
            db.session.rollback()
        return role
    
    @staticmethod
    def update(role: Role, data: dict) -> Role:
        role.name = data["name"]
        role.description = data["description"]
        
        try:
            db.session.commit()
            
        except Exception as exc:
            import logging
            logging.getLogger("app").exception("Error updating role: %s", exc)
            db.session.rollback()
        return role
    
    @staticmethod
    def delete(role: Role) -> None:
        db.session.delete(role)
        db.session.commit()
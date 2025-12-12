from typing import List, Optional
from app.models.role import RoleTable
from app.models.permission import PermissionTable
from extensions import db
from sqlalchemy import select, desc 
class RoleService:
    @staticmethod
    def get_role_all() -> List[RoleTable]:
        return RoleTable.query.order_by(RoleTable.id.desc()).all()
    
    @staticmethod
    def get_role_by_id(role_id: int) -> Optional[RoleTable]:
        return RoleTable.query.get(role_id)
    
    @staticmethod
    
    def create_role(
        data: dict, 
        permission_ids: Optional[List[int]] = None
    ) ->RoleTable:
        role = RoleTable(
            name= data["name"],
            description = data.get("description") or "",
        )
        
        if permission_ids:
            permissions = db.session.scalar(
                db.select(PermissionTable).filter(
                    PermissionTable.id.in_(permission_ids)
                )
            ).all()
            role.permissions = list(permissions)
            
        db.session.add(role)
        db.session.commit()
        return role
        # try:
        #     db.session.commit()
        # except Exception as exc:
        #     # Log and re-raise so caller can handle or app can show error
        #     import logging
        #     logging.getLogger("app").exception("Failed to create user: %s", exc)
        #     db.session.rollback()
        #     raise
        # return user
    
    @staticmethod
    def update_role(
        role: RoleTable, 
        data: dict, 
        permissions_ids: Optional[List[int]] = None
        ) -> RoleTable:
        
        role.name = data["name"],
        role.description = data.get("description") or ""
        
        
        if permissions_ids is not None:
            perms = List[PermissionTable] = []
            if permissions_ids:
                perms = db.session.scalar(
                    db.select(PermissionTable).filter(
                        PermissionTable.id.in_(permissions_ids)
                    )
                ).all()
                role.permissions = list(perms)
            db.session.commit()
            return role
            
        # try:
        #     db.session.commit()
        # except Exception as exc:
        #     import logging
        #     logging.getLogger("app").exception("Failed to update user %s: %s", user.id, exc)
        #     db.session.rollback()
        #     raise
        # return user
    
    @staticmethod
    def delete_role(role: RoleTable) -> None:
        db.session.delete(role)
        db.session.commit()
from datetime import datetime
from extensions import db
from app.models.associations import tbl_user_roles, tbl_role_permissions

# Define association tables inline to avoid circular imports
# user_roles = db.Table(
#     'user_roles',
#     db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
#     db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
# )

# role_permissions = db.Table(
#     'role_permissions',
#     db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
#     db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
# )

class RoleTable(db.Model):
    __tablename__ = "tbl_roles"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    users = db.relationship("User", secondary=tbl_user_roles, back_populates="roles")
    
    permissions = db.relationship("Permission", secondary=tbl_role_permissions, back_populates="roles")
    
    def has_premission(self, permission_name: str) -> bool:
        return any(permission.name == permission_name for permission in self.permissions)
    
    def __repr__(self) -> str:
        return f"<Role {self.name}>"

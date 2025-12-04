from datetime import datetime
from extensions import db
from app.models.association import user_roles, role_premissions

class Role(db.Model):
    __tablename__ = "roles"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    users = db.relationship("User", secondary=user_roles, back_populates="roles")
    permissions = db.relationship("Permission", secondary=role_premissions, back_populates="roles")
    
    def has_premission(self, permission_name: str) -> bool:
        return any(permission.name == permission_name for permission in self.permissions)
    
    def __repr__(self) -> str:
        return f"<Role {self.name}>"
from typing import List, Optional
from app.models.user import User
from extensions import db
from sqlalchemy import select, desc 
class UserService:
    @staticmethod
    def get_all() -> List[User]:
        return User.query.order_by(User.id.desc()).all()
    
    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        return User.query.get(user_id)
    
    @staticmethod
    
    def create(data: dict, password: str) -> User:
        user = User(
            username= data["username"],
            email = data["email"],
            full_name = data["full_name"],
            is_active= data.get("is_active", True),
        )
        user.set_password(password)
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as exc:
            # Log and re-raise so caller can handle or app can show error
            import logging
            logging.getLogger("app").exception("Failed to create user: %s", exc)
            db.session.rollback()
            raise
        return user
    
    @staticmethod
    def update(user: User, data: dict, password: Optional[str] = None) -> User:
        user.username = data["username"]
        user.email = data["email"]
        user.full_name = data["full_name"]
        user.is_active = data.get("is_active", True)
        
        if password:
            user.set_password(password)
            
        try:
            db.session.commit()
        except Exception as exc:
            import logging
            logging.getLogger("app").exception("Failed to update user %s: %s", user.id, exc)
            db.session.rollback()
            raise
        return user
    
    @staticmethod
    def delete(user: User) -> None:
        db.session.delete(user)
        db.session.commit()
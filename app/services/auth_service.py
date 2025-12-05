from typing import List, Optional
from app.models.user import User
from extensions import db
from sqlalchemy import select, desc

class AuthService:
    @staticmethod
    def authenticate(username: str, password: str) -> Optional[User]:
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None
class UserService:
    """Service layer for handling user creation and management (mock implementation)."""
    
    @staticmethod
    def create(data: dict, password: str) -> User:
        """Creates a new user instance and saves it to the database."""
        # This is a mock implementation for the registration route's usage.
        user = User(
            username=data['username'],
            email=data['email'],
            full_name=data['full_name'],
            is_active=data.get('is_active', True)
        )
        user.set_password(password)
        
        # db.session.add(user)
        # db.session.commit()
        
        return user
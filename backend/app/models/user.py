"""
User model for future authentication/multi-user support.
Currently not used, but structured for easy integration later.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


# Note: To enable multi-user support, you would:
# 1. Add a user_id foreign key to the Conversation model
# 2. Create authentication endpoints (login, register, etc.)
# 3. Add JWT token generation and verification
# 4. Protect endpoints with authentication dependencies
# 5. Filter conversations by user_id
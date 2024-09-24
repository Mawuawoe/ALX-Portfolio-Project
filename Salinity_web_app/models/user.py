#!/usr/bin/python3
"""
User model - Defines the User class based on the storage type (db or file-based).
"""
import os
import bcrypt
from flask_login import UserMixin
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

# Check the type of storage, use different model structure depending on the storage
if os.getenv('TYPE_OF_STORAGE') == 'db':
    class User(BaseModel, UserMixin, Base):
        """
        Defines a User (brine attendant) stored in the database.
        Forms the 'users' table.
        """
        __tablename__ = 'users'  # Table name in the database

        # Columns representing user details in the 'users' table
        first_name = Column(String(60), nullable=False)  # User's first name
        last_name = Column(String(60), nullable=False)   # User's last name
        username = Column(String(60), nullable=False)     # User's username
        email = Column(String(60), nullable=False, unique=True)  # Unique email per user
        password = Column(String(60), nullable=False)      # User's hashed password
        contact_info = Column(String(60), nullable=False)  # User's contact information

        # Relationship with the 'Salinity' table (a user has many salinities)
        salinities = relationship("Salinity", back_populates="user")

        def set_password(self, password):
            """Hashes the password and stores it."""
            self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        def check_password(self, password):
            """Checks a password against the stored hash."""
            return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

else:
    class User(BaseModel):
        """
        Defines a User for file-based storage.
        """
        # Attributes for file-based storage
        first_name = ""  # User's first name
        last_name = ""   # User's last name
        email = ""       # User's email
        password = ""    # User's password (not hashed)
        contact_info = ""  # User's contact information

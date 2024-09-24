#!/usr/bin/python3
"""
Salinity model - Defines the Salinity class based on the storage type (db or file-based).
"""
import os
from models.base_model import BaseModel, Base

# Check if storage type is set to 'db', then use SQLAlchemy for database storage
if os.getenv('TYPE_OF_STORAGE') == 'db':
    from sqlalchemy import Column, String, ForeignKey, Integer
    from sqlalchemy.orm import relationship
    
    class Salinity(BaseModel, Base):
        """
        Defines salinity measurements for a salt pan (database storage).
        Forms the 'salinities' table in the database.
        """
        __tablename__ = 'salinities'  # Table name in the database

        # Define columns in the 'salinities' table
        salinity_level = Column(Integer, nullable=False)  # Salinity level measured in the pan
        brine_level = Column(Integer, nullable=False)     # Brine level measured in the pan
        pan_id = Column(String(60), ForeignKey('pans.id'), nullable=False)  # Foreign key to 'pans' table
        brine_attendant_id = Column(String(60), ForeignKey('users.id'), nullable=False)  # Foreign key to 'users' table

        # Relationships to other models
        user = relationship("User", back_populates="salinities")  # Link to User model (brine attendant)
        pan = relationship("Pan", back_populates="salinities")    # Link to Pan model (salt pan)

# Define class for file-based storage if 'db' is not set
else:
    class Salinity(BaseModel):
        """
        Defines salinity measurements for file-based storage.
        """
        # Attributes for file-based storage
        salinity_level = 0   # Default salinity level
        brine_level = 0      # Default brine level
        comments = ""        # Optional comments
        pan_id = ""          # Identifier for the pan
        brine_attendant_id = ""  # Identifier for the brine attendant

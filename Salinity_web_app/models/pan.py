#!/usr/bin/python3
"""
Pan model - Defines the Pan class, representing a salt pan, reservoir, or PCR.
"""
import models
from models.base_model import BaseModel, Base
from models.salinity import Salinity  # Importing the Salinity model for relationship definition
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer
import os

# Check if storage type is set to 'db', then use SQLAlchemy for database storage
if os.getenv('TYPE_OF_STORAGE') == 'db':
    class Pan(BaseModel, Base):
        """
        Class representing a salt pan, reservoir, or PCR (database storage).
        Forms the 'pans' table in the database.
        """
        __tablename__ = 'pans'  # Define the table name when using DB storage
        
        # Columns in the 'pans' table
        location = Column(String(128), nullable=False)  # Location of the pan
        pan_id = Column(String(30), nullable=False)     # Unique identifier for the pan
        size = Column(Integer, nullable=False)          # Size of the pan
        pan_type = Column(String(30), nullable=False)   # Type of pan (e.g., salt pan, reservoir, PCR)

        # Relationship to Salinity model
        salinities = relationship("Salinity", back_populates="pan")  # One-to-many relationship (one pan has many salinity records)

# Define class for file-based storage if 'db' is not set
else:
    class Pan(BaseModel):
        """
        Class representing a salt pan, reservoir, or PCR (file-based storage).
        """
        # Attributes for file-based storage
        location = ""    # Location of the pan
        pan_id = ""      # Unique identifier for the pan
        size = ""        # Size of the pan
        pan_type = ""    # Type of pan (e.g., salt pan, reservoir, PCR)

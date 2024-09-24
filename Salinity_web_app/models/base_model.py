#!/usr/bin/python3
"""
Base model defining attributes and methods common to all classes.
"""
import uuid
from datetime import datetime
import models
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, DateTime

# SQLAlchemy Base class for database models
Base = declarative_base()

# Format for storing datetime strings
timefmt = "%Y-%m-%dT%H:%M:%S.%f"

class BaseModel:
    """
    Base model class that defines all common attributes/methods for other models.
    Serves as the foundation for other models, providing attributes like id, created_at, and updated_at.
    """
    __abstract__ = True  # Indicate that this class will not be mapped to any table

    # Define common attributes for all models when using database storage
    id = Column(String(60), primary_key=True, nullable=False)  # Unique identifier for each instance
    created_at = Column(DateTime, nullable=False, default=datetime.now)  # Timestamp when the instance is created
    updated_at = Column(DateTime, nullable=False, default=datetime.now)  # Timestamp when the instance is last updated
    
    def __init__(self, **kwargs):
        """
        Initialize the BaseModel instance with dynamic attributes.
        Attributes are set from kwargs, and defaults are provided where necessary.
        """
        self.id = str(uuid.uuid4())  # Generate a unique ID for the instance
        self.created_at = datetime.now()  # Set the creation time
        self.updated_at = datetime.now()  # Set the update time

        # Set attributes from kwargs (excluding the class name)
        for key, value in kwargs.items():
            if key != "__class__":
                setattr(self, key, value)

        # Handle created_at and updated_at if passed in kwargs as strings
        if "created_at" in kwargs and isinstance(kwargs["created_at"], str):
            self.created_at = datetime.strptime(kwargs["created_at"], timefmt)
        if "updated_at" in kwargs and isinstance(kwargs["updated_at"], str):
            self.updated_at = datetime.strptime(kwargs["updated_at"], timefmt)

        # Ensure ID is set if not provided in kwargs
        if kwargs.get("id", None) is None:
            self.id = str(uuid.uuid4())  # Generate a new unique ID

    def __str__(self):
        """
        String representation of the instance.
        Example: [ClassName] (id) {attributes}
        """
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """
        Update the updated_at timestamp and save the instance to storage.
        """
        self.updated_at = datetime.now()  # Update the 'updated_at' timestamp
        models.storage.new(self)  # Add the object to the storage
        models.storage.save()  # Save changes to the storage

    def to_dict(self):
        """
        Convert the instance into a dictionary representation, suitable for serialization.
        Includes datetime fields as strings and the class name.
        """
        new_dict = self.__dict__.copy()  # Create a copy of the instance's __dict__
        new_dict["created_at"] = self.created_at.strftime(timefmt)  # Format created_at as a string
        new_dict["updated_at"] = self.updated_at.strftime(timefmt)  # Format updated_at as a string
        new_dict["__class__"] = self.__class__.__name__  # Include the class name

        # Remove the SQLAlchemy instance state (not serializable)
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        return new_dict
    
    def delete(self):
        """
        Delete the current instance from storage.
        """
        models.storage.delete(self)  # Remove the object from storage

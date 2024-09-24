#!/usr/bin/python3
"""
MySQL storage module for the application.
This module manages storage using a MySQL database via SQLAlchemy ORM.
"""

import json
from models.base_model import BaseModel, Base
from models.user import User
from models.salinity import Salinity
from models.pan import Pan
from os import getenv
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import date

# Mapping class names to class objects for easier querying
classes = {
    "User": User,
    "Salinity": Salinity,
    "Pan": Pan,
}

class DBStorage:
    """
    Class responsible for interacting with the MySQL database using SQLAlchemy.
    It provides methods to store, query, and delete objects in the database.
    """

    __engine = None  # SQLAlchemy engine (connection to the database)
    __session = None  # SQLAlchemy session (used for database operations)

    def __init__(self):
        """Instantiate a DBStorage object and create a database engine."""
        MYSQL_USER = getenv('MYSQL_USER')
        MYSQL_PWD = getenv('MYSQL_PWD')
        MYSQL_HOST = getenv('MYSQL_HOST')
        MYSQL_DB = getenv('MYSQL_DB')
        TYPE_ENV = getenv('ENV')  # Check if the environment is 'test'
        
        # Create an engine to connect to the MySQL database
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_DB)
        )
        
        # Drop all tables if we are in the 'test' environment
        if TYPE_ENV == "test":
            Base.metadata.drop_all(self.__engine)
    
    def all(self, cls=None):
        """
        Query all objects from the database.
        If a class is specified, it returns only objects of that class.
        
        Args:
            cls (class): Optional class to filter the query results.
        
        Returns:
            dict: A dictionary where the key is <class-name>.<object-id> and the value is the object.
        """
        results_dict = {}
        for clss in classes:
            # If no class is specified or cls matches the class name
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()  # Query all objects of this class
                for obj in objs:
                    # Key format: <class-name>.<object-id>
                    key = obj.__class__.__name__ + '.' + obj.id
                    results_dict[key] = obj
        return results_dict

    def new(self, obj):
        """
        Add the object to the current database session.
        
        Args:
            obj (BaseModel): The object to add to the session.
        """
        self.__session.add(obj)
    
    def save(self):
        """
        Commit all changes in the current database session.
        This method ensures that changes are written to the database.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete an object from the current database session if it exists.
        
        Args:
            obj (BaseModel): The object to delete from the session.
        """
        if obj is not None:
            self.__session.delete(obj)
            self.__session.commit()

    def reload(self):
        """
        Create a new connection to the database and set up the session.
        This method also creates all tables defined in the models.
        """
        Base.metadata.create_all(self.__engine)  # Create tables if they don't exist
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)  # Session factory
        Session = scoped_session(sess_factory)  # Create a scoped session
        self.__session = Session  # Set the session for the storage

    def close(self):
        """
        Close the current session by calling the `remove()` method on the scoped session.
        This ensures the session is properly closed after each interaction.
        """
        self.__session.remove()

    def get_first_by(self, cls, **filters):
        """
        Query the first object that matches the provided filters.
        
        Args:
            cls (class): The class/table to query (e.g., User, Salinity, etc.).
            filters (dict): The filtering conditions (e.g., email="example@example.com").
        
        Returns:
            obj: The first object that matches the filtering conditions or None if no match is found.
        """
        if cls not in classes.values():
            return None  # If the provided class is not valid, return None
        
        # Perform the query with the provided filters
        return self.__session.query(cls).filter_by(**filters).first()

    def get_by_id(self, cls, id):
        """
        Retrieve an object by its primary key (ID).
        
        Args:
            cls (class): The class/table to query (e.g., User, Salinity, etc.).
            id (str or int): The primary key (ID) of the object to retrieve.
        
        Returns:
            obj: The object that matches the provided ID or None if no match is found.
        """
        if cls not in classes.values():
            return None  # If the provided class is not valid, return None
        
        # Retrieve the object by its primary key
        return self.__session.query(cls).get(id)

    def get_all_by_date(self, cls, filter_dates, records_list=None):
        """
        Query all objects of a given class filtered by the date field.
        
        Args:
            cls (class): The class/table to query (e.g., Salinity, Pan, etc.).
            filter_dates (date or list): A single date or a list of dates to filter records by.
            records_list (list): An optional list of records to filter further by date.
        
        Returns:
            list: A list of objects that match the filtering conditions.
        """
        if cls not in classes.values():
            return None

        # Filter the records based on the provided list of dates
        if isinstance(filter_dates, list):
            # If a list of records is passed, filter only within those records
            if records_list:
                filtered_records = [record for record in records_list if func.date(record.created_at) in filter_dates]
            else:
                filtered_records = self.__session.query(cls).filter(func.date(cls.created_at).in_(filter_dates)).all()
        else:
            # Single date filtering
            if records_list:
                filtered_records = [record for record in records_list if func.date(record.created_at) == filter_dates]
            else:
                filtered_records = self.__session.query(cls).filter(func.date(cls.created_at) == filter_dates).all()
    
        return filtered_records
    
    def get_all_salinity_by_pan(self, salinity_records=None, filter_field=None, value=None):
        """
        Filter Salinity records based on any field from the related Pan.

        Args:
            salinity_records (list): Optional list of Salinity objects to filter. If not provided, all Salinity records are queried.
            filter_field (str): The field name from the Pan table to filter Salinity records.
            value (any): The value of the field to filter by.

        Returns:
            list: A list of Salinity records where the related Pan has the given field and value.
        """
        if Salinity not in classes.values() or Pan not in classes.values():
            return None  # Ensure valid classes

        # If no salinity_records are provided, query all salinity records from the database
        if salinity_records is None:
            salinity_records = self.__session.query(Salinity).join(Pan).filter(getattr(Pan, filter_field) == value).all()
        else:
            # If a list of salinity_records is provided, filter it manually
            filtered_salinities = []
            for salinity in salinity_records:
                # Ensure the relationship name (e.g., 'pan') matches the definition in your model
                if getattr(salinity.pan, filter_field) == value:  # Ensure this attribute matches your model
                    filtered_salinities.append(salinity)
            salinity_records = filtered_salinities

        return salinity_records

    def get_latest_record(self, records_list):
        """
        Get the latest record from a list of records based on the 'created_at' field.

        Args:
            records_list (list): A list of records (e.g., Salinity, Pan, etc.).

        Returns:
            object: The latest record based on the 'created_at' field, or None if the list is empty.
        """
        if not records_list:
            return None  # Return None if the list is empty

        # Use the max() function with a lambda to get the latest record based on 'updated_at'
        latest_record = max(records_list, key=lambda record: getattr(record, 'updated_at'))
        
        return latest_record

#!/usr/bin/python3
"""
File storage module for our application.
This module handles serializing and deserializing objects to and from a JSON file for persistent storage.
"""

import json
from models.base_model import BaseModel
from models.user import User
from models.salinity import Salinity
from models.pan import Pan


class FileStorage:
    """
    Class responsible for storing and retrieving objects in a file system (JSON file).
    """

    # Path to the JSON file where objects will be stored
    __file_path = "file.json"

    # Dictionary to store all objects in memory before saving them to the file
    # The key will be in the format: <class name>.id (e.g., User.1234-5678)
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of all objects currently in storage.
        If a class `cls` is provided, it returns only the objects of that class.

        Args:
            cls (class): Optional class to filter the returned objects.
        
        Returns:
            dict: All objects or filtered objects by class.
        """
        if cls is None:
            return FileStorage.__objects  # Return all objects if no class is specified
        else:
            # Filter and return objects of the specified class
            filtered_objects = {}
            for key, value in FileStorage.__objects.items():
                if isinstance(value, cls):
                    filtered_objects[key] = value
            return filtered_objects

    def new(self, obj):
        """
        Adds a new object to the storage with the key <class_name>.id.

        Args:
            obj (BaseModel): The object to add to storage.
        """
        key = f"{obj.__class__.__name__}.{obj.id}"  # Create the key (e.g., User.1234-5678)
        FileStorage.__objects[key] = obj  # Store the object in the __objects dictionary

    def save(self):
        """
        Serializes the __objects dictionary to a JSON file.
        Converts objects to dictionaries before saving.
        """
        dict_to_save = {}
        for key, value in FileStorage.__objects.items():
            dict_to_save[key] = value.to_dict()  # Convert each object to its dictionary form
        # Write the serialized dictionary to the JSON file
        with open(FileStorage.__file_path, 'w') as json_file:
            json.dump(dict_to_save, json_file)

    def reload(self):
        """
        Deserializes the JSON file back into __objects.
        Reads from the JSON file, converts the JSON strings back into Python objects, 
        and stores them in the __objects dictionary.
        """
        try:
            # Open and load the JSON file
            with open(FileStorage.__file_path) as json_file2:
                dict_data = json.load(json_file2)
                for dict_obt in dict_data.values():
                    cls_name = dict_obt["__class__"]  # Get the class name
                    del dict_obt["__class__"]  # Remove the class name from the dict
                    # Recreate the object from the dictionary and add it to storage
                    self.new(eval(cls_name)(**dict_obt))
        except FileNotFoundError:
            # If the file doesn't exist, do nothing (no objects to load)
            pass

    def delete(self, obj=None):
        """
        Deletes an object from __objects if it exists.
        If obj is None, this method does nothing.

        Args:
            obj (BaseModel): The object to delete from storage.
        """
        if obj is None:
            return  # Do nothing if no object is provided
        # Find the key corresponding to the object
        key_to_delete = None
        for key, value in FileStorage.__objects.items():
            if value == obj:
                key_to_delete = key
                break
        # Delete the object if its key was found
        if key_to_delete:
            del FileStorage.__objects[key_to_delete]

    def close(self):
        """
        Method that calls reload() for deserializing the JSON file to objects.
        """
        self.reload()

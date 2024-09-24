#!/usr/bin/python3
import unittest
import sys
import os
import json

sys.path.append("../../")
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import BrineAttendant
from models.salinity import Salinity
from models.pan import Pan



class TestFileStorage(unittest.TestCase):
    """Test case for the FileStorage class"""

    def setUp(self):
        """Set up test environment"""

        self.storage = FileStorage()
        self.storage._FileStorage__objects = {}

        # Create instances for testing
        self.obj = BaseModel()
        self.brine_attendant = BrineAttendant()
        self.pan = Pan()

        # Add objects to storage
        self.storage.new(self.obj)
        self.storage.new(self.brine_attendant)
        self.storage.new(self.pan)

    def tearDown(self):
        """Tear down test environment"""
        if os.path.exists(self.storage._FileStorage__file_path):
            os.remove(self.storage._FileStorage__file_path)
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        """Test the all() method returns the __objects dict"""
        obj_dict = self.storage.all()
        self.assertIn(f"BaseModel.{self.obj.id}", obj_dict)
        self.assertEqual(obj_dict[f"BaseModel.{self.obj.id}"], self.obj)

    def test_new(self):
        """Test the new() method adds an object to __objects"""
        self.assertIn(f"BaseModel.{self.obj.id}", self.storage.all())

    def test_save(self):
        """Test the save() method serializes __objects to a file"""
        self.storage.save()
        self.assertTrue(os.path.exists(self.storage._FileStorage__file_path))

        with open(self.storage._FileStorage__file_path, 'r') as f:
            file_data = json.load(f)
        self.assertIn(f"BaseModel.{self.obj.id}", file_data)

    def test_reload(self):
        """Test the reload() method deserializes the JSON file to __objects"""
        self.storage.save()
        self.storage.reload()
        self.assertIn(f"BaseModel.{self.obj.id}", self.storage.all())

    def test_reload_empty_file(self):
        """Test reload on an empty or missing file does not crash"""
        self.storage.reload()  # File doesn't exist, should pass without error

    def test_save_and_reload(self):
        """Test saving and reloading objects"""
        # Save object to file
        self.storage.save()

        # Clear the storage and reload from file
        FileStorage._FileStorage__objects = {}
        self.storage.reload()

        # Ensure that the object was reloaded
        all_objs = self.storage.all()
        self.assertIn(f"BaseModel.{self.obj.id}", all_objs)

    def test_delete_existing_object(self):
        """Test that an existing object is deleted."""
        # Ensure object is in storage
        self.assertIn(f"BaseModel.{self.obj.id}", self.storage.all())
        
        # Delete the object
        self.storage.delete(self.obj)
        
        # Ensure object is no longer in storage
        self.assertNotIn(f"BaseModel.{self.obj}", self.storage.all())

    def test_all_no_class_filter(self):
        """Test that all() returns all objects when no class is provided."""
        all_objects = self.storage.all()
        
        # Check that all objects are returned
        self.assertEqual(len(all_objects), 3)
        self.assertIn(f"BaseModel.{self.obj.id}", all_objects)
        self.assertIn(f"BrineAttendant.{self.brine_attendant.id}", all_objects)
        self.assertIn(f"Pan.{self.pan.id}", all_objects)

    def test_all_with_class_filter(self):
        """Test that all() returns only objects of the provided class."""
        base_model_objects = self.storage.all(BrineAttendant)
        
        # Check that only BaseModel objects are returned
        self.assertEqual(len(base_model_objects), 1)
        self.assertIn(f"BrineAttendant.{self.brine_attendant.id}", base_model_objects)


if __name__ == "__main__":
    unittest.main()

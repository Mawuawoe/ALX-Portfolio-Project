#!/usr/bin/python3
"""
test for basemodel
"""
import unittest
import sys
sys.path.append('../')
from models.base_model import BaseModel, timefmt
from datetime import datetime




class TestBasemodel(unittest.TestCase):
    """
    testing the base_model

    """
    def setUp(self):
        """Set up for each test"""
        self.model = BaseModel()

    def test_instantiation(self):
        """
        
        """
        self.assertIs(type(self.model), BaseModel)
        self.model.name = 'Pan_1'
        self.model.location = 'Despa'
        attrs_types = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "name": str,
            "location": str
        }
        for key, value_type in attrs_types.items():
            with self.subTest(attr=key, expected_type=value_type):
                self.assertIn(key, self.model.__dict__)
                self.assertIs(type(self.model.__dict__[key]), value_type)
        self.assertEqual(self.model.name, "Pan_1")
        self.assertEqual(self.model.location, "Despa")
    
    def test_str(self):
        """Test the string representation of the BaseModel object"""
        expected_str = "[BaseModel] ({}) {}".format(self.model.id, self.model.__dict__)
        self.assertEqual(str(self.model), expected_str)

    def test_to_dict(self):
        """Test the to_dict method for proper key-value generation"""
        model_dict = self.model.to_dict()

        # Check if basic keys exist
        self.assertIn("id", model_dict)
        self.assertIn("created_at", model_dict)
        self.assertIn("updated_at", model_dict)
        self.assertIn("__class__", model_dict)
        
        # Check that created_at and updated_at are strings formatted correctly
        self.assertEqual(model_dict["created_at"], self.model.created_at.strftime(timefmt))
        self.assertEqual(model_dict["updated_at"], self.model.updated_at.strftime(timefmt))

    def test_save(self):
        created_time = self.model.updated_at
        self.model.save()
        new_updated_time = self.model.updated_at
        self.assertNotEqual(created_time, new_updated_time)
    
    def test_kwargs(self):
        my_model = BaseModel()
        my_model.name = "Pan_1"
        my_model.location = "Despa"
        dict_to_use = my_model.to_dict()
        new_model = BaseModel(**dict_to_use)
        self.assertEqual(type(new_model), BaseModel)
        self.assertEqual(new_model.name, "Pan_1")
        self.assertEqual(type(new_model.created_at), datetime)

    def tearDown(self):
        """Tear down after each test"""
        # Clean up any setup actions if needed (e.g., removing temporary data, resetting states)
        del self.model


#run test
if __name__ == '__main__':
    unittest.main()
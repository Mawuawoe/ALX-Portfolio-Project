#!/usr/bin/python3
"""
Unit tests for Pan class
"""
import unittest
import sys
sys.path.append('../')
from models.pan import Pan


class TestPan(unittest.TestCase):
    """Unit tests for Pan class"""

    def setUp(self):
        """Set up a Pan instance for testing"""
        self.pan = Pan()

    def test_instance_creation(self):
        """Test that an instance of Pan is created"""
        self.assertIsInstance(self.pan, Pan)

    def test_inheritance(self):
        """Test that Pan inherits from BaseModel"""
        from models.base_model import BaseModel
        self.assertIsInstance(self.pan, BaseModel)

    def test_initial_values(self):
        """Test that the initial values of Pan attributes are empty strings"""
        self.assertEqual(self.pan.location, "")
        self.assertEqual(self.pan.size, "")

    def test_attribute_assignment(self):
        """Test that attributes can be assigned values after creation"""
        self.pan.location = "Salt Valley"
        self.pan.size = "Large"
        
        self.assertEqual(self.pan.location, "Salt Valley")
        self.assertEqual(self.pan.size, "Large")


if __name__ == '__main__':
    unittest.main()

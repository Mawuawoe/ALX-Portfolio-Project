#!/usr/bin/python3
"""
Unit tests for Salinity class
"""
import unittest
import sys
sys.path.append('../')
from models.salinity import Salinity


class TestSalinity(unittest.TestCase):
    """Unit tests for the Salinity class"""

    def setUp(self):
        """Set up a Salinity instance for testing"""
        self.salinity = Salinity()

    def test_instance_creation(self):
        """Test that an instance of Salinity is created"""
        self.assertIsInstance(self.salinity, Salinity)

    def test_inheritance(self):
        """Test that Salinity inherits from BaseModel"""
        from models.base_model import BaseModel
        self.assertIsInstance(self.salinity, BaseModel)

    def test_initial_values(self):
        """Test that the initial values of Salinity attributes are correct"""
        self.assertEqual(self.salinity.salinity_level, 0)
        self.assertEqual(self.salinity.brine_level, 0)
        self.assertEqual(self.salinity.comments, "")
        self.assertEqual(self.salinity.pan_id, "")
        self.assertEqual(self.salinity.brine_attendant, "")

    def test_attribute_assignment(self):
        """Test that attributes can be assigned values after creation"""
        self.salinity.salinity_level = 3.5
        self.salinity.brine_level = 7.8
        self.salinity.comments = "High salinity detected"
        self.salinity.pan_id = "PAN123"
        self.salinity.brine_attendant = "Attendant01"
        
        self.assertEqual(self.salinity.salinity_level, 3.5)
        self.assertEqual(self.salinity.brine_level, 7.8)
        self.assertEqual(self.salinity.comments, "High salinity detected")
        self.assertEqual(self.salinity.pan_id, "PAN123")
        self.assertEqual(self.salinity.brine_attendant, "Attendant01")


if __name__ == '__main__':
    unittest.main()

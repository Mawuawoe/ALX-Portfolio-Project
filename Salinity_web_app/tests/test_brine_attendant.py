#!/usr/bin/python3
"""
Unit tests for User class
"""
import unittest
import sys
sys.path.append('../')
from models.user import User


class TestUser(unittest.TestCase):
    """Unit tests for User class"""

    def setUp(self):
        """Set up a User instance for testing"""
        self.attendant = User()

    def test_instance_creation(self):
        """Test that an instance of User is created"""
        self.assertIsInstance(self.attendant, User)

    def test_inheritance(self):
        """Test that User inherits from BaseModel"""
        from models.base_model import BaseModel
        self.assertIsInstance(self.attendant, BaseModel)

    def test_initial_values(self):
        """Test that the initial values of User attributes are empty strings"""
        self.assertEqual(self.attendant.first_name, "")
        self.assertEqual(self.attendant.last_name, "")
        self.assertEqual(self.attendant.email, "")
        self.assertEqual(self.attendant.password, "")
        self.assertEqual(self.attendant.contact_info, "")

    def test_attribute_assignment(self):
        """Test that attributes can be assigned values after creation"""
        self.attendant.first_name = "John"
        self.attendant.last_name = "Doe"
        self.attendant.email = "john.doe@example.com"
        self.attendant.password = "password123"
        self.attendant.contact_info = "555-1234"
        
        self.assertEqual(self.attendant.first_name, "John")
        self.assertEqual(self.attendant.last_name, "Doe")
        self.assertEqual(self.attendant.email, "john.doe@example.com")
        self.assertEqual(self.attendant.password, "password123")
        self.assertEqual(self.attendant.contact_info, "555-1234")


if __name__ == '__main__':
    unittest.main()

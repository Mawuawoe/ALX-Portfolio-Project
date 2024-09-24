#!/usr/bin/python3
import unittest

#code to be tested
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b

# test case class
class TestMathOperations(unittest.TestCase):

    def steUp(self):
        self.num1 = 10
        self.num2 = 5

    #test method
    def test_add(self):
         # Checks if 2 + 3 equals 5
        self.assertEqual(add(self.num1, self.num2), 15)
        self.assertEqual(add(-1, 1), 0)

    def test_divide(self):
        self.assertEqual(divide(6, 2), 3)
        self.assertRaises(ValueError, divide, 6, 0)
    
    def tearDown(self):
        pass

#run test
if __name__ == '__main__':
    unittest.main()

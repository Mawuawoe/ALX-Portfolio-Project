#!/usr/bin/python3
import json


# Reading from a JSON file (deserialization)
with open("data.json", 'r') as json_file:
    # This reads the file and converts it into a Python object
    data = json.load(json_file)

print(data)

# Converting JSON string back to Python object
json_str = '{"name": "Alice", "age": 30, "is_employee": true, "skills": ["Python", "SQL", "Machine Learning"]}'
data_from_string = json.loads(json_str)

print(data_from_string)

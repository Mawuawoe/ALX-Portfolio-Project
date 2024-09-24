#!/usr/bin/python3
import json

# Python object (dictionary)
data = {
    "name": "Alice",
    "age": 30,
    "is_employee": True,
    "skills": ["Python", "SQL", "Machine Learning"]
}

#write to a Json file(seralization)
with open('data.json', 'w') as json_file:
    # This writes the Python dictionary to a file in JSON format
    json.dump(data, json_file)

# Converting Python object to JSON string
json_str = json.dumps(data, indent=4)
print(json_str)

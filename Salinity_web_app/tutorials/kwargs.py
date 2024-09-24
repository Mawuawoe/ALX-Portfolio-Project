#!/usr/bin/python3
class MyClass:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

data = {"name": "Alice", "age": 30, "country": "USA"}

person = MyClass(**data)

print(person.name)

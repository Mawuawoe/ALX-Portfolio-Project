#!/usr/bin/python3
"""
Initialize the models package and create a unique storage instance for the application.
This file determines whether to use file-based storage or database storage based on the environment variable `TYPE_OF_STORAGE`.
"""

from os import getenv  # Import getenv to retrieve environment variables

# Check the value of the TYPE_OF_STORAGE environment variable
if getenv("TYPE_OF_STORAGE") == 'db':
    # If 'db' is set, use database storage (DBStorage)
    from models.engine.db_storage import DBStorage
    storage = DBStorage()  # Create a unique DBStorage instance
else:
    # Otherwise, default to file-based storage (FileStorage)
    from models.engine.file_storage import FileStorage
    storage = FileStorage()  # Create a unique FileStorage instance

# Call the reload method to load objects from storage
storage.reload()

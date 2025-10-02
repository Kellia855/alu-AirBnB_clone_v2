#!/usr/bin/python3
""" Initialize models package """
import os

# Determine storage type
HBNB_TYPE_STORAGE = os.getenv('HBNB_TYPE_STORAGE')

if HBNB_TYPE_STORAGE == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

# Always reload storage to load existing objects
storage.reload()


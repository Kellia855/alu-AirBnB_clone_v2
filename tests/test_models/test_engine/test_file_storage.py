import unittest
import os
from models.engine.file_storage import FileStorage
from models import storage
from models.base_model import BaseModel

class TestFileStorage(unittest.TestCase):

    def setUp(self):
        """Reset storage and remove file.json before each test"""
        storage._FileStorage__objects.clear()
        try:
            os.remove(storage._FileStorage__file_path)
        except FileNotFoundError:
             pass

    def tearDown(self):
        """Remove storage file after each test"""
        storage._FileStorage__objects.clear()
        try:
            os.remove(storage._FileStorage__file_path)
        except FileNotFoundError:
            pass

    def test_obj_list_empty(self):
        """__objects is initially empty"""
        self.assertEqual(len(storage.all()), 0)

    def test_new_object_added(self):
        """New object is correctly added"""
        new = BaseModel()
        key = f"BaseModel.{new.id}"
        self.assertIn(key, storage.all())
        self.assertIs(storage.all()[key], new)


    def test_all(self):
        """all() returns the dictionary of objects"""
        obj_dict = storage.all()
        self.assertIsInstance(obj_dict, dict)

    def test_base_model_instantiation(self):
        """File is not created on BaseModel instantiation"""
        new = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    def test_empty(self):
        """Data is saved to file after save"""
        new = BaseModel()
        data = new.to_dict()
        new.save()
        new2 = BaseModel(**data)
        self.assertNotEqual(os.path.getsize('file.json'), 0)

    def test_save(self):
        """FileStorage save method creates file"""
        new = BaseModel()
        storage.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_reload(self):
        """Storage file is successfully loaded to __objects"""
        new = BaseModel()
        storage.save()
        storage.reload()
        loaded_obj = None
        for obj in storage.all().values():
            loaded_obj = obj
        self.assertEqual(new.to_dict()['id'], loaded_obj.to_dict()['id'])

    def test_reload_empty(self):
        """Load from an empty file raises ValueError"""
        with open('file.json', 'w') as f:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_from_nonexistent(self):
        """Reload does nothing if file does not exist"""
        self.assertEqual(storage.reload(), None)

    def test_base_model_save(self):
        """BaseModel save method calls storage save"""
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_type_path(self):
        """Confirm __file_path is a string"""
        self.assertIsInstance(storage._FileStorage__file_path, str)

    def test_type_objects(self):
        """Confirm __objects is a dict"""
        self.assertIsInstance(storage.all(), dict)

    def test_key_format(self):
        """Key is properly formatted"""
        new = BaseModel()
        _id = new.to_dict()['id']
        for key in storage.all().keys():
            temp = key
        self.assertEqual(temp, f"BaseModel.{_id}")

    def test_storage_var_created(self):
        """FileStorage object storage exists"""
        self.assertIsInstance(storage, FileStorage)


if __name__ == "__main__":
    unittest.main()


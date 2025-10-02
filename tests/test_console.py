#!/usr/bin/python3
""" Console tests """
import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models import storage
from models.state import State
from models.place import Place


class TestConsoleCreate(unittest.TestCase):
    """Test creating objects via the HBNB console"""

    def setUp(self):
        """Reset storage before each test"""
        storage._FileStorage__objects = {}

    def tearDown(self):
        """Clean up storage after each test"""
        storage._FileStorage__objects = {}

    def test_create_state(self):
        """Test creating a State object with parameters"""
        console = HBNBCommand()
        with patch('sys.stdout', new=StringIO()) as f:
            console.onecmd('create State name="California"')
            new_id = f.getvalue().strip()

        state = storage.all()['State.' + new_id]
        self.assertIsInstance(state, State)
        self.assertEqual(state.name, "California")

    def test_create_place_with_multiple_params(self):
        """Test creating a Place with multiple parameters"""
        console = HBNBCommand()
        cmd = (
            'create Place city_id="0001" user_id="0001" name="My_little_house"'
            'number_rooms=4 number_bathrooms=2 max_guest=10 price_by_night=300'
            'latitude=37.773972 longitude=-122.431297'
            )
        with patch('sys.stdout', new=StringIO()) as f:
            console.onecmd(cmd)
            new_id = f.getvalue().strip()

        place = storage.all()['Place.' + new_id]
        self.assertIsInstance(place, Place)
        self.assertEqual(place.city_id, "0001")
        self.assertEqual(place.user_id, "0001")
        self.assertEqual(place.name, "My little house")
        self.assertEqual(place.number_rooms, 4)
        self.assertEqual(place.number_bathrooms, 2)
        self.assertEqual(place.max_guest, 10)
        self.assertEqual(place.price_by_night, 300)
        self.assertAlmostEqual(place.latitude, 37.773972)
        self.assertAlmostEqual(place.longitude, -122.431297)

    def test_invalid_class(self):
        """Test trying to create a non-existing class"""
        console = HBNBCommand()
        with patch('sys.stdout', new=StringIO()) as f:
            console.onecmd('create Foo name="Test"')
            output = f.getvalue().strip()
        self.assertEqual(output, "** class doesn't exist **")

    def test_missing_class_name(self):
        """Test create with no class name"""
        console = HBNBCommand()
        with patch('sys.stdout', new=StringIO()) as f:
            console.onecmd('create')
            output = f.getvalue().strip()
        self.assertEqual(output, "** class name missing **")


if __name__ == '__main__':
    unittest.main()

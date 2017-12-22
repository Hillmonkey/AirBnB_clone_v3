#!/usr/bin/python3
"""
Contains the TestPlaceDocs classes
"""

from datetime import datetime
import inspect
import models
from models.place import Place
from models.state import State
from models.city import City
from models.user import User
from models.base_model import BaseModel
from models.engine import db_storage
import os
import pep8
import unittest
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.orm.attributes import InstrumentedAttribute


class TestPlaceDocs(unittest.TestCase):
    """Tests to check the documentation and style of Place class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.place_f = inspect.getmembers(Place, inspect.isfunction)

    def test_pep8_conformance_place(self):
        """Test that models/place.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/place.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_place(self):
        """Test that tests/test_models/test_place.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_place.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_place_module_docstring(self):
        """Test for the place.py module docstring"""
        self.assertIsNot(models.place.__doc__, None,
                         "place.py needs a docstring")
        self.assertTrue(len(models.place.__doc__) >= 1,
                        "place.py needs a docstring")

    def test_place_class_docstring(self):
        """Test for the Place class docstring"""
        self.assertIsNot(Place.__doc__, None,
                         "Place class needs a docstring")
        self.assertTrue(len(Place.__doc__) >= 1,
                        "Place class needs a docstring")

    def test_place_func_docstrings(self):
        """Test for the presence of docstrings in Place methods"""
        for func in self.place_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestPlace(unittest.TestCase):
    def setUp(self):
        if (os.getenv('HBNB_TYPE_STORAGE') == 'db'):
            self.session = db_storage.DBStorage()
            self.session.reload()

        self.state = State(name="A State")
        self.city = City(name="A City", state_id=self.state.id)
        self.user = User(email="a@b.com", password="Password")
        self.place = Place(city_id=self.city.id, user_id=self.user.id,
                           name="", description="")
        if (os.getenv('HBNB_TYPE_STORAGE') == 'db'):
            self.session.new(self.state)
            self.session.new(self.city)
            self.session.new(self.user)
            self.session.new(self.place)
            self.session.save()

    """Test the Place class"""
    def test_is_subclass(self):
        """Test that Place is a subclass of BaseModel"""
        self.assertIsInstance(self.place, BaseModel)
        self.assertTrue(hasattr(self.place, "id"))
        self.assertTrue(hasattr(self.place, "created_at"))
        self.assertTrue(hasattr(self.place, "updated_at"))

    def test_city_id_attr(self):
        """Test Place has attr city_id, and it's an empty string"""
        self.assertTrue(hasattr(self.place, "city_id"))
        self.assertEqual(self.place.city_id, self.city.id)

    def test_user_id_attr(self):
        """Test Place has attr user_id, and it's an empty string"""
        self.assertTrue(hasattr(self.place, "user_id"))
        self.assertEqual(self.place.user_id, self.user.id)

    def test_name_attr(self):
        """Test Place has attr name, and it's an empty string"""
        self.assertTrue(hasattr(self.place, "name"))
        self.assertEqual(self.place.name, "")

    def test_description_attr(self):
        """Test Place has attr description, and it's an empty string"""
        self.assertTrue(hasattr(self.place, "description"))
        self.assertEqual(self.place.description, "")

    def test_number_rooms_attr(self):
        """Test Place has attr number_rooms, and it's an int == 0"""
        self.assertTrue(hasattr(self.place, "number_rooms"))
        self.assertEqual(type(self.place.number_rooms), int)
        self.assertEqual(self.place.number_rooms, 0)

    def test_number_bathrooms_attr(self):
        """Test Place has attr number_bathrooms, and it's an int == 0"""
        self.assertTrue(hasattr(self.place, "number_bathrooms"))
        self.assertEqual(type(self.place.number_bathrooms), int)
        self.assertEqual(self.place.number_bathrooms, 0)

    def test_max_guest_attr(self):
        """Test Place has attr max_guest, and it's an int == 0"""
        self.assertTrue(hasattr(self.place, "max_guest"))
        self.assertEqual(type(self.place.max_guest), int)
        self.assertEqual(self.place.max_guest, 0)

    def test_price_by_night_attr(self):
        """Test Place has attr price_by_night, and it's an int == 0"""
        self.assertTrue(hasattr(self.place, "price_by_night"))
        self.assertEqual(type(self.place.price_by_night), int)
        self.assertEqual(self.place.price_by_night, 0)

    def test_latitude_attr(self):
        """Test Place has attr latitude, and it's a float == 0.0"""
        self.assertTrue(hasattr(self.place, "latitude"))
        self.assertEqual(type(self.place.latitude), float)
        self.assertEqual(self.place.latitude, 0.0)

    def test_latitude_attr(self):
        """Test Place has attr longitude, and it's a float == 0.0"""
        self.assertTrue(hasattr(self.place, "longitude"))
        self.assertEqual(type(self.place.longitude), float)
        self.assertEqual(self.place.longitude, 0.0)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Testing DBStorage")
    def test_amenity_ids_attr(self):
        """Test Place has attr amenity_ids, and it's an empty list"""
        self.assertTrue(hasattr(self.place, "amenity_ids"))
        self.assertEqual(type(self.place.amenity_ids), list)
        self.assertEqual(len(self.place.amenity_ids), 0)

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        new_d = self.place.to_dict()
        self.assertEqual(type(new_d), dict)
        for attr in self.place.__dict__:
            if not attr.startswith('_sa_'):
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        new_d = self.place.to_dict()
        self.assertEqual(new_d["__class__"], "Place")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"],
                         self.place.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"],
                         self.place.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        string = "[Place] ({}) {}".format(self.place.id, self.place.__dict__)
        self.assertEqual(string, str(self.place))

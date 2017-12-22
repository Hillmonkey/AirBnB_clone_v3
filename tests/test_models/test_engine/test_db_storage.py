#!/usr/bin/python3
"""module: dbstorage
testing methods for dbstorage"""


from models.engine import db_storage
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import json
import inspect
import os
import pep8
import unittest
import sqlalchemy

classes = {
    'Amenity': Amenity,
    'City': City,
    'Place': Place,
    'State': State,
    'Review': Review,
    'User': User
}
# TODO: use classes in test_new() and test_save()
# see test_file_storage.py for reference


class TestDbStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DbStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.db_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_db_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.db_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """class: TestDbStorage
    all tests to run on Database Storage"""

    def setUp(self):
        """method: setUp
        connect to database before running tests in this class"""
        self.session = db_storage.DBStorage()

    def tearDown(self):
        """method: tearDown
        shut down database connection"""
        self.session.close()

    def test_get(self):
        """method: test_get
        database copy of new object == copy via get"""
        new_obj = Amenity()
        print()
        print("++++++++++ db-test-get ++++++++++")
        print("new_obj = {}".format(new_obj))
        self.session.new(new_obj)
        output = self.session.get("Amenity", new_obj.id)
        print()
        print("++++ Larry test +++++++++++")
        print("type(self.session) = {}".format(type(self.session)))
        print("type(new_obj) = {}".format(type(new_obj)))
        self.assertEqual(5, 4)

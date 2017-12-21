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
import inspect
import json
import os
import pep8
import unittest
import sqlalchemy

DBStorage = db_storage.DBStorage
classes = {
    'Amenity': Amenity,
    'City': City,
    'Place': Place,
    'State': State,
    'Review': Review,
    'User': User
}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(DBStorage, inspect.isfunction)

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
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """class: TestDbStorage
    all tests to run on Database Storage"""

    def setUp(self):
        '''connect & reload the database'''
        self.storage = db_storage.DBStorage()
        # how come the reload() in models/__init__ doesn't take care of it?
        self.storage.reload()

    def tearDown(self):
        '''terminate database connection'''
        self.storage.close()

    def test_get(self):
        '''test that get returns object based on cls name & id
        database copy of new object == copy via get'''
        new_obj = State(name="Test get State")
        self.storage.new(new_obj)
        self.storage.save()
        output = self.storage.get("State", new_obj.id)
        self.assertIs(new_obj, output)

    def test_count(self):
        '''test that count returns the number of objects based on clsname,
        or number of all objects if cls=None'''
        new_obj = State(name="Test count State")
        self.storage.new(new_obj)
        self.storage.save()

        state_count = self.storage.count("State")
        print("state count returned by count():", state_count)
        state_num_query = self.storage._DBStorage__session.query(State).count()
#        print("type of:", type(storage._DBStorage__session))
#        print("state count returned by query:", state_count)
        self.assertEqual(state_count, state_num_query)

        all_count = self.storage.count()
#        print("all object count returned by count():", all_count)
        obj_num_query = 0
        for key, value in classes.items():
            obj_num_query += self.storage._DBStorage__session.query(
                value).count()
#        print("all object count returned by query:", obj_num_query)
        self.assertEqual(all_count, obj_num_query)

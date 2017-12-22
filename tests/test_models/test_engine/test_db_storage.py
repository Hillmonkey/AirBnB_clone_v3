#!/usr/bin/python3
"""module: dbstorage
testing methods for dbstorage"""


from models import storage
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
from os import getenv
import inspect
import json
import inspect
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


@unittest.skipIf(getenv('HBNB_TYPE_STORAGE') != 'db', "Testing FileStorage")
class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
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
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_db_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.db_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


@unittest.skipIf(getenv('HBNB_TYPE_STORAGE') != 'db', "Testing FileStorage")
class TestDBStorage(unittest.TestCase):
    """class: TestDbStorage
    all tests to run on Database Storage"""

    def setUp(self):
        """connect & reload the database"""
        pass

    def tearDown(self):
        '''terminate database connection'''
        pass

    def test_get(self):
        '''test that get returns object based on cls name & id
        database copy of new object == copy via get'''
        new_obj = State(name="Test get State")
        storage.new(new_obj)
        storage.save()
        output = storage.get("State", new_obj.id)
        self.assertIs(new_obj, output)
        # delete the data created for testing from DB
        storage.delete(new_obj)

    def test_count(self):
        '''test that count returns the number of objects based on clsname,
        or number of all objects if cls=None'''
        new_obj = State(name="Test count State")
        storage.new(new_obj)
        storage.save()

        state_count = storage.count("State")
        state_num_query = storage._DBStorage__session.query(State).count()
        self.assertEqual(state_count, state_num_query)

        all_count = storage.count()
        obj_num_query = 0
        for key, value in classes.items():
            obj_num_query += storage._DBStorage__session.query(
                value).count()
        self.assertEqual(all_count, obj_num_query)
        # delete the data created for testing from DB
        storage.delete(new_obj)

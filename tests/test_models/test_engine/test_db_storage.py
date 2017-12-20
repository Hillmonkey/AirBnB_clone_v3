#!/usr/bin/python3
"""module: dbstorage
testing methods for dbstorage"""


#from models.engine import DBStorage
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
import os
import pep8
import unittest
import sqlalchemy

name2class = {
    'Amenity': Amenity,
    'City': City,
    'Place': Place,
    'State': State,
    'Review': Review,
    'User': User
}


class TestDBFormatting(unittest.TestCase):
    """class: TestDBFormatting
    tests for pep8 compliance and existence of doc strings"""

    def TestPep8(self):
        """method: TestPep8
        tests for pep8 compliance of DBStorage"""
        pass

    def TestDocStrings(self):
        """method: TestDocStrings
        tests for existence of doc strings"""
        pass


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

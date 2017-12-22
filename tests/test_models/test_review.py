#!/usr/bin/python3
"""
Contains the TestReviewDocs classes
"""

from datetime import datetime
from models.engine import db_storage
import inspect
import models
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
import os
import pep8
import unittest


class TestReviewDocs(unittest.TestCase):
    """Tests to check the documentation and style of Review class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.review_f = inspect.getmembers(Review, inspect.isfunction)

    def test_pep8_conformance_review(self):
        """Test that models/review.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/review.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_review(self):
        """Test that tests/test_models/test_review.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_review.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_review_module_docstring(self):
        """Test for the review.py module docstring"""
        self.assertIsNot(models.review.__doc__, None,
                         "review.py needs a docstring")
        self.assertTrue(len(models.review.__doc__) >= 1,
                        "review.py needs a docstring")

    def test_review_class_docstring(self):
        """Test for the Review class docstring"""
        self.assertIsNot(Review.__doc__, None,
                         "Review class needs a docstring")
        self.assertTrue(len(Review.__doc__) >= 1,
                        "Review class needs a docstring")

    def test_review_func_docstrings(self):
        """Test for the presence of docstrings in Review methods"""
        for func in self.review_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestReview(unittest.TestCase):
    """Test the Review class"""
    def setUp(self):
        if (os.getenv('HBNB_TYPE_STORAGE') == 'db'):
            self.session = db_storage.DBStorage()
            self.session.reload()

        self.state = State(name="A State")
        self.city = City(name="A City", state_id=self.state.id)
        self.user = User(email="a@b.com", password="Password")
        self.place = Place(city_id=self.city.id, user_id=self.user.id,
                           name="", description="")
        self.review = Review(text="wonderful", place_id=self.place.id,
                             user_id=self.user.id)
        if (os.getenv('HBNB_TYPE_STORAGE') == 'db'):
            self.session.new(self.state)
            self.session.new(self.city)
            self.session.new(self.user)
            self.session.new(self.place)
            self.session.new(self.review)
            self.session.save()

    def test_is_subclass(self):
        """Test if Review is a subclass of BaseModel"""
        self.assertIsInstance(self.review, BaseModel)
        self.assertTrue(hasattr(self.review, "id"))
        self.assertTrue(hasattr(self.review, "created_at"))
        self.assertTrue(hasattr(self.review, "updated_at"))

    def test_place_id_attr(self):
        """Test Self.Review has attr place_id, and it's an empty string"""
        self.assertTrue(hasattr(self.review, "place_id"))
        self.assertTrue(self.review.place_id)

    def test_user_id_attr(self):
        """Test Review has attr user_id, and it's an empty string"""
        self.assertTrue(hasattr(self.review, "user_id"))
        self.assertTrue(self.review.user_id)

    def test_text_attr(self):
        """Test Review has attr text, and it's an empty string"""
        self.assertTrue(hasattr(self.review, "text"))
        self.assertTrue(self.review.text)

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        new_d = self.review.to_dict()
        self.assertEqual(type(new_d), dict)
        for attr in self.review.__dict__:
            self.assertTrue(attr in new_d)
            self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        new_d = self.review.to_dict()
        self.assertEqual(new_d["__class__"], "Review")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"],
                         self.review.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"],
                         self.review.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        string = "[Review] ({}) {}".format(
            self.review.id, self.review.__dict__)
        self.assertEqual(string, str(self.review))

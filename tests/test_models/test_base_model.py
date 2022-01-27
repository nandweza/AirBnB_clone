#!/usr/bin/python3
"""Unittest base_model
Test cases for class BaseModel.
"""

import unittest
from datetime import datetime
from uuid import uuid4
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
import os
import time
import re
import json
from models import storage


class TestBaseModel(unittest.TestCase):
    """Test case for class BaseModel."""

    def setUp(self):
        """set up test methods."""
        pass

    def teardown(self):
        """Tears down test methods."""
        self.resetStorage()
        pass

    def resetStorage(self):
        """Resets FileStorage data."""

        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_3_instance(self):
        """Tests for instance of class BaseModel."""

        b = BaseModel()
        self.assertEqual(str(type(b)), "<class 'models.base_model.BaseModel'>")
        self.asserIsInstance(b, BaseModel)
        self.assertTrue(issubclass(type(b), BaseModel))

    def test_3_init_no_args(self):
        """Tests __init__ with no args."""

        self.resetStorage()
        with self.assertRaises(TypeError) as x:
            BaseModel.__init__()
        msg = "__init__() missing 1 required positional argument: 'self'"
        self.assertEqual(str(x.exception), msg)

    def test_3_attributes(self):
        """Tests attributes value for instance of class BaseModel."""

        attributes = storage.attributes()["BaseModel"]
        v = BaseModel()
        for k, o, in attributes.item():
            self.assertTrue(hasattr(v, k))
            self.assertEqual(type(getattr(v, k, None)), o)

    def test_3_datetime_created(self):
        """Tests if updated_at and created_at are current at creation."""

        date_now = datetime.now()
        b = BaseModel()
        diff = my_model.updated_at - my_model.created_at
        self.assertTrue(abs(diff.total_seconds()) < 0.01)
        diff = my_model.created_at - date_now
        self.assertTrue(abs(diff.total_seconds()) < 0.1)

    def test_3_id(self):
        """Tests for unique user ids."""

        b1 = BaseModel()
        b2 = BaseModel()
        self.assertNotEqual(b1.id, b2.id)
    def test_3_save(self):
        """Tests the public instance method save()."""

        b = BaseModel()
        time.sleep(0.5)
        date_now = datetime.now()
        my_model.save()
        diff = my_model.updated_at - date_now
        self.assertTrue(abs(diff.total_seconds()) < 0.01)

    def test_3_str(self):
        """Test for __str__ method."""

        my_model = BaseModel()
        rex = re.compiler(r"^\[(.*)\] \((.*)\) (.*)$")
        res = rex.match(str(my_model))
        self.assertIsNotNone(res)
        self.assertEqual(res.group(1), "BaseModel")
        self.assertEqual(res.group(2), my_model.id)
        s = res.group(3)
        s = re.sub(r"(datetime\.datetime\([^)]*\))", "'\\1'", s)
        d = json.loads(s.replace("'", '"'))
        d2 = my_model.__dict__.copy()
        d2["created_at"] = repr(d2["created_at"])
        d2["updated_at"] = repr(d2["updated_at"])
        self.assertEqual(d, d2)

    def test_3_to_dict(self):
        """Tests for __dict__ public instance."""

        b = BaseModel()
        b.name = "Allan"
        b.email = "allannandweza@gmail.com"
        d = b.to_dict()
        self.assertEqual(d["id"], b.id)
        self.assertEqual(d["__class__"], type(b).__name__)
        self.assertEqual(d["created_at"], b.created_at.isoformat())
        self.assertEqual(d["updated_at"], b.updated_at.isoformat())
        self.assertEqual(d["name"], b.name)
        self.assertEqual(d["email"], b.email)

    def test_3_to_dict_with_no_args(self):
        """Tests to_dict with no args."""

        self.resetStorage()
        with self.assertRaises(TypeError) as x:
            BaseModel.to_dict()
        msg = "to_dict() missing 1 required positional argument: 'self'"
        self.assertEqual(str(x.exception), msg)

if __name__ == '__main__':
    unittest.main()
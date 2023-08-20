#!/usr/bin/python3
"""Define unittests for class BaseModel

Unittest classes:
    TestBaseModel_instantiation
    TestBaseModel_save
    TestBaseModel_to_dict
"""
import models
import unittest
import os
from datetime import datetime
from models.base_model import BaseModel
from time import sleep


class TestBaseModel_instantiation(unittest.TestCase):
    """Unittests for testing Instance of the class BaseModel"""
    def test_no_arguments_instantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_stored_instance_objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_public_string(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_unique_model_ids(self):
        model1 = BaseModel()
        model2 = BaseModel()
        self.assertNotEqual(model1.id, model2.id)

    def test_different_created_at(self):
        model1 = BaseModel()
        sleep(0.04)
        model2 = BaseModel()
        self.assertLess(model1.created_at, model2.created_at)

    def test_different_updated_at(self):
        model1 = BaseModel()
        sleep(0.05)
        model2 = BaseModel()
        self.assertLess(model1.updated_at, model2.updated_at)

    def test_strng_rep(self):
        d = datetime.today()
        repd = repr(d)
        model = BaseModel()
        model.id = "654321"
        model.created_at = model.updated_at = d
        modelstr = model.__str__()
        self.assertIn("[BaseModel] (654321)", modelstr)
        self.assertIn("'id': '654321'", modelstr)
        self.assertIn("'created_at': " + repd, modelstr)
        self.assertIn("'updated_at': " + repd, modelstr)

    def test_unused_arguments(self):
        model = BaseModel(None)
        self.assertNotIn(None, model.__dict__.values())

    def test_kwargs_instantiation(self):
        d = datetime.today()
        iso_d = d.isoformat()
        model = BaseModel(id="235", created_at=iso_d, updated_at=iso_d)
        self.assertEqual(model.id, "235")
        self.assertEqual(model.created_at, d)
        self.assertEqual(model.updated_at, d)

    def test_instantiation_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_args_and_kwargs_instantiation(self):
        d = datetime.today()
        iso_d = d.isoformat()
        model = BaseModel("14", id="235", created_at=iso_d, updated_at=iso_d)
        self.assertEqual(model.id, "235")
        self.assertEqual(model.created_at, d)
        self.assertEqual(model.updated_at, d)


class TestBaseModel_save(unittest.TestCase):
    """Unittest for testing save method in BaseModel class"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_save_one(self):
        model = BaseModel()
        sleep(0.04)
        initial_updated_at = model.updated_at
        model.save()
        self.assertLess(initial_updated_at, model.updated_at)

    def test_save_two(self):
        model = BaseModel()
        sleep(0.04)
        initial_updated_at = model.updated_at
        model.save()
        second_updated = model.updated_at
        self.assertLess(initial_updated_at, second_updated)
        sleep(0.04)
        model.save()
        self.assertLess(second_updated, model.updated_at)

    def test_save_with_arg(self):
        model = BaseModel()
        with self.assertRaises(TypeError):
            model.save(None)


class TestBaseModel_to_dict(unittest.TestCase):
    """Unittest for testing method to_dict in BaseModel"""

    def test_to_dict_type(self):
        model = BaseModel()
        self.assertTrue(dict, type(model.to_dict()))

    def test_to_dict_contains_keys(self):
        model = BaseModel()
        self.assertIn("id", model.to_dict())
        self.assertIn("created_at", model.to_dict())
        self.assertIn("updated_at", model.to_dict())
        self.assertIn("__class__", model.to_dict())

    def test_to_dict_contains_added_attr(self):
        model = BaseModel()
        model.age = "30"
        model.pet = "cat"
        self.assertIn("age", model.to_dict())
        self.assertIn("pet", model.to_dict())

    def test_to_dict_datetime_str(self):
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertEqual(str, type(model_dict["created_at"]))
        self.assertEqual(str, type(model_dict["updated_at"]))

    def test_to_dict_output(self):
        d = datetime.today()
        model = BaseModel()
        model.id = "654321"
        model.created_at = model.updated_at = d
        mydict = {
             'id': '654321',
             '__class__': 'BaseModel',
             'created_at': d.isoformat(),
             'updated_at': d.isoformat()
        }
        self.assertDictEqual(model.to_dict(), mydict)

    def test_contrast_to_dict(self):
        model = BaseModel()
        self.assertNotEqual(model.to_dict(), model.__dict__)

    def test_to_dict_with_arg(self):
        model = BaseModel()
        with self.assertRaises(TypeError):
            model.to_dict(None)


if __name__ == "__main__":
    unittest.main()

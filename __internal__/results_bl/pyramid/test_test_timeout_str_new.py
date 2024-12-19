import base64
import json
import unittest
from pyramid.testing import DummyRequest

class TestSerializeMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()

    def test_serialize_empty_dict(self):
        result = self._serialize({})
        expected = base64.b64encode(json.dumps({}).encode('utf-8'))
        self.assertEqual(result, expected)

    def test_serialize_empty_list(self):
        result = self._serialize([])
        expected = base64.b64encode(json.dumps([]).encode('utf-8'))
        self.assertEqual(result, expected)

    def test_serialize_string(self):
        result = self._serialize("test string")
        expected = base64.b64encode(json.dumps("test string").encode('utf-8'))
        self.assertEqual(result, expected)

    def test_serialize_integer(self):
        result = self._serialize(42)
        expected = base64.b64encode(json.dumps(42).encode('utf-8'))
        self.assertEqual(result, expected)

    def test_serialize_float(self):
        result = self._serialize(3.14)
        expected = base64.b64encode(json.dumps(3.14).encode('utf-8'))
        self.assertEqual(result, expected)

    def test_serialize_nested_structure(self):
        result = self._serialize({"key": [1, 2, 3], "another_key": {"sub_key": "value"}})
        expected = base64.b64encode(json.dumps({"key": [1, 2, 3], "another_key": {"sub_key": "value"}}).encode('utf-8'))
        self.assertEqual(result, expected)

    def test_serialize_boolean(self):
        result = self._serialize(True)
        expected = base64.b64encode(json.dumps(True).encode('utf-8'))
        self.assertEqual(result, expected)

    def test_serialize_none(self):
        result = self._serialize(None)
        expected = base64.b64encode(json.dumps(None).encode('utf-8'))
        self.assertEqual(result, expected)

    def _serialize(self, value):
        return base64.b64encode(json.dumps(value).encode('utf-8'))
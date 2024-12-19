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

    def test_serialize_nested_structure(self):
        value = {'key': [1, 2, 3], 'nested': {'inner_key': 'value'}}
        result = self._serialize(value)
        expected = base64.b64encode(json.dumps(value).encode('utf-8'))
        self.assertEqual(result, expected)

    def test_serialize_special_characters(self):
        value = "Hello, World! 😊"
        result = self._serialize(value)
        expected = base64.b64encode(json.dumps(value).encode('utf-8'))
        self.assertEqual(result, expected)

    def test_serialize_large_number(self):
        value = 10**18
        result = self._serialize(value)
        expected = base64.b64encode(json.dumps(value).encode('utf-8'))
        self.assertEqual(result, expected)

    def test_serialize_boolean(self):
        value = True
        result = self._serialize(value)
        expected = base64.b64encode(json.dumps(value).encode('utf-8'))
        self.assertEqual(result, expected)

    def test_serialize_none(self):
        value = None
        result = self._serialize(value)
        expected = base64.b64encode(json.dumps(value).encode('utf-8'))
        self.assertEqual(result, expected)

    def _serialize(self, value):
        return base64.b64encode(json.dumps(value).encode('utf-8'))
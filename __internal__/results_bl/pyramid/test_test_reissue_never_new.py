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
        result = self._serialize((1, 2, {'key': 'value', 'list': [1, 2, 3]}))
        expected = base64.b64encode(json.dumps((1, 2, {'key': 'value', 'list': [1, 2, 3]})).encode('utf-8'))
        self.assertEqual(result, expected)

    def test_serialize_non_serializable(self):
        with self.assertRaises(TypeError):
            self._serialize(set([1, 2, 3]))

    def test_serialize_large_data(self):
        large_data = {'key': 'value' * 1000}
        result = self._serialize(large_data)
        expected = base64.b64encode(json.dumps(large_data).encode('utf-8'))
        self.assertEqual(result, expected)

    def _serialize(self, value):
        return base64.b64encode(json.dumps(value).encode('utf-8'))
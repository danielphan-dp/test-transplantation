import base64
import json
import unittest
from pyramid import testing

class TestSerializeMethod(unittest.TestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        self.serializer = self._serialize

    def _serialize(self, value):
        return base64.b64encode(json.dumps(value).encode('utf-8'))

    def test_serialize_empty_dict(self):
        result = self.serializer({})
        expected = base64.b64encode(json.dumps({}).encode('utf-8'))
        self.assertEqual(result, expected)

    def test_serialize_empty_list(self):
        result = self.serializer([])
        expected = base64.b64encode(json.dumps([]).encode('utf-8'))
        self.assertEqual(result, expected)

    def test_serialize_string(self):
        result = self.serializer("test")
        expected = base64.b64encode(json.dumps("test").encode('utf-8'))
        self.assertEqual(result, expected)

    def test_serialize_integer(self):
        result = self.serializer(123)
        expected = base64.b64encode(json.dumps(123).encode('utf-8'))
        self.assertEqual(result, expected)

    def test_serialize_float(self):
        result = self.serializer(123.456)
        expected = base64.b64encode(json.dumps(123.456).encode('utf-8'))
        self.assertEqual(result, expected)

    def test_serialize_boolean(self):
        result_true = self.serializer(True)
        expected_true = base64.b64encode(json.dumps(True).encode('utf-8'))
        self.assertEqual(result_true, expected_true)

        result_false = self.serializer(False)
        expected_false = base64.b64encode(json.dumps(False).encode('utf-8'))
        self.assertEqual(result_false, expected_false)

    def test_serialize_nested_structure(self):
        result = self.serializer({"key": ["value1", "value2"]})
        expected = base64.b64encode(json.dumps({"key": ["value1", "value2"]}).encode('utf-8'))
        self.assertEqual(result, expected)

    def test_serialize_non_serializable(self):
        with self.assertRaises(TypeError):
            self.serializer(set([1, 2, 3]))
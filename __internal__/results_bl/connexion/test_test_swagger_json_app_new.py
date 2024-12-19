import unittest
from connexion import App

class TestGetMethod(unittest.TestCase):
    def setUp(self):
        self.app = App(__name__)
        self.client = self.app.test_client()

    def test_get_with_kwargs(self):
        response = self.client.get('/v1.0/test?key=value')
        self.assertEqual(response.json, {'name': 'get', 'key': 'value'})

    def test_get_without_kwargs(self):
        response = self.client.get('/v1.0/test')
        self.assertEqual(response.json, [{'name': 'get'}])

    def test_get_with_empty_kwargs(self):
        response = self.client.get('/v1.0/test?')
        self.assertEqual(response.json, [{'name': 'get'}])

    def test_get_with_multiple_kwargs(self):
        response = self.client.get('/v1.0/test?key1=value1&key2=value2')
        self.assertEqual(response.json, {'name': 'get', 'key1': 'value1', 'key2': 'value2'})

    def test_get_with_no_query_string(self):
        response = self.client.get('/v1.0/test')
        self.assertEqual(response.json, [{'name': 'get'}])
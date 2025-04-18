import unittest
from connexion import App

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.app = App(__name__)
        self.client = self.app.test_client()

    def test_get_with_kwargs(self):
        response = self.client.get('/v1.0/test_endpoint', query_string={'key': 'value'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'key': 'value', 'name': 'get'})

    def test_get_without_kwargs(self):
        response = self.client.get('/v1.0/test_endpoint')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{'name': 'get'}])

    def test_get_with_empty_kwargs(self):
        response = self.client.get('/v1.0/test_endpoint', query_string={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [{'name': 'get'}])

    def test_get_with_multiple_kwargs(self):
        response = self.client.get('/v1.0/test_endpoint', query_string={'key1': 'value1', 'key2': 'value2'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'key1': 'value1', 'key2': 'value2', 'name': 'get'})

if __name__ == '__main__':
    unittest.main()
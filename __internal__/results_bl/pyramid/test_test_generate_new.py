import unittest
from pyramid.urldispatch import Route

class TestRouteGenerate(unittest.TestCase):

    def setUp(self):
        self.route = Route('name', ':path')

    def test_generate_empty_path(self):
        self.assertEqual(self.route.generate({'path': ''}), '/')

    def test_generate_special_characters(self):
        self.assertEqual(self.route.generate({'path': 'abc@123'}), '/abc@123')

    def test_generate_numeric_path(self):
        self.assertEqual(self.route.generate({'path': '12345'}), '/12345')

    def test_generate_path_with_slash(self):
        self.assertEqual(self.route.generate({'path': 'abc/def'}), '/abc/def')

    def test_generate_path_with_query(self):
        self.assertEqual(self.route.generate({'path': 'abc?query=1'}), '/abc?query=1')

    def test_generate_invalid_key(self):
        with self.assertRaises(KeyError):
            self.route.generate({'invalid_key': 'value'})
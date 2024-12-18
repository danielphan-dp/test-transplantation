import unittest
from pyramid.urldispatch import Route

class TestRouteGenerate(unittest.TestCase):
    def setUp(self):
        self.route = Route('name', ':path')

    def test_generate_with_valid_path(self):
        self.assertEqual(self.route.generate({'path': 'abc'}), '/abc')

    def test_generate_with_empty_path(self):
        self.assertEqual(self.route.generate({'path': ''}), '/')

    def test_generate_with_special_characters(self):
        self.assertEqual(self.route.generate({'path': 'a/b/c'}), '/a/b/c')
        self.assertEqual(self.route.generate({'path': ':@&+$,'}), '/:@&+$,')

    def test_generate_with_multiple_parameters(self):
        self.assertEqual(self.route.generate({'path': 'abc', 'extra': 'data'}), '/abc')

    def test_generate_with_non_string_path(self):
        self.assertEqual(self.route.generate({'path': 123}), '/123')
        self.assertEqual(self.route.generate({'path': None}), '/None')

    def test_generate_with_whitespace(self):
        self.assertEqual(self.route.generate({'path': '   '}), '/   ')

    def test_generate_with_encoded_characters(self):
        self.assertEqual(self.route.generate({'path': 'La Peña'}), '/La%20Pe%C3%B1a')
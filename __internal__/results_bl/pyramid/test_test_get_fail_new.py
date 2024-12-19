import unittest
from pyramid.registry import Registry
from pyramid.registry import Introspectable

class TestGetMethod(unittest.TestCase):
    def setUp(self):
        self.registry = Registry()
        self.introspectable = Introspectable('test')

    def test_get_existing_cookie(self):
        self.registry.cookie = 'existing_cookie'
        self.assertEqual(self.registry.get('cookie'), 'existing_cookie')

    def test_get_non_existing_cookie(self):
        self.registry.cookie = None
        self.assertIsNone(self.registry.get('cookie'))

    def test_get_with_different_name(self):
        self.registry.cookie = 'another_cookie'
        self.assertEqual(self.registry.get('different_name'), 'another_cookie')

    def test_get_empty_cookie(self):
        self.registry.cookie = ''
        self.assertEqual(self.registry.get('cookie'), '')

    def test_get_none_name(self):
        self.registry.cookie = 'none_name_cookie'
        self.assertEqual(self.registry.get(None), 'none_name_cookie')
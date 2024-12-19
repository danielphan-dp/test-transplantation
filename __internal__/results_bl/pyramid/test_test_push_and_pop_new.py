import unittest
from pyramid.testing import DummyRequest
from pyramid.threadlocal import get_current_request

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.local = self._makeOne()

    def _makeOne(self):
        return DummyRequest()

    def test_get_without_cookie(self):
        self.assertIsNone(self.local.get('non_existent_cookie'))

    def test_get_with_cookie(self):
        self.local.cookies = {'test_cookie': 'test_value'}
        self.assertEqual(self.local.get('test_cookie'), 'test_value')

    def test_get_with_empty_cookie(self):
        self.local.cookies = {}
        self.assertIsNone(self.local.get('empty_cookie'))

    def test_get_with_none_name(self):
        with self.assertRaises(TypeError):
            self.local.get(None)

    def test_get_with_invalid_name_type(self):
        with self.assertRaises(TypeError):
            self.local.get(123)
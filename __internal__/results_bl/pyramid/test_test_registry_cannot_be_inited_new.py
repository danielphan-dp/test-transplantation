import unittest
from pyramid.threadlocal import manager
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.cookie = 'test_cookie'

    def test_get_method_returns_cookie(self):
        result = self.request.get('cookie')
        self.assertEqual(result, 'test_cookie')

    def test_get_method_with_nonexistent_name(self):
        result = self.request.get('nonexistent')
        self.assertIsNone(result)

    def test_get_method_with_empty_name(self):
        result = self.request.get('')
        self.assertIsNone(result)

    def test_get_method_with_none_name(self):
        result = self.request.get(None)
        self.assertIsNone(result)

    def test_get_method_does_not_modify_cookie(self):
        original_cookie = self.request.cookie
        self.request.get('cookie')
        self.assertEqual(self.request.cookie, original_cookie)

    def tearDown(self):
        manager.clear()
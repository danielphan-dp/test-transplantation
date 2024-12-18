import unittest
from pyramid.threadlocal import manager
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest(cookie={'foo': 'bar'})
        self.cookie_name = 'foo'
        self.expected_cookie_value = 'bar'

    def test_get_cookie_value(self):
        result = self.request.cookies.get(self.cookie_name)
        self.assertEqual(result, self.expected_cookie_value)

    def test_get_non_existent_cookie(self):
        result = self.request.cookies.get('non_existent')
        self.assertIsNone(result)

    def test_get_cookie_with_multiple_values(self):
        self.request.cookies = DummyCookies({'foo': 'one; foo=two'})
        result = self.request.cookies.getlist('foo')
        self.assertEqual(result, ['one', 'two'])

    def test_get_cookie_with_empty_value(self):
        self.request.cookies = DummyCookies({'empty': ''})
        result = self.request.cookies.get('empty')
        self.assertEqual(result, '')

    def tearDown(self):
        manager.clear()
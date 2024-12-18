import unittest
from pyramid.threadlocal import manager
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.cookies = {'test-cookie': 'test-value'}

    def test_get_existing_cookie(self):
        result = self.request.cookies.get('test-cookie')
        self.assertEqual(result, 'test-value')

    def test_get_non_existing_cookie(self):
        result = self.request.cookies.get('non-existing-cookie')
        self.assertIsNone(result)

    def test_get_cookie_with_special_characters(self):
        self.request.cookies = {'session-token': 'abc123'}
        result = self.request.cookies.get('session-token')
        self.assertEqual(result, 'abc123')

    def test_get_cookie_with_hyphen(self):
        self.request.cookies = {'session-token': 'xyz789'}
        result = self.request.cookies.get('session-token')
        self.assertEqual(result, 'xyz789')

    def test_get_cookie_after_modification(self):
        self.request.cookies['modified-cookie'] = 'new-value'
        result = self.request.cookies.get('modified-cookie')
        self.assertEqual(result, 'new-value')

    def tearDown(self):
        manager.clear()
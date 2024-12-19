import unittest
from pyramid.testing import DummyRequest
from pyramid.threadlocal import get_current_request

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.cookies = {'test_cookie': 'cookie_value'}
        self.manager = ThreadLocalManager()
        self.manager.push(self.request)

    def tearDown(self):
        self.manager.pop()

    def test_get_cookie_value(self):
        local = self._makeOne(lambda: '123')
        self.assertEqual(local.get('test_cookie'), 'cookie_value')

    def test_get_non_existent_cookie(self):
        local = self._makeOne(lambda: '123')
        self.assertIsNone(local.get('non_existent_cookie'))

    def test_get_with_empty_cookie(self):
        self.request.cookies = {}
        local = self._makeOne(lambda: '123')
        self.assertIsNone(local.get('test_cookie'))

    def test_get_with_none(self):
        local = self._makeOne(lambda: None)
        self.assertIsNone(local.get('test_cookie'))
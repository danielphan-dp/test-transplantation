import unittest
from pyramid.testing import DummyRequest
from pyramid.threadlocal import get_current_request

class TestThreadLocalManager(unittest.TestCase):

    def setUp(self):
        self.manager = self._makeOne()

    def _makeOne(self):
        return ThreadLocalManager()

    def test_get_cookie(self):
        self.manager.cookie = 'test_cookie'
        self.assertEqual(self.manager.get('cookie'), 'test_cookie')

    def test_get_non_existent_cookie(self):
        self.assertIsNone(self.manager.get('non_existent_cookie'))

    def test_get_empty_cookie(self):
        self.manager.cookie = ''
        self.assertEqual(self.manager.get('cookie'), '')

    def test_get_with_different_name(self):
        self.manager.cookie = 'another_cookie'
        self.assertEqual(self.manager.get('cookie'), 'another_cookie')

    def test_get_with_none(self):
        self.manager.cookie = None
        self.assertIsNone(self.manager.get('cookie'))
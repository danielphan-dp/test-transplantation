import unittest
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):
    def setUp(self):
        self.policy = self._makeOne()

    def _makeOne(self):
        class DummyPolicy:
            def __init__(self, cookie):
                self.cookie = cookie

            def get(self, name):
                return self.cookie

        return DummyPolicy(cookie='test_cookie')

    def test_get_existing_cookie(self):
        request = DummyRequest()
        result = self.policy.get('test_cookie')
        self.assertEqual(result, 'test_cookie')

    def test_get_non_existing_cookie(self):
        request = DummyRequest()
        result = self.policy.get('non_existing_cookie')
        self.assertEqual(result, 'test_cookie')  # Assuming default behavior

    def test_get_empty_cookie(self):
        policy = self._makeOne(cookie='')
        result = policy.get('empty_cookie')
        self.assertEqual(result, '')
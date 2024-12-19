import unittest
from pyramid.testing import DummyRequest

class TestCacheGetMethod(unittest.TestCase):

    def setUp(self):
        self.cache = self._makeOne()
        self.req = DummyRequest()

    def test_get_returns_no_value_when_not_set(self):
        self.assertIs(self.cache.get(self.req), self.cache.NO_VALUE)

    def test_get_returns_value_when_set(self):
        self.cache.set(self.req, 2)
        self.assertIs(self.cache.get(self.req), 2)

    def test_get_with_different_request(self):
        another_req = DummyRequest()
        self.cache.set(self.req, 3)
        self.assertIs(self.cache.get(another_req), self.cache.NO_VALUE)

    def test_get_after_clear(self):
        self.cache.set(self.req, 4)
        self.cache.clear()
        self.assertIs(self.cache.get(self.req), self.cache.NO_VALUE)

    def test_get_with_none_request(self):
        with self.assertRaises(TypeError):
            self.cache.get(None)

    def test_get_with_invalid_request_type(self):
        with self.assertRaises(TypeError):
            self.cache.get("invalid_request_type")
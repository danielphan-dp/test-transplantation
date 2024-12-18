import unittest
from pyramid.threadlocal import manager
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.cookie_value = 'test_cookie'
        self.obj = self.create_object_with_cookie(self.cookie_value)

    def create_object_with_cookie(self, cookie):
        class TestObject:
            def get(self, name):
                return cookie
        return TestObject()

    def test_get_cookie(self):
        result = self.obj.get('some_name')
        self.assertEqual(result, self.cookie_value)

    def test_get_cookie_with_different_name(self):
        result = self.obj.get('another_name')
        self.assertEqual(result, self.cookie_value)

    def test_get_cookie_with_none(self):
        result = self.obj.get(None)
        self.assertEqual(result, self.cookie_value)

    def test_get_cookie_with_empty_string(self):
        result = self.obj.get('')
        self.assertEqual(result, self.cookie_value)

    def test_it_with_request(self):
        self._callFUT(request=self.request)
        current = manager.get()
        self.assertEqual(current['request'], self.request)

    def _callFUT(self, request):
        manager.set({'request': request})
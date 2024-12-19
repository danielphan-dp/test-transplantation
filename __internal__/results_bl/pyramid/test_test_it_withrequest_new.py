import unittest
from pyramid.scripting import get_root
from pyramid.threadlocal import manager

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.registry = self._makeRegistry()
        self.app = DummyApp(registry=self.registry)
        self.request = DummyRequest({})
        self.root, self.closer = self._callFUT(self.app, self.request)

    def tearDown(self):
        self.closer()

    def test_get_cookie(self):
        cookie_value = self.root.get('cookie_name')
        self.assertEqual(cookie_value, self.root.cookie)

    def test_get_non_existent_cookie(self):
        cookie_value = self.root.get('non_existent_cookie')
        self.assertIsNone(cookie_value)

    def test_get_with_empty_name(self):
        cookie_value = self.root.get('')
        self.assertIsNone(cookie_value)

    def test_get_with_none_name(self):
        with self.assertRaises(TypeError):
            self.root.get(None)

    def test_get_after_closer_called(self):
        self.closer()
        with self.assertRaises(Exception):
            self.root.get('cookie_name')
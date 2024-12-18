import unittest
from pyramid.scripting import get_root
from pyramid.threadlocal import manager
from pyramid.exceptions import ConfigurationError
from pyramid.util import InstancePropertyHelper
from pyramid.scripting import prepare
from pyramid.threadlocal import manager
from http.cookies import SimpleCookie

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.registry = self._makeRegistry()
        self.app = DummyApp(registry=self.registry)
        self.request = DummyRequest({"Cookie": "foo=one; foo=two"})
        self.root, self.closer = get_root(self.app, self.request)

    def tearDown(self):
        self.closer()

    def test_get_cookie_value(self):
        cookie_value = self.request.cookies.get("foo")
        self.assertEqual(cookie_value, "one")

    def test_get_duplicate_cookie_key(self):
        cookie_list = self.request.cookies.getlist("foo")
        self.assertEqual(cookie_list, ["one", "two"])

    def test_get_nonexistent_cookie(self):
        nonexistent_cookie = self.request.cookies.get("bar")
        self.assertIsNone(nonexistent_cookie)

    def test_get_with_registry(self):
        pushed = manager.get()
        self.assertEqual(pushed['registry'], self.registry)
        self.assertEqual(pushed['request'], self.request)
        self.assertEqual(pushed['request'].registry, self.registry)

    def test_get_with_empty_cookie(self):
        empty_request = DummyRequest({"Cookie": ""})
        empty_root, empty_closer = get_root(self.app, empty_request)
        self.assertEqual(empty_request.cookies.get("foo"), None)
        empty_closer()

    def test_get_with_invalid_cookie_format(self):
        invalid_request = DummyRequest({"Cookie": "invalid_format"})
        invalid_root, invalid_closer = get_root(self.app, invalid_request)
        self.assertEqual(invalid_request.cookies.get("foo"), None)
        invalid_closer()
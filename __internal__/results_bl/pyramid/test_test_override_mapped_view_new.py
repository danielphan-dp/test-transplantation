import unittest
from pyramid.testing import DummyRequest
from pyramid.exceptions import ConfigurationError

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.cookie = 'test_cookie'
        self.view = self.get_view()

    def get_view(self):
        class View:
            def get(self, name):
                return self.cookie
        return View()

    def test_get_method_returns_cookie(self):
        result = self.view.get('some_name')
        self.assertEqual(result, self.cookie)

    def test_get_method_with_different_name(self):
        result = self.view.get('another_name')
        self.assertEqual(result, self.cookie)

    def test_get_method_with_empty_name(self):
        result = self.view.get('')
        self.assertEqual(result, self.cookie)

    def test_get_method_with_none_name(self):
        with self.assertRaises(TypeError):
            self.view.get(None)

    def test_get_method_with_unexpected_type(self):
        with self.assertRaises(TypeError):
            self.view.get(123)
import os
import unittest
from pyramid.interfaces import IStaticURLInfo
from pyramid.request import Request

class TestStaticPath(unittest.TestCase):
    def setUp(self):
        self.request = Request.blank('/')
        self.request.script_name = '/foo'
        self.info = DummyStaticURLInfo('abc')
        self.request.registry.registerUtility(self.info, IStaticURLInfo)

    def test_static_path_valid(self):
        result = self.request.static_path('static/foo.css')
        self.assertEqual(result, 'abc')
        self.assertEqual(
            self.info.args, ('tests:static/foo.css', self.request, {'_app_url': '/foo'})
        )

    def test_static_path_invalid(self):
        with self.assertRaises(ValueError):
            self.request.static_path('invalid/path.css')

    def test_static_path_with_additional_kw(self):
        result = self.request.static_path('static/foo.css', extra='value')
        self.assertEqual(result, 'abc')
        self.assertEqual(
            self.info.args, ('tests:static/foo.css', self.request, {'_app_url': '/foo', 'extra': 'value'})
        )

    def test_static_path_with_empty_path(self):
        result = self.request.static_path('')
        self.assertEqual(result, 'abc')
        self.assertEqual(
            self.info.args, ('tests:', self.request, {'_app_url': '/foo'})
        )

class DummyStaticURLInfo:
    def __init__(self, return_value):
        self.return_value = return_value
        self.args = None

    def generate(self, path, request, **kw):
        self.args = (path, request, kw)
        return self.return_value

if __name__ == '__main__':
    unittest.main()
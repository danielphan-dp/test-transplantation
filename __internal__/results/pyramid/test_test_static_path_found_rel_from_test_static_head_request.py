import os
import unittest
from pyramid.interfaces import IStaticURLInfo
from pyramid.testing import DummyRequest

class TestStaticPath(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.script_name = '/foo'
        self.info = DummyStaticURLInfo('abc')
        self.request.registry.registerUtility(self.info, IStaticURLInfo)

    def test_static_path_found_rel(self):
        result = self.request.static_path('static/foo.css')
        self.assertEqual(result, 'abc')
        self.assertEqual(
            self.info.args, ('tests:static/foo.css', self.request, {'_app_url': '/foo'})
        )

    def test_static_path_with_additional_kw(self):
        result = self.request.static_path('static/foo.css', extra='value')
        self.assertEqual(result, 'abc')
        self.assertEqual(
            self.info.args, ('tests:static/foo.css', self.request, {'_app_url': '/foo', 'extra': 'value'})
        )

    def test_static_path_not_found(self):
        self.request.registry.unregisterUtility(self.info, IStaticURLInfo)
        with self.assertRaises(ValueError):
            self.request.static_path('static/foo.css')

    def test_static_path_with_absolute_path(self):
        result = self.request.static_path('/absolute/path/to/static/foo.css')
        self.assertEqual(result, 'abc')
        self.assertEqual(
            self.info.args, ('/absolute/path/to/static/foo.css', self.request, {'_app_url': '/foo'})
        )

class DummyStaticURLInfo:
    def __init__(self, return_value):
        self.return_value = return_value
        self.args = None

    def __call__(self, path, request, **kw):
        self.args = (path, request, kw)
        return self.return_value
import os
import unittest
from pyramid.interfaces import IStaticURLInfo
from pyramid.testing import DummyRequest

class TestStaticPath(unittest.TestCase):

    def _makeOne(self):
        return DummyRequest()

    def test_static_path_with_valid_path(self):
        request = self._makeOne()
        request.script_name = '/foo'
        info = DummyStaticURLInfo('abc')
        request.registry.registerUtility(info, IStaticURLInfo)
        result = request.static_path('tests:static/foo.css')
        self.assertEqual(result, 'abc')
        self.assertEqual(info.args, ('tests:static/foo.css', request, {'_app_url': '/foo'}))

    def test_static_path_with_invalid_path(self):
        request = self._makeOne()
        request.script_name = '/foo'
        with self.assertRaises(ValueError):
            request.static_path('invalid:path')

    def test_static_path_with_empty_path(self):
        request = self._makeOne()
        request.script_name = '/foo'
        result = request.static_path('')
        self.assertEqual(result, 'static path')

    def test_static_path_with_additional_kwargs(self):
        request = self._makeOne()
        request.script_name = '/foo'
        info = DummyStaticURLInfo('abc')
        request.registry.registerUtility(info, IStaticURLInfo)
        result = request.static_path('tests:static/foo.css', extra='value')
        self.assertEqual(result, 'abc')
        self.assertEqual(info.args, ('tests:static/foo.css', request, {'_app_url': '/foo', 'extra': 'value'}))

    def test_static_path_with_absolute_path(self):
        request = self._makeOne()
        request.script_name = '/foo'
        info = DummyStaticURLInfo('abc')
        request.registry.registerUtility(info, IStaticURLInfo)
        result = request.static_path('/absolute/path/to/resource')
        self.assertEqual(result, 'abc')
        self.assertEqual(info.args, ('/absolute/path/to/resource', request, {'_app_url': '/foo'}))

class DummyStaticURLInfo:
    def __init__(self, return_value):
        self.return_value = return_value
        self.args = None

    def __call__(self, path, request, **kw):
        self.args = (path, request, kw)
        return self.return_value
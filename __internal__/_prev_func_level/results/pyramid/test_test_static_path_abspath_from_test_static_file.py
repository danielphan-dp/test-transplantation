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
        registry = request.registry
        registry.registerUtility(info, IStaticURLInfo)
        result = request.static_path('mypackage:static/foo.css')
        self.assertEqual(result, 'abc')
        self.assertEqual(info.args, ('mypackage:static/foo.css', request, {}))

    def test_static_path_with_empty_path(self):
        request = self._makeOne()
        with self.assertRaises(ValueError):
            request.static_path('')

    def test_static_path_with_nonexistent_path(self):
        request = self._makeOne()
        request.script_name = '/foo'
        info = DummyStaticURLInfo(None)
        registry = request.registry
        registry.registerUtility(info, IStaticURLInfo)
        with self.assertRaises(ValueError):
            request.static_path('nonexistent:path')

    def test_static_path_with_additional_kwargs(self):
        request = self._makeOne()
        request.script_name = '/foo'
        info = DummyStaticURLInfo('abc')
        registry = request.registry
        registry.registerUtility(info, IStaticURLInfo)
        result = request.static_path('mypackage:static/foo.css', _app_url='/foo')
        self.assertEqual(result, 'abc')
        self.assertEqual(info.args, ('mypackage:static/foo.css', request, {'_app_url': '/foo'}))

class DummyStaticURLInfo:
    def __init__(self, return_value):
        self.return_value = return_value
        self.args = None

    def __call__(self, path, request, **kw):
        self.args = (path, request, kw)
        return self.return_value
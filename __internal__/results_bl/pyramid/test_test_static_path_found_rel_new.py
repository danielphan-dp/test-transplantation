import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IStaticURLInfo

class TestStaticPath(unittest.TestCase):

    def _makeOne(self):
        return DummyRequest()

    def test_static_path_with_empty_path(self):
        request = self._makeOne()
        request.script_name = '/foo'
        info = DummyStaticURLInfo('abc')
        request.registry.registerUtility(info, IStaticURLInfo)
        result = request.static_path('')
        self.assertEqual(result, 'abc')
        self.assertEqual(info.args, ('tests:static/', request, {'_app_url': '/foo'}))

    def test_static_path_with_invalid_path(self):
        request = self._makeOne()
        request.script_name = '/foo'
        info = DummyStaticURLInfo('abc')
        request.registry.registerUtility(info, IStaticURLInfo)
        result = request.static_path('invalid/path.css')
        self.assertEqual(result, 'abc')
        self.assertEqual(info.args, ('tests:invalid/path.css', request, {'_app_url': '/foo'}))

    def test_static_path_with_additional_kwargs(self):
        request = self._makeOne()
        request.script_name = '/foo'
        info = DummyStaticURLInfo('abc')
        request.registry.registerUtility(info, IStaticURLInfo)
        result = request.static_path('static/foo.css', extra='value')
        self.assertEqual(result, 'abc')
        self.assertEqual(info.args, ('tests:static/foo.css', request, {'_app_url': '/foo', 'extra': 'value'}))

    def test_static_path_with_no_script_name(self):
        request = self._makeOne()
        info = DummyStaticURLInfo('abc')
        request.registry.registerUtility(info, IStaticURLInfo)
        result = request.static_path('static/foo.css')
        self.assertEqual(result, 'abc')
        self.assertEqual(info.args, ('tests:static/foo.css', request, {}))
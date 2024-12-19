import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IStaticURLInfo

class TestStaticPath(unittest.TestCase):

    def _makeOne(self):
        return DummyRequest()

    def test_static_path_empty(self):
        request = self._makeOne()
        request.script_name = '/foo'
        info = DummyStaticURLInfo('abc')
        request.registry.registerUtility(info, IStaticURLInfo)
        result = request.static_path('')
        self.assertEqual(result, 'abc')
        self.assertEqual(info.args, ('', request, {'_app_url': '/foo'}))

    def test_static_path_no_script_name(self):
        request = self._makeOne()
        info = DummyStaticURLInfo('xyz')
        request.registry.registerUtility(info, IStaticURLInfo)
        result = request.static_path('tests:static/bar.css')
        self.assertEqual(result, 'xyz')
        self.assertEqual(info.args, ('tests:static/bar.css', request, {}))

    def test_static_path_with_kwargs(self):
        request = self._makeOne()
        request.script_name = '/foo'
        info = DummyStaticURLInfo('def')
        request.registry.registerUtility(info, IStaticURLInfo)
        result = request.static_path('tests:static/baz.css', key='value')
        self.assertEqual(result, 'def')
        self.assertEqual(info.args, ('tests:static/baz.css', request, {'_app_url': '/foo', 'key': 'value'}))

    def test_static_path_invalid_path(self):
        request = self._makeOne()
        request.script_name = '/foo'
        info = DummyStaticURLInfo('invalid')
        request.registry.registerUtility(info, IStaticURLInfo)
        result = request.static_path('invalid:path')
        self.assertEqual(result, 'invalid')
        self.assertEqual(info.args, ('invalid:path', request, {'_app_url': '/foo'}))
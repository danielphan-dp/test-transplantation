import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IStaticURLInfo

class TestStaticPath(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.script_name = '/foo'
        self.info = DummyStaticURLInfo('abc')
        self.request.registry.registerUtility(self.info, IStaticURLInfo)

    def test_static_path_valid(self):
        result = self.request.static_path('static/foo.css')
        self.assertEqual(result, 'abc')
        self.assertEqual(
            self.info.args, ('tests:static/foo.css', self.request, {'_app_url': '/foo'})
        )

    def test_static_path_empty_string(self):
        result = self.request.static_path('')
        self.assertEqual(result, 'static path')
        self.assertEqual(self.info.args, ('tests:static/', self.request, {'_app_url': '/foo'}))

    def test_static_path_none(self):
        result = self.request.static_path(None)
        self.assertEqual(result, 'static path')
        self.assertEqual(self.info.args, ('tests:static/', self.request, {'_app_url': '/foo'}))

    def test_static_path_invalid_path(self):
        result = self.request.static_path('invalid/path/to/resource')
        self.assertEqual(result, 'abc')
        self.assertEqual(
            self.info.args, ('tests:invalid/path/to/resource', self.request, {'_app_url': '/foo'})
        )

    def test_static_path_with_additional_kwargs(self):
        result = self.request.static_path('static/foo.css', extra='value')
        self.assertEqual(result, 'abc')
        self.assertEqual(
            self.info.args, ('tests:static/foo.css', self.request, {'_app_url': '/foo', 'extra': 'value'})
        )
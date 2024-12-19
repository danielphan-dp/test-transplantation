import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IStaticURLInfo

class TestStaticURL(unittest.TestCase):

    def _makeOne(self, path='tests:static/foo.css', **kw):
        request = DummyRequest()
        request.path = path
        request.kw = kw
        return request

    def test_static_url_with_empty_path(self):
        request = self._makeOne('')
        result = request.static_url('')
        self.assertEqual(result, 'static url')

    def test_static_url_with_none_path(self):
        request = self._makeOne(None)
        result = request.static_url(None)
        self.assertEqual(result, 'static url')

    def test_static_url_with_query_params(self):
        request = self._makeOne('tests:static/foo.css', param1='value1', param2='value2')
        result = request.static_url('tests:static/foo.css', param1='value1', param2='value2')
        self.assertEqual(result, 'static url')

    def test_static_url_found_abs_no_registry_on_request(self):
        request = self._makeOne()
        registry = request.registry
        info = DummyStaticURLInfo('abc')
        registry.registerUtility(info, IStaticURLInfo)
        del request.registry
        result = request.static_url('tests:static/foo.css')
        self.assertEqual(result, 'abc')
        self.assertEqual(info.args, ('tests:static/foo.css', request, {}))

    def test_static_url_with_invalid_path(self):
        request = self._makeOne('invalid:path')
        result = request.static_url('invalid:path')
        self.assertEqual(result, 'static url')

    def test_static_url_with_special_characters(self):
        request = self._makeOne('tests:static/foo@#$.css')
        result = request.static_url('tests:static/foo@#$.css')
        self.assertEqual(result, 'static url')
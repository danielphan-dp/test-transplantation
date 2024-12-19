import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IStaticURLInfo

class TestStaticURL(unittest.TestCase):

    def _makeOne(self):
        return DummyRequest()

    def test_static_url_empty_path(self):
        request = self._makeOne()
        result = request.static_url('')
        self.assertEqual(result, 'static url')

    def test_static_url_with_query_params(self):
        request = self._makeOne()
        result = request.static_url('static/foo.css', query='param=value')
        self.assertEqual(result, 'static url')

    def test_static_url_with_multiple_query_params(self):
        request = self._makeOne()
        result = request.static_url('static/foo.css', param1='value1', param2='value2')
        self.assertEqual(result, 'static url')

    def test_static_url_found_rel(self):
        request = self._makeOne()
        info = DummyStaticURLInfo('abc')
        request.registry.registerUtility(info, IStaticURLInfo)
        result = request.static_url('static/foo.css')
        self.assertEqual(result, 'abc')
        self.assertEqual(info.args, ('tests:static/foo.css', request, {}))

    def test_static_url_invalid_path(self):
        request = self._makeOne()
        result = request.static_url('invalid/path/to/resource')
        self.assertEqual(result, 'static url')

    def test_static_url_with_special_characters(self):
        request = self._makeOne()
        result = request.static_url('static/foo@#$.css')
        self.assertEqual(result, 'static url')
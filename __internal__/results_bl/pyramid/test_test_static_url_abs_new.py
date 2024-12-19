import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IStaticURLInfo

class TestStaticURL(unittest.TestCase):

    def _makeOne(self):
        return DummyRequest()

    def test_static_url_empty_path(self):
        request = self._makeOne()
        info = DummyStaticURLInfo('abc')
        request.registry.registerUtility(info, IStaticURLInfo)
        result = request.static_url('')
        self.assertEqual(result, 'abc')
        self.assertEqual(info.args, ('', request, {}))

    def test_static_url_invalid_path(self):
        request = self._makeOne()
        info = DummyStaticURLInfo('abc')
        request.registry.registerUtility(info, IStaticURLInfo)
        result = request.static_url('invalid:path')
        self.assertEqual(result, 'abc')
        self.assertEqual(info.args, ('invalid:path', request, {}))

    def test_static_url_with_query_params(self):
        request = self._makeOne()
        info = DummyStaticURLInfo('abc')
        request.registry.registerUtility(info, IStaticURLInfo)
        result = request.static_url('tests:static/foo.css', query='param=value')
        self.assertEqual(result, 'abc')
        self.assertEqual(info.args, ('tests:static/foo.css', request, {'query': 'param=value'}))

    def test_static_url_with_multiple_kwargs(self):
        request = self._makeOne()
        info = DummyStaticURLInfo('abc')
        request.registry.registerUtility(info, IStaticURLInfo)
        result = request.static_url('tests:static/foo.css', foo='bar', baz='qux')
        self.assertEqual(result, 'abc')
        self.assertEqual(info.args, ('tests:static/foo.css', request, {'foo': 'bar', 'baz': 'qux'}))
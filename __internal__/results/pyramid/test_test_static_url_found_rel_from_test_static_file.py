import os
import unittest
from pyramid.interfaces import IStaticURLInfo
from pyramid.request import Request

class TestStaticURL(unittest.TestCase):
    def setUp(self):
        self.request = Request({})
        self.info = DummyStaticURLInfo('http://example.com/static')
        self.request.registry.registerUtility(self.info, IStaticURLInfo)

    def test_static_url_found_abs(self):
        result = self.request.static_url('/static/foo.css')
        self.assertEqual(result, 'http://example.com/static/foo.css')
        self.assertEqual(self.info.args, ('/static/foo.css', self.request, {}))

    def test_static_url_found_rel(self):
        result = self.request.static_url('static/foo.css')
        self.assertEqual(result, 'http://example.com/static/static/foo.css')
        self.assertEqual(self.info.args, ('static/foo.css', self.request, {}))

    def test_static_url_no_scheme(self):
        self.info = DummyStaticURLInfo('//subdomain.example.com/static')
        self.request.registry.registerUtility(self.info, IStaticURLInfo)
        result = self.request.static_url('static/foo.css')
        self.assertEqual(result, 'http://subdomain.example.com/static/static/foo.css')

    def test_static_url_invalid_path(self):
        with self.assertRaises(ValueError):
            self.request.static_url('invalid/path/to/resource')

    def test_static_url_with_query_params(self):
        result = self.request.static_url('static/foo.css', _query='id=123')
        self.assertEqual(result, 'http://example.com/static/static/foo.css?id=123')
        self.assertEqual(self.info.args, ('static/foo.css', self.request, {'_query': 'id=123'}))

class DummyStaticURLInfo:
    def __init__(self, base_url):
        self.base_url = base_url
        self.args = None

    def __call__(self, path, request, **kw):
        self.args = (path, request, kw)
        return os.path.join(self.base_url, path)
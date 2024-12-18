import os
import unittest
from pyramid.interfaces import IStaticURLInfo
from pyramid.request import Request

class TestStaticURL(unittest.TestCase):
    def setUp(self):
        self.request = Request({})
        self.registry = self.request.registry

    def test_static_url_found_with_registry(self):
        info = DummyStaticURLInfo('http://example.com/static')
        self.registry.registerUtility(info, IStaticURLInfo)
        result = self.request.static_url('tests:static/foo.css')
        self.assertEqual(result, 'http://example.com/static')
        self.assertEqual(info.args, ('tests:static/foo.css', self.request, {}))

    def test_static_url_not_found(self):
        with self.assertRaises(ValueError):
            self.request.static_url('nonexistent:path')

    def test_static_url_with_additional_params(self):
        info = DummyStaticURLInfo('http://example.com/static')
        self.registry.registerUtility(info, IStaticURLInfo)
        result = self.request.static_url('tests:static/foo.css', _app_url='/foo')
        self.assertEqual(result, 'http://example.com/static')
        self.assertEqual(info.args, ('tests:static/foo.css', self.request, {'_app_url': '/foo'}))

    def test_static_url_with_absolute_path(self):
        info = DummyStaticURLInfo('http://example.com/static')
        self.registry.registerUtility(info, IStaticURLInfo)
        abspath = os.path.abspath('tests/static/foo.css')
        result = self.request.static_url(abspath)
        self.assertEqual(result, 'http://example.com/static')
        self.assertEqual(info.args, (abspath, self.request, {}))

class DummyStaticURLInfo:
    def __init__(self, url):
        self.url = url
        self.args = None

    def generate(self, path, request, **kw):
        self.args = (path, request, kw)
        return self.url
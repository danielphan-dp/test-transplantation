import os
import unittest
from pyramid.config.views import StaticURLInfo
from pyramid.interfaces import IStaticURLInfo
from pyramid.request import Request

class TestStaticURL(unittest.TestCase):

    def setUp(self):
        self.info = StaticURLInfo()
        self.here = os.path.abspath(os.path.dirname(__file__))
        self.info.add(self.config, '//subdomain.example.com/static', self.here)
        self.request = self._makeOne({'wsgi.url_scheme': 'http'})
        registry = self.request.registry
        registry.registerUtility(self.info, IStaticURLInfo)

    def _makeOne(self, environ):
        return Request(environ)

    def test_static_url_with_http_scheme(self):
        abspath = os.path.join(self.here, 'test_url.py')
        result = self.request.static_url(abspath)
        self.assertEqual(result, 'http://subdomain.example.com/static/test_url.py')

    def test_static_url_with_https_scheme(self):
        self.request.environ['wsgi.url_scheme'] = 'https'
        abspath = os.path.join(self.here, 'test_url.py')
        result = self.request.static_url(abspath)
        self.assertEqual(result, 'https://subdomain.example.com/static/test_url.py')

    def test_static_url_with_invalid_path(self):
        abspath = os.path.join(self.here, 'non_existent_file.py')
        result = self.request.static_url(abspath)
        self.assertEqual(result, 'http://subdomain.example.com/static/non_existent_file.py')

    def test_static_url_with_empty_path(self):
        result = self.request.static_url('')
        self.assertEqual(result, 'http://subdomain.example.com/static/')

    def test_static_url_with_query_parameters(self):
        abspath = os.path.join(self.here, 'test_url.py')
        result = self.request.static_url(abspath, foo='bar')
        self.assertEqual(result, 'http://subdomain.example.com/static/test_url.py?foo=bar')
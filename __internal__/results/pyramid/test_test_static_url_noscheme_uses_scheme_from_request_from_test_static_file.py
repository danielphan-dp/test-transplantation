import os
import unittest
from pyramid.config.views import StaticURLInfo
from pyramid.interfaces import IStaticURLInfo
from pyramid.request import Request

class TestStaticURL(unittest.TestCase):

    def setUp(self):
        self.config = self._makeConfig()
        self.request = self._makeRequest()

    def _makeConfig(self):
        # Mock configuration setup
        return {}

    def _makeRequest(self, environ=None):
        if environ is None:
            environ = {}
        return Request(environ)

    def test_static_url_with_valid_path(self):
        info = StaticURLInfo()
        here = os.path.abspath(os.path.dirname(__file__))
        info.add(self.config, '//example.com/static', here)
        registry = self.request.registry
        registry.registerUtility(info, IStaticURLInfo)
        abspath = os.path.join(here, 'test_file.py')
        result = self.request.static_url(abspath)
        self.assertEqual(result, 'http://example.com/static/test_file.py')

    def test_static_url_with_invalid_path(self):
        info = StaticURLInfo()
        here = os.path.abspath(os.path.dirname(__file__))
        info.add(self.config, '//example.com/static', here)
        registry = self.request.registry
        registry.registerUtility(info, IStaticURLInfo)
        with self.assertRaises(ValueError):
            self.request.static_url('invalid_path.py')

    def test_static_url_with_custom_scheme(self):
        info = StaticURLInfo()
        here = os.path.abspath(os.path.dirname(__file__))
        info.add(self.config, '//example.com/static', here)
        self.request.environ['wsgi.url_scheme'] = 'ftp'
        registry = self.request.registry
        registry.registerUtility(info, IStaticURLInfo)
        abspath = os.path.join(here, 'test_file.py')
        result = self.request.static_url(abspath)
        self.assertEqual(result, 'ftp://example.com/static/test_file.py')

    def test_static_url_with_additional_query_params(self):
        info = StaticURLInfo()
        here = os.path.abspath(os.path.dirname(__file__))
        info.add(self.config, '//example.com/static', here)
        registry = self.request.registry
        registry.registerUtility(info, IStaticURLInfo)
        abspath = os.path.join(here, 'test_file.py')
        result = self.request.static_url(abspath, version='1.0', lang='en')
        self.assertIn('version=1.0', result)
        self.assertIn('lang=en', result)

    def test_static_url_with_relative_path(self):
        info = StaticURLInfo()
        here = os.path.abspath(os.path.dirname(__file__))
        info.add(self.config, '//example.com/static', here)
        registry = self.request.registry
        registry.registerUtility(info, IStaticURLInfo)
        abspath = 'relative/path/to/test_file.py'
        result = self.request.static_url(abspath)
        self.assertEqual(result, 'http://example.com/static/relative/path/to/test_file.py')
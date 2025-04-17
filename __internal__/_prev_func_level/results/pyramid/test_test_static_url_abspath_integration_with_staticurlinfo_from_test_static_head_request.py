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

    def test_static_url_with_query_params(self):
        info = StaticURLInfo()
        here = os.path.abspath(os.path.dirname(__file__))
        info.add(self.config, 'absstatic', here)
        self.request.registry.registerUtility(info, IStaticURLInfo)
        abspath = os.path.join(here, 'test_url.py')
        result = self.request.static_url(abspath, query='param=value')
        self.assertEqual(result, 'http://example.com:5432/absstatic/test_url.py?query=param=value')

    def test_static_url_with_invalid_path(self):
        info = StaticURLInfo()
        here = os.path.abspath(os.path.dirname(__file__))
        info.add(self.config, 'absstatic', here)
        self.request.registry.registerUtility(info, IStaticURLInfo)
        with self.assertRaises(ValueError):
            self.request.static_url('invalid_path.py')

    def test_static_url_with_no_scheme(self):
        info = StaticURLInfo()
        here = os.path.abspath(os.path.dirname(__file__))
        info.add(self.config, '//subdomain.example.com/static', here)
        self.request = self._makeRequest({'wsgi.url_scheme': 'http'})
        self.request.registry.registerUtility(info, IStaticURLInfo)
        abspath = os.path.join(here, 'test_url.py')
        result = self.request.static_url(abspath)
        self.assertEqual(result, 'http://subdomain.example.com/static/test_url.py')

    def test_static_url_with_empty_path(self):
        info = StaticURLInfo()
        here = os.path.abspath(os.path.dirname(__file__))
        info.add(self.config, 'absstatic', here)
        self.request.registry.registerUtility(info, IStaticURLInfo)
        result = self.request.static_url('')
        self.assertEqual(result, 'http://example.com:5432/absstatic/')

if __name__ == '__main__':
    unittest.main()
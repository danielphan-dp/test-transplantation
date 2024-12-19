import os
import unittest
from pyramid.config.views import StaticURLInfo
from pyramid.interfaces import IStaticURLInfo
from pyramid.testing import DummyRequest

class TestStaticURL(unittest.TestCase):

    def setUp(self):
        self.config = StaticURLInfo()
        self.here = os.path.abspath(os.path.dirname(__file__))
        self.config.add(self.config, 'absstatic', self.here)

    def _makeOne(self):
        request = DummyRequest()
        request.registry = self.config.registry
        return request

    def test_static_url_with_valid_path(self):
        request = self._makeOne()
        registry = request.registry
        registry.registerUtility(self.config, IStaticURLInfo)
        abspath = os.path.join(self.here, 'test_url.py')
        result = request.static_url(abspath)
        self.assertEqual(result, 'http://example.com:5432/absstatic/test_url.py')

    def test_static_url_with_nonexistent_file(self):
        request = self._makeOne()
        registry = request.registry
        registry.registerUtility(self.config, IStaticURLInfo)
        abspath = os.path.join(self.here, 'nonexistent_file.py')
        result = request.static_url(abspath)
        self.assertEqual(result, 'http://example.com:5432/absstatic/nonexistent_file.py')

    def test_static_url_with_empty_path(self):
        request = self._makeOne()
        registry = request.registry
        registry.registerUtility(self.config, IStaticURLInfo)
        result = request.static_url('')
        self.assertEqual(result, 'http://example.com:5432/absstatic/')

    def test_static_url_with_special_characters(self):
        request = self._makeOne()
        registry = request.registry
        registry.registerUtility(self.config, IStaticURLInfo)
        abspath = os.path.join(self.here, 'test file@.py')
        result = request.static_url(abspath)
        self.assertEqual(result, 'http://example.com:5432/absstatic/test%20file%40.py')

    def test_static_url_with_query_parameters(self):
        request = self._makeOne()
        registry = request.registry
        registry.registerUtility(self.config, IStaticURLInfo)
        abspath = os.path.join(self.here, 'test_url.py')
        result = request.static_url(abspath, _query='param=value')
        self.assertEqual(result, 'http://example.com:5432/absstatic/test_url.py?_query=param=value')
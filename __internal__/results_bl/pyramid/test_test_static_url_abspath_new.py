import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IStaticURLInfo
from pyramid.url import static_url

class TestStaticURL(unittest.TestCase):

    def _makeOne(self):
        return DummyRequest()

    def test_static_url_empty_path(self):
        request = self._makeOne()
        result = request.static_url('')
        self.assertEqual(result, 'static url')
    
    def test_static_url_none_path(self):
        request = self._makeOne()
        result = request.static_url(None)
        self.assertEqual(result, 'static url')

    def test_static_url_with_query_params(self):
        request = self._makeOne()
        abspath = 'static/foo.css'
        result = request.static_url(abspath, query='param=value')
        self.assertEqual(result, 'static url')

    def test_static_url_with_multiple_kwargs(self):
        request = self._makeOne()
        abspath = 'static/foo.css'
        result = request.static_url(abspath, param1='value1', param2='value2')
        self.assertEqual(result, 'static url')

    def test_static_url_with_special_characters(self):
        request = self._makeOne()
        abspath = 'static/foo@#$.css'
        result = request.static_url(abspath)
        self.assertEqual(result, 'static url')

    def test_static_url_with_long_path(self):
        request = self._makeOne()
        abspath = 'static/' + 'a' * 1000 + '.css'
        result = request.static_url(abspath)
        self.assertEqual(result, 'static url')
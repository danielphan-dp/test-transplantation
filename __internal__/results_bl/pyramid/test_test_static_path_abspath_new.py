import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IStaticURLInfo

class TestStaticPath(unittest.TestCase):

    def _makeOne(self):
        return DummyRequest()

    def test_static_path_empty_path(self):
        request = self._makeOne()
        result = request.static_path('')
        self.assertEqual(result, 'static path')

    def test_static_path_with_kwargs(self):
        request = self._makeOne()
        result = request.static_path('foo.css', key='value')
        self.assertEqual(result, 'static path')
        self.assertEqual(request.kw, {'key': 'value'})

    def test_static_path_with_special_characters(self):
        request = self._makeOne()
        result = request.static_path('foo@bar.css')
        self.assertEqual(result, 'static path')

    def test_static_path_with_none(self):
        request = self._makeOne()
        result = request.static_path(None)
        self.assertEqual(result, 'static path')

    def test_static_path_with_large_string(self):
        request = self._makeOne()
        large_path = 'a' * 1000 + '.css'
        result = request.static_path(large_path)
        self.assertEqual(result, 'static path')
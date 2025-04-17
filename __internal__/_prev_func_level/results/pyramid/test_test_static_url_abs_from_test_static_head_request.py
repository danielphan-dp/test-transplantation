import os
import unittest
from pyramid.interfaces import IStaticURLInfo
from pyramid.request import Request

class TestStaticURL(unittest.TestCase):

    def setUp(self):
        self.request = Request({})
        self.info = DummyStaticURLInfo('http://example.com/static')
        self.request.registry.registerUtility(self.info, IStaticURLInfo)

    def test_static_url_with_valid_path(self):
        result = self.request.static_url('tests:static/foo.css')
        self.assertEqual(result, 'http://example.com/static/tests:static/foo.css')
        self.assertEqual(self.info.args, ('tests:static/foo.css', self.request, {}))

    def test_static_url_with_invalid_path(self):
        with self.assertRaises(ValueError):
            self.request.static_url('invalid:path')

    def test_static_url_with_additional_kwargs(self):
        result = self.request.static_url('tests:static/foo.css', _app_url='/foo')
        self.assertEqual(result, 'http://example.com/static/tests:static/foo.css?_app_url=/foo')
        self.assertEqual(self.info.args, ('tests:static/foo.css', self.request, {'_app_url': '/foo'}))

    def test_static_url_with_empty_path(self):
        with self.assertRaises(ValueError):
            self.request.static_url('')

    def test_static_url_with_absolute_path(self):
        abs_path = os.path.abspath('tests/static/foo.css')
        result = self.request.static_url(abs_path)
        self.assertEqual(result, 'http://example.com/static/tests/static/foo.css')
        self.assertEqual(self.info.args, (abs_path, self.request, {}))
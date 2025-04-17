import os
import unittest
from pyramid.interfaces import IStaticURLInfo
from pyramid.testing import DummyRequest

class TestStaticURL(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.info = DummyStaticURLInfo('http://example.com/static')
        self.request.registry.registerUtility(self.info, IStaticURLInfo)

    def test_static_url_with_valid_path(self):
        abspath = os.path.join('static', 'foo.css')
        result = self.request.static_url(abspath)
        self.assertEqual(result, 'http://example.com/static/foo.css')
        self.assertEqual(self.info.args, (abspath, self.request, {}))

    def test_static_url_with_invalid_path(self):
        with self.assertRaises(ValueError):
            self.request.static_url('invalid_path')

    def test_static_url_with_additional_kwargs(self):
        abspath = os.path.join('static', 'foo.css')
        result = self.request.static_url(abspath, cache='max-age=3600')
        self.assertEqual(result, 'http://example.com/static/foo.css')
        self.assertEqual(self.info.args, (abspath, self.request, {'cache': 'max-age=3600'}))

    def test_static_url_with_absolute_path(self):
        abspath = os.path.abspath('static/foo.css')
        result = self.request.static_url(abspath)
        self.assertEqual(result, 'http://example.com/static/foo.css')
        self.assertEqual(self.info.args, (abspath, self.request, {}))

    def test_static_url_with_empty_path(self):
        with self.assertRaises(ValueError):
            self.request.static_url('')

    def test_static_url_with_nonexistent_file(self):
        abspath = os.path.join('static', 'nonexistent.css')
        result = self.request.static_url(abspath)
        self.assertEqual(result, 'http://example.com/static/nonexistent.css')
        self.assertEqual(self.info.args, (abspath, self.request, {}))
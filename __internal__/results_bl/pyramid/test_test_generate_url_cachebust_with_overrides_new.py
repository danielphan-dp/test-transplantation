import os
import unittest
from pyramid import testing

class TestStaticURL(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.request = testing.DummyRequest()
        self.config.add_static_view('static', 'path')

    def tearDown(self):
        testing.tearDown()

    def test_static_url_with_no_cache_buster(self):
        result = self.request.static_url('path/foo.png')
        self.assertEqual(result, 'http://example.com/static/foo.png')

    def test_static_url_with_empty_cache_buster(self):
        self.config.add_cache_buster('path', lambda val: (val, {}))
        result = self.request.static_url('path/foo.png')
        self.assertEqual(result, 'http://example.com/static/foo.png')

    def test_static_url_with_nonexistent_path(self):
        result = self.request.static_url('path/nonexistent.png')
        self.assertEqual(result, 'http://example.com/static/nonexistent.png')

    def test_static_url_with_multiple_cache_busters(self):
        self.config.add_cache_buster('path', lambda val: (val, {'_query': {'x': val}}))
        self.config.add_cache_buster('other_path', lambda val: (val, {'_query': {'y': val}}), explicit=True)
        result = self.request.static_url('path/foo.png')
        self.assertEqual(result, 'http://example.com/static/foo.png?x=foo')
        result = self.request.static_url('other_path/foo.png')
        self.assertEqual(result, 'http://example.com/static/foo.png?y=foo')

    def test_static_url_with_query_parameters(self):
        self.config.add_cache_buster('path', lambda val: (val, {'_query': {'x': 'test'}}))
        result = self.request.static_url('path/foo.png')
        self.assertEqual(result, 'http://example.com/static/foo.png?x=test')

    def test_static_url_with_invalid_path(self):
        with self.assertRaises(ValueError):
            self.request.static_url(None)

    def test_static_url_with_special_characters(self):
        result = self.request.static_url('path/foo bar.png')
        self.assertEqual(result, 'http://example.com/static/foo%20bar.png')
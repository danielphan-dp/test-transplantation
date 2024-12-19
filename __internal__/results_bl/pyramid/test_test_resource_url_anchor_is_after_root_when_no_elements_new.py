import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.url import resource_url

class TestResourceURL(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.info = {
            'virtual_path': '/context/',
            'physical_path': '/context/',
            'app_url': 'http://example.com:5432'
        }

    def test_resource_url_with_no_anchor(self):
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_empty_anchor(self):
        result = resource_url(self.request, self.info, anchor='')
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_special_character_anchor(self):
        result = resource_url(self.request, self.info, anchor='@')
        self.assertEqual(result, 'http://example.com/contextabc/#@')

    def test_resource_url_with_long_anchor(self):
        long_anchor = 'a' * 1000
        result = resource_url(self.request, self.info, anchor=long_anchor)
        self.assertEqual(result, f'http://example.com/contextabc/#{long_anchor}')

    def test_resource_url_with_none_anchor(self):
        result = resource_url(self.request, self.info, anchor=None)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_invalid_info(self):
        with self.assertRaises(KeyError):
            resource_url(self.request, {})

    def test_resource_url_with_different_app_url(self):
        self.info['app_url'] = 'http://different.com:1234'
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://different.com/contextabc/')
import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.util import text_
from pyramid.url import resource_url

class TestResourceURL(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.info = {
            'virtual_path': '/context/',
            'physical_path': '/context/',
            'app_url': 'http://example.com:5432'
        }

    def test_resource_url_basic(self):
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_unicode_in_virtual_path(self):
        self.info['virtual_path'] = text_(b'La Pe\xc3\xb1a', 'utf-8')
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_empty_virtual_path(self):
        self.info['virtual_path'] = ''
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_invalid_info(self):
        with self.assertRaises(KeyError):
            resource_url(self.request, {})

    def test_resource_url_different_app_url(self):
        self.info['app_url'] = 'http://another-example.com:1234'
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://another-example.com/contextabc/')
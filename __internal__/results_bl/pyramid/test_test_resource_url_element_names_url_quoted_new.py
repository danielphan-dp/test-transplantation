import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.url import resource_url

class TestResourceUrl(unittest.TestCase):

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

    def test_resource_url_with_special_characters(self):
        self.info['virtual_path'] = '/context/a b c'
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_empty_info(self):
        with self.assertRaises(KeyError):
            resource_url(self.request, {})

    def test_resource_url_with_missing_virtual_path(self):
        del self.info['virtual_path']
        with self.assertRaises(KeyError):
            resource_url(self.request, self.info)

    def test_resource_url_with_invalid_app_url(self):
        self.info['app_url'] = 'invalid_url'
        result = resource_url(self.request, self.info)
        self.assertNotEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_different_context(self):
        self.info['virtual_path'] = '/different_context/'
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')
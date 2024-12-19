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

    def test_resource_url_default(self):
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_different_app_url(self):
        self.info['app_url'] = 'http://anotherurl.com'
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://anotherurl.com/contextabc/')

    def test_resource_url_with_missing_virtual_path(self):
        self.info['virtual_path'] = None
        with self.assertRaises(KeyError):
            resource_url(self.request, self.info)

    def test_resource_url_with_empty_physical_path(self):
        self.info['physical_path'] = ''
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_invalid_app_url(self):
        self.info['app_url'] = 'invalid-url'
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')
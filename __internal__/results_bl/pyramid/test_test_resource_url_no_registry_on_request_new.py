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

    def test_resource_url_with_valid_info(self):
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_missing_virtual_path(self):
        del self.info['virtual_path']
        with self.assertRaises(KeyError):
            resource_url(self.request, self.info)

    def test_resource_url_with_missing_physical_path(self):
        del self.info['physical_path']
        with self.assertRaises(KeyError):
            resource_url(self.request, self.info)

    def test_resource_url_with_missing_app_url(self):
        del self.info['app_url']
        with self.assertRaises(KeyError):
            resource_url(self.request, self.info)

    def test_resource_url_with_empty_info(self):
        with self.assertRaises(KeyError):
            resource_url(self.request, {})

    def test_resource_url_with_invalid_request(self):
        invalid_request = None
        with self.assertRaises(AssertionError):
            resource_url(invalid_request, self.info)

    def test_resource_url_with_different_app_url(self):
        self.info['app_url'] = 'http://different.com:1234'
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://different.com/contextabc/')
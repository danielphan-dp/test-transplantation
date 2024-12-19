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

    def test_resource_url_basic(self):
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_extra_path(self):
        result = resource_url(self.request, {'virtual_path': '/context/extra', 'physical_path': '/context/extra', 'app_url': 'http://example.com:5432'})
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_different_app_url(self):
        self.info['app_url'] = 'http://different.com:1234'
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_invalid_info(self):
        with self.assertRaises(KeyError):
            resource_url(self.request, {})

    def test_resource_url_missing_virtual_path(self):
        del self.info['virtual_path']
        with self.assertRaises(KeyError):
            resource_url(self.request, self.info)

    def test_resource_url_missing_physical_path(self):
        del self.info['physical_path']
        with self.assertRaises(KeyError):
            resource_url(self.request, self.info)

    def test_resource_url_with_special_characters(self):
        result = resource_url(self.request, {'virtual_path': '/context/special%20chars/', 'physical_path': '/context/special%20chars/', 'app_url': 'http://example.com:5432'})
        self.assertEqual(result, 'http://example.com/contextabc/')
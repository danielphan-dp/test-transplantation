import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper

class TestResourceURL(unittest.TestCase):

    def setUp(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '5432',
            'SERVER_NAME': 'example.com',
        }
        self.request = DummyRequest(environ)

    def test_resource_url_with_valid_info(self):
        info = {
            'virtual_path': '/context/',
            'physical_path': '/context/',
            'app_url': 'http://example.com:5432'
        }
        result = resource_url(self.request, info)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_invalid_virtual_path(self):
        info = {
            'virtual_path': '/invalid/',
            'physical_path': '/context/',
            'app_url': 'http://example.com:5432'
        }
        result = resource_url(self.request, info)
        self.assertNotEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_missing_info(self):
        info = {}
        with self.assertRaises(KeyError):
            resource_url(self.request, info)

    def test_resource_url_with_different_app_url(self):
        info = {
            'virtual_path': '/context/',
            'physical_path': '/context/',
            'app_url': 'http://different.com:8080'
        }
        result = resource_url(self.request, info)
        self.assertNotEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_empty_info(self):
        info = {
            'virtual_path': '',
            'physical_path': '',
            'app_url': ''
        }
        result = resource_url(self.request, info)
        self.assertEqual(result, 'http://example.com/contextabc/')
import os
import unittest
from pyramid.testing import DummyRequest

class TestResourceUrl(unittest.TestCase):

    def setUp(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        self.request = DummyRequest(environ)
        self.info = {
            'virtual_path': '/context/',
            'physical_path': '/context/',
            'app_url': 'http://example.com:5432'
        }

    def test_resource_url_with_valid_info(self):
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_different_virtual_path(self):
        self.info['virtual_path'] = '/different_context/'
        result = resource_url(self.request, self.info)
        self.assertNotEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_invalid_request(self):
        with self.assertRaises(AssertionError):
            resource_url(None, self.info)

    def test_resource_url_with_missing_info(self):
        with self.assertRaises(KeyError):
            resource_url(self.request, {})

    def test_resource_url_with_empty_info(self):
        self.info = {}
        with self.assertRaises(KeyError):
            resource_url(self.request, self.info)

    def test_resource_url_with_invalid_app_url(self):
        self.info['app_url'] = 'invalid_url'
        result = resource_url(self.request, self.info)
        self.assertNotEqual(result, 'http://example.com/contextabc/')
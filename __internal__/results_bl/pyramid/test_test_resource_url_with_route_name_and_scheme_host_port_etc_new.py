import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper

class TestResourceUrl(unittest.TestCase):

    def setUp(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '5432',
            'SERVER_NAME': 'example.com',
        }
        self.request = DummyRequest(environ)
        self.info = {
            'virtual_path': '/context/',
            'physical_path': '/context/',
            'app_url': 'http://example.com:5432'
        }

    def test_resource_url_valid(self):
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_invalid_virtual_path(self):
        self.info['virtual_path'] = '/invalid/'
        with self.assertRaises(AssertionError):
            resource_url(self.request, self.info)

    def test_resource_url_invalid_physical_path(self):
        self.info['physical_path'] = '/invalid/'
        with self.assertRaises(AssertionError):
            resource_url(self.request, self.info)

    def test_resource_url_invalid_app_url(self):
        self.info['app_url'] = 'http://invalid.com:5432'
        with self.assertRaises(AssertionError):
            resource_url(self.request, self.info)

    def test_resource_url_empty_info(self):
        with self.assertRaises(KeyError):
            resource_url(self.request, {})

    def test_resource_url_missing_keys(self):
        del self.info['virtual_path']
        with self.assertRaises(KeyError):
            resource_url(self.request, self.info)

    def test_resource_url_with_different_scheme(self):
        self.request.environ['wsgi.url_scheme'] = 'https'
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')  # Should still return http

    def test_resource_url_with_different_host(self):
        self.request.environ['SERVER_NAME'] = 'another-example.com'
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')  # Should still return original host

    def test_resource_url_with_different_port(self):
        self.request.environ['SERVER_PORT'] = '8080'
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')  # Should still return original port

if __name__ == '__main__':
    unittest.main()
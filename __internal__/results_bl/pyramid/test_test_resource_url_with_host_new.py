import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.url import resource_url

class TestResourceURL(unittest.TestCase):

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

    def test_resource_url_default(self):
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_different_host(self):
        result = resource_url(self.request, self.info, host='anotherhost.com')
        self.assertEqual(result, 'http://anotherhost.com/contextabc/')

    def test_resource_url_with_missing_info(self):
        with self.assertRaises(KeyError):
            resource_url(self.request, {})

    def test_resource_url_with_invalid_scheme(self):
        self.request.environ['wsgi.url_scheme'] = 'ftp'
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_empty_virtual_path(self):
        self.info['virtual_path'] = ''
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_custom_port(self):
        self.request.environ['SERVER_PORT'] = '8080'
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com:8080/contextabc/')
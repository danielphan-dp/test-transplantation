import os
import unittest
from pyramid.testing import DummyRequest

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

    def test_resource_url_default(self):
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_different_port(self):
        self.request.environ['SERVER_PORT'] = '8080'
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_no_port(self):
        self.request.environ['SERVER_PORT'] = ''
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_invalid_info(self):
        invalid_info = {
            'virtual_path': None,
            'physical_path': None,
            'app_url': None
        }
        with self.assertRaises(KeyError):
            resource_url(self.request, invalid_info)

    def test_resource_url_with_empty_request(self):
        empty_request = DummyRequest()
        with self.assertRaises(AssertionError):
            resource_url(empty_request, self.info)
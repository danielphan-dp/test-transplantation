import os
import unittest
from pyramid.testing import DummyRequest, DummyResource
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

    def test_resource_url_with_valid_info(self):
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_missing_virtual_path(self):
        info = self.info.copy()
        del info['virtual_path']
        with self.assertRaises(KeyError):
            resource_url(self.request, info)

    def test_resource_url_with_invalid_app_url(self):
        info = self.info.copy()
        info['app_url'] = 'invalid_url'
        with self.assertRaises(ValueError):
            resource_url(self.request, info)

    def test_resource_url_with_different_server_port(self):
        self.request.environ['SERVER_PORT'] = '8080'
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_empty_info(self):
        with self.assertRaises(KeyError):
            resource_url(self.request, {})

    def test_resource_url_with_unexpected_info_structure(self):
        info = {'unexpected_key': 'value'}
        with self.assertRaises(KeyError):
            resource_url(self.request, info)
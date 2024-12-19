import unittest
from pyramid.request import Request
from pyramid.testing import DummyRequest

class TestResourceURL(unittest.TestCase):

    def setUp(self):
        environ = {
            'PATH_INFO': '/',
            'SERVER_NAME': 'example.com',
            'SERVER_PORT': '5432',
            'wsgi.url_scheme': 'http',
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

    def test_resource_url_missing_info(self):
        with self.assertRaises(KeyError):
            resource_url(self.request, {})

    def test_resource_url_different_server_port(self):
        self.request.environ['SERVER_PORT'] = '80'
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')
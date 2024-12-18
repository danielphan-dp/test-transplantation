import unittest
from pyramid.request import Request
from pyramid.testing import DummyRequest

class TestResourceUrl(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '5432',
            'SERVER_NAME': 'example.com',
        }
        self.info = {
            'virtual_path': '/context/',
            'physical_path': '/context/',
            'app_url': 'http://example.com:5432'
        }

    def test_resource_url_with_default_values(self):
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_custom_app_url(self):
        self.info['app_url'] = 'http://custom.com'
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://custom.com/contextabc/')

    def test_resource_url_with_empty_app_url(self):
        self.info['app_url'] = ''
        result = resource_url(self.request, self.info)
        self.assertEqual(result, '/contextabc/')

    def test_resource_url_with_different_virtual_path(self):
        self.info['virtual_path'] = '/different_context/'
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/different_contextabc/')

    def test_resource_url_with_invalid_info(self):
        with self.assertRaises(KeyError):
            resource_url(self.request, {})

    def test_resource_url_with_no_info(self):
        result = resource_url(self.request, None)
        self.assertEqual(result, 'http://example.com/contextabc/')
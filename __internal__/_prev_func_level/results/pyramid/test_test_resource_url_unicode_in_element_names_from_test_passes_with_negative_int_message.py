import unittest
from pyramid.testing import DummyRequest
from pyramid.url import resource_url

class TestResourceURL(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.host = 'example.com:5432'
        self.request.environ = {'wsgi.url_scheme': 'http'}

    def test_resource_url_with_unicode_context(self):
        uc = 'La Pe\xc3\xb1a'
        result = resource_url(self.request, {'virtual_path': '/context/', 'physical_path': '/context/', 'app_url': 'http://example.com:5432'}, uc)
        self.assertEqual(result, 'http://example.com:5432/context/La%20Pe%C3%B1a')

    def test_resource_url_with_empty_app_url(self):
        result = resource_url(self.request, {'virtual_path': '/context/', 'physical_path': '/context/', 'app_url': ''})
        self.assertEqual(result, '/context/')

    def test_resource_url_with_none_anchor(self):
        result = resource_url(self.request, {'virtual_path': '/context/', 'physical_path': '/context/', 'app_url': 'http://example.com:5432'}, anchor=None)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_special_characters(self):
        special_char = ' /#?&+'
        result = resource_url(self.request, {'virtual_path': '/context/', 'physical_path': '/context/', 'app_url': 'http://example.com:5432'}, anchor=special_char)
        self.assertEqual(result, 'http://example.com:5432/context/#%20/%23?&+')

    def test_resource_url_with_different_scheme(self):
        self.request.environ['wsgi.url_scheme'] = 'https'
        result = resource_url(self.request, {'virtual_path': '/context/', 'physical_path': '/context/', 'app_url': 'http://example.com:5432'})
        self.assertEqual(result, 'https://example.com:5432/context/')

    def test_resource_url_with_custom_host(self):
        result = resource_url(self.request, {'virtual_path': '/context/', 'physical_path': '/context/', 'app_url': 'http://customhost.com'})
        self.assertEqual(result, 'http://customhost.com/context/')
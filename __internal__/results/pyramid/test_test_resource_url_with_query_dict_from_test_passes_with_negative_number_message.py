import unittest
from pyramid.testing import DummyRequest
from pyramid.url import resource_url

class TestResourceURL(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.host = 'example.com:5432'
        self.request.environ = {'wsgi.url_scheme': 'http'}

    def test_resource_url_with_no_context(self):
        result = resource_url(None, self.request)
        self.assertEqual(result, 'http://example.com:5432/')

    def test_resource_url_with_empty_context(self):
        result = resource_url('', self.request)
        self.assertEqual(result, 'http://example.com:5432/')

    def test_resource_url_with_app_url(self):
        result = resource_url(None, self.request, app_url='http://somewhere.com')
        self.assertEqual(result, 'http://somewhere.com/')

    def test_resource_url_with_scheme(self):
        self.request.environ['wsgi.url_scheme'] = 'https'
        result = resource_url(None, self.request)
        self.assertEqual(result, 'https://example.com:5432/')

    def test_resource_url_with_custom_port(self):
        self.request.environ['SERVER_PORT'] = '8080'
        result = resource_url(None, self.request)
        self.assertEqual(result, 'http://example.com:8080/')

    def test_resource_url_with_anchor(self):
        result = resource_url(None, self.request, anchor='section1')
        self.assertEqual(result, 'http://example.com:5432/#section1')

    def test_resource_url_with_query_params(self):
        result = resource_url(None, self.request, query={'param': 'value'})
        self.assertEqual(result, 'http://example.com:5432/?param=value')

    def test_resource_url_with_unicode_anchor(self):
        uc = 'La Peñá'
        result = resource_url(None, self.request, anchor=uc)
        self.assertEqual(result, 'http://example.com:5432/#La%20Pe%C3%B1a')

    def test_resource_url_with_special_characters_in_anchor(self):
        result = resource_url(None, self.request, anchor=' /#?&+')
        self.assertEqual(result, 'http://example.com:5432/#%20/%23?&+')

    def test_resource_url_with_none_anchor(self):
        result = resource_url(None, self.request, anchor=None)
        self.assertEqual(result, 'http://example.com:5432/')
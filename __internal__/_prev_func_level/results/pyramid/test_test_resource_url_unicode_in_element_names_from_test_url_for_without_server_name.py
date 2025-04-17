import unittest
from pyramid.testing import DummyRequest
from pyramid.util import text_

class TestResourceURL(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '5432',
            'SERVER_NAME': 'example.com',
        }
        self.context = DummyContext()

    def test_resource_url_with_unicode_context(self):
        uc = text_(b'La Pe\xc3\xb1a', 'utf-8')
        result = self.request.resource_url(self.context, uc)
        self.assertEqual(result, 'http://example.com:5432/context/La%20Pe%C3%B1a')

    def test_resource_url_with_empty_anchor(self):
        result = self.request.resource_url(self.context, anchor='')
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_none_anchor(self):
        result = self.request.resource_url(self.context, anchor=None)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_special_characters(self):
        result = self.request.resource_url(self.context, anchor=' /#?&+')
        self.assertEqual(result, 'http://example.com:5432/context/#%20/%23?&+')

    def test_resource_url_with_app_url(self):
        result = self.request.resource_url(self.context, app_url='http://somewhere.com')
        self.assertEqual(result, 'http://somewhere.com/context/')

    def test_resource_url_with_scheme(self):
        result = self.request.resource_url(self.context, scheme='https')
        self.assertEqual(result, 'https://example.com:5432/context/')

    def test_resource_url_with_host(self):
        result = self.request.resource_url(self.context, host='someotherhost.com')
        self.assertEqual(result, 'http://someotherhost.com:5432/context/')

    def test_resource_url_with_port(self):
        result = self.request.resource_url(self.context, port='8181')
        self.assertEqual(result, 'http://example.com:8181/context/')

    def test_resource_url_no_registry_on_request(self):
        del self.request.registry
        result = self.request.resource_url(self.context)
        self.assertEqual(result, 'http://example.com:5432/context/')
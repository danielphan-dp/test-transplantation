import unittest
from pyramid.request import Request
from pyramid.url import resource_url
from pyramid.testing import DummyRequest, DummyResource

class TestResourceUrl(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.host = 'example.com:5432'
        self.request.environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '5432',
            'SERVER_NAME': 'example.com',
        }
        self.context = DummyResource()

    def test_resource_url_with_app_url(self):
        result = resource_url(self.context, app_url='http://somewhere.com')
        self.assertEqual(result, 'http://somewhere.com/context/')

    def test_resource_url_with_scheme(self):
        result = resource_url(self.context, scheme='https')
        self.assertEqual(result, 'https://example.com:5432/context/')

    def test_resource_url_with_host(self):
        result = resource_url(self.context, host='someotherhost.com')
        self.assertEqual(result, 'http://someotherhost.com:5432/context/')

    def test_resource_url_with_port(self):
        result = resource_url(self.context, port='8181')
        self.assertEqual(result, 'http://example.com:8181/context/')

    def test_resource_url_anchor_is_after_qs_when_qs_is_present(self):
        result = resource_url(self.context, 'a', query={'b': 'c'}, anchor='d')
        self.assertEqual(result, 'http://example.com:5432/context/a?b=c#d')

    def test_resource_url_anchor_is_encoded_utf8_if_unicode(self):
        uc = 'La Peña'
        result = resource_url(self.context, anchor=uc)
        self.assertEqual(result, 'http://example.com:5432/context/#La%20Pe%C3%B1a')

    def test_resource_url_anchor_is_urlencoded_safe(self):
        result = resource_url(self.context, anchor=' /#?&+')
        self.assertEqual(result, 'http://example.com:5432/context/#%20/%23?&+')

    def test_resource_url_anchor_is_None(self):
        result = resource_url(self.context, anchor=None)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_no_IResourceURL_registered(self):
        self.request.registry = None
        result = resource_url(self.context)
        self.assertEqual(result, 'http://example.com:5432/context/')
import unittest
from pyramid.request import Request
from pyramid.url import resource_url

class TestResourceUrl(unittest.TestCase):

    def setUp(self):
        self.environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '5432',
            'SERVER_NAME': 'example.com',
        }
        self.request = Request(self.environ)
        self.context = DummyContext()

    def test_resource_url_no_registry_on_request(self):
        del self.request.registry
        result = resource_url(self.context, request=self.request)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_app_url(self):
        result = resource_url(self.context, request=self.request, app_url='http://somewhere.com')
        self.assertEqual(result, 'http://somewhere.com/context/')

    def test_resource_url_with_scheme(self):
        result = resource_url(self.context, request=self.request, scheme='https')
        self.assertEqual(result, 'https://example.com:5432/context/')

    def test_resource_url_with_host(self):
        result = resource_url(self.context, request=self.request, host='someotherhost.com')
        self.assertEqual(result, 'http://someotherhost.com:5432/context/')

    def test_resource_url_with_port(self):
        result = resource_url(self.context, request=self.request, port='8181')
        self.assertEqual(result, 'http://example.com:8181/context/')

    def test_resource_url_with_query(self):
        result = resource_url(self.context, request=self.request, query={'a': '1'})
        self.assertEqual(result, 'http://example.com:5432/context/?a=1')

    def test_resource_url_anchor_is_after_qs_when_qs_is_present(self):
        result = resource_url(self.context, request=self.request, query={'b': 'c'}, anchor='d')
        self.assertEqual(result, 'http://example.com:5432/context/?b=c#d')

    def test_resource_url_anchor_is_encoded_utf8_if_unicode(self):
        uc = 'La Peña'
        result = resource_url(self.context, request=self.request, anchor=uc)
        self.assertEqual(result, 'http://example.com:5432/context/#La%20Pe%C3%B1a')

    def test_resource_url_anchor_is_urlencoded_safe(self):
        result = resource_url(self.context, request=self.request, anchor=' /#?&+')
        self.assertEqual(result, 'http://example.com:5432/context/#%20/%23?&+')

    def test_resource_url_anchor_is_None(self):
        result = resource_url(self.context, request=self.request, anchor=None)
        self.assertEqual(result, 'http://example.com:5432/context/')
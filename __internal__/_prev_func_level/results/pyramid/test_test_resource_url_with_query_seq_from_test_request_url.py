import unittest
from pyramid.testing import DummyRequest
from pyramid.url import resource_url

class TestResourceUrl(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.host = 'example.com:5432'
        self.request.environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '5432',
            'SERVER_NAME': 'example.com',
        }
        self.context = DummyContext()

    def test_resource_url_no_registry_on_request(self):
        del self.request.registry
        result = resource_url(self.context, request=self.request)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_app_url(self):
        result = resource_url(self.context, app_url='http://somewhere.com', request=self.request)
        self.assertEqual(result, 'http://somewhere.com/context/')

    def test_resource_url_with_scheme(self):
        self.request.environ['wsgi.url_scheme'] = 'http'
        result = resource_url(self.context, scheme='https', request=self.request)
        self.assertEqual(result, 'https://example.com:5432/context/')

    def test_resource_url_with_host(self):
        result = resource_url(self.context, host='someotherhost.com', request=self.request)
        self.assertEqual(result, 'http://someotherhost.com:5432/context/')

    def test_resource_url_with_port(self):
        result = resource_url(self.context, port='8181', request=self.request)
        self.assertEqual(result, 'http://example.com:8181/context/')

    def test_resource_url_anchor_is_after_qs_when_qs_is_present(self):
        result = resource_url(self.context, 'a', query={'b': 'c'}, anchor='d', request=self.request)
        self.assertEqual(result, 'http://example.com:5432/context/a?b=c#d')

    def test_resource_url_anchor_is_encoded_utf8_if_unicode(self):
        uc = text_(b'La Pe\xc3\xb1a', 'utf-8')
        result = resource_url(self.context, anchor=uc, request=self.request)
        self.assertEqual(result, 'http://example.com:5432/context/#La%20Pe%C3%B1a')

    def test_resource_url_anchor_is_urlencoded_safe(self):
        result = resource_url(self.context, anchor=' /#?&+', request=self.request)
        self.assertEqual(result, 'http://example.com:5432/context/#%20/%23?&+')

    def test_resource_url_anchor_is_None(self):
        result = resource_url(self.context, anchor=None, request=self.request)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_no_IResourceURL_registered(self):
        self.context.__name__ = ''
        self.context.__parent__ = None
        result = resource_url(self.context, request=self.request)
        self.assertEqual(result, 'http://example.com:5432/')
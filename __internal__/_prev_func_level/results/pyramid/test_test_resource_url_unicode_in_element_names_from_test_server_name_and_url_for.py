import unittest
from pyramid.testing import DummyRequest
from pyramid.url import resource_url

class TestResourceURL(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.registry = self._registerResourceURL(self.request.registry)

    def _registerResourceURL(self, registry):
        # Mock registration logic for resource URL
        return registry

    def test_resource_url_with_unicode_context(self):
        uc = 'La Pe\xc3\xb1a'
        context = DummyContext()
        result = resource_url(context, uc, request=self.request)
        self.assertEqual(result, 'http://example.com:5432/context/La%20Pe%C3%B1a')

    def test_resource_url_with_empty_anchor(self):
        context = DummyContext()
        result = resource_url(context, anchor='', request=self.request)
        self.assertEqual(result, 'http://example.com:5432/context/#')

    def test_resource_url_with_none_anchor(self):
        context = DummyContext()
        result = resource_url(context, anchor=None, request=self.request)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_app_url(self):
        context = DummyContext()
        result = resource_url(context, app_url='http://somewhere.com', request=self.request)
        self.assertEqual(result, 'http://somewhere.com/context/')

    def test_resource_url_with_scheme(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        self.request.environ = environ
        context = DummyContext()
        result = resource_url(context, scheme='https', request=self.request)
        self.assertEqual(result, 'https://example.com/context/')

    def test_resource_url_with_host(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        self.request.environ = environ
        context = DummyContext()
        result = resource_url(context, host='someotherhost.com', request=self.request)
        self.assertEqual(result, 'http://someotherhost.com:8080/context/')

    def test_resource_url_with_port(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        self.request.environ = environ
        context = DummyContext()
        result = resource_url(context, port='8181', request=self.request)
        self.assertEqual(result, 'http://example.com:8181/context/')

    def test_resource_url_anchor_is_encoded_utf8_if_unicode(self):
        context = DummyContext()
        uc = 'La Pe\xc3\xb1a'
        result = resource_url(context, anchor=uc, request=self.request)
        self.assertEqual(result, 'http://example.com:5432/context/#La%20Pe%C3%B1a')

    def test_resource_url_anchor_is_urlencoded_safe(self):
        context = DummyContext()
        result = resource_url(context, anchor=' /#?&+', request=self.request)
        self.assertEqual(result, 'http://example.com:5432/context/#%20/%23?&+')

    def test_resource_url_no_IResourceURL_registered(self):
        root = DummyContext()
        root.__name__ = ''
        root.__parent__ = None
        self.request.environ = {}
        result = resource_url(root, request=self.request)
        self.assertEqual(result, 'http://example.com:5432/')
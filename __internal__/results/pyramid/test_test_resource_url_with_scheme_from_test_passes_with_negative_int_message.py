import unittest
from pyramid.request import Request
from pyramid.testing import DummyRequest

class TestResourceUrl(unittest.TestCase):

    def setUp(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '5432',
            'SERVER_NAME': 'example.com',
        }
        self.request = DummyRequest(environ)
        self.request.registry = self._registerResourceURL(self.request.registry)

    def _registerResourceURL(self, registry):
        # Mock registration of resource URL
        return registry

    def test_resource_url_with_app_url(self):
        root = DummyContext()
        result = self.request.resource_url(root, app_url='http://somewhere.com')
        self.assertEqual(result, 'http://somewhere.com/context/')

    def test_resource_url_with_host(self):
        root = DummyContext()
        result = self.request.resource_url(root, host='someotherhost.com')
        self.assertEqual(result, 'http://someotherhost.com:5432/context/')

    def test_resource_url_with_port(self):
        root = DummyContext()
        result = self.request.resource_url(root, port='8181')
        self.assertEqual(result, 'http://example.com:8181/context/')

    def test_resource_url_with_scheme(self):
        root = DummyContext()
        result = self.request.resource_url(root, scheme='https')
        self.assertEqual(result, 'https://example.com/context/')

    def test_resource_url_no_registry_on_request(self):
        del self.request.registry
        root = DummyContext()
        result = self.request.resource_url(root)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_anchor_is_after_qs_when_qs_is_present(self):
        context = DummyContext()
        result = self.request.resource_url(context, 'a', query={'b': 'c'}, anchor='d')
        self.assertEqual(result, 'http://example.com:5432/context/a?b=c#d')

    def test_resource_url_anchor_is_encoded_utf8_if_unicode(self):
        context = DummyContext()
        uc = 'La Peñá'
        result = self.request.resource_url(context, anchor=uc)
        self.assertEqual(result, 'http://example.com:5432/context/#La%20Pe%C3%B1a')

    def test_resource_url_anchor_is_urlencoded_safe(self):
        context = DummyContext()
        result = self.request.resource_url(context, anchor=' /#?&+')
        self.assertEqual(result, 'http://example.com:5432/context/#%20/%23?&+')

    def test_resource_url_anchor_is_None(self):
        context = DummyContext()
        result = self.request.resource_url(context, anchor=None)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_no_IResourceURL_registered(self):
        root = DummyContext()
        root.__name__ = ''
        root.__parent__ = None
        self.request.environ = {}
        result = self.request.resource_url(root)
        self.assertEqual(result, 'http://example.com:5432/')
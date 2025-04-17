import unittest
from pyramid.request import Request
from pyramid.url import resource_url

class TestResourceURL(unittest.TestCase):

    def setUp(self):
        self.request = Request.blank('/')
        self.request.registry = self._make_registry()

    def _make_registry(self):
        from pyramid.registry import Registry
        return Registry()

    def test_resource_url_with_app_url(self):
        root = DummyContext()
        result = resource_url(root, app_url='http://somewhere.com', req=self.request)
        self.assertEqual(result, 'http://somewhere.com/context/')

    def test_resource_url_with_scheme(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        request = Request(environ)
        root = DummyContext()
        result = resource_url(root, scheme='https', req=request)
        self.assertEqual(result, 'https://example.com/context/')

    def test_resource_url_with_host(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        request = Request(environ)
        root = DummyContext()
        result = resource_url(root, host='someotherhost.com', req=request)
        self.assertEqual(result, 'http://someotherhost.com:8080/context/')

    def test_resource_url_with_port(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        request = Request(environ)
        root = DummyContext()
        result = resource_url(root, port='8181', req=request)
        self.assertEqual(result, 'http://example.com:8181/context/')

    def test_resource_url_anchor_is_after_qs_when_qs_is_present(self):
        root = DummyContext()
        result = resource_url(root, 'a', query={'b': 'c'}, anchor='d', req=self.request)
        self.assertEqual(result, 'http://example.com:5432/context/a?b=c#d')

    def test_resource_url_anchor_is_encoded_utf8_if_unicode(self):
        root = DummyContext()
        uc = 'La Peñá'
        result = resource_url(root, anchor=uc, req=self.request)
        self.assertEqual(result, 'http://example.com:5432/context/#La%20Pe%C3%B1a')

    def test_resource_url_anchor_is_urlencoded_safe(self):
        root = DummyContext()
        result = resource_url(root, anchor=' /#?&+', req=self.request)
        self.assertEqual(result, 'http://example.com:5432/context/#%20/%23?&+')

    def test_resource_url_anchor_is_None(self):
        root = DummyContext()
        result = resource_url(root, anchor=None, req=self.request)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_no_IResourceURL_registered(self):
        root = DummyContext()
        root.__name__ = ''
        root.__parent__ = None
        request = Request.blank('/')
        request.environ = {}
        result = resource_url(root, req=request)
        self.assertEqual(result, 'http://example.com:5432/')
import unittest
from pyramid.testing import DummyRequest
from pyramid.url import resource_url

class TestResourceUrl(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.host = 'example.com:5432'
        self.request.environ = {'wsgi.url_scheme': 'http'}

    def test_resource_url_no_registry_on_request(self):
        context = DummyContext()
        result = resource_url(context, request=self.request)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_app_url(self):
        context = DummyContext()
        result = resource_url(context, request=self.request, app_url='http://somewhere.com')
        self.assertEqual(result, 'http://somewhere.com/context/')

    def test_resource_url_with_scheme(self):
        context = DummyContext()
        result = resource_url(context, request=self.request, scheme='https')
        self.assertEqual(result, 'https://example.com:5432/context/')

    def test_resource_url_with_host(self):
        context = DummyContext()
        result = resource_url(context, request=self.request, host='someotherhost.com')
        self.assertEqual(result, 'http://someotherhost.com:5432/context/')

    def test_resource_url_with_port(self):
        context = DummyContext()
        result = resource_url(context, request=self.request, port='8181')
        self.assertEqual(result, 'http://example.com:8181/context/')

    def test_resource_url_anchor_is_after_root_when_no_elements(self):
        context = DummyContext()
        result = resource_url(context, request=self.request, anchor='a')
        self.assertEqual(result, 'http://example.com:5432/context/#a')

    def test_resource_url_anchor_is_encoded_utf8_if_unicode(self):
        context = DummyContext()
        uc = text_(b'La Pe\\xc3\\xb1a', 'utf-8')
        result = resource_url(context, request=self.request, anchor=uc)
        self.assertEqual(result, 'http://example.com:5432/context/#La%20Pe%C3%B1a')

    def test_resource_url_anchor_is_urlencoded_safe(self):
        context = DummyContext()
        result = resource_url(context, request=self.request, anchor=' /#?&+')
        self.assertEqual(result, 'http://example.com:5432/context/#%20/%23?&+')

    def test_resource_url_anchor_is_None(self):
        context = DummyContext()
        result = resource_url(context, request=self.request, anchor=None)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_no_IResourceURL_registered(self):
        root = DummyContext()
        root.__name__ = ''
        root.__parent__ = None
        result = resource_url(root, request=self.request)
        self.assertEqual(result, 'http://example.com:5432/')
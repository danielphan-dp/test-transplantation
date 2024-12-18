import unittest
from pyramid.testing import DummyRequest
from pyramid.url import resource_url

class TestResourceUrl(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.host = 'example.com:5432'
        self.request.environ = {'wsgi.url_scheme': 'http'}

    def test_resource_url_with_no_context(self):
        result = resource_url(self.request, {})
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_app_url(self):
        result = resource_url(self.request, {}, app_url='http://somewhere.com')
        self.assertEqual(result, 'http://somewhere.com/context/')

    def test_resource_url_with_scheme(self):
        result = resource_url(self.request, {}, scheme='https')
        self.assertEqual(result, 'https://example.com/context/')

    def test_resource_url_with_host(self):
        result = resource_url(self.request, {}, host='someotherhost.com')
        self.assertEqual(result, 'http://someotherhost.com:5432/context/')

    def test_resource_url_with_port(self):
        result = resource_url(self.request, {}, port='8181')
        self.assertEqual(result, 'http://example.com:8181/context/')

    def test_resource_url_anchor_is_after_root_when_no_elements(self):
        context = {}
        result = resource_url(self.request, context, anchor='a')
        self.assertEqual(result, 'http://example.com:5432/context/#a')

    def test_resource_url_anchor_is_encoded_utf8_if_unicode(self):
        context = {}
        uc = 'La Peñá'
        result = resource_url(self.request, context, anchor=uc)
        self.assertEqual(result, 'http://example.com:5432/context/#La%20Pe%C3%B1a')

    def test_resource_url_anchor_is_urlencoded_safe(self):
        context = {}
        result = resource_url(self.request, context, anchor=' /#?&+')
        self.assertEqual(result, 'http://example.com:5432/context/#%20/%23?&+')

    def test_resource_url_anchor_is_None(self):
        context = {}
        result = resource_url(self.request, context, anchor=None)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_no_IResourceURL_registered(self):
        context = {}
        result = resource_url(self.request, context)
        self.assertEqual(result, 'http://example.com:5432/context/')
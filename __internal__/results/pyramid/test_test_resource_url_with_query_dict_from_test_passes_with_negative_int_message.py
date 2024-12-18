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
        context = DummyContext()
        result = resource_url(context, self.request)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_app_url(self):
        context = DummyContext()
        result = resource_url(context, self.request, app_url='http://somewhere.com')
        self.assertEqual(result, 'http://somewhere.com/context/')

    def test_resource_url_with_scheme(self):
        environ = {
            'wsgi.url_scheme': 'https',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        request = DummyRequest(environ=environ)
        context = DummyContext()
        result = resource_url(context, request)
        self.assertEqual(result, 'https://example.com/context/')

    def test_resource_url_with_invalid_context(self):
        with self.assertRaises(TypeError):
            resource_url('invalid_context', self.request)

    def test_resource_url_with_query_params(self):
        context = DummyContext()
        result = resource_url(context, self.request, query={'param': 'value'})
        self.assertEqual(result, 'http://example.com:5432/context/?param=value')

    def test_resource_url_with_anchor(self):
        context = DummyContext()
        result = resource_url(context, self.request, anchor='section1')
        self.assertEqual(result, 'http://example.com:5432/context/#section1')

    def test_resource_url_with_encoded_anchor(self):
        context = DummyContext()
        result = resource_url(context, self.request, anchor='La Pe\xc3\xb1a')
        self.assertEqual(result, 'http://example.com:5432/context/#La%20Pe%C3%B1a')

    def test_resource_url_with_none_anchor(self):
        context = DummyContext()
        result = resource_url(context, self.request, anchor=None)
        self.assertEqual(result, 'http://example.com:5432/context/')
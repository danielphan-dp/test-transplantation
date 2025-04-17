import unittest
from pyramid.testing import DummyRequest
from pyramid.url import resource_url

class TestResourceURL(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.registry = self._registerResourceURL(self.request.registry)

    def _registerResourceURL(self, registry):
        # Mock registration of resource URL
        return registry

    def test_resource_url_with_no_context(self):
        result = resource_url(self.request, {})
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_app_url(self):
        result = resource_url(self.request, {}, app_url='http://somewhere.com')
        self.assertEqual(result, 'http://somewhere.com/context/')

    def test_resource_url_with_scheme(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        self.request.environ = environ
        result = resource_url(self.request, {}, scheme='https')
        self.assertEqual(result, 'https://example.com/context/')

    def test_resource_url_with_host(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        self.request.environ = environ
        result = resource_url(self.request, {}, host='someotherhost.com')
        self.assertEqual(result, 'http://someotherhost.com:8080/context/')

    def test_resource_url_with_port(self):
        environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '8080',
            'SERVER_NAME': 'example.com',
        }
        self.request.environ = environ
        result = resource_url(self.request, {}, port='8181')
        self.assertEqual(result, 'http://example.com:8181/context/')

    def test_resource_url_with_query_params(self):
        result = resource_url(self.request, {}, query=[('a', 'hi there'), ('b', 'value')])
        self.assertEqual(result, 'http://example.com:5432/context/?a=hi+there&b=value')

    def test_resource_url_with_anchor(self):
        result = resource_url(self.request, {}, anchor='section1')
        self.assertEqual(result, 'http://example.com:5432/context/#section1')

    def test_resource_url_with_encoded_anchor(self):
        result = resource_url(self.request, {}, anchor='La Pe\xc3\xb1a')
        self.assertEqual(result, 'http://example.com:5432/context/#La%20Pe%C3%B1a')

    def test_resource_url_with_none_anchor(self):
        result = resource_url(self.request, {}, anchor=None)
        self.assertEqual(result, 'http://example.com:5432/context/')
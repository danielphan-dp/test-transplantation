import unittest
from pyramid.request import Request
from pyramid.testing import DummyRequest

class TestResourceUrl(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.environ = {
            'wsgi.url_scheme': 'http',
            'SERVER_PORT': '5432',
            'SERVER_NAME': 'example.com',
        }
        self.context = DummyContext()

    def test_resource_url_with_no_registry(self):
        del self.request.registry
        result = self.request.resource_url(self.context)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_app_url(self):
        result = self.request.resource_url(self.context, app_url='http://somewhere.com')
        self.assertEqual(result, 'http://somewhere.com/context/')

    def test_resource_url_with_scheme(self):
        result = self.request.resource_url(self.context, scheme='https')
        self.assertEqual(result, 'https://example.com:5432/context/')

    def test_resource_url_with_host(self):
        result = self.request.resource_url(self.context, host='someotherhost.com')
        self.assertEqual(result, 'http://someotherhost.com:5432/context/')

    def test_resource_url_with_port(self):
        result = self.request.resource_url(self.context, port='8181')
        self.assertEqual(result, 'http://example.com:8181/context/')

    def test_resource_url_with_query(self):
        result = self.request.resource_url(self.context, query={'a': '1'})
        self.assertEqual(result, 'http://example.com:5432/context/?a=1')

    def test_resource_url_with_anchor(self):
        result = self.request.resource_url(self.context, anchor='section1')
        self.assertEqual(result, 'http://example.com:5432/context/#section1')

    def test_resource_url_with_encoded_anchor(self):
        uc = 'La Peñ'
        result = self.request.resource_url(self.context, anchor=uc)
        self.assertEqual(result, 'http://example.com:5432/context/#La%20Pe%C3%B1')

    def test_resource_url_with_none_anchor(self):
        result = self.request.resource_url(self.context, anchor=None)
        self.assertEqual(result, 'http://example.com:5432/context/')
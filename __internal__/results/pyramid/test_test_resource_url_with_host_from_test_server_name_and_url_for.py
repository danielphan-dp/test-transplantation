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

    def test_resource_url_with_default_context(self):
        root = DummyContext()
        result = self.request.resource_url(root)
        self.assertEqual(result, 'http://example.com:5432/context/')

    def test_resource_url_with_app_url(self):
        root = DummyContext()
        result = self.request.resource_url(root, app_url='http://anotherhost.com')
        self.assertEqual(result, 'http://anotherhost.com/context/')

    def test_resource_url_with_scheme(self):
        root = DummyContext()
        result = self.request.resource_url(root, scheme='https')
        self.assertEqual(result, 'https://example.com:5432/context/')

    def test_resource_url_with_host(self):
        root = DummyContext()
        result = self.request.resource_url(root, host='someotherhost.com')
        self.assertEqual(result, 'http://someotherhost.com:5432/context/')

    def test_resource_url_with_port(self):
        root = DummyContext()
        result = self.request.resource_url(root, port='8080')
        self.assertEqual(result, 'http://example.com:8080/context/')

    def test_resource_url_with_anchor(self):
        root = DummyContext()
        result = self.request.resource_url(root, anchor='section1')
        self.assertEqual(result, 'http://example.com:5432/context/#section1')

    def test_resource_url_with_unicode_anchor(self):
        root = DummyContext()
        result = self.request.resource_url(root, anchor='La Peñita')
        self.assertEqual(result, 'http://example.com:5432/context/#La%20Pe%C3%B1ita')

    def test_resource_url_with_empty_anchor(self):
        root = DummyContext()
        result = self.request.resource_url(root, anchor='')
        self.assertEqual(result, 'http://example.com:5432/context/#')

    def test_resource_url_no_registry(self):
        del self.request.registry
        root = DummyContext()
        result = self.request.resource_url(root)
        self.assertEqual(result, 'http://example.com:5432/context/')

if __name__ == '__main__':
    unittest.main()
import unittest
from pyramid.interfaces import IStaticURLInfo
from pyramid.testing import DummyRequest

class TestStaticURL(unittest.TestCase):

    def setUp(self):
        self.environ = {
            'PATH_INFO': '/',
            'SERVER_NAME': 'example.com',
            'SERVER_PORT': '5432',
            'QUERY_STRING': '',
            'wsgi.url_scheme': 'http',
        }
        self.request = DummyRequest(self.environ)

    def test_static_url_with_valid_path(self):
        info = DummyStaticURLInfo('abc')
        self.request.registry.registerUtility(info, IStaticURLInfo)
        result = self.request.static_url('pyramid.tests:static/foo.css')
        self.assertEqual(result, 'abc')
        self.assertEqual(info.args, ('pyramid.tests:static/foo.css', self.request, {}))

    def test_static_url_with_empty_path(self):
        info = DummyStaticURLInfo('empty')
        self.request.registry.registerUtility(info, IStaticURLInfo)
        result = self.request.static_url('')
        self.assertEqual(result, 'empty')
        self.assertEqual(info.args, ('', self.request, {}))

    def test_static_url_with_query_string(self):
        info = DummyStaticURLInfo('query')
        self.request.registry.registerUtility(info, IStaticURLInfo)
        result = self.request.static_url('pyramid.tests:static/foo.css', query='test')
        self.assertEqual(result, 'query')
        self.assertEqual(info.args, ('pyramid.tests:static/foo.css', self.request, {'query': 'test'}))

    def test_static_url_with_additional_kwargs(self):
        info = DummyStaticURLInfo('kwargs')
        self.request.registry.registerUtility(info, IStaticURLInfo)
        result = self.request.static_url('pyramid.tests:static/foo.css', extra='value')
        self.assertEqual(result, 'kwargs')
        self.assertEqual(info.args, ('pyramid.tests:static/foo.css', self.request, {'extra': 'value'}))

    def test_static_url_with_nonexistent_path(self):
        info = DummyStaticURLInfo('not_found')
        self.request.registry.registerUtility(info, IStaticURLInfo)
        result = self.request.static_url('pyramid.tests:static/nonexistent.css')
        self.assertEqual(result, 'not_found')
        self.assertEqual(info.args, ('pyramid.tests:static/nonexistent.css', self.request, {}))
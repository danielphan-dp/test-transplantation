import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.url import resource_url

class TestResourceURL(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.info = {
            'virtual_path': '/context/',
            'physical_path': '/context/',
            'app_url': 'http://example.com:5432'
        }

    def test_resource_url_with_valid_context(self):
        context = DummyContext()
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_invalid_context(self):
        context = None
        with self.assertRaises(TypeError):
            resource_url(self.request, self.info)

    def test_resource_url_with_altered_info(self):
        self.info['app_url'] = 'http://different.com:1234'
        context = DummyContext()
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://different.com/contextabc/')

    def test_resource_url_with_empty_info(self):
        self.info = {}
        context = DummyContext()
        with self.assertRaises(KeyError):
            resource_url(self.request, self.info)

    def test_resource_url_with_missing_virtual_path(self):
        del self.info['virtual_path']
        context = DummyContext()
        with self.assertRaises(KeyError):
            resource_url(self.request, self.info)

    def test_resource_url_with_missing_physical_path(self):
        del self.info['physical_path']
        context = DummyContext()
        with self.assertRaises(KeyError):
            resource_url(self.request, self.info)

    def test_resource_url_with_query_param(self):
        context = DummyContext()
        result = resource_url(self.request, self.info, query={'param': 'value'})
        self.assertEqual(result, 'http://example.com/contextabc/?param=value')
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

    def test_resource_url_with_different_virtual_path(self):
        self.info['virtual_path'] = '/different_context/'
        context = DummyContext()
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/different_contextabc/')

    def test_resource_url_with_none_context(self):
        context = None
        with self.assertRaises(TypeError):
            resource_url(self.request, self.info)

    def test_resource_url_with_empty_info(self):
        context = DummyContext()
        with self.assertRaises(KeyError):
            resource_url(self.request, {})

    def test_resource_url_with_invalid_app_url(self):
        self.info['app_url'] = 'invalid_url'
        context = DummyContext()
        with self.assertRaises(ValueError):
            resource_url(self.request, self.info)
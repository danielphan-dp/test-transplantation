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

    def test_resource_url_valid(self):
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_invalid_virtual_path(self):
        self.info['virtual_path'] = '/invalid/'
        with self.assertRaises(KeyError):
            resource_url(self.request, self.info)

    def test_resource_url_invalid_physical_path(self):
        self.info['physical_path'] = '/invalid/'
        with self.assertRaises(KeyError):
            resource_url(self.request, self.info)

    def test_resource_url_missing_app_url(self):
        del self.info['app_url']
        with self.assertRaises(KeyError):
            resource_url(self.request, self.info)

    def test_resource_url_edge_case_empty_info(self):
        with self.assertRaises(KeyError):
            resource_url(self.request, {})

    def test_resource_url_edge_case_none_info(self):
        with self.assertRaises(TypeError):
            resource_url(self.request, None)

    def test_resource_url_edge_case_unexpected_info(self):
        self.info['unexpected_key'] = 'value'
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')
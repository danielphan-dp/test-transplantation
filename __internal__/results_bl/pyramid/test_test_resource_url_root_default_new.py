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

    def test_resource_url_missing_info(self):
        with self.assertRaises(KeyError):
            resource_url(self.request, {})

    def test_resource_url_different_app_url(self):
        self.info['app_url'] = 'http://another-example.com:1234'
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://another-example.com/contextabc/')

    def test_resource_url_edge_case_empty_info(self):
        self.info = {}
        with self.assertRaises(KeyError):
            resource_url(self.request, self.info)

    def test_resource_url_edge_case_none_request(self):
        with self.assertRaises(TypeError):
            resource_url(None, self.info)

    def test_resource_url_edge_case_none_info(self):
        with self.assertRaises(TypeError):
            resource_url(self.request, None)
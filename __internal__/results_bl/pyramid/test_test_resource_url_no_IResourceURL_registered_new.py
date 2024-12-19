import os
import unittest
from pyramid.testing import DummyRequest, DummyContext
from pyramid.url import resource_url

class TestResourceUrl(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.info = {
            'virtual_path': '/context/',
            'physical_path': '/context/',
            'app_url': 'http://example.com:5432'
        }

    def test_resource_url_valid(self):
        root = DummyContext()
        root.__name__ = 'context'
        root.__parent__ = None
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_no_virtual_path(self):
        self.info['virtual_path'] = None
        with self.assertRaises(KeyError):
            resource_url(self.request, self.info)

    def test_resource_url_no_physical_path(self):
        self.info['physical_path'] = None
        with self.assertRaises(KeyError):
            resource_url(self.request, self.info)

    def test_resource_url_no_app_url(self):
        self.info['app_url'] = None
        with self.assertRaises(KeyError):
            resource_url(self.request, self.info)

    def test_resource_url_empty_info(self):
        with self.assertRaises(KeyError):
            resource_url(self.request, {})

    def test_resource_url_invalid_request(self):
        invalid_request = object()
        with self.assertRaises(AssertionError):
            resource_url(invalid_request, self.info)
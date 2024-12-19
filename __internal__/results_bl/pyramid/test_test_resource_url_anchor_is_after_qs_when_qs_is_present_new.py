import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.url import resource_url

class TestResourceUrl(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.info = {
            'virtual_path': '/context/',
            'physical_path': '/context/',
            'app_url': 'http://example.com:5432'
        }

    def test_resource_url_basic(self):
        result = resource_url(self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_anchor(self):
        result = resource_url(self.request, self.info, anchor='d')
        self.assertEqual(result, 'http://example.com/contextabc/#d')

    def test_resource_url_with_query(self):
        result = resource_url(self.request, self.info, query={'b': 'c'})
        self.assertEqual(result, 'http://example.com/contextabc/?b=c')

    def test_resource_url_with_query_and_anchor(self):
        result = resource_url(self.request, self.info, query={'b': 'c'}, anchor='d')
        self.assertEqual(result, 'http://example.com/contextabc/?b=c#d')

    def test_resource_url_invalid_info(self):
        with self.assertRaises(KeyError):
            resource_url(self.request, {})

    def test_resource_url_missing_virtual_path(self):
        self.info.pop('virtual_path')
        with self.assertRaises(KeyError):
            resource_url(self.request, self.info)

    def test_resource_url_missing_physical_path(self):
        self.info.pop('physical_path')
        with self.assertRaises(KeyError):
            resource_url(self.request, self.info)

    def test_resource_url_missing_app_url(self):
        self.info.pop('app_url')
        with self.assertRaises(KeyError):
            resource_url(self.request, self.info)
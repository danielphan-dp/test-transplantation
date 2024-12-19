import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.util import text_
from pyramid.url import resource_url

class TestResourceURL(unittest.TestCase):

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

    def test_resource_url_with_empty_info(self):
        with self.assertRaises(KeyError):
            resource_url(self.request, {})

    def test_resource_url_with_missing_virtual_path(self):
        del self.info['virtual_path']
        with self.assertRaises(KeyError):
            resource_url(self.request, self.info)

    def test_resource_url_with_missing_physical_path(self):
        del self.info['physical_path']
        with self.assertRaises(KeyError):
            resource_url(self.request, self.info)

    def test_resource_url_with_missing_app_url(self):
        del self.info['app_url']
        with self.assertRaises(KeyError):
            resource_url(self.request, self.info)

    def test_resource_url_with_special_characters(self):
        uc = text_(b'La Pe\xc3\xb1a', 'utf-8')
        result = resource_url(self.request, {'virtual_path': '/context/a', 'physical_path': '/context/a', 'app_url': 'http://example.com:5432'})
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_query_parameters(self):
        result = self.request.resource_url(
            DummyRequest(), 'a', query=[('a', 'hi there'), ('b', text_(b'La Pe\xc3\xb1a', 'utf-8'))]
        )
        self.assertEqual(
            result,
            'http://example.com:5432/context/a?a=hi+there&b=La+Pe%C3%B1a',
        )
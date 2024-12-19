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
        info = self.info.copy()
        del info['virtual_path']
        with self.assertRaises(KeyError):
            resource_url(self.request, info)

    def test_resource_url_with_missing_physical_path(self):
        info = self.info.copy()
        del info['physical_path']
        with self.assertRaises(KeyError):
            resource_url(self.request, info)

    def test_resource_url_with_invalid_app_url(self):
        info = self.info.copy()
        info['app_url'] = 'invalid_url'
        with self.assertRaises(ValueError):
            resource_url(self.request, info)

    def test_resource_url_with_query_dict(self):
        uc = text_(b'La Pe\xc3\xb1a', 'utf-8')
        result = self.request.resource_url(DummyContext(), 'a', query={'a': uc})
        self.assertEqual(result, 'http://example.com:5432/context/a?a=La+Pe%C3%B1a')
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

    def test_resource_url_with_valid_context(self):
        context = DummyContext()
        result = resource_url(context, self.request, self.info)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_invalid_context(self):
        context = None
        with self.assertRaises(TypeError):
            resource_url(context, self.request, self.info)

    def test_resource_url_with_missing_info(self):
        context = DummyContext()
        with self.assertRaises(KeyError):
            resource_url(context, self.request, {})

    def test_resource_url_with_different_app_url(self):
        self.info['app_url'] = 'http://different.com:1234'
        context = DummyContext()
        result = resource_url(context, self.request, self.info)
        self.assertEqual(result, 'http://different.com/contextabc/')

    def test_resource_url_anchor_is_after_elements_when_no_qs(self):
        context = DummyContext()
        result = self.request.resource_url(context, 'a', anchor='b')
        self.assertEqual(result, 'http://example.com:5432/context/a#b')
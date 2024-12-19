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

    def test_resource_url_with_unicode_anchor(self):
        uc = text_(b'La Pe\xc3\xb1a', 'utf-8')
        result = resource_url(self.request, self.info, anchor=uc)
        self.assertEqual(result, 'http://example.com/contextabc/#La%20Pe%C3%B1a')

    def test_resource_url_with_empty_anchor(self):
        result = resource_url(self.request, self.info, anchor='')
        self.assertEqual(result, 'http://example.com/contextabc/#')

    def test_resource_url_with_none_anchor(self):
        result = resource_url(self.request, self.info, anchor=None)
        self.assertEqual(result, 'http://example.com/contextabc/')

    def test_resource_url_with_special_characters(self):
        uc = text_(b'Hello@World!', 'utf-8')
        result = resource_url(self.request, self.info, anchor=uc)
        self.assertEqual(result, 'http://example.com/contextabc/#Hello%40World%21')

    def test_resource_url_with_long_anchor(self):
        uc = text_(b'A' * 1000, 'utf-8')
        result = resource_url(self.request, self.info, anchor=uc)
        self.assertEqual(result, 'http://example.com/contextabc/#' + 'A%20' * 999 + 'A')

if __name__ == '__main__':
    unittest.main()
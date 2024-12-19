import unittest
from pyramid.request import Request
from pyramid.response import Response
from pyramid.testing import DummyRequest

class TestBlankMethod(unittest.TestCase):

    def test_blank_creates_request_with_valid_path(self):
        path = '/test/path'
        request = Request.blank(path)
        self.assertEqual(request.path, path)

    def test_blank_creates_request_with_empty_path(self):
        path = ''
        request = Request.blank(path)
        self.assertEqual(request.path, path)

    def test_blank_creates_request_with_none_path(self):
        path = None
        with self.assertRaises(TypeError):
            Request.blank(path)

    def test_blank_creates_request_with_special_characters(self):
        path = '/test/path/with/special/characters/!@#$%^&*()'
        request = Request.blank(path)
        self.assertEqual(request.path, path)

    def test_blank_creates_request_with_long_path(self):
        path = '/' + 'a' * 2048
        request = Request.blank(path)
        self.assertEqual(request.path, path)

    def test_blank_creates_request_with_query_string(self):
        path = '/test/path?query=string'
        request = Request.blank(path)
        self.assertEqual(request.path, '/test/path')
        self.assertEqual(request.query_string, 'query=string')
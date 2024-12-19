import unittest
from pyramid.testing import DummyRequest
from pyramid.httpexceptions import HTTPNotFound
from pyramid.request import Request

class TestBlankMethod(unittest.TestCase):

    def test_blank_creates_request_with_valid_path(self):
        path = '/valid/path'
        request = DummyRequest.blank(path)
        self.assertEqual(request.path, path)

    def test_blank_creates_request_with_empty_path(self):
        path = ''
        request = DummyRequest.blank(path)
        self.assertEqual(request.path, path)

    def test_blank_creates_request_with_none_path(self):
        path = None
        with self.assertRaises(TypeError):
            DummyRequest.blank(path)

    def test_blank_creates_request_with_special_characters(self):
        path = '/path/with/special/characters/!@#$%^&*()'
        request = DummyRequest.blank(path)
        self.assertEqual(request.path, path)

    def test_blank_creates_request_with_long_path(self):
        path = '/' + 'a' * 2048
        request = DummyRequest.blank(path)
        self.assertEqual(request.path, path)

    def test_blank_creates_request_with_query_string(self):
        path = '/path?query=string'
        request = DummyRequest.blank(path)
        self.assertEqual(request.path, '/path')
        self.assertEqual(request.query_string, 'query=string')
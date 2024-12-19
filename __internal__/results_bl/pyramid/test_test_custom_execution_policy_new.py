import unittest
from pyramid.request import Request

class TestRequestBlank(unittest.TestCase):

    def test_blank_with_valid_path(self):
        path = '/valid/path'
        req = Request.blank(path)
        self.assertEqual(req.path, path)

    def test_blank_with_empty_path(self):
        path = ''
        req = Request.blank(path)
        self.assertEqual(req.path, path)

    def test_blank_with_special_characters(self):
        path = '/path/with/special/characters/!@#$%^&*()'
        req = Request.blank(path)
        self.assertEqual(req.path, path)

    def test_blank_with_leading_slash(self):
        path = '/leading/slash'
        req = Request.blank(path)
        self.assertEqual(req.path, path)

    def test_blank_with_trailing_slash(self):
        path = '/trailing/slash/'
        req = Request.blank(path)
        self.assertEqual(req.path, path)

    def test_blank_with_multiple_slashes(self):
        path = '///multiple///slashes///'
        req = Request.blank(path)
        self.assertEqual(req.path, path)

    def test_blank_with_query_string(self):
        path = '/path?query=string'
        req = Request.blank(path)
        self.assertEqual(req.path, '/path')
        self.assertEqual(req.query_string, 'query=string')

    def test_blank_with_fragment(self):
        path = '/path#fragment'
        req = Request.blank(path)
        self.assertEqual(req.path, '/path')
        self.assertEqual(req.fragment, 'fragment')
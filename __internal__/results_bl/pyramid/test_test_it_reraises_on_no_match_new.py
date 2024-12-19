import unittest
from pyramid.request import Request

class TestBlankMethod(unittest.TestCase):

    def test_blank_creates_request_with_valid_path(self):
        path = '/valid/path'
        request = Request.blank(path)
        self.assertEqual(request.path, path)

    def test_blank_creates_request_with_empty_path(self):
        path = ''
        request = Request.blank(path)
        self.assertEqual(request.path, path)

    def test_blank_creates_request_with_special_characters(self):
        path = '/path/with/special/characters/!@#$%^&*()'
        request = Request.blank(path)
        self.assertEqual(request.path, path)

    def test_blank_creates_request_with_leading_slash(self):
        path = '/leading/slash'
        request = Request.blank(path)
        self.assertEqual(request.path, path)

    def test_blank_creates_request_with_trailing_slash(self):
        path = '/trailing/slash/'
        request = Request.blank(path)
        self.assertEqual(request.path, path)

    def test_blank_creates_request_with_none_path(self):
        path = None
        with self.assertRaises(TypeError):
            Request.blank(path)
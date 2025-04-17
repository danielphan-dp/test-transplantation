import unittest
from pyramid.request import Request
from pyramid.testing import DummyRequest

class TestBlankMethod(unittest.TestCase):
    def test_blank_creates_request_with_given_path(self):
        path = '/test/path'
        request = DummyRequest.blank(path)
        self.assertEqual(request.path, path)

    def test_blank_creates_request_with_root_path(self):
        path = '/'
        request = DummyRequest.blank(path)
        self.assertEqual(request.path, path)

    def test_blank_creates_request_with_empty_path(self):
        path = ''
        request = DummyRequest.blank(path)
        self.assertEqual(request.path, path)

    def test_blank_creates_request_with_special_characters(self):
        path = '/test/path/with/special/characters/!@#$%^&*()'
        request = DummyRequest.blank(path)
        self.assertEqual(request.path, path)

    def test_blank_creates_request_with_long_path(self):
        path = '/a' * 1000
        request = DummyRequest.blank(path)
        self.assertEqual(request.path, path)

if __name__ == '__main__':
    unittest.main()
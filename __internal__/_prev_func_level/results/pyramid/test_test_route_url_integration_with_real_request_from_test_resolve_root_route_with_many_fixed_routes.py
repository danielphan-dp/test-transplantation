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

    def test_blank_creates_request_with_invalid_path(self):
        path = 'invalid/path'
        request = DummyRequest.blank(path)
        self.assertEqual(request.path, path)

    def test_blank_creates_request_with_query_string(self):
        path = '/test/path?query=1'
        request = DummyRequest.blank(path)
        self.assertEqual(request.path, '/test/path')
        self.assertEqual(request.query_string, 'query=1')

if __name__ == '__main__':
    unittest.main()
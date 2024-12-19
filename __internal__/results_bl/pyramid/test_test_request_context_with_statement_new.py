import unittest
from pyramid.request import Request

class TestRequestBlankMethod(unittest.TestCase):

    def test_blank_with_valid_path(self):
        path = '/valid_path'
        req = Request.blank(path)
        self.assertEqual(req.path_info, path)

    def test_blank_with_empty_path(self):
        path = ''
        req = Request.blank(path)
        self.assertEqual(req.path_info, path)

    def test_blank_with_special_characters(self):
        path = '/path/with/special@chars!'
        req = Request.blank(path)
        self.assertEqual(req.path_info, path)

    def test_blank_with_leading_slash(self):
        path = '/leading_slash'
        req = Request.blank(path)
        self.assertEqual(req.path_info, path)

    def test_blank_with_trailing_slash(self):
        path = '/trailing_slash/'
        req = Request.blank(path)
        self.assertEqual(req.path_info, path)

    def test_blank_with_multiple_slashes(self):
        path = '///multiple///slashes///'
        req = Request.blank(path)
        self.assertEqual(req.path_info, path)

    def test_blank_with_query_string(self):
        path = '/path?query=string'
        req = Request.blank(path)
        self.assertEqual(req.path_info, path)
        self.assertEqual(req.query_string, 'query=string')

    def test_blank_with_non_ascii_characters(self):
        path = '/path/with/非ASCII字符'
        req = Request.blank(path)
        self.assertEqual(req.path_info, path)

if __name__ == '__main__':
    unittest.main()
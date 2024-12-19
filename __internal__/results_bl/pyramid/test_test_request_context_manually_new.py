import unittest
from pyramid.request import Request

class TestRequestBlankMethod(unittest.TestCase):

    def test_blank_method_with_valid_path(self):
        path = '/valid_path'
        req = Request.blank(path)
        self.assertEqual(req.path_info, path)

    def test_blank_method_with_empty_path(self):
        path = ''
        req = Request.blank(path)
        self.assertEqual(req.path_info, path)

    def test_blank_method_with_none_path(self):
        path = None
        with self.assertRaises(TypeError):
            Request.blank(path)

    def test_blank_method_with_special_characters(self):
        path = '/path/with/special/characters/!@#$%^&*()'
        req = Request.blank(path)
        self.assertEqual(req.path_info, path)

    def test_blank_method_with_long_path(self):
        path = '/' + 'a' * 2048  # Assuming a long path
        req = Request.blank(path)
        self.assertEqual(req.path_info, path)

    def test_blank_method_with_query_string(self):
        path = '/path?query=string'
        req = Request.blank(path)
        self.assertEqual(req.path_info, '/path')
        self.assertEqual(req.query_string, 'query=string')

if __name__ == '__main__':
    unittest.main()
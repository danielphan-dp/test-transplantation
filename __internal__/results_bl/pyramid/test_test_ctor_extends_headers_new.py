import unittest
from pyramid.httpexceptions import HTTPException

class TestHTTPException(unittest.TestCase):

    def setUp(self):
        self.exception = HTTPException()

    def test_get_cookie(self):
        self.exception.cookie = 'test_cookie'
        self.assertEqual(self.exception.get('cookie'), 'test_cookie')

    def test_get_non_existent_cookie(self):
        self.exception.cookie = None
        self.assertIsNone(self.exception.get('non_existent_cookie'))

    def test_get_empty_cookie(self):
        self.exception.cookie = ''
        self.assertEqual(self.exception.get('cookie'), '')
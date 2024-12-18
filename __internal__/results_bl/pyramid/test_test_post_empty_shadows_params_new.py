import unittest
from pyramid.testing import DummyRequest

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.cookie = {'session_id': '12345'}

    def test_get_existing_cookie(self):
        result = self.request.get('session_id')
        self.assertEqual(result, {'session_id': '12345'})

    def test_get_non_existing_cookie(self):
        result = self.request.get('non_existing_cookie')
        self.assertEqual(result, None)

    def test_get_empty_cookie(self):
        self.request.cookie = {}
        result = self.request.get('session_id')
        self.assertEqual(result, {})
import unittest
from pyramid.testing import DummySession

class TestSessionGetMethod(unittest.TestCase):

    def setUp(self):
        self.session = DummySession()

    def test_get_existing_cookie(self):
        self.session.cookie = 'test_cookie'
        result = self.session.get('cookie')
        self.assertEqual(result, 'test_cookie')

    def test_get_non_existing_cookie(self):
        result = self.session.get('non_existing_cookie')
        self.assertIsNone(result)

    def test_get_empty_cookie(self):
        self.session.cookie = ''
        result = self.session.get('cookie')
        self.assertEqual(result, '')

    def test_get_with_none_cookie(self):
        self.session.cookie = None
        result = self.session.get('cookie')
        self.assertIsNone(result)

    def test_get_after_setting_cookie(self):
        self.session.cookie = 'new_cookie'
        result = self.session.get('cookie')
        self.assertEqual(result, 'new_cookie')

if __name__ == '__main__':
    unittest.main()
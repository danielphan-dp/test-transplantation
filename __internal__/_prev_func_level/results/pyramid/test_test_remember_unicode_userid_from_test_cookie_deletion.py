import unittest
from pyramid.util import text_

class TestCookieValue(unittest.TestCase):

    def setUp(self):
        self.helper = self._makeOne('secret')

    def test_cookie_value_with_valid_cookie(self):
        cookie = 'key1=value1/key2=value2'
        result = self.helper._cookieValue(cookie)
        self.assertEqual(result['key1'], 'value1')
        self.assertEqual(result['key2'], 'value2')

    def test_cookie_value_with_empty_cookie(self):
        cookie = ''
        result = self.helper._cookieValue(cookie)
        self.assertEqual(result, {})

    def test_cookie_value_with_invalid_format(self):
        cookie = 'key1=value1/key2'
        with self.assertRaises(ValueError):
            self.helper._cookieValue(cookie)

    def test_cookie_value_with_special_characters(self):
        cookie = 'key1=val%20ue1/key2=val%40ue2'
        result = self.helper._cookieValue(cookie)
        self.assertEqual(result['key1'], 'val ue1')
        self.assertEqual(result['key2'], 'val@ue2')

    def test_cookie_value_with_unicode(self):
        cookie = 'userid=%C2%A9/user_data=userid_type:b64unicode'
        result = self.helper._cookieValue(cookie)
        self.assertEqual(result['userid'], text_(b'\xc2\xa9'))
        self.assertEqual(result['user_data'], 'userid_type:b64unicode')
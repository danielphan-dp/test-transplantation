import unittest
from http.cookies import SimpleCookie
from aiohttp import CookieJar
from yarl import URL

class TestCookieJar(unittest.TestCase):
    def setUp(self):
        self.jar = CookieJar()

    def test_empty_url(self):
        cookies_sent, cookies_received = self.jar.request_reply_with_same_url("")
        self.assertEqual(cookies_sent, {})
        self.assertEqual(cookies_received, SimpleCookie())

    def test_no_cookies_sent(self):
        self.jar.update_cookies({})
        cookies_sent, cookies_received = self.jar.request_reply_with_same_url("http://no-cookies.com/")
        self.assertEqual(cookies_sent, {})
        self.assertEqual(cookies_received, SimpleCookie())

    def test_special_characters_in_url(self):
        self.jar.update_cookies({'special-cookie': 'value'})
        cookies_sent, cookies_received = self.jar.request_reply_with_same_url("http://special-characters.com/?query=space%20and%20%23")
        self.assertIn('special-cookie', cookies_sent)

    def test_multiple_cookies_received(self):
        self.jar.update_cookies({'cookie1': 'value1', 'cookie2': 'value2'})
        cookies_sent, cookies_received = self.jar.request_reply_with_same_url("http://multiple-cookies.com/")
        self.assertEqual(set(cookies_received.keys()), {'cookie1', 'cookie2'})

    def test_invalid_cookie_format(self):
        self.jar.update_cookies({'invalid-cookie': 'value; HttpOnly; Path=/'})
        cookies_sent, cookies_received = self.jar.request_reply_with_same_url("http://invalid-format.com/")
        self.assertIn('invalid-cookie', cookies_sent)

    def test_cookie_with_no_value(self):
        self.jar.update_cookies({'empty-cookie': ''})
        cookies_sent, cookies_received = self.jar.request_reply_with_same_url("http://empty-value.com/")
        self.assertEqual(cookies_sent['empty-cookie'].value, '')

if __name__ == '__main__':
    unittest.main()
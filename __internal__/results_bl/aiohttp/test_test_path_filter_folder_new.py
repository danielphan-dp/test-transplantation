import unittest
from http.cookies import SimpleCookie
from aiohttp import CookieJar

class TestRequestReplyWithSameUrl(unittest.TestCase):
    def setUp(self):
        self.cookie_jar = CookieJar()
        self.cookies_to_send = SimpleCookie()
        self.cookies_to_receive = SimpleCookie()
        self.cookies_to_send['shared-cookie'] = 'value1'
        self.cookies_to_send['no-path-cookie'] = 'value2'
        self.cookies_to_receive['path1-cookie'] = 'value3'
        self.cookies_to_receive['path2-cookie'] = 'value4'
        self.cookie_jar.update_cookies(self.cookies_to_send)

    def test_empty_url(self):
        cookies_sent, cookies_received = self.cookie_jar.request_reply_with_same_url("")
        self.assertEqual(cookies_sent, SimpleCookie())
        self.assertEqual(cookies_received, SimpleCookie())

    def test_invalid_url(self):
        with self.assertRaises(ValueError):
            self.cookie_jar.request_reply_with_same_url("invalid-url")

    def test_no_cookies_sent(self):
        self.cookie_jar.clear()
        cookies_sent, cookies_received = self.cookie_jar.request_reply_with_same_url("http://pathtest.com/one/")
        self.assertEqual(cookies_sent, SimpleCookie())

    def test_cookies_received(self):
        cookies_sent, cookies_received = self.cookie_jar.request_reply_with_same_url("http://pathtest.com/one/")
        self.assertEqual(
            set(cookies_received.keys()),
            {"path1-cookie", "path2-cookie"},
        )

    def test_multiple_calls(self):
        for _ in range(5):
            cookies_sent, cookies_received = self.cookie_jar.request_reply_with_same_url("http://pathtest.com/one/")
        self.assertEqual(
            set(cookies_sent.keys()),
            {"shared-cookie", "no-path-cookie", "path1-cookie", "path2-cookie"},
        )
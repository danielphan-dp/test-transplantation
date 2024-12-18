import unittest
from http.cookies import SimpleCookie
from aiohttp import CookieJar
from yarl import URL

class TestCookieJar(unittest.TestCase):
    def setUp(self):
        self.jar = CookieJar()
        self.jar.update_cookies({'shared-cookie': 'value1', 'no-path-cookie': 'value2', 'path1-cookie': 'value3'})
        self.cookies_to_send = {'shared-cookie': 'value1', 'no-path-cookie': 'value2'}
        self.cookies_to_receive = {'path1-cookie': 'value3'}

    def request_reply_with_same_url(self, url: str):
        self.jar.update_cookies(self.cookies_to_send)
        cookies_sent = self.jar.filter_cookies(URL(url))
        self.jar.clear()
        self.jar.update_cookies(self.cookies_to_receive, URL(url))
        cookies_received = SimpleCookie()
        for cookie in self.jar:
            dict.__setitem__(cookies_received, cookie.key, cookie)
        self.jar.clear()
        return (cookies_sent, cookies_received)

    def test_empty_url(self):
        cookies_sent, cookies_received = self.request_reply_with_same_url("")
        self.assertEqual(cookies_sent, {})
        self.assertEqual(cookies_received, SimpleCookie())

    def test_invalid_url(self):
        with self.assertRaises(ValueError):
            self.request_reply_with_same_url("invalid-url")

    def test_url_with_query_params(self):
        cookies_sent, _ = self.request_reply_with_same_url("http://pathtest.com/?query=1")
        self.assertEqual(
            set(cookies_sent.keys()),
            {"shared-cookie", "no-path-cookie", "path1-cookie"},
        )

    def test_url_with_different_path(self):
        cookies_sent, _ = self.request_reply_with_same_url("http://pathtest.com/path2/")
        self.assertEqual(
            set(cookies_sent.keys()),
            {"shared-cookie", "no-path-cookie"},
        )

    def test_no_cookies_sent(self):
        self.jar.clear()
        cookies_sent, _ = self.request_reply_with_same_url("http://pathtest.com/")
        self.assertEqual(cookies_sent, {})

    def test_multiple_cookies_received(self):
        self.jar.update_cookies({'cookie1': 'value1', 'cookie2': 'value2'})
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://pathtest.com/")
        self.assertEqual(
            set(cookies_received.keys()),
            {"cookie1", "cookie2"},
        )
import unittest
from http.cookies import SimpleCookie
from aiohttp import CookieJar
from yarl import URL

class TestCookieJar(unittest.TestCase):
    def setUp(self):
        self.jar = CookieJar()
        self.cookies_to_send = SimpleCookie("shared-cookie=value; no-path-cookie=value; path1-cookie=value;")
        self.cookies_to_receive = SimpleCookie("received-cookie=value; another-cookie=value;")
    
    def test_request_reply_with_same_url(self):
        self.jar.update_cookies(self.cookies_to_send, URL("http://example.com/"))
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://example.com/")
        
        self.assertEqual(
            set(cookies_sent.keys()),
            {"shared-cookie", "no-path-cookie", "path1-cookie"},
        )
        self.assertEqual(
            set(cookies_received.keys()),
            {"received-cookie", "another-cookie"},
        )

    def test_request_reply_with_different_url(self):
        self.jar.update_cookies(self.cookies_to_send, URL("http://example.com/"))
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://different.com/")
        
        self.assertEqual(
            set(cookies_sent.keys()),
            {"shared-cookie", "no-path-cookie", "path1-cookie"},
        )
        self.assertEqual(
            set(cookies_received.keys()),
            set(),
        )

    def test_request_reply_with_empty_cookies(self):
        self.jar.clear()
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://example.com/")
        
        self.assertEqual(
            set(cookies_sent.keys()),
            set(),
        )
        self.assertEqual(
            set(cookies_received.keys()),
            set(),
        )

    def test_request_reply_with_invalid_url(self):
        with self.assertRaises(ValueError):
            self.request_reply_with_same_url("invalid-url")

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
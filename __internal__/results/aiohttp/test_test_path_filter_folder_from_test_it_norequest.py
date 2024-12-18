import unittest
from http.cookies import SimpleCookie
from aiohttp import CookieJar
from yarl import URL

class TestCookieJar(unittest.TestCase):
    def setUp(self):
        self.jar = CookieJar()
        self.cookies_to_send = SimpleCookie("shared-cookie=value; no-path-cookie=value; path1-cookie=value; path2-cookie=value;")
        self.cookies_to_receive = SimpleCookie("unconstrained-cookie=first; domain-cookie=second; subdomain1-cookie=third; subdomain2-cookie=fourth; dotted-domain-cookie=fifth; different-domain-cookie=sixth; no-path-cookie=seventh; path-cookie=eighth; wrong-path-cookie=ninth;")
        self.jar.update_cookies(self.cookies_to_send)

    def test_request_reply_with_same_url(self):
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://pathtest.com/one/")
        
        self.assertEqual(
            set(cookies_sent.keys()),
            {"shared-cookie", "no-path-cookie", "path1-cookie", "path2-cookie"},
        )
        
        self.assertEqual(
            set(cookies_received.keys()),
            {"unconstrained-cookie", "domain-cookie", "subdomain1-cookie", "subdomain2-cookie", "dotted-domain-cookie", "different-domain-cookie", "no-path-cookie", "path-cookie", "wrong-path-cookie"},
        )

    def test_request_reply_with_different_url(self):
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://example.com/")
        
        self.assertEqual(
            set(cookies_sent.keys()),
            {"shared-cookie", "no-path-cookie", "path1-cookie", "path2-cookie"},
        )
        
        self.assertNotIn("path-cookie", cookies_received.keys())

    def test_request_reply_with_empty_url(self):
        cookies_sent, cookies_received = self.request_reply_with_same_url("")
        
        self.assertEqual(cookies_sent, SimpleCookie())
        self.assertEqual(cookies_received, SimpleCookie())

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
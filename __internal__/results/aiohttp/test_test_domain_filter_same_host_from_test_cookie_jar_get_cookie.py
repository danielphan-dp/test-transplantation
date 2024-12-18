import unittest
from http.cookies import SimpleCookie
from aiohttp import CookieJar
from yarl import URL

class TestCookieJar(unittest.TestCase):
    def setUp(self):
        self.jar = CookieJar()
        self.cookies_to_send = SimpleCookie("shared-cookie=value; domain-cookie=value; dotted-domain-cookie=value")
        self.cookies_to_receive = SimpleCookie(
            "unconstrained-cookie=first; domain-cookie=second; dotted-domain-cookie=third"
        )

    def test_request_reply_with_same_url(self):
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://example.com/")
        
        self.assertEqual(
            set(cookies_sent.keys()),
            {"shared-cookie", "domain-cookie", "dotted-domain-cookie"},
        )

        self.assertEqual(
            set(cookies_received.keys()),
            {"unconstrained-cookie", "domain-cookie", "dotted-domain-cookie"},
        )

    def test_request_reply_with_different_url(self):
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://different.com/")
        
        self.assertEqual(
            set(cookies_sent.keys()),
            set(),  # Expecting no cookies sent for a different domain
        )

        self.assertEqual(
            set(cookies_received.keys()),
            set(),  # Expecting no cookies received for a different domain
        )

    def test_request_reply_with_empty_cookies(self):
        self.jar.clear()
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://example.com/")
        
        self.assertEqual(
            set(cookies_sent.keys()),
            set(),  # Expecting no cookies sent when jar is empty
        )

        self.assertEqual(
            set(cookies_received.keys()),
            set(),  # Expecting no cookies received when jar is empty
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
import unittest
from http.cookies import SimpleCookie
from aiohttp import CookieJar
from yarl import URL

class TestCookieJar(unittest.TestCase):
    def setUp(self):
        self.jar = CookieJar()
        self.cookies_to_send = SimpleCookie("shared-cookie=value; domain-cookie=domain.com;")
        self.cookies_to_receive = SimpleCookie(
            "unconstrained-cookie=first; domain-cookie=second; dotted-domain-cookie=third;"
        )

    def test_request_reply_with_same_url(self):
        url = "http://example.com/"
        cookies_sent, cookies_received = self.request_reply_with_same_url(url)

        self.assertEqual(
            set(cookies_sent.keys()),
            {"shared-cookie", "domain-cookie"},
        )

        self.assertEqual(
            set(cookies_received.keys()),
            {"unconstrained-cookie", "domain-cookie"},
        )

    def test_request_reply_with_different_url(self):
        url = "http://different.example.com/"
        cookies_sent, cookies_received = self.request_reply_with_same_url(url)

        self.assertEqual(
            set(cookies_sent.keys()),
            {"shared-cookie", "domain-cookie"},
        )

        self.assertEqual(
            set(cookies_received.keys()),
            {"unconstrained-cookie", "domain-cookie"},
        )

    def test_request_reply_with_no_cookies(self):
        self.jar.clear()
        url = "http://example.com/"
        cookies_sent, cookies_received = self.request_reply_with_same_url(url)

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
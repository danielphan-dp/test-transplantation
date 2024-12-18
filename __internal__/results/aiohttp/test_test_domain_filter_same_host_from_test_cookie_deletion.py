import unittest
from http.cookies import SimpleCookie
from aiohttp import CookieJar
from yarl import URL

class TestCookieJar(unittest.TestCase):
    def setUp(self):
        self.jar = CookieJar()
        self.cookies_to_send = SimpleCookie(
            "shared-cookie=value1; domain-cookie=value2; dotted-domain-cookie=value3"
        )
        self.cookies_to_receive = SimpleCookie(
            "unconstrained-cookie=value4; domain-cookie=value5; dotted-domain-cookie=value6"
        )

    def test_request_reply_with_same_url(self):
        url = "http://example.com/"
        cookies_sent, cookies_received = self.request_reply_with_same_url(url)

        self.assertEqual(
            set(cookies_sent.keys()),
            {"shared-cookie", "domain-cookie", "dotted-domain-cookie"},
        )

        self.assertEqual(
            set(cookies_received.keys()),
            {"unconstrained-cookie", "domain-cookie", "dotted-domain-cookie"},
        )

    def test_request_reply_with_different_url(self):
        url = "http://another-example.com/"
        cookies_sent, cookies_received = self.request_reply_with_same_url(url)

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
        url = "http://example.com/"
        cookies_sent, cookies_received = self.request_reply_with_same_url(url)

        self.assertEqual(
            set(cookies_sent.keys()),
            set(),  # Expecting no cookies sent
        )

        self.assertEqual(
            set(cookies_received.keys()),
            set(),  # Expecting no cookies received
        )

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
import unittest
from http.cookies import SimpleCookie
from aiohttp import CookieJar
from yarl import URL

class TestCookieJar(unittest.TestCase):
    def setUp(self):
        self.jar = CookieJar()
        self.cookies_to_send = SimpleCookie("shared-cookie=value; secure-cookie=secure_value;")
        self.cookies_to_receive = SimpleCookie("shared-cookie=first; secure-cookie=second;")
        self.jar.update_cookies(self.cookies_to_send)

    def test_request_reply_with_same_url(self):
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://secure.com/")
        self.assertEqual(set(cookies_sent.keys()), {"shared-cookie"})
        self.assertEqual(cookies_received["shared-cookie"].value, "first")
        self.assertNotIn("secure-cookie", cookies_received)

        cookies_sent, cookies_received = self.request_reply_with_same_url("https://secure.com/")
        self.assertEqual(set(cookies_sent.keys()), {"shared-cookie", "secure-cookie"})
        self.assertEqual(cookies_received["secure-cookie"].value, "second")

    def test_request_reply_with_different_domains(self):
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://example.com/")
        self.assertEqual(set(cookies_sent.keys()), {"shared-cookie"})
        self.assertEqual(cookies_received["shared-cookie"].value, "first")

        cookies_sent, cookies_received = self.request_reply_with_same_url("http://different.com/")
        self.assertEqual(set(cookies_sent.keys()), {"shared-cookie"})
        self.assertEqual(cookies_received["shared-cookie"].value, "first")

    def test_request_reply_with_no_cookies(self):
        self.jar.clear()
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://empty.com/")
        self.assertEqual(set(cookies_sent.keys()), set())
        self.assertEqual(set(cookies_received.keys()), set())

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
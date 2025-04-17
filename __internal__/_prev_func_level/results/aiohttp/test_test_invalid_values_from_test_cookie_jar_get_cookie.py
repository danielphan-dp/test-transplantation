import unittest
from http.cookies import SimpleCookie
from aiohttp import CookieJar
from yarl import URL

class TestCookieJar(unittest.TestCase):
    def setUp(self):
        self.jar = CookieJar()
        self.cookies_to_send = SimpleCookie("shared-cookie=value; invalid-max-age-cookie=invalid; invalid-expires-cookie=invalid")
        self.cookies_to_receive = SimpleCookie("valid-cookie=valid; another-cookie=another")

    def test_request_reply_with_same_url_valid_cookies(self):
        self.jar.update_cookies(self.cookies_to_send)
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://example.com/")
        
        self.assertEqual(set(cookies_sent.keys()), {"shared-cookie", "invalid-max-age-cookie", "invalid-expires-cookie"})
        self.assertEqual(cookies_sent["shared-cookie"].value, "value")
        self.assertEqual(cookies_received["valid-cookie"].value, "valid")
        self.assertEqual(cookies_received["another-cookie"].value, "another")

    def test_request_reply_with_same_url_empty_cookies(self):
        self.jar.clear()
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://empty.com/")
        
        self.assertEqual(cookies_sent, SimpleCookie())
        self.assertEqual(cookies_received, SimpleCookie())

    def test_request_reply_with_same_url_invalid_url(self):
        with self.assertRaises(ValueError):
            self.request_reply_with_same_url("invalid-url")

    def test_request_reply_with_same_url_different_domains(self):
        self.jar.update_cookies(self.cookies_to_send)
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://different.com/")
        
        self.assertEqual(set(cookies_sent.keys()), {"shared-cookie", "invalid-max-age-cookie", "invalid-expires-cookie"})
        self.assertNotIn("valid-cookie", cookies_received)

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
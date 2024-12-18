import unittest
from http.cookies import SimpleCookie
from aiohttp import CookieJar
from yarl import URL

class TestCookieJar(unittest.TestCase):
    def setUp(self):
        self.jar = CookieJar()
        self.cookies_to_send = SimpleCookie("shared-cookie=value; invalid-max-age-cookie=invalid; invalid-expires-cookie=invalid")
        self.cookies_to_receive = SimpleCookie("valid-cookie=valid; invalid-cookie=invalid")

    def test_valid_cookie_reception(self):
        self.jar.update_cookies(self.cookies_to_send)
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://example.com/")
        
        self.assertIn("shared-cookie", cookies_sent.keys())
        self.assertEqual(cookies_sent["shared-cookie"].value, "value")
        self.assertIn("valid-cookie", cookies_received.keys())
        self.assertEqual(cookies_received["valid-cookie"].value, "valid")

    def test_invalid_cookie_reception(self):
        self.jar.update_cookies(self.cookies_to_send)
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://example.com/")
        
        self.assertIn("invalid-max-age-cookie", cookies_sent.keys())
        self.assertEqual(cookies_sent["invalid-max-age-cookie"]["max-age"], "")
        self.assertIn("invalid-expires-cookie", cookies_sent.keys())
        self.assertEqual(cookies_sent["invalid-expires-cookie"]["expires"], "")

    def test_no_cookies_sent(self):
        self.jar.clear()
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://example.com/")
        
        self.assertEqual(len(cookies_sent), 0)
        self.assertEqual(len(cookies_received), 0)

    def test_multiple_cookies(self):
        self.jar.update_cookies(self.cookies_to_send)
        self.jar.update_cookies(SimpleCookie("another-cookie=another-value"))
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://example.com/")
        
        self.assertIn("another-cookie", cookies_sent.keys())
        self.assertEqual(cookies_sent["another-cookie"].value, "another-value")

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
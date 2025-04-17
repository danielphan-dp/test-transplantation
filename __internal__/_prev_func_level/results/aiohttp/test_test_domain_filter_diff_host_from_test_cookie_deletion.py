import unittest
from http.cookies import SimpleCookie
from aiohttp import CookieJar
from yarl import URL

class TestCookieJar(unittest.TestCase):
    def setUp(self):
        self.jar = CookieJar()
        self.cookies_to_send = SimpleCookie("shared-cookie=value; different-domain-cookie=value;")
        self.cookies_to_receive = SimpleCookie(
            "unconstrained-cookie=first; different-domain-cookie=sixth; Path=/; Domain=different.org;"
        )
        self.jar.update_cookies(self.cookies_to_send)

    def test_request_reply_with_same_url(self):
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://different.org/")
        
        self.assertEqual(set(cookies_sent.keys()), {"shared-cookie", "different-domain-cookie"})
        self.assertEqual(set(cookies_received.keys()), {"unconstrained-cookie", "different-domain-cookie"})

    def test_request_reply_with_empty_cookies(self):
        self.jar.clear()
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://empty.org/")
        
        self.assertEqual(set(cookies_sent.keys()), set())
        self.assertEqual(set(cookies_received.keys()), set())

    def test_request_reply_with_no_matching_domain(self):
        self.jar.update_cookies(SimpleCookie("non-matching-cookie=value;"))
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://unmatched.org/")
        
        self.assertEqual(set(cookies_sent.keys()), {"non-matching-cookie"})
        self.assertEqual(set(cookies_received.keys()), set())

    def test_request_reply_with_multiple_domains(self):
        self.jar.update_cookies(SimpleCookie("shared-cookie=value; domain-cookie=value;"))
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://example.com/")
        
        self.assertEqual(set(cookies_sent.keys()), {"shared-cookie", "domain-cookie"})
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
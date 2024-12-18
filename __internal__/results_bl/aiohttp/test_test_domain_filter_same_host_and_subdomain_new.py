import unittest
from http.cookies import SimpleCookie
from aiohttp import CookieJar
from yarl import URL

class TestCookieJar(unittest.TestCase):
    def setUp(self):
        self.jar = CookieJar()
        self.cookies_to_send = SimpleCookie()
        self.cookies_to_receive = SimpleCookie()

    def test_empty_cookies(self):
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://empty.example.com/")
        self.assertEqual(cookies_sent, {})
        self.assertEqual(cookies_received, {})

    def test_no_matching_domain(self):
        self.cookies_to_send["test-cookie"] = "value"
        self.cookies_to_receive["unrelated-cookie"] = "value"
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://no-match.example.com/")
        self.assertEqual(set(cookies_sent.keys()), {"test-cookie"})
        self.assertEqual(set(cookies_received.keys()), set())

    def test_subdomain_only_cookies(self):
        self.cookies_to_send["subdomain-cookie"] = "value"
        self.cookies_to_receive["subdomain1-cookie"] = "value"
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://subdomain.example.com/")
        self.assertEqual(set(cookies_sent.keys()), {"subdomain-cookie"})
        self.assertEqual(set(cookies_received.keys()), {"subdomain1-cookie"})

    def test_different_path_cookies(self):
        self.cookies_to_send["path-cookie"] = "value"
        self.cookies_to_receive["path-restricted-cookie"] = "value"
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://path.example.com/some/path/")
        self.assertEqual(set(cookies_sent.keys()), {"path-cookie"})
        self.assertEqual(set(cookies_received.keys()), {"path-restricted-cookie"})

    def test_cookie_expiration(self):
        self.cookies_to_send["expired-cookie"] = "value"
        self.cookies_to_send["valid-cookie"] = "value"
        self.cookies_to_receive["received-cookie"] = "value"
        # Simulate expiration logic here if applicable
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://expire.example.com/")
        self.assertEqual(set(cookies_sent.keys()), {"valid-cookie"})
        self.assertEqual(set(cookies_received.keys()), {"received-cookie"})
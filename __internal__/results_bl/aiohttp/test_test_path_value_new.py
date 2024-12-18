import unittest
from http.cookies import SimpleCookie
from aiohttp import CookieJar

class TestCookieJar(unittest.TestCase):
    def setUp(self):
        self.jar = CookieJar()
        self.cookies_to_send = SimpleCookie()
        self.cookies_to_receive = SimpleCookie()

    def test_empty_cookies(self):
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://emptycookies.com/")
        self.assertEqual(cookies_sent, SimpleCookie())
        self.assertEqual(cookies_received, SimpleCookie())

    def test_single_cookie(self):
        self.cookies_to_send["test-cookie"] = "test-value"
        self.cookies_to_receive["received-cookie"] = "received-value"
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://singlecookie.com/")
        self.assertEqual(set(cookies_sent.keys()), {"test-cookie"})
        self.assertEqual(set(cookies_received.keys()), {"received-cookie"})

    def test_multiple_cookies(self):
        self.cookies_to_send["cookie1"] = "value1"
        self.cookies_to_send["cookie2"] = "value2"
        self.cookies_to_receive["cookie3"] = "value3"
        self.cookies_to_receive["cookie4"] = "value4"
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://multiplecookies.com/")
        self.assertEqual(set(cookies_sent.keys()), {"cookie1", "cookie2"})
        self.assertEqual(set(cookies_received.keys()), {"cookie3", "cookie4"})

    def test_cookie_with_different_paths(self):
        self.cookies_to_send["path-cookie"] = "value"
        self.cookies_to_receive["no-path-cookie"] = "value"
        self.cookies_to_receive["wrong-path-cookie"] = "value"
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://pathcookies.com/")
        self.assertEqual(set(cookies_received.keys()), {"no-path-cookie", "wrong-path-cookie", "path-cookie"})

    def test_cookie_with_expiration(self):
        self.cookies_to_send["expiring-cookie"] = "value"
        self.cookies_to_receive["expired-cookie"] = "value"
        # Simulate expiration logic if applicable
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://expiringcookies.com/")
        self.assertIn("expiring-cookie", cookies_sent)
        self.assertNotIn("expired-cookie", cookies_received)

    def test_invalid_url(self):
        with self.assertRaises(ValueError):
            self.request_reply_with_same_url("invalid-url")

    def request_reply_with_same_url(self, url: str) -> Tuple['BaseCookie[str]', SimpleCookie]:
        self.jar.update_cookies(self.cookies_to_send)
        cookies_sent = self.jar.filter_cookies(URL(url))
        self.jar.clear()
        self.jar.update_cookies(self.cookies_to_receive, URL(url))
        cookies_received = SimpleCookie()
        for cookie in self.jar:
            dict.__setitem__(cookies_received, cookie.key, cookie)
        self.jar.clear()
        return (cookies_sent, cookies_received)
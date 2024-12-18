import unittest
from http.cookies import SimpleCookie
from aiohttp import CookieJar
from yarl import URL

class TestCookieJar(unittest.TestCase):
    def setUp(self):
        self.jar = CookieJar()
        self.cookies_to_send = SimpleCookie()
        self.cookies_to_receive = SimpleCookie()

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

    def test_no_cookies_sent_or_received(self):
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://emptycookies.com/")
        self.assertEqual(len(cookies_sent), 0)
        self.assertEqual(len(cookies_received), 0)

    def test_only_cookies_sent(self):
        self.cookies_to_send["test-cookie"] = "test-value"
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://test.com/")
        self.assertEqual(set(cookies_sent.keys()), {"test-cookie"})
        self.assertEqual(len(cookies_received), 0)

    def test_only_cookies_received(self):
        self.cookies_to_receive["received-cookie"] = "received-value"
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://test.com/")
        self.assertEqual(len(cookies_sent), 0)
        self.assertEqual(set(cookies_received.keys()), {"received-cookie"})

    def test_cookies_sent_and_received(self):
        self.cookies_to_send["sent-cookie"] = "sent-value"
        self.cookies_to_receive["received-cookie"] = "received-value"
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://test.com/")
        self.assertEqual(set(cookies_sent.keys()), {"sent-cookie"})
        self.assertEqual(set(cookies_received.keys()), {"received-cookie"})

    def test_path_filter_with_different_url(self):
        self.cookies_to_send["shared-cookie"] = "value1"
        self.cookies_to_send["no-path-cookie"] = "value2"
        self.cookies_to_send["path1-cookie"] = "value3"
        self.cookies_to_receive["received-cookie"] = "value4"
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://pathtest.com/another/")
        self.assertEqual(set(cookies_sent.keys()), {"shared-cookie", "no-path-cookie", "path1-cookie"})
        self.assertEqual(len(cookies_received), 0)
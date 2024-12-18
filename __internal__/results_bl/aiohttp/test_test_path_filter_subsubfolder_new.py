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

    def test_empty_cookies(self):
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://emptycookies.com/")
        self.assertEqual(len(cookies_sent), 0)
        self.assertEqual(len(cookies_received), 0)

    def test_no_matching_path(self):
        self.cookies_to_send["test-cookie"] = "value"
        self.cookies_to_send["test-cookie"]["path"] = "/differentpath"
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://pathtest.com/one/two/three/")
        self.assertEqual(set(cookies_sent.keys()), set())

    def test_single_cookie_sent(self):
        self.cookies_to_send["single-cookie"] = "value"
        self.cookies_to_send["single-cookie"]["path"] = "/one/two/three/"
        cookies_sent, _ = self.request_reply_with_same_url("http://pathtest.com/one/two/three/")
        self.assertEqual(set(cookies_sent.keys()), {"single-cookie"})

    def test_multiple_cookies_received(self):
        self.cookies_to_receive["received-cookie1"] = "value1"
        self.cookies_to_receive["received-cookie2"] = "value2"
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://pathtest.com/one/two/three/")
        self.assertEqual(set(cookies_received.keys()), {"received-cookie1", "received-cookie2"})

    def test_path_specific_cookies(self):
        self.cookies_to_send["path-cookie"] = "value"
        self.cookies_to_send["path-cookie"]["path"] = "/one/two/"
        self.cookies_to_send["other-cookie"] = "value"
        self.cookies_to_send["other-cookie"]["path"] = "/"
        cookies_sent, _ = self.request_reply_with_same_url("http://pathtest.com/one/two/three/")
        self.assertEqual(set(cookies_sent.keys()), {"path-cookie", "other-cookie"})
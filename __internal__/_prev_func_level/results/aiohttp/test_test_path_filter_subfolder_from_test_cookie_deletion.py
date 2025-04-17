import unittest
from http.cookies import SimpleCookie
from aiohttp import CookieJar
from yarl import URL

class TestCookieJar(unittest.TestCase):
    def setUp(self):
        self.jar = CookieJar()
        self.cookies_to_send = SimpleCookie("shared-cookie=value; Path=/;")
        self.cookies_to_receive = SimpleCookie(
            "unconstrained-cookie=first; Path=/; "
            "domain-cookie=second; Domain=example.com; Path=/; "
            "subdomain1-cookie=third; Domain=test1.example.com; Path=/; "
            "subdomain2-cookie=fourth; Domain=test2.example.com; Path=/; "
            "dotted-domain-cookie=fifth; Domain=.example.com; Path=/; "
            "different-domain-cookie=sixth; Domain=different.org; Path=/; "
            "no-path-cookie=seventh; Domain=pathtest.com; "
            "path-cookie=eighth; Domain=pathtest.com; Path=/somepath; "
            "wrong-path-cookie=ninth; Domain=pathtest.com; Path=somepath;"
        )

    def test_request_reply_with_same_url(self):
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://pathtest.com/one/two/")
        
        self.assertEqual(
            set(cookies_sent.keys()),
            {
                "shared-cookie",
                "no-path-cookie",
                "path-cookie",
                "wrong-path-cookie",
            },
        )
        
        self.assertEqual(
            set(cookies_received.keys()),
            {
                "unconstrained-cookie",
                "domain-cookie",
                "subdomain1-cookie",
                "subdomain2-cookie",
                "dotted-domain-cookie",
                "different-domain-cookie",
                "no-path-cookie",
                "path-cookie",
                "wrong-path-cookie",
            },
        )

    def test_request_reply_with_different_url(self):
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://example.com/")
        
        self.assertEqual(
            set(cookies_sent.keys()),
            {
                "shared-cookie",
                "no-path-cookie",
            },
        )
        
        self.assertEqual(
            set(cookies_received.keys()),
            {
                "domain-cookie",
                "dotted-domain-cookie",
            },
        )

    def test_request_reply_with_empty_cookies(self):
        self.jar.clear()
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://empty.com/")
        
        self.assertEqual(cookies_sent, SimpleCookie())
        self.assertEqual(cookies_received, SimpleCookie())

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

if __name__ == '__main__':
    unittest.main()
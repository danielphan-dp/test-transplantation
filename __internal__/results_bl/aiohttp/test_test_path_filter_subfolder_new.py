import unittest
from http.cookies import SimpleCookie
from aiohttp import CookieJar
from yarl import URL

class TestCookieJar(unittest.TestCase):
    def setUp(self):
        self.jar = CookieJar()
        self.jar.update_cookies({
            'shared-cookie': 'value1',
            'no-path-cookie': 'value2',
            'path1-cookie': 'value3; Path=/one/',
            'path2-cookie': 'value4; Path=/one/two/',
            'path3-cookie': 'value5; Path=/one/two/',
            'path4-cookie': 'value6; Path=/one/two/',
        })
        self.cookies_to_send = SimpleCookie()
        self.cookies_to_receive = SimpleCookie()

    def test_request_reply_with_same_url_no_cookies(self):
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://pathtest.com/empty/")
        self.assertEqual(cookies_sent, SimpleCookie())

    def test_request_reply_with_same_url_different_path(self):
        self.cookies_to_send['test-cookie'] = 'test-value; Path=/different/'
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://pathtest.com/one/two/")
        self.assertIn('test-cookie', cookies_sent)
        self.assertEqual(cookies_sent['test-cookie'].value, 'test-value')

    def test_request_reply_with_same_url_edge_case(self):
        self.cookies_to_send['edge-case-cookie'] = 'edge-value; Path=/'
        self.cookies_to_receive['response-cookie'] = 'response-value; Path=/one/two/'
        cookies_sent, cookies_received = self.request_reply_with_same_url("http://pathtest.com/one/two/")
        self.assertIn('edge-case-cookie', cookies_sent)
        self.assertIn('response-cookie', cookies_received)
        self.assertEqual(cookies_received['response-cookie'].value, 'response-value')

    def test_request_reply_with_same_url_invalid_url(self):
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

if __name__ == '__main__':
    unittest.main()
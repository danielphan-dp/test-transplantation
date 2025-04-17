import unittest
from unittest.mock import patch
from freezegun import freeze_time
from aiohttp import CookieJar
from http.cookies import SimpleCookie

class TestTimedRequest(unittest.TestCase):
    def setUp(self):
        self.jar = CookieJar()
        self.cookies_to_send = SimpleCookie("test-cookie=value; Path=/; Max-Age=3600")
        self.jar.update_cookies(self.cookies_to_send)

    @freeze_time("2023-01-01")
    def test_timed_request_with_integer_times(self):
        cookies_sent = self.timed_request("http://test.com/", 1000, 2000)
        self.assertEqual(set(cookies_sent.keys()), {"test-cookie"})

    @freeze_time("2023-01-01")
    def test_timed_request_with_datetime_times(self):
        update_time = datetime.datetime(2023, 1, 1, 0, 0, 0)
        send_time = datetime.datetime(2023, 1, 1, 0, 0, 10)
        cookies_sent = self.timed_request("http://test.com/", update_time, send_time)
        self.assertEqual(set(cookies_sent.keys()), {"test-cookie"})

    @freeze_time("2023-01-01")
    def test_timed_request_with_expired_cookie(self):
        self.cookies_to_send = SimpleCookie("expired-cookie=value; Path=/; Max-Age=0")
        self.jar.update_cookies(self.cookies_to_send)
        cookies_sent = self.timed_request("http://test.com/", 1000, 2000)
        self.assertEqual(set(cookies_sent.keys()), set())

    @freeze_time("2023-01-01")
    def test_timed_request_with_no_cookies(self):
        self.jar.clear()
        cookies_sent = self.timed_request("http://test.com/", 1000, 2000)
        self.assertEqual(set(cookies_sent.keys()), set())

    @patch('aiohttp.CookieJar.filter_cookies')
    def test_timed_request_mocked_filter(self, mock_filter):
        mock_filter.return_value = SimpleCookie("mocked-cookie=value; Path=/;")
        cookies_sent = self.timed_request("http://mocked.com/", 1000, 2000)
        self.assertEqual(set(cookies_sent.keys()), {"mocked-cookie"})
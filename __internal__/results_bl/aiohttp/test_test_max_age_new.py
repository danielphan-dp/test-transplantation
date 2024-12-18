import unittest
from unittest.mock import patch
from freezegun import freeze_time
from aiohttp import CookieJar

class TestCookieJar(unittest.TestCase):
    def setUp(self):
        self.jar = CookieJar()
        self.cookies_to_send = {'shared-cookie': 'value1', 'max-age-cookie': 'value2'}
        self.jar.update_cookies(self.cookies_to_send)

    @freeze_time("2023-01-01")
    def test_timed_request_with_integer_times(self):
        cookies_sent = self.jar.timed_request("http://test.com/", 500, 1000)
        self.assertEqual(set(cookies_sent.keys()), {"shared-cookie", "max-age-cookie"})

    @freeze_time("2023-01-01")
    def test_timed_request_with_float_times(self):
        cookies_sent = self.jar.timed_request("http://test.com/", 1000.0, 2000.0)
        self.assertEqual(set(cookies_sent.keys()), {"shared-cookie"})

    @freeze_time("2023-01-01")
    def test_timed_request_with_future_times(self):
        cookies_sent = self.jar.timed_request("http://test.com/", 3000, 4000)
        self.assertEqual(set(cookies_sent.keys()), set())

    @freeze_time("2023-01-01")
    def test_timed_request_with_negative_times(self):
        cookies_sent = self.jar.timed_request("http://test.com/", -1000, -2000)
        self.assertEqual(set(cookies_sent.keys()), set())

    @freeze_time("2023-01-01")
    def test_timed_request_with_zero_times(self):
        cookies_sent = self.jar.timed_request("http://test.com/", 0, 0)
        self.assertEqual(set(cookies_sent.keys()), {"shared-cookie", "max-age-cookie"})
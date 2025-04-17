import datetime
import unittest
from freezegun import freeze_time
from aiohttp import CookieJar
from http.cookies import SimpleCookie

class TestCookieJar(unittest.TestCase):
    def setUp(self):
        self.jar = CookieJar()
        self.cookies_to_send = SimpleCookie("test-cookie=value; Path=/; HttpOnly")

    def timed_request(self, url: str, update_time: float, send_time: float) -> 'BaseCookie[str]':
        freeze_update_time: Union[datetime.datetime, datetime.timedelta]
        freeze_send_time: Union[datetime.datetime, datetime.timedelta]
        if isinstance(update_time, int):
            freeze_update_time = datetime.timedelta(seconds=update_time)
        else:
            freeze_update_time = datetime.datetime.fromtimestamp(update_time)
        if isinstance(send_time, int):
            freeze_send_time = datetime.timedelta(seconds=send_time)
        else:
            freeze_send_time = datetime.datetime.fromtimestamp(send_time)

        with freeze_time(freeze_update_time):
            self.jar.update_cookies(self.cookies_to_send)

        with freeze_time(freeze_send_time):
            cookies_sent = self.jar.filter_cookies(URL(url))

        self.jar.clear()
        return cookies_sent

    def test_timed_request_with_past_time(self):
        ts_past = datetime.datetime(2000, 1, 1, tzinfo=datetime.timezone.utc).timestamp()
        cookies_sent = self.timed_request("http://test.com/", ts_past, ts_past)
        self.assertEqual(set(cookies_sent.keys()), {"test-cookie"})

    def test_timed_request_with_future_time(self):
        ts_future = datetime.datetime(3000, 1, 1, tzinfo=datetime.timezone.utc).timestamp()
        cookies_sent = self.timed_request("http://test.com/", ts_future, ts_future)
        self.assertEqual(set(cookies_sent.keys()), {"test-cookie"})

    def test_timed_request_with_zero_time(self):
        cookies_sent = self.timed_request("http://test.com/", 0, 0)
        self.assertEqual(set(cookies_sent.keys()), {"test-cookie"})

    def test_timed_request_with_negative_time(self):
        ts_negative = -1
        cookies_sent = self.timed_request("http://test.com/", ts_negative, ts_negative)
        self.assertEqual(set(cookies_sent.keys()), {"test-cookie"})

    def test_timed_request_with_different_update_and_send_time(self):
        ts_update = datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc).timestamp()
        ts_send = datetime.datetime(2025, 1, 1, tzinfo=datetime.timezone.utc).timestamp()
        cookies_sent = self.timed_request("http://test.com/", ts_update, ts_send)
        self.assertEqual(set(cookies_sent.keys()), {"test-cookie"})
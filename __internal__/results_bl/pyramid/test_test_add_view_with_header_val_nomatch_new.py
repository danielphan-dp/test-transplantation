import unittest
from pyramid.httpexceptions import HTTPNotFound

class TestAssertNotFound(unittest.TestCase):

    def setUp(self):
        self.config = self._makeOne(autocommit=True)

    def test_assert_not_found_with_valid_request(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, header=r'Host:\d')
        wrapper = self._getViewCallable(self.config)
        request = self._makeRequest(self.config)
        request.headers = {'Host': '123'}
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, None, request)

    def test_assert_not_found_with_empty_request(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, header=r'Host:\d')
        wrapper = self._getViewCallable(self.config)
        request = self._makeRequest(self.config)
        request.headers = {}
        self._assertNotFound(wrapper, None, request)

    def test_assert_not_found_with_invalid_header_format(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, header=r'Host:\d')
        wrapper = self._getViewCallable(self.config)
        request = self._makeRequest(self.config)
        request.headers = {'Host': 'invalid_format'}
        self._assertNotFound(wrapper, None, request)

    def test_assert_not_found_with_none_request(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, header=r'Host:\d')
        wrapper = self._getViewCallable(self.config)
        self._assertNotFound(wrapper, None, None)

    def test_assert_not_found_with_multiple_arguments(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, header=r'Host:\d')
        wrapper = self._getViewCallable(self.config)
        request = self._makeRequest(self.config)
        request.headers = {'Host': 'abc'}
        self._assertNotFound(wrapper, None, request, 'extra_arg')
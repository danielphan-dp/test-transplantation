import unittest
from pyramid.httpexceptions import HTTPNotFound

class TestAssertNotFound(unittest.TestCase):

    def setUp(self):
        self.config = self._makeOne(autocommit=True)

    def test_assert_not_found_with_none_request(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, accept='text/xml')
        wrapper = self._getViewCallable(self.config)
        request = self._makeRequest(self.config)
        request.accept = None
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, None, request)

    def test_assert_not_found_with_empty_accept(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, accept='text/xml')
        wrapper = self._getViewCallable(self.config)
        request = self._makeRequest(self.config)
        request.accept = ''
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, None, request)

    def test_assert_not_found_with_invalid_accept_type(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, accept='application/json')
        wrapper = self._getViewCallable(self.config)
        request = self._makeRequest(self.config)
        request.accept = 'text/plain'
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, None, request)

    def test_assert_not_found_with_multiple_accept_types(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, accept='text/xml')
        wrapper = self._getViewCallable(self.config)
        request = self._makeRequest(self.config)
        request.accept = 'text/html, application/json'
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, None, request)
import unittest
from pyramid.httpexceptions import HTTPNotFound

class TestAssertNotFound(unittest.TestCase):

    def setUp(self):
        self.config = self._makeOne(autocommit=True)

    def test_assert_not_found_with_none_request(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, is_authenticated=True)
        wrapper = self._getViewCallable(self.config)
        request = None
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, None, request)

    def test_assert_not_found_with_authenticated_request(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, is_authenticated=True)
        wrapper = self._getViewCallable(self.config)
        request = self._makeRequest(self.config)
        request.is_authenticated = True
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, None, request)

    def test_assert_not_found_with_invalid_argument(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, is_authenticated=True)
        wrapper = self._getViewCallable(self.config)
        request = self._makeRequest(self.config)
        invalid_arg = 'invalid'
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, invalid_arg, request)

    def test_assert_not_found_with_empty_request(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, is_authenticated=True)
        wrapper = self._getViewCallable(self.config)
        request = self._makeRequest(self.config)
        request.is_authenticated = False
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, '', request)

    def test_assert_not_found_with_multiple_arguments(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, is_authenticated=True)
        wrapper = self._getViewCallable(self.config)
        request = self._makeRequest(self.config)
        request.is_authenticated = False
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, None, request, 'extra_arg')
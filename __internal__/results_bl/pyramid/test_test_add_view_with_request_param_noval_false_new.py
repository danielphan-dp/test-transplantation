import os
import unittest
from pyramid.httpexceptions import HTTPNotFound
from pyramid.config import Configurator

class TestAssertNotFound(unittest.TestCase):

    def setUp(self):
        self.config = Configurator()

    def test_assert_not_found_with_valid_view(self):
        view = lambda request: 'OK'
        self.config.add_view(view=view)
        wrapper = self.config.make_wsgi_app()
        request = self.config.make_request()
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, None, request)

    def test_assert_not_found_with_invalid_view(self):
        view = lambda request: HTTPNotFound()
        self.config.add_view(view=view)
        wrapper = self.config.make_wsgi_app()
        request = self.config.make_request()
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, None, request)

    def test_assert_not_found_with_missing_request_param(self):
        view = lambda request: 'OK'
        self.config.add_view(view=view, request_param='abc')
        wrapper = self.config.make_wsgi_app()
        request = self.config.make_request()
        request.params = {}
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, None, request)

    def test_assert_not_found_with_invalid_param_type(self):
        view = lambda request: 'OK'
        self.config.add_view(view=view, request_param='abc')
        wrapper = self.config.make_wsgi_app()
        request = self.config.make_request()
        request.params = {'abc': 'invalid'}
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, None, request)

    def _assertNotFound(self, wrapper, *arg):
        self.assertRaises(HTTPNotFound, wrapper, *arg)

if __name__ == '__main__':
    unittest.main()
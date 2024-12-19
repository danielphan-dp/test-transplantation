import os
import unittest
from pyramid.httpexceptions import HTTPNotFound
from pyramid.config import Configurator

class TestNotFoundAssertion(unittest.TestCase):

    def setUp(self):
        self.config = Configurator()

    def test_assert_not_found_with_none_request(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, request_method='POST')
        wrapper = self.config.make_wsgi_app()
        request = self.config.make_request()
        request.method = 'GET'
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, None, request)

    def test_assert_not_found_with_invalid_argument(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, request_method='POST')
        wrapper = self.config.make_wsgi_app()
        request = self.config.make_request()
        request.method = 'GET'
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, 'invalid_arg', request)

    def test_assert_not_found_with_empty_request(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, request_method='POST')
        wrapper = self.config.make_wsgi_app()
        request = self.config.make_request()
        request.method = 'GET'
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, '', request)

    def _assertNotFound(self, wrapper, *arg):
        self.assertRaises(HTTPNotFound, wrapper, *arg)

if __name__ == '__main__':
    unittest.main()
import unittest
from pyramid.httpexceptions import HTTPNotFound
from pyramid.config import Configurator

class TestAssertNotFound(unittest.TestCase):

    def setUp(self):
        self.config = Configurator()

    def test_assert_not_found_with_none(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view)
        wrapper = self.config.make_wsgi_app()
        request = self.config.make_request()
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, None, request)

    def test_assert_not_found_with_empty_request(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view)
        wrapper = self.config.make_wsgi_app()
        request = self.config.make_request()
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, {}, request)

    def test_assert_not_found_with_invalid_context(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view)
        wrapper = self.config.make_wsgi_app()
        request = self.config.make_request()
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, 'invalid_context', request)

    def _assertNotFound(self, wrapper, *arg):
        self.assertRaises(HTTPNotFound, wrapper, *arg)
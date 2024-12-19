import os
import unittest
from pyramid.httpexceptions import HTTPNotFound
from pyramid.testing import DummyRequest

class TestAssertNotFound(unittest.TestCase):

    def setUp(self):
        self.config = self._makeOne(autocommit=True)

    def _makeOne(self, autocommit=False):
        from pyramid.config import Configurator
        return Configurator(autocommit=autocommit)

    def _getViewCallable(self, config):
        return config.make_wsgi_app()

    def _makeRequest(self, config):
        return DummyRequest()

    def test_assert_not_found_with_none_request(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, path_info='/foo')
        wrapper = self._getViewCallable(self.config)
        request = self._makeRequest(self.config)
        request.upath_info = text_('/')
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, None, request)

    def test_assert_not_found_with_invalid_path(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, path_info='/bar')
        wrapper = self._getViewCallable(self.config)
        request = self._makeRequest(self.config)
        request.upath_info = text_('/invalid')
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, None, request)

    def test_assert_not_found_with_empty_path(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, path_info='/baz')
        wrapper = self._getViewCallable(self.config)
        request = self._makeRequest(self.config)
        request.upath_info = text_('')
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, None, request)

    def test_assert_not_found_with_non_callable_view(self):
        view = 'not_a_callable'
        self.config.add_view(view=view, path_info='/foo')
        wrapper = self._getViewCallable(self.config)
        request = self._makeRequest(self.config)
        request.upath_info = text_('/')
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, None, request)
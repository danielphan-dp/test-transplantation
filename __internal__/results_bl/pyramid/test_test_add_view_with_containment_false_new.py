import os
import unittest
from pyramid.httpexceptions import HTTPNotFound
from pyramid.testing import DummyRequest
from . import IDummy

class TestAssertNotFound(unittest.TestCase):

    def setUp(self):
        self.config = self._makeOne(autocommit=True)

    def test_assert_not_found_with_valid_context(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, containment=IDummy)
        wrapper = self._getViewCallable(self.config)
        context = DummyContext()
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, context, None)

    def test_assert_not_found_with_invalid_context(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, containment=IDummy)
        wrapper = self._getViewCallable(self.config)
        invalid_context = None
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, invalid_context)

    def test_assert_not_found_with_extra_arguments(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, containment=IDummy)
        wrapper = self._getViewCallable(self.config)
        context = DummyContext()
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, context, 'extra_arg')

    def test_assert_not_found_with_different_view(self):
        view = lambda *arg: HTTPNotFound()
        self.config.add_view(view=view, containment=IDummy)
        wrapper = self._getViewCallable(self.config)
        context = DummyContext()
        self._assertNotFound(wrapper, context)

    def test_assert_not_found_with_empty_context(self):
        view = lambda *arg: 'OK'
        self.config.add_view(view=view, containment=IDummy)
        wrapper = self._getViewCallable(self.config)
        context = {}
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, context)
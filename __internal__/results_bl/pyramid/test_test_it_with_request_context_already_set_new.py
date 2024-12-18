import unittest
from pyramid.scripting import closer
from pyramid.threadlocal import manager
from pyramid.exceptions import ConfigurationError
from pyramid.scripting import get_root
from pyramid.scripting import prepare
from collections import deque

class TestCloserMethod(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest({})
        self.context = Dummy()
        self.request.context = self.context
        self.registry = self._makeRegistry()
        self.info = self._callFUT(request=self.request, registry=self.registry)
        self.closer = self.info['closer']

    def test_closer_called_sets_context(self):
        self.closer()
        self.assertEqual(self.request.context, self.context)

    def test_closer_called_twice(self):
        self.closer()
        self.closer()
        self.assertEqual(self.request.context, self.context)

    def test_closer_with_no_request_context(self):
        self.request.context = None
        with self.assertRaises(ConfigurationError):
            self.closer()

    def test_closer_state_change(self):
        closer_called = [False]
        def orig_closer():
            closer_called[0] = True
        self.closer = closer
        self.closer()
        self.assertTrue(closer_called[0])

    def test_closer_with_invalid_registry(self):
        self.registry = None
        with self.assertRaises(ConfigurationError):
            self.closer()
import unittest
from pyramid.scripting import closer
from pyramid.threadlocal import manager
from pyramid.exceptions import ConfigurationError
from pyramid.scripting import get_root
from pyramid.scripting import prepare
from collections import deque

class TestCloserFunction(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest({})
        self.context = Dummy()
        self.request.context = self.context
        self.registry = self._makeRegistry()

    def test_closer_called_sets_closer_called_flag(self):
        info = self._callFUT(request=self.request, registry=self.registry)
        closer_func = info['closer']
        closer_func()
        self.assertTrue(closer_called[0])

    def test_closer_does_not_change_context(self):
        info = self._callFUT(request=self.request, registry=self.registry)
        closer_func = info['closer']
        original_context = self.request.context
        closer_func()
        self.assertEqual(self.request.context, original_context)

    def test_closer_called_multiple_times(self):
        info = self._callFUT(request=self.request, registry=self.registry)
        closer_func = info['closer']
        closer_func()
        closer_func()
        self.assertTrue(closer_called[0])

    def test_closer_with_no_request_context(self):
        self.request.context = None
        info = self._callFUT(request=self.request, registry=self.registry)
        closer_func = info['closer']
        closer_func()
        self.assertIsNone(self.request.context)

    def test_closer_raises_exception_on_invalid_state(self):
        self.request.context = "invalid_state"
        info = self._callFUT(request=self.request, registry=self.registry)
        closer_func = info['closer']
        with self.assertRaises(ConfigurationError):
            closer_func()
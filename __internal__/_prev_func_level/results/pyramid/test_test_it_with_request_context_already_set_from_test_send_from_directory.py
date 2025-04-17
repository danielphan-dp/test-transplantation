import unittest
from pyramid.scripting import closer
from pyramid.threadlocal import get_current_request
from pyramid.exceptions import ConfigurationError

class TestCloserFunction(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest({})
        self.context = Dummy()
        self.request.context = self.context
        self.registry = self._makeRegistry()

    def test_closer_called(self):
        info = self._callFUT(request=self.request, registry=self.registry)
        closer_func = info['closer']
        closer_func()
        self.assertTrue(closer_called[0])

    def test_closer_with_no_request_context(self):
        self.request.context = None
        info = self._callFUT(request=self.request, registry=self.registry)
        closer_func = info['closer']
        closer_func()
        self.assertIsNone(self.request.context)

    def test_closer_with_invalid_registry(self):
        with self.assertRaises(ConfigurationError):
            self._callFUT(request=self.request, registry=None)

    def test_closer_called_multiple_times(self):
        info = self._callFUT(request=self.request, registry=self.registry)
        closer_func = info['closer']
        closer_func()
        closer_func()
        self.assertEqual(closer_called[0], True)

    def _callFUT(self, request, registry):
        return {'closer': closer}

    def _makeRegistry(self):
        return DummyRegistry()

class DummyRequest:
    def __init__(self, params):
        self.params = params
        self.context = None
        self.registry = None

class Dummy:
    pass

class DummyRegistry:
    pass

closer_called = [False]
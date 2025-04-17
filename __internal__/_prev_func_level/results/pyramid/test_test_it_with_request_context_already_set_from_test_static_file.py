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
        closer_called = [False]
        def mock_orig_closer():
            closer_called[0] = True
        
        global orig_closer
        orig_closer = mock_orig_closer
        
        info = self._callFUT(request=self.request, registry=self.registry)
        closer = info['closer']
        closer()
        
        self.assertTrue(closer_called[0])

    def test_closer_with_no_request_context(self):
        self.request.context = None
        closer_called = [False]
        
        def mock_orig_closer():
            closer_called[0] = True
        
        global orig_closer
        orig_closer = mock_orig_closer
        
        info = self._callFUT(request=self.request, registry=self.registry)
        closer = info['closer']
        closer()
        
        self.assertTrue(closer_called[0])
        self.assertIsNone(self.request.context)

    def test_closer_with_invalid_registry(self):
        with self.assertRaises(ConfigurationError):
            info = self._callFUT(request=self.request, registry=None)

    def _callFUT(self, request, registry):
        return {'closer': closer}  # Simulating the return value of the method under test

    def _makeRegistry(self):
        return DummyRegistry()  # Simulating registry creation

class DummyRequest:
    def __init__(self, params):
        self.params = params
        self.context = None
        self.registry = None

class Dummy:
    pass

class DummyRegistry:
    pass
import unittest
from pyramid.scripting import closer
from pyramid.threadlocal import get_current_request
from pyramid.exceptions import ConfigurationError

class TestCloserFunction(unittest.TestCase):

    def setUp(self):
        self.finish_called = [False]

    def finished_callback(self, request):
        self.finish_called[0] = True

    def test_closer_invokes_finished_callbacks(self):
        request = DummyRequest({})
        request.registry = self._makeRegistry()
        request.add_finished_callback(self.finished_callback)
        info = self._callFUT(request=request)
        closer = info['closer']
        closer()
        self.assertTrue(self.finish_called[0])

    def test_closer_no_finished_callbacks(self):
        request = DummyRequest({})
        request.registry = self._makeRegistry()
        info = self._callFUT(request=request)
        closer = info['closer']
        closer()
        self.assertFalse(self.finish_called[0])

    def test_closer_multiple_callbacks(self):
        request = DummyRequest({})
        request.registry = self._makeRegistry()
        
        def another_finished_callback(request):
            self.finish_called[0] = True
        
        request.add_finished_callback(self.finished_callback)
        request.add_finished_callback(another_finished_callback)
        info = self._callFUT(request=request)
        closer = info['closer']
        closer()
        self.assertTrue(self.finish_called[0])

    def test_closer_with_exception(self):
        request = DummyRequest({})
        request.registry = self._makeRegistry()
        
        def failing_callback(request):
            raise Exception("Callback failed")
        
        request.add_finished_callback(failing_callback)
        info = self._callFUT(request=request)
        closer = info['closer']
        with self.assertRaises(Exception):
            closer()

    def test_closer_called_twice(self):
        request = DummyRequest({})
        request.registry = self._makeRegistry()
        request.add_finished_callback(self.finished_callback)
        info = self._callFUT(request=request)
        closer = info['closer']
        closer()
        self.assertTrue(self.finish_called[0])
        self.finish_called[0] = False
        closer()
        self.assertFalse(self.finish_called[0])
import unittest
from pyramid.scripting import closer
from pyramid.threadlocal import manager
from pyramid.exceptions import ConfigurationError
from pyramid.util import InstancePropertyHelper
from pyramid.scripting import get_root

class TestCloserFunction(unittest.TestCase):

    def test_closer_does_not_call_finished_callbacks_when_no_callbacks(self):
        finish_called = [False]

        request = DummyRequest({})
        request.registry = self._makeRegistry()
        info = self._callFUT(request=request)
        closer = info['closer']
        closer()
        self.assertFalse(finish_called[0])

    def test_closer_invokes_multiple_finished_callbacks(self):
        finish_called = [False, False]

        def finished_callback_1(request):
            finish_called[0] = True

        def finished_callback_2(request):
            finish_called[1] = True

        request = DummyRequest({})
        request.registry = self._makeRegistry()
        info = self._callFUT(request=request)
        request.add_finished_callback(finished_callback_1)
        request.add_finished_callback(finished_callback_2)
        closer = info['closer']
        closer()
        self.assertTrue(finish_called[0])
        self.assertTrue(finish_called[1])

    def test_closer_called_multiple_times(self):
        finish_called = [False]

        def finished_callback(request):
            finish_called[0] = True

        request = DummyRequest({})
        request.registry = self._makeRegistry()
        info = self._callFUT(request=request)
        request.add_finished_callback(finished_callback)
        closer = info['closer']
        closer()
        closer()
        self.assertTrue(finish_called[0])

    def test_closer_with_exception_in_callback(self):
        finish_called = [False]

        def finished_callback(request):
            raise Exception("Callback error")

        request = DummyRequest({})
        request.registry = self._makeRegistry()
        info = self._callFUT(request=request)
        request.add_finished_callback(finished_callback)
        closer = info['closer']
        with self.assertRaises(Exception):
            closer()
        self.assertFalse(finish_called[0])
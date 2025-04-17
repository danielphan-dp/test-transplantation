import unittest
from pyramid.scripting import closer
from pyramid.tests.test_scripting import DummyRequest

class TestCloserFunction(unittest.TestCase):

    def test_closer_invokes_finished_callbacks_multiple_times(self):
        finish_called = [False]

        def finished_callback(request):
            finish_called[0] = True

        request = DummyRequest({})
        request.registry = self._makeRegistry()
        info = self._callFUT(request=request)
        request.add_finished_callback(finished_callback)
        closer_func = info['closer']
        
        # Call closer multiple times
        for _ in range(3):
            closer_func()
        
        self.assertTrue(finish_called[0])

    def test_closer_does_not_invoke_finished_callbacks_when_not_added(self):
        finish_called = [False]

        request = DummyRequest({})
        request.registry = self._makeRegistry()
        info = self._callFUT(request=request)
        closer_func = info['closer']
        
        # Call closer without adding a finished callback
        closer_func()
        
        self.assertFalse(finish_called[0])

    def test_closer_invokes_finished_callbacks_in_order(self):
        finish_called_order = []

        def finished_callback_1(request):
            finish_called_order.append(1)

        def finished_callback_2(request):
            finish_called_order.append(2)

        request = DummyRequest({})
        request.registry = self._makeRegistry()
        info = self._callFUT(request=request)
        request.add_finished_callback(finished_callback_1)
        request.add_finished_callback(finished_callback_2)
        closer_func = info['closer']
        
        closer_func()
        
        self.assertEqual(finish_called_order, [1, 2])

    def test_closer_with_no_callbacks(self):
        request = DummyRequest({})
        request.registry = self._makeRegistry()
        info = self._callFUT(request=request)
        closer_func = info['closer']
        
        # Call closer with no callbacks added
        closer_func()
        # No assertions needed, just ensuring no exceptions are raised

if __name__ == '__main__':
    unittest.main()
import unittest
from pyramid.scripting import closer
from pyramid.threadlocal import manager

class TestCloserFunction(unittest.TestCase):

    def setUp(self):
        self.manager = manager
        self.closer_called = [False]

    def test_closer_function_called(self):
        closer()
        self.assertTrue(self.closer_called[0])

    def test_closer_function_state(self):
        closer()
        self.assertEqual(self.manager.get(), None)

    def test_closer_function_multiple_calls(self):
        closer()
        self.assertTrue(self.closer_called[0])
        closer()  # Call again to ensure no side effects
        self.assertTrue(self.closer_called[0])

    def test_closer_function_with_registry(self):
        request = DummyRequest({})
        registry = request.registry = self._makeRegistry()
        info = self._callFUT(request=request)
        root, closer, request = info['root'], info['closer'], info['request']
        closer()
        self.assertEqual(request.registry, registry)

    def _makeRegistry(self):
        # Mock registry creation
        return {}

    def _callFUT(self, request):
        # Mock function to simulate the original function behavior
        return {
            'root': DummyRoot(),
            'closer': self.closer,
            'request': request
        }

class DummyRequest:
    def __init__(self, params):
        self.params = params
        self.registry = None

class DummyRoot:
    def __init__(self):
        self.a = ()
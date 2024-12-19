import unittest
from pyramid.request import Request
from pyramid.interfaces import IRequestExtensions
from pyramid.testing import DummyRequest

class TestFooMethod(unittest.TestCase):

    def setUp(self):
        self.config = Dummy()
        self.request = DummyRequest()
        self.request.registry = self.config.registry

    def test_foo_yield(self):
        gen = foo()
        self.assertEqual(next(gen), '')

    def test_foo_multiple_yields(self):
        gen = foo()
        self.assertEqual(next(gen), '')
        with self.assertRaises(StopIteration):
            next(gen)

    def test_foo_with_request_extensions(self):
        extensions = Dummy()
        extensions.methods = {'foo': lambda x, y: y}
        extensions.descriptors = {'bar': property(lambda x: 'bar')}
        self.config.registry.registerUtility(extensions, IRequestExtensions)
        self._callFUT(self.request, extensions=extensions)
        self.assertEqual(self.request.foo('xyz'), 'xyz')
        self.assertEqual(self.request.bar, 'bar')

    def test_foo_with_no_extensions(self):
        self._callFUT(self.request)
        with self.assertRaises(AttributeError):
            self.request.foo('abc')

    def _callFUT(self, request, extensions=None):
        if extensions:
            request.extensions = extensions
        else:
            request.extensions = None
        return foo()
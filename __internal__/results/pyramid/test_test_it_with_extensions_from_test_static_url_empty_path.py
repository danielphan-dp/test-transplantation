import unittest
from pyramid.util import InstancePropertyHelper
from pyramid.scripting import DummyRequest

class TestCloserFunction(unittest.TestCase):

    def setUp(self):
        self.closer_called = [False]

    def _callFUT(self, request, registry):
        def closer():
            self.closer_called[0] = True
        return {'closer': closer}

    def test_closer_called(self):
        exts = DummyExtensions()
        ext_method = lambda r: 'bar'
        name, fn = InstancePropertyHelper.make_property(ext_method, 'foo')
        exts.descriptors[name] = fn
        request = DummyRequest({})
        registry = request.registry = self._makeRegistry([exts, DummyFactory])
        info = self._callFUT(request=request, registry=registry)
        self.assertEqual(request.foo, 'bar')
        closer = info['closer']
        closer()
        self.assertTrue(self.closer_called[0])

    def test_closer_not_called(self):
        exts = DummyExtensions()
        ext_method = lambda r: 'baz'
        name, fn = InstancePropertyHelper.make_property(ext_method, 'foo')
        exts.descriptors[name] = fn
        request = DummyRequest({})
        registry = request.registry = self._makeRegistry([exts, DummyFactory])
        info = self._callFUT(request=request, registry=registry)
        self.assertEqual(request.foo, 'baz')
        self.assertFalse(self.closer_called[0])  # Closer should not be called yet

    def test_closer_called_multiple_times(self):
        exts = DummyExtensions()
        ext_method = lambda r: 'qux'
        name, fn = InstancePropertyHelper.make_property(ext_method, 'foo')
        exts.descriptors[name] = fn
        request = DummyRequest({})
        registry = request.registry = self._makeRegistry([exts, DummyFactory])
        info = self._callFUT(request=request, registry=registry)
        self.assertEqual(request.foo, 'qux')
        closer = info['closer']
        closer()
        self.assertTrue(self.closer_called[0])
        self.closer_called[0] = False  # Reset for next call
        closer()  # Call closer again
        self.assertTrue(self.closer_called[0])  # Should still be True

if __name__ == '__main__':
    unittest.main()
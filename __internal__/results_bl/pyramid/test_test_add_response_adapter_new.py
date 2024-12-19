import unittest
from pyramid.interfaces import IResponse
from pyramid.config import Configurator

class TestAddResponseAdapter(unittest.TestCase):

    def setUp(self):
        self.config = Configurator(autocommit=True)

    def test_add_response_adapter_with_valid_adapter(self):
        class Adapter:
            def __init__(self, other):
                self.other = other

        self.config.add_response_adapter(Adapter, str)
        result = self.config.registry.queryAdapter('foo', IResponse)
        self.assertTrue(result.other, 'foo')

    def test_add_response_adapter_with_invalid_type(self):
        class Adapter:
            def __init__(self, other):
                self.other = other

        self.config.add_response_adapter(Adapter, int)
        result = self.config.registry.queryAdapter('foo', IResponse)
        self.assertIsNone(result)

    def test_add_response_adapter_with_none(self):
        self.config.add_response_adapter(None, str)
        result = self.config.registry.queryAdapter('foo', IResponse)
        self.assertIsNone(result)

    def test_add_multiple_response_adapters(self):
        class Adapter1:
            def __init__(self, other):
                self.other = other

        class Adapter2:
            def __init__(self, other):
                self.other = other

        self.config.add_response_adapter(Adapter1, str)
        self.config.add_response_adapter(Adapter2, str)
        result1 = self.config.registry.queryAdapter('foo', IResponse)
        result2 = self.config.registry.queryAdapter('bar', IResponse)
        self.assertTrue(result1.other, 'foo')
        self.assertIsNone(result2)

    def test_add_response_adapter_with_different_interfaces(self):
        class Adapter:
            def __init__(self, other):
                self.other = other

        self.config.add_response_adapter(Adapter, str)
        self.config.add_response_adapter(Adapter, bytes)
        result_str = self.config.registry.queryAdapter('foo', IResponse)
        result_bytes = self.config.registry.queryAdapter(b'foo', IResponse)
        self.assertTrue(result_str.other, 'foo')
        self.assertIsNone(result_bytes)
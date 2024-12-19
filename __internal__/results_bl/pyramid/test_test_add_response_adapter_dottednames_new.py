import unittest
from pyramid.interfaces import IResponse
from pyramid.config import Configurator

class TestAddResponseAdapter(unittest.TestCase):

    def setUp(self):
        self.config = Configurator(autocommit=True)

    def test_add_response_adapter_with_invalid_type(self):
        with self.assertRaises(TypeError):
            self.config.add_response_adapter('pyramid.response.Response', None)

    def test_add_response_adapter_with_empty_string(self):
        self.config.add_response_adapter('pyramid.response.Response', '')
        result = self.config.registry.queryAdapter('foo', IResponse)
        self.assertIsNone(result)

    def test_add_response_adapter_multiple_types(self):
        self.config.add_response_adapter('pyramid.response.Response', 'builtins.str')
        self.config.add_response_adapter('pyramid.response.Response', 'builtins.bytes')
        result_str = self.config.registry.queryAdapter('foo', IResponse)
        result_bytes = self.config.registry.queryAdapter(b'foo', IResponse)
        self.assertTrue(result_str.body, b'foo')
        self.assertTrue(result_bytes.body, b'foo')

    def test_add_response_adapter_with_nonexistent_adapter(self):
        result = self.config.registry.queryAdapter('bar', IResponse)
        self.assertIsNone(result)

    def test_add_response_adapter_overwrite_existing(self):
        self.config.add_response_adapter('pyramid.response.Response', 'builtins.str')
        self.config.add_response_adapter('pyramid.response.Response', 'builtins.bytes')
        result = self.config.registry.queryAdapter('foo', IResponse)
        self.assertTrue(result.body, b'foo')
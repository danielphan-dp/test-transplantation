import unittest
from pyramid.interfaces import IResponse
from pyramid.config import Configurator

class TestAddResponseAdapter(unittest.TestCase):

    def setUp(self):
        self.config = Configurator(autocommit=True)

    def test_add_response_adapter_none(self):
        self.config.add_response_adapter(None, None)
        adapter = None
        result = self.config.registry.queryAdapter(adapter, IResponse)
        self.assertIsNone(result)

    def test_add_response_adapter_multiple(self):
        class Adapter1:
            pass

        class Adapter2:
            pass

        self.config.add_response_adapter(None, Adapter1)
        self.config.add_response_adapter(None, Adapter2)
        
        adapter1 = Adapter1()
        adapter2 = Adapter2()
        
        result1 = self.config.registry.queryAdapter(adapter1, IResponse)
        result2 = self.config.registry.queryAdapter(adapter2, IResponse)
        
        self.assertIs(result1, adapter1)
        self.assertIs(result2, adapter2)

    def test_add_response_adapter_invalid_type(self):
        with self.assertRaises(TypeError):
            self.config.add_response_adapter(None, "invalid_type")

    def test_add_response_adapter_interface(self):
        from zope.interface import Interface, implementer

        class ICustomResponse(Interface):
            pass

        @implementer(ICustomResponse)
        class CustomAdapter:
            pass

        self.config.add_response_adapter(None, CustomAdapter)
        adapter = CustomAdapter()
        result = self.config.registry.queryAdapter(adapter, ICustomResponse)
        self.assertIs(result, adapter)

    def test_add_response_adapter_empty_registry(self):
        class Adapter:
            pass

        adapter = Adapter()
        result = self.config.registry.queryAdapter(adapter, IResponse)
        self.assertIsNone(result)
import unittest
from pyramid.testing import DummyRequest
from pyramid.registry import Registry
from pyramid.security import Everyone

class TestMakeRequest(unittest.TestCase):

    def test_request_has_registry(self):
        request = _makeRequest()
        self.assertIsInstance(request.registry, Registry)

    def test_request_is_authenticated(self):
        request = _makeRequest()
        self.assertIs(request.is_authenticated, False)

    def test_request_has_default_principals(self):
        request = _makeRequest()
        self.assertEqual(request.effective_principals, [Everyone])

    def test_request_has_no_attributes(self):
        request = _makeRequest()
        self.assertFalse(hasattr(request, 'some_non_existent_attribute'))

    def test_request_initialization(self):
        request = _makeRequest()
        self.assertIsNotNone(request)

    def test_request_registry_is_unique(self):
        request1 = _makeRequest()
        request2 = _makeRequest()
        self.assertIsNot(request1.registry, request2.registry)
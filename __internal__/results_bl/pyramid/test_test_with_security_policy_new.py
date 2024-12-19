import unittest
from pyramid.testing import DummyRequest
from pyramid.registry import Registry
from pyramid.security import LegacySecurityPolicy

class TestMakeRequest(unittest.TestCase):

    def test_make_request_with_default_environ(self):
        request = _makeRequest()
        self.assertIsInstance(request, DummyRequest)
        self.assertIsInstance(request.registry, Registry)

    def test_make_request_with_custom_environ(self):
        environ = {'REQUEST_METHOD': 'GET'}
        request = _makeRequest(environ)
        self.assertEqual(request.environ['REQUEST_METHOD'], 'GET')

    def test_make_request_registry_initialization(self):
        request = _makeRequest()
        self.assertIsNotNone(request.registry)
        self.assertIsInstance(request.registry, Registry)

    def test_make_request_with_security_policy(self):
        request = _makeRequest()
        registry = request.registry
        registry.registerUtility(LegacySecurityPolicy(), ISecurityPolicy)
        self.assertIsInstance(registry.getUtility(ISecurityPolicy), LegacySecurityPolicy)

    def test_make_request_with_no_environ(self):
        request = _makeRequest(None)
        self.assertIsInstance(request, DummyRequest)
        self.assertIsInstance(request.registry, Registry)
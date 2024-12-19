import unittest
from pyramid.router import Router
from pyramid.interfaces import IViewClassifier
from pyramid.testing import DummyRequest, DummyResponse

class TestMockFinishRequest(unittest.TestCase):

    def setUp(self):
        self.router = Router()

    def test_mock_finish_request_no_op(self):
        self.router._mockFinishRequest(self.router)
        request = DummyRequest()
        self.router.finish_request(request)
        # No exception should be raised, and nothing should happen

    def test_mock_finish_request_context_preserved(self):
        context = DummyContext()
        self.router._mockFinishRequest(self.router)
        request = DummyRequest()
        request.context = context
        self.router.finish_request(request)
        self.assertEqual(request.context, context)

    def test_mock_finish_request_with_different_context(self):
        context1 = DummyContext()
        context2 = DummyContext()
        self.router._mockFinishRequest(self.router)
        request1 = DummyRequest()
        request1.context = context1
        request2 = DummyRequest()
        request2.context = context2
        self.router.finish_request(request1)
        self.router.finish_request(request2)
        self.assertEqual(request1.context, context1)
        self.assertEqual(request2.context, context2)

    def test_mock_finish_request_multiple_calls(self):
        self.router._mockFinishRequest(self.router)
        request = DummyRequest()
        for _ in range(10):
            self.router.finish_request(request)
        # No exception should be raised, and nothing should happen

if __name__ == '__main__':
    unittest.main()
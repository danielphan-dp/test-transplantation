import unittest
from pyramid.router import Router
from pyramid.interfaces import INewRequest
from zope.interface import Interface, alsoProvides

class TestMockFinishRequest(unittest.TestCase):

    def setUp(self):
        self.router = Router()

    def test_mock_finish_request_no_op(self):
        self.router.finish_request = lambda request: None
        request = object()
        self.router.finish_request(request)  # Should not raise an error

    def test_mock_finish_request_context_preserved(self):
        class IFoo(Interface):
            pass

        def listener(event):
            alsoProvides(event.request, IFoo)

        self.router.registry.registerHandler(listener, (INewRequest,))
        request = object()
        self.router.finish_request(request)  # Should not alter request context

        self.assertTrue(IFoo.providedBy(request))

    def test_mock_finish_request_multiple_calls(self):
        call_count = [0]

        def mock_finish_request(request):
            call_count[0] += 1

        self.router.finish_request = mock_finish_request
        request = object()
        self.router.finish_request(request)
        self.router.finish_request(request)

        self.assertEqual(call_count[0], 2)

    def test_mock_finish_request_with_different_requests(self):
        request1 = object()
        request2 = object()

        def mock_finish_request(request):
            return request

        self.router.finish_request = mock_finish_request
        result1 = self.router.finish_request(request1)
        result2 = self.router.finish_request(request2)

        self.assertIs(result1, request1)
        self.assertIs(result2, request2)

if __name__ == '__main__':
    unittest.main()
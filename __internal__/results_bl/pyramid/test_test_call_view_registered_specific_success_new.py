import unittest
from pyramid.router import Router
from pyramid.interfaces import IRequest
from zope.interface import Interface, directlyProvides

class TestMockFinishRequest(unittest.TestCase):

    class DummyContext:
        pass

    class DummyResponse:
        def __init__(self):
            self.app_iter = []

    class DummyView:
        def __init__(self, response):
            self.response = response
            self.request = self.DummyRequest()

        class DummyRequest:
            def __init__(self):
                self.view_name = ''
                self.subpath = []
                self.context = None
                self.root = None

    class DummyStartResponse:
        def __init__(self):
            self.status = ''
            self.headers = ()

        def __call__(self, status, headers):
            self.status = status
            self.headers = headers

    def setUp(self):
        self.router = Router()

    def test_mock_finish_request_no_op(self):
        context = self.DummyContext()
        directlyProvides(context, Interface)
        response = self.DummyResponse()
        response.app_iter = ['Hello world']
        view = self.DummyView(response)
        environ = {}
        self.router.finish_request = lambda request: None
        start_response = self.DummyStartResponse()
        result = self.router(environ, start_response)
        self.assertEqual(result, [])
        self.assertEqual(start_response.headers, ())
        self.assertEqual(start_response.status, '')

    def test_mock_finish_request_with_context(self):
        context = self.DummyContext()
        directlyProvides(context, Interface)
        response = self.DummyResponse()
        response.app_iter = ['Hello world']
        view = self.DummyView(response)
        view.request.context = context
        environ = {}
        self.router.finish_request = lambda request: None
        start_response = self.DummyStartResponse()
        result = self.router(environ, start_response)
        self.assertEqual(result, [])
        self.assertEqual(view.request.context, context)

    def test_mock_finish_request_edge_case(self):
        context = self.DummyContext()
        directlyProvides(context, Interface)
        response = self.DummyResponse()
        response.app_iter = []
        view = self.DummyView(response)
        environ = {}
        self.router.finish_request = lambda request: None
        start_response = self.DummyStartResponse()
        result = self.router(environ, start_response)
        self.assertEqual(result, [])
        self.assertEqual(view.request.app_iter, [])

if __name__ == '__main__':
    unittest.main()
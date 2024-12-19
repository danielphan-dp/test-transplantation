import unittest
from pyramid.router import Router
from pyramid.interfaces import INewRequest, IBeforeTraversal, IContextFound, INewResponse, IViewClassifier

class TestRouter(unittest.TestCase):

    def setUp(self):
        self.router = Router()

    def test_mockFinishRequest_no_op(self):
        self.router._mockFinishRequest(self.router)
        self.assertEqual(self.router.finish_request, self.router._mockFinishRequest.__closure__[0].cell_contents)

    def test_mockFinishRequest_with_events(self):
        context = DummyContext()
        self._registerTraverserFactory(context)
        response = DummyResponse()
        response.app_iter = ['Hello world']
        view = DummyView(response)
        environ = self._makeEnviron()
        self._registerView(view, '', IViewClassifier, None, None)
        request_events = self._registerEventListener(INewRequest)
        beforetraversal_events = self._registerEventListener(IBeforeTraversal)
        context_found_events = self._registerEventListener(IContextFound)
        response_events = self._registerEventListener(INewResponse)
        self.router._mockFinishRequest(self.router)
        start_response = DummyStartResponse()
        result = self.router(environ, start_response)
        self.assertEqual(len(request_events), 1)
        self.assertEqual(len(beforetraversal_events), 1)
        self.assertEqual(len(context_found_events), 1)
        self.assertEqual(len(response_events), 1)
        self.assertEqual(result, response.app_iter)

    def test_mockFinishRequest_no_events(self):
        self.router._mockFinishRequest(self.router)
        environ = self._makeEnviron()
        start_response = DummyStartResponse()
        result = self.router(environ, start_response)
        self.assertIsNone(result)

    def test_mockFinishRequest_multiple_calls(self):
        self.router._mockFinishRequest(self.router)
        for _ in range(5):
            environ = self._makeEnviron()
            start_response = DummyStartResponse()
            result = self.router(environ, start_response)
            self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
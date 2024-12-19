import os
import unittest
from pyramid.renderers import null_renderer
from pyramid.response import Response
from pyramid.exceptions import HTTPForbidden

class TestViewMethod(unittest.TestCase):

    def test_view_with_none_context(self):
        view = lambda context, request: Response('OK')
        request = self._makeRequest()
        self.assertEqual(view(None, request).text, 'OK')

    def test_view_with_valid_context(self):
        view = lambda context, request: Response(f'Context: {context}')
        request = self._makeRequest()
        self.assertEqual(view('valid_context', request).text, 'Context: valid_context')

    def test_view_with_forbidden_permission(self):
        view = lambda context, request: Response('Forbidden', status=403)
        request = self._makeRequest()
        self.assertEqual(view(None, request).status_code, 403)

    def test_view_with_invalid_request(self):
        view = lambda context, request: Response('Invalid Request', status=400)
        request = self._makeRequest()
        self.assertEqual(view(None, request).status_code, 400)

    def _makeRequest(self):
        class DummyRequest:
            pass
        return DummyRequest()
import sys
import unittest
from pyramid.testing import DummyRequest, DummyResponse
from pyramid.view import make_view

class TestMakeView(unittest.TestCase):

    def test_make_view_returns_function(self):
        response = DummyResponse()
        view = make_view(response)
        self.assertTrue(callable(view))

    def test_make_view_calls_response(self):
        response = DummyResponse(b'test response')
        view = make_view(response)
        context = object()
        request = DummyRequest()
        result = view(context, request)
        self.assertEqual(result, response)

    def test_make_view_with_different_response(self):
        response = DummyResponse(b'another response')
        view = make_view(response)
        context = object()
        request = DummyRequest()
        result = view(context, request)
        self.assertEqual(result, response)

    def test_make_view_with_none_response(self):
        response = None
        view = make_view(response)
        context = object()
        request = DummyRequest()
        result = view(context, request)
        self.assertIsNone(result)

    def test_make_view_with_empty_response(self):
        response = DummyResponse(b'')
        view = make_view(response)
        context = object()
        request = DummyRequest()
        result = view(context, request)
        self.assertEqual(result, response)

    def test_make_view_with_custom_context(self):
        response = DummyResponse(b'custom context response')
        view = make_view(response)
        context = {'key': 'value'}
        request = DummyRequest()
        result = view(context, request)
        self.assertEqual(result, response)
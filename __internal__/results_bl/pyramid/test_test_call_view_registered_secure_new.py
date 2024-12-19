import sys
import unittest
from pyramid.testing import DummyRequest, DummyResponse
from pyramid.view import make_view

class TestMakeView(unittest.TestCase):

    def test_make_view_returns_function(self):
        response = DummyResponse()
        view = make_view(response)
        self.assertTrue(callable(view))

    def test_view_function_returns_response(self):
        response = DummyResponse()
        view = make_view(response)
        context = object()
        request = DummyRequest()
        result = view(context, request)
        self.assertEqual(result, response)

    def test_view_function_with_different_context(self):
        response = DummyResponse()
        view = make_view(response)
        context = object()
        request = DummyRequest()
        result = view(context, request)
        self.assertEqual(result, response)

    def test_view_function_with_none_context(self):
        response = DummyResponse()
        view = make_view(response)
        context = None
        request = DummyRequest()
        result = view(context, request)
        self.assertEqual(result, response)

    def test_view_function_with_different_request(self):
        response = DummyResponse()
        view = make_view(response)
        context = object()
        request = DummyRequest()
        result = view(context, request)
        self.assertEqual(result, response)

    def test_view_function_with_custom_request_attributes(self):
        response = DummyResponse()
        view = make_view(response)
        context = object()
        request = DummyRequest()
        request.custom_attr = 'test'
        result = view(context, request)
        self.assertEqual(result, response)
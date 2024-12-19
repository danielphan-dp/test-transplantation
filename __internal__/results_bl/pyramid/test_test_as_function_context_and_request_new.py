import unittest
from pyramid.response import Response
from pyramid.exceptions import ConfigurationError

class TestViewFunction(unittest.TestCase):

    def test_view_with_valid_context_and_request(self):
        def view(context, request):
            return Response('Valid Response')

        result = view({}, {})
        self.assertEqual(result.text, 'Valid Response')

    def test_view_with_none_context(self):
        def view(context, request):
            return Response('Context is None')

        result = view(None, {})
        self.assertEqual(result.text, 'Context is None')

    def test_view_with_none_request(self):
        def view(context, request):
            return Response('Request is None')

        result = view({}, None)
        self.assertEqual(result.text, 'Request is None')

    def test_view_with_both_none(self):
        def view(context, request):
            return Response('Both are None')

        result = view(None, None)
        self.assertEqual(result.text, 'Both are None')

    def test_view_with_empty_context(self):
        def view(context, request):
            return Response('Empty Context')

        result = view({}, {})
        self.assertEqual(result.text, 'Empty Context')

    def test_view_with_invalid_context_type(self):
        def view(context, request):
            if not isinstance(context, dict):
                raise ConfigurationError("Invalid context type")
            return Response('Valid Response')

        with self.assertRaises(ConfigurationError):
            view([], {})

    def test_view_with_invalid_request_type(self):
        def view(context, request):
            if not hasattr(request, 'some_attribute'):
                raise ConfigurationError("Invalid request type")
            return Response('Valid Response')

        with self.assertRaises(ConfigurationError):
            view({}, 'invalid_request')
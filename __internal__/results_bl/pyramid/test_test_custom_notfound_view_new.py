import sys
import unittest
from pyramid.testing import DummyRequest
from pyramid.exceptions import HTTPNotFound
from pyramid.view import view_config

class TestView(unittest.TestCase):

    def _makeRequest(self, **kwargs):
        return DummyRequest(**kwargs)

    def _makeOne(self, view):
        return view

    def test_custom_notfound_view_with_valid_path(self):
        request = self._makeRequest(PATH_INFO='/valid-path')
        context = ExceptionResponse()

        def custom_notfound(context, request):
            return 'Found'

        view = self._makeOne(custom_notfound)
        response = view(context, request)
        self.assertEqual(response, 'Found')

    def test_custom_notfound_view_with_invalid_path(self):
        request = self._makeRequest(PATH_INFO='/invalid-path')
        context = ExceptionResponse()

        def custom_notfound(context, request):
            return 'Not Found'

        view = self._makeOne(custom_notfound)
        response = view(context, request)
        self.assertEqual(response, 'Not Found')

    def test_custom_notfound_view_with_empty_path(self):
        request = self._makeRequest(PATH_INFO='')
        context = ExceptionResponse()

        def custom_notfound(context, request):
            return 'Empty Path'

        view = self._makeOne(custom_notfound)
        response = view(context, request)
        self.assertEqual(response, 'Empty Path')

    def test_custom_notfound_view_with_none_context(self):
        request = self._makeRequest(PATH_INFO='/abc')
        context = None

        def custom_notfound(context, request):
            return 'No Context'

        view = self._makeOne(custom_notfound)
        response = view(context, request)
        self.assertEqual(response, 'No Context')

    def test_custom_notfound_view_raises_http_not_found(self):
        request = self._makeRequest(PATH_INFO='/abc')
        context = ExceptionResponse()

        def custom_notfound(context, request):
            raise HTTPNotFound()

        view = self._makeOne(custom_notfound)
        with self.assertRaises(HTTPNotFound):
            view(context, request)
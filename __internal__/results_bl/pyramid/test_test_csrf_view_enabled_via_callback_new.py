import unittest
from pyramid.exceptions import BadCSRFToken
from pyramid.response import Response
from pyramid.request import Request
from pyramid.testing import DummyRequest

class TestView(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.request.method = 'POST'
        self.request.session = {'csrf_token': 'foo'}

    def test_view_with_valid_csrf_token(self):
        self.request.session['csrf_token'] = 'foo'
        response = view(None, self.request)
        self.assertIsInstance(response, Response)

    def test_view_with_invalid_csrf_token(self):
        self.request.session['csrf_token'] = 'bar'
        with self.assertRaises(BadCSRFToken):
            view(None, self.request)

    def test_view_with_no_csrf_token(self):
        del self.request.session['csrf_token']
        with self.assertRaises(BadCSRFToken):
            view(None, self.request)

    def test_view_with_get_method(self):
        self.request.method = 'GET'
        response = view(None, self.request)
        self.assertIsInstance(response, Response)

    def test_view_with_empty_request(self):
        empty_request = DummyRequest()
        with self.assertRaises(BadCSRFToken):
            view(None, empty_request)
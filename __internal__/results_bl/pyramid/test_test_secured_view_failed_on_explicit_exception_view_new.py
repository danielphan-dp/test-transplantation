import unittest
from pyramid.httpexceptions import HTTPForbidden
from pyramid.request import Request
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.testing import DummyRequest

class TestGetResponse(unittest.TestCase):

    def setUp(self):
        from pyramid.config import Configurator
        self.config = Configurator()
        self._registerSecurityPolicy(False)

    def _registerSecurityPolicy(self, allow):
        # Mock security policy registration
        pass

    def test_get_response_with_valid_app(self):
        app = self.config.make_wsgi_app()
        request = Request.blank('/foo', base_url='http://example.com')
        response = request.get_response(app)
        self.assertIsNotNone(response)

    def test_get_response_with_invalid_app(self):
        app = None
        request = Request.blank('/foo', base_url='http://example.com')
        with self.assertRaises(TypeError):
            request.get_response(app)

    def test_get_response_with_forbidden_view(self):
        def view(request):
            raise HTTPForbidden()

        self.config.add_view(view, name='foo', permission=NO_PERMISSION_REQUIRED)
        app = self.config.make_wsgi_app()
        request = Request.blank('/foo', base_url='http://example.com')
        with self.assertRaises(HTTPForbidden):
            request.get_response(app)

    def test_get_response_with_no_permission_view(self):
        def view(request):
            return "Hello, World!"

        self.config.add_view(view, name='foo', permission=NO_PERMISSION_REQUIRED)
        app = self.config.make_wsgi_app()
        request = Request.blank('/foo', base_url='http://example.com')
        response = request.get_response(app)
        self.assertEqual(response.text, "Hello, World!")
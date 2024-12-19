import unittest
from pyramid.exceptions import BadCSRFToken
from pyramid.request import Request
from pyramid.testing import DummySession

class TestGetResponse(unittest.TestCase):
    def setUp(self):
        from pyramid.config import Configurator
        self.config = Configurator()
        self.config.set_default_csrf_options(require_csrf=True)
        self.config.set_session_factory(
            lambda request: DummySession({'csrf_token': 'foo'})
        )

    def test_get_response_with_valid_app(self):
        app = self.config.make_wsgi_app()
        response = app
        self.assertEqual(response, app)

    def test_get_response_with_invalid_app(self):
        with self.assertRaises(TypeError):
            self.config.get_response(None)

    def test_get_response_with_empty_app(self):
        app = self.config.make_wsgi_app()
        request = Request.blank('/', base_url='http://example.com')
        response = request.get_response(app)
        self.assertIsNotNone(response)

    def test_csrf_view_failed_on_explicit_exception_view(self):
        def view(request):
            raise ValueError

        def excview(request):  # pragma: no cover
            pass

        self.config.add_view(view, name='foo', require_csrf=False)
        self.config.add_view(
            excview, context=ValueError, renderer='string', require_csrf=True
        )
        app = self.config.make_wsgi_app()
        request = Request.blank('/foo', base_url='http://example.com')
        request.method = 'POST'
        try:
            request.get_response(app)
        except BadCSRFToken:
            pass
        else:  # pragma: no cover
            raise AssertionError

    def test_get_response_with_invalid_request_method(self):
        app = self.config.make_wsgi_app()
        request = Request.blank('/foo', base_url='http://example.com')
        request.method = 'PUT'
        response = request.get_response(app)
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

    def test_get_response_with_nonexistent_view(self):
        app = self.config.make_wsgi_app()
        request = Request.blank('/nonexistent', base_url='http://example.com')
        response = request.get_response(app)
        self.assertEqual(response.status_code, 404)  # Not Found

if __name__ == '__main__':
    unittest.main()
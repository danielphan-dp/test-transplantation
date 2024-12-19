import unittest
from pyramid.config import Configurator
from pyramid.response import Response

class TestGetMethod(unittest.TestCase):

    def setUp(self):
        self.config = Configurator()
        self.config.add_route('myroute', '/test')
        self.config.add_view(self.myview, route_name='myroute', renderer='json')
        self.testapp = self.config.make_wsgi_app()

    def myview(self, request):
        return Response('Test Response')

    def test_get_method_returns_cookie(self):
        request = self.testapp.get('/test', status=200)
        self.assertEqual(request.text, 'Test Response')

    def test_get_method_with_nonexistent_route(self):
        response = self.testapp.get('/nonexistent', status=404)
        self.assertIn('Not Found', response.text)

    def test_get_method_with_unicode(self):
        request_path = '/avalia%C3%A7%C3%A3o_participante'
        response = self.testapp.get(request_path, status=200)
        self.assertEqual(response.text, 'Test Response')

    def test_get_method_with_empty_cookie(self):
        self.config.add_view(lambda request: Response(''), route_name='myroute', renderer='json')
        response = self.testapp.get('/test', status=200)
        self.assertEqual(response.text, '')
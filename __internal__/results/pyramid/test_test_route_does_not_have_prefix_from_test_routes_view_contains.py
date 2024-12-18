import unittest
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):
    def setUp(self):
        self.config = Configurator()

    def test_add_route_with_valid_name_and_path(self):
        self.config.add_route('test_route', '/test')
        request = self._makeRequest('/')
        self.assertEqual(request.route_url('test_route'), 'http://localhost/test')

    def test_add_route_with_empty_name(self):
        with self.assertRaises(ValueError):
            self.config.add_route('', '/test')

    def test_add_route_with_empty_path(self):
        with self.assertRaises(ValueError):
            self.config.add_route('test_route', '')

    def test_add_route_with_duplicate_name(self):
        self.config.add_route('duplicate_route', '/first')
        self.config.add_route('duplicate_route', '/second')
        request = self._makeRequest('/')
        self.assertEqual(request.route_url('duplicate_route'), 'http://localhost/second')

    def test_add_route_with_special_characters(self):
        self.config.add_route('special_route', '/test/!@#$%^&*()')
        request = self._makeRequest('/')
        self.assertEqual(request.route_url('special_route'), 'http://localhost/test/!@#$%^&*()')

    def _makeRequest(self, path):
        from pyramid.request import Request
        from pyramid.testing import DummyRequest
        return DummyRequest(path=path)

if __name__ == '__main__':
    unittest.main()
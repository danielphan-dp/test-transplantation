import unittest
from pyramid.config import Configurator

class TestAddRoute(unittest.TestCase):

    def setUp(self):
        self.config = Configurator()

    def test_add_route_with_no_arguments(self):
        self.config.add_route()
        self.assertEqual(self.config.route_args, ())
        self.assertEqual(self.config.route_kw, {})

    def test_add_route_with_only_name(self):
        self.config.add_route('name')
        self.assertEqual(self.config.route_args, ('name',))
        self.assertEqual(self.config.route_kw, {})

    def test_add_route_with_name_and_path(self):
        self.config.add_route('name', 'path')
        self.assertEqual(self.config.route_args, ('name', 'path'))
        self.assertEqual(self.config.route_kw, {})

    def test_add_route_with_name_path_and_extra_kw(self):
        self.config.add_route('name', 'path', request_method='GET')
        self.assertEqual(self.config.route_args, ('name', 'path'))
        self.assertEqual(self.config.route_kw, {'request_method': 'GET'})

    def test_add_route_with_multiple_routes(self):
        self.config.add_route('first', '/first')
        self.config.add_route('second', '/second')
        self.assertEqual(self.config.route_args, ('second', '/second'))
        self.assertEqual(self.config.route_kw, {})

    def test_add_route_discriminator(self):
        self.config.add_route('name', 'path')
        self.assertEqual(
            self.config.action_state.actions[-1]['discriminator'], ('route', 'name')
        )
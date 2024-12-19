import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper
from pyramid.util import text_
from pyramid.url import current_route_path

class TestCurrentRoutePath(unittest.TestCase):

    def setUp(self):
        self.request = DummyRequest()
        self.route = DummyRoute('/1/2/3')
        self.mapper = DummyRoutesMapper(route=self.route)
        self.request.matched_route = self.route
        self.request.matchdict = {}
        self.request.script_name = '/script_name'
        self.request.registry.registerUtility(self.mapper, IRoutesMapper)

    def test_current_route_path_with_extra_elements(self):
        result = self.request.current_route_path('extra1', 'extra2')
        self.assertEqual(result, '/script_name/1/2/3/extra1/extra2')

    def test_current_route_path_with_query_params(self):
        result = self.request.current_route_path('extra1', 'extra2', _query={'a': 1})
        self.assertEqual(result, '/script_name/1/2/3/extra1/extra2?a=1')

    def test_current_route_path_with_anchor(self):
        result = self.request.current_route_path('extra1', 'extra2', _anchor=text_(b"foo"))
        self.assertEqual(result, '/script_name/1/2/3/extra1/extra2#foo')

    def test_current_route_path_with_empty_elements(self):
        result = self.request.current_route_path()
        self.assertEqual(result, '/script_name/1/2/3')

    def test_current_route_path_with_no_script_name(self):
        self.request.script_name = ''
        result = self.request.current_route_path('extra1', 'extra2')
        self.assertEqual(result, '/1/2/3/extra1/extra2')

    def test_current_route_path_with_invalid_route(self):
        self.request.matched_route = None
        result = self.request.current_route_path('extra1', 'extra2')
        self.assertEqual(result, '/script_name/extra1/extra2')  # Assuming it defaults to script_name

    def test_current_route_path_with_multiple_query_params(self):
        result = self.request.current_route_path('extra1', 'extra2', _query={'a': 1, 'b': 2})
        self.assertEqual(result, '/script_name/1/2/3/extra1/extra2?a=1&b=2')
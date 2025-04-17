import os
import unittest
from pyramid.testing import DummyRequest
from pyramid.interfaces import IRoutesMapper

class TestRoutePath(unittest.TestCase):

    def _makeOne(self):
        return DummyRequest()

    def test_route_path_with_no_elements(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_path('flub')
        self.assertEqual(result, '/')

    def test_route_path_with_single_element(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/single'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_path('flub', 'element1')
        self.assertEqual(result, '/single/element1')

    def test_route_path_with_query_params(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/query'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_path('flub', _query={'param1': 'value1', 'param2': 'value2'})
        self.assertEqual(result, '/query?param1=value1&param2=value2')

    def test_route_path_with_anchor(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/anchor'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_path('flub', _anchor='section1')
        self.assertEqual(result, '/anchor#section1')

    def test_route_path_with_multiple_elements_and_query(self):
        request = self._makeOne()
        mapper = DummyRoutesMapper(route=DummyRoute('/multi'))
        request.registry.registerUtility(mapper, IRoutesMapper)
        result = request.route_path('flub', 'elem1', 'elem2', _query={'key': 'value'})
        self.assertEqual(result, '/multi/elem1/elem2?key=value')
import unittest
from pyramid.urldispatch import RoutesMapper

class TestRoutesMapper(unittest.TestCase):

    def _makeOne(self):
        return RoutesMapper()

    def test_get_route_misses(self):
        mapper = self._makeOne()
        result = mapper.get_route('whatever')
        self.assertEqual(result, None)

    def test_get_route_with_existing_route(self):
        mapper = self._makeOne()
        mapper.add_route('test_route', '/test')
        result = mapper.get_route('test_route')
        self.assertIsNotNone(result)

    def test_get_route_with_different_route_name(self):
        mapper = self._makeOne()
        mapper.add_route('another_route', '/another')
        result = mapper.get_route('non_existent_route')
        self.assertEqual(result, None)

    def test_get_route_with_empty_string(self):
        mapper = self._makeOne()
        result = mapper.get_route('')
        self.assertEqual(result, None)

    def test_get_route_with_none(self):
        mapper = self._makeOne()
        result = mapper.get_route(None)
        self.assertEqual(result, None)
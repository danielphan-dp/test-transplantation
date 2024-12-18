import unittest
from pyramid.testing import DummyRequest
from pyramid.urldispatch import RoutesMapper

class TestConnectMethod(unittest.TestCase):
    def setUp(self):
        self.mapper = RoutesMapper()

    def test_connect_with_valid_object(self):
        obj = {'key': 'value'}
        self.mapper.connect('foo', '/path', obj=obj)
        result = self.mapper.routes['foo'].obj
        self.assertEqual(result, obj)

    def test_connect_with_no_object(self):
        with self.assertRaises(IndexError):
            self.mapper.connect('foo', '/path')

    def test_connect_multiple_objects(self):
        obj1 = {'key1': 'value1'}
        obj2 = {'key2': 'value2'}
        self.mapper.connect('foo', '/path1', obj=obj1)
        self.mapper.connect('bar', '/path2', obj=obj2)
        result1 = self.mapper.routes['foo'].obj
        result2 = self.mapper.routes['bar'].obj
        self.assertEqual(result1, obj1)
        self.assertEqual(result2, obj2)

    def test_connect_with_different_paths(self):
        obj = {'key': 'value'}
        self.mapper.connect('foo', '/path1', obj=obj)
        self.mapper.connect('bar', '/path2', obj=obj)
        result1 = self.mapper.routes['foo'].obj
        result2 = self.mapper.routes['bar'].obj
        self.assertEqual(result1, obj)
        self.assertEqual(result2, obj)

    def test_connect_with_invalid_route(self):
        obj = {'key': 'value'}
        self.mapper.connect('foo', '/path', obj=obj)
        request = DummyRequest(path_info='/invalid_path')
        with self.assertRaises(KeyError):
            self.mapper(request)

if __name__ == '__main__':
    unittest.main()
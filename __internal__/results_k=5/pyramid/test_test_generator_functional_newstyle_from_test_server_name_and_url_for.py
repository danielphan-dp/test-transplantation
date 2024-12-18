import unittest
from pyramid.urldispatch import _compile_route
from pyramid.util import text_

class TestCompileRouteFunctional(unittest.TestCase):
    def generates(self, pattern, dict, result):
        self.assertEqual(_compile_route(pattern)[1](dict), result)

    def test_empty_string(self):
        self.generates('/{x}', {'x': ''}, '/')
        self.generates('/{x}', {'x': None}, '/')

    def test_special_characters(self):
        self.generates('/{x}', {'x': ' ', '/': 'value'}, '/ ')
        self.generates('/{x}', {'x': '%20'}, '/%20')
        self.generates('/{x}', {'x': '!', 'y': 'test'}, '/!')

    def test_nested_paths(self):
        self.generates('/{x}/{y}', {'x': 'foo', 'y': 'bar'}, '/foo/bar')
        self.generates('/{x}/{y}/{z}', {'x': 'foo', 'y': 'bar', 'z': 'baz'}, '/foo/bar/baz')

    def test_encoded_characters(self):
        self.generates('/{x}', {'x': text_(b'/La Pe\xc3\xb1a', 'utf-8')}, '//La%20Pe%C3%B1a')
        self.generates('/{x}', {'x': text_(b'/Hello World!', 'utf-8')}, '//Hello%20World!')

    def test_traversal(self):
        self.generates('/{x}*traverse', {'x': 'abc', 'traverse': ''}, '/abc')
        self.generates('/{x}*traverse', {'x': 'abc', 'traverse': '/def'}, '/abc/def')

    def test_multiple_parameters(self):
        self.generates('/foo/{id}/bar/{name}', {'id': '123', 'name': 'test'}, '/foo/123/bar/test')
        self.generates('/foo/{id}/{name}/{age}', {'id': '123', 'name': 'test', 'age': '30'}, '/foo/123/test/30')

    def test_invalid_parameters(self):
        with self.assertRaises(KeyError):
            self.generates('/{x}', {}, '/')
        with self.assertRaises(KeyError):
            self.generates('/{x}/{y}', {'x': 'foo'}, '/foo/')
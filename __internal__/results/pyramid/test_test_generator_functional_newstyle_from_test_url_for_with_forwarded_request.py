import unittest
from pyramid.urldispatch import _compile_route
from pyramid.util import text_

class TestCompileRouteFunctional(unittest.TestCase):
    def generates(self, pattern, dict, result):
        self.assertEqual(_compile_route(pattern)[1](dict), result)

    def test_edge_cases(self):
        self.generates('/{x}', {'x': None}, '/None')
        self.generates('/{x}', {'x': ' '}, '/ ')
        self.generates('/{x}', {'x': '123'}, '/123')
        self.generates('/{x}', {'x': 'special!@#'}, '/special!@#')
        self.generates('/{x}', {'x': 'a/b/c'}, '/a/b/c')
        self.generates('/{x}', {'x': 'a?b=c'}, '/a?b=c')
        self.generates('/{x}', {'x': 'a#b'}, '/a#b')
        self.generates('/{x}', {'x': 'a b'}, '/a%20b')
        self.generates('/{x}', {'x': text_(b'\xe9')}, '/%C3%A9')

    def test_traverse_cases(self):
        self.generates('/{x}*traverse', {'x': 'abc', 'traverse': 'def'}, '/abc/def')
        self.generates('/{x}*traverse', {'x': '', 'traverse': 'def'}, '/def')
        self.generates('/{x}*traverse', {'x': 'abc', 'traverse': ''}, '/abc')
        self.generates('/{x}*traverse', {'x': 'abc', 'traverse': '/def/ghi'}, '/abc/def/ghi')

    def test_invalid_cases(self):
        with self.assertRaises(TypeError):
            self.generates('/{x}', {'x': 123}, '/123')
        with self.assertRaises(KeyError):
            self.generates('/{x}', {}, '/')
        with self.assertRaises(ValueError):
            self.generates('/{x}', {'x': 'invalid'}, '/invalid')

    def test_special_characters(self):
        self.generates('/{x}', {'x': ':@&+$,'}, '/:@&+$,')
        self.generates('/{x}', {'x': 'a/b/c'}, '/a/b/c')
        self.generates('/{x}', {'x': ' '}, '/ ')
        self.generates('/{x}', {'x': '%20'}, '/%20')
import unittest
from pyramid.util import text_
from pyramid.urldispatch import _compile_route

class TestRouteGeneration(unittest.TestCase):

    def generates(self, pattern, dict, result):
        self.assertEqual(_compile_route(pattern)[1](dict), result)

    def test_generator_functional_edge_cases(self):
        self.generates('/:x', {'x': None}, '/None')
        self.generates('/:x', {'x': ' '}, '/ ')
        self.generates('/:x', {'x': '123'}, '/123')
        self.generates('/:x', {'x': 'special!@#'}, '/special!@#')
        self.generates('/:x', {'x': text_(b'\xe2\x9c\x94', 'utf-8')}, '/✓')
        self.generates('/:x', {'x': 'a/b/c'}, '/a/b/c')
        self.generates('/:x*traverse', {'x': 'a', 'traverse': 'b/c'}, '/a/b/c')
        self.generates('*traverse', {'traverse': ('',)}, '/')
        self.generates('*traverse', {'traverse': ('a',)}, '/a')
        self.generates('*traverse', {'traverse': ('a', 'b', 'c')}, '/a/b/c')
        self.generates('/foo/:id.html', {'id': ''}, '/foo/.html')
        self.generates('/foo/:id.html', {'id': '1234567890'}, '/foo/1234567890.html')
        self.generates('/foo/:id.html', {'id': text_(b'\xe2\x9c\x94', 'utf-8')}, '/foo/✓.html')
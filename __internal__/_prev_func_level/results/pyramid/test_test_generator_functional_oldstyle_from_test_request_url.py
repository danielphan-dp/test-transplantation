import unittest
from pyramid.urldispatch import _compile_route
from pyramid.util import text_

class TestCompileRouteFunctional(unittest.TestCase):
    def generates(self, pattern, dict, result):
        self.assertEqual(_compile_route(pattern)[1](dict), result)

    def test_generator_functional_edge_cases(self):
        self.generates('/:x', {'x': None}, '/None')
        self.generates('/:x', {'x': ' '}, '/ ')
        self.generates('/:x', {'x': '123'}, '/123')
        self.generates('/:x', {'x': 'test/test'}, '/test/test')
        self.generates('/:x', {'x': text_(b'La Pe\xc3\xb1a')}, '//La%20Pe%C3%B1a')
        self.generates('/:x', {'x': 'a/b/c'}, '/a/b/c')
        self.generates('/:x*traverse', {'x': 'abc', 'traverse': 'def/ghi'}, '/abc/def/ghi')
        self.generates('*traverse', {'traverse': ('', 'a', 'b', 'c')}, '/a/b/c')
        self.generates('/foo/:id', {'id': ''}, '/foo/')
        self.generates('/foo/:id', {'id': 'bar/baz'}, '/foo/bar/baz')
        self.generates('/foo/:id.html', {'id': None}, '/foo/None.html')
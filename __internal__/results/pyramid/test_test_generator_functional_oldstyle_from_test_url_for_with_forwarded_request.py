import unittest
from pyramid.urldispatch import _compile_route
from pyramid.util import text_

class TestCompileRouteFunctional(unittest.TestCase):
    def generates(self, pattern, dict, result):
        self.assertEqual(_compile_route(pattern)[1](dict), result)

    def test_generator_functional_edge_cases(self):
        self.generates('/:x', {'x': None}, '/')
        self.generates('/:x', {'x': ' '}, '/ ')
        self.generates('/:x', {'x': '123'}, '/123')
        self.generates('/:x', {'x': 'test/test'}, '/test/test')
        self.generates('/:x*traverse', {'x': 'test', 'traverse': 'path'}, '/test/path')
        self.generates('/:x*traverse', {'x': '', 'traverse': 'path'}, '/path')
        self.generates('/:x*traverse', {'x': 'test', 'traverse': None}, '/test')
        self.generates('/:x*traverse', {'x': 'test', 'traverse': ' '}, '/test/ ')
        self.generates('/foo/:id', {'id': None}, '/foo/')
        self.generates('/foo/:id', {'id': ''}, '/foo/')
        self.generates('/foo/:id', {'id': 'bar/baz'}, '/foo/bar/baz')
        self.generates('/foo/:id', {'id': text_(b'La Pe\xc3\xb1a')}, '/foo/La%20Pe%C3%B1a')
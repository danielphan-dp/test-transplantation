import unittest
from pyramid.urldispatch import _compile_route
from pyramid.util import text_

class TestCompileRouteFunctional(unittest.TestCase):
    def generates(self, pattern, dict, result):
        self.assertEqual(_compile_route(pattern)[1](dict), result)

    def test_generator_functional_edge_cases(self):
        self.generates('/{x}', {'x': None}, '/None')
        self.generates('/{x}', {'x': ' '}, '/ ')
        self.generates('/{x}', {'x': '123'}, '/123')
        self.generates('/{x}', {'x': 'foo/bar'}, '/foo/bar')
        self.generates('/{x}', {'x': 'a b'}, '/a%20b')
        self.generates('/{x}', {'x': 'a+b'}, '/a+b')
        self.generates('/{x}', {'x': 'a?b'}, '/a%3Fb')
        self.generates('/{x}', {'x': 'a#b'}, '/a%23b')
        self.generates('/{x}', {'x': 'a/b/c'}, '/a/b/c')
        self.generates('/{x}*traverse', {'x': 'a', 'traverse': 'b/c'}, '/a/b/c')
        self.generates('/foo/{id}', {'id': 'bar'}, '/foo/bar')
        self.generates('/foo/{id}', {'id': ''}, '/foo/')
        self.generates('/foo/{id}', {'id': '123'}, '/foo/123')
        self.generates('/foo/{id}', {'id': 'abc'}, '/foo/abc')
        self.generates('/foo/{id}', {'id': text_(b'/La Pe\xc3\xb1a')}, '/foo//La%20Pe%C3%B1a')
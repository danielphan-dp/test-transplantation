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
        self.generates('/:x', {'x': 'abc def'}, '/abc%20def')
        self.generates('/:x', {'x': text_(b'\xe2\x9c\x94', 'utf-8')}, '/%E2%9C%94')
        self.generates('/:x*traverse', {'x': 'abc', 'traverse': 'def/ghi'}, '/abc/def/ghi')
        self.generates('*traverse', {'traverse': ('',)}, '/')
        self.generates('*traverse', {'traverse': ('a',)}, '/a')
        self.generates('*traverse', {'traverse': ('a', 'b', 'c')}, '/a/b/c')
        self.generates('/foo/:id.html', {'id': ''}, '/foo/.html')
        self.generates('/foo/:id.html', {'id': 'bar baz'}, '/foo/bar%20baz.html')
        self.generates('/foo/:id.html', {'id': text_(b'\xe2\x9c\x94', 'utf-8')}, '/foo/%E2%9C%94.html')
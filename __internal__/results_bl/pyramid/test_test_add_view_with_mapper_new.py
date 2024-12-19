import os
import unittest
from pyramid.renderers import null_renderer
from pyramid.config import Configurator

class TestViewMethod(unittest.TestCase):

    def setUp(self):
        self.config = Configurator(autocommit=True)

    def test_view_returns_none(self):
        def view(context, request):
            return None

        self.config.add_view(view=view, renderer=null_renderer)
        view_callable = self.config.make_wsgi_app()
        self.assertIsNone(view_callable(None, None))

    def test_view_with_empty_context(self):
        def view(context, request):
            return 'Empty Context'

        self.config.add_view(view=view, renderer=null_renderer)
        view_callable = self.config.make_wsgi_app()
        self.assertEqual(view_callable({}, None), 'Empty Context')

    def test_view_with_invalid_request(self):
        def view(context, request):
            return 'Invalid Request'

        self.config.add_view(view=view, renderer=null_renderer)
        view_callable = self.config.make_wsgi_app()
        with self.assertRaises(TypeError):
            view_callable(None, 'invalid_request')

    def test_view_with_mapper_and_context(self):
        class Mapper:
            def __init__(self, **kw):
                self.__class__.kw = kw

            def __call__(self, view):
                return view

        def view(context, request):
            return 'OK with Mapper'

        self.config.add_view(view=view, mapper=Mapper, renderer=null_renderer)
        view_callable = self.config.make_wsgi_app()
        self.assertEqual(view_callable({}, None), 'OK with Mapper')
        self.assertEqual(Mapper.kw['mapper'], Mapper)

    def test_view_with_different_context(self):
        def view(context, request):
            return f'Context: {context}'

        self.config.add_view(view=view, renderer=null_renderer)
        view_callable = self.config.make_wsgi_app()
        self.assertEqual(view_callable('Test Context', None), 'Context: Test Context')
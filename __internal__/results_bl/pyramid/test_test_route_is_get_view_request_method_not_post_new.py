import os
import unittest
from pyramid.config import Configurator
from pyramid.renderers import null_renderer as nr
from pyramid.scripts.proutes import PRoutesCommand
from pyramid.registry import Registry
from pyramid.interfaces import IRouteRequest, IView, IViewClassifier
from pyramid.config import not_

class TestAddRoute(unittest.TestCase):

    def setUp(self):
        self.config = Configurator(autocommit=True)

    def test_add_route_with_get_method(self):
        def view1(context, request):  # pragma: no cover
            return 'view1'

        self.config.add_route('foo', '/a/b', request_method='GET')
        self.config.add_view(route_name='foo', view=view1, renderer=nr)

        command = PRoutesCommand()
        command.bootstrap = dummy.DummyBootstrap(registry=self.config.registry)
        result = command.run()
        self.assertEqual(result, 0)

    def test_add_route_with_post_method(self):
        def view2(context, request):  # pragma: no cover
            return 'view2'

        self.config.add_route('bar', '/c/d', request_method='POST')
        self.config.add_view(route_name='bar', view=view2, renderer=nr)

        command = PRoutesCommand()
        command.bootstrap = dummy.DummyBootstrap(registry=self.config.registry)
        result = command.run()
        self.assertEqual(result, 0)

    def test_add_route_with_invalid_method(self):
        def view3(context, request):  # pragma: no cover
            return 'view3'

        self.config.add_route('baz', '/e/f', request_method='INVALID')
        self.config.add_view(route_name='baz', view=view3, renderer=nr)

        command = PRoutesCommand()
        command.bootstrap = dummy.DummyBootstrap(registry=self.config.registry)
        result = command.run()
        self.assertEqual(result, 0)

    def test_add_route_without_method(self):
        def view4(context, request):  # pragma: no cover
            return 'view4'

        self.config.add_route('qux', '/g/h')
        self.config.add_view(route_name='qux', view=view4, renderer=nr)

        command = PRoutesCommand()
        command.bootstrap = dummy.DummyBootstrap(registry=self.config.registry)
        result = command.run()
        self.assertEqual(result, 0)

    def test_add_route_with_multiple_methods(self):
        def view5(context, request):  # pragma: no cover
            return 'view5'

        self.config.add_route('quux', '/i/j', request_method='GET, POST')
        self.config.add_view(route_name='quux', view=view5, renderer=nr)

        command = PRoutesCommand()
        command.bootstrap = dummy.DummyBootstrap(registry=self.config.registry)
        result = command.run()
        self.assertEqual(result, 0)
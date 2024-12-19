import unittest
from pyramid.httpexceptions import HTTPNotFound
from pyramid.interfaces import IRequest
from pyramid.renderers import null_renderer
from zope.interface import directlyProvides
from pyramid.testing import DummyRequest

class TestViewNotFound(unittest.TestCase):

    def setUp(self):
        self.config = self._makeOne(autocommit=True)

    def test_view_not_found_with_none_request(self):
        view = lambda *arg: 'OK'
        self.config.add_view(
            view=view,
            request_type='pyramid.interfaces.IRequest',
            renderer=null_renderer,
        )
        wrapper = self._getViewCallable(self.config)
        request = None
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, None, request)

    def test_view_not_found_with_invalid_request(self):
        view = lambda *arg: 'OK'
        self.config.add_view(
            view=view,
            request_type='pyramid.interfaces.IRequest',
            renderer=null_renderer,
        )
        wrapper = self._getViewCallable(self.config)
        request = DummyRequest()
        directlyProvides(request, IRequest)
        result = wrapper(None, request)
        self.assertEqual(result, 'OK')

        # Test with an invalid argument
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, 'invalid_arg', request)

    def test_view_not_found_with_missing_view(self):
        view = lambda *arg: 'OK'
        self.config.add_view(
            view=view,
            request_type='pyramid.interfaces.IRequest',
            renderer=null_renderer,
        )
        wrapper = self._getViewCallable(self.config)
        request = DummyRequest()
        directlyProvides(request, IRequest)
        
        # Test with a missing view
        self.config.add_view(view=None, request_type='pyramid.interfaces.IRequest')
        with self.assertRaises(HTTPNotFound):
            self._assertNotFound(wrapper, None, request)
import pathlib
import pytest
from aiohttp import web
from typing import Callable, List

@pytest.fixture
def router() -> web.UrlDispatcher:
    return web.UrlDispatcher()

@pytest.fixture
def fill_routes(router: web.UrlDispatcher) -> Callable[[], List[web.AbstractRoute]]:
    def go() -> List[web.AbstractRoute]:
        route1 = router.add_route('GET', '/plain', make_handler())
        route2 = router.add_route('GET', '/variable/{name}', make_handler())
        resource = router.add_static('/static', pathlib.Path(aiohttp.__file__).parent)
        return [route1, route2] + list(resource)
    return go

def test_routes_view_len(router: web.UrlDispatcher, fill_routes: Callable[[], List[web.AbstractRoute]]) -> None:
    fill_routes()
    assert 4 == len(router.routes())

def test_add_route_with_invalid_method(router: web.UrlDispatcher) -> None:
    with pytest.raises(ValueError):
        router.add_route('INVALID_METHOD', '/invalid', make_handler())

def test_add_static_route(router: web.UrlDispatcher) -> None:
    static_route = router.add_static('/static', pathlib.Path(aiohttp.__file__).parent)
    assert static_route is not None
    assert len(router.routes()) == 1

def test_variable_route(router: web.UrlDispatcher, fill_routes: Callable[[], List[web.AbstractRoute]]) -> None:
    fill_routes()
    request = web.Request(web.abc.HTTPVersion, 'GET', '/variable/test')
    route = router.match(request)
    assert route is not None
    assert route.handler is not None

def test_route_not_found(router: web.UrlDispatcher) -> None:
    request = web.Request(web.abc.HTTPVersion, 'GET', '/nonexistent')
    route = router.match(request)
    assert route is None

def test_multiple_routes(router: web.UrlDispatcher, fill_routes: Callable[[], List[web.AbstractRoute]]) -> None:
    fill_routes()
    assert len(router.routes()) == 4
    assert any(route.path == '/plain' for route in router.routes())
    assert any(route.path == '/variable/{name}' for route in router.routes())
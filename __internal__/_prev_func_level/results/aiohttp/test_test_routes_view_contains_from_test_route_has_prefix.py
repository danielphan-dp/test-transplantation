import pathlib
from typing import Callable, List
import pytest
from aiohttp import web

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

def test_routes_view_contains(router: web.UrlDispatcher, fill_routes: Callable[[], List[web.AbstractRoute]]) -> None:
    routes = fill_routes()
    for route in routes:
        assert route in router.routes()

def test_route_with_invalid_method(router: web.UrlDispatcher) -> None:
    with pytest.raises(ValueError):
        router.add_route('INVALID_METHOD', '/invalid', make_handler())

def test_route_with_empty_path(router: web.UrlDispatcher) -> None:
    with pytest.raises(ValueError):
        router.add_route('GET', '', make_handler())

def test_route_with_static_file(router: web.UrlDispatcher, fill_routes: Callable[[], List[web.AbstractRoute]]) -> None:
    routes = fill_routes()
    static_route = next(route for route in routes if route.path == '/static')
    assert static_route is not None
    assert static_route.method == 'GET'

def test_route_variable_name(router: web.UrlDispatcher, fill_routes: Callable[[], List[web.AbstractRoute]]) -> None:
    routes = fill_routes()
    variable_route = next(route for route in routes if route.path == '/variable/{name}')
    assert variable_route is not None
    assert variable_route.method == 'GET'
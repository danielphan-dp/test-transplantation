import pytest
from aiohttp import web
from typing import Callable, List

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

def test_routes_view_empty_router(router: web.UrlDispatcher) -> None:
    assert len(router.routes()) == 0

def test_routes_view_static_route(router: web.UrlDispatcher, fill_routes: Callable[[], List[web.AbstractRoute]]) -> None:
    routes = fill_routes()
    static_route = next((route for route in routes if route.path == '/static'), None)
    assert static_route is not None
    assert static_route.method == 'GET'

def test_routes_view_variable_route(router: web.UrlDispatcher, fill_routes: Callable[[], List[web.AbstractRoute]]) -> None:
    routes = fill_routes()
    variable_route = next((route for route in routes if route.path == '/variable/{name}'), None)
    assert variable_route is not None
    assert variable_route.method == 'GET'

def test_routes_view_invalid_method(router: web.UrlDispatcher, fill_routes: Callable[[], List[web.AbstractRoute]]) -> None:
    routes = fill_routes()
    invalid_route = router.add_route('POST', '/plain', make_handler())
    assert invalid_route not in routes

def test_routes_view_duplicate_route(router: web.UrlDispatcher, fill_routes: Callable[[], List[web.AbstractRoute]]) -> None:
    fill_routes()
    duplicate_route = router.add_route('GET', '/plain', make_handler())
    assert duplicate_route not in router.routes()
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

def test_routes_view_iter(router: web.UrlDispatcher, fill_routes: Callable[[], List[web.AbstractRoute]]) -> None:
    routes = fill_routes()
    assert list(routes) == list(router.routes())

def test_empty_router(router: web.UrlDispatcher) -> None:
    assert list(router.routes()) == []

def test_single_route(router: web.UrlDispatcher) -> None:
    router.add_route('GET', '/test', make_handler())
    assert len(router.routes()) == 1
    assert router.routes()[0].path == '/test'

def test_static_route(router: web.UrlDispatcher, fill_routes: Callable[[], List[web.AbstractRoute]]) -> None:
    fill_routes()
    static_routes = [route for route in router.routes() if isinstance(route, web.StaticResource)]
    assert len(static_routes) > 0

def test_variable_route(router: web.UrlDispatcher, fill_routes: Callable[[], List[web.AbstractRoute]]) -> None:
    fill_routes()
    variable_route = next((route for route in router.routes() if '{name}' in route.path), None)
    assert variable_route is not None
    assert variable_route.method == 'GET'

def test_route_order(router: web.UrlDispatcher, fill_routes: Callable[[], List[web.AbstractRoute]]) -> None:
    routes = fill_routes()
    assert routes[0].path == '/plain'
    assert routes[1].path == '/variable/{name}'
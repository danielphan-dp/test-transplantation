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

def test_routes_count(router: web.UrlDispatcher, fill_routes: Callable[[], List[web.AbstractRoute]]) -> None:
    routes = fill_routes()
    assert len(routes) == 3  # Expecting 2 routes and 1 static resource

def test_route_methods(router: web.UrlDispatcher, fill_routes: Callable[[], List[web.AbstractRoute]]) -> None:
    routes = fill_routes()
    assert all(route.method in ['GET', 'HEAD'] for route in routes)

def test_static_route_exists(router: web.UrlDispatcher, fill_routes: Callable[[], List[web.AbstractRoute]]) -> None:
    routes = fill_routes()
    static_routes = [route for route in routes if isinstance(route, web.StaticResource)]
    assert len(static_routes) == 1
    assert static_routes[0].path == '/static'

def test_variable_route_match(router: web.UrlDispatcher, fill_routes: Callable[[], List[web.AbstractRoute]]) -> None:
    routes = fill_routes()
    variable_route = next(route for route in routes if '/variable/' in route.path)
    assert variable_route.path == '/variable/{name}'

def test_route_names(router: web.UrlDispatcher, fill_routes: Callable[[], List[web.AbstractRoute]]) -> None:
    routes = fill_routes()
    names = {route.name for route in routes if route.name is not None}
    assert len(names) == 0  # Assuming no names are assigned in fill_routes

def test_empty_routes(router: web.UrlDispatcher) -> None:
    assert len(router.routes()) == 0  # Ensure router starts empty

def test_duplicate_route_error(router: web.UrlDispatcher) -> None:
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Hello")
    
    router.add_route('GET', '/duplicate', handler)
    with pytest.raises(RuntimeError):
        router.add_route('GET', '/duplicate', handler)  # Adding duplicate route should raise error
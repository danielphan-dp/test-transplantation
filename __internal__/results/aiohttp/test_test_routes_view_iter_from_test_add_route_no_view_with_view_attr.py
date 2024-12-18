import pathlib
import pytest
from aiohttp import web
from aiohttp.web_urldispatcher import UrlDispatcher

@pytest.fixture
def router() -> UrlDispatcher:
    return UrlDispatcher()

@pytest.fixture
def fill_routes(router: web.UrlDispatcher) -> Callable[[], List[web.AbstractRoute]]:
    def go() -> List[web.AbstractRoute]:
        route1 = router.add_route('GET', '/plain', make_handler())
        route2 = router.add_route('GET', '/variable/{name}', make_handler())
        resource = router.add_static('/static', pathlib.Path(aiohttp.__file__).parent)
        return [route1, route2] + list(resource)
    return go

def test_fill_routes(router: web.UrlDispatcher, fill_routes: Callable[[], List[web.AbstractRoute]]) -> None:
    routes = fill_routes()
    assert len(routes) == 3  # Expecting 2 routes and 1 static resource
    assert any(route.path == '/plain' for route in routes)
    assert any(route.path == '/variable/{name}' for route in routes)
    assert any(route.path == '/static' for route in routes)

def test_route_methods(router: web.UrlDispatcher, fill_routes: Callable[[], List[web.AbstractRoute]]) -> None:
    routes = fill_routes()
    assert all(route.method == 'GET' for route in routes[:2])  # Check methods for the first two routes

def test_static_resource(router: web.UrlDispatcher, fill_routes: Callable[[], List[web.AbstractRoute]]) -> None:
    routes = fill_routes()
    static_route = next(route for route in routes if route.path == '/static')
    assert static_route.handler is not None  # Ensure static resource has a handler

def test_route_names(router: web.UrlDispatcher, fill_routes: Callable[[], List[web.AbstractRoute]]) -> None:
    routes = fill_routes()
    assert all(route.name is None for route in routes)  # Ensure no names are assigned

def test_empty_router(router: web.UrlDispatcher) -> None:
    assert len(router.routes()) == 0  # Ensure router is empty initially

def test_duplicate_route_addition(router: web.UrlDispatcher) -> None:
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="Hello")

    router.add_route('GET', '/duplicate', handler)
    with pytest.raises(RuntimeError):
        router.add_route('GET', '/duplicate', handler)  # Ensure adding the same route raises an error
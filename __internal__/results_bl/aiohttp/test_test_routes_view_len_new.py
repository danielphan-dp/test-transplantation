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

def test_routes_view_len(router: web.UrlDispatcher, fill_routes: Callable[[], List[web.AbstractRoute]]) -> None:
    fill_routes()
    assert 4 == len(router.routes())

def test_routes_view_contains_plain_route(router: web.UrlDispatcher, fill_routes: Callable[[], List[web.AbstractRoute]]) -> None:
    fill_routes()
    assert any(route.path == '/plain' for route in router.routes())

def test_routes_view_contains_variable_route(router: web.UrlDispatcher, fill_routes: Callable[[], List[web.AbstractRoute]]) -> None:
    fill_routes()
    assert any(route.path == '/variable/{name}' for route in router.routes())

def test_routes_view_contains_static_route(router: web.UrlDispatcher, fill_routes: Callable[[], List[web.AbstractRoute]]) -> None:
    fill_routes()
    assert any(route.path.startswith('/static') for route in router.routes())

def test_routes_view_empty_router(router: web.UrlDispatcher) -> None:
    assert 0 == len(router.routes())

def test_routes_view_multiple_calls(router: web.UrlDispatcher, fill_routes: Callable[[], List[web.AbstractRoute]]) -> None:
    fill_routes()
    fill_routes()
    assert 4 == len(router.routes())  # Ensure routes are not duplicated

def test_routes_view_invalid_method(router: web.UrlDispatcher, fill_routes: Callable[[], List[web.AbstractRoute]]) -> None:
    fill_routes()
    with pytest.raises(web.HTTPMethodNotAllowed):
        router.add_route('POST', '/plain', make_handler())  # Testing invalid method for existing route
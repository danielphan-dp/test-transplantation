import pytest
from connexion.operations import OpenAPIOperation
from connexion.resolver import MethodViewResolver

@pytest.fixture(scope='session', params=METHOD_VIEW_RESOLVERS)
def method_view_resolver(request):
    return request.param

def test_methodview_resolve_with_invalid_controller(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="/hello",
        path_parameters=[],
        operation={
            "x-openapi-router-controller": "invalidapi.controller",
        },
        components=COMPONENTS,
        resolver=method_view_resolver("invalidapi"),
    )
    assert operation.operation_id is None

def test_methodview_resolve_with_no_controller(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="/hello",
        path_parameters=[],
        operation={},
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id is None

def test_methodview_resolve_with_different_http_method(method_view_resolver):
    operation = OpenAPIOperation(
        method="POST",
        path="/hello",
        path_parameters=[],
        operation={
            "x-openapi-router-controller": "fakeapi.pets",
        },
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id == "fakeapi.PetsView.create"

def test_methodview_resolve_with_multiple_controllers(method_view_resolver):
    operation = OpenAPIOperation(
        method="GET",
        path="/hello",
        path_parameters=[],
        operation={
            "x-openapi-router-controller": "fakeapi.pets",
            "x-openapi-router-controller": "fakeapi.animals",
        },
        components=COMPONENTS,
        resolver=method_view_resolver("fakeapi"),
    )
    assert operation.operation_id == "fakeapi.PetsView.search" or operation.operation_id == "fakeapi.AnimalsView.search"